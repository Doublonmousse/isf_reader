meta:
  id: isf_format
  endian: be
doc: tentative to read the whole of the isf format using ksy
seq:
  - id: hdr
    doc: header
    type: header
  - id: stream_size
    type: multibyte_int_decoded
  - id: isf_tag
    type: table_element
    repeat: eos

types:
  header:
    seq:
    - id: isf_version
      type: u1
      doc: This SHOULD be 0, abort otherwise (wrong version otherwise)
  multibyte_int:
    seq:
    - id: int_value
      type: u1
      repeat: until
      repeat-until: _ & 0b1000_0000 == 0
  multibyte_int_signed:
    doc: This is the same as multibyte_int as far as parsing goes
      But there is some difference in how to read the output value
      For now we don't decode it with the multibyte_int_decoded
      instance as this isn't needed
    seq:
    - id: int_value
      type: u1
      repeat: until
      repeat-until: _ & 0b1000_0000 == 0
  table_element:
    seq:
    - id: isf_tag
      type: u1
      enum: tag_table
    - id: content
      type:
        switch-on: isf_tag
        cases:
          'tag_table::tag_ink_space_rect': ink_space_rect
          'tag_table::tag_guid_table' : guid_table
          'tag_table::tag_himetric_size': himetric_size
          'tag_table::tag_buttons': unread_tag
          'tag_table::tag_draw_attrs_table': tag_draw_attrs_table
          'tag_table::tag_draw_attrs_block': tag_draw_attrs_block 
          'tag_table::tag_stroke_desc_block': tag_stroke_desc_block
          'tag_table::tag_metric_block': metric_block
          'tag_table::tag_stroke': stroke
          'tag_table::tag_didx': didx
          'tag_table::tag_transform_and_scale': transform_and_scale
          _: custom_guid
  didx:
    seq:
    - id: value
      type: multibyte_int_decoded
  transform_and_scale:
    seq:
    - id: values
      type: f4le
      repeat: expr
      repeat-expr: 4
  unread_tag:
   seq:
    - id: header
      type: multibyte_int_decoded
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: header.value
  custom_guid:
    seq:
    - id: tag
      type: multibyte_int_decoded
      doc: if there is a tag, we have to read it from the stream
    - id: info
      type: u1
      repeat: expr
      repeat-expr: 4
      doc: For a guid with known size (105/3), we know to read 4 bytes
         there is a table of guid to size in the isf spec
    doc: To affine to really take into account all guids
      Here we suppose the isf_tag == 105 .. 
  tag_draw_attrs_block:
    seq:
    - id: header
      type: multibyte_int_decoded
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: header.value
  ink_space_rect:
    seq:
    - id: left_d
      type: multibyte_int_decoded
    - id: top_d
      type: multibyte_int_decoded
    - id: right_d
      type: multibyte_int_decoded
    - id: bottom_d
      type: multibyte_int_decoded
    instances:
      left:
        value: left_d.value_signed
      top:
        value: top_d.value_signed
      right:
        value: right_d.value_signed
      bottom:
        value: bottom_d.value_signed
  stroke:
    seq:
    - id: cb_stroke
      type: multibyte_int_decoded
    - id: cpoints
      type: multibyte_int_decoded
    - id: compressed_data
      type: u1
      repeat: expr
      repeat-expr: cb_stroke.value - cpoints.len
  packed_data:
    doc: This is only used to show the format used for stroke packing
      This is not used in practice in the file
    params:
    - id: cb_stroke
      type: multibyte_int_decoded
    - id: cpoints
      type: multibyte_int_decoded 
    seq:
    - id: compression_id
      type: u1
      doc: | 
        Should be read to know the type of compression. 
        We'll assume default here. As we are dealing with
        Stroke data, should be PROPERTY_BIT_PACK_LONG 
        with _signed_ values ? maybe need to look at the code
        in more detail to really understand what is done
        at the lowest level
    - id: compressed_data
      type:
        switch-on: compression_type
        cases:
          0x00: uncompressed(cb_stroke.value - cpoints.len - 1)
          0x80: huffman(cb_stroke.value - cpoints.len - 1, 
            compression_id & 0b00011111)
    instances:
      compression_type:
        value: compression_id & 0b11000000
  huffman:
    params:
    - id: n_bytes
      type: u4
    - id: codec
      type: u1
    seq:
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: n_bytes
    instances:
      codec_f:
        value: codec
        doc: |
          This is the index to point to in the huffman precalculated tables. ONLY TRUE FOR THE FIRST
          LIST
  uncompressed:
    params:
    - id: n_bytes
      type: u4
    seq:
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: n_bytes
  metric_block:
    seq:
    - id: header
      type: multibyte_int_decoded
    #- id: metric_element
    #  type: single_metric_element
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: header.value
      doc: Array of tag/size then a list of bytes to decode until header.value bytes are read
  single_metric_element:
    seq:
    - id: tag
      type: multibyte_int_decoded
      doc: tag that corresponds to the property of interest
    - id: payload_size
      type: multibyte_int_decoded
    - id: min
      type: multibyte_int_decoded
    - id: max
      type: multibyte_int_decoded
    - id: unit
      type: u1
    - id: resolution
      type: f4
      doc: may be == 0 ?
  himetric_size:
    seq:
    - id: header
      type: multibyte_int_decoded
    - id: himetric_size_x
      type: multibyte_int_decoded
    - id: himetric_size_y
      type: multibyte_int_decoded
    instances: # pulling the value out for convenience
      size_x:
        value: himetric_size_x.value_signed
      size_y:
        value: himetric_size_y.value_signed
  guid_table:
    seq:
    - id: header
      type: multibyte_int_decoded
    - id : guids
      type: guid_el
      repeat: expr
      repeat-expr: header.value / 16
  guid_el:
    seq:
    - id: tag
      type: u4
    - id: b1
      type: u2
    - id: b2
      type: u2
    - id: ch_list
      type: u1
      repeat: expr
      repeat-expr: 8
  tag_stroke_desc_block:
    seq:
    - id: size_total
      type: multibyte_int_decoded
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: size_total.value
    #- id: descriptor_blocks
    #  type: descriptor_block
  descriptor_block:
    seq:
    - id: tag
      type: u1
    - id: content
      type: 
        switch-on: tag
        cases:
          56: buttons 
          #61: stroke_properties_list
  buttons:
    seq:
    - id: nof_buttons
      type: multibyte_int_decoded
      doc: no way is there > 255 buttons right ?
  tag_draw_attrs_table:
    doc: |
      This is a block that can ONLY be decoded once
    seq:
      - id: size_total
        type: multibyte_int_decoded
        doc: Size in bytes of the full tag draw attr table content
      - id: draw_attributes_list
        type: read_until_draw_attrs(size_total.value)
      #  doc: TODO, repeat until we get to the size_total.value (in the DRAW ATTRIBUTE element)
  read_until_draw_attrs:
    params:
    - id: n_bytes_total
      type: u4
    seq:
    - id: draw_attr
      type: |
        draw_attr(_index == 0 ? n_bytes_total : draw_attr[_index -1].interm_value)
      repeat: until
      repeat-until: _.interm_value == 0
    types:
      draw_attr:
        params:
        - id: prev_bytes_left
          type: u4
        seq:
        - id: size
          type: multibyte_int_decoded
        - id: drawing_properties
          type: drawing_properties(size.value)
        instances:
          interm_value:
            value: prev_bytes_left - size.value - size.len
  drawing_properties:
    params:
    - id: size
      type: u4
    seq:
    - id: tag
      type: multibyte_int_decoded
      doc: value for that guid. Here this is unchecked but in practice we should match that tag with the guid (fixed + custom) present
    - id: drawing_attribute
      type: 
        switch-on: tag.value
        cases:
          #72: drawing_flags #72-50 so 22 in original index
          # also got 100 but nothing is said for 100- 50 = 50 ..
          # should still be known ?
          _: skip(size - tag.len)
  skip:
    params:
    - id: size
      type: u4
    seq:
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: size
  drawing_flags:
    seq:
    - id: drawing_flag
      type: multibyte_int_decoded
      doc: |
        Get the int out, and use the masks from 
        https://source.dot.net/#PresentationCore/MS/Internal/Ink/DrawingFlags.cs,6b5b5b1c32977bf7,references
        To know what flags are set
  da_pen_tip:
    seq:
    - id: pen_tip_type
      type: u1
  multibyte_int_decoded:
    doc: |
      Extracted from https://github.com/kaitai-io/kaitai_struct_formats/blob/5f37c8178a631ae1d50e044be7af58dced0d0b69/common/vlq_base128_le.ksy#L11
      Not sure I understand everything happenning here but it works !
      At least for now, maybe needs to be read attentively to understand/adapt to our usecase
    seq:
      - id: groups
        type: |
          group(
            _index,
            _index != 0 ? groups[_index - 1].interm_value : 0,
            _index != 0 ? (_index == 9 ? 0x8000_0000_0000_0000 : groups[_index - 1].multiplier * 128) : 1
          )
        repeat: until
        repeat-until: not _.has_next
    types:
      group:
        doc: |
          One byte group, clearly divided into 7-bit "value" chunk and 1-bit "continuation" flag.
        params:
          - id: idx
            type: s4
          - id: prev_interm_value
            type: u8
          - id: multiplier
            type: u8
        seq:
          - id: has_next
            type: b1
            valid: 'idx == 9 ? false : has_next'
          - id: value
            type: b7
            valid:
              max: '(idx == 9 ? 1 : 0b111_1111).as<u8>'
            doc: |
              The 7-bit (base128) numeric value chunk of this group

              Since this implementation only supports integer values up to 64 bits,
              the `value` in the 10th group (`groups[9]`) can only be `0` or `1`
              (otherwise the width of the represented value would be 65 bits or
              more, which is not supported).
        instances:
          interm_value:
            value: (prev_interm_value + value * multiplier).as<u8>
            doc: was previously cast as u8 with a
    instances:
      len:
        value: groups.size
      value:
        value: groups.last.interm_value
        doc: Resulting unsigned value as normal integer
      value_signed:
        value: '(value & 0x01 > 0) ? (-value>>1) : value>>1'

enums:
  tag_table:
    0: tag_ink_space_rect
    1: tag_guid_table
    2: tag_draw_attrs_table
    3: tag_draw_attrs_block
    5: tag_stroke_desc_block
    6: tag_buttons
    9: tag_didx
    10: tag_stroke
    21: tag_transform_and_scale
    25: tag_metric_block
    29: tag_himetric_size
  guid_enum:
    72: transform_quad
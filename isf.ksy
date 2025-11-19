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
          'tag_table::tag_draw_attrs_table': tag_draw_attrs_table
          'tag_table::tag_draw_attrs_block': tag_draw_attrs_block 
          'tag_table::tag_stroke_desc_table': tag_stroke_desc_table
          'tag_table::tag_stroke_desc_block': tag_stroke_desc_block
          'tag_table::tag_didx': didx
          'tag_table::tag_stroke': stroke
          'tag_table::stroke_descriptor_table_index': stroke_descriptor_table_index
          'tag_table::compression_header': compression_header

          'tag_table::transform': transform
          'tag_table::transform_isotropic_scale': transform_isotropic_scale
          'tag_table::transform_anisotropic_scale': transform_anisotropic_scale
          'tag_table::transform_rotate': transform_rotate
          'tag_table::transform_translate': transform_translate
          'tag_table::tag_transform_and_scale': transform_and_scale

          'tag_table::transform_table_index': transform_table_index

          'tag_table::tag_metric_block': metric_block
          'tag_table::tag_metric_table_index': metric_table_index
          'tag_table::persistence_format': persistence_format
          'tag_table::tag_himetric_size': himetric_size
          'tag_table::stroke_ids': stroke_ids
          _: custom_guid_tagged
  tag_stroke_desc_table:
    seq:
    - id: size
      type: multibyte_int_decoded
    - id: stroke_descriptor_block_list
      type: stroke_descriptor_block_list
      size: size.value
  stroke_descriptor_block_list:
    seq:
    - id: stroke_descriptor_block_list
      type: tag_stroke_desc_block
      repeat: eos
  didx:
    seq:
    - id: value
      type: multibyte_int_decoded
    instances:
      new_index:
        value: value.value
  compression_header:
    doc: unused in the format so skipped
    seq:
    - id: size
      type: multibyte_int_decoded
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: size.value
  transform:
    seq:
    - id: scale_x_himetric
      type: f4le
    - id: scale_y_himetric
      type: f4le
    - id: shear_x
      type: f4le
    - id: shear_y
      type: f4le
    - id: dx
      type: f4le
    - id: dy
      type: f4le
    instances:
      scale_x_px:
        value: scale_x_himetric / 26.4572454037811
      scale_y_py:
        value: scale_y_himetric / 26.4572454037811
  transform_isotropic_scale:
    seq:
    - id: scale
      type: f4le
  transform_anisotropic_scale:
    seq:
    - id: scale_x_himetric
      type: f4le
    - id: scale_y_himetric
      type: f4le
    instances:
      scale_x_px:
        value: scale_x_himetric / 26.4572454037811
      scale_y_py:
        value: scale_y_himetric / 26.4572454037811
  transform_rotate:
    seq:
    - id: rotate_amount
      type: f4le
    instances:
      rotate:
        value: rotate_amount / 100
  transform_translate:
    seq:
    - id: dx
      type: f4le
    - id: dy
      type: f4le
  persistence_format:
    seq:
    - id: size
      type: multibyte_int_decoded
    - id: format
      type: multibyte_int_decoded
    instances:
      is_gif: 
        value: format.value & 0x00000001
  stroke_ids:
    doc: This is neither used in libisf-qt nor the official C# impl
    seq:
    - id: size
      type: multibyte_int_decoded
    - id: nof_ids
      type: multibyte_int_decoded
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: size.value - nof_ids.len
  metric_table_index:
    seq: 
    - id: size
      type: multibyte_int_decoded
    - id: index
      type: multibyte_int_decoded
  transform_table_index:
    seq: 
    - id: size
      type: multibyte_int_decoded
    - id: index
      type: multibyte_int_decoded
  stroke_descriptor_table_index:
    seq:
    - id: value
      type: multibyte_int_decoded
    instances:
      new_index:
        value: value.value
  transform_and_scale:
    seq:
    - id: scale_x_himetric
      type: f4le
    - id: scale_y_himetric
      type: f4le
    - id: dx
      type: f4le
    - id: dy
      type: f4le
    instances:
      scale_x_px: 
        value: scale_x_himetric / 26.4572454037811
      scale_y_px:
        value: scale_y_himetric / 26.4572454037811
  unread_tag:
   seq:
    - id: header
      type: multibyte_int_decoded
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: header.value
  tag_draw_attrs_block:
    seq:
    - id: header
      type: multibyte_int_decoded
    - id: drawing_properties
      type: drawing_properties_list(header.value)
      size: header.value
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
  metric_block:
    seq:
    - id: header
      type: multibyte_int_decoded
    - id: metric_element_list
      type: metric_element_list
      size: header.value
  metric_element_list:
    seq:
    - id: metric_element
      type: single_metric_element
      repeat: eos
  single_metric_element:
    seq:
    - id: tag
      type: multibyte_int_decoded
      doc: tag that corresponds to the property of interest
    - id: payload_size
      type: multibyte_int_decoded
    - id: metric_values
      type: metric_values(payload_size.value)
      size: payload_size.value
    instances:
      tag_v:
        value: tag.value
        enum: tags_stroke_desc
  metric_values:
    doc: |
      metric blocks always have the min value. The rest are optional, and we either have
      - min
      - min,max
      - min,max,unit
      - min,max,unit,resolution
    params:
      - id: size
        type: u4
    seq:
      - id: min
        type: multibyte_int_decoded
        doc: the min is in min.value_signed
      - id: max
        type: multibyte_int_decoded
        if: min.len < size
        doc: the max is in max.value_signed
      - id: unit
        type: u1
        enum: metric_scale
        if: min.len + max.len < size
      - id: resolution
        type: f4le
        if: min.len + max.len + 1 + 4 == size
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
    - id: descriptor_blocks
      type: descriptor_block_list
      size: size_total.value
  descriptor_block_list:
    seq:
    - id: descriptor
      type: descriptor_block
      repeat: eos
  descriptor_block:
    seq:
    - id: tag
      type: u1
    - id: content
      type: 
        switch-on: tag
        cases:
          # not checked : 6 for buttons (special case) TODO
          11: stroke_property_list
          _: add_tag(tag)
  add_tag:
    params:
    - id: tag
      type: u4
    doc: This is the case where we just add the tag to the list 
    seq: []
    instances:
      tag_value:
        value: tag
        enum: tags_stroke_desc
  stroke_property_list:
    seq:
     - id: tags
       type: multibyte_int_decoded
       repeat: eos
  tag_draw_attrs_table:
    doc: |
      This is a block that can ONLY be decoded once
    seq:
      - id: size_total
        type: multibyte_int_decoded
        doc: Size in bytes of the full tag draw attr table content
      - id: draw_attributes_list
        type: read_until_draw_attrs(size_total.value)
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
        - id: drawing_properties_list
          type: drawing_properties_list(size.value)
          size: size.value
        instances:
          interm_value:
            value: prev_bytes_left - size.value - size.len
  drawing_properties_list:
    params:
    - id: size
      type: u4
    doc: |
      Correspond to a call to DrawingAttributeSerializer.DecodeAsISF(strm, guidList, cbDA, attributes)
      With cbDA corresponding to size here.
      Each drawing attribute is a list of tags that each update/set a different field.
      Beware here that we ONLY have the tag and no size indicator so we need to know all tag-> size
      correspondances correctly and/or jump/skip to the end to preserve the alignment to the next tag.
      Ref : https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/DrawingAttributeSerializer.cs,111
    seq:
    - id: drawing_properties
      type: drawing_property_bounded(size)
      repeat: eos
    types:
      drawing_property_bounded:
        params:
        - id: prev_bytes_left
          type: u4
        seq:
        - id: tag
          type: u1
          doc: Pretty sure we are on 1 byte for tags ...
        - id: drawing_attribute
          type: 
            switch-on: tag
            cases:
              27: mantissa

              # 50 : start of the drawing attributes list

              # TODO

              65: roll_rotation
              68: color_ref
              69: pen_width
              70: pen_width # actually pen height 
              71: da_pen_tip
              72: drawing_flags

              # TODO

              80: transparency

              87: raster_operation
              
              100: custom_guid_tagged
              101: custom_guid_tagged
              102: custom_guid_tagged
              103: custom_guid_tagged
              104: custom_guid_tagged
              105: custom_guid_tagged
              106: custom_guid_tagged
              107: custom_guid_tagged
              108: custom_guid_tagged
              109: custom_guid_tagged
              110: custom_guid_tagged
              111: custom_guid_tagged
              112: custom_guid_tagged
              113: custom_guid_tagged
              114: custom_guid_tagged
              115: custom_guid_tagged
              116: custom_guid_tagged
              117: custom_guid_tagged
              118: custom_guid_tagged
              119: custom_guid_tagged
              120: custom_guid_tagged
              121: custom_guid_tagged
              122: custom_guid_tagged
              123: custom_guid_tagged
              124: custom_guid_tagged
              125: custom_guid_tagged
              126: custom_guid_tagged
              127: custom_guid_tagged

              _: skip(0) # because we choose to skip 0, we'd be okay unless we trip on the tag
  skip:
    params:
    - id: size_jump
      type: u4
    seq:
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: size_jump
  transparency:
    seq:
    - id: transparency_value
      type: multibyte_int_decoded
  roll_rotation:
    doc: tag 65, extended prop with size from https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/ISFTagAndGuidCache.cs,71
    seq:
    - id: unread
      type: u2
      doc: size of ushort
  custom_guid_tagged:
    doc: Corresponds to https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/CustomAttributeSerializer.cs,440
     Starts at 100 included(?) https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/ISFTagAndGuidCache.cs,175
    seq:
    - id: size
      type: multibyte_int_decoded
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: size.value + 1
      doc: |
        This corresponds to extended properties, that are encoded/compressed ...We suppose a u1 is added for the compression 
        header. 
        For the +1, see
        https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/CustomAttributeSerializer.cs,445
        We are _fine_ for now because
        - it is custom guids we may not read or know the content therein
        - the size is the compressed one so we can jump without having to decompress
  drawing_flags:
    doc: See https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/DrawingAttributeSerializer.cs,446 ?
      It's not apparent at a first read what all of the bytes actually do (there are more than the flags shown here)
    seq:
    - id: drawing_flag
      type: multibyte_int_decoded
      doc: |
        Get the int out, and use the masks from 
        https://source.dot.net/#PresentationCore/MS/Internal/Ink/DrawingFlags.cs,6b5b5b1c32977bf7,references
        To know what flags are set
    instances:
      fit_to_curve:
        value: (drawing_flag.value & 0x0001) >0
        doc: The stroke should be fit to a curve, such as a bezier.
      subtractive_transparency:
        value: (drawing_flag.value & 0x0002) > 0
        doc: |
          The stroke should be rendered by subtracting its rendering values
          from those on the screen
      ignore_pressure:
        value: (drawing_flag.value & 0x0004) > 0
        doc: Ignore any stylus pressure information when rendering
      is_highligher:
        value: (drawing_flag.value & 0x0100) > 0
  color_ref:
    seq:
    - id: encoded_bgr
      type: multibyte_int_decoded
      doc: The rgb value is encoded on a multibyte int. So for black we have 4 bytes !!
        We read the multibyte then reconvert to the correct values
    instances:
      blue: 
        value: (encoded_bgr.value & 0xFF)
      green:
        value: ((encoded_bgr.value & 0xff00) >> 8)
      red:
        value: ((encoded_bgr.value & 0xff0000) >> 16)
  pen_width:
    seq:
    - id: encoded_width
      type: multibyte_int_decoded
    instances:
      pen_width_himetric:
        value: encoded_width.value
      pen_width_pixel:
        value: encoded_width.value / 26.4572454037811
  da_pen_tip:
    seq:
    - id: pen_tip_type
      type: u1
    instances:
      is_rectangular:
        value: pen_tip_type == 1
  raster_operation:
    seq:
    - id: rop
      type: u1
      enum: rop_enum
    - id: unread
      type: u1
      repeat: expr
      repeat-expr: 3
      doc: we jump the size of an uint32 so 4 bytes total
  mantissa:
    doc: Optional block that can happen after a stylus height/width element to have better
      width/height size precision
    seq:
    - id: size
      type: multibyte_int_decoded
    - id: unread
      type: skip(size.value+1)
      doc: |
        Compressed int16 that adds a little something to the pen size with
        _size += (double)(sFraction / 1000.0f); ?
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

enums:
  tag_descriptor_specific:
    #6: tag_buttons # TODO
    11: stroke_property_list

  tag_table:
    0: tag_ink_space_rect
    1: tag_guid_table
    2: tag_draw_attrs_table
    3: tag_draw_attrs_block
    4: tag_stroke_desc_table 
    5: tag_stroke_desc_block
    # 6 is descriptor specific
    # 7 and 8 are no_x and no_y, but only seen on incorrect ISF files
    9: tag_didx
    10: tag_stroke
    # 11 is descriptor specific
    # TODO
    # 12 is stroke specific (TODO in the stroke reader itself)
    13: stroke_descriptor_table_index
    14: compression_header
    # TODO
    # 15: transform_table
    # TODO
    16: transform
    17: transform_isotropic_scale
    18: transform_anisotropic_scale
    19: transform_rotate
    20: transform_translate
    21: tag_transform_and_scale
    # 22 transform_quad is unused, it never appears in the C# impl
    23: transform_table_index
    # TODO
    # 24: tag_metric_table
    25: tag_metric_block
    26: tag_metric_table_index
    # 27: mantissa (specific/internal to stroke descriptor)
    28: persistence_format
    29: tag_himetric_size
    30: stroke_ids
    # TODO:
    # 31: ExtendedTransformTable
  rop_enum:
    9: mask_pen_highlighter
    13: default
    # See https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/DrawingAttributeSerializer.cs,396
  tags_stroke_desc:
    50: x
    51: y
    52: z
    53: packetstatus
    54: timertick
    55: serialnumber
    56: normalpressure
    57: tangentpressure
    58: buttonpressure
    59: xtiltorientation
    60: ytiltorientation
    61: azimuthorientation
    62: altitudeorientation
    63: twistorientation
    64: pitchrotation
    65: rollrotation
    66: yawrotation
    67: penstyle
    68: colorref
    69: styluswidth
    70: stylusheight
    71: pentip
    72: drawingflags
    73: cursorid
    74: wordalternates
    75: charalternates
    76: inkmetrics
    77: guidestructure
    78: timestamp
    79: language
    80: transparency
    81: curvefittingerror
    82: recolattice
    83: cursordown
    84: secondarytipswitch
    85: barreldown
    86: tabletpick
    87: rasteroperation
  metric_scale:
    0: unit_default
    1: unit_inch
    2: unit_centimeter
    3: unit_degree
    4: unit_radian
    5: unit_second
    6: unit_pound
    7: unit_gram

meta:
  id: test_read_until_n_bytes
  endian: be
seq:
  - id: zero
    type: u1
  - id: header
    doc: header
    type: u4
  - id: element
    type: read_until(12)
  

types:
  read_until:
    params:
    - id: n_bytes_total
      type: u4
    seq:
    - id: groups
      type: |
        group(
          _index == 0 ? n_bytes_total : groups[_index -1].interm_value)
      repeat: until
      repeat-until: _.interm_value == 0
    types:
      group: 
        params:
        - id: prev_bytes_left
          type: u4
        seq:
        - id: read_data
          type: u4
        instances:
          interm_value:
            value: prev_bytes_left - 4

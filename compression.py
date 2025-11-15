import numpy as np
from enum import Enum, auto
from huffman import huffman_list_decode
from delta_delta_transform import inverse_delta_delta

class CompressionType(Enum):
    HUFFMAN = auto()
    UNCOMPRESSED = auto()

def get_compression_info(
    list_logical:np.ndarray
    ):
    elmt_value = np.array([16,8,4,2,1])

    bit_compression = list_logical[0:8]
    print("compression bit is", bit_compression)

    compression_type = bit_compression[0]
    
    if compression_type:
        # then huffman
        # we need to find the index

        left_values = np.where(bit_compression[-5:],elmt_value, 0*elmt_value)
        index = np.sum(left_values)
        
        return (CompressionType.HUFFMAN,index)
    else:
        return (CompressionType.UNCOMPRESSED,None)
    
def inflate_property_data(offset:int, logical_array:np.ndarray, cpoints:int):

    comp_type, index = get_compression_info(logical_array[offset:offset+8])
    offset += 8
    print(comp_type,index)
    match comp_type:
        case CompressionType.HUFFMAN:
            propertylist,read = huffman_list_decode(logical_array[offset:],cpoints,index)
            inverse_delta_delta(propertylist) # under conditions
            offset += read
        case CompressionType.UNCOMPRESSED:
            print("unsupported for now")

    if offset % 8 !=0:
        # align back to the byte grid
        offset = 8*(1 + (offset // 8))

    return (offset, propertylist)
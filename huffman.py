from typing import List
import numpy as np
from typing import Tuple


def get_huffman_data(index):
    bits_amounts_dic = {
        0:[0, 1,  2,  4,  6,  8, 12, 16, 24, 32],
        1:[0, 1,  1,  2,  4,  8, 12, 16, 24, 32],
        2:[0, 1,  1,  1,  2,  4,  8, 14, 22, 32],
        3:[0, 2, 2,  3,  5,  8, 12, 16, 24, 32],
        4:[0, 2,  2,  3,  5,  8, 12, 16, 24, 32],
        5:[0, 3,  4,  5,  8, 12, 16, 24, 32],
        6:[0, 4,  6,  8, 12, 16, 24, 32],
        7:[0, 7,  8, 12, 16, 24, 32],
    }

    bits_amounts = bits_amounts_dic[index]

    huffman_base = [0]
    base: int = 1
    for k in range(1, len(bits_amounts)):
        huffman_base.append(base)
        value = bits_amounts[k]
        base += 2 ** (value - 1)

    return bits_amounts, huffman_base


def huffman_list_decode(logical_array: np.ndarray, n_points: int, index:int)->Tuple[list[int], int]:
    print(f"inflating {n_points} elements with index {index}")
    decoded_array: List[int] = []

    offset = 0
    bits_amounts, huffman_base = get_huffman_data(index)

    print("huffman_base",huffman_base)

    decoded_elements: int = 0
    count: int = 0

    while decoded_elements < n_points:
        bit = logical_array[offset]
        offset += 1

        if bit:
            count += 1
            continue

        if count == 0:
            value: int = 0
        elif count < len(bits_amounts):
            # bits to read as uint64
            bits_offset = logical_array[offset : offset + bits_amounts[count]]
            offset += bits_amounts[count]
            power2 = np.power(2,np.arange(0,bits_amounts[count]))
            offset_value = int(np.sum(bits_offset[::-1].dot(power2)))

            print("count : ", count,"bits offset : ", bits_offset,"offset value : ", offset_value)

            sign = offset_value % 2 == 1 # not sure here
            offset_value = offset_value // 2
            value = huffman_base[count] + offset_value

            print("huffman offset", huffman_base[count], "offset value", offset_value)

            if sign:
                value = -value
                print("negative value")
        else:
            raise NotImplementedError("this type is not implemented")

        decoded_array.append(value)
        count = 0
        decoded_elements += 1
        print("final value : ",value)
    return decoded_array, offset


def list_int_to_logical_array(list_int: List[int]):
    return np.unpackbits(np.array(list_int, dtype=np.dtypes.UInt8DType)).astype(np.bool)

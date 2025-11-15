from pathlib import Path
from isf_format import IsfFormat
from huffman import huffman_list_decode, list_int_to_logical_array
from delta_delta_transform import inverse_delta_delta
import numpy as np


isf_file = Path.cwd() / "files_test" / "binary_isf.txt"

read_file = IsfFormat.from_file(isf_file)

# for the flag
# print("polyline {0:b}".format(0x00000000))
# print("Fit to curve {0:b}".format(0x00000001))
# print("subtractive transparency {0:b}".format(0x00000002))
# print("ignore pressure {0:b}".format(0x00000004))
# print("antialiased {0:b}".format(0x00000010))
# print("ignore rotation {0:b}".format(0x00000020))
# print("ignore angle {0:b}".format(0x00000040))

print(read_file.isf_tag[5].content.cpoints.value) #nof points
print("{0:b}".format(read_file.isf_tag[5].content.compression_id))

# read the unread bytes for this
bytes_compressed = read_file.isf_tag[5].content.compressed_data.unread
cpoints = read_file.isf_tag[5].content.cpoints.value
index = read_file.isf_tag[5].content.compressed_data.codec

# huffman
logical_array = list_int_to_logical_array(bytes_compressed)
offset = 0

x_list, read = huffman_list_decode(logical_array[0:],cpoints,index)
inverse_delta_delta(x_list)
offset += read
print("the offset is", read)
# BEWARE, we need to read the next byte and check from that both the algorithm AND the index

y_list, read = huffman_list_decode(logical_array[offset:],cpoints,index)
inverse_delta_delta(y_list)
offset += read


expected_list = [
                {
                    "X": 210.96153259277344,
                    "Y": 177.30769348144531,
                    "pressure": 0.281206131
                },
                {
                    "X": 210.84616088867188,
                    "Y": 179.19230651855469,
                    "pressure": 0.306109995
                },
                {
                    "X": 210.73077392578125,
                    "Y": 181.19230651855469,
                    "pressure": 0.310993105
                },
                {
                    "X": 210.73077392578125,
                    "Y": 182.92308044433594,
                    "pressure": 0.310993105
                },
                {
                    "X": 210.69230651855469,
                    "Y": 184.26922607421875,
                    "pressure": 0.310993105
                },
                {
                    "X": 210.69230651855469,
                    "Y": 185.80769348144531,
                    "pressure": 0.324421644
                },
                {
                    "X": 210.61538696289062,
                    "Y": 188.80769348144531,
                    "pressure": 0.339315146
                },
                {
                    "X": 210.57691955566406,
                    "Y": 194.5,
                    "pressure": 0.354696929
                },
                {
                    "X": 210.53846740722656,
                    "Y": 203.23077392578125,
                    "pressure": 0.370078743
                },
                {
                    "X": 210.61538696289062,
                    "Y": 213.84616088867188,
                    "pressure": 0.380821586
                },
                {
                    "X": 210.88461303710938,
                    "Y": 225,
                    "pressure": 0.390587807
                },
                {
                    "X": 211.30769348144531,
                    "Y": 234.80769348144531,
                    "pressure": 0.400109857
                },
                {
                    "X": 211.76922607421875,
                    "Y": 242.69230651855469,
                    "pressure": 0.409631938
                },
                {
                    "X": 212.15383911132812,
                    "Y": 248.26922607421875,
                    "pressure": 0.40621376
                },
                {
                    "X": 212.53846740722656,
                    "Y": 253.07691955566406,
                    "pressure": 0.400354028
                },
                {
                    "X": 212.96153259277344,
                    "Y": 257.0384521484375,
                    "pressure": 0.393761814
                },
                {
                    "X": 213.42308044433594,
                    "Y": 260.26922607421875,
                    "pressure": 0.387169629
                },
                {
                    "X": 213.96153259277344,
                    "Y": 262.61538696289062,
                    "pressure": 0.363974839
                },
                {
                    "X": 214.42308044433594,
                    "Y": 264.11538696289062,
                    "pressure": 0.337606043
                },
                {
                    "X": 214.42308044433594,
                    "Y": 264.11538696289062,
                    "pressure": 0.310260624
                },
                {
                    "X": 214.42308044433594,
                    "Y": 264.11538696289062,
                    "pressure": 0.183299765
                }
            ]
found_isf_library = [5485 ,5482 ,5479 ,5479 ,5478 ,5478 ,5476 ,5475 ,5474 ,5476 ,5483 ,5494 ,5506 ,5516 ,5526 ,5537 ,5549 ,5563 ,5575 ,5575 ,5575 ]
print("ours:", x_list)
print("correct: ",found_isf_library)

found_isf_library_y = [4610 ,4659 ,4711 ,4756 ,4791 ,4831 ,4909 ,5057 ,5284 ,5560 ,5850 ,6105 ,6310 ,6455 ,6580 ,6683 ,6767 ,6828 ,6867 ,6867 ,6867 ]
print("ours:", y_list)
print("correct: ",found_isf_library_y)

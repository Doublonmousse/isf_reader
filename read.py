from pathlib import Path
from isf_format import IsfFormat
from huffman import list_int_to_logical_array
from compression import inflate_property_data
import matplotlib.pyplot as plt


isf_file = Path.cwd() / "files_test" / "binary_isf.txt"

read_file = IsfFormat.from_file(isf_file)

print(read_file.isf_tag[5].content.cpoints.value) #nof points

# read the unread bytes for this
bytes_compressed = read_file.isf_tag[5].content.compressed_data
cpoints = read_file.isf_tag[5].content.cpoints.value

# huffman
# from 
offset = 0
logical_array = list_int_to_logical_array(bytes_compressed)

# in order (from the stroke descr): 
# - x
# - y
# - pressure
# - xtilt
# - ytilt
# - timertick
offset, x_list = inflate_property_data(offset, logical_array, cpoints)
offset, y_list = inflate_property_data(offset, logical_array, cpoints)
offset, pressure_data = inflate_property_data(offset, logical_array, cpoints)
offset, xtilt = inflate_property_data(offset, logical_array, cpoints) 
offset, ytilt = inflate_property_data(offset, logical_array, cpoints) 
offset, timertick = inflate_property_data(offset, logical_array, cpoints)

# Then button if they exist
# https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/StrokeSerializer.cs,468

print("final offset : ", offset)

# comp with libisf qt
found_isf_library = [5485 ,5482 ,5479 ,5479 ,5478 ,5478 ,5476 ,5475 ,5474 ,5476 ,5483 ,5494 ,5506 ,5516 ,5526 ,5537 ,5549 ,5563 ,5575 ,5575 ,5575 ]
print("ours:", x_list)
print("correct: ",found_isf_library)

found_isf_library_y = [4610 ,4659 ,4711 ,4756 ,4791 ,4831 ,4909 ,5057 ,5284 ,5560 ,5850 ,6105 ,6310 ,6455 ,6580 ,6683 ,6767 ,6828 ,6867 ,6867 ,6867 ]
print("ours:", y_list)
print("correct: ",found_isf_library_y)

found_isf_library_pressure = [4607 ,5015 ,5095 ,5095 ,5095 ,5315 ,5559 ,5811 ,6063 ,6239 ,6399 ,6555 ,6711 ,6655 ,6559 ,6451 ,6343 ,5963 ,5531 ,5083 ,3003 ]
print("ours:", pressure_data)
print("correct: ",found_isf_library_pressure)

found_isf_library_xtilt = [2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2641 ,2650 ,2658 ,2665 ,2665 ,2673 ]
print("ours:", xtilt)
print("correct: ",found_isf_library_xtilt)
print("okay", xtilt == found_isf_library_xtilt)

found_isf_library_ytilt = [1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1139 ,1115 ,1090 ,1066 ,1066 ,1040 ]
print("ours:", ytilt)
print("correct: ",found_isf_library_ytilt)
print("okay", ytilt == found_isf_library_ytilt)

print(timertick)
# timertick starts at 0 so we need to find somewhere the
# start timetick ?
# but where ?

# beware of buttons ?
#             int intsPerPoint = stylusPointDescription.GetInputArrayLengthPerPoint();
# then buttons
#             int buttonCount = stylusPointDescription.ButtonCount;

# then extended properties depending on the stroke descriptor
# basically this is the info by guid
# as long as we don't know what that info corresponds to this isn't useful for us
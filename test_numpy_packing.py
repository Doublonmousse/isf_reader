import numpy as np

logical_array = np.array([True,False], dtype=np.bool)
larger_array = np.zeros((64),dtype=np.bool)
larger_array[0:logical_array.shape[0]] = logical_array

read_value = np.frombuffer(np.packbits(larger_array),dtype=np.uint64)[0]
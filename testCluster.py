from numpy import genfromtxt
from dataProcessor import Processor

dataset_raw = genfromtxt('./datasets/soybean-small.data', delimiter=',', dtype=None)
# dataset_raw = genfromtxt('./datasets/mushroom.data', delimiter=',', dtype=None)

processor = Processor(dataset_raw)
processor.apply_nominal_conversation()
processor.apply_scaling()

d = processor.get_data()
print d
# dataset = processor.get_structured_data()

# print dataset.data[0]
# print dataset.target[0]
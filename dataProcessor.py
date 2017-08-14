import numpy as np
from sklearn.preprocessing import MinMaxScaler


class Processor:

	def __init__(self, data):
		self.data = [list(item) for item in data]
		self.attr_count = len(self.data[0])

	# # Used to map strings in numbers
	# def apply_nominal_conversation(self):
	# 	for i in range(0, self.attr_count):
    # 			if(type(self.data[0][i]) is np.string_):
	# 					strings = set([x[i] for x in self.data])
	# 					nums = range(0, len(strings))
	# 					table = dict(zip(strings, nums))
	# 					for j, item in enumerate(self.data):
    # 							item[i] = table[item[i]]

	def apply_scaling(self):
		scaler = MinMaxScaler()
		scaler.fit(self.data)
		self.data = scaler.transform(self.data)

	def get_data(self):
    		return self.data

	# # Only for classification or clustering comparison
	# def get_structured_data(self):
	# 	return StructuredData(self.data[:, :self.attr_count - 1], self.data[:, self.attr_count - 1])


class StructuredData:

	def __init__(self, X, y):
		self.data = (X)
		self.target = (y)

import random as rand;

## mlCons / dlCons structure: [(instance, instance), ... (instance, instance)]
## instance / point structure: Set(attr1, attr2...)
class ConstrainedKMeans:
	def __init__(self, clustersQty):
		self.clustersQty = clustersQty;

	#This functiion trains with the dataset.
	def clusterize(self, dataset, mlCons, dlCons):
		print('clusterizing with ', initClusters.length, " clusters...");
		self.clusters = [[rand.random() for x in range(len(dataset[0]))]]*clustersQty ### check dataset length / init clusters

		__preprocessDataset(dataset);

		while (not __converged()):
			clusterPoints = __assignPoints(dataset, mlCons, dlCons);
			self.oldClusters = self.clusters;
			self.clusters = __updateClusters(clusterPoints);

		return self.clusters;

	#This function preprocess the dataset.
	#It should put values in [0,1] and transform symbolic data into numerical data.
	def __preprocessDataset(self, dataset):
    		return None

	#This function shall check if the function has stop converging (we should limit a threshold)
	def __converged(self):
    		return false

	#This function shall assign the points to the clusters according to its distance from the clusters.
	def __assignPoints(self, dataset, mlCons, dlCons):
    		return None

	#This function shall move the clusters according to its points' positions.
	def __updateClusters(self, clusterPoints):
    		return None

	#This function is the article's violate-contraint function.
	def __violateConstraints(self, point, cluster, mlCons, dlCons):
		print('checking constraints...');
		mustLink = [x for x in mlCons if point in x];

		if (mustLink.length > 0):
			for ml in mustLink:
				if (ml[0] == point):
					if (ml[1] not in cluster):
						return true;
				else:
					if (ml[0] not in cluster):
						return true;

		dontLink = [x for x in dlCons if point in x];

		if (dontLink.length > 0):
			for dl in dontLink:
				if (dl[0] == point):
					if (ml[1] in cluster):
						return true;
				else:
					if (ml[0] in cluster):
						return true;

		return false;

	#This function calculates the hamming distance.
	def __hammingDist(a, b):
		return abs(ord(a) - ord(b));


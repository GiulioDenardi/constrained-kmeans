import random as rand;
import math
from sets import Set;

## mlCons / dlCons structure: [(instance, instance), ... (instance, instance)]
## instance / point structure: Set(attr1, attr2...)
class ConstrainedKMeans:
	def __init__(self, clustersQty, convergeThreshold, distFunction):
		self.clustersQty = clustersQty;
		self.convergeThreshold = convergeThreshold;
		self.distFunction = distFunction;

	#This functiion trains with the dataset.
	def clusterize(self, dataset, mlCons, dlCons):
		print('clusterizing with ', self.clustersQty, " clusters...");
		self.clusters = {k : rand.choice(dataset) for k in range(self.clustersQty)}
		self.clusterPoints = {k : [] for k in self.clusters.keys()};
		self.oldClusters = self.clusters; # TODO: Remove this line
		
		while (not self.__converged()):
			self.clusterPoints = {k : [] for k in self.clusters.keys()}
			self.__assignPoints(dataset, mlCons, dlCons);
			self.oldClusters = self.clusters;
			self.clusters = self.__updateClusters(self.clusterPoints);

		return self.clusterPoints;

	#This function preprocess the dataset.
	#It should put values in [0,1] and transform symbolic data into numerical data.
	def __preprocessDataset(self, dataset):
    		return None

	#This function shall check if the function has stop converging (we should limit a threshold)
	def __converged(self):
		if (self.oldClusters != None):
    			for i in self.oldClusters.items:
					for attr in self.oldClusters[i].length:
						if (self.oldClusters[i][attr] - self.clusters[i][attr] > self.convergeThreshold):
							return False;

		return True;

	#This function shall assign the points to the clusters according to its distance from the clusters.
	def __assignPoints(self, dataset, mlCons, dlCons):
		for point in dataset:
			##TODO check if should insert the points with constraints first.
			cluster = self.__findNearestCluster(point);
			if (not self.__violateConstraints(point, cluster, mlCons, dlCons)):
				self.clusterPoints[cluster].append(point);

	def __findNearestCluster(self, point):
		choosenCluster = None;
		choosenDist = None;
		for c in self.clusters:
			if (choosenCluster == None):
				choosenCluster = c;
				choosenDist = self.distFunction.getDist(point);
			elif (self.distFunction.getDist(point) < choosenDist):
				choosenCluster = c;
				choosenDist = self.distFunction.getDist(point);

		return choosenCluster;


	#This function shall move the clusters according to its points' positions.
	def __updateClusters(self, clusterPoints):
		for cp in self.clusterPoints:
			for attr in self.clusters[cp]:
				self.clusters[cp][attr] = sum(x[attr] for x in self.clusterPoints[cp])/len(self.clusterPoints[cp]);


	#This function is the article's violate-contraint function.
	def __violateConstraints(self, point, cluster, mlCons, dlCons):
		print('checking constraints...');
		mustLink = [x for x in mlCons if (point == x or point[::-1] == x)];

		if (mustLink.length > 0):
			for ml in mustLink:
				if (ml[0] == point):
					if (ml[1] not in cluster):
						return True;
				else:
					if (ml[0] not in cluster):
						return True;

		dontLink = [x for x in dlCons if (point == x or point[::-1] == x)];

		if (dontLink.length > 0):
			for dl in dontLink:
				if (dl[0] == point):
					if (ml[1] in cluster):
						return True;
				else:
					if (ml[0] in cluster):
						return True;

		return False;


class DistanceMetrics:

    def EuclidianDistance(self, X, Y):
        tuples = zip(X, Y)
        distance = 0
        for x, y in tuples:
            distance += (x ** 2 - y ** 2)
        return math.sqrt(distance)

    def SimpleMatchDistance(self, X, Y):
        tuples = zip(X, Y)
        distance = 0
        for x, y in tuples:
            if(x != y):
                distance += 1
        return distance

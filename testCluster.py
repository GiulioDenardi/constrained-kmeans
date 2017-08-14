from numpy import genfromtxt
from dataProcessor import Processor
from constrainedKMeans import ConstrainedKMeans, DistanceMetrics

# Dataset loading
dataset_raw = genfromtxt('./datasets/soybean-small.clean.data', delimiter=',', dtype=None) # numeric only dataset

# Data pre-processing
processor = Processor(dataset_raw)
processor.apply_scaling() # just in case the whole dataset is composed by numeric attributes
dataset = processor.get_data()

# Algorithm execution
k_clusters = 4
converge_threshold = 1.0
distance_metric = DistanceMetrics.EuclidianDistance
constrained_kmeans = ConstrainedKMeans(k_clusters, converge_threshold, distance_metric)

must_link = []
cannot_link = []
constrained_kmeans.clusterize(dataset, must_link, cannot_link)
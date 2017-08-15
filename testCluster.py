import numpy as np;
from numpy import genfromtxt;
import random as rand;
from dataProcessor import Processor;
from constrainedKMeans import ConstrainedKMeans, DistanceMetrics;

# Dataset loading
print('getting dataset...')
dataset_raw = genfromtxt('./datasets/soybean-small.clean.data', delimiter=',', dtype=None) # numeric only dataset
print('Got dataset!');

# Data pre-processing
print('Starting data processing...');
processor = Processor(dataset_raw)
processor.apply_scaling() # just in case the whole dataset is composed by numeric attributes
dataset = processor.get_data()
print('Data processed! dataset: ', dataset);

# Algorithm execution
k_clusters = 4 # number of classes from the original dataset
converge_threshold = 0.02
distance_metric = DistanceMetrics.EuclidianDistance() # just in case the whole dataset is composed by numeric attributes
constrained_kmeans = ConstrainedKMeans(k_clusters, converge_threshold, distance_metric)

must_link = [ [np.array([4,0,2,1,1,1,0,1,0,2,1,1,0,2,2,0,0,0,1,0,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0]), np.array([5,0,2,1,0,3,1,1,1,2,1,1,0,2,2,0,0,0,1,1,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0])],
				[np.array([5,0,2,1,0,3,1,1,1,2,1,1,0,2,2,0,0,0,1,1,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0]),np.array([3,0,2,1,0,2,0,2,1,1,1,1,0,2,2,0,0,0,1,0,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0])] ];
cannot_link = []
constrained_kmeans.clusterize(dataset, must_link, cannot_link)
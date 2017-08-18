import numpy as np;
from numpy import genfromtxt;
import random as rand;
from dataProcessor import Processor;
from constrainedKMeans import ConstrainedKMeans, DistanceMetrics, ReportResults;

# Dataset loading
print('getting dataset...')
dataset_raw = genfromtxt('./datasets/soybean-small.clean.data', delimiter=',', dtype=None) # numeric only dataset
print('Got dataset!');

# Data pre-processing
print('Starting data processing...');
processor = Processor(dataset_raw)
processor.apply_scaling() # just in case the whole dataset is composed by numeric attributes
dataset = processor.get_data()

# Algorithm execution
k_clusters = 4 # number of classes from the original dataset
converge_threshold = 0.02
distance_metric = DistanceMetrics.EuclidianDistance() # just in case the whole dataset is composed by numeric attributes
constrained_kmeans = ConstrainedKMeans(k_clusters, converge_threshold, distance_metric)

must_link = [
    [dataset[0], dataset[1]],
    [dataset[1], dataset[2]],
	[dataset[2], dataset[12]],
]
cannot_link = [
	[dataset[10], dataset[11]]
]
results = constrained_kmeans.clusterize(dataset, must_link, cannot_link)

# Results report
report = ReportResults()
report.print_clusters(dataset, results)

# Evaluation
report.print_evaluation(dataset, results, must_link, cannot_link)
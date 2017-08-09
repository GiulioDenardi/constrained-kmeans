# [DRAFT]

# Constrained K-Means
This is an implementation of the K-means algorithm variation with constraints to represent (when possible) better data information.


# The algorithm
The algorithm basically does the same as the K-means [(Check here)](https://www.coursera.org/learn/machine-learning/lecture/93VPG/k-means-algorithm). But when converging the clusters, it will consider information about two types of constraints:


- *Must-Link (ML)*: This constraint represents relationships between two points that must be in the same cluster.
- *Cannot-Link (CL)*: This constraint represents relationships between two points that must be in different clusters.


### For example:

ML(d, d') = d and d' shall be in the same cluster.
ML({1, 2}, {3, 4}) = {1,2} must belong to the same cluster as {3, 4}.
CL(d, d') = d e d' must be in different clusters.
And so on.

For a complete look at the article used as base of this implementation, check [here](http://www.cs.cmu.edu/~dgovinda/pdf/icml-2001.pdf).


### Implementation

The implementation of the algorithm is at the _constrainedKMeans.py_ file. It contains the #clusterize public function and the private #violateConstraints "private" function.

For the tests, we used the _testCluster.py_ file, that contains some basic tests and a presentation of this implementation. So, if you want to easily check the algorithm, just open this file!

For productivity purposes, here is a simple [Python cheat sheet](http://www.cogsci.rpi.edu/~destem/igd/python_cheat_sheet.pdf) for checking basic python commands.


### Authors

The authors of this implementation are:

- Allan Targino
- Dani Lucarini
- Giulio Denardi

#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import random as rand;
import math;
from sets import Set;
import copy;
import numpy as np;
import itertools;

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

        self.clusters = self.__getInitialClusters(dataset.copy());
        self.oldClusters = None;
        
        while (not self.__converged()):
            self.clusterPoints = {k : [] for k in self.clusters.keys()};
            self.noCluster = [];
            self.__assignPoints(dataset, mlCons, dlCons);
            self.oldClusters = copy.deepcopy(self.clusters);
            self.__updateClusters();

        # print('Cluster x Points: ', self.clusterPoints);
        # print('Clusters: ', self.clusters);
        return self.clusterPoints;

    #This function shall check if the function has stop converging (we should limit a threshold)
    def __converged(self):
        if (self.oldClusters != None):
            for i in self.oldClusters.keys():
                if (abs(np.std(self.oldClusters[i]) - np.std(self.clusters[i])) > self.convergeThreshold):
                    print('CONVERGE MORE!')
                    return False;
        else:
            return False;

        return True;

    #This function shall assign the points to the clusters according to its distance from the clusters.
    def __assignPoints(self, dataset, mlCons, dlCons):
        for point in dataset:
            ##TODO check if should insert the points with constraints first.
            cluster = self.__findNearestCluster(point);
            if (not self.__violateConstraints(point, cluster, mlCons, dlCons)):
                self.clusterPoints[cluster].append(point);
            else:
                self.noCluster.append(point);

    def __findNearestCluster(self, point):
        choosenCluster = None;
        choosenDist = None;
        for c in self.clusters.items():
            if (choosenCluster == None):
                choosenCluster = c[0];
                choosenDist = self.distFunction.getDist(point, c[1]);
            elif (self.distFunction.getDist(point, c[1]) < choosenDist):
                choosenCluster = c[0];
                choosenDist = self.distFunction.getDist(point, c[1]);

        return choosenCluster;


    #This function shall move the clusters according to its points' positions.
    def __updateClusters(self):
        for cp in self.clusterPoints.keys():
            for attr in range(0, self.clusters[cp].size):
                self.clusters[cp][attr] = sum(x[attr] for x in self.clusterPoints[cp])/len(self.clusterPoints[cp]);

    #This function gets the initial clusters, avoiding to get the same cluster point at the same time.
    ##TODO do this better.
    def __getInitialClusters(self, dataset):
        if (np.unique(dataset).size < self.clustersQty):
            raise ValueError('O número de instâncias únicas do dataset deve ser maior ou igual o número de grupos.');

        keepChoosingPoints = True;
        while (keepChoosingPoints):
            cls = {k : rand.choice(dataset) for k in range(self.clustersQty)};
            aux = set([tuple(cl) for cl in cls.values()]);

            if (self.clustersQty == len(aux)):
                keepChoosingPoints = False;

        return cls;

    #This function is the article's violate-contraint function.
    def __violateConstraints(self, point, cluster, mlCons, dlCons):
        mustLink = [x for x in mlCons if (any((point == y).all() for y in x))];

        if (len(mustLink) > 0):
            for ml in mustLink:
                if ((point == ml[0]).all()):
                    pairCluster = self.__findNearestCluster(ml[1]);
                else:
                    pairCluster = self.__findNearestCluster(ml[0]);
                if (pairCluster != cluster):
                    return True;

        dontLink = [x for x in dlCons if (any((point == y).all() for y in x))];

        if (len(dontLink) > 0):
            for dl in dontLink:
                if ((point == dl[0]).all()):
                    pairCluster = self.__findNearestCluster(dl[1]);
                else:
                    pairCluster = self.__findNearestCluster(dl[0]);
                if (pairCluster == cluster):
                    return True;

        return False;


class DistanceMetrics:

    class EuclidianDistance:
        def getDist(self, X, Y):
            tuples = zip(X, Y)
            distance = 0
            for x, y in tuples:
                distance += (x - y) ** 2
            return math.sqrt(distance)
        
    class SimpleMatchDistance:
        def getDist(self, X, Y):
            tuples = zip(X, Y)
            distance = 0
            for x, y in tuples:
                if(x != y):
                    distance += 1
            return distance

class ReportResults:
    
    def __print_index(self, source, item_to_search):
        list_items = list(source)
        for i, item in enumerate(list_items):
            if((item==item_to_search).all()):
                print(i, end=' ')

    def print_clusters(self, dataset, results):
        for i in range(len(results)):
            cluster = results[i]
            print("\nCluster " + str(i) + "(" + str(len(cluster)) + " items):")
            for item in cluster:
                self.__print_index(dataset, item)
        print("\n")

    def __item_in_cluster(self, results, constraint_pair):
        for i in range(len(results)):
            cluster = list(results[i])
            res = 0
            for i, item in enumerate(cluster):
                if((item==constraint_pair[0]).all() or (item==constraint_pair[1]).all()):
                    res+=1
            if(res==2):
                return True
        return False

    def __compute_evaluation_must_link(self, n_ml, a):
        return a/float(n_ml)

    def __compute_evaluation_cannot_link(self, n_cl, b):
        return b/float(n_cl)

    def __compute_evaluation_ordinary(self, n, a, b):
        return (a + b)/float(n)

    def __compute_evaluation_overall(self, n, a, b):
        return ((a + b)/((n*(float(n)-1))/2))

    def print_evaluation(self, dataset, results, must_link, cannot_link):
        n_ml = len(must_link)
        n_cl = len(cannot_link)
        n = n_ml + n_cl
        
        a=0
        for i in range(len(must_link)):
            constraint = must_link[i]
            if(self.__item_in_cluster(results,constraint)):
                a+=1
        b=0
        for i in range(len(cannot_link)):
            constraint = cannot_link[i]
            if(not self.__item_in_cluster(results,constraint)):
                b+=1
        
        evaluation_must_link = self.__compute_evaluation_must_link(n_ml, a)
        evaluation_cannot_link = self.__compute_evaluation_cannot_link(n_cl, b)
        evaluation_ordinary = self.__compute_evaluation_ordinary(n, a, b)
        evaluation_overall = self.__compute_evaluation_overall(n, a, b)

        print("n=" + str(n))
        print("a=" + str(a))
        print("b=" + str(b))
        print("evaluation_must_link=" + str(evaluation_must_link))
        print("evaluation_cannot_link=" + str(evaluation_cannot_link))
        print("evaluation_ordinary=" + str(evaluation_ordinary))
        print("evaluation_overall=" + str(evaluation_overall))
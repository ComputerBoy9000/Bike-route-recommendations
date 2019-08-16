import numpy as np
import pandas as pd
import itertools 
import random 
import scipy.stats as st

city_data = pd.read_csv('uscitiesv1.5.csv')

cities = city_data['city']

city_list = cities.tolist()

class Graph:

    def __init__(self, nodes, edges):

        self.nodes = nodes
        self.edges = edges

        num_nodes = len(nodes)
        num_edges = len(edges)

class RandomGraph:

    def __init__(self, num_nodes, num_edges):

        num_nodes = self.num_nodes
        num_edges = self.num_edges

        nodes = cities.sample(n = num_nodes).tolist()

        all_edges = itertools.product(nodes,nodes)

        ## Some housekeeping needed because we could generate a 
        ## random graph that is disconnected, could
        ## mandate a minimum number of edges or iterate
        ## over the set to delete disconnected graphs 
        
        edges = random.sample(all_edges, num_edges)



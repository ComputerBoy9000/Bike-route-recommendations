import numpy as np
import pandas as pd
import itertools 
import random 
import scipy.stats as st
import Graph
import RandomGraph

## road conditions X
## traffic conditions 
## grade X
## bike lane X
## stop sign vs. stop light vs. no stop X

class CityNetwork:

    def __init__(self, graph,stop_types, bike_lane_types):

        graph = self.graph

        ## stop types should typically have 3 values and be associated with nodes-
        ## no stop, a stop sign, or a stoplight
        stop_types = self.stop_types

        node_stops = np.random.choice(stop_types, n = graph.num_nodes, p = 'probability_vector')


        ## The two shape parameters just generate mostly flat to moderate grade roads with
        ## some outliers

        road_grades = st.beta.rvs(1.5,15, size = graph.num_edges)


         ## in general lanes can be none, protected, or unprotected 
        road_bike_lanes = np.random.choice(bike_lane_types, n = graph.num_edges, p = 'probability vector')


        ## Road conditions (smoothness/potholes/etc) generated as uniform on the unit interval
        road_conditions = st.uniform.rvs(graph.num_edges)

        ## traffic conditions (density of cars) generated as beta with some cherry-picked shape
        ## parameters- the relationship between beta and Poission/exponential makes sense here? 

        traffic_conditions = st.beta.rvs(4,8, size = graph.num_edges)

        intersections = []
        roads = []
        #assemble all the properties of nodes (intersections)
        for i in range(graph.num_nodes):
            intersection_tuple = (graph.nodes[i], node_stops[i])
            intersections.append(intersection_tuple)

        #assemble all the properties of edges (roads)
        for i in range(graph.num_edges):
            road_tuple = (graph.num_edges[i],road_grades[i],road_bike_lanes[i],
                            road_conditions[i],traffic_conditions[i])
            roads.append(road_tuple)






import numpy as np
import pandas as pd
import itertools 
import random 
import scipy.stats as st
import networkx as nx

city_data = pd.read_csv('uscitiesv1.5.csv')

cities = city_data['city'].to_list()

def city_generator(num_intersections):

    city = nx.DiGraph()

    intersections = random.sample(cities, num_intersections)

    for x in intersections:
        city.add_node(x, stop_type = np.random.choice(['None', 'Stop Sign', 'Stop Light']))

    possible_streets = [(x,y )for (x,y) in itertools.product(intersections,intersections) if x != y]

    num_streets = random.randint(num_intersections - 1, 2*(num_intersections-1))

    streets = random.sample(possible_streets,num_streets)

    for (x,y) in streets:

        city.add_edge(x, y, grade = st.beta.rvs(1.5,15, size = 1),
                    lane_type = np.random.choice(['None','Unprotected','Protected']), 
                    road_condition = st.uniform.rvs(loc = 0, scale = 1, size = 1),
                    traffic_conditions = st.beta.rvs(4,8, size = 1),
                    length = st.uniform.rvs(loc = 0, scale = 10, size = 1))

    
    return city
    
g = city_generator(5)

print(g.nodes())

print(g.edges())

print(g.nodes.data())
print(g.edges.data())




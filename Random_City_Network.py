import numpy as np
import pandas as pd
import itertools 
import random 
import scipy.stats as st
import networkx as nx

city_data = pd.read_csv('uscitiesv1.5.csv')

cities = city_data['city'].unique().tolist()

def city_generator(intersections):
    """
    This function uses the NetworkX package to generate graphs that act as synthetic data for city streets.

    Attributes:
            intersections (list): A set of graph nodes that represent the intersection of city streets.

    """
    city = nx.DiGraph()

    num_intersections = len(intersections)

    for x in intersections:
        city.add_node(x, stop_type =np.random.choice(['None','Stop Sign', 'Stop Light']))

        possible_streets = [(x, y) for (x, y) in itertools.product(intersections, intersections) if x != y]

    num_streets = random.randint(num_intersections - 1, 2 * (num_intersections - 1))

    streets = random.sample(possible_streets, num_streets)

    for (x, y) in streets:

        city.add_edge(x, y, 
                    grade= st.beta.rvs(1.5,15, size = 1)[0],
                    lane_type= np.random.choice(['None','Unprotected','Protected']), 
                    road_condition= st.uniform.rvs(loc = 0, scale = 1, size = 1)[0],
                    traffic_conditions= st.beta.rvs(4,8, size = 1)[0],
                    length= st.uniform.rvs(loc = 0, scale = 10, size = 1)[0], weight = 0
                    )
    return city

def random_city_generator(num_intersections):
    """
    This function uses the NetworkX package to generate random graphs that act as synthetic data for city streets.

    Attributes:
            num_intersections (int): A set of graph nodes that represent the intersection of city streets.
            The intersections are represented by the name of a US city as imported from the uscities1.5.csv
            file.

    """

    city = nx.DiGraph()

    intersections = random.sample(cities, num_intersections)

    for x in intersections:
        city.add_node(x, stop_type = np.random.choice(['None', 'Stop Sign', 'Stop Light']))

    possible_streets = [(x, y) for (x, y) in itertools.product(intersections, intersections) if x != y]

    num_streets = random.randint(num_intersections - 1, 2 * (num_intersections - 1))

    streets = random.sample(possible_streets, num_streets)

    for (x, y) in streets:

        city.add_edge(x, y, 
                    grade = st.beta.rvs(1.5,15, size = 1),
                    lane_type = np.random.choice(['None','Unprotected','Protected']), 
                    road_condition = st.uniform.rvs(loc = 0, scale = 1, size = 1),
                    traffic_conditions = st.beta.rvs(4,8, size = 1),
                    length = st.uniform.rvs(loc = 0, scale = 10, size = 1), weight = 0
                    )
    return city
    
def simple_route_weigher(city, street_attribute):
    """
    This function creates weights for the edges of a given city network according to a 
    chosen street attribute.
        
    Attributes:
        city (nx.DiGraph): A city network compiled using the city_network() or random_city_network() functions
        street_attribute (any): The grade, lane type, road condition, etc. metric chosen to weigh the edges.
    """

    for (x, y) in city.edges():
        city[x][y]['weight']= city[x][y][street_attribute]

def simple_uniform_route_weigher(city, street_attributes):
    """
    This function creates weights for the edges of a given city network by weighing the 
    chosen street attributes evenly.
        
    Attributes:
        city (nx.DiGraph): A city network compiled using the city_network() or random_city_network() functions
        street_attributes (list): The set of grade, lane type, road condition, etc. metrics chosen to weigh the edges.
    """

    for(x, y) in city.edges():
        for attribute in street_attributes:
            city[x][y]['weight'] += city[x][y][attribute]/len(street_attributes)

def route_weigher(city, street_attributes, street_attribute_weights):
    """
    This function creates weights for a given city network by weighing the chosen street attributes evenly.
        
    Attributes:
        city (nx.DiGraph): A city network compiled using the city_network() or random_city_network() functions
        street_attributes (list): The set of grade, lane type, road condition, etc. metrics chosen to weigh the edges.
        street_attribute_weights (np.array): A vector of weights to apply to each of the individual street attributes
        to form a linear combination of the given street attributes to form the weight of each edge.
    """

    for (x, y) in city.edges():
        city[x][y]['weight'] = 0
        for i in range(len(street_attributes)):
            city[x][y]['weight'] += float(street_attribute_weights[i])*float(city[x][y][street_attributes[i]])


def minimizing_search(graph, node_1, node_2, street_attribute):
    """
    This function finds the shortest distance from node_1 to node_2. 

    Attributes:
        graph (nx.DiGraph): The network being searched.
        node_1 (nx.DiGraph.node): The first node in the desired route.
        node_2 (nx.DiGraph.node): The final node in the desired route.
        street_attribute (any): The criteria to be used as weight for edges.
    """
    path = []
    dead_ends = []
    if nx.has_path(graph, node_1, node_2) == True:
        starting_point = node_1
        path.append(starting_point)
        while starting_point != node_2:
            possible_stops = [x for x in nx.neighbors(graph, starting_point) if x not in path]
            if possible_stops == []:
                dead_ends.append(starting_point)
                path = path[:len(path-1)]
                starting_point = path[len(path)-1]
                possible_stops = [x for x in nx.neighbors(graph, starting_point) if x not in path
                                            and x not in dead_ends]

            slopes = [graph[starting_point][x][attribute] for x in possible_stops]
            next_stop = possible_stops[np.argmin(slopes)]
            path.append(next_stop)
            starting_point = next_stop
       
    else:
        print('Can\'t take that route, sorry!')

    return path

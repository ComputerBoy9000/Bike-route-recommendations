import numpy as np
import pandas as pd
import itertools 
import random 
import scipy.stats as st
import networkx as nx

city_data = pd.read_csv('uscitiesv1.5.csv')

cities = city_data['city'].unique().tolist()


### added a 'less random' graph generator for easier testing
def city_generator(intersections):
    city = nx.DiGraph()

    num_intersections = len(intersections)


    for x in intersections:
        city.add_node(x, stop_type = np.random.choice(['None','Stop Sign', 'Stop Light']))

        possible_streets = [(x,y)for (x,y) in itertools.product(intersections,intersections) if x != y]

    num_streets = random.randint(num_intersections - 1, 2*(num_intersections-1))

    streets = random.sample(possible_streets,num_streets)

    for (x,y) in streets:

        city.add_edge(x, y, grade = st.beta.rvs(1.5,15, size = 1)[0],
                    lane_type = np.random.choice(['None','Unprotected','Protected']), 
                    road_condition = st.uniform.rvs(loc = 0, scale = 1, size = 1)[0],
                    traffic_conditions = st.beta.rvs(4,8, size = 1)[0],
                    length = st.uniform.rvs(loc = 0, scale = 10, size = 1)[0], weight = 0)

    
    return city

def random_city_generator(num_intersections):
    
    city = nx.DiGraph()

    # These are the nodes of the graph- the intersection (literally) of edges
    intersections = random.sample(cities, num_intersections)


    # The randomness here doesn't need to be uniform, and that ultimately doesn't reflect reality
    # in all likelihood- not sure where *realistic* data would come from, and I couldn't find a
    # straightforward way to generate random probability vectors p = <p_1,p_2,p_3> 
    for x in intersections:
        city.add_node(x, stop_type = np.random.choice(['None', 'Stop Sign', 'Stop Light']))


    # The graph doesn't need to be entirely connected, but these are all possible edges
    possible_streets = [(x,y )for (x,y) in itertools.product(intersections,intersections) if x != y]

    # Determines how many edges are in the graph
    num_streets = random.randint(num_intersections - 1, 2*(num_intersections-1))

    # The randomly selected edges of the graph
    streets = random.sample(possible_streets,num_streets)

    # Adds attributes to each street- the grade (distribution is heavily weighted to not having unrealistically
    # steep streets), discrete possibilities for bike lane types, uniform variables for length and road conditions
    # (guess these could be N(0,1) if necessary but make a lot of sense in this package, a beta distribution
    # that allows for the possibility of heavy traffic but weighs moderate traffic nicely, and initializing
    # the weight to be 0 at first so that the user choice can determine weight
    for (x,y) in streets:

        city.add_edge(x, y, grade = st.beta.rvs(1.5,15, size = 1),
                    lane_type = np.random.choice(['None','Unprotected','Protected']), 
                    road_condition = st.uniform.rvs(loc = 0, scale = 1, size = 1),
                    traffic_conditions = st.beta.rvs(4,8, size = 1),
                    length = st.uniform.rvs(loc = 0, scale = 10, size = 1), weight = 0)

    
    return city
    
def simple_route_weigher(city,attribute):
    # This can turn numerical attributes directly into weights. Looking for shortest paths
    # matches the modeling features from the city generator as more traffic, steeper, etc = bad.
    for (x,y) in city.edges():
        g[x][y]['weight']= g[x][y][attribute]

def simple_uniform_route_weigher(city,attributes):
    # Evenly weighs each attribute entered
    for(x,y) in city.edges():
        for attribute in attributes:
            g[x][y]['weight'] += g[x][y][attribute]/len(attributes)

def route_weigher(city,attributes,weights):
    ## the route weights can be normalized to make sure the edge weights are all less than 1 
    ## if it matters for the neural network 

    for (x,y) in city.edges():
        for i in range(len(attributes):
            g[x][y]['weight'] += weights[i]*attributes[i]


#### This function also does constrained search according to one of the parameters. It would also
#### be possible to change the single attribute to a linear combination of attributes as above. 
#### This seems a little more stilted since A* does essentially the same thing just by treating
#### the constraint of interest as weights- it's a cardinal and not an ordinal problem from the 
#### perspective of choosing graphs, but it's certainly an ordinal problem once we want to start
#### doing inference. 
def minimizing_search(graph,node_1,node_2,attribute):
    path = []
    dead_ends = []
    if nx.has_path(graph,node_1,node_2) == True:
        starting_point = node_1
        path.append(starting_point)
        while starting_point != node_2:
            possible_stops = [x for x in nx.neighbors(graph,starting_point) if x not in path]
            if possible_stops == []:
                dead_ends.append(starting_point)
                path = path[:len(path-1)]
                starting_point = path[len(path)-1]
                possible_stops = [x for x in nx.neighbors(graph,starting_point) if x not in path
                                            and x not in dead_ends]

            slopes = [graph[starting_point][x][attribute] for x in possible_stops]
            next_stop = possible_stops[np.argmin(slopes)]
            path.append(next_stop)
            starting_point = next_stop
       
    else:
        print('Can\'t take that route, sorry!')
    return path    
import pytest 
import numpy as np
import networkx as nx
from Random_City_Network import simple_route_weigher, route_weigher

test_graph = nx.DiGraph()
test_graph.add_edge('Boston','New York', grade= .2, lane_type= "None", road_condition= .12, traffic_conditions=.73, length= .8)
test_graph.add_edge('New York', 'Boston', grade= .3, lane_type= "None", road_condition= .31, traffic_conditions=.46, length= .18)
test_graph.add_edge('Boston','Los Angeles', grade= .55, lane_type= "Protected", road_condition= .42, traffic_conditions=.1, length= .323)    
test_graph.add_edge('Los Angeles', 'New York', grade =.1, lane_type= "Unprotected", road_condition= .02, traffic_conditions=.68, length= .22)    
test_graph.add_edge('New York', 'Los Angeles', grade = .01, lane_type= "None", road_condition= .062, traffic_conditions=.43, length= .27)                        
                        
class TestClass:
    def test_simple_route(self):
        simple_route_weigher(test_graph,'road_condition')
        assert(test_graph['Boston']['New York']['weight'] == .12)
        assert(nx.dijkstra_path(test_graph,'Boston','Los Angeles') == ['Boston', 'Los Angeles'])

    def test_route_weigher(self):
        route_weigher(test_graph,['road_condition','traffic_conditions'],np.array([.5,.01]))
        assert(test_graph['Boston']['New York']['weight'] == .0673)
        assert(nx.dijsktra_path(test_graph,'Boston','Los Angeles', weight = 'weight') == ['Boston', 'New York', 'Los Angeles'])

route_weigher(test_graph,['road_condition','traffic_conditions'],np.array([.5,.01]))



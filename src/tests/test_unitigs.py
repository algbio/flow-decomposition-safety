from src.scripts.main import flow_decomposition
from src.scripts.unitigs import get_unitigs
import unittest
import networkx as nx


class MainTest(unittest.TestCase):

    def setUp(self):
        self.nx_simple_graph = nx.DiGraph(source=0, sink=4)

        self.nx_simple_graph.add_edge(1, 2, weight=19, weight_copy=19)
        self.nx_simple_graph.nodes[1]['flow_out'] = 19
        self.nx_simple_graph.nodes[2]['flow_in'] = 19
        self.nx_simple_graph.add_edge(2, 3, weight=19, weight_copy=19)
        self.nx_simple_graph.nodes[2]['flow_out'] = 19
        self.nx_simple_graph.nodes[3]['flow_in'] = 19
        self.nx_simple_graph.add_edge(3, 4, weight=19, weight_copy=19)
        self.nx_simple_graph.nodes[3]['flow_out'] = 19
        self.nx_simple_graph.nodes[4]['flow_in'] = 19
        self.nx_simple_graph.nodes[4]['flow_out'] = 0
        self.nx_simple_graph.add_edge(0, 1, weight=19, weight_copy=19)
        self.nx_simple_graph.nodes[0]['flow_out'] = 19
        self.nx_simple_graph.nodes[0]['flow_in'] = 0
        self.nx_simple_graph.nodes[1]['flow_in'] = 19

        self.nx_graph1 = nx.DiGraph(source=1, sink=11)
        self.nx_graph1.add_edge(1,2, weight=2, weight_copy=2)
        self.nx_graph1.nodes[1]['flow_out'] = 2
        self.nx_graph1.nodes[2]['flow_in'] = 2
        self.nx_graph1.add_edge(2,3, weight=2, weight_copy=2)
        self.nx_graph1.nodes[2]['flow_out'] = 2
        self.nx_graph1.nodes[3]['flow_in'] = 2
        self.nx_graph1.add_edge(3,4, weight=1, weight_copy=1)
        self.nx_graph1.nodes[3]['flow_out'] = 1
        self.nx_graph1.nodes[4]['flow_in'] = 1
        self.nx_graph1.add_edge(4,5, weight=1, weight_copy=1)
        self.nx_graph1.nodes[4]['flow_out'] = 1
        self.nx_graph1.nodes[5]['flow_in'] = 1
        self.nx_graph1.add_edge(5,6, weight=1, weight_copy=1)
        self.nx_graph1.nodes[5]['flow_out'] = 1
        self.nx_graph1.nodes[6]['flow_in'] = 1
        self.nx_graph1.add_edge(6,7, weight=1, weight_copy=1)
        self.nx_graph1.nodes[6]['flow_out'] = 1
        self.nx_graph1.nodes[7]['flow_in'] = 1
        self.nx_graph1.add_edge(3,9, weight=1, weight_copy=1)
        self.nx_graph1.nodes[3]['flow_out'] += 1
        self.nx_graph1.nodes[9]['flow_in'] = 1
        self.nx_graph1.add_edge(9,5, weight=1, weight_copy=1)
        self.nx_graph1.nodes[9]['flow_out'] = 1
        self.nx_graph1.nodes[5]['flow_in'] += 1
        self.nx_graph1.add_edge(5,10, weight=1, weight_copy=1)
        self.nx_graph1.nodes[5]['flow_out'] += 1
        self.nx_graph1.nodes[10]['flow_in'] = 1
        self.nx_graph1.add_edge(10,7, weight=1, weight_copy=1)
        self.nx_graph1.nodes[10]['flow_out'] = 1
        self.nx_graph1.nodes[7]['flow_in'] += 1
        self.nx_graph1.add_edge(7,8, weight=2, weight_copy=2)
        self.nx_graph1.nodes[7]['flow_out'] = 2
        self.nx_graph1.nodes[8]['flow_in'] = 2
        self.nx_graph1.add_edge(8,11, weight=2, weight_copy=2)
        self.nx_graph1.nodes[8]['flow_out'] = 2
        self.nx_graph1.nodes[11]['flow_in'] = 2
        self.nx_graph1.nodes[11]['flow_out'] = 0

    def test_get_unitigs_simple_graph(self):
        fd = flow_decomposition(self.nx_simple_graph)
        result = get_unitigs(fd[0], self.nx_simple_graph)
        self.assertListEqual([[0,1,2,3,4]], result)
    
    def test_get_unitigs_complex_graph(self):
        fd = flow_decomposition(self.nx_graph1)
        result = get_unitigs(fd[0], self.nx_graph1)
        self.assertListEqual([
            [1,2,3], [3,4,5],[5,6,7],[7,8,11]], result)
        
    
    

                    

if __name__ == '__main__':
    unittest.main()

from src.scripts.graph import Graph
import unittest
import networkx as nx


class GraphTest(unittest.TestCase):

    def setUp(self):
        self.nx_simple_graph = nx.DiGraph()

        self.nx_simple_graph.add_edge(1, 2, capacity=19)
        self.nx_simple_graph.nodes[1]['flow_out'] = 19
        self.nx_simple_graph.nodes[2]['flow_in'] = 19
        self.nx_simple_graph.add_edge(2, 3, capacity=19)
        self.nx_simple_graph.nodes[2]['flow_out'] = 19
        self.nx_simple_graph.nodes[3]['flow_in'] = 19
        self.nx_simple_graph.add_edge(3, 4, capacity=19)
        self.nx_simple_graph.nodes[3]['flow_out'] = 19
        self.nx_simple_graph.nodes[4]['flow_in'] = 19
        self.nx_simple_graph.add_edge(0, 1, capacity=19)
        self.nx_simple_graph.nodes[0]['flow_out'] = 19
        self.nx_simple_graph.nodes[1]['flow_in'] = 19

        self.simple_graph = Graph(graph=self.nx_simple_graph, s=0, t=4)
    
    def test_graph_initial_state(self):
        self.assertEqual(self.nx_simple_graph, self.simple_graph.graph)
        self.assertEqual(0, self.simple_graph.s)
        self.assertEqual(4, self.simple_graph.t)
        self.assertEqual([], self.simple_graph.flow_decomposition_paths)
        self.assertEqual([], self.simple_graph.max_safe_paths)
        self.assertEqual({'decomposition': 0, 'safety': 0}, self.simple_graph.times)


    def test_flow_decomposition(self):
        self.assertEqual([[(0, 1), (1, 2), (2, 3), (3, 4)]], self.simple_graph.flow_decomposition())
        self.assertEqual([[(0, 1), (1, 2), (2, 3), (3, 4)]], self.simple_graph.flow_decomposition_paths)
    
    def test_maximum_safe_path(self):
        self.assertEqual([[(0, 1), (1, 2), (2, 3), (3, 4)]], self.simple_graph.maximal_safe_paths())
        self.assertEqual([[(0, 1), (1, 2), (2, 3), (3, 4)]], self.simple_graph.max_safe_paths)

if __name__ == '__main__':
    unittest.main()

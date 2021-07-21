from src.scripts.graph import Graph
import unittest
import networkx as nx


class GraphTest(unittest.TestCase):

    def setUp(self):
        self.nx_graph = nx.DiGraph()

        self.nx_graph.add_edge(1, 2, capacity=19)
        self.nx_graph.nodes[1]['flow_out'] = 19
        self.nx_graph.nodes[2]['flow_in'] = 19
        self.nx_graph.add_edge(2, 3, capacity=19)
        self.nx_graph.nodes[2]['flow_out'] = 19
        self.nx_graph.nodes[3]['flow_in'] = 19
        self.nx_graph.add_edge(3, 4, capacity=19)
        self.nx_graph.nodes[3]['flow_out'] = 19
        self.nx_graph.nodes[4]['flow_in'] = 19
        self.nx_graph.add_edge(0, 1, capacity=19)
        self.nx_graph.nodes[0]['flow_out'] = 19
        self.nx_graph.nodes[1]['flow_in'] = 19

        self.graph = Graph(graph=self.nx_graph, s=0, t=4)
    
    def test_graph_initial_state(self):
        self.assertEqual(self.nx_graph, self.graph.graph)
        self.assertEqual(0, self.graph.s)
        self.assertEqual(4, self.graph.t)
        self.assertEqual([], self.graph.flow_decomposition_paths)
        self.assertEqual([], self.graph.max_safe_paths)
        self.assertEqual({'decomposition': 0, 'safety': 0}, self.graph.times)


    def test_flow_decomposition(self):
        pass 
if __name__ == '__main__':
    unittest.main()

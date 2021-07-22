from logging import setLogRecordFactory
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
        nx_graph1 = nx.DiGraph()
        nx_graph1.add_edge(1,2, capacity=2)
        nx_graph1.nodes[1]['flow_out'] = 2
        nx_graph1.nodes[2]['flow_in'] = 2
        nx_graph1.add_edge(2,3, capacity=2)
        nx_graph1.nodes[2]['flow_out'] = 2
        nx_graph1.nodes[3]['flow_in'] = 2
        nx_graph1.add_edge(3,4, capacity=1)
        nx_graph1.nodes[3]['flow_out'] = 1
        nx_graph1.nodes[4]['flow_in'] = 1
        nx_graph1.add_edge(4,5, capacity=1)
        nx_graph1.nodes[4]['flow_out'] = 1
        nx_graph1.nodes[5]['flow_in'] = 1
        nx_graph1.add_edge(5,6, capacity=1)
        nx_graph1.nodes[5]['flow_out'] = 1
        nx_graph1.nodes[6]['flow_in'] = 1
        nx_graph1.add_edge(6,7, capacity=1)
        nx_graph1.nodes[6]['flow_out'] = 1
        nx_graph1.nodes[7]['flow_in'] = 1
        nx_graph1.add_edge(3,9, capacity=1)
        nx_graph1.nodes[3]['flow_out'] += 1
        nx_graph1.nodes[9]['flow_in'] = 1
        nx_graph1.add_edge(9,5, capacity=1)
        nx_graph1.nodes[9]['flow_out'] = 1
        nx_graph1.nodes[5]['flow_in'] += 1
        nx_graph1.add_edge(5,10, capacity=1)
        nx_graph1.nodes[5]['flow_out'] += 1
        nx_graph1.nodes[10]['flow_in'] = 1
        nx_graph1.add_edge(10,7, capacity=1)
        nx_graph1.nodes[10]['flow_out'] = 1
        nx_graph1.nodes[7]['flow_in'] += 1
        nx_graph1.add_edge(7,8, capacity=2)
        nx_graph1.nodes[7]['flow_out'] = 2
        nx_graph1.nodes[8]['flow_in'] = 2
        nx_graph1.add_edge(8,11, capacity=2)
        nx_graph1.nodes[8]['flow_out'] = 2
        nx_graph1.nodes[11]['flow_in'] = 2
        self.graph1 = Graph(nx_graph1, 1, 11)

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

    def test_graph1_decomposition(self):
        self.assertEqual([[(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 11)], [(1, 2), (2, 3), (3, 9), (9, 5), (5, 10), (10, 7), (7, 8), (8, 11)]]
                        , self.graph1.flow_decomposition())

    def test_graph1_maximal_safepath(self):
        self.assertEqual([[(1, 2), (2, 3), (3, 4), (4, 5)], [(5, 6), (6, 7), (7, 8), (8, 11)], [(1, 2), (2, 3), (3, 9), (9, 5)], [(5, 10), (10, 7), (7, 8), (8, 11)]], self.graph1.maximal_safe_paths())

    def test_graph1_maximal_safepaths_with_different_flow_decomposition(self):
        flow_dec = [[(1,2),(2,3),
                    (3,4),(4,5),
                    (5,10),(10,7),
                    (7,8),(8,11)],
                    [(1,2),(2,3),
                    (3,9),(9,5),
                    (5,6),(6,7),
                    (7,8),(8,11)]]
        result = self.graph1.maximal_safe_paths(flow_dec)
        correct = [[(1, 2), (2, 3), (3, 4), (4, 5)], [(5, 6), (6, 7), (7, 8), (8, 11)], [(1, 2), (2, 3), (3, 9), (9, 5)], [(5, 10), (10, 7), (7, 8), (8, 11)]]
        check_list = [False, False, False, False]
        for (i,r) in enumerate(result):
            for c in correct:
                if r == c:
                    check_list[i] = True
        self.assertEqual([True,True,True,True],check_list)

if __name__ == '__main__':
    unittest.main()

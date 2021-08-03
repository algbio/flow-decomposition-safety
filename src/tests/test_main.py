from src.scripts.main import flow_decomposition, maximal_safety, maximal_safety_indices
import unittest
import networkx as nx


class MainTest(unittest.TestCase):

    def setUp(self):
        self.nx_simple_graph = nx.DiGraph(source=0, sink=4)

        self.nx_simple_graph.add_edge(1, 2, weight=19)
        self.nx_simple_graph.nodes[1]['flow_out'] = 19
        self.nx_simple_graph.nodes[2]['flow_in'] = 19
        self.nx_simple_graph.add_edge(2, 3, weight=19)
        self.nx_simple_graph.nodes[2]['flow_out'] = 19
        self.nx_simple_graph.nodes[3]['flow_in'] = 19
        self.nx_simple_graph.add_edge(3, 4, weight=19)
        self.nx_simple_graph.nodes[3]['flow_out'] = 19
        self.nx_simple_graph.nodes[4]['flow_in'] = 19
        self.nx_simple_graph.add_edge(0, 1, weight=19)
        self.nx_simple_graph.nodes[0]['flow_out'] = 19
        self.nx_simple_graph.nodes[1]['flow_in'] = 19

        self.nx_graph1 = nx.DiGraph(source=1, sink=11)
        self.nx_graph1.add_edge(1,2, weight=2)
        self.nx_graph1.nodes[1]['flow_out'] = 2
        self.nx_graph1.nodes[2]['flow_in'] = 2
        self.nx_graph1.add_edge(2,3, weight=2)
        self.nx_graph1.nodes[2]['flow_out'] = 2
        self.nx_graph1.nodes[3]['flow_in'] = 2
        self.nx_graph1.add_edge(3,4, weight=1)
        self.nx_graph1.nodes[3]['flow_out'] = 1
        self.nx_graph1.nodes[4]['flow_in'] = 1
        self.nx_graph1.add_edge(4,5, weight=1)
        self.nx_graph1.nodes[4]['flow_out'] = 1
        self.nx_graph1.nodes[5]['flow_in'] = 1
        self.nx_graph1.add_edge(5,6, weight=1)
        self.nx_graph1.nodes[5]['flow_out'] = 1
        self.nx_graph1.nodes[6]['flow_in'] = 1
        self.nx_graph1.add_edge(6,7, weight=1)
        self.nx_graph1.nodes[6]['flow_out'] = 1
        self.nx_graph1.nodes[7]['flow_in'] = 1
        self.nx_graph1.add_edge(3,9, weight=1)
        self.nx_graph1.nodes[3]['flow_out'] += 1
        self.nx_graph1.nodes[9]['flow_in'] = 1
        self.nx_graph1.add_edge(9,5, weight=1)
        self.nx_graph1.nodes[9]['flow_out'] = 1
        self.nx_graph1.nodes[5]['flow_in'] += 1
        self.nx_graph1.add_edge(5,10, weight=1)
        self.nx_graph1.nodes[5]['flow_out'] += 1
        self.nx_graph1.nodes[10]['flow_in'] = 1
        self.nx_graph1.add_edge(10,7, weight=1)
        self.nx_graph1.nodes[10]['flow_out'] = 1
        self.nx_graph1.nodes[7]['flow_in'] += 1
        self.nx_graph1.add_edge(7,8, weight=2)
        self.nx_graph1.nodes[7]['flow_out'] = 2
        self.nx_graph1.nodes[8]['flow_in'] = 2
        self.nx_graph1.add_edge(8,11, weight=2)
        self.nx_graph1.nodes[8]['flow_out'] = 2
        self.nx_graph1.nodes[11]['flow_in'] = 2

    def test_flow_decomposition(self):
        self.assertEqual([[0, 1, 2, 3, 4]], flow_decomposition(self.nx_simple_graph))
    
    def test_maximum_safe_path(self):
        self.assertEqual([[0, 1, 2, 3, 4]], maximal_safety(self.nx_simple_graph))

    def test_graph1_decomposition(self):
        self.assertEqual([[1, 2, 3, 4, 5, 6 , 7, 8, 11], [1, 2, 3, 9, 5, 10, 7, 8, 11]]
                        , flow_decomposition(self.nx_graph1))

    def test_graph1_maximal_safetypath(self):
        self.assertEqual([[1, 2, 3, 4, 5], [5, 6, 7, 8, 11], [1, 2, 3, 9, 5], [5, 10, 7, 8, 11]], maximal_safety(self.nx_graph1))

    def test_graph1_maximal_safetypaths_with_different_flow_decomposition(self):
        flow_dec = [[1, 2, 3, 4, 5, 10, 7, 8, 11],
                    [1, 2, 3, 9, 5, 6, 7, 8, 11]]
        result = maximal_safety(self.nx_graph1, flow_dec)
        correct = [[1, 2, 3, 4, 5], [5, 6, 7, 8, 11], [1, 2, 3, 9, 5], [5, 10, 7, 8, 11]]
        check_list = [False, False, False, False]
        for (i,r) in enumerate(result):
            for c in correct:
                if r == c:
                    check_list[i] = True
        self.assertEqual([True,True,True,True],check_list)
    '''
    def test_graph1_maximal_safetyindices_with_different_flow_decomposition(self):
        flow_dec = [[(1,2),(2,3),
                    (3,4),(4,5),
                    (5,10),(10,7),
                    (7,8),(8,11)],
                    [(1,2),(2,3),
                    (3,9),(9,5),
                    (5,6),(6,7),
                    (7,8),(8,11)]]
        result = maximal_safety_indices(self.nx_graph1, flow_dec)
        self.assertListEqual([[(0, 4), (4, 7)], [(0, 4), (4, 7)]], result)
    '''
if __name__ == '__main__':
    
    unittest.main()

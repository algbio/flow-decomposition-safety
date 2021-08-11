from src.scripts.main import flow_decomposition, to_vertex_list
from src.scripts.unitigs import get_unitigs, reverse_enumerator
from src.scripts.io_helper import read_gfa_file
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
        self.nx_graph1.add_edge(2,3, weight=2, weight_copy=2)
        self.nx_graph1.add_edge(3,4, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(4,5, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(5,6, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(6,7, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(3,9, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(9,5, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(5,10, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(10,7, weight=1, weight_copy=1)
        self.nx_graph1.add_edge(7,8, weight=2, weight_copy=2)
        self.nx_graph1.add_edge(8,11, weight=2, weight_copy=2)
        self.nx_graph1.nodes[1]['flow_out'] = 2
        self.nx_graph1.nodes[2]['flow_in'] = 2
        self.nx_graph1.nodes[2]['flow_out'] = 2
        self.nx_graph1.nodes[3]['flow_in'] = 2
        self.nx_graph1.nodes[3]['flow_out'] = 1
        self.nx_graph1.nodes[4]['flow_in'] = 1
        self.nx_graph1.nodes[4]['flow_out'] = 1
        self.nx_graph1.nodes[5]['flow_in'] = 1
        self.nx_graph1.nodes[5]['flow_out'] = 1
        self.nx_graph1.nodes[6]['flow_in'] = 1
        self.nx_graph1.nodes[6]['flow_out'] = 1
        self.nx_graph1.nodes[7]['flow_in'] = 1
        self.nx_graph1.nodes[3]['flow_out'] += 1
        self.nx_graph1.nodes[9]['flow_in'] = 1
        self.nx_graph1.nodes[9]['flow_out'] = 1
        self.nx_graph1.nodes[5]['flow_in'] += 1
        self.nx_graph1.nodes[5]['flow_out'] += 1
        self.nx_graph1.nodes[10]['flow_in'] = 1
        self.nx_graph1.nodes[10]['flow_out'] = 1
        self.nx_graph1.nodes[7]['flow_in'] += 1
        self.nx_graph1.nodes[7]['flow_out'] = 2
        self.nx_graph1.nodes[8]['flow_in'] = 2
        self.nx_graph1.nodes[8]['flow_out'] = 2
        self.nx_graph1.nodes[11]['flow_in'] = 2
        self.nx_graph1.nodes[11]['flow_out'] = 0

    def test_get_unitigs_simple_graph(self):
        fd = flow_decomposition(self.nx_simple_graph)
        enum = enumerate(to_vertex_list(fd[0])[1:-1], start=1)
        pre = lambda out_degree, in_degree: out_degree == 1 and in_degree == 1
        result = get_unitigs(to_vertex_list(fd[0]), self.nx_simple_graph, enum, pre, 1)
        self.assertListEqual([(0,1,2,3,4)], result)
    
    def test_get_unitigs_complex_graph(self):
        fd = flow_decomposition(self.nx_graph1)
        enum = enumerate(to_vertex_list(fd[0])[1:-1], start=1)
        pre = lambda out_degree, in_degree: out_degree == 1 and in_degree == 1
        result = get_unitigs(to_vertex_list(fd[0]), self.nx_graph1, enum, pre, 1)
        self.assertListEqual([
            (1,2,3), (3,4,5),(5,6,7),(7,8,11)], result)
    
    def test_reverse_enumerator(self):
        res = reverse_enumerator([7,8,9,5])
        self.assertListEqual([(3,5), (2,9), (1,8), (0,7)], [(x,y) for (x,y) in res])
        res2 = reverse_enumerator([7,8,9,5], 2)
        self.assertListEqual([(5,5), (4,9), (3,8), (2,7)], [(x,y) for (x,y) in res2])
    
    def test_modified_unitigs_simple(self):
        fd = flow_decomposition(self.nx_simple_graph)
        enum = enumerate(to_vertex_list(fd[0])[1:-1], start=1)
        pre = lambda out_degree, in_degree: out_degree == 1
        result = get_unitigs(to_vertex_list(fd[0]), self.nx_simple_graph, enum, pre, 1)
        self.assertListEqual([(0,1,2,3,4)], result)

    def test_modified_unitigs(self):
        fd = flow_decomposition(self.nx_graph1)
        enum = enumerate(to_vertex_list(fd[0])[1:-1], start=1)
        pre = lambda out_degree, in_degree: out_degree == 1
        result = get_unitigs(to_vertex_list(fd[0]), self.nx_graph1, enum, pre, 1)
        self.assertListEqual([
            (1,2,3), (3,4,5),(5,6,7,8,11)], result)

    def test_modified_rev_unitigs_simple(self):
            fd = flow_decomposition(self.nx_simple_graph)
            enum = reverse_enumerator(to_vertex_list(fd[0])[1:-1], start=1)
            pre = lambda out_degree, in_degree: in_degree == 1
            result = get_unitigs(to_vertex_list(fd[0]), self.nx_simple_graph, enum, pre, -1)
            self.assertListEqual([(0,1,2,3,4)], result)

    def test_modified_rev_unitigs(self):
            fd = flow_decomposition(self.nx_graph1)
            enum = reverse_enumerator(to_vertex_list(fd[0])[1:-1], start=1)
            pre = lambda out_degree, in_degree: in_degree == 1
            result = get_unitigs(to_vertex_list(fd[0]), self.nx_graph1, enum, pre, -1)
            self.assertListEqual([(7,8,11), (5,6,7), (1,2,3,4,5)], result)
                    

if __name__ == '__main__':
    unittest.main()

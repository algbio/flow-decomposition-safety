from src.scripts.io_helper import new_nx_graph, read_gfa_file
import unittest


class ConverterTest(unittest.TestCase):

    def test_new_nx_graph(self):
        edges = [(0,1,{'weight':1}),
                (1,2,{'weight':1}),
                (2,3,{'weight':1})]
        nodes = [(0,{'flow_out':1}),
                (1,{'flow_out':1, 'flow_in':1}),
                (2,{'flow_out':1, 'flow_in':1}),
                (3,{ 'flow_in':1})]
        graph = new_nx_graph(nodes, edges)
        self.assertDictEqual({'source': 0, 'sink': 3}, graph.graph)
        self.assertEqual(3, len(graph.edges))
        self.assertDictEqual({'weight':1}, graph.get_edge_data(0,1))
        self.assertDictEqual({'weight':1}, graph.get_edge_data(1,2))
        self.assertDictEqual({'weight':1}, graph.get_edge_data(2,3))
        self.assertEqual(4, len(graph.nodes))
        self.assertDictEqual({'flow_out':1}, graph.nodes[0])
        self.assertDictEqual({'flow_out':1, 'flow_in':1}, graph.nodes[1])
        self.assertDictEqual({'flow_out':1, 'flow_in':1}, graph.nodes[2])
        self.assertDictEqual({'flow_in':1}, graph.nodes[3])
        
    def test_read_gfa_file(self):
        graphs = read_gfa_file('src/tests/one_graph.gfa')
        self.assertEqual(1, len(graphs))
        self.assertEqual(17, len(graphs[0].edges))
        self.assertEqual(17, len(graphs[0].nodes))
        self.assertEqual(0, graphs[0].graph['source'])
        self.assertEqual(16, graphs[0].graph['sink'])
        graphs = read_gfa_file('src/tests/multiple_graphs.gfa')
        self.assertEqual(5, len(graphs))
if __name__ == '__main__':
    unittest.main()

from src.scripts.converter import edge_to_gfa
import unittest


class ConverterTest(unittest.TestCase):

    def setUp(self):
        # Should these two variables be used in some test?
        sgr_graph = '''
        # graph number = 4 name = ENSG00000187608
        5
        1 2 19.00
        2 3 19.00
        3 4 19.00
        0 1 19.00
        '''
        gfa_graph = '''
        H # graph number = 4 name = ENSG00000187608
        L	1	+	2	+	19M
        L	2	+	3	+	19M
        L	3	+	4	+	19M
        L	0	+	1	+	19M
        '''

    def test_edge_to_gfa(self):
        self.assertEqual('L	0	+	1	+	42M\n', edge_to_gfa('0 1 42.00'))

if __name__ == '__main__':
    unittest.main()

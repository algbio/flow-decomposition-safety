from src.scripts.compare import longest_overlap, number_of_vertices, vertex_coverage
import unittest


class CompareTest(unittest.TestCase):

    def test_longest_overlap(self):
        path1 = [1, 2, 3, 4, 5]
        path2 = [9, 9, 1, 2, 3, 4, 8, 6]
        path3 = [3, 4, 5]
        path4 = [1, 2, 3]
        path5 = [0, 0, 0]
        self.assertEqual(4, longest_overlap(path1, path2))
        self.assertEqual(5, longest_overlap(path1, path1))
        self.assertEqual(3, longest_overlap(path1, path3))
        self.assertEqual(3, longest_overlap(path1, path4))
        self.assertEqual(0, longest_overlap(path1, path5))
    
    def test_number_of_vertices(self):
        graph = [(1, 2, 3, 4, 5), (9, 9, 1, 2, 3, 4, 8, 6), (3, 4, 5)]
        self.assertEqual(8, number_of_vertices(graph))
    
    def test_coverage_vertices(self):
        graph = [(1, 2, 3, 4, 5), (9, 1, 2, 3, 4, 8, 6), (3, 4, 5)]
        self.assertDictEqual({1: 2, 2:2, 3:3, 4: 3, 5:2,
         9:1, 8:1, 6: 1}, vertex_coverage(graph))


if __name__ == '__main__':
    unittest.main()

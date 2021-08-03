from src.scripts.compare import longest_overlap
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

        # What about a test longest_overlap(path1, [0,1,2,8,9,3,4,5,6,7]), it should return 3, the idea of this test is
        # that has two segments that coincide and it should report the longest


if __name__ == '__main__':
    unittest.main()

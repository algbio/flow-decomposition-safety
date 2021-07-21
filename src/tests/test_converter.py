from src.scripts.converter import to_gfa
import unittest

class ConverterTest(unittest.TestCase):

    def test_last_answer_init(self):
        self.assertEqual('L	0	+	1	+	42M\n', to_gfa('0 1 42.00'))


if __name__ == '__main__':
    unittest.main()
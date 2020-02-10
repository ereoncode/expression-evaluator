import unittest
from evaluator import ExpressionEvaluator, ExpressionTreeBuilder


class TestExpressionEvaluator(unittest.TestCase):
    def setUp(self):
        self.ev = ExpressionEvaluator()

    def test_simple_operations(self):
        self.assertEqual(4, self.ev.parse('2 * 2'))
        self.assertEqual(5, self.ev.parse('2 + 3'))
        self.assertEqual(-1, self.ev.parse('3 - 4'))
        self.assertEqual(2, self.ev.parse('6 / 3'))
        self.assertEqual(4.5, self.ev.parse('9 / 2'))
        self.assertEqual(4, self.ev.parse('9 // 2'))
        self.assertEqual(1, self.ev.parse('9 % 2'))
        self.assertEqual(9, self.ev.parse('3 ** 2'))

    def test_nested_expressions(self):
        self.assertEqual(8.5, self.ev.parse('5 + (4 * 3 - 5) / 2'))
        self.assertEqual(3.5, self.ev.parse('-1 * (4 * 3 - 5) / (-2)'))
        self.assertEqual(-3.5, self.ev.parse('-1 * (4 * 3 - 5) / 2'))


class TestExpressionTreeBuilder(unittest.TestCase):
    def setUp(self):
        self.tb = ExpressionTreeBuilder()

    def test_tree_building(self):
        self.assertEqual(('+', 5, ('/', ('-', ('*', 4, 3), 5), 2)), self.tb.parse('5 + (4 * 3 - 5) / 2'))
        self.assertEqual(('+', 5, ('/', ('-', ('*', 4, 3), 5), 2)), self.tb.parse('5 + (4 * 3 - 5) / 2'))
        self.assertEqual(('/', ('*', ('*', -1, 1), ('-', ('*', 4, 3), 5)), 2), self.tb.parse('(-1) * (4 * 3 - 5) / 2'))
        self.assertEqual(('/', ('*', -1, ('-', ('*', 4, 3), 5)), 2), self.tb.parse('- (4 * 3 - 5) / 2'))


if __name__ == '__main__':
    unittest.main()

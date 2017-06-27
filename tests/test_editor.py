# -*- coding: utf-8 -*-

import sys, os, unittest

from gramophone import gp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gramophone')))

class EditorTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True


if __name__ == '__main__':
    unittest.main()

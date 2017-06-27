# -*- coding: utf-8 -*-

import sys, os, unittest

from gramophone import gp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gramophone')))

class EditorTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_constructor(self):
        editor = gp.Editor()
        self.assertIsNotNone(editor)


if __name__ == '__main__':
    unittest.main()

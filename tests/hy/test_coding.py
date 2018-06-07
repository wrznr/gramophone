# -*- coding: utf-8 -*-

import sys, os, pytest

from distutils import dir_util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gramophone')))

from gramophone import hy

def test_constructor():
    coder = hy.Coder()
    assert(coder != None)

def test_encode():
    coder = hy.Coder()

    encodement = coder.encode(u"Maul-ar·beit")
    assert(encodement[0] == "<w>\t<w>\t0\t6")
    assert(encodement[1] == "M\tm\t0\t0")
    assert(encodement[2] == "a\ta\t0\t0")
    assert(encodement[3] == "u\tu\t0\t0")
    assert(encodement[4] == "l\tl\t0\t0")
    assert(encodement[5] == "a\ta\t1\t1")
    assert(encodement[6] == "r\tr\t0\t0")
    assert(encodement[7] == "b\tb\t0\t1")
    assert(encodement[-1] == "</w>\t</w>\t0\t7")

if __name__ == '__main__':
    unittest.main()

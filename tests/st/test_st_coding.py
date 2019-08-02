# -*- coding: utf-8 -*-

import sys, os, pytest

from distutils import dir_util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gramophone')))

from gramophone import st

def test_constructor():
    coder = st.Coder()
    assert(coder != None)

def test_encode():
    coder = st.Coder()

    encodement = coder.encode("ˈhaʊ̯sʔaʁˌbaɪ̯t")
    assert(encodement[0] == "<w>\t6")
    assert(encodement[1] == "h\t1")
    assert(encodement[2] == "a\t0")
    assert(encodement[3] == "ʊ̯\t0")
    assert(encodement[4] == "s\t0")
    assert(encodement[5] == "ʔ\t0")
    assert(encodement[6] == "a\t0")
    assert(encodement[7] == "ʁ\t0")
    assert(encodement[8] == "b\t2")
    assert(encodement[9] == "a\t0")
    assert(encodement[10] == "ɪ̯\t0")
    assert(encodement[11] == "t\t0")
    assert(encodement[-1] == "</w>\t7")

def test_decode():
    coder = st.Coder()

    test_string = "ˈhaʊ̯sʔaʁˌbaɪ̯t"

    assert(coder.decode(coder.encode(test_string)) == test_string)


if __name__ == '__main__':
    unittest.main()

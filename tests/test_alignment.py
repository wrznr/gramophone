# -*- coding: utf-8 -*-

import sys, os, pytest

from distutils import dir_util

from gramophone import gp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gramophone')))


@pytest.fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_constructor():
    aligner = gp.Aligner()
    assert(aligner != None)

def test_loading(datadir):
    aligner = gp.Aligner(mapping=datadir.join('test_alignment.txt'))
    assert(aligner.status == 1)

def test_chain(datadir):
    aligner = gp.Aligner(mapping=datadir.join('test_alignment.txt'))

    chain_fst = aligner.chain(u"aabb")
    chain_fst.draw('/tmp/chain.dot')
    assert(chain_fst.verify())

def test_segment(datadir):
    aligner = gp.Aligner(mapping=datadir.join('test_alignment.txt'))

    seg_fst = aligner.segment(u"aabb")
    seg_fst.draw('/tmp/seg.dot')
    assert(seg_fst.verify())

def test_expand(datadir):
    aligner = gp.Aligner(mapping=datadir.join('test_alignment.txt'))

    exp_fst = aligner.expand(u"aabb")
    exp_fst.draw('/tmp/exp.dot')
    assert(exp_fst.verify())

def test_align(datadir):
    aligner = gp.Aligner(mapping=datadir.join('test_alignment.txt'))

    alignment_fst = aligner.align(u"aabb",u"abbbb")
    alignment_fst.draw('/tmp/alg.dot')
    assert(alignment_fst.verify())



if __name__ == '__main__':
    unittest.main()

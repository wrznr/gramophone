# -*- coding: utf-8 -*-

import sys, os, pytest

from distutils import dir_util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gramophone')))

from gramophone import gp

def test_constructor():
    rater = gp.Rater()
    assert(rater != None)

def test_train():
    rater = gp.Rater()
    rater.train([[['aa', 'b', 'b'], ['a', 'bb', 'bb']], [['aa'], ['a']], [['b', 'a', 'b'], ['bb', 'a', 'bb']]])
    assert(rater.status == 1)

def test_rate():
    rater = gp.Rater()
    rater.train([[['aa', 'b', 'b'], ['a', 'bb', 'bb']], [['aa'], ['a']], [['b', 'a', 'b'], ['bb', 'a', 'bb']]])
    assert(rater.rate([['aa'],['a']]) > 0.0)

def test_save_load():
    rater = gp.Rater()
    rater.train([[['aa', 'b', 'b'], ['a', 'bb', 'bb']], [['aa'], ['a']], [['b', 'a', 'b'], ['bb', 'a', 'bb']]])
    rater.save('/tmp/model.ngram')
    rater2 = gp.Rater.load('/tmp/model.ngram')
    assert(rater.rate([['aa'],['a']]) == rater2.rate([['aa'],['a']]))

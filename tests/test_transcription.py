# -*- coding: utf-8 -*-

import sys, os, pytest

from distutils import dir_util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gramophone')))

from gramophone import gp

def test_constructor():
    transcriber = gp.Transcriber()
    assert(transcriber != None)

def test_train():
    transcriber = gp.Transcriber()
    transcriber.train([[['aa', 'b', 'b'], ['a', 'bb', 'bb']], [['aa'], ['a']], [['b', 'a', 'b'], ['bb', 'a', 'bb']]])
    assert(transcriber.status == 1)

def test_transcribe():
    transcriber = gp.Transcriber()
    transcriber.train([[['aa', 'b', 'b'], ['a', 'bb', 'bb']], [['aa'], ['a']], [['b', 'a', 'b'], ['bb', 'a', 'bb']]])
    print(transcriber.transcribe(['b','a']))
    assert(transcriber.transcribe(['b','a'])==['bb', 'a', '', 'bb', 'bb'])

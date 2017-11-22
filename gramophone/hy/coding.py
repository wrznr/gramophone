# -*- coding: utf-8 -*-

import sys
import regex as re

class Coder:

    def __init__(self):
        """
        The constructor.

        """

        self.clear()
        self.clean_re = re.compile("\s+", re.U)

    def clear(self):
        """
        Clears all internal data.
        """
        pass

    def scan(self,g):
        '''
        Tokenizes a (possibly pre-segmented) grapheme sequence.
        '''

        # return value, beginning of word
        alignment = ["<w>\t<w>\t0"]

        # initial guard
        j = 1
        hint = 0

        # iterate over graphemes
        for i in range(0,len(g)):
            # hyphenation point
            if g[i] == u"·":
                split = 1
                hint = 1
            # hyphen
            elif g[i] == u"-" and i != 0 and i != len(g) - 1:
                hint = 1
            elif special_char_re.match(g[i]):
                alignment.append((g[i],u"'",j,hint))
            else:
                alignment.append((g[i],g[i].lower(),j,hint))
                hint = 0
                j += 1
            
        alignment.append["</w>\t</w>\t0"]
        return alignment

    def align(self,g):
        '''
        Aligns a pre-segmented grapheme sequence for training.
        '''

        # return value, beginning of word
        alignment = ["<w>\t<w>\t0\t6"]

        # initial guard
        j = 1
        split = 0
        hint = 0

        # iterate over graphemes
        for i in range(0,len(g)):
            # hyphenation point
            if g[i] == u"·":
                split = 1
            # hyphen
            elif g[i] == u"-" and i != 0 and i != len(g) - 1:
                split = 1
                hint = 1
            elif special_char_re.match(g[i]):
                alignment.append((g[i],u"'",j,hint,split))
            else:
                alignment.append((g[i],g[i].lower(),j,hint,split))
                split = 0
                hint = 0
                j += 1
            
        alignment.append["</w>\t</w>\t0\t7"]
        return alignment


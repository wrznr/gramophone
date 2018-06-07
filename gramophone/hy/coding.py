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
        self.special_char_re = re.compile("[']", re.U)

    def clear(self):
        """
        Clears all internal data.
        """
        pass

    def decode(self,g):
        '''
        Decodes a labelled hyphenation sequence for printing.
        '''

        output = u""
        for line in g:
            if line:
                fields = line.split(u"\t")
                if fields[-1] == '1':
                    output += u"-"
                    output += fields[0]
                elif fields[-1] == '0':
                    output += fields[0]
        return output


    def encode(self,g,mode="train"):
        '''
        Encodes a (possibly) pre-segmented hyphenation for training.
        '''

        # return value, beginning of word
        encodement = [["<w>","<w>","0","6"]]

        # initial guard
        j = 1
        split = "0"
        hint = "0"

        # iterate over graphemes
        for i in range(0,len(g)):
            # hyphenation point
            if g[i] == u"·":
                split = "1"
            # hyphen
            elif g[i] == u"-" and i != 0 and i != len(g) - 1:
                split = "1"
                hint = "1"
            elif self.special_char_re.match(g[i]):
                encodement.append([g[i],u"'",hint,split])
            else:
                encodement.append([g[i],g[i].lower(),hint,split])
                split = "0"
                hint = "0"
                j += 1
            
        encodement.append(["</w>","</w>","0","7"])
        if mode == "train":
            return ['\t'.join(x) for x in encodement]
        else:
            return ['\t'.join(x[0:-1]) for x in encodement]


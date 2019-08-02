# -*- coding: utf-8 -*-

import sys
import unicodedata
import regex as re

class Coder:

    def __init__(self):
        """
        The constructor.

        """

        self.clear()
        self.special_char_re = re.compile("[']")

    def clear(self):
        """
        Clears all internal data.
        """
        pass

    def decode(self,g):
        '''
        Decodes a labelled stress sequence for printing.
        '''

        output = ""
        for line in g:
            if line:
                fields = line.split("\t")
                if fields[-1] == '1':
                    output += u"ˈ"
                    output += fields[0]
                elif fields[-1] == '2':
                    output += u"ˌ"
                    output += fields[0]
                elif fields[-1] == '0':
                    output += fields[0]
        return output


    def encode(self,g,mode="train"):
        '''
        Encodes a (possibly) pre-segmented hyphenation for training.
        '''

        # return value, beginning of word
        encodement = [["<w>","6"]]

        # initial guard
        stress = "0"
        char = ""

        i = 0
        # iterate over graphemes
        while i < len(g):
            # primary stress
            if g[i] == "ˈ":
                stress = "1"
            # secondary stress
            elif g[i] == "ˌ":
                stress = "2"
            elif self.special_char_re.match(g[i]):
                encodement.append(["'",stress])
                stress = "0"
                char = ""
            else:
                char = g[i]
                while i < len(g) - 1 and (unicodedata.combining(g[i + 1]) or g[i + 1] == 'ː'):
                    i += 1
                    char += g[i]
                encodement.append([char,stress])
                stress = "0"
                char = ""
            i += 1
            
        encodement.append(["</w>","7"])
        if mode == "train":
            return ['\t'.join(x) for x in encodement]
        else:
            return ['\t'.join(x[0:-1]) for x in encodement]


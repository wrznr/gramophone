# -*- coding: utf-8 -*-

import wapiti

patterns = '''
# Unigram
U1+0:%x[0,1]

# Bigram
U1-1:%x[-1,1]
U1+1:%x[1,1]
U2-1:%x[-1,1]/%x[0,1]
U2+0:%x[0,1]/%x[1,1]

# Trigram
U1-2:%x[-2,1]
U1+2:%x[2,1]
U2-2:%x[-2,1]/%x[-1,1]
U2+1:%x[1,1]/%x[2,1]
U3-2:%x[-2,1]/%x[-1,1]/%x[0,1]
U3-1:%x[-1,1]/%x[0,1]/%x[1,1]
U3+0:%x[0,1]/%x[1,1]/%x[2,1]

# 4-gram
U1-3:%x[-3,1]
U1+3:%x[3,1]
U2-3:%x[-3,1]/%x[-2,1]
U2+2:%x[2,1]/%x[3,1]
U3-3:%x[-3,1]/%x[-2,1]/%x[-1,1]
U3+1:%x[1,1]/%x[2,1]/%x[3,1]
U4-3:%x[-3,1]/%x[-2,1]/%x[-1,1]/%x[0,1]
U4-2:%x[-2,1]/%x[-1,1]/%x[0,1]/%x[1,1]
U4-1:%x[-1,1]/%x[0,1]/%x[1,1]/%x[2,1]
U4+0:%x[0,1]/%x[1,1]/%x[2,1]/%x[3,1]

# 5-gram
U1-4:%x[-4,1]
U1+4:%x[4,1]
U2-4:%x[-4,1]/%x[-3,1]
U2+3:%x[3,1]/%x[4,1]
U3-4:%x[-4,1]/%x[-3,1]/%x[-2,1]
U3+2:%x[2,1]/%x[3,1]/%x[4,1]
U4-4:%x[-4,1]/%x[-3,1]/%x[-2,1]/%x[-1,1]
U4+1:%x[1,1]/%x[2,1]/%x[3,1]/%x[4,1]
U5-4:%x[-4,1]/%x[-3,1]/%x[-2,1]/%x[-1,1]/%x[0,1]
U5-3:%x[-3,1]/%x[-2,1]/%x[-1,1]/%x[0,1]/%x[1,1]
U5-2:%x[-2,1]/%x[-1,1]/%x[0,1]/%x[1,1]/%x[2,1]
U5-1:%x[-1,1]/%x[0,1]/%x[1,1]/%x[2,1]/%x[3,1]
U5+0:%x[0,1]/%x[1,1]/%x[2,1]/%x[3,1]/%x[4,1]

#Bigram
B01:%x[0,2]/%x[1,2]
'''

class Labeller:

    def __init__(self):
        '''
        The constructor.
        '''

        self.clear()

    def clear(self):
        '''
        Resets labeller.
        '''

        self.model = wapiti.Model(patterns=patterns,nbest=1)
        self.status = 0


    def train(self, training_data):
        '''
        Trains a crf model.
        '''
        if self.status != 0:
            self.clear()
        
        # parse training data
        for encoded_seq in training_data:
            self.model.add_training_sequence(u"\n".join(encoded_seq))

        # training step
        self.model.train()

        self.status = 1

    def save(self,model_file):
        '''
        Saves a crf model.
        '''
        self.model.save(model_file)

    def load(self,model_file):
        '''
        Loads a previously trained model.
        '''
        self.model = wapiti.Model(model=model_file,nbest=1)
        self.status = 1

    def label(self,encoded_seq):
        if self.status > 0:
            labelled_seqs = []
            labelled_seq = []
            for seg in self.model.label_sequence(u"\n".join(encoded_seq)).split(b"\n"):
                if seg:
                    labelled_seq.append(seg.decode("utf-8"))
                else:
                    labelled_seqs.append(labelled_seq)
                    labelled_seq = []
            if labelled_seq:
                labelled_seqs.append(labelled_seq)
            return labelled_seqs
        else:
            return []

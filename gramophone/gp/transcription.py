# -*- coding: utf-8 -*-

import wapiti

patterns = '''
# Unigram
U1+0:%x[0,0]

# Bigram
U1-1:%x[-1,0]
U1+1:%x[1,0]
U2-1:%x[-1,0]/%x[0,0]
U2+0:%x[0,0]/%x[1,0]

# Trigram
U1-2:%x[-2,0]
U1+2:%x[2,0]
U2-2:%x[-2,0]/%x[-1,0]
U2+1:%x[1,0]/%x[2,0]
U3-2:%x[-2,0]/%x[-1,0]/%x[0,0]
U3-1:%x[-1,0]/%x[0,0]/%x[1,0]
U3+0:%x[0,0]/%x[1,0]/%x[2,0]

# 4-gram
U1-3:%x[-3,0]
U1+3:%x[3,0]
U2-3:%x[-3,0]/%x[-2,0]
U2+2:%x[2,0]/%x[3,0]
U3-3:%x[-3,0]/%x[-2,0]/%x[-1,0]
U3+1:%x[1,0]/%x[2,0]/%x[3,0]
U4-3:%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]
U4-2:%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]
U4-1:%x[-1,0]/%x[0,0]/%x[1,0]/%x[2,0]
U4+0:%x[0,0]/%x[1,0]/%x[2,0]/%x[3,0]

# 5-gram
U1-4:%x[-4,0]
U1+4:%x[4,0]
U2-4:%x[-4,0]/%x[-3,0]
U2+3:%x[3,0]/%x[4,0]
U3-4:%x[-4,0]/%x[-3,0]/%x[-2,0]
U3+2:%x[2,0]/%x[3,0]/%x[4,0]
U4-4:%x[-4,0]/%x[-3,0]/%x[-2,0]/%x[-1,0]
U4+1:%x[1,0]/%x[2,0]/%x[3,0]/%x[4,0]
U5-4:%x[-4,0]/%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]
U5-3:%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]
U5-2:%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]/%x[2,0]
U5-1:%x[-1,0]/%x[0,0]/%x[1,0]/%x[2,0]/%x[3,0]
U5+0:%x[0,0]/%x[1,0]/%x[2,0]/%x[3,0]/%x[4,0]
'''

class Transcriber:

    def __init__(self):
        '''
        The constructor.
        '''

        self.clear()

    def clear(self):
        '''
        Resets transcriber.
        '''

        self.model = wapiti.Model(patterns=patterns,nbest=2)
        self.status = 0


    def train(self, training_data):
        '''
        Trains a crf model.
        '''
        if self.status != 0:
            self.clear()
        
        # parse training data
        for alignment in training_data:
            seq = u"\n".join(u"%s %s" % (alignment[0][i],alignment[1][i]) for i in range(len(alignment[0])))
            #seq = u"\n".join(u"%s %s" % (x,y) for x,y in zip(alignment[0],alignment[1]))
            self.model.add_training_sequence(seq)

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
        self.model = wapiti.Model(model=model_file,nbest=2)
        self.status = 1

    def transcribe(self,graphemes):
        if self.status > 0:
            transcriptions = []
            transcription = []
            for seg in self.model.label_sequence(u"\n".join(graphemes)).decode("utf-8").split("\n"):
                if seg:
                    transcription.append(seg)
                else:
                    transcriptions.append(transcription)
                    transcription = []
            if transcription:
                transcriptions.append(transcription)
            return transcriptions
        else:
            return []

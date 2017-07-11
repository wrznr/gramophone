# -*- coding: utf-8 -*-

import wapiti

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

        self.model = wapiti.Model(patterns="U1+0:%x[0,0]",nbest=2)
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

    @classmethod
    def load(self,model_file):
        '''
        Loads a previously trained model.
        '''
        model = wapiti.Model(model=model_file)
        model.status = 1
        return model

    def transcribe(self,graphemes):
        if self.status > 0:
            return self.model.label_sequence(u"\n".join(graphemes)).decode("utf-8").strip().split(u"\n")
        else:
            return []

# -*- coding: utf-8 -*-

import nltk, pickle

class Rater(object):

    def __init__(self):
        '''
        The constructor.
        '''

        self.clear()

    def clear(self):
        '''
        Resets rater.
        '''

        self.uni = nltk.FreqDist()
        self.bi = nltk.FreqDist()
        self.tri = nltk.FreqDist()
        self.quad = nltk.FreqDist()
        self.quin = nltk.FreqDist()
        self.N = nltk.FreqDist()
        self.lambda1 = 0.0
        self.lambda2 = 0.0
        self.lambda3 = 0.0
        self.lambda4 = 0.0
        self.lambda5 = 0.0
        self.status = 0

    def train(self, training_data):
        '''
        Trains an n-gram model.
        '''
        if self.status != 0:
            self.clear()

        # parse training data, counting n-grams
        for alignment in training_data:
            graphs = ['<','<','<','<']
            graphs.extend(alignment[0])
            graphs.append('>')
            phons = ['<','<','<','<']
            phons.extend(alignment[1])
            phons.append('>')
            for i in range(4,len(phons)):
                self.uni[(graphs[i],phons[i])] += 1
                self.bi[((graphs[i-1],graphs[i]),(phons[i-1],phons[i]))] += 1
                self.tri[((graphs[i-2],graphs[i-1],graphs[i]),(phons[i-2],phons[i-1],phons[i]))] += 1
                self.quad[((graphs[i-3],graphs[i-2],graphs[i-1],graphs[i]),(phons[i-3],phons[i-2],phons[i-1],phons[i]))] += 1
                self.quin[((graphs[i-4],graphs[i-3],graphs[i-2],graphs[i-1],graphs[i]),(phons[i-4],phons[i-3],phons[i-2],phons[i-1],phons[i]))] += 1
                self.N[((graphs[i-4],graphs[i-3],graphs[i-2],graphs[i-1],graphs[i]),(phons[i-4],phons[i-3],phons[i-2],phons[i-1],phons[i]))] += 1
            
        # smoothing
        self.uni = nltk.MLEProbDist(self.uni)
        self.bi = nltk.MLEProbDist(self.bi)
        self.tri = nltk.MLEProbDist(self.tri)
        self.quad = nltk.MLEProbDist(self.quad)
        self.quin = nltk.MLEProbDist(self.quin)

        # lambda estimation
        for ngram in self.N:
            four_gram = ((ngram[0][1],ngram[0][2],ngram[0][3],ngram[0][4]),(ngram[1][1],ngram[1][2],ngram[1][3],ngram[1][4]))
            three_gram = ((ngram[0][2],ngram[0][3],ngram[0][4]),(ngram[1][2],ngram[1][3],ngram[1][4]))
            two_gram = ((ngram[0][3],ngram[0][4]),(ngram[1][3],ngram[1][4]))
            one_gram = (ngram[0][4],ngram[1][4])

            if self.quin.prob(ngram) >= self.quad.prob(four_gram) and self.quin.prob(ngram) >= self.tri.prob(three_gram) and self.quin.prob(ngram) >= self.bi.prob(two_gram) and self.quin.prob(ngram) >= self.uni.prob(one_gram):
                self.lambda5 += self.N.freq(ngram) * self.N.N()
            elif self.quad.prob(four_gram) >= self.tri.prob(three_gram) and self.quad.prob(four_gram) >= self.bi.prob(two_gram) and self.quad.prob(four_gram) >= self.uni.prob(one_gram):
                self.lambda4 += self.N.freq(ngram) * self.N.N()
            elif self.tri.prob(three_gram) >= self.bi.prob(two_gram) and self.tri.prob(three_gram) >= self.uni.prob(one_gram):
                self.lambda3 += self.N.freq(ngram) * self.N.N()
            elif self.bi.prob(two_gram) >= self.uni.prob(one_gram):
                self.lambda2 += self.N.freq(ngram) * self.N.N()
            else:
                self.lambda1 += self.N.freq(ngram) * self.N.N()

        self.lambda5 = self.lambda5 / self.N.N()
        self.lambda4 = self.lambda4 / self.N.N()
        self.lambda3 = self.lambda3 / self.N.N()
        self.lambda2 = self.lambda2 / self.N.N()
        self.lambda1 = self.lambda1 / self.N.N()

        # set status
        self.status = 1

    def save(self,model_file):
        '''
        Saves an ngram model.
        '''
        # pickle to file
        model_f = open(model_file, "wb")
        pickle.dump(self,model_f)

    @classmethod
    def load(self,model_file):
        '''
        Loads a previously trained model.
        '''
        # load from pickle
        model_f = open(model_file, "rb")
        return pickle.load(model_f, encoding="utf-8")

    def rate(self,alignment):
        prob = 1.0
        if self.status > 0:
            graphs = ['<','<','<','<']
            graphs.extend(alignment[0])
            graphs.append('>')
            phons = ['<','<','<','<']
            phons.extend(alignment[1])
            phons.append('>')
            for i in range(4,len(phons)):
                p1 = self.uni.prob((graphs[i],phons[i])) * self.lambda1
                p2 = self.bi.prob(((graphs[i-1],graphs[i]),(phons[i-1],phons[i]))) * self.lambda2
                p3 = self.tri.prob(((graphs[i-2],graphs[i-1],graphs[i]),(phons[i-2],phons[i-1],phons[i]))) * self.lambda3
                p4 = self.quad.prob(((graphs[i-3],graphs[i-2],graphs[i-1],graphs[i]),(phons[i-3],phons[i-2],phons[i-1],phons[i]))) * self.lambda5
                p5 = self.quin.prob(((graphs[i-4],graphs[i-3],graphs[i-2],graphs[i-1],graphs[i]),(phons[i-4],phons[i-3],phons[i-2],phons[i-1],phons[i]))) * self.lambda5
                prob *= (p4 + p3 + p2 + p1)
                #print(prob,p4,p3,p2,p1)
        return prob

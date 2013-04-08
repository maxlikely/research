'''
Created on Oct 25, 2012

@author: timmahrt
'''

import pickle

def loadAPB():
    return pickle.load(open("propbank.pickle", "r"))


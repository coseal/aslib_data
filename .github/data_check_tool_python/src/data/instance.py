'''
Created on Feb 28, 2014

@author: Marius Lindauer
'''
import random
import copy

class Instance(object):
    '''
       benchmark instance with runtime list, feature list and sat/unsat status
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        self._name = name
        self._cost = {} # cost name -> algorithm -> [float]
        self._status = {} # algorithm -> status
        self._cost_vec = []
        self._transformed_cost_vec = []
        self._features = []
        self._features_status = {} # feature step -> status
        self._normed_features = None
        self._ground_truth = {}
        self._weight = 1
        self._feature_group_cost_dict = {} # feature group -> cost
        self._feature_cost_total = 0.0 # float
        self._fold= {} # mapping: repetition -> cv fold split
        self._pre_solved = False
        
    def __str__(self):
        return self._name
        
    def get_name(self):
        return self._name
        
    def finished_input(self, algorithm_list):
        
        avg = lambda x: sum(x)/len(x)
        #only relevant for claspfolio
        #self._cost_vec = [avg(self._cost["runtime"][algo]) for algo in algorithm_list] # ensure the same order in all vectors
        #self._transformed_cost_vec = [avg(self._cost["runtime"][algo]) for algo in algorithm_list] # ensure the same order in all vectors

    def penalize_weight(self, gamma):
        '''
            new weight: weight * gamma
        '''
        self._weight *= gamma

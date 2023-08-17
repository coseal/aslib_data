'''
Created on Jan 15, 2021

@author: Damir Pulatov

Heavily inspired by instance.py created by Marius Lindauer
'''
import random
import copy

class Algorithm(object):
    '''
       algorithm with runtime list and feature list 
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
        self._feature_group_cost_dict = {} # feature group -> cost
        self._feature_cost_total = 0.0 # float
        
    def __str__(self):
        return self._name
        
    def get_name(self):
        return self._name

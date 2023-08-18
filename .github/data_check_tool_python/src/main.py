'''
Created on Feb 28, 2014

@author: Marius Lindauer

'''

import sys
import argparse
import os
import json

import arff

from misc.printer import Printer
from coseal_reader import CosealReader

class Checker(object):
    
    def __init__(self):
        '''
            Constructor
        '''
        pass

        
    def main(self):
        '''
            main method of Checker
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("--dir",dest="dir_", required=True, help="directory path with input files")
        
        args_ = parser.parse_args(sys.argv[1:])
        
        # dummy parameter
        args_.feat_time = -1
        args_.feature_steps = None
        
        reader = CosealReader()
        instance_dict, metainfo, algo_dict = reader.parse_coseal(coseal_dir = args_.dir_, args_=args_)
        
        #inst = "SAT_Competition2009/APPLICATION/SAT07/industrial/anbulagan/hard-unsat/total-10-19-u.cnf"
        #print(instance_dict[inst]._features)
        #print(json.dumps(instance_dict[inst]._features_status, indent=2))
        #print(json.dumps(instance_dict[inst]._status, indent=2))
        
if __name__ == '__main__':
    
    checker = Checker()
    checker.main()
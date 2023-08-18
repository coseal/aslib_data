#!/bin/python

'''
Created on Oct 09, 2014

generates CV splits for a given ASlib Scenario

@author: Marius Lindauer
@contact: lindauer@cs.uni-freiburg.de
'''

import sys
import argparse
import os
import logging
import random
import arff

class CVGenerator(object):
    
    def __init__(self):
        '''
            Constructor
        '''
        logging.basicConfig(level=logging.DEBUG)
        
        self.FOLDS = 10 #number of cv folds
        
    def main(self):
        '''
            main method of CV-Generator
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("--dir",dest="dir_", required=True, help="directory path with input files")
        
        args_ = parser.parse_args(sys.argv[1:])
        
        instances = self.find_instances(args_.dir_)
        splits = self.split_instances(instances)
        self.write_cv(splits)

    def find_instances(self, dir_):
        '''
            looks for feature_values.arff in <dir_> 
            and read the instances
        '''
        
        feature_file = os.path.join(dir_, "feature_values.arff")
        if not os.path.isfile(feature_file):
            logging.error("Have not found: %s" %(feature_file))
            sys.exit(1)
        
        with open(feature_file) as fp:
            arff_dict = arff.load(fp)
        
        instances = set()
        for data in arff_dict["data"]:
            inst_name = str(data[0])
            instances.add(inst_name)
            
        return instances
    
    def split_instances(self, instances):
        '''
            generate CV split
        '''
        
        splits = []
        for i in range(0, self.FOLDS):
            n_split = len(instances) / (self.FOLDS - i)
            split = random.sample(instances, n_split)
            splits.append(split)
            instances = instances.difference(split)
            
        return splits
    
    def write_cv(self, splits):
        '''
            write cv.arff
        '''
        content = {"relation" : "CV_Folds",
                   "attributes": [
                                  ("instance_id", "STRING"),
                                  ("repetition", "NUMERIC"),
                                  ("fold", "NUMERIC")
                                  ],
                   "data": []
                   }
        
        for split, idx in zip(splits, range(1, self.FOLDS+1)):
            for inst_name in split:
                content["data"].append([inst_name, 1, idx])
                
        print(arff.dumps(content))
        
            
if __name__ == '__main__':
    
    gen = CVGenerator()
    gen.main()

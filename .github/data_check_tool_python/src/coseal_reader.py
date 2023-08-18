'''
Created on Sept 24, 2014

@author: Marius Lindauer

Problems:
  * feature cost vs. feature cutoff time ... how to replace ?
'''

import os
import sys
import arff
import yaml 

from misc.printer import Printer
from data.instance import Instance
from data.algorithm import Algorithm

class Metainfo(object):
    '''
        all meta information about an algorithm selection scenario
    '''
    
    
    def __init__(self):
        # listed in description.txt
        self.scenario = None # string
        self.performance_measure = [] #list of strings
        self.performance_type = [] # list of "runtime" or "solution_quality"
        self.maximize = [] # list of "true" or "false"
        self.algorithm_cutoff_time = None # float
        self.algorithm_cutoff_memory = None # integer
        self.features_cutoff_time = None # float
        self.features_cutoff_memory = None # integer
        self.features_deterministic = [] # list of strings
        self.features_stochastic = [] # list of strings
        self.algorithms = [] # list of strings
        self.algorithms_deterministics = [] # list of strings
        self.algorithms_stochastic = [] # list of strings
        self.feature_group_dict = {} # string -> [] of strings
        self.feature_steps = []
        self.algorithm_feature_group_dict = {}
        self.algorithm_feature_steps = []

        # extracted in other files
        self.features = []
        self.algorithm_features = []
        self.ground_truths = {} # type -> [values]
        self.cv_given = False
        
        # command line options
        self.options = None 
        
        
class CosealReader(object):
    
    def __init__(self):
        '''
            Constructor
        '''
        
        self.dir_ = None # directory with all files for parsing
        self.found_files = [] # all found files in self.dir_
        self.read_funcs = {                        
                               "description.txt" : self.read_description,
                               "algorithm_runs.arff" : self.read_algorithm_runs,
                               "feature_costs.arff": self.read_feature_costs,
                               "feature_values.arff": self.read_feature_values,
                               "feature_runstatus.arff": self.read_feature_runstatus,
                               "algorithm_feature_values.arff": self.read_algorithm_feature_values,
                               "algorithm_feature_runstatus.arff": self.read_algorithm_feature_runstatus,
                               "ground_truth.arff": self.read_ground_truth,
                               "cv.arff": self.read_cv                   
                        }

        self.metainfo = Metainfo()
        self.instances = {}
        self.algorithms = {}
        
        
    def parse_coseal(self, coseal_dir, args_):
        '''
            main method of Checker
        '''
        #add command line arguments in metainfo
        self.metainfo.options = args_
        self.dir_ = coseal_dir
        self.find_files()
        self.read_files()
        self.check_feature_status()
        self.remove_features()
        if self.metainfo.algorithm_features:
            self.remove_algorithm_features()
        self.check_instances()
        
        #empty algorithm dict
        algo_dict = dict((algo, "") for algo in self.metainfo.algorithms)
        
        if self.metainfo.options.feat_time == -1:
            self.metainfo.options.feat_time = int(self.metainfo.algorithm_cutoff_time) / 10
        
        return self.instances, self.metainfo, algo_dict
        
    def find_files(self):
        '''
            find all expected files in self.dir_
            fills self.found_files
        '''
        expected = ["description.txt", "algorithm_runs.arff", "feature_values.arff", "feature_runstatus.arff"]
        optional = ["algorithm_feature_values.arff", "algorithm_feature_runstatus.arff", "ground_truth.arff", "feature_costs.arff", "citation.bib", "cv.arff"]
        
        for expected_file in expected:
            full_path = os.path.join(self.dir_,expected_file)
            if not os.path.isfile(full_path):
                Printer.print_e("Not found: %s (has to be added)" %(full_path))
            else:
                self.found_files.append(full_path)
                
        for expected_file in optional:
            full_path = os.path.join(self.dir_,expected_file)
            if not os.path.isfile(full_path):
                Printer.print_w("Not found: %s (maybe you want to add it)" %(full_path))
            else:
                self.found_files.append(full_path)
            
    def read_files(self):
        '''
            iterates over all found files (self.found_files) and 
            calls the corresponding function to validate file
        '''
        for file_ in self.found_files:
            read_func = self.read_funcs.get(os.path.basename(file_))
            if read_func:
                read_func(file_)
        
    def read_description(self, file_):
        '''
            reads description file
            and saves all meta information
        ''' 
        Printer.print_c("Read %s" %(file_))
        
        with open(file_, "r") as fh:
            description = yaml.load(fh)
            
        self.metainfo.scenario = description.get('scenario_id')
        self.metainfo.performance_measure = description.get('performance_measures')

        if not isinstance(description.get('performance_measures'), list):
            Printer.print_e("'performance_measures' has to be list")
            
        self.metainfo.maximize = description.get('maximize')
        if not isinstance(description.get('maximize'), list):
            Printer.print_e("'maximize' has to be list")

        self.metainfo.performance_type = description.get('performance_type')
        if not isinstance(description.get('performance_type'), list):
            Printer.print_e("'performance_type' has to be list")
            
        self.metainfo.algorithm_cutoff_time = description.get('algorithm_cutoff_time')
        self.metainfo.algorithm_cutoff_memory = description.get('algorithm_cutoff_memory')
        self.metainfo.features_cutoff_time = description.get('features_cutoff_time')
        self.metainfo.features_cutoff_memory = description.get('features_cutoff_memory')
        self.metainfo.features_deterministic = description.get('features_deterministic')
        if self.metainfo.features_deterministic is None:
            self.metainfo.features_deterministic = set()
        self.metainfo.features_stochastic = description.get('features_stochastic')
        if self.metainfo.features_stochastic is None:
            self.metainfo.features_stochastic = set()
        self.metainfo.algorithm_features_cutoff_time = description.get('algorithm_features_cutoff_time')
        self.metainfo.algorithm_features_cutoff_memory = description.get('algorithm_features_cutoff_memory')
        self.metainfo.algorithm_features_deterministic = description.get('algorithm_features_deterministic')
        if self.metainfo.algorithm_features_deterministic is None: 
            self.metainfo.algorithm_features_deterministic = set()
        self.metainfo.algorithm_features_stochastic = description.get('algorithm_features_stochastic')
        if self.metainfo.algorithm_features_stochastic is None: 
            self.metainfo.algorithm_features_stochastic = set()
        self.metainfo.algorithms_deterministics = description.get('algorithms_deterministic')
        if self.metainfo.algorithms_deterministics is None:
            self.metainfo.algorithms_deterministics = set()
        self.metainfo.algorithms_stochastic = description.get('algorithms_stochastic')
        if self.metainfo.algorithms_stochastic is None:
            self.metainfo.algorithms_stochastic = set()
        self.metainfo.feature_group_dict = description.get('feature_steps')
        self.metainfo.algorithm_feature_group_dict = description.get('algorithm_feature_steps')
        self.metainfo.feature_steps = description.get('default_steps')

        self.metainfo.algorithms = list(
            set(self.metainfo.algorithms_stochastic).union(
                self.metainfo.algorithms_deterministics))
                  
        if not self.metainfo.scenario:
            Printer.print_w("Have not found SCENARIO_ID")
        if not self.metainfo.performance_measure:
            Printer.print_w("Have not found PERFORMANCE_MEASURE")
        if not self.metainfo.performance_type:
            Printer.print_w("Have not found PERFORMANCE_TYPE")
        if not self.metainfo.maximize:
            Printer.print_w("Have not found MAXIMIZE")
        if not self.metainfo.algorithm_cutoff_time:
            Printer.print_e("Have not found algorithm_cutoff_time")
        if not self.metainfo.algorithm_cutoff_memory:
            Printer.print_w("Have not found algorithm_cutoff_memory")
        if not self.metainfo.features_cutoff_time:
            Printer.print_w("Have not found features_cutoff_time")
            Printer.print_w("Assumption FEATURES_CUTOFF_TIME == ALGORITHM_CUTOFF_TIME ")
            self.metainfo.features_cutoff_time = self.metainfo.algorithm_cutoff_time
        if not self.metainfo.features_cutoff_memory:
            Printer.print_w("Have not found features_cutoff_memory")
        if not self.metainfo.algorithm_features_cutoff_time:
            Printer.print_w("Have not found algorithm_features_cutoff_time")
            Printer.print_w("Assumption ALGORITHM_FEATURES_CUTOFF_TIME == ALGORITHM_CUTOFF_TIME ")
            self.metainfo.algorithm_features_cutoff_time = self.metainfo.algorithm_cutoff_time
        if not self.metainfo.algorithm_features_cutoff_memory:
            Printer.print_w("Have not found algorithm_features_cutoff_memory")
        if not self.metainfo.features_deterministic:
            Printer.print_w("Have not found features_deterministic")
        if not self.metainfo.features_stochastic:
            Printer.print_w("Have not found features_stochastic")
        if not self.metainfo.algorithm_features_deterministic:
            Printer.print_w("Have not found algorithm_features_deterministic")
        if not self.metainfo.algorithm_features_stochastic:
            Printer.print_w("Have not found algorithm_features_stochastic")
        if not self.metainfo.algorithms_deterministics:
            Printer.print_w("Have not found algorithms_deterministics")
        if not self.metainfo.algorithms_stochastic:
            Printer.print_w("Have not found algorithms_stochastic")
        if not self.metainfo.feature_group_dict:
            Printer.print_e("Have not found any feature step")
        if not self.metainfo.algorithm_feature_group_dict:
            Printer.print_w("Have not found any algorithm feature step")
        if not self.metainfo.feature_steps:
            Printer.print_e("Have not found default feature step")   
            
        for step, d in self.metainfo.feature_group_dict.items():
            if  d.get("requires") and not isinstance(d["requires"], list):
                Printer.print_e("'requires' of a feature step (%s) has to be list." %(step))

        if self.metainfo.feature_steps:
            f_groups = set(self.metainfo.feature_group_dict.keys())
            if self.metainfo.algorithm_feature_group_dict:
                algo_f_groups = set(self.metainfo.algorithm_feature_group_dict.keys())
                f_groups = f_groups.union(algo_f_groups)
            if set(self.metainfo.feature_steps).difference(f_groups):
                Printer.print_e("Default feature steps are not listed (%s)" %(set(self.metainfo.feature_steps).difference(f_groups)))   
           
        feature_intersec = set(self.metainfo.features_deterministic).intersection(self.metainfo.features_stochastic)
        if feature_intersec:
            Printer.print_w("Intersection of deterministic and stochastic features is not empty: %s" %(str(feature_intersec)))
        algo_feature_intersec = set(self.metainfo.algorithm_features_deterministic).intersection(self.metainfo.algorithm_features_stochastic)
        if algo_feature_intersec:
            Printer.print_w("Intersection of deterministic and stochastic algorithm features is not empty: %s" %(str(algo_feature_intersec)))
        algo_intersec = set(self.metainfo.algorithms_deterministics).intersection(self.metainfo.algorithms_stochastic)
        if algo_intersec:
            Printer.print_w("Intersection of deterministic and stochastic algorithms is not empty: %s" %(str(algo_intersec)))
        
            
    def read_algorithm_runs(self, file_):
        '''
            read performance file
            and saves information
            add Instance() in self.instances
            add Algorithm() in self.algorithms
            
            unsuccessful runs are replaced by algorithm_cutoff_time if performance_type is runtime
            
            EXPECTED HEADER:
            @RELATION ALGORITHM_RUNS_2013-SAT-Competition

            @ATTRIBUTE instance_id STRING
            @ATTRIBUTE repetition NUMERIC
            @ATTRIBUTE algorithm STRING
            @ATTRIBUTE PAR10 NUMERIC
            @ATTRIBUTE Number_of_satisfied_clauses NUMERIC
            @ATTRIBUTE runstatus {ok, timeout, memout, not_applicable, crash, other}
        '''
        Printer.print_c("Read %s" %(file_))
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        
        if arff_dict["attributes"][0][0] != "instance_id":
            Printer.print_e("instance_id as first attribute is missing in %s" %(file_))
        if arff_dict["attributes"][1][0] != "repetition":
            Printer.print_e("repetition as second attribute is missing in %s" %(file_))    
        if arff_dict["attributes"][2][0] != "algorithm":
            Printer.print_e("algorithm as third attribute is missing in %s" %(file_))
            
        listed_metrics = map(lambda x: x[0], arff_dict["attributes"][3 : 3 + len(self.metainfo.performance_measure)])
        diff_set = set(self.metainfo.performance_measure).difference(listed_metrics)
        if diff_set:
            Printer.print_e("\"%s\" as attribute is missing in %s" %(diff_set, file_))
        
        if arff_dict["attributes"][-1][0] != "runstatus":
            Printer.print_e("runstatus as last attribute is missing in %s" %(file_))
               
        pairs_inst_rep_alg = []
        for data in arff_dict["data"]:
            inst_name = str(data[0])
            repetition = data[1]
            algorithm = str(data[2])
            perf_list = data[3:-1]
            status = data[-1]
            
            inst_ = self.instances.get(inst_name,Instance(inst_name))
            algo_ = self.algorithms.get(algorithm,Algorithm(algorithm))
            
            for p_measure, p_type, perf in zip(self.metainfo.performance_measure, self.metainfo.performance_type, perf_list):       
                if perf is None:
                    Printer.print_e("The following performance data has missing values. Please impute all missing values.\n"+ 
                                    "%s" % (",".join(map(str,data))))
                if p_type == "runtime" and (perf is None or status != "ok"): # if broken run, replace with cutoff time
                    perf = self.metainfo.algorithm_cutoff_time
                inst_._cost[p_measure] = inst_._cost.get(p_measure,{})
                perf_measure_dict = inst_._cost[p_measure]
                perf_measure_dict[algorithm] = perf_measure_dict.get(algorithm,[])
                perf_measure_dict[algorithm].append(max(float(perf),0.00001))
            
            inst_._status[algorithm] = status
            
            self.instances[inst_name] = inst_
            self.algorithms[algorithm.replace('-', '.')] = algo_
            if (inst_name,repetition, algorithm) in pairs_inst_rep_alg:
                Printer.print_w("Pair (%s,%s,%s) is not unique in %s" %(inst_name, repetition, algorithm, file_))
            else:
                pairs_inst_rep_alg.append((inst_name,repetition, algorithm))

    def read_feature_costs(self, file_):
        '''
            reads feature time file
            and saves in self.instances
            
            Expected header:
            @RELATION FEATURE_COSTS_2013-SAT-Competition

            @ATTRIBUTE instance_id STRING
            @ATTRIBUTE repetition NUMERIC
            @ATTRIBUTE preprocessing NUMERIC
            @ATTRIBUTE local_search_probing NUMERIC

        '''
        Printer.print_c("Read %s" %(file_))
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        if arff_dict["attributes"][0][0] != "instance_id":
            Printer.print_e("\"instance_id\" as first attribute is missing in %s" %(file_))
        if arff_dict["attributes"][1][0] != "repetition":
            Printer.print_e("\"repetition\" as second attribute is missing in %s" %(file_)) 
        found_groups = map(str,sorted(map(lambda x: x[0], arff_dict["attributes"][2:])))
        for meta_group in self.metainfo.feature_group_dict.keys():
            if meta_group not in found_groups:
                Printer.print_e("\"%s\" as attribute is missing in %s" %(meta_group, file_))
        
        pairs_inst_rep = []
        for data in arff_dict["data"]:
            inst_name = str(data[0])
            repetition = data[1]
            feature_cost = data[2:]

            inst_ = self.instances.get(inst_name)
            if not inst_:
                Printer.print_w("Instance \"%s\" has feature cost but was not found in algorithm_runs.arff" %(inst_name))
                continue
            
            for cost, f_group in zip(feature_cost,arff_dict["attributes"][2:]):
                inst_._feature_group_cost_dict[str(f_group[0])] = cost
            
            if (inst_name,repetition) in pairs_inst_rep:
                Printer.print_w("Pair (%s,%s) is not unique in %s" %(inst_name,repetition, file_))
            else:
                pairs_inst_rep.append((inst_name,repetition))
        
    def read_feature_values(self, file_):
        '''
            reads feature file
            and saves them in self.instances
            
            Expected Header:
            @RELATION FEATURE_VALUES_2013-SAT-Competition

            @ATTRIBUTE instance_id STRING
            @ATTRIBUTE repetition NUMERIC
            @ATTRIBUTE number_of_variables NUMERIC
            @ATTRIBUTE number_of_clauses NUMERIC
            @ATTRIBUTE first_local_min_steps NUMERIC
        '''
        
        Printer.print_c("Read %s" %(file_))
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        if arff_dict["attributes"][0][0] != "instance_id":
            Printer.print_e("instance_id as first attribute is missing in %s" %(file_))
        if arff_dict["attributes"][1][0] != "repetition":
            Printer.print_e("repetition as second attribute is missing in %s" %(file_))            
        
        feature_set = set(self.metainfo.features_deterministic).union(self.metainfo.features_stochastic)
        
        for f_name in arff_dict["attributes"][2:]:
            f_name = f_name[0]
            self.metainfo.features.append(f_name)
            if not f_name in feature_set:
                Printer.print_e("Feature \"%s\" was not defined as deterministic or stochastic" %(f_name))

        pairs_inst_rep = []
        encoutered_features = []
        for data in arff_dict["data"]:
            inst_name = data[0]
            repetition = data[1]
            features = data[2:]
            
            if len(features) != len(self.metainfo.features):
                Printer.print_e("Number of features in attributes does not match number of found features; instance: %s" %(inst_name))
                
            if not self.instances.get(inst_name):
                Printer.print_w("Instance \"%s\" has features but was not found in performance file" %(inst_name))
                continue
            
            inst_ = self.instances[inst_name]
            
            inst_._features = features #TODO: handle feature repetitions
                
            # not only Nones in feature vector and previously seen
            if reduce(lambda x,y: True if (x or y) else False, features, False) and features in encoutered_features:
                Printer.print_w("Feature vector found twice: %s" %(",".join(map(str,features))))
            else:
                encoutered_features.append(features)
                
            if (inst_name,repetition) in pairs_inst_rep:
                Printer.print_w("Pair (%s,%s) is not unique in %s" %(inst_name,repetition, file_))
            else:
                pairs_inst_rep.append((inst_name,repetition))
                
    def read_feature_runstatus(self, file_):
        '''
            reads run stati of all pairs instance x feature step
            and saves them self.instances
            
            Expected header:
            @RELATION FEATURE_RUNSTATUS_2013 - SAT - Competition
            @ATTRIBUTE instance_id STRING
            @ATTRIBUTE repetition NUMERIC
            @ATTRIBUTE preprocessing { ok , timeout , memout , presolved , crash , other }
            @ATTRIBUTE local_search_probing { ok , timeout , memout , presolved , crash , other }
        '''
        Printer.print_c("Read %s" %(file_))
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        if arff_dict["attributes"][0][0] != "instance_id":
            Printer.print_e("instance_id as first attribute is missing in %s" %(file_))
        if arff_dict["attributes"][1][0] != "repetition":
            Printer.print_e("repetition as second attribute is missing in %s" %(file_))            

        for f_name in arff_dict["attributes"][2:]:
            f_name = f_name[0]
            if not f_name in self.metainfo.feature_group_dict.keys():
                Printer.print_e("Feature step \"%s\" was not defined in feature steps" %(f_name))
                
        if len(self.metainfo.feature_group_dict.keys()) != len(arff_dict["attributes"][2:]):
            Printer.print_e("Number of feature steps in description.txt (%d) and feature_runstatus.arff (%d) does not match." %(len(self.metainfo.feature_group_dict.keys()), len(arff_dict["attributes"][2:-1])))

        pairs_inst_rep = []
        for data in arff_dict["data"]:
            inst_name = data[0]
            repetition = data[1]
            stati = data[2:]
            inst_ = self.instances.get(inst_name)
            if not inst_:
                Printer.print_w("Instance \"%s\" has feature step status but was not found in performance file" %(inst_name))
                continue
                
            if (inst_name,repetition) in pairs_inst_rep:
                Printer.print_w("Pair (%s,%s) is not unique in %s" %(inst_name,repetition,file_))
            else:
                pairs_inst_rep.append((inst_name,repetition))
                
            #===================================================================
            # # if runstatus of feature vector is not always ok, remove feature vector
            # if reduce(lambda x,y: False if ((not x) and y == "ok") else True, stati, False):
            #     inst_._features = None
            #===================================================================
            for status, f_step in zip(stati,arff_dict["attributes"][2:]):
                inst_._features_status[f_step[0]] = status
            
            #inst_ = self.instances[inst_name] = self.instances.get(inst_name, Instance)

    def read_algorithm_feature_values(self, file_):
        '''
            reads algorithm feature file
            and saves them in self.algorithms
            
            Expected Header:
            @RELATION ALGORITHM_FEATURE_VALUES_2013-SAT-Competition

            @ATTRIBUTE algorithm STRING
            @ATTRIBUTE repetition NUMERIC
            @ATTRIBUTE number_of_lines NUMERIC
            @ATTRIBUTE op_bit NUMERIC
        '''
        
        Printer.print_c("Read %s" %(file_))
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        if arff_dict["attributes"][0][0] != "algorithm":
            Printer.print_e("algorithm as first attribute is missing in %s" %(file_))
        if arff_dict["attributes"][1][0] != "repetition":
            Printer.print_e("repetition as second attribute is missing in %s" %(file_))            
        
        feature_set = set(self.metainfo.algorithm_features_deterministic).union(self.metainfo.algorithm_features_stochastic)
        
        for f_name in arff_dict["attributes"][2:]:
            f_name = f_name[0]
            self.metainfo.algorithm_features.append(f_name)
            if not f_name in feature_set:
                Printer.print_e("Feature \"%s\" was not defined as deterministic or stochastic" %(f_name))

        pairs_algo_rep = []
        encoutered_features = []
        for data in arff_dict["data"]:
            algo_name = data[0]
            repetition = data[1]
            features = data[2:]
            
            if len(features) != len(self.metainfo.algorithm_features):
                Printer.print_e("Number of features in attributes does not match number of found features; algorithm: %s" %(algo_name))

            if not self.algorithms.get(algo_name):
                Printer.print_w("Algorithm \"%s\" has features but was not found in performance file" %(algo_name))
                continue
            
            algo_ = self.algorithms[algo_name]
            
            algo_._features = features #TODO: handle feature repetitions
                
            # not only Nones in feature vector and previously seen
            if reduce(lambda x,y: True if (x or y) else False, features, False) and features in encoutered_features:
                Printer.print_w("Feature vector found twice: %s" %(",".join(map(str,features))))
            else:
                encoutered_features.append(features)
                
            if (algo_name,repetition) in pairs_algo_rep:
                Printer.print_w("Pair (%s,%s) is not unique in %s" %(algo_name,repetition, file_))
            else:
                pairs_algo_rep.append((algo_name,repetition))
                
    def read_algorithm_feature_runstatus(self, file_):
        '''
            reads run stati of all pairs algorithm x feature step
            and saves them self.algorithms
            
            Expected header:
            @RELATION ALGORITHM_FEATURE_RUNSTATUS_2013 - SAT - Competition
            @ATTRIBUTE algorithm STRING
            @ATTRIBUTE repetition NUMERIC
            @ATTRIBUTE code { ok , timeout , memout , crash , other }
            @ATTRIBUTE AST { ok , timeout , memout , crash , other }
        '''
        Printer.print_c("Read %s" %(file_))
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        if arff_dict["attributes"][0][0] != "algorithm":
            Printer.print_e("algorithm as first attribute is missing in %s" %(file_))
        if arff_dict["attributes"][1][0] != "repetition":
            Printer.print_e("repetition as second attribute is missing in %s" %(file_))            

        for f_name in arff_dict["attributes"][2:]:
            f_name = f_name[0]
            if not f_name in self.metainfo.algorithm_feature_group_dict.keys():
                Printer.print_e("Feature step \"%s\" was not defined in feature steps" %(f_name))
                
        if len(self.metainfo.algorithm_feature_group_dict.keys()) != len(arff_dict["attributes"][2:]):
            Printer.print_e("Number of feature steps in description.txt (%d) and algorithm_feature_runstatus.arff (%d) does not match." %(len(self.metainfo.algorithm_feature_group_dict.keys()), len(arff_dict["attributes"][2:-1])))

        pairs_algo_rep = []
        for data in arff_dict["data"]:
            algo_name = data[0]
            repetition = data[1]
            stati = data[2:]
            algo_ = self.algorithms.get(algo_name)
            if not algo_:
                Printer.print_w("Algorithm \"%s\" has feature step status but was not found in performance file" %(algo_name))
                continue
                
            if (algo_name,repetition) in pairs_algo_rep:
                Printer.print_w("Pair (%s,%s) is not unique in %s" %(algo_name,repetition,file_))
            else:
                pairs_algo_rep.append((algo_name,repetition))
                
            for status, f_step in zip(stati,arff_dict["attributes"][2:]):
                algo_._features_status[f_step[0]] = status
            
    def read_ground_truth(self,file_):
        '''
            read ground truths of all instances
            and save them in self.instances
            
            @RELATION GROUND_TRUTH_2013-SAT-Competition

            @ATTRIBUTE instance_id STRING
            @ATTRIBUTE SATUNSAT {SAT,UNSAT}
            @ATTRIBUTE OPTIMAL_VALUE NUMERIC
        '''
        
        Printer.print_c("Read %s" %(file_))
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        if arff_dict["attributes"][0][0] != "instance_id":
            Printer.print_e("instance_id as first attribute is missing in %s" %(file_))

        # extract feature names
        for attr in arff_dict["attributes"][1:]:
            self.metainfo.ground_truths[attr[0]] = attr[1]
            
        insts = []                
        for data in arff_dict["data"]:
            inst_name = data[0]
            truth = data[1:]

            inst_ = self.instances.get(inst_name)
            if not inst_:
                Printer.print_w("Instance \"%s\" has ground truths but was not found in performance file" %(inst_name))
                continue
            
            truth_dict = {}
            for truth_name, truth_value in zip(arff_dict["attributes"][1:], truth):
                if type(truth_name[1]) is list:
                    truth_dict[truth_name[0]] = self.metainfo.ground_truths[truth_name[0]].index(truth_value) if truth_value else -1
                else:
                    truth_dict[truth_name[0]] = truth_value

            inst_._ground_truth = truth_dict
                
            if inst_name in insts:
                Printer.print_e("Instance \"%s\" is not unique in %s" %(inst_name,file_))
            else:
                insts.append(inst_name)  
                
    def read_cv(self, file_):
        '''
            read cross validation <file_>
            
            @RELATION CV_2013 - SAT - Competition
            @ATTRIBUTE instance_id STRING
            @ATTRIBUTE repetition NUMERIC
            @ATTRIBUTE fold NUMERIC
        '''
        Printer.print_c("Read %s" %(file_))
        self.metainfo.cv_given = True
        
        with open(file_,"rb") as fp:
            try:
                arff_dict = arff.load(fp)
            except arff.BadNominalValue:
                Printer.print_e("Parsing of arff file failed (%s) - maybe conflict of header and data." %(file_))
        
        if arff_dict["attributes"][0][0] != "instance_id":
            Printer.print_e("instance_id as first attribute is missing in %s" %(file_))
        if arff_dict["attributes"][1][0] != "repetition":
            Printer.print_e("repetition as second attribute is missing in %s" %(file_))
        if arff_dict["attributes"][2][0] != "fold":
            Printer.print_e("fold as third attribute is missing in %s" %(file_))
        
        rep_fold_dict = {}
        all_instances = set(self.instances.keys())
        for data in arff_dict["data"]:
            inst_name = data[0]
            rep = int(data[1])
            fold = int(data[2])
            
            inst_ = self.instances.get(inst_name)
            if not inst_:
                Printer.print_w("Instance \"%s\" has ground truths but was not found in performance file")
                continue   

            all_instances.remove(inst_name)
            inst_._fold[rep] = fold
            fold_distribution = rep_fold_dict.get(rep,{})
            rep_fold_dict[rep] = fold_distribution
            fold_distribution[fold] = fold_distribution.get(fold,0)
            fold_distribution[fold] += 1
            
        for rep, fold_dist in rep_fold_dict.items():
            Printer.print_c("%d-th repetition: %s distribution" %(rep, ",".join(map(str,list(fold_dist.values())))))
        
        if len(all_instances) > 0:
            Printer.print_e("Instances: %s are missing from cv.arff" % ",".join(all_instances))
            
                
    def check_instances(self):
        '''
            check each instances of completeness and soundness
        '''
        Printer.print_c("Check Consistency and Completeness of input data")
        
        n_instances = len(self.instances)
        n_no_feats = 0
        n_unsolvable = 0
        n_unsolvable2 = 0
        n_valid = 0
        n_presolved = 0
        feature_costs = 0
        
        for inst_ in self.instances.values():
            valid = True
            unsolvable =  "ok" not in list(inst_._status.values())
            if unsolvable:
                n_unsolvable += 1
                valid = False
            if not inst_._cost:
                Printer.print_e("Missing algorithm cost for instance \"%s\"" %(inst_._name))
                valid = False
            inst_.finished_input(self.metainfo.algorithms)
            if not inst_._features:
                Printer.print_verbose("Missing features values for instance \"%s\"" %(inst_._name))
                n_no_feats += 1
                valid = False
            if inst_._pre_solved:
                n_presolved += 1
            if valid: 
                n_valid += 1
            times = filter(lambda x: x < self.metainfo.algorithm_cutoff_time, inst_._cost_vec)
            #===================================================================
            # if not times:
            #     n_unsolvable2 += 1
            #===================================================================
            feature_costs += inst_._feature_cost_total
                
            #if not times and not unsolvable:
            #    print(inst_._name)
            #    print(inst_._cost_vec)
            #    print(inst_._status.values())
            #===================================================================
            # if not unsolvable and not times: 
            #     print(inst_)
            #===================================================================
            #if not inst_._feature_runtimes:
            #    Printer.print_e("Miss feature costs for instance %s" %(inst_._name))
            #if not inst_._stati:
            #    Printer.print_e("Miss run status for instance %s" %(inst_._name), type_="w")
            #if not inst_._ground_truth:
            #    Printer.print_e("Miss ground truth for instance %s" %(inst_._name), type_="w")
        
        Printer.print_c("Instances: \t\t %d" %(n_instances))
        Printer.print_c("Incomplete Feature Vector: \t %d" %(n_no_feats))
        Printer.print_c("Unsolvable Instances (status): \t %d" %(n_unsolvable))
        #Printer.print_c("Unsolvable Instances (runtime): \t %d" %(n_unsolvable2))
        Printer.print_c("Valid Instances: \t %d" %(n_valid))
        Printer.print_c("Presolved: \t\t %d" %(n_presolved))
        Printer.print_c("Average Feature Costs on all features: \t %.4f" %(feature_costs / n_instances))
        
        #=======================================================================
        # if n_unsolvable != n_unsolvable2:
        #     Printer.print_w("Number of unsolvable instances regarding status and runtime is not consistent.")
        #=======================================================================
    
        if not n_valid:
            Printer.print_e("Have not found valid instances",-10)
        
    def check_feature_status(self):
        '''
            check that features are Na
        '''
        
        feature_group_dict = self.metainfo.feature_group_dict
        
        for inst_ in self.instances.values():
            not_ok_steps = []
            for step, status in inst_._features_status.items():
                if status.upper() != "OK":
                    not_ok_steps.append(step)
                    
            not_ok_features = []
            for u_step in not_ok_steps:
                not_ok_features.extend(feature_group_dict[u_step]["provides"])
                
            not_ok_index_features = map(lambda x: self.metainfo.features.index(x), not_ok_features)
            
            #===================================================================
            # unused_features = set()
            # for u_step in not_ok_steps:
            #     not_processed_features = feature_group_dict[u_step]
            #     unused_features = unused_features.union(set(not_processed_features))
            #===================================================================
            #not_ok_index_features = sorted(list(map(str,self.metainfo.features).index(un_feature) for un_feature in unused_features), reverse=True)

            ok_index_features = set(range(len(self.metainfo.features))).difference(not_ok_index_features)
            
            warned = False
            for indx in not_ok_index_features:
                if inst_._features[indx] is not None:
                    if not warned:
                        Printer.print_w("Not all features of %s are NA although the corresponding feature step is not OK." %(inst_._name))
                        warned = True
                    #inst_._features[indx] = None
            
            ok_values = [inst_._features[indx] for indx in ok_index_features]
            if None in ok_values: 
                Printer.print_e("Missing Features with status OK: %s." % (inst_._name))
        
    def remove_features(self):
        '''
            inst_dict: instance name -> Instance()
            meta_info: parsed coseal meta information and command line arguments (meta_info.options)
        '''
        
        feature_steps = self.metainfo.options.feature_steps
        feature_group_dict = self.metainfo.feature_group_dict
        algorithm_feature_group_dict = self.metainfo.algorithm_feature_group_dict
        features = None #self.metainfo.options.features
            
        if features: #the user specified a subset of features (disables given feature_steps)
            
            empty_check = set(features).difference(self.metainfo.features)
            if empty_check:
                Printer.print_e("Features (--features [list]) are not defined in data: %s" %(",".join(empty_check)), -2)
            
            unused_features = set(self.metainfo.features).difference(features)
            # find the corresponding feature steps
            feature_steps = set()
            for f in features:
                for f_group, f_list in feature_group_dict.iteritems():
                    if f in f_list["provides"]:
                        feature_steps.add(f_group)
                        
            changed = True
            while changed:
                changed = False
                for step in feature_steps:
                    missing_steps = set(feature_group_dict[step].get("requires",set())).difference(feature_steps)
                    if missing_steps:
                        changed = True
                        feature_steps = feature_steps.union(missing_steps)
                        Printer.print_w("Adding missing feature step because of a pre-condition: %s" %(",".join(missing_steps)))
                        
            unused_steps = set(feature_group_dict.keys()).difference(set(feature_steps))
            Printer.print_c("Used feature steps (%d): %s" %(len(feature_steps), ",".join(feature_steps)))
            
        else:
            if not feature_steps:
                feature_steps = list(self.metainfo.feature_steps) # if no steps are specified, use default
                if self.metainfo.algorithm_feature_group_dict:
                    for key in self.metainfo.algorithm_feature_group_dict.keys():
                        feature_steps.remove(key)
            
            empty_check = set(feature_steps).difference(set(feature_group_dict.keys()))
            if empty_check:
                Printer.print_e("Feature steps (--feature-steps [list]) are not defined in data: %s" %(",".join(empty_check)), -2)

            # check preconditions of features
            available_steps = set()
            used_features = set()
            for step in feature_steps: #TODO: order of feature steps could be an issue
                req_steps = set(feature_group_dict[step].get("requires", set()))
                miss_steps = req_steps.difference(feature_steps)
                if miss_steps:
                    Printer.print_w("Feature Step %s does not met his pre-conditions (%s). Adding feature step to set (but not to feature set!)." %(step, ",".join(miss_steps)))
                
                available_steps.add(step)
                for f in feature_group_dict[step]["provides"]:
                    used_features.add(f) 
                    
                for ms in miss_steps:
                    available_steps.add(ms)
                    for f in feature_group_dict[ms]["provides"]:
                        used_features.add(f)            
                        
            feature_steps = available_steps
            Printer.print_c("Used Feature Steps (%d): %s" % (len(feature_steps), ",".join(feature_steps)))        
            
            unused_features = set(self.metainfo.features).difference(set(used_features))
            unused_steps = set(feature_group_dict.keys()).difference(set(available_steps))
            
        
        Printer.print_nearly_verbose("Remove features: %s\n" %(",".join(unused_features)))
        used_features = set(self.metainfo.features).difference(unused_features)
        Printer.print_c("Used features (%d): %s\n" %(len(used_features), ",".join(used_features)))
        
        if not used_features:
            Printer.print_w("Empty feature set - fall back to default feature set.")
            return False
        
        unused_index_features = sorted(list(map(str,self.metainfo.features).index(un_feature) for un_feature in unused_features), reverse=True)
        
        # remove unused features
        for inst_ in self.instances.values():
            for un_feature_indx in unused_index_features:
                inst_._features.pop(un_feature_indx)
                
        # compute feature costs
        for inst_ in self.instances.values():
            total_cost = 0
            previous_presolved = False
            for f_step in feature_steps:
                if inst_._feature_group_cost_dict.get(f_step) and not previous_presolved: # feature costs are maybe None
                    total_cost += inst_._feature_group_cost_dict[f_step]
                if inst_._features_status[f_step] == "PRESOLVED":
                    previous_presolved = True
            for un_step in unused_steps:        # remove step status if unused 
                del inst_._features_status[un_step]
            
            inst_._feature_cost_total = total_cost
            inst_._pre_solved = "PRESOLVED" in map(lambda x: x.upper(), inst_._features_status.values())
            
        for un_feature_indx in unused_index_features:
            self.metainfo.features.pop(un_feature_indx)        
        
        #=======================================================================
        # if self.metainfo.options.impute == "none":
        #     for inst_ in self.instances.values():
        #         if reduce(lambda x,y: False if ((not x) and y.upper() == "OK") else True, inst_._features_status.values(), False):
        #             inst_._features = None
        #=======================================================================
                    
        return True
        
    def remove_algorithm_features(self):
        '''
            remove unused algorithm features
            algo_dict: algorithm name -> Algorithm()
            meta_info: parsed coseal meta information and command line arguments (meta_info.options)
        '''
        
        feature_steps = self.metainfo.options.feature_steps
        feature_group_dict = self.metainfo.feature_group_dict
        algorithm_feature_group_dict = self.metainfo.algorithm_feature_group_dict
        features = None #self.metainfo.options.features
            
        if features: #the user specified a subset of features (disables given feature_steps)
            
            empty_check = set(features).difference(self.metainfo.algorithm_features)
            if empty_check:
                Printer.print_e("Features (--features [list]) are not defined in data: %s" %(",".join(empty_check)), -2)
            
            unused_features = set(self.metainfo.algorithm_features).difference(features)
            # find the corresponding feature steps
            feature_steps = set()
            for f in features:
                for f_group, f_list in algorithm_feature_group_dict.iteritems():
                    if f in f_list["provides"]:
                        feature_steps.add(f_group)
                        
            changed = True
            while changed:
                changed = False
                for step in feature_steps:
                    missing_steps = set(algorithm_feature_group_dict[step].get("requires",set())).difference(feature_steps)
                    if missing_steps:
                        changed = True
                        feature_steps = feature_steps.union(missing_steps)
                        Printer.print_w("Adding missing feature step because of a pre-condition: %s" %(",".join(missing_steps)))
                        
            unused_steps = set(algorithm_feature_group_dict.keys()).difference(set(feature_steps))
            Printer.print_c("Used feature steps (%d): %s" %(len(feature_steps), ",".join(feature_steps)))
            
        else:
            if not feature_steps:
                feature_steps = list(self.metainfo.feature_steps) # if no steps are specified, use default
                for key in self.metainfo.feature_group_dict.keys():
                    if key in feature_steps:
                        feature_steps.remove(key)
            
            empty_check = set(feature_steps).difference(set(algorithm_feature_group_dict.keys()))
            if empty_check:
                Printer.print_e("Algorithm feature steps (--feature-steps [list]) are not defined in data: %s" %(",".join(empty_check)), -2)

            # check preconditions of features
            available_steps = set()
            used_features = set()
            for step in feature_steps: #TODO: order of feature steps could be an issue
                req_steps = set(algorithm_feature_group_dict[step].get("requires", set()))
                miss_steps = req_steps.difference(feature_steps)
                if miss_steps:
                    Printer.print_w("Algorithm Feature Step %s does not met his pre-conditions (%s). Adding feature step to set (but not to feature set!)." %(step, ",".join(miss_steps)))
                
                available_steps.add(step)
                for f in algorithm_feature_group_dict[step]["provides"]:
                    used_features.add(f) 
                    
                for ms in miss_steps:
                    available_steps.add(ms)
                    for f in algorithm_feature_group_dict[ms]["provides"]:
                        used_features.add(f)            
                        
            feature_steps = available_steps
            Printer.print_c("Used Feature Steps (%d): %s" % (len(feature_steps), ",".join(feature_steps)))        
            
            unused_features = set(self.metainfo.algorithm_features).difference(set(used_features))
            unused_steps = set(algorithm_feature_group_dict.keys()).difference(set(available_steps))
            
        
        Printer.print_nearly_verbose("Remove features: %s\n" %(",".join(unused_features)))
        used_features = set(self.metainfo.algorithm_features).difference(unused_features)
        Printer.print_c("Used features (%d): %s\n" %(len(used_features), ",".join(used_features)))
        
        if not used_features:
            Printer.print_w("Empty feature set - fall back to default feature set.")
            return False
        
        unused_index_features = sorted(list(map(str,self.metainfo.algorithm_features).index(un_feature) for un_feature in unused_features), reverse=True)
        
        # remove unused features
        for algo_ in self.algorithms.values():
            for un_feature_indx in unused_index_features:
                algo_._features.pop(un_feature_indx)
                
        # compute feature costs
        for algo_ in self.algorithms.values():
            total_cost = 0
            for f_step in feature_steps:
                if algo_._feature_group_cost_dict.get(f_step): # feature costs are maybe None
                    total_cost += algo_._feature_group_cost_dict[f_step]
            for un_step in unused_steps:        # remove step status if unused 
                del algo_._features_status[un_step]
            
            algo_._feature_cost_total = total_cost
            
        for un_feature_indx in unused_index_features:
            self.metainfo.features.pop(un_feature_indx)        
        
        return True

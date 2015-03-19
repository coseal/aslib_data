source: An Algorithm Selection Benchmark for the Container Pre-Marshalling Problem
authors: K. Tierney and Y. Malitsky (features) / K. Tierney and D. Pacino and S. Voss (algorithms)
translator in coseal format: K. Tierney

This is an extension of the 2013 premarshalling dataset that includes more features and a set of test instances. 

There are three sets of features:

feature_values.arff contains the full set of features from iteration 2 of our latent feature analysis (LFA) process (see paper)
feature_values_itr1.arff contains only the features after iteration 1 of LFA
feature_values_orig.arff containers the features used in PREMARHSALLING-ASTAR-2013

We also provide test data with an identical naming scheme (see _test). 

The features for the pre-marshalling problem are all extremely easy and fast to
compute, thus the feature_costs.arff file has been omitted, as it would be time
0 for every feature (regardless of using original, iteration 1 or iteration 2
features).

The feature computation code is available at https://bitbucket.org/eusorpb/cpmp-as

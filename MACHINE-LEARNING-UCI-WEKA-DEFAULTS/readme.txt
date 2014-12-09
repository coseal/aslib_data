source: http://www.openml.org
authors: J. Vanschoren
translator in coseal format: J. Vanschoren with help from M. Lindauer and B. Bischl
Instances are all machine learning datasets from the UCI reposity, reformatted in the ARFF format. They can be found by searching OpenML.
Algorithms are all classification algorithms from the WEKA workbench, version 3.4.8. WEKA is available at http://www.cs.waikato.ac.nz/ml/weka/

The scenario is supervised classification on tabular data. Classification algorithms (classifiers) build a model predicting q target variable based on a set of descriptive features. Models are evaluated by splitting the data into a training and a test set, training the model on the training data and testing it on the test data. A cross-validation procedure is used to more accurately estimate the real performance. 

The algorithms are evaluated in different ways, including runtime, predictive accuracy, but also measures such as precision and recall. See OpenML for complete descriptions.

Algorithms were run on a PBS computing cluster with a maximal walltime of 3 days and the maximum memory available in each node, typically 4GB. Timeouts and OutOfMemories are indicated in the feature_runstatus. More frequent are NA's where the algorithm was not able to process the data, for instance because it cannot handle nominal features or missing values.  

Features are a relatively small subset of meta-learning features such as statistical and information-theoretic properties of the data distribution. It also include landmarkers, i.e. the performances of simplified classifiers run on the datasets. We plan to add a considerably larger set of features in the near future. Code for computing the features can be found on https://github.com/openml/OpenML/tree/master/Java

No feature costs were recorded. Future updates will include them. Some feature calculations crashed, typically because they were not applicable (e.g., datasets with only nominal values).

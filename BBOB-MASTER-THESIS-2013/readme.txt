source: manually generated as part of a master thesis
authors: P. Kerschke
translator in coseal format: P. Kerschke
The data was generated as part of a master thesis.
Each instance is described by a dimension (2, 3, 5, 10, 20), a function id (1 - 24) and an instance id (1 - 10).
The algorithms that were used, were basically run in their default settings (from R).
In that data set, a run was considered to be successful if it approached the optimum up to a threshold of 10^-1.
The ERT (expected run time) of the algorithms was calculated on ten repetitions per instance.
The relERT (relative ERT) used par10 for the algorithms that did not find the optimum in any of its ten repetitions.
A run is considered to be "ok", if at least one of the ten repetitions found the optimum, otherwise it was stopped because of a "timeout".
The feature values were calculated independently from the algorithm runs.
Some of the features resulted in NAs, e.g. due to dividing by zero. As those NAs result from mathematical problems, they were marked as "other".
Each instance is replicated ten times as well - in order to respect the stochastic properties of some of the ELA features.
The features are the ELA features as described in "Exploratory Landscape Analysis" by O. Mersmann et al. (2011).

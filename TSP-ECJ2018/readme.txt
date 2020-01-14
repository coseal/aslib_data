Source: ECJ-paper 2018 (Leveraging TSP Solver Complementarity through Machine Learning, Evolutionary Computation, December 2018)
Authors: P. Kerschke, L. Kotthoff, J. Bossek, H. Hoos, H. Trautmann
Date: 16.05.2019
Translator in coseal format: P. Kerschke

This data was generated as part of the aforementioned ECJ publication.
Note that all our features were listed as deterministic (which actually is not true for all of them) and only computed once per instance. Hence, the feature values and costs on the remaining replications are just duplicates of the values / costs of the first instance.

If one wants to reproduce the experiments from our paper, one has to aggregate the algorithm runs accordingly, i.e., if at least 6 out of 10 replications were successful, the MEDIAN of all 10 runtimes was used -- which is equivalent to taking the arithmetic mean of the 5th and 6th best runtime of the 10 corresponding ones. Furthermore, the corresponding aggregated runstatus was set to "ok".
Otherwise (i.e., if at most 5 of the 10 replications were successful), the algorithm was defined "unsuccessful" on that instance and hence, runtime = walltime = 3600s and runstatus = "timeout".

Also, note that the pihera-features for the tsplib-instance "att532" could not be computed, because that instance has edge weight type "ATT", but the pihera features can only handle TSP problems with Euclidean edge weights.
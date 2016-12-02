Source: LION-paper 2015 (Improving the State of the Art in Inexact TSP Solving using Per-Instance Algorithm Selection, Learning and Intelligent OptimizatioN 9, Lille, France, January 2015)
Authors: L. Kotthoff, P. Kerschke, H. Hoos, H. Trautmann
Date: 13.02.2015
Translator in coseal format: P. Kerschke

This data was generated for a publication as part of the LION2015.
Note that the feature group ubc_cheap is a subgroup of ubc_all.
Also, the features that belong to ubc_all or tspmeta were considered as deterministic (which actually is not true for all of them) and only computed once per instance. Hence, the feature values and costs on the remaining replications are just duplicates of the values / costs of the first instance.
On the other hand, the features that belong to eax_probing are stochastic and were handled as such.

If one wants to reproduce the experiments from the aforementioned paper, one has to aggregate the algorithm runs accordingly, i.e., if at least 6 out of 10 replications were successful, the MEDIAN of all 10 runtimes was used (and the corresponding aggregated runstatus was set to "ok"), otherwise the algorithm was unsuccessful (i.e., runtime = walltime = 3600s and runstatus = "timeout").

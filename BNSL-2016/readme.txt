source: http://bnportfolio.cs.helsinki.fi/
authors: B. Malone, K. Kangas, M. Jarvisalo, M. Koivisto, P. Myllymaki
translator in coseal format: K. Kangas

The problem concerns score-based structure learning in Bayesian networks. Specifically, the input consists of a number of variables (network nodes) and a list of candidate parent sets associated with real-valued scores. The task is to choose a set of parent nodes for each variable so that the resulting directed graph is acyclic and the total score of the parent sets is maximized.

The included algorithms are all exact, that is, they are guaranteed to terminate in a finite number of steps and output the score of an optimal network. The algorithms are also deterministic: the number of computational steps is determined by the input alone.

The performance of the algorithms is measured as the runtime. Failed runs (timeout or memout) count as the cutoff time of 7200 seconds.

The included solvers are:

- URLearning: http://url.cs.qc.cuny.edu/software/URLearning.html

an A* search based solver, with three variants, labeled astar-ec, astar-ed3, and astar-comp.

- GOBNILP: https://www.cs.york.ac.uk/aig/sw/gobnilp/

an integer linear programming based solver, with two versions 1.4.1 and 1.6.2. We consider both a default configuration and an alternative configuration, resulting in four variants, ilp-141, ilp-141-nc, ilp-162, ilp-162-nc.

- CPBayes: https://cs.uwaterloo.ca/~vanbeek/Research/research_ml.html

a constraint programming based solver, with a single default configuration, cpbayes.

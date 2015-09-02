Authors
=======

Roberto Amadini (amadini@cs.unibo.it)
Jacopo Mauro (jmauro@cs.unibo.it)


Sources
=======

MiniZinc 1.6 benchmarks (http://www.minizinc.org/g12distrib.html)
MiniZinc Challenge 2012 (http://www.minizinc.org/challenge2012/results2012.html)


Dataset
=======

The dataset is a collection of 2670 COP instances encoded in MiniZinc format.
Precisely:
  * 2618 come from MiniZinc 1.6 benchmarks
  * 52   come from MiniZinc Challenge 2012
  
  
The data does not distinguish between timeouts, out-of-memory, crashes, or other
issues: just the "other" runstatus is set when a solver gives no answer before 
the timeout expires. Thus, the runstatus will be in {ok, other}.


Features
========

For every instance of the dataset we generate a set of 155 features by using the 
mzn2feat extractor available at http://www.cs.unibo.it/~amadini/sac_2014.zip
and described in [1]. Note that:
  * features are not scaled and some of them are constants over all the dataset;
  * the runstatus for features is always "ok" since:
    - we discarded from the dataset all the instances already solved during the 
      feature computation;
    - we discarded from the dataset all the instances for which the whole 
      extraction failed (e.g., due to timeout or memory issues);
    - if the extraction of a number n < 155 of features fails, we simply assign 
      to each of such features the default value -1.
      
Note that the version of mzn2feat used in these experiments is currently 
replaced by mzn2feat-1.0. For more details, please see: 
  
  https://github.com/jacopoMauro/mzn2feat

  
Algorithms
==========

We used 12 different solvers that attended the MiniZinc Challenge 2012, namely: 
bprolog, fzn2smt, g12cpx, g12fd, g12lazyfd, g12mip, gecode, izplus, jacop, 
minisatid, mistral, and ortools. We used all of them with their default 
parameters, their global constraint redefinitions when available, and keeping 
track of their performances on every instance of the dataset within a timeout 
T = 900 seconds. For each pair (problem, solver) we define two performance 
measures:
  * score: 1 if the solver solves the problem within T seconds;
           0 if the solver does not give any answer for the problem in T sec.;
           otherwise, a value in [0.25, 0.75] linearly dependent on the distance
           between the best solution found by solver and the best solutions 
           found by every other available solver.
  *  time: t if the solver solves the problem in t < T seconds, T otherwise.

where a solver solves a problem if and only if it completes the search for such 
problem, i.e., it finds an optimal solution and proves its optimality, it proves
that the problem is unsatisfiable, or that it is unbounded. For more details 
about the score metric we refer the reader to [2].

Note that the dataset contains also 4 problems not solvable by any solver. 
Such problems are marked with "?" in ground_truth.arff file.
  
  
Environment
===========

We computed the runtimes on Intel Dual-Core 2.93GHz computers with 3 MB of 
CPU cache, 2 GB of RAM, and Ubuntu 12.04 operating system. The runtimes refer to 
the CPU time, computed by exploiting the Unix "time" command.


References
==========

[1] Roberto Amadini, Maurizio Gabbrielli, Jacopo Mauro:
    An enhanced features extractor for a portfolio of constraint solvers. 
    SAC 2014: 1357-1359

[2] Roberto Amadini, Maurizio Gabbrielli, Jacopo Mauro:
    Portfolio Approaches for Constraint Optimization Problems. 
    LION 2014: 21-35
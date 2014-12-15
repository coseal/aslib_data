Authors
=======

Roberto Amadini (amadini@cs.unibo.it)
Jacopo Mauro (jmauro@cs.unibo.it)


Sources
=======

Third International CSP Solver Competition (http://cpai.ucc.ie/08/)
MiniZinc 1.6 benchmarks (http://www.minizinc.org/g12distrib.html)
MiniZinc Challenge 2012 (http://www.minizinc.org/challenge2012/results2012.html)


Dataset
=======

The dataset is a collection of 4642 CSP instances encoded in MiniZinc format.
Precisely:
  * 3538 come from CSP Solver Competition (converted by means of xcsp2mzn tool, 
    available at https://github.com/jacopoMauro/mzn2feat)
  * 6    come from MiniZinc Challenge 2012
  * 1098 come from MiniZinc 1.6 benchmarks
  
The data does not distinguish between out-of-memory, crashes, or other: just the 
"other" runstatus is set when a solver gives no answer on a certain instance 
before the timeout expires. Thus, the runstatus will be in {ok, timeout, other}.


Features
========

For every instance of the dataset we generate a set of 155 features by using the 
mzn2feat extractor available at http://www.cs.unibo.it/~amadini/sac_2014.zip
Note that:
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

We used 11 different solvers that attended the MiniZinc Challenge 2012, namely: 
bprolog, fzn2smt, g12cpx, g12fd, g12lazyfd, g12mip, gecode, izplus, minisatid, 
mistral, and ortools. We used all of them with their default parameters, their 
global constraint redefinitions when available, and keeping track of their 
performances on every instance of the dataset within a timeout T = 1800 seconds.
For each pair (problem, solver) we defined two performance measures:
  * solved: 1 if the solver solves the problem within T seconds, 0 otherwise;
  *   time: t if the solver solves the problem in t < T seconds, T otherwise.

Note that the dataset contains also 944 problems not solvable by any solver. 
Such problems are marked with "?" in ground_truth.arff file.
  
  
Environment
===========

We computed the runtimes on Intel Dual-Core 2.93GHz computers with 3 MB of 
CPU cache, 2 GB of RAM, and Ubuntu 12.04 operating system. The runtimes refer to 
the CPU time, computed by exploiting the Unix "time" command.
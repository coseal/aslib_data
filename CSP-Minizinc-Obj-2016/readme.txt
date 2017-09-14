source: http://www.minizinc.org/challenge2016/results2016.html
authors: Rolf-David Bergdoll

Performances of the 2016 MiniZinc Challenge ('Free Search' Category) based on
the provided objective values.

All algorithms and instances of this category are used.

The scenario provides two measurements:
- obj: the objective value taken from the challenge website normalized to
  values between 0 and 1, with 0 being the value of the best performance
  and 1 the worst. Timeouts also were measured as 1.
  For instances, where no solution exists, all solvers that performed a
  complete search were assigned 0.
- time (PAR1): the solver runtimes as recorded on the challenge website.

The features were obtained using mzn2feat 
(https://github.com/CP-Unibo/mzn2feat).
For one problem group ('nfc'), the tool terminated with an error message in
our experiments ('MiniZinc: type error:...'). Those instances are therefore
marked as 'crash' in feature_runstatus.arff.

To record runtimes of the feature computations, runsolver was used: 
http://www.cril.univ-artois.fr/~roussel/runsolver/

Part of Open Algorithm Challenge 2017 (Camilla for "obj" and Caren for "time")

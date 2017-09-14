source: http://www.minizinc.org/challenge2016/results2016.html
authors: Rolf-David Bergdoll

PAR10 performances of the 2016 MiniZinc Challenge ('Free Search' Category).

In order to translate the results of the competition into PAR10 scores, we only
considered an instance solved, if the search was complete (status 'C' or 'SC'
in the competition results). Incomplete searches (status 'S') were counted as
timeouts.

We considered all solvers participating in the 'Free Search' category; two of
them were removed from the scenario, since they did not solve any instance.

The features were obtained using mzn2feat: 
https://github.com/CP-Unibo/mzn2feat
For one problem group ('nfc'), the tool terminated with an error message in
our experiments ('MiniZinc: type error:...'). Those instances are therefore
marked as 'crash' in feature_runstatus.arff.

To record runtimes of the feature computations, runsolver was used: 
http://www.cril.univ-artois.fr/~roussel/runsolver/

Part of Open Algorithm Challenge 2017 (Camilla for "obj" and Caren for "time")
authors: Rolf-David Bergdoll

This scenario contains 10 modern SAT solvers run on 2000 industrial instances
of SAT-Competitions.

The algorithms were selected based on their performance on the industrial track
of the 2016 SAT-Competition (http://baldur.iti.kit.edu/sat-competition-2016/).
More precisely, we built the portfolio of 10 algorithms step by step, by adding
the one which would improve the PAR10 score of the virtual best solver the most.
Solvers with license restrictions were not taken into account.

The instances are compiled of the industrial instance sets from the
SAT-Competitions of 2003 to 2016 (http://www.satcompetition.org/). Duplicate 
instances were removed by comparing the feature vectors of all instances, which
might however also have removed some instances that simply had the same
features.

The features were generated using two different sources:
- The feature computation tool of SATzilla 2012, which we also used to remove
  instance duplicates (http://www.cs.ubc.ca/labs/beta/Projects/SATzilla/).
- The tool provided by the International Center of Computationla Logic
  (http://tools.computational-logic.org/content/evaluation.php). To distinguish
  those features from the SATzilla ones, we gave all their identifiers the
  prefix "tud_" for this scenario.

To record runtimes and to enforce memory limits for algorithm runs and feature
computations, runsolver was used. 
http://www.cril.univ-artois.fr/~roussel/runsolver/

Run status 'crash' marks algorithm and feature runs, that terminated within
time and memory limits without usable output.

Part of Open Algorithm Challenge 2017 ("Sora").
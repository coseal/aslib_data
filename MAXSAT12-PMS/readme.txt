source: COSEAL Portfolio Benchmark
authors: Carlos Ansotegui, Yuri Malitsky, Meinolf Sellmann
translator into coseal format: Yuri Malitsky

The data does not distinguish between timeout, memout or crashes!
The status file will only have ok, timeout, or out of memory!

This data is a collection of random, crafted and industrial Unweighted MaxSAT instances 
from the 2012 Evaluation (http://maxsat.ia.udl.cat:81/12/benchmarks/index.html) 
There are a total of 876 instances each of which is defined by 37 features and solved
with 6 state-of-the-art solvers from 2012 (akmaxsat_ls, akmaxsat, DSWPM1_924, pwbo2.1, 
qmaxsat0.21comp, qmaxsat0.21g2comp). 

The best single solver, qmaxsat0.21g2comp, solves 674 instances with a PAR10 score of 4,893 
while the virtual best of all 6 solvers finishes 747 instances with a PAR10 score 
of 3,128.

The features computed using an in house developed tool and are based on a version of UBC SAT 
features and provide the following:

Problem Size Features:
	[1-2]	Number of variables and clauses in original formula: denoted v and c, respectively
	[3] 	Percentage of Soft Clauses
	[4-7]	Soft Clause Weights: mean, stdev, min and max
	[8] 	Ratio of variables to clauses

Variable-Clause Graph Features:
	[9-13]	Variable node degree statistics: mean, stdev, min, max, spread
	[14-18] Clause node degree statistics: mean, stdev, min, max, spread
	
Balance Features:
	[19-23]	Positive to negative occurrences of each variable: mean, stdev, min, max, spread
	[24-28] Positive to negative literals in each clause: mean, stdev, min, max, spread
	[29-31] Fraction of unary, binary and ternary clauses

Proximity to Horn Formula:
	[32-36] Occurrences of a variable in a Horn clause: mean, stdev, min, max, spread
	[37]	Fraction of Horn clauses


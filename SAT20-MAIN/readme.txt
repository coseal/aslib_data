source: https://satcompetition.github.io/2020/
translator in coseal format: Marie Anastacio, Théo Matricon

This dataset contains all the solvers and instances of the main track of the SAT 2020 competition.

Features have been extracted using the extractor of SATzilla with a timeout of 1 minute for each feature category.

An algorithm and configuration pair is given name algorithm+configuration.

OutOfMemory errors are tagged as memout while other errors are marked as crash.
There is no disctinction between timeout (wallclock) and timeout (cpu), both are marked as timeout.
Indeterminate runs were marked as other.

Errors in result are marked as timeout and incorrect results are maked as other.
For both these cases times are set to the cutoff time.
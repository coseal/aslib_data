source: Proteus: A Hierarchical Portfolio of Solvers and Transformations
authors: Barry Hurley, Lars Kotthoff, Yuri Malitsky, Barry O'Sullivan
translator in coseal format: Barry Hurley


This data set includes performance data of four CSP solvers and six SAT solvers
on three SAT encodings on problem instances from the CSP solver competitions. In
total there are 4021 XCSP instances involving global and intensional
constraints, 1974 are solved during feature computation, and 554 instances are
not solved by any CSP or SAT method. This leaves 1493 challenging instances
which were used for the above paper; the entire set with appropriate annotations
is included here for completeness.

The original CSP benchmarks are available from:
http://www.cril.univ-artois.fr/~lecoutre/benchmarks.html

The CSP solvers used are:
- Abscon [Lecoutre and Tabary 2008]
- Choco 2 [Choco Team 2008]
- Gecode [Gecode Team 2006]
- Mistral [Hebrard 2008]

The SAT solvers used are:
– clasp [Gebser et al 2007]
– cryptominisat [Soos 2011]
- glucose [Audemard and Simon 2013]
– lingeling [Biere 2013]
– riss [Manthey 2013]
– MiniSat [Een and Sorensson 2013]

The three SAT encodings are the direct (also known as the sparse), support (or
AC encoding), and the direct-order (also known as the regular encoding).

The CSP features are those used in CPHydra [O'Mahony et al 2008], prefixed with
'csp'. Features of each of the SAT encodings are computed using the base
SATzilla [Xu et al 2008] feature set and are prefixed by the encoding name.

Note that the computation time for the SAT-based features includes the time to
encode the instance, therefor if the portfolio chooses to subsequently use this
encoding, it will double count the time to encode the instance. But this allows
for the possibility of using features from one encoding to make the solver
selection decision under another encoding.

Features for instances containing the cumulative constraint are missing since it
is not supported in Mistral which is used for the CSP feature computation, nor
is there a SAT encoding implemented for this. But it is supported by other CSP
solvers.



References:

Audemard, G., Simon, L.: Glucose 2.3 in the SAT 2013 Competition. Proceedings of
SAT Competition 2013 p. 42 (2013)

Biere, A.: Lingeling, Plingeling and Treengeling Entering the SAT Competition
2013. Proceedings of SAT Competition 2013 (2013)

Choco Team: Choco: an Open Source Java Constraint Programming Library (2008)

Een, N., Sorensson, N.: Minisat 2.2. http://minisat.se (2013)

Gebser, M., Kaufmann, B., Neumann, A., Schaub, T.: clasp: A conflict-driven
answer set solver. In: Logic Programming and Nonmonotonic Reasoning 2007. pp.
260–265. Springer (2007)

Gecode Team: Gecode: Generic Constraint Development Environment (2006),
http://www.gecode.org

Hebrard, E.: Mistral, a Constraint Satisfaction Library. In: Proceedings of the
Third International CSP Solver Competition (2008)

Lecoutre, C., Tabary, S.: Abscon 112, Toward more Robustness. In: Proceedings
of the Third International CSP Solver Competition (2008)

Manthey, N.: The SAT Solver RISS3G at SC 2013. Proceedings of SAT Competition
2013 p. 72 (2013)

O'Mahony, E., Hebrard, E., Holland, A., Nugent, C., O'Sullivan, B.: Using Case-
based Reasoning in an Algorithm Portfolio for Constraint Solving. Proceeding of
the 19th Irish Conference on Artificial Intelligence and Cognitive Science
(2008)

Soos, M.: Cryptominisat 2.9.0 (2011)

Xu, L., Hutter, F., Hoos, H.H., Leyton-Brown, K.: SATzilla: Portfolio-based
Algorithm Selection for SAT. Journal of Artificial Intelligence Research
pp. 565–606 (2008)


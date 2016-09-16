source: http://www.openml.org
translator in coseal format: W. Raynaut

This data has been extracted from the OpenML database for the scenario of supervised classification. Datasets (instances), classifiers (algorithms), features and performance measurements were selected so as to minimize missing values. As a result, we obtain an "algorithm_runs" matrix featuring 11 performance measurements of 86 classifiers evaluated each on 404 datasets. This amounts to near 350k performance measurements, with less than 300 missing values. Additionally, we extract from OpenML 105 feature values on each dataset instance, covering statistical, information-theoretic and landmarking-based characterizations.

The near completion of the "algorithm_runs" matrix should help in the definition of a performance criterion for the meta-learners, as we can only compare the performance of the recomended classifiers against the performance of others on the same dataset.

The datasets and classifiers are identified by their OpenML id. To access all details available, please visit :
- http://www.openml.org/d/{instance_id here} for datasets
- http://www.openml.org/f/{algorithm here} for algorithms

Feature details can be found on 
http://www.openml.org/search?q=+type%3Aevaluation_measure&type=measure
and generation code on 
https://github.com/openml/OpenML
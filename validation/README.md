# Independent fixed-effect reference

The test suite compares the common-effect mean, its standard error, Q, I2 and
the conditional normal interval against the fixed-effect quantities returned by
`statsmodels.stats.meta_analysis.combine_effects`. The comparison uses the same
estimand and supplied variances; it does not compare against the random-effects
or HKSJ quantities that statsmodels also calculates. The nonnegative I2
convention is applied consistently.

Four synthetic inputs cover two cohorts, unequal precision, constant effects,
and heterogeneous observed effects. The relative/absolute tolerances are 1e-10.
No real cohort or biomarker data are needed. This checks computational agreement,
not validity of the common-effect assumption in a biological dataset.

To run the portable comparison:

```sh
python -m pip install '.[test]'
python validation/compare_statsmodels.py --output new_reference_result.json
```

`REFERENCE_RESULT.json` records the comparison performed for this candidate
with statsmodels 0.15.0. It includes all expected/actual quantities and their
absolute deviations. Synthetic design labels must not be interpreted as evidence
of independence in a real study; source biological units still determine that.

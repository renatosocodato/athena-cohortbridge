# athena-cohortbridge

Independent cohort evidence synthesis. Author: Renato Socodato. Version **0.1.0rc3**, prepared for review; not published.

## Install and run

```sh
python -m pip install .
athena-cohortbridge example --output example_output
athena-cohortbridge run --input examples/input.csv --output analysis_output
python -m pip install '.[test]'
python -m pytest tests -q
```

Both examples use synthetic values. Input schemas and assumptions are in
[INPUTS.md](INPUTS.md). Output directories must be new. Input validation and
serialization finish in a temporary staging directory before the requested
output directory is reserved. Existing outputs are refused; invalid inputs do
not leave an empty output directory.

The Python API is `athena_cohortbridge.core`. No network, cloud account, original grant
tree, external engine or private dataset is required. The core dependency set
is NumPy and pandas. Code and synthetic examples are under MIT; no human data
or private model is redistributed.

## Scientific scope

Fixed-effect synthesis assumes a common, commensurate effect across independent cohorts. The tool rejects mismatched tissue/endpoint/unit labels and known reused independence groups. Normal intervals condition on supplied standard errors; small-sample calibration and random effects are not implemented. See INPUTS.md before pooling.

When there are at least three independent cohorts, leave-one-cohort-out effect
extremes describe fragility. They are not confidence limits and do not validate
the model assumptions. Tests use known numerical answers, invalid inputs,
independence boundaries and synthetic CLI examples. They do not establish
clinical, biomarker or therapeutic validity.

## Independent reference check

The tests compare the fixed-effect estimate, supplied-SE normal interval, Q and
I2 with the matching fixed-effect quantities from statsmodels on four synthetic
designs. See [the reference comparison and portable command](validation/README.md).
Agreement verifies the selected calculation, not the biological independence
or commensurability of a user's cohorts.

## Relation to the original scientific workflow

This is a general implementation extracted from a scientific use case. It does
not reproduce every original study-specific estimate. No private donor aliases,
project-specific paths, exclusion decisions or source-data trees are shipped.
Future user-supplied identifiers may appear in output tables; review those
outputs before sharing them publicly.

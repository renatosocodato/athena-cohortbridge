# 0.1.0rc4

- Compute Q and influence estimates in centered coordinates to prevent rounding from fabricating heterogeneity for identical effects.

# 0.1.0rc3

- Added same-estimand fixed-effect comparisons with statsmodels on four synthetic designs, plus portable reference script and results.

# 0.1.0rc2

- Added explicit schema, nonempty identifier and design-boundary validation.
- Added leave-one-independent-unit-out effect ranges as fragility diagnostics.
- Made CLI arguments package-specific and preserved string IDs in CSV ingestion.
- Validated and serialized outputs before reserving a new output directory.
- Documented conditional interval assumptions and the limits of small independent-unit samples.
- Added regression tests for numerical/reference answers, privacy-relevant identifier preservation and invalid-input behavior.

# 0.1.0rc1

Initial review candidate with portable API, explicit input schema and synthetic example.

The rc2 estimator uses scaled inverse-variance weights to avoid numeric overflow. Optional independence_group identifiers reject known cohort overlap.

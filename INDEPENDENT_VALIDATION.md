# Independent implementation and scientific checks

Fixed/common-effect estimates, standard error, Q, I2 and normal intervals were compared with statsmodels.stats.meta_analysis.combine_effects over four independent fixtures. The maximum absolute deviation across the recorded quantities was 5.68e-14. The independent implementation comparison is included in validation/ and runs in the test suite.

Pooling still requires commensurable effects and biologically independent cohorts. Software cannot detect undisclosed participant overlap or repair an unidentified confound.

These are internal computational checks against independent implementations, public inputs and real engines. No external peer review is claimed. Full execution details are in VALIDATION.md.

## Revision after independent candidate review

Compute Q and influence estimates in centered coordinates to prevent rounding from fabricating heterogeneity for identical effects. Hosted execution records for the exact distributions are tracked separately.

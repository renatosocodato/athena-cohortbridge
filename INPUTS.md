# CohortBridge input and estimator

CSV columns: `cohort,endpoint,unit,tissue,effect,se`. Every row is one independent
cohort estimate, with a strictly positive standard error `se`. Additional input
columns are ignored except the optional `independence_group` described below.
Identifiers are read as strings so leading zeros are preserved. Whitespace is
trimmed; blank identifiers, missing columns and nonfinite values are rejected.

Effects must estimate the same contrast, on the same scale and in the same
tissue. A log odds ratio and a standardized mean difference are different
estimands even if both are written as a number. Matching labels cannot establish
that the estimands are compatible; the analyst must verify the design and
orientation before pooling. This version handles a single endpoint at a time.

Two different `cohort` labels do not establish independent donors. Shared
participants must be excluded or modeled separately before using this tool.
An optional `independence_group` column rejects duplicate values to detect known
reuse under different cohort labels. Missing or blank values in that column are
rejected. Absence of a detected duplicate is not evidence of independence.

The estimator uses relative inverse-variance weights and a fixed common-effect
model. Its normal 95% interval conditions on supplied standard errors and
approximately normal independent cohort estimates. At two cohorts, coverage and
heterogeneity cannot be calibrated from the two rows. A random-effects interval,
small-sample adjustment and equivalence/non-effect conclusion are not supplied.
`Q` and `I2` are descriptive; they never decide what may enter the result.
Three or more cohorts additionally receive leave-one-cohort-out pooled-effect
extremes to expose influence. These are fragility diagnostics, not an interval.

Very extreme numeric scales that cannot be represented as finite JSON numbers
are rejected. `interval_resolution_limited` flags a normal interval whose
endpoints round to the same floating-point value. Preserve the standard error
and use an appropriate numerical representation before interpreting its width.

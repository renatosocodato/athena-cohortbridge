"""Compare the common-effect estimand against statsmodels, not copied formulas."""
import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.meta_analysis import combine_effects

from athena_cohortbridge.core import pool_effects


@pytest.mark.parametrize('effects,standard_errors', [
    ([.2, .4, -.1, .7], [.1, .3, .2, .15]),
    ([1., 1., 1.], [.2, .5, .3]),
    ([-3., 0., 2., 5.], [.4, .2, .3, .7]),
    ([1., 3.], [1., 1.]),
])
def test_same_fixed_effect_estimand_as_statsmodels(effects, standard_errors):
    frame = pd.DataFrame({
        'cohort': [f'synthetic_{i}' for i in range(len(effects))],
        'endpoint': 'example', 'unit': 'log_ratio', 'tissue': 'synthetic',
        'effect': effects, 'se': standard_errors,
    })
    result = pool_effects(frame)
    with np.errstate(divide='ignore', invalid='ignore'):
        reference = combine_effects(np.asarray(effects), np.square(standard_errors),
                                    method_re='iterated', use_t=False)
    np.testing.assert_allclose(result['effect'], reference.mean_effect_fe,
                               atol=1e-10, rtol=1e-10)
    np.testing.assert_allclose(result['se'], reference.sd_eff_w_fe,
                               atol=1e-10, rtol=1e-10)
    np.testing.assert_allclose(result['Q'], reference.q, atol=1e-10, rtol=1e-10)
    expected_i2 = max(0., 1. - (len(effects) - 1.) / reference.q) if reference.q > 1e-10 else 0.
    np.testing.assert_allclose(result['I2'], expected_i2, atol=1e-10, rtol=1e-10)
    reference_ci = reference.conf_int(alpha=.05, use_t=False)[0]
    np.testing.assert_allclose([result['ci_low'], result['ci_high']], reference_ci,
                               atol=1e-10, rtol=1e-10)

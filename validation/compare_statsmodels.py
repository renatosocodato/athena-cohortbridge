"""Portable same-estimand reference comparison, requiring the test extra."""
import argparse
import json
from pathlib import Path
import importlib.metadata
import numpy as np
import pandas as pd
from statsmodels.stats.meta_analysis import combine_effects
from athena_cohortbridge.core import pool_effects

CASES = [
    ('unequal_precision', [.2, .4, -.1, .7], [.1, .3, .2, .15]),
    ('constant_effect', [1., 1., 1.], [.2, .5, .3]),
    ('heterogeneous_effects', [-3., 0., 2., 5.], [.4, .2, .3, .7]),
    ('two_cohorts', [1., 3.], [1., 1.]),
]


def compare():
    rows = []
    for name, effects, se in CASES:
        frame = pd.DataFrame({'cohort': [f'synthetic_{i}' for i in range(len(effects))],
                              'endpoint': 'example', 'unit': 'log_ratio',
                              'tissue': 'synthetic', 'effect': effects, 'se': se})
        actual = pool_effects(frame)
        with np.errstate(divide='ignore', invalid='ignore'):
            reference = combine_effects(np.array(effects), np.square(se),
                                        method_re='iterated', use_t=False)
            ci = reference.conf_int(alpha=.05, use_t=False)[0]
        expected = {'effect': float(reference.mean_effect_fe),
                    'se': float(reference.sd_eff_w_fe), 'Q': float(reference.q),
                    'I2': float(max(0., 1 - (len(effects)-1)/reference.q)) if reference.q > 1e-10 else 0.,
                    'ci_low': float(ci[0]), 'ci_high': float(ci[1])}
        deviation = {key: abs(actual[key]-value) for key, value in expected.items()}
        rows.append({'case': name, 'actual': {k: actual[k] for k in expected},
                     'reference': expected, 'absolute_deviation': deviation})
    return {'data_kind': 'synthetic', 'estimand': 'fixed/common effect',
            'reference': 'statsmodels.stats.meta_analysis.combine_effects fixed-effect quantities',
            'statsmodels_version': importlib.metadata.version('statsmodels'),
            'cases': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Output file must not exist')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = compare()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'cases': len(result['cases']),
                      'max_absolute_deviation': max(x for r in result['cases'] for x in r['absolute_deviation'].values())}))

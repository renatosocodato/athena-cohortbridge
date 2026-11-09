"""Synthesis of independent cohort estimates with a common estimand."""
import numpy as np
import pandas as pd


def _center_effects(effects):
    # The effect range's nearest point to zero keeps the offsets representable.
    origin = np.clip(0, effects.min(), effects.max())
    return origin, effects - origin


def pool_effects(frame):
    """Fixed-effect inverse-variance synthesis, with a conditional normal interval.

    Cohort independence must be established from study design, not labels.
    An optional independence_group column rejects known reused biological units.
    Q/I2 are descriptive and do not decide whether heterogeneous effects may pool.
    """
    columns = ['cohort', 'endpoint', 'unit', 'tissue', 'effect', 'se']
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError('Missing required columns: ' + ', '.join(missing))
    if len(frame) < 2 or frame[columns].isna().any().any():
        raise ValueError('At least two complete independent cohorts required')
    data = frame.copy()
    for column in ['cohort', 'endpoint', 'unit', 'tissue']:
        data[column] = data[column].astype(str).str.strip()
        if data[column].eq('').any():
            raise ValueError('Blank cohort, endpoint, unit or tissue label')
    if data.cohort.duplicated().any():
        raise ValueError('Repeated cohort: independence not established')
    if 'independence_group' in data:
        groups = data.independence_group.astype('string').str.strip()
        if groups.isna().any() or groups.eq('').any() or groups.duplicated().any():
            raise ValueError('Distinct, nonempty independence_group identifiers required')
    if any(data[c].nunique() != 1 for c in ['endpoint', 'unit', 'tissue']):
        raise ValueError('Endpoint, unit and tissue must match')
    try:
        y = data.effect.to_numpy(dtype=np.longdouble)
        se = data.se.to_numpy(dtype=np.longdouble)
    except (TypeError, ValueError) as exc:
        raise ValueError('Effects and standard errors must be numeric') from exc
    if not np.isfinite(y).all() or not np.isfinite(se).all() or (se <= 0).any():
        raise ValueError('Finite effects and positive standard errors required')
    # Relative weights avoid overflow of 1/se**2 for very precise measurements.
    scale = se.min()
    weights = (scale / se) ** 2
    weight_total = weights.sum()
    origin, offsets = _center_effects(y)
    mean_offset = np.sum((weights / weight_total) * offsets)
    sigma = scale / np.sqrt(weight_total)
    # Form residuals before adding back the common level of the effects.
    q = np.sum(((offsets - mean_offset) / se) ** 2)
    half_width = 1.95996398454 * sigma
    values = np.array([origin + mean_offset, sigma, origin + (mean_offset - half_width),
                       origin + (mean_offset + half_width), q], dtype=np.longdouble)
    if not np.isfinite(values).all() or (abs(values) > np.finfo(float).max).any():
        raise ValueError('Effect/uncertainty scale exceeds supported numeric range')
    result = dict(zip(['effect', 'se', 'ci_low', 'ci_high', 'Q'], map(float, values)))
    if result['se'] <= 0:
        raise ValueError('Standard error underflows the supported numeric range')
    result['interval_resolution_limited'] = result['ci_low'] == result['ci_high']
    result.update({
        'cohorts': len(y), 'I2': float(max(0., (q - len(y) + 1) / q)) if q else 0.,
        'model': 'fixed_effect', 'interval': 'conditional_normal_95_percent',
        'endpoint': str(data.endpoint.iloc[0]), 'unit': str(data.unit.iloc[0]),
        'tissue': str(data.tissue.iloc[0]),
        'interpretation': 'Common-effect estimate; interval assumes independent approximately normal cohort estimates and supplied standard errors',
    })
    if len(y) >= 3:
        loo = []
        for i in range(len(y)):
            keep = np.arange(len(y)) != i
            relative = (se[keep].min() / se[keep]) ** 2
            loo_origin, loo_offsets = _center_effects(y[keep])
            loo.append(loo_origin + np.sum((relative / relative.sum()) * loo_offsets))
        result['leave_one_cohort_out_min'] = float(min(loo))
        result['leave_one_cohort_out_max'] = float(max(loo))
    return result

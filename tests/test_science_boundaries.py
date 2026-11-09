import pandas as pd
import pytest
from athena_cohortbridge.core import pool_effects

def fixture():
    return pd.DataFrame({'cohort':['a','b'],'endpoint':['x']*2,'unit':['log_ratio']*2,'tissue':['csf']*2,'effect':[1.,3.],'se':[1.,1.]})

def test_known_fixed_effect_answer():
    r=pool_effects(fixture());assert r['effect']==2
    assert abs(r['se']-2**-.5)<1e-12
    assert r['cohorts']==2 and r['Q']==2

@pytest.mark.parametrize('column,value',[('tissue','plasma'),('unit','percent'),('endpoint','other'),('cohort','a'),('se',0)])
def test_incompatible_or_nonindependent_evidence_rejected(column,value):
    x=fixture();x.loc[1,column]=value
    with pytest.raises(ValueError):pool_effects(x)


def test_very_small_standard_errors_do_not_overflow_inverse_variance():
    x=fixture();x['effect']=2.;x['se']=1e-200
    result=pool_effects(x)
    assert result['effect']==2.
    assert result['se']>0
    assert result['Q']==0


def test_unknown_schema_and_blank_identifiers_have_clear_errors():
    with pytest.raises(ValueError,match='Missing required columns'):
        pool_effects(fixture().drop(columns='se'))
    x=fixture();x.loc[1,'cohort']=' '
    with pytest.raises(ValueError,match='Blank'):
        pool_effects(x)


def test_known_shared_independence_group_cannot_be_relabelled_as_replication():
    x=fixture();x['independence_group']=['shared','shared']
    with pytest.raises(ValueError,match='independence_group'):
        pool_effects(x)


def test_leave_one_cohort_out_exposes_influential_cohort():
    x=fixture();x=pd.concat([x,x.iloc[[1]].assign(cohort='c',effect=9.)],ignore_index=True)
    result=pool_effects(x)
    assert result['leave_one_cohort_out_min']==2.
    assert result['leave_one_cohort_out_max']==6.
    assert result['interval']=='conditional_normal_95_percent'


def test_identical_effects_have_no_heterogeneity_at_large_common_offset():
    frame = pd.concat([fixture(), fixture().iloc[[1]].assign(cohort='c')], ignore_index=True)
    frame = frame.assign(effect=1e16, se=[1., 3., 4.])
    result = pool_effects(frame)
    assert result['effect'] == 1e16
    assert result['Q'] == result['I2'] == 0
    assert result['leave_one_cohort_out_min'] == result['leave_one_cohort_out_max'] == 1e16


def test_heterogeneity_is_invariant_to_a_representable_common_offset():
    frame = pd.concat([fixture(), fixture().iloc[[1]].assign(cohort='c')], ignore_index=True)
    frame = frame.assign(effect=[0., 2., 8.], se=[1., 3., 4.])
    baseline = pool_effects(frame)
    shifted = pool_effects(frame.assign(effect=frame.effect + 1e16))
    assert shifted['Q'] == pytest.approx(baseline['Q'])
    assert shifted['I2'] == pytest.approx(baseline['I2'])

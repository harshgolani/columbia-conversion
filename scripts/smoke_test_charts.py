"""Smoke-tests every chart function with representative mock data."""
import sys, traceback
sys.path.insert(0, '.')

import pandas as pd
import plotly.graph_objects as go
from src.charts import (
    chart_conversion_donut,
    chart_model_comparison,
    chart_pagevalues_effect,
    chart_monthly_conversion,
    chart_exit_rate,
    chart_browsing_depth,
)

PASS = '\033[92m PASS\033[0m'
FAIL = '\033[91m FAIL\033[0m'

def check(name, fn):
    try:
        fig = fn()
        assert isinstance(fig, go.Figure), f'returned {type(fig)}, expected go.Figure'
        print(f'{PASS}  {name}')
    except Exception:
        print(f'{FAIL}  {name}')
        traceback.print_exc()

# ── mock data ─────────────────────────────────────────────────────────────────

overview_mock = {'conversion_rate': 15.5, 'non_conversion_rate': 84.5,
                 'total_sessions': 12330, 'purchasers': 1908,
                 'non_purchasers': 10422, 'additional_purchases': 123,
                 'pct_revenue_increase': 6.4}

model_mock = pd.DataFrame([
    {'model': 'Keras Neural Network (100%)', 'tpr': 0.7876, 'ppv': 0.6055, 'f1': 0.6847, 'auc': 0.9306, 'champion': True},
    {'model': 'Keras Neural Network (64%)',  'tpr': 0.7941, 'ppv': 0.5898, 'f1': 0.6769, 'auc': 0.9302, 'champion': False},
    {'model': 'XGBoost',                     'tpr': 0.7516, 'ppv': 0.6101, 'f1': 0.6735, 'auc': 0.9294, 'champion': False},
    {'model': 'LightGBM',                    'tpr': 0.7549, 'ppv': 0.6144, 'f1': 0.6774, 'auc': 0.9284, 'champion': False},
])

pv_mock = pd.DataFrame([
    {'pagevalue': 0,  'conversion_prob': 0.08},
    {'pagevalue': 1,  'conversion_prob': 0.55},
    {'pagevalue': 10, 'conversion_prob': 0.60},
    {'pagevalue': 25, 'conversion_prob': 0.64},
    {'pagevalue': 50, 'conversion_prob': 0.70},
])

month_order = ['Feb','Mar','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthly_mock = pd.DataFrame({
    'month': pd.Categorical(['Mar','May','Aug','Nov','Dec'],
                            categories=month_order, ordered=True),
    'purchases':        [55,  65,  90, 760,  80],
    'sessions':         [520, 580, 650, 2998, 540],
    'conversion_rate':  [10.6, 11.2, 13.8, 25.4, 14.8],
})

exit_mock = pd.DataFrame([
    {'exit_rate': 0.00, 'conversion_prob': 0.19},
    {'exit_rate': 0.05, 'conversion_prob': 0.15},
    {'exit_rate': 0.10, 'conversion_prob': 0.14},
    {'exit_rate': 0.20, 'conversion_prob': 0.132},
])

browsing_mock = pd.DataFrame([
    {'product_pages': 0,   'conversion_prob': 0.215},
    {'product_pages': 5,   'conversion_prob': 0.200},
    {'product_pages': 40,  'conversion_prob': 0.165},
    {'product_pages': 140, 'conversion_prob': 0.155},
])

# ── run checks ────────────────────────────────────────────────────────────────

check('chart_conversion_donut',  lambda: chart_conversion_donut(overview_mock))
check('chart_model_comparison',  lambda: chart_model_comparison(model_mock))
check('chart_pagevalues_effect', lambda: chart_pagevalues_effect(pv_mock))
check('chart_monthly_conversion',lambda: chart_monthly_conversion(monthly_mock))
check('chart_exit_rate',         lambda: chart_exit_rate(exit_mock))
check('chart_browsing_depth',    lambda: chart_browsing_depth(browsing_mock))

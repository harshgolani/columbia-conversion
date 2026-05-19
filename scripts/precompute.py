"""
Run locally to regenerate precomputed analysis results.
Requires the full dataset in data/raw/.

Usage: python3 scripts/precompute.py
Output: assets/precomputed.json
"""
import sys, json, os
sys.path.append('.')
from src.analysis import (
    load_data, business_overview, model_comparison,
    pagevalues_effect, pagevalues_distribution,
    monthly_conversion, exit_rate_effect, browsing_depth_effect,
    recommendations
)

df = load_data()
os.makedirs('assets', exist_ok=True)

data = {
    'overview': business_overview(df),
    'models': model_comparison().to_dict(orient='records'),
    'pv_effect': pagevalues_effect().to_dict(orient='records'),
    'pv_dist': pagevalues_distribution(df),
    'monthly': monthly_conversion(df).to_dict(orient='records'),
    'exit_rate': exit_rate_effect().to_dict(orient='records'),
    'browsing': browsing_depth_effect().to_dict(orient='records'),
    'recommendations': recommendations().to_dict(orient='records'),
}

with open('assets/precomputed.json', 'w') as f:
    json.dump(data, f)

print('Saved to assets/precomputed.json')

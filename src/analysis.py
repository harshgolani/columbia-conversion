import pandas as pd # type: ignore

def load_data():
    return pd.read_csv('data/raw/online_shoppers_intention.csv')

def business_overview(df):
    total = len(df)
    purchasers = int(df['Revenue'].sum())
    non_purchasers = total - purchasers
    conversion_rate = round(purchasers / total * 100, 1)
    non_conversion_rate = round(non_purchasers / total * 100, 1)

    additional_purchases = round((0.165 - 0.155) * total)
    pct_revenue_increase = round(additional_purchases / purchasers * 100, 1)

    return {
        'total_sessions': total,
        'purchasers': purchasers,
        'non_purchasers': non_purchasers,
        'conversion_rate': float(conversion_rate),
        'non_conversion_rate': float(non_conversion_rate),
        'additional_purchases': int(additional_purchases),
        'pct_revenue_increase': float(pct_revenue_increase)
    }

def model_comparison():
    """
    Hardcoded from DataRobot results - Keras Neural Network champion model.
    CV AUC 0.9306, Holdout AUC 0.9377.
    """
    models = [
        {'model': 'Keras Neural Network (100%)', 'tpr': 0.7876, 'ppv': 0.6055, 'f1': 0.6847, 'auc': 0.9306, 'champion': True},
        {'model': 'Keras Neural Network (64%)', 'tpr': 0.7941, 'ppv': 0.5898, 'f1': 0.6769, 'auc': 0.9302, 'champion': False},
        {'model': 'XGBoost', 'tpr': 0.7516, 'ppv': 0.6101, 'f1': 0.6735, 'auc': 0.9294, 'champion': False},
        {'model': 'LightGBM', 'tpr': 0.7549, 'ppv': 0.6144, 'f1': 0.6774, 'auc': 0.9284, 'champion': False},
    ]
    return pd.DataFrame(models)

def pagevalues_effect():
    """
    Partial dependence data from DataRobot SHAP analysis.
    Hardcoded from slide findings - Keras Neural Network champion model.
    Key finding: conversion spikes from ~8% to 55%+ as PageValues rises above zero.
    """
    data = [
        {'pagevalue': 0, 'conversion_prob': 0.08},
        {'pagevalue': 1, 'conversion_prob': 0.55},
        {'pagevalue': 5, 'conversion_prob': 0.58},
        {'pagevalue': 10, 'conversion_prob': 0.60},
        {'pagevalue': 15, 'conversion_prob': 0.61},
        {'pagevalue': 20, 'conversion_prob': 0.63},
        {'pagevalue': 25, 'conversion_prob': 0.64},
        {'pagevalue': 30, 'conversion_prob': 0.65},
        {'pagevalue': 35, 'conversion_prob': 0.66},
        {'pagevalue': 40, 'conversion_prob': 0.67},
        {'pagevalue': 45, 'conversion_prob': 0.68},
        {'pagevalue': 50, 'conversion_prob': 0.70},
    ]

    # Also compute actual PageValues distribution from real data
    return pd.DataFrame(data)

def pagevalues_distribution(df):
    zero_pv = round(float((df['PageValues'] == 0).sum() / len(df) * 100), 1)
    nonzero_pv = round(100 - zero_pv, 1)
    median_pv = round(float(df[df['PageValues'] > 0]['PageValues'].median()), 1)

    return {
        'zero_pagevalues_pct': zero_pv,
        'nonzero_pagevalues_pct': nonzero_pv,
        'median_nonzero_pagevalues': median_pv
    }

def monthly_conversion(df):
    monthly = df.groupby('Month')['Revenue'].agg(['sum', 'count']).reset_index()
    monthly.columns = ['month', 'purchases', 'sessions']
    monthly['conversion_rate'] = round(monthly['purchases'] / monthly['sessions'] * 100, 1)

    month_order = ['Feb', 'Mar', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly = monthly[monthly['month'].isin(month_order)]
    monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
    monthly = monthly.sort_values('month').reset_index(drop=True)

    return monthly

def exit_rate_effect():
    """
    Hardcoded from DataRobot partial dependence plot.
    Key finding: conversion drops 30% as exit rate increases from 0 to 0.2.
    """
    data = [
        {'exit_rate': 0.00, 'conversion_prob': 0.19},
        {'exit_rate': 0.01, 'conversion_prob': 0.18},
        {'exit_rate': 0.02, 'conversion_prob': 0.17},
        {'exit_rate': 0.03, 'conversion_prob': 0.16},
        {'exit_rate': 0.04, 'conversion_prob': 0.155},
        {'exit_rate': 0.05, 'conversion_prob': 0.150},
        {'exit_rate': 0.06, 'conversion_prob': 0.148},
        {'exit_rate': 0.08, 'conversion_prob': 0.145},
        {'exit_rate': 0.10, 'conversion_prob': 0.140},
        {'exit_rate': 0.14, 'conversion_prob': 0.137},
        {'exit_rate': 0.18, 'conversion_prob': 0.135},
        {'exit_rate': 0.20, 'conversion_prob': 0.132},
    ]
    return pd.DataFrame(data)

def browsing_depth_effect():
    """
    Hardcoded from DataRobot partial dependence plot.
    Key finding: conversion drops 25% as product pages viewed increases from 0 to 80+.
    Window shoppers browse more but buy less.
    """
    data = [
        {'product_pages': 0, 'conversion_prob': 0.215},
        {'product_pages': 5, 'conversion_prob': 0.200},
        {'product_pages': 10, 'conversion_prob': 0.190},
        {'product_pages': 20, 'conversion_prob': 0.178},
        {'product_pages': 30, 'conversion_prob': 0.170},
        {'product_pages': 40, 'conversion_prob': 0.165},
        {'product_pages': 50, 'conversion_prob': 0.161},
        {'product_pages': 60, 'conversion_prob': 0.158},
        {'product_pages': 80, 'conversion_prob': 0.156},
        {'product_pages': 100, 'conversion_prob': 0.155},
        {'product_pages': 120, 'conversion_prob': 0.155},
        {'product_pages': 140, 'conversion_prob': 0.155},
    ]
    return pd.DataFrame(data)

def recommendations():
    """
    Business recommendations derived from model findings.
    Hardcoded — translates SHAP findings into actionable business interventions.
    """
    data = [
        {
            'feature': 'PageValues',
            'finding': 'Conversion spikes from 8% to 55%+ as soon as PageValues > 0. 77.9% of sessions never reach high-value pages.',
            'action': 'Surface high-value pages earlier via personalized recommendations, "Best Sellers" modules, and smarter search ranking.',
            'tradeoff': 'Requires strong product data infrastructure and A/B testing to avoid over-promoting low-margin items.'
        },
        {
            'feature': 'Exit Rate',
            'finding': 'Conversion drops 30% as exit rate increases from 0 to 0.2. High exit = disengagement, not comparison.',
            'action': 'Deploy exit-intent popups with targeted discounts or "Notify me when on sale" to capture email without margin loss.',
            'tradeoff': 'Overuse of discounts trains customers to wait for deals and erodes long-term brand value.'
        },
        {
            'feature': 'Browsing Depth',
            'finding': 'Users viewing 0-5 pages convert at 21.5%. Users viewing 80+ pages convert at 15.5% — a 25% decline.',
            'action': 'Reduce decision friction. Highlight recommended choice, simplify comparisons, add internal comparison tools to keep users on site.',
            'tradeoff': 'Excessive curation limits product discovery and may reduce basket size for users who would have bought more.'
        },
        {
            'feature': 'Month (Seasonality)',
            'finding': 'November converts at 25.4% — 2.3x the baseline of ~11%. Driven by winter onset in Turkey, not Black Friday.',
            'action': 'Invest in lower-intent months (Mar, May) with loyalty programs and retention campaigns rather than over-investing in already-high November.',
            'tradeoff': 'Shifting spend away from November risks leaving high-intent demand uncaptured during peak window.'
        },
    ]
    return pd.DataFrame(data)

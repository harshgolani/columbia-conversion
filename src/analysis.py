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

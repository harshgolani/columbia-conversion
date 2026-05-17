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

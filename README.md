# Columbia Conversion Dashboard

Conversion analytics dashboard for Columbia Sportswear Turkey, built on the UCI Online Shoppers Purchasing Intention Dataset (Sakar et al. 2019).

**Live Demo:** https://columbia-conversion.streamlit.app

---

## What it shows

Five tabs, each with a structured Finding / Why It Matters / Recommendation:

- **The Problem** — 84.5% non-conversion rate, class imbalance, revenue opportunity from 1% lift
- **Model Results** — 4 models compared by AUC, Keras Neural Network champion (AUC 0.9306)
- **PageValues Effect** — SHAP feature importance, partial dependence curve showing conversion spike
- **Behavioral Patterns** — November seasonality, exit rate effect, browsing depth vs conversion
- **Recommendations** — Feature → finding → action → tradeoff table

## Key Findings

- Columbia Turkey converts at 15.5% vs 5–6% industry average — brand-driven traffic, not a traffic problem
- PageValues dominates at 100% relative importance — 77.9% of sessions never reach a high-value page
- November spike driven by winter onset in Turkey, not Black Friday — a durable seasonal signal
- Users browsing 80+ product pages convert 25% less — high browsing = comparison shopping, not engagement
- 1% conversion improvement = 123 additional purchases = 6.4% revenue increase

## Stack

Python · Pandas · Plotly · Streamlit · DataRobot (model training)

## Architecture

Analysis is pre-computed from the full dataset and served as static JSON for fast load times on Streamlit Cloud. To regenerate:

```bash
pip install -r requirements.txt
python3 scripts/precompute.py
```

Raw dataset: UCI Online Shoppers Purchasing Intention (Sakar et al. 2019) — place in `data/raw/online_shoppers_intention.csv`

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Streamlit dashboard analyzing Columbia Sportswear Turkey's e-commerce conversion data. Based on the UCI Online Shoppers Purchasing Intention Dataset (Sakar et al. 2019), cross-referenced with DataRobot model outputs from a Columbia business case (Spring 2026).

## Commands

```bash
# Run the Streamlit app
streamlit run app.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

The app is structured in three layers:

- **`app.py`** — Streamlit entry point. Renders 5 tabs: Business Overview, Model Comparison, PageValues Effect, Behavioral Patterns, Recommendations.
- **`src/analysis.py`** — All data logic. Functions return DataFrames or dicts consumed by `app.py`. No Streamlit imports here.
- **`src/charts.py`** — Chart/visualization functions. Takes DataFrames from `analysis.py`, returns Plotly (or similar) figures.
- **`data/raw/online_shoppers_intention.csv`** — Source dataset. Gitignored by the `data/` rule but manually committed (the gitignore has `data/` but the file is tracked).

## Data Sourcing — Critical Distinction

Many values in `analysis.py` are **hardcoded from DataRobot slides**, not computed from the CSV. The model files do not exist in this repo. Before adding or modifying any number, check `DECISIONS.md` to determine whether it comes from:

1. **Live CSV computation** — `load_data()` + analysis functions (e.g., `monthly_conversion`, `pagevalues_distribution`)
2. **Hardcoded DataRobot output** — partial dependence curves, model metrics, SHAP rankings (e.g., `pagevalues_effect`, `exit_rate_effect`, `browsing_depth_effect`, `model_comparison`)

Never replace hardcoded DataRobot values with CSV-derived approximations — they represent model outputs that can't be recomputed here.

## Key Analytical Findings (from DECISIONS.md)

- Conversion rate: 15.5% (3x e-commerce industry average) — brand-driven traffic, not a traffic problem
- Champion model: Keras Neural Network (100% data), CV AUC 0.9306, Holdout AUC 0.9377
- PageValues is the #1 SHAP feature — 77.9% of sessions have zero PageValues (never reach high-value pages)
- November converts at 25.4% (2.3x baseline) — attributed to Turkish winter onset, not Black Friday
- High browsing depth (80+ pages) correlates with *lower* conversion — window shoppers, not engaged buyers

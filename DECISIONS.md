# Analysis Decisions & Findings

## Dataset
- Source: UCI Online Shoppers Purchasing Intention Dataset (Sakar et al. 2019)
- 12,330 sessions, 17 features, 1 binary target (Revenue)
- Same dataset used in Columbia Sportswear Turkey business case (Spring 2026)

## Business Overview (Tab 1)

### Conversion Rate
- 15.5% conversion rate confirmed from data (1,908 / 12,330)
- Industry average e-commerce conversion is 2-4% globally, 5-6% for strong brands
- Columbia Turkey at 15.5% = 3x industry average — signals brand-driven traffic not a traffic problem
- Hardcoded industry benchmark (not from dataset) — sourced from Sakar et al. context

### Revenue Opportunity
- Skipped dollar amount — AOV ($120 current) is from Columbia business case, not this dataset. Including it would be fabricated.
- Instead show: 1% conversion improvement = 123 additional purchases = 6.4% revenue increase
- This is honest and still compelling

### November Spike
- Dataset shows November as peak conversion month (~22-23% vs 14-16% baseline)
- Turkey is majority Muslim — Black Friday not culturally anchored
- November marks winter onset in Istanbul (10-17°C average)
- Columbia's winter collection aligns with seasonal demand
- Insight: November spike is weather-driven, not promotional — more durable and predictable signal

### Window Shopper Finding
- Users browsing 0-5 product pages convert at ~20%
- Users browsing 80+ product pages convert at ~15% (25% decline)
- Interpretation: high browsing = comparison shopping across sites, not high engagement
- These users likely have multiple tabs open comparing Columbia vs competitors

## Model Comparison (Tab 2)

- All model results hardcoded from DataRobot output — we don't have model files, only the findings
- Champion: Keras Neural Network (100% data) — CV AUC 0.9306, Holdout AUC 0.9377
- Narrow CV to Holdout gap (0.9306 → 0.9377) confirms no overfitting — model generalizes well
- PPV of 0.61 means 39% of predicted converters won't actually buy — precision limitation noted
- 4 models compared: Keras (x2), XGBoost, LightGBM — all competitive, Keras wins on AUC

## PageValues Effect (Tab 3)

- Partial dependence curve hardcoded from DataRobot slide output
- Key finding: conversion spikes from 8% to 55%+ the moment PageValues > 0
- After that spike, conversion grows gradually to ~70% at PageValues = 50
- 77.9% of sessions have zero PageValues (not 84.5% — that's the non-conversion rate, different metric)
- 84.5% non-conversion ≠ 77.9% zero PageValues — these are related but distinct
- Median PageValues for sessions that DO have it: 16.7
- Insight: funnel is broken before checkout — most users never reach pages that drive conversion

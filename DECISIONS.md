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

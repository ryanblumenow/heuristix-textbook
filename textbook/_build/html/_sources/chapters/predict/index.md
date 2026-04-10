# Part IV · Predict

**Machine learning, statistical modelling, forecasting, and scoring.**

The Predict stage is the heart of data science. It is where we build models that generalise from historical data to make predictions about the future, score new records, forecast time series, recommend items, and quantify uncertainty.

Heuristix provides 42 Predict nodes spanning the full landscape of supervised learning, time series forecasting, probabilistic modelling, recommendation systems, and model development tooling.

## A Map of Prediction Problems

Not all prediction problems are the same. Understanding which type of problem you have is the first step to choosing the right node:

| Problem Type | Output | Example Nodes |
|---|---|---|
| **Binary classification** | Probability 0–1 | Predict, Estimate Propensity, Score Anomalies |
| **Regression** | Continuous number | Model a Value, Linear Regression, Gaussian Process |
| **Time series forecast** | Future values | Forecast, Smart Forecast, LSTM, Nowcast |
| **Survival / time-to-event** | Duration + hazard | Time to Event |
| **Ranking / recommendation** | Ordered list | Recommend, Rank Items, Find Similar |
| **Causal uplift** | Treatment effect | Uplift Model |
| **Count data** | Non-negative integers | Model Event Counts, Zero-Inflated Model |
| **Volatility** | Variance over time | Model Volatility |

## Chapters in This Part

**Core ML** — Predict, Score, Classify Records, Deep Learning, Find Best Model, Tune Model, Validate Reliability, Balance Classes, Calibrate Predictions, Combine Predictors, Estimate Uncertainty, Conformal Predict, Explain Predictions

**Regression** — Model a Value, Linear Regression, Polynomial Regression, Model Response Curve, Generalised Estimation, Gaussian Process, Ordinal Outcome

**Forecasting** — Forecast, Smart Forecast, Forecast with Drivers, Hierarchical Forecasting, Nowcast, Detect Time Anomaly, Structural Break, State Space, Detect Regimes, Model Volatility, LSTM

**Specialised** — Estimate Propensity, Time to Event, Uplift Model, Track Groups, Find Similar, Recommend, Rank Items, Estimate Lifetime Value, Model Event Counts, Zero-Inflated Model, Score Anomalies

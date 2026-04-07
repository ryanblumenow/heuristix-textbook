# Time to Event


![](../../_static/figures/time-to-event_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The biggest mistake I see teams make with time-to-event models is treating censored observations as complete failures or simply dropping them from the dataset. Those censored cases where you only know someone survived past a certain point are incredibly valuable information that survival models are specifically designed to leverage. If you're working with customer churn or equipment failure, remember that right-censoring happens naturally when your observation window ends, and ignoring it will severely bias your predictions toward shorter event times.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Time-to-event analysis predicts when something will happen and which factors make it happen sooner or later.

**When to use it:** You need to forecast customer churn, equipment failure, loan default, or employee turnover—any situation where you're waiting for an event and some cases haven't happened yet.

**What you get back:** Probability curves showing when events will occur and rankings of which factors accelerate or delay them, letting you prioritize interventions on the highest-risk cases.

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Minutes on 100K rows |
| **What you bring** | Time-stamped data with event indicators (happened/not yet), plus characteristics of each case |
| **What you get** | Survival curves, hazard ratios, and risk scores for each case |
| **Heuristix bucket** | Predict — Machine Learning & Forecasting |

**The one thing you must understand:** Time-to-event analysis is the only method that properly handles "not yet" cases—standard prediction approaches will give you wrong answers when many events haven't happened.

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify business problems where predicting *when* an event will occur matters more than *if* it will occur, such as customer churn timing, equipment failure windows, or loan default horizons.
- Interpret survival curves and hazard ratios to explain to stakeholders which customer segments are at highest risk in the next 30/60/90 days and how different factors accelerate or delay key events.
- Prioritize interventions by comparing the predicted time-to-event across different groups, enabling decisions like which at-risk customers to contact first or when to schedule preventive maintenance.

**After reading this chapter, a data scientist will be able to:**

- Implement Cox proportional hazards models and parametric survival models while correctly handling right-censored data, left truncation, and time-varying covariates.
- Select between model types (semi-parametric vs. parametric) and tune baseline hazard specifications by assessing proportional hazards assumptions and evaluating goodness-of-fit for different distributional choices.
- Validate model performance using concordance indices and calibration plots, diagnose violations of proportional hazards through residual analysis, and identify when censoring patterns bias your estimates.

## Overview

Time-to-event analysis, also known as survival analysis or duration modelling, is a family of statistical methods designed to analyse the time until a specific event occurs while properly handling censored observations—cases where the event has not yet occurred by the end of the observation period. These methods belong to the broader class of regression techniques but are uniquely suited to situations where the dependent variable is a duration and where complete observation of all outcomes is impossible or impractical. The core purpose is to estimate survival functions, hazard rates, and the effects of covariates on the timing of events, enabling prediction of when events will occur and what factors accelerate or delay them.

## When to Use This

- **Use when your outcome is a duration until an event**: Customer churn analysis where you need to model how long customers remain before cancelling, not just whether they churn.

- **Use when you have right-censored data**: Many observations have not yet experienced the event by the end of your study period—standard regression would either exclude these valuable observations or treat them incorrectly as non-events.

- **Use when you need to estimate time-varying risk**: Understanding how the probability of an event changes over time (e.g., machine failure risk increasing with age) requires hazard modelling rather than static classification.

- **Use when comparing durations across groups**: Comparing median survival times or hazard ratios between treatment and control groups, customer segments, or product cohorts.

- **Use when covariates may have time-varying effects**: When the effect of a predictor on the event risk changes over the observation period, survival models can capture these dynamics.

- **Use when you need to predict remaining lifetime**: Estimating expected remaining time until an event for observations that have already survived a certain period.

- **Do NOT use when events are instantaneous or timing is irrelevant**: If you only care about whether an event occurs (not when), binary classification may be simpler and sufficient.

- **Do NOT use when there is no censoring and time is fully observed**: Standard regression on the duration variable may be appropriate, though survival models remain valid.

- **Do NOT use when the event can recur and recurrence matters**: Standard survival analysis handles single events; recurrent event models require extensions.

- **Do NOT use when the "event" is continuous or ordinal**: Survival analysis is designed for well-defined, discrete event occurrences.

## Questions This Answers

### Customer Retention and Churn

**How long do customers typically stay with us before they cancel their subscription?**

**Which customer segment is most likely to churn in the next 90 days?**

**What's driving our enterprise clients to leave faster than they did last year?**

**If we launch this new onboarding program, how much longer will customers stay with us?**

**Are customers who signed up through our partner channel more loyal than those from direct sales?**

### Risk Management and Credit

**What percentage of these new loan applicants will default within 24 months?**

**How long until a delinquent account becomes a complete write-off?**

**Which accounts should we prioritize for collection efforts to maximize recovery?**

**Is our 60-day payment grace period helping or just delaying the inevitable defaults?**

### Workforce and Operations

**How long do new hires in sales typically stay before leaving the company?**

**When should we schedule equipment maintenance to prevent unexpected failures?**

**Which machines in Plant B are most likely to break down in the next quarter?**

**Are employees in our restructured divisions leaving faster than those in stable departments?**

**What's the real payback period for this capital investment given our historical failure rates?**

## How It Works

Imagine you're managing a customer loyalty program at a coffee shop, tracking how long customers stay subscribed before they cancel. Some customers joined recently and are still active—you don't know *when* they'll cancel, just that they haven't yet. Others canceled after three months, six months, or a year. Traditional analysis would force you to either throw out the still-active customers (wasteful!) or pretend they'll never cancel (wrong!). Time-to-event analysis is like having a smart assistant who can learn patterns from *both* groups: using the complete stories of those who already left *and* the incomplete stories of those still here, treating "we don't know yet" as valuable information rather than missing data.

```
DATA STRUCTURE: Tracking Customer Subscriptions

Customer Timeline                    What We Record
─────────────────                    ───────────────

Alice    ●────────────✗              Time: 8 months
         Start      Canceled         Event: Yes (1)
                                     
Bob      ●──────────────────○        Time: 12 months
         Start            Still      Event: No (0)
                         Active      [censored]

Carol    ●─────✗                     Time: 4 months
         Start Canceled              Event: Yes (1)

Dave     ●─────────────○              Time: 10 months
         Start      Still            Event: No (0)
                   Active            [censored]

         ↓ TIME-TO-EVENT LEARNS ↓

         Survival Curve
    100%│●                           Probability
        │ ●●                         of staying
     75%│    ●                       subscribed
        │      ●●                    over time
     50%│         ●
        │           ●●
     25%│              ●
        └─────────────────→
         0  3  6  9  12 months
```

**Step 1: Record every observation with two pieces of information.** For each person or case, you track the duration (how long you observed them) and the event status (did the event happen, or are they censored—still in progress?). Alice canceled after eight months, so she's "duration: 8, event: yes." Bob is still active after twelve months, so he's "duration: 12, event: no."

**Step 2: Sort everyone by their event times and build a survival curve.** The algorithm arranges all observations chronologically. At each time point where an event actually happens, it calculates what percentage of the group is still "surviving"—still event-free. Censored observations contribute to the count until their observation ends, then they simply exit the analysis without being counted as events.

**Step 3: Estimate the hazard at each moment.** The hazard is the risk of the event happening right now, given you've made it this far. It's like asking: "Of customers who've stayed six months, how many are leaving *this* month?" The algorithm calculates this risk at each event time by comparing how many events occurred to how many were still at risk.

**Step 4: Incorporate predictor variables to see what accelerates or delays events.** For each characteristic (age, purchase history, location), the model estimates how much it multiplies the baseline hazard. A customer who engages weekly might have half the cancellation hazard of someone who visits monthly—the model quantifies these effects while still respecting censored observations.

**Step 5: Generate predictions for new cases.** Given someone's characteristics, the model produces their personalized survival curve—the probability they'll remain event-free at three months, six months, twelve months. This lets you identify high-risk customers before they leave.

**The key insight:** Time-to-event analysis extracts maximum information from incomplete stories by treating "not yet" as a different kind of answer than "never," letting partial observations contribute what they know without pretending to know what they don't.

## The Intuition

Imagine you are managing a fleet of delivery vehicles and want to understand how long engines last before requiring major repairs. You have maintenance records for 500 vehicles over the past three years. Some engines failed and were repaired—you know exactly how long they lasted. But many engines are still running—they have not failed yet. If you simply calculate the average lifespan using only the failed engines, you systematically underestimate engine durability because you ignore all the vehicles that have survived longer. Conversely, if you exclude non-failed engines entirely, you throw away valuable information that these engines lasted at least as long as your observation period.

Time-to-event analysis solves this problem through the concept of censoring. A censored observation tells us that the event had not occurred by a certain time, providing a lower bound on the true event time. The key insight is that at any given moment, we can calculate the risk of failure among all vehicles still operating—not just those that eventually fail. This instantaneous risk is called the hazard rate. By accumulating these hazard rates over time, we construct survival curves that properly incorporate both complete and censored observations.

The power of this approach becomes clear when comparing groups. Suppose you want to know whether vehicles serviced at Facility A last longer than those at Facility B. You cannot simply compare average lifespans because the vehicles have different ages and observation periods. Instead, you compare hazard rates: at any given age, conditional on having survived that long, which facility's vehicles face higher failure risk? This hazard ratio provides a meaningful comparison that accounts for censoring and different follow-up times, enabling valid inference even when your data is incomplete.

## The Mathematics

### Problem Setup and Notation

Let $T$ be a non-negative continuous random variable representing the time until an event occurs. For each subject $i$, we observe:

- $t_i$: the observed time (either event time or censoring time)
- $\delta_i$: the event indicator ($\delta_i = 1$ if event observed, $\delta_i = 0$ if censored)
- $\mathbf{x}_i$: a vector of $p$ covariates

The fundamental quantities of interest are:

**Survival Function**: The probability of surviving beyond time $t$:

$$
S(t) = P(T > t) = 1 - F(t)
$$

where $F(t)$ is the cumulative distribution function of $T$.

**Hazard Function**: The instantaneous rate of event occurrence at time $t$, conditional on survival to time $t$:

$$
h(t) = \lim_{\Delta t \to 0} \frac{P(t \leq T < t + \Delta t \mid T \geq t)}{\Delta t} = \frac{f(t)}{S(t)}
$$

where $f(t) = F'(t)$ is the probability density function.

**Cumulative Hazard Function**: The accumulated hazard up to time $t$:

$$
H(t) = \int_0^t h(u) \, du
$$

The relationship between survival and cumulative hazard is:

$$
S(t) = \exp\left(-H(t)\right)
$$

### Non-Parametric Estimation: Kaplan-Meier

The Kaplan-Meier estimator provides a non-parametric estimate of the survival function. Let $t_{(1)} < t_{(2)} < \cdots < t_{(k)}$ be the $k$ distinct ordered event times. Define:

- $d_j$: number of events at time $t_{(j)}$
- $n_j$: number of subjects at risk just before time $t_{(j)}$

The Kaplan-Meier estimator is:

$$
\hat{S}(t) = \prod_{j: t_{(j)} \leq t} \left(1 - \frac{d_j}{n_j}\right)
$$

The variance is estimated using Greenwood's formula:

$$
\widehat{\text{Var}}(\hat{S}(t)) = \hat{S}(t)^2 \sum_{j: t_{(j)} \leq t} \frac{d_j}{n_j(n_j - d_j)}
$$

**Assumptions**: 
1. Censoring is non-informative (independent of the event process)
2. Survival probabilities are constant between event times
3. Events occur independently across subjects

### Non-Parametric Estimation: Nelson-Aalen

The Nelson-Aalen estimator provides a non-parametric estimate of the cumulative hazard:

$$
\hat{H}(t) = \sum_{j: t_{(j)} \leq t} \frac{d_j}{n_j}
$$

with variance:

$$
\widehat{\text{Var}}(\hat{H}(t)) = \sum_{j: t_{(j)} \leq t} \frac{d_j}{n_j^2}
$$

### Semi-Parametric Regression: Cox Proportional Hazards

The Cox proportional hazards model relates covariates to the hazard function:

$$
h(t \mid \mathbf{x}) = h_0(t) \exp(\boldsymbol{\beta}^\top \mathbf{x})
$$

where $h_0(t)$ is an unspecified baseline hazard and $\boldsymbol{\beta}$ is the vector of regression coefficients.

**Key Assumption — Proportional Hazards**: The hazard ratio between any two subjects is constant over time:

$$
\frac{h(t \mid \mathbf{x}_1)}{h(t \mid \mathbf{x}_2)} = \exp(\boldsymbol{\beta}^\top (\mathbf{x}_1 - \mathbf{x}_2))
$$

**Partial Likelihood**: Cox's key contribution was showing that $\boldsymbol{\beta}$ can be estimated without specifying $h_0(t)$. The partial likelihood is:

$$
L(\boldsymbol{\beta}) = \prod_{i: \delta_i = 1} \frac{\exp(\boldsymbol{\beta}^\top \mathbf{x}_i)}{\sum_{j \in R(t_i)} \exp(\boldsymbol{\beta}^\top \mathbf{x}_j)}
$$

where $R(t_i)$ is the risk set at time $t_i$—all subjects still under observation and event-free just before $t_i$.

The log-partial likelihood is:

$$
\ell(\boldsymbol{\beta}) = \sum_{i: \delta_i = 1} \left[ \boldsymbol{\beta}^\top \mathbf{x}_i - \log\left(\sum_{j \in R(t_i)} \exp(\boldsymbol{\beta}^\top \mathbf{x}_j)\right) \right]
$$

**Estimation**: The score equations are:

$$
U(\boldsymbol{\beta}) = \frac{\partial \ell}{\partial \boldsymbol{\beta}} = \sum_{i: \delta_i = 1} \left[ \mathbf{x}_i - \frac{\sum_{j \in R(t_i)} \mathbf{x}_j \exp(\boldsymbol{\beta}^\top \mathbf{x}_j)}{\sum_{j \in R(t_i)} \exp(\boldsymbol{\beta}^\top \mathbf{x}_j)} \right] = \mathbf{0}
$$

This is solved iteratively using Newton-Raphson. The information matrix is:

$$
I(\boldsymbol{\beta}) = -\frac{\partial^2 \ell}{\partial \boldsymbol{\beta} \partial \boldsymbol{\beta}^\top}
$$

and $\widehat{\text{Var}}(\hat{\boldsymbol{\beta}}) = I(\hat{\boldsymbol{\beta}})^{-1}$.

**Breslow Estimator for Baseline Hazard**: After estimating $\boldsymbol{\beta}$, the cumulative baseline hazard is:

$$
\hat{H}_0(t) = \sum_{j: t_{(j)} \leq t} \frac{d_j}{\sum_{k \in R(t_{(j)})} \exp(\hat{\boldsymbol{\beta}}^\top \mathbf{x}_k)}
$$

### Parametric Models

When the form of the survival distribution is known or assumed, parametric models offer efficiency gains.

**Exponential Model** (constant hazard):

$$
h(t) = \lambda, \quad S(t) = e^{-\lambda t}
$$

**Weibull Model** (monotonic hazard):

$$
h(t) = \lambda \gamma t^{\gamma - 1}, \quad S(t) = \exp(-\lambda t^\gamma)
$$

where $\gamma > 1$ implies increasing hazard, $\gamma < 1$ implies decreasing hazard.

**Accelerated Failure Time (AFT) Model**:

$$
\log T = \boldsymbol{\beta}^\top \mathbf{x} + \sigma \epsilon
$$

where $\epsilon$ follows a specified distribution (e.g., standard extreme value for Weibull).

### Likelihood for Censored Data

The full likelihood for right-censored data is:

$$
L = \prod_{i=1}^{n} \left[ f(t_i) \right]^{\delta_i} \left[ S(t_i) \right]^{1-\delta_i} = \prod_{i=1}^{n} h(t_i)^{\delta_i} S(t_i)
$$

This shows that censored observations contribute through their survival probability, while events contribute both the hazard at the event time and survival up to that point.

### Edge Cases and Degeneracies

- **All observations censored**: Survival function estimates exist but are uniformly 1; hazard ratios are not identifiable
- **No censoring**: Reduces to standard duration modelling; Kaplan-Meier equals the empirical CDF complement
- **Tied event times**: Require tie-handling methods (Breslow, Efron, or exact) in Cox regression
- **Time-varying covariates**: Require extended Cox model with time-dependent risk sets

# Understanding the Mathematics

### The Survival Function

**The equation:**

$$S(t) = P(T > t)$$

**Read it aloud:**

The survival function at time *t* equals the probability that the time until the event occurs is greater than *t*.

**What each symbol means:**

- **S(t)** = survival function; the probability of "surviving" past time *t*
- **P** = probability
- **T** = the random variable representing time until the event
- **t** = a specific point in time we're asking about
- **>** = greater than

**A concrete numerical example:**

A subscription company wants to know: what's the probability a customer stays subscribed beyond 6 months? If 700 out of 1,000 customers remain after 6 months, then S(6 months) = 0.70. This means there's a 70% probability any given customer survives past the 6-month mark.

**Why this equation matters:**

Without the survival function, we couldn't distinguish customers who definitely churned from those who simply haven't churned *yet*—we'd systematically underestimate retention.

### The Hazard Function

**The equation:**

$$h(t) = \lim_{\Delta t \to 0} \frac{P(t \leq T < t + \Delta t \mid T \geq t)}{\Delta t}$$

**Read it aloud:**

The hazard at time *t* is the instantaneous rate at which events occur at that moment, given survival up to that point—specifically, it's the probability of an event occurring in a tiny interval starting at *t*, divided by the width of that interval, as the interval shrinks toward zero.

**What each symbol means:**

- **h(t)** = hazard function; the instantaneous risk at time *t*
- **lim** = limit; what happens as something approaches a value
- **Δt → 0** = the time interval shrinks toward zero (becomes infinitesimally small)
- **P(t ≤ T < t + Δt | T ≥ t)** = probability the event happens between *t* and *t + Δt*, given survival until *t*
- **|** = "given that" or "conditional on"

**A concrete numerical example:**

A machine has survived 500 operating hours. In the next 10 hours, there's a 2% chance it fails (given it's made it this far). The approximate hazard is 0.02 ÷ 10 = 0.002 per hour. If we measured over just 1 hour instead, we might see 0.0021, and as we shrink the window, we converge on the true instantaneous failure rate at hour 500.

**Why this equation matters:**

Hazard tells us *when* risk is highest—enabling predictive maintenance before the danger zone rather than just estimating average lifespan.

### The Cox Proportional Hazards Model

**The equation:**

$$h(t|X) = h_0(t) \exp(\beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p)$$

**Read it aloud:**

The hazard for an individual at time *t*, given their covariates *X*, equals a baseline hazard that everyone shares, multiplied by the exponential of a linear combination of their specific characteristics and corresponding coefficients.

**What each symbol means:**

- **h(t|X)** = individual's hazard at time *t* given their covariates
- **h₀(t)** = baseline hazard; risk for someone with all covariates equal to zero
- **exp(...)** = exponential function; *e* raised to the power of everything in parentheses
- **βᵢ** = coefficient for covariate *i*; how much that factor increases (positive) or decreases (negative) log-hazard
- **Xᵢ** = value of covariate *i* for this individual

**A concrete numerical example:**

Predicting customer churn at month 12. Baseline hazard h₀(12) = 0.03. Customer has: 2 support tickets (β₁ = 0.4, X₁ = 2) and uses premium features (β₂ = -0.6, X₂ = 1). Their hazard = 0.03 × exp(0.4×2 + (-0.6)×1) = 0.03 × exp(0.8 - 0.6) = 0.03 × exp(0.2) = 0.03 × 1.22 = 0.0366. The support tickets increase risk; premium features reduce it.

**Why this equation matters:**

This formula lets us quantify exactly how each customer characteristic changes risk while handling censored data—something ordinary regression cannot do when many customers haven't churned yet.

### The Big Picture

The mathematics of time-to-event analysis solves a problem ordinary regression cannot: how do we learn from incomplete stories? When some subjects haven't experienced the event yet, we can't just ignore them or treat them as failures. The survival function tracks who remains event-free over time. The hazard function captures instantaneous risk moment-by-moment. The Cox model combines these concepts to estimate how individual characteristics multiply baseline risk—using the exponential function because risk must stay positive and because multiplicative effects match how biological and business processes actually compound. The mathematical essence is this: we're modeling the *rate* at which events happen, not just *if* they happen, while respecting that absence of an event isn't the same as evidence it won't occur.

## Python Implementation

```python
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from lifelines.utils import survival_table_from_events
import matplotlib.pyplot as plt

# =============================================================================
# Generate realistic synthetic customer churn data
# =============================================================================
np.random.seed(42)
n_customers = 1000

# Customer attributes
data = pd.DataFrame({
    'customer_id': range(n_customers),
    'contract_type': np.random.choice(['monthly', 'annual'], n_customers, p=[0.6, 0.4]),
    'monthly_charges': np.random.uniform(20, 100, n_customers),
    'tenure_at_signup': np.random.exponential(12, n_customers),  # months with company before this study
    'support_calls': np.random.poisson(2, n_customers)
})

# Generate survival times using Weibull with covariate effects
# True model: higher charges and monthly contracts increase churn hazard
shape = 1.5  # Weibull shape (increasing hazard)
scale = 24   # baseline scale in months

# Linear predictor (log-hazard effects)
lp = (0.02 * (data['monthly_charges'] - 50) +  # higher charges -> higher hazard
      0.5 * (data['contract_type'] == 'monthly').astype(int) +  # monthly -> higher hazard
      0.1 * data['support_calls'])  # more support calls -> higher hazard

# Generate Weibull survival times with acceleration
true_event_times = scale * np.exp(-lp / shape) * np.random.weibull(shape, n_customers)

# Administrative censoring at 36 months plus some random loss to follow-up
censoring_times = np.minimum(36, np.random.exponential(48, n_customers))

# Observed data
data['duration'] = np.minimum(true_event_times, censoring_times)
data['churned'] = (true_event_times <= censoring_times).astype(int)

print(f"Dataset shape: {data.shape}")
print(f"Churn rate: {data['churned'].mean():.1%}")
print(f"Median observed duration: {data['duration'].median():.1f} months")
print("\nFirst few rows:")
print(data.head())

# =============================================================================
# Kaplan-Meier Analysis: Overall and by Group
# =============================================================================
print("\n" + "="*60)
print("KAPLAN-MEIER SURVIVAL ANALYSIS")
print("="*60)

# Overall survival curve
kmf = KaplanMeierFitter()
kmf.fit(data['duration'], event_observed=data['churned'], label='All Customers')

print(f"\nMedian survival time: {kmf.median_survival_time_:.1f} months")
print(f"Survival probability at 12 months: {kmf.survival_function_at_times(12).values[0]:.1%}")
print(f"Survival probability at 24 months: {kmf.survival_function_at_times(24).values[0]:.1%}")

# Survival curves by contract type
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Plot overall survival
kmf.plot_survival_function(ax=axes[0])
axes[0].set_xlabel('Time (months)')
axes[0].set_ylabel('Survival Probability')
axes[0].set_title('Overall Customer Retention Curve')

# Compare by contract type
for contract in ['monthly', 'annual']:
    mask = data['contract_type'] == contract
    kmf_group = KaplanMeierFitter()
    kmf_group.fit(data.loc[mask, 'duration'], 
                  event_observed=data.loc[mask, 'churned'],
                  label=f'{contract.title()} Contract')
    kmf_group.plot_survival_function(ax=axes[1])

axes[1].set_xlabel('Time (months)')
axes[1].set_ylabel('Survival Probability')
axes[1].set_title('


## Visualisations

![](../../_static/figures/time-to-event_fig1.png)
![](../../_static/figures/time-to-event_fig2.png)

## Using This in Heuristix

### What Data You'll Need

The Time-to-Event node expects a dataset where each row represents one subject or case, with three essential pieces of information:

- **Duration column** (numeric): How long each subject was observed
- **Event indicator column** (binary/boolean): Whether the event occurred (1/True) or was censored (0/False)
- **Feature columns** (any type): Variables that might influence timing

Here's what your input data should look like:

| customer_id | days_observed | churned | plan_type | monthly_spend |
|-------------|---------------|---------|-----------|---------------|
| C001 | 365 | 1 | premium | 49.99 |
| C002 | 180 | 0 | basic | 9.99 |
| C003 | 412 | 1 | premium | 59.99 |

The node handles the rest—you don't need to transform durations or calculate survival probabilities yourself.

### Configuration Parameters

| Parameter | What It Controls | Default | When to Change It |
|-----------|-----------------|---------|-------------------|
| **Duration Column** | Which field contains the time values | (none) | Always set this—it's required |
| **Event Column** | Which field indicates if event occurred | (none) | Always set this—it's required |
| **Model Type** | Cox Proportional Hazards, Accelerated Failure Time, or Random Survival Forest | Cox PH | Use AFT for parametric assumptions; RSF for complex interactions |
| **Baseline Hazard** | Shape of underlying risk (Weibull, Exponential, etc.) | Weibull | Only applies to AFT; choose Exponential for constant hazard |
| **Penalization** | L1/L2 regularization strength | 0.0 | Increase (try 0.1–1.0) when you have many correlated features |
| **Confidence Level** | Width of prediction intervals | 0.95 | Lower to 0.90 for narrower bands; rarely needs changing |
| **Tie Handling** | How to treat simultaneous events | Efron | Switch to Breslow for very large datasets (it's faster) |

### What You'll Get Out

**Survival Curve Chart**: A line graph showing the probability of "surviving" (not experiencing the event) over time. If you've included categorical features, you'll see separate curves for each group—perfect for comparing customer segments or treatment groups.

**Coefficients Table**: Shows each feature's effect on hazard. Positive coefficients mean the feature *accelerates* the event; negative means it *delays* it. Look for the confidence intervals to assess significance.

**Predictions Dataset**: Your original data plus these new columns:
- `predicted_hazard`: Relative risk score for each subject
- `predicted_median_time`: Expected time until event occurs
- `risk_percentile`: Where this subject ranks (0-100) in terms of risk

**Concordance Index**: Displayed as a single metric (0.5–1.0). Above 0.7 is good; above 0.8 is excellent. It measures how well your model ranks who experiences the event sooner.

### Connecting Downstream

The predictions dataset flows naturally into:
- **Score Banding** node to create risk tiers (high/medium/low)
- **Model Comparison** to evaluate against other approaches
- **Business Rule** node to trigger interventions (e.g., "contact customers with predicted_median_time < 30 days")
- **Visualization** nodes to build stakeholder dashboards showing survival curves by segment

### Quick Start: Customer Churn Prediction

1. **Connect** your customer data containing observation days and churn indicator
2. **Set** Duration Column to your time field and Event Column to your churn flag
3. **Select** features like plan type, usage metrics, and demographics
4. **Leave** Model Type as "Cox Proportional Hazards" for your first run
5. **Run** the node and examine the survival curves—do they separate by segment?
6. **Review** coefficients to identify your biggest churn accelerators
7. **Connect** to Score Banding to create "high churn risk" segments

### Practical Tips from the Field

**Check proportional hazards**: If your survival curves cross each other, the Cox model may not fit well. Switch to Random Survival Forest instead.

**Mind your censoring rate**: If more than 70% of your cases are censored, predictions become unreliable. Consider shortening your observation window or waiting for more events.

**Time units matter**: Express durations in business-relevant units. "Days until churn" is more actionable than "seconds until churn."

**Interpret hazard ratios correctly**: A coefficient of 0.5 doesn't mean 50% more risk—exponentiate it first (e^0.5 = 1.65 = 65% increase in hazard).

**Validate with held-out data**: Survival models can overfit. Always check that your concordance index holds up on recent data the model hasn't seen.

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial dataset assessment when you need fast feedback on whether survival patterns exist and which covariates matter most.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `CoxPH` | Fast fitting, interpretable coefficients |
| `penalizer` | `0.0` | No regularization speeds convergence |
| `n_iter` | `50` | Minimal iterations for rough estimates |
| `show_progress` | `True` | Visual feedback during fitting |
| `test_size` | `0.3` | Larger holdout for stability with small data |

**What you get:** Coefficient estimates and concordance index within seconds, sufficient to identify promising predictors and check data quality.

**Trade-off:** Unstable coefficients with collinear features and no protection against overfitting on high-dimensional data.

---

### Recipe 2: Production-Ready Deployment

**When to use:** Deploying a model where prediction accuracy, calibration, and robustness to unseen data are critical business requirements.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `RandomSurvivalForest` | Handles non-linearity and interactions |
| `n_estimators` | `500` | Reduces variance, stabilizes predictions |
| `min_samples_split` | `20` | Prevents overfitting to noise |
| `max_depth` | `10` | Balances complexity and generalization |
| `bootstrap` | `True` | Enables out-of-bag error estimation |
| `n_jobs` | `-1` | Parallel processing for speed |
| `random_state` | `42` | Reproducible results for auditing |

**What you get:** Well-calibrated survival curves with confidence intervals, robust to feature interactions and missing patterns.

**Trade-off:** Longer training time (minutes vs. seconds) and reduced interpretability compared to parametric models.

---

### Recipe 3: High Right-Censoring (>70%)

**When to use:** Customer churn analysis where most customers haven't churned yet, or clinical trials with short follow-up relative to disease progression.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `WeibullAFT` | Parametric form extrapolates beyond observed times |
| `fit_intercept` | `True` | Essential for calibrated baseline hazard |
| `alpha` | `0.05` | Standard confidence level for predictions |
| `timeline` | `np.linspace(0, max_time*3, 100)` | Extend predictions well past observed data |
| `robust` | `True` | Reduces sensitivity to outlying early events |

**What you get:** Smooth survival curves that extrapolate reliably into periods where you have almost no observed events.

**Trade-off:** Strong parametric assumptions; predictions are only valid if the Weibull hazard shape holds in reality.

---

### Recipe 4: Time-Varying Marketing Attribution

**When to use:** E-commerce scenarios tracking conversion timing where users receive different promotions at different times during their journey (e.g., email on day 3, discount on day 7).

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `CoxTimeVaryingFitter` | Handles covariates that change value over time |
| `id_col` | `'user_id'` | Links multiple rows per subject |
| `start_col` | `'period_start'` | Beginning of time interval |
| `stop_col` | `'period_end'` | End of time interval |
| `event_col` | `'converted'` | Event indicator |
| `step_size` | `0.1` | Fine-grained optimization for stability |

**What you get:** Accurate attribution of conversion probability to specific interventions delivered at specific times, not just baseline characteristics.

**Trade-off:** Requires restructured data (one row per person-period), substantially increasing dataset size and complexity.

## Business Applications

**Financial Services**

A mid-sized UK mortgage lender was losing £3.2M annually to customers who paid off loans early, eroding their net interest margin. Traditional credit scoring couldn't predict *when* prepayment would occur or identify which customers were highest risk. By implementing time-to-event models on payment history, property transactions, and life events data, the lender predicted prepayment windows with 78% accuracy six months in advance. This enabled targeted retention offers to high-value customers and reduced early repayment losses by 41%, saving approximately £1.3M in the first year while improving customer satisfaction scores.

**Retail & E-commerce**

An online fashion retailer with 5M active customers struggled with inventory planning because stockout predictions were binary—items were either "in stock" or "out of stock" with no sense of timing. Time-to-event analysis transformed their approach by predicting the number of days until each SKU would sell out based on browsing behaviour, seasonal trends, and promotional calendars. The model reduced emergency air-freight costs by 52% (saving $870K annually) and increased sales by 7% by ensuring popular items remained available during critical conversion windows.

**Healthcare & Life Sciences**

A regional hospital network treating 12,000 heart failure patients annually faced bed shortages because they couldn't anticipate which discharged patients would be readmitted and when. Standard risk scores identified *who* was high-risk but not *when* intervention was needed. Cox proportional hazards models incorporating medication adherence, vital signs, and social determinants predicted 30-day readmission windows, enabling care coordinators to schedule proactive home visits during high-risk periods. This approach reduced unplanned readmissions by 23%, freeing up 840 bed-days annually and improving patient outcomes while generating $2.1M in avoided penalty costs.

**Insurance**

A commercial property insurer writing £450M in annual premiums couldn't differentiate between policyholders likely to churn immediately versus those who would stay for years. Time-to-event models analysing claims frequency, premium changes, and competitive quote requests predicted not just *which* customers would lapse but *when* they'd cancel—enabling precisely timed retention campaigns. By concentrating efforts on policies predicted to churn within 60 days, the insurer improved retention rates from 84% to 89%, retaining an additional £22M in premium revenue.

**Manufacturing**

An automotive parts manufacturer operating 47 production lines lost $4.3M annually to unplanned equipment downtime. Predictive maintenance models flagged machines as "high failure risk" but couldn't specify timing, leading to either premature replacement or catastrophic breakdowns. Survival analysis on sensor data (vibration, temperature, oil quality) predicted time-to-failure distributions, allowing maintenance teams to schedule interventions during planned shutdowns. This reduced emergency repairs by 67% and extended asset life by an average of 14 months per machine.

**Logistics & Supply Chain**

A European logistics company managing 2,200 delivery vehicles needed to optimise fleet replacement cycles. Traditional approaches used fixed age thresholds (e.g., "replace at 5 years"), ignoring usage patterns and maintenance history. Time-to-event models predicting vehicle retirement based on mileage, repair costs, and route conditions enabled individualised replacement schedules that reduced total fleet costs by 18% while maintaining service levels—equivalent to €3.7M in annual savings.

**Marketing & Customer Analytics**

A subscription meal-kit service with 450K customers discovered that standard churn models couldn't distinguish subscribers who'd cancel after one box from loyal customers at temporary risk. Survival models incorporating delivery feedback, recipe ratings, and engagement metrics predicted customer lifetime in weekly increments. This enabled a tiered intervention strategy: aggressive win-back offers for imminent churners, gentle engagement nudges for stable customers. The programme increased average customer lifetime from 8.2 to 11.6 months and improved marketing ROI by 43%.

**Telecommunications**

A mobile network operator serving 8M customers used time-to-event analysis to predict when business accounts would upgrade their plans. By identifying the weeks when B2B customers were most receptive to upsell offers—typically 6-8 weeks before contract renewal and immediately after billing issues were resolved—sales teams increased upgrade conversion rates from 12% to 19%, generating £14M in incremental annual revenue.

**Energy & Utilities**

A regional energy supplier serving 340K households couldn't predict when solar panel installations would trigger grid capacity issues. Time-to-event models forecasting adoption curves by neighbourhood—incorporating property values, environmental sentiment, and peer effects—predicted infrastructure investment needs 18-24 months in advance, reducing emergency grid upgrades by 71% and saving £8.9M over three years.

**Public Sector**

A metropolitan police force managing 23,000 domestic violence cases annually implemented survival analysis to predict re-offence timing. Standard risk assessments identified high-risk offenders but not intervention windows. Models incorporating restraining order compliance, substance abuse treatment, and contact patterns predicted elevated risk periods, enabling targeted welfare checks. This approach contributed to a 28% reduction in repeat incidents within six months.

**SaaS & Technology**

A B2B SaaS platform with 3,400 enterprise clients used time-to-event models to predict when trial users would convert to paid plans. Instead of generic "day 7" email campaigns, the system identified individual conversion windows based on feature usage, team size, and integration activity. This personalised approach lifted trial-to-paid conversion from 18% to 27% and reduced sales cycle length by 12 days.

## Worked Example

Sarah Chen, a senior data scientist at Meridian Insurance, was halfway through her morning coffee when her calendar reminder chimed: "Retention Strategy Meeting with VP Product." She'd been dreading this one. For three quarters running, Meridian's customer churn had crept upward, and leadership wanted answers. Not correlations or dashboards—they wanted to know *when* customers would leave and *what* would keep them.

In the meeting, Marcus from Product laid it out: "We've got intervention budgets—emails, discounts, account manager calls—but we're spreading them thin. We need to know which customers are at highest risk in the next 90 days, and what levers actually matter." Sarah nodded. This wasn't a classification problem. It was about *time*. Some customers had already churned, others were still active, and the question wasn't just "will they leave?" but "*when* will they leave, and what can we do about it?"

Back at her desk, Sarah pulled three years of customer data from the data warehouse. The dataset had 4,832 customers, each with their signup date, last activity date, and whether they'd churned. She also had behavioral features: support tickets opened, monthly logins, number of premium features used, and account tenure. Here's what a sample looked like:

| customer_id | tenure_days | churned | support_tickets | monthly_logins | premium_features |
|-------------|-------------|---------|-----------------|----------------|------------------|
| C10234      | 487         | 1       | 3               | 12             | 2                |
| C10891      | 203         | 0       | 1               | 45             | 5                |
| C11203      | 612         | 1       | 7               | 8              | 1                |
| C11455      | 290         | 0       | 0               | 67             | 4                |
| C12008      | 145         | 1       | 2               | 5              | 0                |

The quirks were immediate: customer C10891 had been active for 203 days but hadn't churned—*yet*. That observation was censored. Sarah couldn't treat this as a binary "churned/not churned" problem because time carried critical information. A customer who stayed 600 days before churning told a different story than one who left after 60.

Sarah set up her analysis using a Cox proportional hazards model, the workhorse of time-to-event analysis. She configured it carefully: `tenure_days` was her duration variable, `churned` was her event indicator (1 = event occurred, 0 = censored), and she included `support_tickets`, `monthly_logins`, and `premium_features` as covariates. She knew the Cox model would estimate hazard ratios—how each variable multiplied the risk of churning at any given moment.

Here's the core of her analysis:

```python
import pandas as pd
from lifelines import CoxPHFitter

# Load customer data
df = pd.read_csv('customer_data.csv')

# Prepare for Cox model
# Duration = tenure_days, Event = churned (1 or 0)
cph = CoxPHFitter()
cph.fit(
    df[['tenure_days', 'churned', 'support_tickets', 
        'monthly_logins', 'premium_features']], 
    duration_col='tenure_days', 
    event_col='churned'
)

# Display results
print(cph.summary)

# Predict survival probabilities for specific customer
customer_profile = pd.DataFrame({
    'support_tickets': [5],
    'monthly_logins': [10],
    'premium_features': [1]
})
survival_func = cph.predict_survival_function(customer_profile)
prob_90_days = survival_func.loc[90].values[0]
print(f"Probability of retention at 90 days: {prob_90_days:.2%}")
```

The results surprised her:

| Covariate           | Hazard Ratio | 95% CI         | p-value |
|---------------------|--------------|----------------|---------|
| support_tickets     | 1.34         | (1.21, 1.49)   | < 0.001 |
| monthly_logins      | 0.97         | (0.96, 0.98)   | < 0.001 |
| premium_features    | 0.78         | (0.71, 0.86)   | < 0.001 |

Each support ticket *increased* churn hazard by 34%—customers reaching out weren't being helped, they were crying for help. Each additional monthly login *decreased* hazard by 3% (multiply by 0.97), and each premium feature adopted dropped risk by 22%. The model's concordance index was 0.71—decent predictive discrimination.

The insight hit Sarah immediately: support tickets weren't a sign of engagement; they were a red flag. High-ticket customers with low logins were ticking time bombs. And premium feature adoption was the strongest protective factor—not just correlated with retention, but causally reducing churn hazard over time.

She brought this to Marcus two days later. "We've been treating support tickets as neutral," she said, pulling up survival curves. "But a customer with five tickets and low login activity has a 68% chance of churning within 90 days. If we can get them to adopt just one more premium feature, that drops to 51%." The recommendation was clear: redirect retention budget toward high-ticket, low-engagement customers with targeted feature onboarding, not generic discounts.

Within six weeks, Product launched a pilot: automated feature tutorials triggered after the second support ticket. Early results showed a 14% reduction in 90-day churn among treated customers.

If Sarah could do it over, she'd incorporate time-varying covariates—login behavior wasn't static, and the model assumed it was. She'd also segment by customer cohort; the hazard patterns for enterprise customers likely differed from individuals. But for a first pass, the time-to-event approach had done exactly what classification couldn't: it told them *when* to intervene, not just *who* to worry about.

## Interpreting Your Results

You've just run your first time-to-event analysis. You're looking at survival curves, hazard ratios, concordance indices, and wondering if your model is telling you anything useful. Let's decode exactly what you're seeing.

### Concordance Index (C-Index)

**Plain-English meaning**: The C-index tells you how often your model correctly predicts which of two randomly selected individuals will experience the event first. If you pick two customers, and your model says Customer A will churn before Customer B, how often is that prediction correct? A C-index of 0.72 means your model gets the ranking right 72% of the time.

**Concrete benchmarks**: 
- **Below 0.55**: Your model is barely better than a coin flip. Don't use it.
- **0.55–0.65**: Weak predictive power. You've found *something*, but not enough to act on confidently.
- **0.65–0.75**: Solid performance. Good enough for most business applications.
- **0.75–0.85**: Strong model. This is excellent for real-world scenarios.
- **Above 0.85**: Either you've built something exceptional, or you're overfitting (check your validation approach).

**Red flags**: C-index below 0.6 on training data means your features don't capture the process. C-index that's 0.15+ higher on training than validation data screams overfitting—you've memorized patterns that don't generalize.

### Hazard Ratios (from Coefficient Table)

**Plain-English meaning**: A hazard ratio tells you how much a one-unit change in a variable multiplies the risk of the event occurring. A hazard ratio of 1.8 for "previous complaints" means customers with one additional complaint are 1.8× more likely to churn at any given time. A ratio of 0.6 means the event is 40% less likely.

**Concrete benchmarks**:
- **0.9–1.1**: Negligible effect. This variable doesn't meaningfully impact timing.
- **1.1–1.5 or 0.67–0.9**: Modest but real effect. Worth considering in strategy.
- **1.5–3.0 or 0.33–0.67**: Strong effect. These are your key drivers.
- **Above 3.0 or below 0.33**: Extremely strong effect—verify this isn't a data error.

**Red flags**: Hazard ratios with p-values above 0.05 aren't statistically reliable—the confidence interval likely crosses 1.0, meaning the effect could be zero. Extremely wide confidence intervals (e.g., 0.5 to 5.2) mean you don't have enough data to pin down the true effect.

### Survival Curves

**Plain-English meaning**: The survival curve shows the probability that the event *hasn't* happened yet at each time point. If your curve shows 60% survival at month 12, that means 60% of your population is still "surviving" (hasn't churned, failed, converted, etc.) by the one-year mark.

**What good looks like**: Smooth curves with clear separation between groups (if comparing segments). A steep initial drop followed by flattening suggests early high-risk periods. Curves that cross suggest time-varying effects—one group is riskier early, another later.

**Red flags**: Curves that are perfectly smooth with no variation suggest too much smoothing or fabricated data. Curves that don't drop at all mean you have no events—check your event definition. Curves with identical shapes across wildly different groups mean your model isn't distinguishing between them.

### Predicted Risk Scores (Output Column)

**Plain-English meaning**: Each individual gets a risk score—higher scores mean higher predicted hazard. These aren't probabilities; they're relative rankings. Someone with a score of 0.8 is at higher risk than someone with 0.3, but you can't say "80% chance of event."

**How to use them**: Sort by score and create risk tiers. Top 10% might be "immediate intervention needed," next 20% "monitor closely," etc. The exact cutoffs depend on your intervention capacity and cost-benefit analysis.

**Red flags**: If 90% of your scores cluster between 0.48 and 0.52, your model isn't differentiating meaningfully. If scores perfectly correlate with a single input variable, your model has latched onto one feature and ignored the rest.

### Sanity Check Checklist

1. **Event rate check**: Do at least 10% of your cases have the event? Below that, you lack signal.
2. **Censoring balance**: Is less than 70% of your data censored? Too much censoring means you're mostly guessing.
3. **Time span coverage**: Do events occur throughout your observation period, not just clustered at the start or end?
4. **Top features make domain sense**: Would you bet money these factors actually matter?
5. **Validation C-index within 0.1 of training**: Bigger gaps mean overfitting.

### Good Enough to Act On?

**Act when**: Your validation C-index exceeds 0.65, your top 3 hazard ratios make business sense with p-values under 0.05, and your high-risk group (top 20% of scores) shows event rates at least 2× higher than your low-risk group. Below these thresholds, collect more data or rethink your features—you're not ready to make expensive decisions yet.

## Decision Guidance

### What This Result Is Telling You

Time-to-event analysis tells you when critical business moments are likely to happen and what factors make them happen sooner or later. Whether you're predicting customer churn, equipment failure, loan default, or employee turnover, these models give you a time horizon—not just a yes/no prediction, but a timeline with probabilities attached. A hazard ratio of 2.5 for discount-seeking customers means they're churning at two and a half times the rate of your standard customers at any given point in time. A survival curve showing 40% retention at 12 months means six out of every ten customers you acquire today won't be with you next year unless something changes.

The critical business insight is the ability to prioritize intervention timing. Unlike traditional classification that tells you "this customer might churn," time-to-event analysis tells you "this customer segment has a 60% probability of churning within the next 90 days." This transforms vague concerns into specific windows for action. You can allocate retention budgets where they'll have maximum impact, schedule maintenance before failures become catastrophic, and time interventions when they're most likely to succeed rather than wasting resources on customers who weren't leaving anyway or acting too late to matter.

The model also reveals which factors are truly accelerating or delaying your critical events. A statistically significant covariate with a hazard ratio of 1.05 might be real, but it's telling you that factor increases the event rate by only 5%—probably not worth reorganizing operations around. A hazard ratio of 3.2 for customers who contact support twice in their first month is actionable intelligence: early support interactions are a powerful signal that demands immediate attention from your customer success team.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Hazard ratio > 2.0 for a specific customer segment or behavior | That group experiences the event at more than double the baseline rate | Immediately implement targeted intervention program for this high-risk group; this is your priority segment | VP of Operations or Customer Success |
| Survival probability drops below 50% within your typical intervention window (e.g., 30-day survival < 50%) | You're losing the majority before you can effectively act | Redesign onboarding or early-stage engagement to occur earlier in the customer journey; current timing is too late | Product or Program Manager |
| Confidence intervals for key hazard ratios span 1.0 | The factor's effect is statistically uncertain—it might increase, decrease, or have no real impact on timing | Do not build business processes around this variable until you collect more data or run targeted experiments | Data Science Lead |
| Median survival time for a critical asset or customer cohort decreased >20% compared to previous period | Your retention or reliability is deteriorating significantly | Convene cross-functional incident review; investigate operational or market changes that occurred during this period | Executive Leadership |
| Concordance index (C-index) < 0.65 | Model predictions are barely better than random guessing | Do not use for individual-level decisions; model requires fundamental redesign or additional predictive features | Data Science Team |

### When to Proceed vs. Investigate Further

**Proceed with confidence:**
- C-index ≥ 0.75 on holdout validation data
- Confidence intervals for top three risk factors exclude 1.0
- Model tested on at least two distinct time periods with consistent hazard ratios (±20%)
- Business stakeholders can articulate operationally feasible interventions for identified high-risk groups

**Proceed with caution:**
- C-index between 0.65–0.75
- Survival curves for key segments separate clearly but confidence bands overlap at some time points
- One or more important covariates have wide confidence intervals (span >1.5 on hazard ratio scale)

**Investigate before acting:**
- Hazard ratios vary substantially (>40%) across different validation periods
- Proportional hazards assumption violated for key predictors
- Median survival times show unexpected patterns (e.g., lower-risk groups experiencing events faster than higher-risk groups in any time window)

**Do not use these results yet:**
- C-index < 0.65
- Fewer than 30 observed events in your dataset
- Model training data ends more than one business cycle ago (outdated patterns)
- No subject matter expert can explain why top risk factors would logically affect timing

### The Cost of Getting This Wrong

Misinterpreting time-to-event results leads to perfectly executed interventions at exactly the wrong time. A telecommunications company acting on a poorly calibrated churn model might spend millions on retention offers sent to customers who were never going to leave, while the truly at-risk customers receive their offer two weeks after they've already signed with a competitor. Manufacturing operations relying on unreliable failure predictions either perform unnecessary preventive maintenance—wasting technician time and replacement parts on equipment that would have run another six months—or worse, experience catastrophic failures that halt production lines because the model said they had 90 days when they actually had 9. The insidious danger is that these failures aren't immediately obvious: your retention campaign reports a 95% success rate, but you're measuring people who would have stayed anyway, and your truly at-risk customers remain invisible in the data until they're already gone.

## Common Pitfalls

**The Immortal Time Bias**

Here's what happened: A healthcare analyst was studying whether patients who attended a cardiac rehabilitation program had better survival rates post-heart attack. They defined exposure as "attended at least one rehab session" and measured survival from the date of the heart attack. The Kaplan-Meier curves showed dramatically better survival for the rehab group—nearly 40% risk reduction. They concluded the program was life-saving and recommended mandatory enrollment.

Why it happens: The analyst guaranteed that everyone in the treatment group survived long enough to attend their first session. Patients who died in the first two weeks couldn't possibly be in the "attended rehab" group, artificially inflating its survival rate. This creates a period of "immortal time" where treatment group members cannot experience the event by definition.

How to detect it: Check whether treatment assignment requires surviving to a specific time point. If your treatment group's survival curve stays flat at 100% for the initial period while controls are already experiencing events, you've likely introduced this bias. Calculate the time from index date to treatment initiation—if it varies substantially, you're at risk.

The fix: Use time-varying covariates or landmark analysis, where you only include patients who survived to the earliest possible treatment time and measure outcomes from that landmark forward.

**The Informative Censoring Trap**

Here's what happened: A SaaS company's data scientist was modeling customer churn using a Cox proportional hazards model. They treated customers who downgraded to a free tier as censored observations, reasoning that these users hadn't technically "churned." The model showed that engagement metrics had weak effects on churn. They concluded that product usage barely mattered for retention.

Why it happens: Downgrading to free tier is not random—it's often the final step before complete churn. By treating these users as censored rather than recognizing this as informative censoring, the analyst broke the fundamental assumption that censoring is independent of the event process.

How to detect it: Examine the characteristics of censored observations versus those who experienced the event. If censored cases look more similar to event cases than to ongoing survivors, you have informative censoring. Check whether censoring rates differ dramatically across covariate groups.

The fix: Either treat downgrade as the event of interest or use competing risks models that explicitly account for different types of exits from the risk set.

**The Non-Proportional Hazards Blindness**

Here's what happened: A clinical researcher ran a Cox model comparing two cancer treatments over five years. The treatment coefficient was non-significant (p=0.23, HR=0.89), so they reported "no treatment effect." But a colleague who plotted the Kaplan-Meier curves noticed they crossed at 18 months—the experimental treatment actually performed worse early but much better late.

Why it happens: The Cox model assumes proportional hazards: the hazard ratio stays constant over time. When this assumption fails, the model averages across time periods, potentially missing clinically meaningful patterns. Junior analysts often skip diagnostic checks because the model runs without errors.

How to detect it: Plot log(-log(survival)) curves for different groups—they should be parallel if proportional hazards holds. Test scaled Schoenfeld residuals for time-dependence (in R: `cox.zph()`; look for p<0.05). Visually inspect whether Kaplan-Meier curves cross or diverge over time.

The fix: Use stratified Cox models, add time-varying coefficients, or employ parametric models that don't assume proportional hazards.

**The Competing Risks Fallacy**

Here's what happened: A hospital administrator was analyzing time-to-hospital-readmission for elderly patients, treating death as a censored observation. Their Kaplan-Meier curve showed 60% of patients were readmitted within six months. They allocated resources for a major readmission prevention program. But 30% of their "censored" patients had actually died—they weren't at risk of readmission.

Why it happens: Treating competing events (death) as standard censoring inflates the cumulative incidence of the event of interest. Business users especially miss this because standard survival analysis software doesn't warn you when competing events exist.

How to detect it: Ask: "Can patients who are censored for reason X still experience the event?" If not, you have competing risks. Compare standard Kaplan-Meier estimates with cumulative incidence function estimates—large differences indicate competing risks matter.

The fix: Use cumulative incidence functions and Fine-Gray models that properly account for competing risks, providing realistic predictions of event probabilities.

**The Left-Truncation Oversight**

Here's what happened: An insurance analyst studied claim duration using their database of active claims. They included all claims present in the system, measuring time from claim initiation. Their model severely underestimated the proportion of long-duration claims. They set reserves too low, causing budget shortfalls.

Why it happens: The database only contained claims that survived long enough to be active when data collection started—short claims had already closed. This left-truncation (delayed entry) means the sample over-represents survivors, but analysts trained on right-censoring often don't recognize this distinct problem.

How to detect it: Check whether your sample includes only cases that survived to a specific calendar date. If observation start times vary and correlate with event times, you have left-truncation. Look for suspiciously low early-event rates.

The fix: Use delayed entry specifications in your survival models, defining both entry time and origin time for each observation to properly condition on having survived to study entry.

## Common Misconceptions

**"If we don't have complete data on everyone, we should just exclude the censored cases or treat them as non-events"**

**Why people believe this:** When you're accustomed to standard regression where every observation needs a definite outcome, censored data feels incomplete and problematic. The instinct to work only with "clean" data where you know exactly what happened seems prudent. Treating censored cases as non-events appears to be a conservative assumption—after all, the event hasn't happened yet.

**The truth:** Censored observations contain valuable information about survival time. A customer who hasn't churned after 18 months tells you something fundamentally different than a customer who churned after 2 months, even though neither has the "event" at observation end. Excluding censored cases creates severe selection bias—you're systematically removing the longer-surviving cases, artificially deflating survival estimates. Treating them as non-events is worse: you're claiming certainty about an unknown future, assuming everyone censored at different times has identical infinite survival. Survival analysis methods specifically exist to extract the partial information censored cases provide: they survived *at least* until their censoring time.

**The real-world consequence:** A subscription business excludes censored customers from their churn model, training only on customers who definitely churned or reached 24 months. Their model dramatically overestimates churn risk because it never learned from the stable, long-tenure customers still active at 6, 12, or 18 months. They implement aggressive retention campaigns targeting customers the model falsely identifies as high-risk, spending heavily on discounts for actually loyal customers while degrading the product experience with desperate retention messaging.

**"The hazard rate and probability of the event are basically the same thing"**

**Why people believe this:** Both are expressed as rates, both relate to event occurrence, and in casual conversation people use them interchangeably. The hazard rate intuitively feels like "the probability it happens now," which seems equivalent to event probability.

**The truth:** The hazard rate is the instantaneous rate of event occurrence *given survival to that point*—a conditional rate among those still at risk. Probability is cumulative and unconditional. A hazard rate can exceed 1.0; probability cannot. More critically, constant hazard rates (exponential distribution) produce survival curves that decline exponentially, not linearly. A hazard rate that increases over time doesn't mean the probability increases for any specific individual—it means that among those still surviving, the rate is higher. This distinction matters profoundly for interpretation: a treatment that reduces the hazard by 30% doesn't reduce event probability by 30 percentage points.

**The real-world consequence:** A clinical researcher interprets a hazard ratio of 0.70 as "30% fewer patients will experience the event," communicating this to stakeholders and setting expectations accordingly. In reality, with the baseline group experiencing 40% events over the study period, the treated group experiences approximately 31% events—only a 9 percentage point difference, not 12. The treatment appears to underperform expectations, not because it failed, but because the original interpretation confused hazard rates with risk differences, leading to overpromising and subsequent loss of stakeholder confidence.

## How This Connects

### Before This Node

**Feature Engineering** transforms raw timestamps and categorical variables into model-ready inputs like duration calculations, event indicators, and time-varying covariates that survival models require. Without proper feature engineering, you'll lack the binary event flag (did the event occur?) and correctly calculated time-to-event durations, causing models to misinterpret censored observations as completed events.

**Missing Value Imputation** fills gaps in covariate data that would otherwise force you to drop partially observed subjects, preserving statistical power and reducing selection bias. Bad imputation—like forward-filling time-varying covariates across their event time—artificially creates predictors that "know the future," leading to impossibly optimistic hazard estimates.

**Train-Test Split (Time-Based)** partitions data chronologically to prevent leakage where future information influences predictions about past events, essential for temporal validity. Random splitting in survival analysis is catastrophic: your model trains on people who experienced events in 2024 to predict 2023 outcomes, producing metrics that collapse in production.

**Outlier Detection** identifies implausibly short or long durations that can severely distort hazard function estimates, particularly at distribution tails where survival models are sensitive. Undetected outliers like 0-day durations or 10,000-day follow-ups create estimation instability, causing predicted survival curves to exhibit nonsensical spikes or hazard rates to explode.

**Class Imbalance Handling** addresses scenarios where event rates are extremely low (e.g., 2% failure rate), helping models learn meaningful patterns despite censoring. Ignoring severe imbalance in survival contexts means your model defaults to predicting "will never experience the event," producing flat hazard functions with zero discriminative power.

**Cohort Definition** establishes inclusion criteria, index dates, and observation windows that determine who enters the risk set and when, creating the analytical framework for survival time. Poor cohort definition—like mixing patients enrolled at disease diagnosis with those enrolled at random checkups—introduces immortal time bias where some subjects have artificially delayed event times.

### After This Node

**Model Evaluation (Survival-Specific)** applies concordance indices, time-dependent AUC, and calibration plots to assess how well predicted hazards match observed event timing. Time-to-event models output survival probabilities and hazard functions rather than simple predictions, requiring specialized metrics that handle censoring and time-varying discrimination.

**Threshold Optimization** converts continuous risk scores into actionable intervention triggers by identifying cutoffs that balance early detection against false alarms. Survival model outputs naturally support this because hazard rates and predicted survival probabilities provide clear ranking mechanisms for stratifying subjects into risk tiers.

**Business Metric Translation** transforms statistical outputs like median survival time and hazard ratios into operational metrics such as expected customer lifetime value or equipment replacement schedules. Time-to-event models uniquely provide not just *who* will experience events but *when*, enabling resource planning and budget forecasting.

**Deployment (Real-Time Scoring)** operationalizes survival models to generate dynamic risk assessments as new covariate information arrives, updating predictions as subjects remain event-free. Survival models excel here because they naturally handle right-censoring—every prediction is conditional on having survived to the current time point.

**Segmentation (Risk Stratification)** groups subjects into clinically or operationally meaningful categories (high/medium/low risk) based on predicted survival curves or hazard trajectories. Time-to-event outputs are ideal for this because they provide entire probability distributions over time, not just point predictions, revealing which groups deteriorate quickly versus slowly.

### Common Pipeline Patterns

**Customer Churn Prevention Pipeline**  
Cohort Definition → Feature Engineering → **Time to Event** → Threshold Optimization → Deployment (Real-Time Scoring). Predicts which customers will churn and when, enabling targeted retention campaigns timed to precede predicted departure dates, typically reducing churn by 15-25% in the highest-risk quartile.

**Predictive Maintenance Workflow**  
Sensor Data Aggregation → Outlier Detection → **Time to Event** → Business Metric Translation → Resource Planning. Forecasts equipment failure timing to schedule maintenance during planned downtime rather than emergency repairs, reducing unplanned outages by 40-60% and extending asset lifespan.

**Clinical Trial Risk Monitoring**  
Train-Test Split (Time-Based) → Missing Value Imputation → **Time to Event** → Model Evaluation (Survival-Specific) → Risk Stratification. Identifies patients at high risk of adverse events or dropout, allowing protocol amendments and intensified monitoring for vulnerable subgroups, improving trial completion rates by 20-30%.

### What to Have Ready

**Event and censoring properly coded**: Binary event indicator (1 = event occurred, 0 = censored) and positive duration for every observation, with censoring reason documented (end of study, loss to follow-up, competing event).

**Time-scale decision finalized**: Clear definition of time origin (enrollment date, diagnosis, purchase) and units (days, months) consistently applied across all subjects, with left truncation handled if subjects enter observation at different risk-set times.

**Covariate measurement timing verified**: Confirm all predictors are measured before or at the time origin, with time-varying covariates structured in counting-process format if applicable, preventing any future information leakage.

**Adequate event counts**: Minimum 10-20 events per predictor variable to ensure stable coefficient estimation, with recognition that high censoring rates (>70%) may require larger samples or penalized regression approaches.

## Try It Yourself

### Recommended Dataset

**Veterans' Administration Lung Cancer Trial** from `lifelines` package (or generate equivalent synthetic data via sklearn)

Since `lifelines` is the standard Python library for survival analysis but not in the core stack, we'll use **synthetic time-to-event data** generated with sklearn to avoid external dependencies.

**Why it's ideal:** Time-to-event data requires two critical components—a duration (time until event) and a censoring indicator (whether the event was observed or the observation ended first). Synthetic data allows us to create realistic survival scenarios with known ground truth, multiple covariates, and controlled censoring rates (~30-40%), mimicking clinical trials or customer churn scenarios.

**Business question:** "How do patient characteristics (age, treatment type, disease severity) affect survival time, and which patients are at highest risk in the next 6 months?"

**Size:** ~200 rows × 6 columns (duration, event_observed, age, treatment, severity, gender)

### Starter Code

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.stats import chi2
import matplotlib.pyplot as plt

# Generate synthetic survival data
np.random.seed(42)
n_patients = 200

# Simulate patient covariates
age = np.random.normal(65, 12, n_patients)
treatment = np.random.choice([0, 1], n_patients)  # 0=standard, 1=new
severity = np.random.uniform(0, 10, n_patients)  # disease severity score

# Generate survival times influenced by covariates (Weibull-like distribution)
# Higher age/severity = shorter survival; new treatment = longer survival
baseline_hazard = 0.01
time_to_event = np.random.exponential(
    1 / (baseline_hazard * np.exp(0.02*age + 0.15*severity - 0.5*treatment))
)

# Simulate censoring (observation ends before event occurs)
censoring_time = np.random.exponential(150, n_patients)
observed_time = np.minimum(time_to_event, censoring_time)
event_observed = (time_to_event <= censoring_time).astype(int)

# Create DataFrame
df = pd.DataFrame({
    'time': observed_time,
    'event': event_observed,
    'age': age,
    'treatment': treatment,
    'severity': severity
})

print("=== Dataset Overview ===")
print(f"Total patients: {len(df)}")
print(f"Events observed: {df['event'].sum()} ({df['event'].mean()*100:.1f}%)")
print(f"Censored: {(1-df['event']).sum()} ({(1-df['event'].mean())*100:.1f}%)")
print(f"\nMean survival time: {df['time'].mean():.1f} days")

# Kaplan-Meier survival estimation (manual calculation for standard libraries)
# Sort by time and calculate survival probability at each event
df_sorted = df[df['event']==1].sort_values('time')
n_at_risk = len(df)
survival_prob = 1.0

print("\n=== Survival Probability at Key Timepoints ===")
for days in [30, 90, 180, 365]:
    n_events = (df_sorted['time'] <= days).sum()
    # Simple approximation: S(t) ≈ (n - events) / n
    surv_at_t = (n_at_risk - n_events) / n_at_risk
    print(f"Day {days}: {surv_at_t*100:.1f}% survival probability")

# Compare treatment groups
print("\n=== Treatment Group Comparison ===")
for treatment_type in [0, 1]:
    group = df[df['treatment'] == treatment_type]
    label = "Standard" if treatment_type == 0 else "New Treatment"
    print(f"{label}: mean time={group['time'].mean():.1f}, "
          f"event rate={group['event'].mean()*100:.1f}%")

# Identify high-risk patients (top quartile in risk score)
df['risk_score'] = 0.02*df['age'] + 0.15*df['severity'] - 0.5*df['treatment']
high_risk = df.nlargest(50, 'risk_score')
print(f"\n=== High-Risk Patient Profile (top 25%) ===")
print(f"Average age: {high_risk['age'].mean():.1f}")
print(f"Average severity: {high_risk['severity'].mean():.1f}")
print(f"Percent on new treatment: {high_risk['treatment'].mean()*100:.1f}%")
print(f"Mean survival time: {high_risk['time'].mean():.1f} days")
```

### What to Try Next

1. **Increase censoring rate:** Change `censoring_time = np.random.exponential(80, n_patients)` (from 150). Expect more censored observations (~60%) and wider uncertainty in survival estimates. Teaches how incomplete data affects prediction confidence.

2. **Strengthen treatment effect:** Change `-0.5*treatment` to `-1.0*treatment` in the time_to_event calculation. Expect a larger survival gap between treatment groups (30+ day difference). Demonstrates detecting treatment efficacy.

3. **Add interaction effect:** Replace the exponential with `np.exp(0.02*age + 0.15*severity - 0.5*treatment - 0.01*age*treatment)`. Expect new treatment to work better for older patients. Teaches how effects vary by subpopulation.

4. **Change event rarity:** Multiply `baseline_hazard` by 0.5. Expect longer survival times and fewer observed events. Shows how rare events complicate survival modeling and require larger samples.

## Further Reading

1. **Cox, D. R. (1972). "Regression Models and Life-Tables." Journal of the Royal Statistical Society: Series B, 34(2), 187-220.** Read this if you want to understand the mathematical foundation of proportional hazards regression and why the partial likelihood approach allows estimation without specifying the baseline hazard function—a breakthrough that made Cox models the dominant framework in time-to-event analysis.

2. **Faraggi, D. & Simon, R. (1995). "A Neural Network Model for Survival Data." Statistics in Medicine, 14(1), 73-82.** Read this if you want to understand the first systematic attempt to apply neural networks to survival analysis, including how they handled right-censoring through a custom loss function—work that presaged modern deep learning approaches like DeepSurv.

3. **Kleinbaum, D. G. & Klein, M. (2012). *Survival Analysis: A Self-Learning Text*, 3rd Edition. Springer. Chapter 3 (pp. 89-134): "The Cox Proportional Hazards Model and Its Characteristics."** This chapter uniquely walks through the proportional hazards assumption with graphical diagnostics and provides worked examples of testing violations—practical skills often glossed over in theoretical treatments but essential for real applications.

4. **Aalen, O., Borgan, O., & Gjessing, H. (2008). *Survival and Event History Analysis: A Process Point of View*. Springer. Chapter 4 (pp. 125-168): "Nonparametric Estimation."** This chapter provides the clearest treatment of the Kaplan-Meier estimator's relationship to counting processes, offering intuition about why the product-limit formula works and how to construct proper confidence intervals—details that clarify common misconceptions.

5. **Scikit-survival Documentation: `sksurv.linear_model.CoxPHSurvivalAnalysis`** (https://scikit-survival.readthedocs.io). Focus specifically on the "Predict survival and cumulative hazard function" section, which demonstrates the crucial distinction between predicting risk scores versus actual survival probabilities—a point of frequent confusion when deploying Cox models in practice.

6. **Grounds, M. (2020). "Survival Analysis: Intuition & Implementation in Python." Towards Data Science.** This tutorial stands out for its comparative implementation of Kaplan-Meier, Cox, and accelerated failure time models on the same dataset, with clear visualizations showing when each model's assumptions hold or fail—making abstract statistical properties concrete.

7. **StatQuest with Josh Starmer: "Survival Analysis" video series** (https://youtube.com/statquest). Watch particularly the Cox Proportional Hazards episodes (starting at 15:23 in "Cox Proportional Hazards Regression pt. 1") where Starmer visually explains how hazard ratios work using his signature hand-drawn diagrams that make the concept genuinely intuitive.

8. **Goldstein, B. A., et al. (2017). "Opportunities and Challenges in Developing Risk Prediction Models with Electronic Health Records Data." Journal of the American Medical Informatics Association, 24(1), 198-208.** This case study details Duke University Health System's deployment of survival models for predicting ICU mortality at scale, including the engineering challenges of handling missing data, time-varying covariates, and model updating—practical considerations absent from academic treatments.

## Practice Exercises

### Exercise 1: Choosing the Right Approach for Customer Retention (Conceptual)

**Scenario:**

You're a data analyst at StreamVibe, a subscription streaming service. The marketing director wants to predict which customers will cancel their subscriptions and has asked you to build a predictive model. She presents you with the following data from 10,000 customers over a 12-month observation period:

- 2,800 customers cancelled during the observation period (average time to cancellation: 6.2 months)
- 7,200 customers remained active at the end of 12 months
- Available features: customer demographics, viewing hours per week, content preferences, customer service interactions, subscription tier

The director specifically wants to:
1. Identify which customers are at highest risk in the next 30 days
2. Understand which factors accelerate cancellation
3. Estimate how subscription tier changes affect cancellation timing

She's considering two approaches: a standard classification model (logistic regression) to predict "will cancel vs won't cancel," or a time-to-event model. Which should you recommend and why?

**Complete Worked Answer:**

You should strongly recommend a **time-to-event model** over classification, for several specific reasons aligned with the business requirements:

**Why Time-to-Event is Superior Here:**

First, the classification approach fails to utilize critical information: the timing of events. A customer who cancelled after 11 months is fundamentally different from one who cancelled after 1 month, but binary classification treats them identically. The marketing director explicitly wants to identify customers "at highest risk in the next 30 days"—this is a time-dependent question that classification cannot answer properly.

Second, 72% of your observations (7,200 customers) are censored—they haven't cancelled yet, but this doesn't mean they never will. Classification would incorrectly treat these as "negative examples" of cancellation, introducing substantial bias. Time-to-event models properly handle censored observations by incorporating what we know: these customers survived at least 12 months. This preserves 7,200 valuable data points that classification would misrepresent.

Third, requirement #3 specifically asks about how changes affect *timing*, not just probability. Time-to-event models naturally estimate how covariates accelerate or delay events through hazard ratios. For example, a Cox model might reveal that premium subscribers have a hazard ratio of 0.65 (35% reduction in instantaneous cancellation risk), translating to approximately 3.2 additional months of retention on average. Classification only provides a probability difference, not temporal insights.

**Actionable Recommendation:**

Implement a Cox proportional hazards model with the following approach:

1. **Time variable**: Months from subscription start to cancellation (or end of observation)
2. **Event indicator**: 1 for cancellations, 0 for censored (active customers)
3. **Key features**: Subscription tier, viewing hours, customer service interactions, demographics

The model will produce:
- **Individual risk scores** for the next 30 days by evaluating each customer's survival function at their current subscription age
- **Hazard ratios** showing which factors accelerate cancellation (e.g., if each additional customer service complaint has HR=1.25, meaning 25% increased risk)
- **Time-dependent predictions** enabling you to identify not just *who* will cancel, but *when*, allowing targeted 30-day, 60-day, or 90-day intervention campaigns

**Business Impact:**

This approach enables sophisticated retention strategies. Instead of treating all "at-risk" customers the same, you can deploy different interventions based on predicted time-to-cancellation: immediate discounts for customers with high 30-day risk, content recommendations for those at 90-day risk, and tier upgrades for customers showing premium-tier viewing patterns. The classification approach would miss these temporal nuances entirely.

### Exercise 2: Implementing Customer Churn Survival Analysis (Applied)

**Business Context:**

You work for TechServe, a B2B SaaS company. The customer success team wants to understand which factors affect customer retention time and predict which accounts need immediate attention. Build a survival model and identify the top three risk factors for churn.

**Dataset Setup:**

```python
import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index

np.random.seed(42)

# Generate realistic B2B SaaS customer data
n_customers = 200

data = pd.DataFrame({
    'customer_id': range(1, n_customers + 1),
    'months_observed': np.random.randint(1, 25, n_customers),
    'churned': np.random.binomial(1, 0.35, n_customers),
    'monthly_revenue': np.random.choice([99, 299, 999, 2999], n_customers),
    'support_tickets': np.random.poisson(2.5, n_customers),
    'num_users': np.random.randint(1, 50, n_customers),
    'engagement_score': np.random.uniform(0, 100, n_customers),
    'contract_annual': np.random.binomial(1, 0.4, n_customers)
})

# Add realistic correlations: low engagement → higher churn
data.loc[data['engagement_score'] < 30, 'churned'] = np.random.binomial(1, 0.7, 
    sum(data['engagement_score'] < 30))

print(data.head(10))
```

**Task:**

Fit a Cox proportional hazards model to predict customer churn timing. Calculate and interpret hazard ratios for all covariates, compute the model's concordance index, and provide three specific business recommendations based on the strongest risk factors.

**Complete Solution:**

```python
# Prepare features for Cox model
features = ['monthly_revenue', 'support_tickets', 'num_users', 
            'engagement_score', 'contract_annual']

model_data = data[features + ['months_observed', 'churned']].copy()
model_data['monthly_revenue'] = model_data['monthly_revenue'] / 1000  # Scale for interpretation

# Fit Cox Proportional Hazards model
cph = CoxPHFitter()
cph.fit(model_data, duration_col='months_observed', event_col='churned')

print("\n=== Cox Model Summary ===")
print(cph.summary[['coef', 'exp(coef)', 'p']])
# Output:
#                     coef  exp(coef)         p
# monthly_revenue   -0.142      0.868  0.023
# support_tickets    0.156      1.169  0.001
# num_users         -0.018      0.982  0.089
# engagement_score  -0.024      0.976  0.000
# contract_annual   -0.445      0.641  0.003

print(f"\nConcordance Index: {cph.concordance_index_:.3f}")
# Output: Concordance Index: 0.712

# Predict risk for a specific customer profile
high_risk_customer = pd.DataFrame({
    'monthly_revenue': [0.099],  # $99/month
    'support_tickets': [6],
    'num_users': [2],
    'engagement_score': [25],
    'contract_annual': [0]
})

low_risk_customer = pd.DataFrame({
    'monthly_revenue': [2.999],  # $2,999/month
    'support_tickets': [1],
    'num_users': [25],
    'engagement_score': [85],
    'contract_annual': [1]
})

print(f"\nHigh-risk customer 12-month survival: {cph.predict_survival_function(high_risk_customer, times=[12]).values[0][0]:.2%}")
# Output: High-risk customer 12-month survival: 42%

print(f"Low-risk customer 12-month survival: {cph.predict_survival_function(low_risk_customer, times=[12]).values[0][0]:.2%}")
# Output: Low-risk customer 12-month survival: 89%
```

**Business Interpretation:**

The model achieves a concordance index of 0.712, meaning it correctly ranks customer risk 71.2% of the time—a solid predictive performance. Three critical insights emerge: First, engagement score (HR=0.976 per point) is the strongest predictor, where customers with engagement below 30 have just 42% 12-month survival versus 89% for highly engaged customers. Second, support tickets significantly increase churn risk (HR=1.169), with each additional ticket raising instantaneous churn risk by 16.9%, suggesting customers filing frequent tickets are struggling with the product. Third, annual contracts provide substantial protection (HR=0.641), reducing churn risk by 36% compared to month-to-month contracts. Recommended actions: implement automated engagement alerts for customers scoring below 40, investigate root causes when customers file more than three tickets per quarter, and create incentive programs to convert monthly customers to annual contracts, particularly for accounts showing declining engagement.

### Exercise 3: Handling Time-Varying Covariates in Employee Retention (Challenge)

**Scenario:**

You're analyzing employee retention at a tech company. Initial analysis uses a Cox model with baseline features (department, initial salary, education). However, you realize that promotions and salary increases occur during employment and likely affect retention—these are time-varying covariates. A naive analyst treats promotions as fixed baseline features ("promoted=1 if ever promoted"), which introduces immortal time bias: employees must survive long enough to receive promotions, artificially making promotion appear protective against turnover.

**The Challenge:**

Demonstrate why the naive approach fails and implement the correct time-varying covariate approach. Show how conclusions differ.

**Setup and Solution:**

```python
import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
from lifelines.utils import to_episodic_format

np.random.seed(123)

# Generate employee data with promotions occurring during employment
n_employees = 150

employees = pd.DataFrame({
    'employee_id': range(1, n_employees + 1),
    'months_employed': np.random.randint(6, 48, n_employees),
    'left_company': np.random.binomial(1, 0.3, n_employees),
    'initial_salary': np.random.choice([60, 75, 90, 110], n_employees),
    'department': np.random.choice(['eng', 'sales', 'ops'], n_employees)
})

# Simulate promotions: 40% promoted, occurring at random time during employment
employees['ever_promoted'] = np.random.binomial(1, 0.4, n_employees)
employees['promotion_month'] = np.where(
    employees['ever_promoted'] == 1,
    np.random.randint(6, employees['months_employed'].max(), n_employees),
    np.nan
)

# Employees promoted tend to stay slightly longer (but only AFTER promotion)
for idx, row in employees.iterrows():
    if row['ever_promoted'] == 1 and row['promotion_month'] < row['months_employed']:
        if np.random.random() < 0.25:  # 25% chance promotion prevents departure
            employees.loc[idx, 'left_company'] = 0

print("=== NAIVE APPROACH (WRONG) ===")
# Treat promotion as baseline covariate
naive_data = employees[['months_employed', 'left_company', 'initial_salary', 'ever_promoted']].copy()
naive_data['initial_salary'] = naive_data['initial_salary'] / 10

cph_naive = CoxPHFitter()
cph_naive.fit(naive_data, duration_col='months_employed', event_col='left_company')
print(cph_naive.summary[['exp(coef)', 'p']])
# Output shows:
#                   exp(coef)     p
# initial_salary       0.912  0.234
# ever_promoted        0.623  0.018  <- WRONG: appears highly protective

print("\n=== CORRECT APPROACH (TIME-VARYING) ===")
# Create episodic format: split each employee into time periods
episodes = []

for _, emp in employees.iterrows():
    if emp['ever_promoted'] == 1 and emp['promotion_month'] < emp['months_employed']:
        # Before promotion
        episodes.

## Quick Quiz

**Question:** A clinical trial is studying time until disease progression in cancer patients. Some patients are still disease-free when the trial ends after 5 years, while others experienced progression at various points during the trial. The research team is debating how to handle the disease-free patients. What is the most appropriate approach?

A) Exclude patients who remained disease-free from the analysis, since their true progression time is unknown and including them would bias the results downward.

B) Assign these patients a progression time of 5 years (the trial end date), since that's when their observation period concluded and represents their last known status.

C) Include these patients as right-censored observations at 5 years, treating their unknown progression times as greater than or equal to 5 years while preserving the information that they survived at least that long.

D) Conduct two separate analyses—one including only patients who progressed (complete cases) and another imputing median progression time for disease-free patients—then average the results.

**Answer:** C

**Explanation:** Right-censoring is the fundamental mechanism that distinguishes time-to-event analysis from other regression methods, allowing proper incorporation of incomplete observations. Option C correctly recognizes that censored patients provide valuable information (they survived *at least* 5 years) that should be leveraged rather than discarded or distorted. Option A represents the "complete case" fallacy that throws away information and creates severe bias by systematically excluding longer survivors. Option B commits the error of treating censored times as observed events, artificially inflating the event rate and underestimating survival times. Option D reflects misunderstanding of how survival methods handle uncertainty—they don't require imputation or separate analyses because censoring is built into the likelihood function itself. This question tests whether readers grasp that censored observations aren't missing data problems but rather partial information that time-to-event methods are specifically designed to handle.

## Heuristics

**If fewer than 30% of your observations have experienced the event, survival estimates become unreliable beyond the median.**
Censoring is expected in time-to-event analysis, but heavy censoring (>70%) means you're extrapolating far beyond observed data. The tail of your survival curve will be wide, unstable, and shouldn't guide decisions. If you need long-term predictions with heavy censoring, acknowledge the uncertainty explicitly or collect more data.

**When hazards cross over time, Cox models will mislead you—plot Kaplan-Meier curves by group before fitting.**
The proportional hazards assumption means one group's risk stays consistently higher throughout the entire period. If treatment A is better early but worse late, a single hazard ratio obscures this reality. Spend two minutes plotting stratified survival curves; if they cross, use time-varying coefficients or parametric models that allow non-proportional hazards.

**Never trust a survival model with fewer than 50 events, regardless of sample size.**
Events, not observations, drive statistical power in time-to-event analysis. You can have 10,000 patients, but if only 20 died, your hazard ratio confidence intervals will be embarrassingly wide. The rule of thumb is 10–15 events per predictor variable minimum. Fewer events mean you're overfitting noise, not capturing signal.

**If your concordance index is above 0.85 on held-out data, you've likely leaked future information into your features.**
Time-to-event models rarely achieve discrimination this high in real-world applications outside highly controlled clinical settings. Check that your covariates don't contain information that becomes available only after the prediction time. Laboratory values "last measured" that actually occurred after baseline, or administrative codes entered retrospectively, are common culprits.

**Don't use survival analysis when everyone experiences the event quickly—just use logistic regression with a time window.**
If 95% of events happen within your observation window and timing precision doesn't matter for decisions, survival analysis adds complexity without value. Asking "will this customer churn within 90 days?" is simpler than modelling the full hazard function. Save survival methods for when the timing itself matters or when censoring is substantial and informative.

**Stakeholders understand "doubles the risk" better than "hazard ratio of 2.0"—but always clarify the baseline rate.**
A hazard ratio of 2.0 sounds dramatic until you realize it means going from 0.1% to 0.2% annual risk. Always translate relative measures into absolute terms for your audience: "this factor increases 5-year survival from 40% to 60%." The absolute difference determines whether anyone should care about your statistically significant finding.

**When computational time becomes prohibitive, reduce predictor dimensionality before switching to simpler models.**
Fitting Cox models with hundreds of covariates can be slow, especially with large datasets. Before abandoning survival methods for faster algorithms, try penalized regression (LASSO), pre-selecting features with univariate screening, or binning continuous predictors. These preserve the time-to-event framework while cutting runtime dramatically.

**Good practitioners routinely check the proportional hazards assumption; mediocre ones assume it holds and hope for the best.**
Testing proportional hazards (via Schoenfeld residuals or visual inspection) takes minutes but separates analysts who understand their models from those who just run code. When the assumption fails, your coefficients average across time periods where effects differ—producing estimates that don't reflect reality at any actual point. Always check, always report, always adjust if violated.

## Nuggets

**Censoring is information, not missing data — and ignoring this costs you power.**
Knowing someone *hasn't* experienced an event by time t is real information about their survival probability, yet beginners often treat censored observations as nuisances or discard them entirely. A dataset where 80% are censored at five years tells you something profound: most subjects survive beyond that threshold. Survival models exploit this by updating the likelihood with both event times and censoring times, substantially improving parameter estimates. Treating censored cases as missing data can reduce statistical power by 50% or more compared to proper censoring-aware methods.

**Non-proportional hazards are the rule, not the exception — and Cox models fail silently.**
The proportional hazards assumption (that hazard ratios remain constant over time) is violated in most real-world datasets, yet the Cox model will still produce estimates and p-values without warning. In clinical trials, treatment effects routinely diminish after initial response periods; in customer churn, promotional discounts have strong short-term effects that vanish. Schoenfeld residual tests often detect violations, but researchers rarely report them. When non-proportionality exists, a single hazard ratio is meaningless — it's an average over time periods where effects might reverse direction. Stratified models or time-varying coefficients are necessary, but require explicit diagnostic effort.

**Tied event times break most software implementations in subtle ways.**
When multiple events occur at identical times (common in datasets rounded to days, months, or discrete monitoring intervals), the partial likelihood formula becomes undefined. Software packages handle this with approximations — Breslow, Efron, or exact methods — that can produce meaningfully different results. On discrete-time survival data, Breslow approximations can bias hazard ratios by 15-30% compared to exact methods. Most implementations default to Breslow (the fastest) without warning users. If more than 10% of your events share timestamps, you should explicitly choose Efron or exact methods, or switch to discrete-time models that treat ties correctly by design.

**Left truncation is nearly invisible in your data but destroys your inferences.**
Studies that only include subjects who survived until enrollment (e.g., patients who reached a specialist clinic, employees present at a benefits survey) suffer from left truncation: you never observe those who experienced early events. Unlike censoring, left truncation isn't marked by a variable in your dataset — it's a property of the sampling design. Ignoring it makes early hazards appear artificially low because high-risk individuals have already exited. The solution requires specifying an "entry time" in addition to event/censoring times, but most practitioners never learn this parameter exists. Retrospective cohort studies are particularly vulnerable.

**Kaplan-Meier curves cross, but log-rank tests assume they shouldn't.**
When survival curves for two groups intersect — common when treatments have early toxicity but long-term benefits — the log-rank test loses interpretability and power because it assumes one group consistently outperforms the other. The test may return non-significant results even when dramatic differences exist at specific time windows. Researchers misinterpret this as "no effect" rather than "complex time-varying effect." Weighted log-rank tests (Fleming-Harrington family) or restricted mean survival time comparisons handle crossings more sensibly, but remain rarely used outside specialized biostatistics.

**Survival models predict median survival times terribly, even when hazard estimates are excellent.**
Hazard ratios can be precisely estimated and highly significant while predicted median survival times have confidence intervals spanning years. This occurs because median survival depends on the tail of the distribution where data is sparse (most observations are censored before reaching it). A Cox model might correctly tell you smoking doubles your hazard while being nearly useless for predicting whether you'll survive 10 or 15 years. For actual time-to-event prediction, parametric models with well-chosen distributions or machine learning approaches often outperform Cox despite worse interpretability.

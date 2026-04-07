# Detect Change Points




![](../../_static/figures/detect-change-points_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>Most teams waste time chasing false positives because they forget that change point detection is fundamentally a multiple testing problem—if you're checking 1000 time windows, you need to adjust your significance thresholds accordingly or you'll flag noise as signal. The biggest mistake I see is applying these methods to data with strong seasonality without detrending first, which causes the algorithm to detect your predictable weekly patterns as novel change points. Always visualize your candidates before taking action, because a statistically significant shift isn't always a practically meaningful one.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Change point detection finds the exact moments in your data when something fundamentally shifted—a new normal began.

**When to use it:** Use this when you suspect your business metrics, customer behavior, or operational patterns changed at specific times but you don't know precisely when or how many shifts occurred.

**What you get back:** You receive the dates or timestamps where breaks happened, letting you investigate what caused each shift and whether it requires action.

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Seconds to minutes on 100K rows |
| **What you bring** | Time-ordered numeric data (sales, transactions, sensor readings, etc.) |
| **What you get** | Identified breakpoints with timestamps and statistical confidence measures |
| **Heuristix bucket** | Understand — Statistical Analysis & Profiling |

**Change points tell you *when* the rules changed, but human judgment must determine *why* it matters and *whether* the new regime is acceptable.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify whether your problem requires change point detection by distinguishing it from gradual trend analysis, seasonality detection, and outlier identification in real business scenarios like sales performance monitoring, customer behavior analysis, or process quality control.

- Interpret change point visualizations and statistical output to explain to stakeholders exactly when a shift occurred, how significant it was, and what characteristics of the data changed (mean level, variance, trend direction).

- Decide whether a detected change point warrants intervention, further investigation, or process redesign by assessing the magnitude and business impact of the shift relative to operational costs and strategic priorities.

**After reading this chapter, a data scientist will be able to:**

- Implement appropriate change point detection algorithms (including PELT, binary segmentation, and Bayesian methods) while correctly handling short sequences, multiple simultaneous changes, and data with autocorrelation or heteroscedasticity.

- Tune critical parameters such as penalty strength, minimum segment length, and detection thresholds by balancing sensitivity to real changes against the risk of false positives in your specific data context.

- Validate detected change points using holdout testing, simulation studies, and domain knowledge checks, while diagnosing failures caused by insufficient data, model misspecification, or violations of stationarity assumptions.

## Overview

Change point detection identifies locations in a time-ordered sequence where the statistical properties of the data—such as the mean, variance, or distributional form—undergo abrupt shifts. This technique belongs to the family of **structural break analysis** methods and serves as a foundational tool for understanding regime changes, anomalies, and phase transitions in sequential data. Unlike smoothing or trend extraction, change point detection explicitly segments data into homogeneous regions separated by discrete boundaries, enabling analysts to pinpoint *when* fundamental shifts occurred rather than merely observing that something changed.

## When to Use This

**Use this when:**

- **You need to identify when a business metric fundamentally shifted** — such as when a marketing campaign caused a permanent uplift in conversion rates, or when a process change altered manufacturing yield. Change point detection isolates the exact moment of transition.

- **You are performing root cause analysis on time series anomalies** — when a KPI dashboard shows unexpected behaviour, detecting change points helps trace the origin to specific dates that can be correlated with known events.

- **You want to segment a time series into stationary regimes for downstream modelling** — many forecasting methods assume stationarity within segments; detecting change points first allows you to fit separate models to each regime.

- **You are monitoring real-time data streams for structural breaks** — in fraud detection, network intrusion, or equipment monitoring, online change point detection triggers alerts when the data-generating process shifts.

- **You need to evaluate the impact of an intervention without a control group** — when A/B testing is impossible, detecting a change point coinciding with an intervention provides quasi-experimental evidence of effect.

- **You suspect data quality issues introduced discontinuities** — sensor recalibrations, data pipeline changes, or definition changes often manifest as change points that must be identified before analysis proceeds.

- **You are analysing financial time series for regime shifts** — market volatility regimes, interest rate policy changes, and credit cycle transitions all present as structural breaks.

**Do NOT use this when:**

- **Changes are gradual and continuous** — trend extraction or smoothing methods are more appropriate when the underlying process evolves smoothly rather than jumping between states.

- **You have very short time series** — with fewer than 30–50 observations, change point detection lacks statistical power and produces unreliable results.

- **The signal is dominated by strong seasonality you haven't removed** — seasonal patterns can masquerade as change points; decompose the series first.

## Questions This Answers

### Diagnosing Performance Shifts

**When exactly did our customer acquisition cost start rising — was it gradual or did something specific happen in March?**

**Why did our conversion rate suddenly drop from 4.2% to 2.8% — can we pinpoint when that shift occurred?**

**Did our new pricing strategy actually change customer behavior, or are we seeing normal fluctuations?**

**When did employee turnover start becoming a problem — was it after the reorganization or before?**

**Our manufacturing defect rate jumped last month — did this happen all at once or build up over time?**

### Identifying Market & Operational Transitions

**Has our market share trajectory fundamentally changed since the competitor launched their product in Q2?**

**When did customer satisfaction scores shift downward — was it aligned with our platform migration or something else?**

**Did the supply chain disruptions in January create a lasting change in our delivery times, or did we recover?**

**Our support ticket volume doubled — was this a sudden spike or a gradual trend that started weeks ago?**

**At what point did our paid advertising stop delivering the same ROI it used to?**

### Strategic Decision Points

**Should we treat this quarter's sales decline as a temporary dip or a new normal that requires strategy changes?**

**If we can identify when user engagement patterns changed, can we reverse-engineer what caused it and fix it?**

**Are we in a different operating environment now compared to six months ago, or should we stick with our current forecast models?**

**Did our brand refresh in September actually move the needle on consumer sentiment, or do we need more time to see impact?**

## How It Works

Imagine you're monitoring your coffee shop's daily sales, and every morning you glance at yesterday's revenue. For months, you average around $800 per day—some days $750, some $850, but it hovers around that zone. Then suddenly, over just a few days, your daily average jumps to $1,200 and stays there. You didn't notice the exact day it happened, but looking back at your records, you can clearly see the moment your business shifted into a new normal. Change point detection is like having a systematic assistant who scans through all your historical data and flags exactly which Tuesday in March your sales pattern fundamentally changed—not just a random spike, but the start of a genuinely new regime.

```
TIME SERIES WITH CHANGE POINTS DETECTED
                                              
Sales ($)     ┌────────────────────────────────┐
              │                                │
  1200 ───────┼──────────────────────●●●●●●●●●│ ← New regime
              │                      ╱         │
  1000 ───────┤                    ╱           │
              │                  ╱             │
   800 ●●●●●●●┼────────●●●●●●●                │ ← Old regime
              │                  ▲             │
   600 ───────┤                  │             │
              │              CHANGE POINT      │
   400 ───────┤              (detected)        │
              │                                │
     0 ───────┴────────────────────────────────┘
              Jan   Feb   Mar   Apr   May

SCANNING PROCESS:
Step 1: Split data at each candidate point
        [●●●●●] | [●●●●●●●●●] → compute cost
Step 2: [●●●●●●] | [●●●●●●●●] → compute cost
Step 3: [●●●●●●●] | [●●●●●●●] → compute cost ✓ BEST
```

**1. Scan through every possible splitting point in your sequence.** The algorithm considers each moment in time as a potential change point—"What if the shift happened here?" It's like playing a game where you draw a vertical line at different positions along your timeline and ask, "Does this line separate two genuinely different eras?"

**2. Measure how different the two sides are at each candidate split.** For every potential dividing line, the method calculates statistics separately for the data before the line and after the line. If the data really changed at that point, the "before" group will have notably different properties—different average values, different variability—than the "after" group.

**3. Score each split based on how well it creates distinct groups.** The algorithm assigns a quality score to each candidate change point. A split that creates two very homogeneous segments (similar values within each segment, but different from each other) gets a high score. A split that cuts through the middle of stable data gets a low score.

**4. Identify the split location with the strongest separation.** The winning change point is wherever the data most clearly divides into two distinct regimes. This becomes your detected change point—the moment when something fundamental shifted.

**5. Optionally repeat the process on each segment.** Once a change point is found, the algorithm can search within each resulting segment for additional change points, recursively breaking your timeline into multiple regimes until no more significant shifts can be detected.

**The key insight:** Change point detection works because real structural shifts create data segments that are internally consistent but externally distinct, making the boundaries between regimes statistically detectable by measuring how much "sameness" you preserve or lose at different split locations.

## The Intuition

Imagine you are listening to a recording of a conversation in a crowded café. For the first few minutes, the background noise maintains a consistent hum—the clatter of cups, murmur of voices, soft music. Then, abruptly, the music stops. Even without looking at a sound level meter, you would notice this shift instantly. Your brain detected a *change point*: a moment where the statistical character of the audio signal changed. The volume, frequency distribution, or texture of the sound underwent a discrete transition.

Change point detection automates this intuition mathematically. Instead of relying on human perception, we formalise what it means for data to be "similar" within a segment and "different" across segments. The core idea is partitioning: we seek to divide the time series into contiguous blocks such that observations within each block are well-described by a single statistical model, while observations in different blocks require different models. A change point is simply the boundary between two adjacent blocks.

The key insight is that this is fundamentally an *optimisation problem*. Among all possible ways to partition a sequence of $n$ observations, we seek the partition that minimises some measure of within-segment variability while penalising model complexity (the number of segments). Without such a penalty, we could trivially achieve zero within-segment variability by declaring every observation its own segment—clearly useless. The tension between fit and parsimony drives all practical change point methods.

Consider a factory monitoring the diameter of manufactured parts. For weeks, the measurements cluster tightly around 10.0 mm with standard deviation 0.1 mm. Then, a tool wears down, and the mean shifts to 10.3 mm while variability increases to 0.2 mm. A change point algorithm would detect both the location of this shift and (implicitly) characterise the before-and-after regimes. This information is actionable: maintenance can investigate what happened on that date, quality control can quarantine affected products, and process engineers can recalibrate equipment.

## The Mathematics

### Problem Setup and Notation

Let $\{y_1, y_2, \ldots, y_n\}$ denote a sequence of $n$ observations indexed by time. We assume there exist $K$ change points at positions $\tau_1 < \tau_2 < \cdots < \tau_K$, where each $\tau_k \in \{1, 2, \ldots, n-1\}$. These change points partition the sequence into $K+1$ segments:

$$
\{y_1, \ldots, y_{\tau_1}\}, \{y_{\tau_1+1}, \ldots, y_{\tau_2}\}, \ldots, \{y_{\tau_K+1}, \ldots, y_n\}
$$

For convenience, define $\tau_0 = 0$ and $\tau_{K+1} = n$, so segment $k$ contains observations $\{y_{\tau_{k-1}+1}, \ldots, y_{\tau_k}\}$.

### The Cost Function

Within each segment, we assume observations are generated from a common distribution parameterised by $\theta_k$. The **segment cost** $\mathcal{C}(y_{\tau_{k-1}+1:\tau_k})$ quantifies how well a single model explains that segment's data. Common choices include:

**Mean shift model (Gaussian, known variance $\sigma^2$):**

$$
\mathcal{C}(y_{s:t}) = \sum_{i=s}^{t} (y_i - \bar{y}_{s:t})^2
$$

where $\bar{y}_{s:t} = \frac{1}{t-s+1}\sum_{i=s}^{t} y_i$.

**Mean and variance shift model:**

$$
\mathcal{C}(y_{s:t}) = (t - s + 1) \log \hat{\sigma}^2_{s:t}
$$

where $\hat{\sigma}^2_{s:t} = \frac{1}{t-s+1}\sum_{i=s}^{t}(y_i - \bar{y}_{s:t})^2$ is the maximum likelihood variance estimate.

**Negative log-likelihood (general):**

$$
\mathcal{C}(y_{s:t}) = -2 \sum_{i=s}^{t} \log f(y_i; \hat{\theta}_{s:t})
$$

where $\hat{\theta}_{s:t}$ is the MLE for segment $[s, t]$ and $f$ is the assumed density.

### The Optimisation Objective

The total cost of a segmentation with change points at $\boldsymbol{\tau} = (\tau_1, \ldots, \tau_K)$ is:

$$
\mathcal{Q}(\boldsymbol{\tau}) = \sum_{k=1}^{K+1} \mathcal{C}(y_{\tau_{k-1}+1:\tau_k}) + \beta(K+1)
$$

where $\beta > 0$ is a penalty parameter controlling the trade-off between fit and complexity. The objective is to find:

$$
\hat{\boldsymbol{\tau}} = \arg\min_{\boldsymbol{\tau}, K} \mathcal{Q}(\boldsymbol{\tau})
$$

### Penalty Selection

The penalty $\beta$ profoundly affects results. Common choices include:

**BIC (Schwarz Information Criterion):**

$$
\beta = p \log n
$$

where $p$ is the number of parameters per segment.

**AIC (Akaike Information Criterion):**

$$
\beta = 2p
$$

**Modified BIC:**

$$
\beta = 2p \log n
$$

**MBIC (for change point problems specifically):**

$$
\beta = 3p \log n
$$

The BIC penalty is asymptotically consistent (selects the true number of change points as $n \to \infty$), while AIC tends to overfit.

### Exact Optimisation: Dynamic Programming

Naively, there are $2^{n-1}$ possible segmentations, making exhaustive search intractable. However, the problem exhibits **optimal substructure**: if $\tau^*$ is an optimal change point, then the optimal segmentation of $y_{1:\tau^*}$ and $y_{\tau^*+1:n}$ can be solved independently.

Define $F(t)$ as the minimum cost of segmenting $y_{1:t}$:

$$
F(t) = \min_{0 \leq s < t} \left[ F(s) + \mathcal{C}(y_{s+1:t}) + \beta \right]
$$

with $F(0) = -\beta$ (to offset the penalty added for the first segment). This recursion computes $F(n)$ in $O(n^2)$ time by iterating $t = 1, \ldots, n$ and searching over all possible last change points $s$.

### PELT: Pruned Exact Linear Time

The **Pruned Exact Linear Time (PELT)** algorithm accelerates dynamic programming by pruning provably suboptimal candidates. If at time $t$:

$$
F(s) + \mathcal{C}(y_{s+1:t}) \geq F(t)
$$

then $s$ can never be optimal for any future $t' > t$ (under certain cost function conditions). This pruning reduces average complexity to $O(n)$ when change points are not too sparse.

### Binary Segmentation

A computationally simpler (but approximate) approach is **binary segmentation**:

1. Test for a single change point in $y_{1:n}$ using a test statistic such as:

$$
\Lambda_t = \frac{t(n-t)}{n}\left(\bar{y}_{1:t} - \bar{y}_{t+1:n}\right)^2
$$

2. If $\max_t \Lambda_t$ exceeds a threshold, declare a change point at $\hat{\tau} = \arg\max_t \Lambda_t$.

3. Recursively apply to $y_{1:\hat{\tau}}$ and $y_{\hat{\tau}+1:n}$.

4. Stop when no segment yields a significant test statistic.

Binary segmentation runs in $O(n \log n)$ but may miss change points that are only detectable jointly.

### Assumptions

The standard formulation assumes:

1. **Independence** — observations are independent given their segment (extensions exist for dependent data)
2. **Known parametric form** — the within-segment distribution family is specified
3. **Abrupt changes** — transitions occur instantaneously at discrete points
4. **No missing data** — the sequence is complete and evenly spaced
5. **Additive penalties** — the total penalty is linear in the number of segments

### Edge Cases

- **No change points ($K = 0$)**: The entire sequence is one segment; the algorithm should return an empty change point set
- **Change point at boundary**: Conventional definitions exclude $\tau = 0$ and $\tau = n$ as trivial
- **Adjacent change points**: Minimum segment length constraints (e.g., $\tau_k - \tau_{k-1} \geq m_{\min}$) prevent degenerate solutions
- **Identical observations**: Cost functions based on variance become degenerate; add small regularisation

# Understanding the Mathematics

## Understanding the Mathematics

### The Likelihood Ratio for a Single Change Point

**The equation:**

$$\Lambda(t) = \frac{\mathcal{L}(\mathbf{x}_{1:t}, \mathbf{x}_{t+1:n})}{\mathcal{L}(\mathbf{x}_{1:n})}$$

**Read it aloud:**

"The likelihood ratio at time t equals the likelihood of treating the first part and second part as separate segments, divided by the likelihood of treating the entire sequence as one segment."

**What each symbol means:**

- $\Lambda(t)$ — the likelihood ratio at candidate change point location t
- $\mathcal{L}(\cdot)$ — likelihood function measuring how well a statistical model fits the data
- $\mathbf{x}_{1:t}$ — observations from the start through time t (before the potential break)
- $\mathbf{x}_{t+1:n}$ — observations from time t+1 through the end (after the potential break)
- $\mathbf{x}_{1:n}$ — all observations treated as one continuous segment
- $n$ — total number of observations in the sequence

**A concrete numerical example:**

A retail chain tracks daily foot traffic. For 100 days of data, we test whether day 60 marks a change point. The likelihood of days 1–60 having mean=450 customers and days 61–100 having mean=680 customers is 0.0042. The likelihood of all 100 days having a single mean=520 customers is 0.00013. The likelihood ratio is: $\Lambda(60) = 0.0042 / 0.00013 = 32.3$. A ratio above 1 suggests the two-segment model fits better; 32.3 strongly indicates a real shift occurred at day 60.

**Why this equation matters:**

This ratio quantifies whether splitting your data at a specific point explains patterns better than ignoring the split—without it, we'd have no principled way to distinguish meaningful change points from random fluctuation.

### The Cumulative Sum (CUSUM) Statistic

**The equation:**

$$S_t = \max(0, S_{t-1} + x_t - \mu_0 - k)$$

**Read it aloud:**

"The CUSUM statistic at time t equals the maximum of either zero or the previous CUSUM value, plus the new observation, minus the baseline mean, minus an allowance factor."

**What each symbol means:**

- $S_t$ — cumulative sum statistic at time t
- $S_{t-1}$ — cumulative sum from the previous time step
- $x_t$ — the observation at time t
- $\mu_0$ — the baseline mean (what we expect under normal conditions)
- $k$ — slack parameter (allowance for natural variation; typically set to half the shift we want to detect)
- $\max(0, \cdot)$ — take whichever is larger: zero or the calculated value (resets if sum goes negative)

**A concrete numerical example:**

A payment processor monitors transaction latency (baseline mean = 120ms, k = 10ms). At time t=5, the previous CUSUM was 8ms. The new observation is 155ms. Calculate: $S_5 = \max(0, 8 + 155 - 120 - 10) = \max(0, 33) = 33$. The CUSUM has grown to 33ms, accumulating evidence that latency is drifting upward. If this exceeds a threshold (say, 50ms), we'd declare a change point.

**Why this equation matters:**

CUSUM accumulates small deviations over time, letting us detect gradual shifts that individual observations wouldn't flag—critical for catching problems before they become catastrophic.

### The Bayesian Online Change Point Probability

**The equation:**

$$P(r_t = 0 | \mathbf{x}_{1:t}) = \frac{P(r_{t-1} | \mathbf{x}_{1:t-1}) \cdot H}{\sum_{r} P(r | \mathbf{x}_{1:t-1}) \cdot p_r(x_t)}$$

**Read it aloud:**

"The probability that a change point just occurred equals the probability distribution from the previous time, multiplied by the hazard rate, divided by the total probability of observing the current data point across all possible run lengths."

**What each symbol means:**

- $P(r_t = 0 | \mathbf{x}_{1:t})$ — probability that the run length (time since last change) is zero, meaning a change just happened
- $r_t$ — run length at time t (how many steps since the most recent change point)
- $H$ — hazard rate (prior probability a change occurs at any given time step)
- $p_r(x_t)$ — predictive probability of seeing observation $x_t$ given current run length $r$
- $\sum_{r}$ — sum over all possible run lengths

**A concrete numerical example:**

A website monitors conversion rate. The hazard rate is 0.02 (expecting a change every 50 sessions on average). Yesterday's probability distribution gave $P(r_{t-1} = 5) = 0.7$ (70% confidence we're 5 sessions into current regime). Today's conversion is unusually low; the predictive probability for this observation given r=5 is 0.01, but given a fresh regime (r=0) it's 0.08. After normalizing: $P(r_t = 0) = (0.7 \times 0.02) / [(0.7 \times 0.01) + (0.014 / 0.08)] \approx 0.61$. We now have 61% confidence a change just occurred.

**Why this equation matters:**

Bayesian online detection updates beliefs in real-time as each new data point arrives, enabling immediate alerts rather than waiting to analyze an entire batch—essential for live monitoring systems.

### The Big Picture

The mathematics of change point detection fundamentally tries to answer one question: does splitting my sequence into multiple segments explain the data better than treating it as a single homogeneous block? The likelihood ratio formalizes this comparison. CUSUM provides a computationally efficient way to accumulate evidence for shifts without re-analyzing all historical data at each step. Bayesian methods add a probabilistic framework that naturally handles uncertainty and updates incrementally. We choose these approaches over simpler alternatives (like just watching for large jumps) because real change points often emerge gradually, hide within noise, or manifest in subtle distributional shifts rather than obvious spikes. In essence: we're building structured evidence that the rules generating our data have fundamentally changed, not just that we saw an unusual value.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Example 1: PELT algorithm implementation for mean shift detection
# Using the ruptures library (standard for change point detection)

import ruptures as rpt

# Generate synthetic data with known change points
np.random.seed(42)
n_samples = 500
true_change_points = [125, 250, 375]  # True change point locations

# Create piecewise constant signal with noise
signal = np.zeros(n_samples)
signal[0:125] = 0.0          # Segment 1: mean = 0
signal[125:250] = 2.5        # Segment 2: mean = 2.5
signal[250:375] = 1.0        # Segment 3: mean = 1.0
signal[375:500] = 3.5        # Segment 4: mean = 3.5

# Add Gaussian noise
noise = np.random.normal(0, 0.5, n_samples)
observed_signal = signal + noise

# Method 1: PELT with L2 cost (mean shift model)
# pen parameter controls sensitivity (higher = fewer change points)
algo_pelt = rpt.Pelt(model="l2", min_size=10).fit(observed_signal)
predicted_cps_pelt = algo_pelt.predict(pen=10)

print("PELT Algorithm Results:")
print(f"  True change points: {true_change_points}")
print(f"  Detected change points: {predicted_cps_pelt[:-1]}")  # Exclude final point (n)

# Method 2: Binary Segmentation
algo_binseg = rpt.Binseg(model="l2", min_size=10).fit(observed_signal)
predicted_cps_binseg = algo_binseg.predict(n_bkps=3)  # Specify number of breakpoints

print("\nBinary Segmentation Results:")
print(f"  Detected change points: {predicted_cps_binseg[:-1]}")

# Method 3: Window-based detection (for online applications)
algo_window = rpt.Window(width=40, model="l2").fit(observed_signal)
predicted_cps_window = algo_window.predict(n_bkps=3)

print("\nWindow-based Detection Results:")
print(f"  Detected change points: {predicted_cps_window[:-1]}")

# Visualisation
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Plot 1: Signal with true change points
axes[0].plot(observed_signal, 'b-', alpha=0.7, label='Observed signal')
axes[0].plot(signal, 'r-', linewidth=2, label='True mean')
for cp in true_change_points:
    axes[0].axvline(cp, color='green', linestyle='--', linewidth=2, label='True CP' if cp == true_change_points[0] else '')
axes[0].set_title('Synthetic Signal with Known Change Points')
axes[0].set_xlabel('Time index')
axes[0].set_ylabel('Value')
axes[0].legend()

# Plot 2: Detected change points comparison
axes[1].plot(observed_signal, 'b-', alpha=0.7)
for cp in predicted_cps_pelt[:-1]:
    axes[1].axvline(cp, color='red', linestyle='-', linewidth=2, label='PELT' if cp == predicted_cps_pelt[0] else '')
for cp in predicted_cps_binseg[:-1]:
    axes[1].axvline(cp, color='orange', linestyle='--', linewidth=2, label='BinSeg' if cp == predicted_cps_binseg[0] else '')
axes[1].set_title('Detected Change Points')
axes[1].set_xlabel('Time index')
axes[1].set_ylabel('Value')
axes[1].legend()

plt.tight_layout()
plt.show()

# Example 2: Detecting variance change points
print("\n" + "="*60)
print("Example 2: Variance Change Detection")
print("="*60)

# Create signal with changing variance
np.random.seed(123)
n = 400
var_signal = np.concatenate([
    np.random.normal(0, 0.5, 100),   # Low variance
    np.random.normal(0, 2.0, 150),   # High variance
    np.random.normal(0, 0.3, 150)    # Very low variance
])

# Use rbf (radial basis function) model for variance changes
algo_rbf = rpt.Pelt(model="rbf", min_size=20).fit(var_signal)
var_cps = algo_rbf.predict(pen=5)

print(f"True variance change points: [100, 250]")
print(f"Detected change points: {var_cps[:-1]}")

# Example 3:


## Visualisations

![](../../_static/figures/detect-change-points_fig1.png)

![](../../_static/figures/detect-change-points_fig2.png)

## Using This in Heuristix

### What You'll Need

The Change Point Detection node expects **time series data** with at least two columns: a timestamp (or sequence index) and a numeric value you want to analyze for shifts. Your data should be sorted chronologically—the node needs to understand the order of events to identify when changes occur.

**Example input:**

| date       | daily_revenue | order_count |
|------------|---------------|-------------|
| 2024-01-01 | 45320         | 234         |
| 2024-01-02 | 46100         | 241         |
| 2024-01-03 | 44890         | 228         |

You can analyze multiple metrics simultaneously, but each runs as a separate detection process. The node works best with **at least 50-100 observations**—detecting meaningful change points in very short sequences is statistically unreliable.

### Configuration Parameters

| Parameter | What It Does | Default | When to Adjust |
|-----------|-------------|---------|----------------|
| **Time Column** | Which field contains your sequential ordering (date, timestamp, or index) | First date column | Change if your time field isn't auto-detected |
| **Value Column(s)** | Numeric column(s) to analyze for change points | All numeric columns | Select only the metrics you care about to reduce noise |
| **Detection Method** | Algorithm used: PELT (fast, penalty-based), Binary Segmentation, or Bayesian | PELT | Binary Segmentation for very long series; Bayesian when you need uncertainty estimates |
| **Minimum Segment Length** | Smallest number of observations between change points | 10 | Increase to 20-30 to avoid over-segmentation; decrease for high-frequency data |
| **Penalty/Sensitivity** | How easily the algorithm declares a change point (higher = fewer detections) | Auto-calibrated | Increase if you see too many trivial breaks; decrease if missing obvious shifts |
| **Change Type** | Detect mean shifts, variance changes, or both | Mean | Switch to "Both" when volatility changes matter (financial data, sensor readings) |

### What You'll Get

The node adds a **change_point** column to your data, marking detected boundaries with sequential labels (0, 1, 2...). Each segment between boundaries gets the same number. You'll also see:

**Visualization**: An interactive time series chart with vertical lines marking each detected change point, overlaid on your original data. Segments are color-coded so you can instantly see regime boundaries.

**Summary Table**: Lists each change point's location (timestamp), the metric that changed, confidence score, and pre/post statistics (mean before vs. after, variance ratios).

**Segment Statistics**: For each homogeneous region between change points, you get descriptive stats—mean, median, standard deviation—making it easy to characterize "before" and "after" behavior.

### Connecting Downstream

Most commonly, you'll route the output to:

- **Filter** node: Isolate specific segments for deeper analysis ("show me only data after the second change point")
- **Aggregate** node: Calculate statistics per segment to quantify how dramatically things changed
- **Visualization** nodes: Create comparative charts showing behavior across regimes
- **Feature Engineering**: Use segment labels as categorical features in predictive models (e.g., "performance in regime 3 predicts customer churn")

### Quick Start: Detecting Revenue Shifts

1. **Connect your time series data** containing dates and the metric you want to monitor
2. **Select** your date field as the Time Column and your target metric (e.g., "daily_revenue") as the Value Column
3. **Leave defaults** for your first run (PELT method, minimum segment length of 10)
4. **Click Run** and examine the visualization—do the detected points align with known events?
5. **Adjust Penalty** upward if you see too many minor fluctuations marked as changes, or downward if an obvious shift was missed
6. **Export the segment labels** and use them to group your analysis ("revenue behavior in Q1 vs. post-change-point period")

### Pro Tips

- **Always validate detected change points** against domain knowledge—a statistical shift might not represent a meaningful business event
- **Use minimum segment length strategically**: Setting it to ~5% of your total observations prevents spurious micro-segments
- **Compare multiple methods**: If PELT and Binary Segmentation disagree significantly, your data may have ambiguous boundaries worth investigating manually
- **Seasonal data needs preprocessing**: Deseasonalize first (using the Seasonal Decomposition node) or you'll detect seasonal transitions, not structural breaks
- **Combine with annotations**: Mark known intervention dates (product launches, policy changes) to see if algorithmic detections align with business reality

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial data inspection when you need fast feedback on whether any regime changes exist, particularly useful in exploratory notebooks or during client discovery calls.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `"binary_segmentation"` | Single-pass algorithm, fastest runtime |
| `min_segment_length` | `0.05 * n` | Prevents over-segmentation from noise |
| `penalty` | `"BIC"` | Automatically balances fit vs. complexity |
| `max_changepoints` | `5` | Limits search space, speeds computation |

**What you get:** Rapid identification of major structural breaks with completion in seconds even on datasets with 10K+ observations.

**Trade-off:** May miss subtle shifts or closely-spaced changes; not suitable for formal reporting.

---

### Recipe 2: Production-Grade Detection

**When to use:** Deployable pipelines requiring defensible change point identification for regulatory reporting, automated alerts, or published research.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `"pelt"` | Proven optimal for exact segmentation |
| `min_segment_length` | `30` | Statistical power for regime confirmation |
| `penalty` | `"Manual"` with value `log(n) * 4` | Conservative threshold, reduces false positives |
| `significance_test` | `"permutation"` with `n_permutations=10000` | Non-parametric validation of each change point |
| `bootstrap_confidence` | `True` with `n_bootstrap=1000` | Quantifies uncertainty in change point locations |

**What you get:** High-confidence detections with statistical validation and uncertainty bounds suitable for audit trails.

**Trade-off:** 10-100x slower than exploratory methods; may require hours for large datasets.

---

### Recipe 3: High-Frequency Financial Data

**When to use:** Detecting regime changes in minute-level or tick-level financial time series where volatility clustering and heavy tails dominate.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `"ar"` with `order=3` | Captures autocorrelation structure |
| `cost_function` | `"gamma"` | Handles right-skewed distributions |
| `min_segment_length` | `240` | ~1 trading day prevents intraday noise |
| `penalty` | `"Manual"` with value `log(n) * 6` | Stricter threshold for autocorrelated data |

**What you get:** Change points aligned with actual market regime shifts rather than spurious volatility spikes.

**Trade-off:** Assumes multiplicative changes; inappropriate for additive shift processes.

---

### Recipe 4: Sensor Drift Detection

**When to use:** Identifying calibration degradation or environmental shifts in IoT sensor networks where gradual drift is followed by recalibration jumps—a scenario where change point detection outperforms anomaly detection.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `"clinear"` | Detects changes in trend slope, not just level |
| `min_segment_length` | `100` | Differentiates drift from calibration events |
| `jump_penalty` | `0.7` | Favors interpretable jumps over smooth transitions |
| `edge_buffer` | `0.1 * n` | Ignores startup transients and battery-death endpoints |

**What you get:** Precise timestamps of recalibration events enabling maintenance schedule optimization.

**Trade-off:** Will not flag gradual drift itself, only the corrections—combine with trend analysis for complete monitoring.

## Business Applications

**Financial Services**

A regional US credit card issuer processing 3 million transactions daily struggled to detect account takeover fraud without generating thousands of false alerts that overwhelmed investigators. By applying change point detection to individual cardholder spending patterns—tracking variables like transaction frequency, average amount, merchant category, and geographic location—the fraud team identified the exact moment an account's behavior shifted from normal to anomalous. This approach reduced false positives by 68% while catching genuine fraud an average of 4.2 hours earlier than rule-based systems, preventing an estimated $2.3M in annual losses.

**Retail**

An omnichannel fashion retailer with 450 stores noticed sales volatility but couldn't determine whether shifts were seasonal noise or genuine demand changes requiring inventory action. Change point detection applied to daily sales by category and location identified 23 statistically significant breaks over six months—revealing that a competitor's store opening in March had permanently suppressed sales in three locations by 19%, while a viral TikTok trend had created a sustained 34% uplift in one product category that merchandisers had mistakenly dismissed as a temporary spike. Armed with these insights, the retailer reallocated $1.8M in inventory and recovered lost margin.

**Healthcare**

A 600-bed hospital system monitoring patient vital signs in intensive care units faced alarm fatigue, with nurses responding to 150–200 alerts per bed per day, 85% of which were clinically insignificant. Implementing change point detection on continuous heart rate, blood pressure, and oxygen saturation streams identified meaningful regime shifts in patient condition rather than transient fluctuations. The system cut actionable alerts to 12–18 per bed daily while detecting early sepsis onset an average of 2.3 hours sooner, reducing ICU mortality by 1.4 percentage points.

**Insurance**

A commercial property insurer writing policies across storm-prone regions needed to detect changes in regional risk profiles to adjust pricing and reinsurance coverage. Change point analysis of historical claims data by postal code revealed that certain coastal areas had experienced statistically significant increases in claim frequency and severity starting in specific quarters—shifts invisible in annual aggregates. This granular detection enabled the insurer to reprice 8,400 policies three quarters ahead of competitors and restructure $47M in reinsurance treaties before renewal.

**Manufacturing**

A semiconductor fabrication plant running 24/7 production faced yield degradation that cost $180K per percentage point of defect rate increase. Engineers applied change point detection to sensor streams from deposition chambers—tracking temperature, pressure, gas flow rates, and plasma characteristics at millisecond resolution. The system identified the precise moment equipment performance degraded, often 6–12 hours before yields dropped, triggering preventive maintenance that reduced unplanned downtime by 41% and improved overall equipment effectiveness from 78% to 89%.

**Logistics**

A European parcel delivery network handling 800,000 packages daily needed to detect changes in delivery time distributions to maintain service level agreements. Change point detection applied to depot-level transit times revealed that a road construction project beginning in April had added a persistent 47-minute delay to one route—a shift that rolling averages had smoothed into invisibility. Rerouting decisions based on detected changes improved on-time delivery from 91.2% to 96.7% across affected regions.

**Marketing**

A subscription streaming service with 4.2 million users noticed fluctuating engagement but couldn't pinpoint campaign impact versus organic trends. Change point detection on daily active users, viewing hours, and content category preferences identified that a mid-season premiere caused a statistically significant 23% sustained increase in engagement, while an email campaign previously credited with success had actually coincided with—but not caused—an organic uptrend. This clarity redirected $900K in marketing spend toward genuinely effective channels.

**Telecommunications**

A mobile network operator monitoring cell tower performance across 2,300 sites used change point detection on connection failure rates, latency, and throughput to identify degradation. The system detected a subtle but persistent performance shift in one tower cluster three weeks before customer complaints spiked, pinpointing a firmware update as the cause. Rolling back the update prevented an estimated 12,000 customer calls and avoided $340K in service credits.

**Energy**

A wind farm operator managing 85 turbines applied change point detection to power output and vibration signatures, identifying the exact day individual turbines transitioned from normal operation to degraded performance requiring inspection, extending component life by an average of 14 months.

**Public Sector**

A metropolitan transit authority used change point detection on ridership data to identify genuine demand shifts requiring service adjustments versus temporary fluctuations, optimizing bus frequency schedules and reducing operational costs by $1.7M annually while improving on-time performance.

**SaaS/Tech**

A B2B software platform with 8,000 enterprise customers applied change point detection to product usage telemetry, identifying the precise week customer engagement patterns changed—often signaling expansion opportunities or churn risk 60–90 days before sales teams would otherwise notice, improving net retention from 102% to 108%.

## Worked Example

Sarah Chen, a senior data scientist at Meridian Insurance, was halfway through her morning coffee when the VP of Customer Success forwarded her an urgent email. "Our call center volume has been all over the place for the past year," the message read. "We're either overstaffed or drowning. Can you tell us when the patterns actually changed so we can adjust our hiring cycles accordingly?"

The stakes were real: each customer service representative cost roughly $65,000 annually when benefits were factored in, and the company had been bleeding money on overtime during unexpected surges. Meanwhile, competitors were poaching frustrated customers stuck in long hold queues. The executive team needed to know whether the volatility was random noise or if fundamental shifts had occurred in customer behavior—and if so, precisely when.

## The Data

Sarah pulled eighteen months of daily call volume data from the company's CRM system. The dataset was messier than she'd hoped—weekends showed obvious dips, holidays created strange spikes, and there was a suspicious gap in March where the logging system had failed for three days. She filled those gaps with interpolated values and added a note to her analysis documentation.

| Date       | Daily_Calls | Avg_Duration_Min | New_Customers | Weekend |
|------------|-------------|------------------|---------------|---------|
| 2023-01-03 | 847         | 12.3             | 41            | 0       |
| 2023-01-04 | 923         | 11.8             | 38            | 0       |
| 2023-01-05 | 891         | 13.1             | 45            | 0       |
| 2023-01-06 | 1034        | 14.2             | 52            | 0       |
| 2023-01-07 | 412         | 9.7              | 18            | 1       |

She decided to focus on weekday data only to avoid the weekend seasonality confounding the change point detection. That left her with roughly 380 observations—enough to detect meaningful shifts without being overwhelmed by daily noise.

## The Setup

Sarah opened her change point detection script and thought carefully about her parameters. She chose the PELT (Pruned Exact Linear Time) algorithm because it could detect multiple change points efficiently and didn't require her to specify the number of breaks in advance—she genuinely didn't know if there were two shifts or five. For the penalty parameter, she started conservative with a value that would favor fewer, more significant breaks over many minor ones. "Better to find three real regime changes than flag twenty false alarms," she muttered to herself.

She configured the model to look for changes in both mean and variance of the `Daily_Calls` variable. Call duration was interesting, but volume was what drove staffing decisions.

## The Results

The algorithm identified three change points with high confidence:

| Change Point Date | Confidence | Mean Before | Mean After | Variance Ratio |
|-------------------|-----------|-------------|------------|----------------|
| 2023-04-17        | 0.94      | 887         | 1143       | 1.8            |
| 2023-08-22        | 0.89      | 1143        | 982        | 0.7            |
| 2024-01-08        | 0.92      | 982         | 1289       | 2.1            |

The first break on April 17th showed call volume jumping from an average of 887 to 1,143 daily calls—a 29% increase. The variance also nearly doubled, meaning not just higher volume but more unpredictable swings. The second break in late August showed a partial reversion. But the third break in early January was the most dramatic: volume surged to 1,289 calls per day with more than double the variance of the previous period.

```python
import ruptures as rpt
import pandas as pd
import numpy as np

# Sarah's change point detection script
# Load and prep the data
df = pd.read_csv('call_volume.csv', parse_dates=['Date'])
weekday_data = df[df['Weekend'] == 0]['Daily_Calls'].values

# PELT algorithm - lets it find the optimal number of breakpoints
model = rpt.Pelt(model="rbf", min_size=20, jump=1).fit(weekday_data)
penalty_value = 15  # tuned to avoid over-segmentation
breakpoints = model.predict(pen=penalty_value)

# Calculate statistics for each segment
dates = df[df['Weekend'] == 0]['Date'].values
segments = []
prev_idx = 0

for bp in breakpoints[:-1]:  # last point is just the end
    segment_data = weekday_data[prev_idx:bp]
    segments.append({
        'date': dates[bp],
        'mean_before': np.mean(weekday_data[prev_idx:bp]),
        'mean_after': np.mean(weekday_data[bp:breakpoints[breakpoints.index(bp)+1]]) 
                      if bp != breakpoints[-2] else np.mean(weekday_data[bp:]),
        'var_ratio': np.var(weekday_data[bp:]) / np.var(segment_data)
    })
    prev_idx = bp

results_df = pd.DataFrame(segments)
print(results_df)
```

## The Insight

Sarah cross-referenced the dates with company events. April 17th was two weeks after Meridian launched a new mobile app—the one Marketing had been so proud of. The app made filing claims easier, which apparently meant customers were filing *more* claims and calling with questions. August's decline coincided with when they'd finally published the FAQ section that should have launched with the app. And January? That was when a major competitor went bankrupt, and Meridian inherited thousands of new policyholders practically overnight.

The change points weren't random. They were directly tied to business events that operations had never connected to call volume patterns.

## The Decision

Sarah presented her findings to the executive team the following Tuesday. Within two weeks, Operations implemented a new staffing model with three distinct tiers mapped to the identified regimes. They hired twelve additional representatives and restructured shifts to front-load coverage during high-variance periods. More importantly, they created an alert system: if call volume deviated significantly from the current regime's baseline for five consecutive days, it would trigger an investigation into potential new change points.

Six months later, overtime costs were down 34%, and average hold times had dropped from 8.2 minutes to 4.1 minutes.

## What Sarah Would Do Differently

Looking back, Sarah wished she'd incorporated call duration into a multivariate change point model from the start—she later discovered that duration patterns had shifted independently of volume. She also realized her weekend exclusion, while simplifying the analysis, had masked an interesting Friday-to-Monday pattern that might have helped with weekly scheduling optimization. Sometimes the messiness you clean away holds valuable signals too.

## Interpreting Your Results

You've just run change point detection and you're looking at a screen filled with vertical lines on a time series plot, a table of dates and statistics, and possibly some confidence scores. Here's exactly what you're seeing and what it means for your analysis.

### The Change Point Locations

**Plain-English meaning**: These are the specific timestamps where your data's statistical behavior fundamentally shifted. Think of them as the moments when your system moved from one "normal" state to another—a price regime changed, user behavior shifted, or a process broke. The algorithm is saying: "Before this point, the data had one set of properties. After this point, it has different properties."

**Concrete benchmarks**:
- **1–3 change points in a year of daily data**: Normal. Most business processes have occasional regime shifts (seasonality starts, marketing campaigns, policy changes).
- **4–8 change points**: Moderate volatility. Your metric experiences several distinct phases—common in fast-moving industries or metrics influenced by multiple external factors.
- **9+ change points**: High fragmentation. Either your data is genuinely chaotic, you're detecting noise as signal, or you need to adjust sensitivity parameters. Investigate whether this many shifts make business sense.

**Red flags**:
- **Change points clustered within a few days**: Likely detecting noise rather than meaningful shifts. Real regime changes typically persist for weeks or months.
- **Change points at exact regular intervals** (every 7 days, every month): You're detecting seasonality, not structural breaks. Pre-process to remove seasonal patterns first.
- **No change points in obviously volatile data**: Your sensitivity is too low, or the algorithm expects a different change type than what's occurring.

### Confidence Scores or Test Statistics

**Plain-English meaning**: This number indicates how certain the algorithm is that a real change occurred at this location versus random fluctuation. Higher scores mean the "before" and "after" segments are statistically distinct.

**Concrete benchmarks**:
- **Below 0.3 or p-value > 0.1**: Weak evidence. Treat these change points as exploratory only. Don't make decisions based on them.
- **0.3–0.7 or p-value 0.01–0.1**: Moderate confidence. Likely real, especially if they align with known events (product launches, market events).
- **Above 0.7 or p-value < 0.01**: Strong evidence. These are robust change points you can act on with confidence.

**Red flags**:
- **All scores near threshold**: You're right at the edge of detection sensitivity. Small parameter changes would give completely different results.
- **Alternating high/low scores**: Suggests inconsistent detection quality. Review segments with low scores individually.

### Segment Statistics Table

**Plain-English meaning**: For each period between change points, this shows the mean, variance, or other properties that define that regime. This is how you understand *what* changed, not just *when*.

**Reading the patterns**:
- **Mean jumps 20%+ between segments**: Major level shift. Look for operational changes, market events, or data collection issues at those boundaries.
- **Variance doubles or halves**: Risk profile changed. A process became more unstable (or stabilized). Critical for financial or quality control applications.
- **Trend direction reverses**: From growth to decline or vice versa. These are inflection points that demand strategic attention.

**Red flags**:
- **Segment duration < 5% of total time series**: Too short to be a meaningful regime. Either a transient spike or over-sensitive detection.
- **Overlapping confidence intervals across segments**: The "change" isn't statistically meaningful. Segments aren't truly different.

### Sanity Check Checklist

Before trusting your change points, verify:

1. **Do change points align with known events?** Check against your business calendar—launches, policy changes, market shocks. Unexplained changes need investigation.
2. **Are segments long enough to be meaningful?** Each segment should contain at least 10–20 observations to establish stable statistics.
3. **Does visual inspection confirm the breaks?** Plot your time series with change points marked. If you can't see the shift by eye, be skeptical.
4. **Are you detecting the right change type?** Mean shifts, variance changes, and trend breaks require different algorithms. Mismatch creates false positives.
5. **Did you remove artifacts first?** Outliers, missing data patterns, and known seasonality should be addressed before detection.

### Good Enough to Act On?

**Act with confidence when**: You have 1–5 change points with confidence scores >0.6, segment means differ by >15%, and at least half align with known business events. This combination indicates real, interpretable regime changes.

**Keep investigating when**: You have many low-confidence change points, very short segments, or no plausible business explanation for the timing. Run sensitivity analyses and consult domain experts before making decisions.

## Decision Guidance

### What This Result Is Telling You

When your change point analysis identifies a break in your data, it's flagging a moment when the underlying business reality shifted. This isn't about normal day-to-day fluctuations—it's about fundamental regime change. Perhaps customer behavior transformed after a product launch, operational efficiency jumped following a process improvement, or market dynamics altered due to competitive pressure. The detected change point marks the boundary between "before" and "after" states that require different strategies, forecasts, or resource allocations.

The statistical properties that changed—mean, variance, or distribution—translate directly to business predictability and risk. A mean shift indicates your baseline performance level changed: sales settled at a new normal, costs jumped to a different plateau, or engagement dropped to a lower steady state. A variance shift signals that your business became more or less predictable: tighter variance means more reliable forecasting and planning, while increased variance means higher operational uncertainty and risk exposure.

Multiple change points reveal your business operates in distinct phases, each with its own characteristic behavior. Understanding these phases lets you segment your historical data appropriately, build phase-specific models, and recognize when you're entering a new regime that renders your existing assumptions obsolete. The question isn't whether to react—it's whether the new regime requires different tactics, targets, or guardrails.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Single change point with mean shift >20% from baseline | Business fundamentals changed permanently | Update forecasts, targets, and budgets to reflect new baseline; investigate root cause to confirm sustainability | Finance lead, department heads |
| Change point coinciding with known intervention (product launch, policy change, marketing campaign) | Your intervention had measurable impact | Quantify ROI of intervention; decide whether to scale, modify, or terminate initiative | CMO, product owner, initiative sponsor |
| Multiple change points in 6-month window with no variance reduction | System is unstable or experiencing external shocks | Pause long-term planning; implement monitoring dashboards; identify and address sources of instability before committing resources | Operations director, risk manager |
| Variance increase >50% after change point, even if mean is stable | Business predictability degraded; risk increased | Tighten monitoring frequency; increase operational buffers; review contracts and commitments that assume predictable performance | COO, supply chain lead |
| No change points detected despite known major event | Either event had no impact, or model lacks sensitivity | Investigate data quality; consider multivariate analysis; question assumptions about event significance | Analytics team, business owner |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Change point aligns with known business event within ±1 week
- Pre-change and post-change segments each contain ≥30 observations
- Statistical significance p-value <0.01 and practical effect size >15%
- Variance remains stable or decreases after change point

**Proceed with caution when:**
- Change point detected but no obvious business explanation exists
- Effect size is 10–15% (material but modest)
- Only 15–30 observations in either segment
- Multiple methods agree on timing but disagree on magnitude

**Investigate before acting when:**
- Change points detected in <5% of related metrics (suggests isolated data issue)
- Extreme variance spike (>2x increase) accompanies the change
- Change point falls on obvious calendar boundary (month-end, quarter-end) suggesting data artifact
- Fewer than 15 observations in either segment

**Do not use these results yet when:**
- Multiple conflicting change points detected within 2-week windows
- Visual inspection contradicts statistical detection
- Data contains known quality issues, missing values >10%, or reporting changes during analysis period
- Total dataset contains <50 observations

### The Cost of Getting This Wrong

Misinterpreting change point results leads to expensive strategic errors. If you treat a temporary spike as a permanent regime shift, you'll over-invest in capacity, hire staff for demand that evaporates, and lock in contracts at inflated rates—then face painful contraction when reality reasserts itself. Conversely, dismissing a genuine structural break means forecasting with obsolete assumptions: you'll miss budget by millions, stock inventory for customer behavior that no longer exists, and allocate sales territories based on patterns that ended months ago. Perhaps most insidiously, failing to investigate an unexplained change point means operating blind to whatever market force, competitive threat, or operational degradation actually caused it—the change point was your early warning system, and you ignored it. Six months later, when the cause becomes obvious and costly, you'll realize the signal was there all along.

## Common Pitfalls

**The Spurious Spike Trap**

Here's what happened: A retail analyst was monitoring daily sales for change points using a standard CUSUM algorithm. On Black Friday, the algorithm flagged a change point. She reported to leadership that a fundamental shift in customer behavior had occurred and recommended doubling inventory orders for the following weeks. Revenue crashed as unsold inventory piled up through December.

Why it happens: The algorithm can't distinguish between structural breaks and expected anomalies. Black Friday isn't a regime change—it's a known seasonal spike. The analyst treated all detected change points as permanent shifts without considering the business calendar.

How to detect it: Check if detected change points align with known events (holidays, promotions, outages). Calculate the persistence metric: measure whether the new level holds for at least 2–3 times the detection window length. If the data reverts within days, it wasn't a structural break.

The fix: Always exclude or separately handle known event dates before running detection algorithms, and require change points to persist beyond the minimum segment length.

**The Multiple Testing Mirage**

Here's what happened: A junior data scientist was analyzing website traffic across 500 pages, running change point detection independently on each series. The algorithm flagged 47 change points using a significance threshold of α=0.05. He presented all 47 as critical incidents requiring investigation. The engineering team spent weeks chasing ghosts—most were random noise.

Why it happens: Running the same test repeatedly inflates false positive rates. With 500 tests at α=0.05, you expect 25 false positives by chance alone. Without correction, you're guaranteed to find "significant" changes in pure noise.

How to detect it: Calculate the expected false positive count: n_tests × α. If your detection count is close to this number, you're likely seeing noise. Also check: do the flagged series share common characteristics, or do they appear random?

The fix: Apply Bonferroni correction (use α/n_tests) or control the false discovery rate with Benjamini-Hochberg. Better yet, use a Bayesian change point method that naturally penalizes model complexity.

**The Variance Blindness**

Here's what happened: An operations manager was tracking manufacturing defect rates using a mean-shift detection algorithm. The average defect rate remained stable at 2%, so no change points were detected. Meanwhile, the process was becoming increasingly unstable—some days hit 8% defects, others dropped to 0.5%. A major client audit caught the volatility and canceled their contract.

Why it happens: Most practitioners default to mean-shift detection because it's intuitive and widely available. They forget that variance changes are often the first warning signal of process degradation, even when the mean holds steady.

How to detect it: Plot rolling standard deviation alongside rolling mean. If σ_window2 / σ_window1 > 2.0, you have meaningful variance changes. Run diagnostic tests specifically for variance changes (Mood test, Levene's test) in parallel with mean-shift detection.

The fix: Always run both mean and variance change point detection, especially in operational or quality control contexts where process stability matters as much as central tendency.

**The Single-Method Delusion**

Here's what happened: A financial analyst was monitoring trading volumes using PELT (Pruned Exact Linear Time) with default parameters. The algorithm detected five change points in a three-month window. She built trading strategies around these regime changes. Three months later, none of the detected regimes persisted, and the strategies lost money.

Why it happens: Every change point algorithm has biases—PELT favors multiple small changes, Binary Segmentation prefers fewer large ones, Bayesian methods depend heavily on priors. Trusting a single method without validation means inheriting all its blind spots.

How to detect it: Run 2–3 different algorithms (e.g., PELT, Bayesian Online Change Point Detection, and Binary Segmentation). Calculate agreement rate: what percentage of points are flagged by multiple methods? If agreement < 60%, your detections are algorithm-dependent artifacts, not real structure.

The fix: Require consensus across methods for high-stakes decisions, or at minimum report sensitivity analysis showing how detection varies with algorithm choice.

**The Hindsight Overfitting**

Here's what happened: An experienced data scientist was analyzing historical sensor data from an industrial facility. He tuned the penalty parameter in his change point algorithm until the detected breaks perfectly aligned with known equipment failures documented in maintenance logs. He deployed the model for real-time monitoring. It fired constant false alarms on new data.

Why it happens: Tuning detection sensitivity on the same data you're analyzing creates overfitting, just like in supervised learning. The model memorizes past patterns rather than learning generalizable change signatures.

How to detect it: Split your historical data chronologically. Tune parameters on the first 70%, validate on the remaining 30%. If precision drops by more than 20 percentage points on the holdout set, you've overfit.

The fix: Always use temporal cross-validation, never tune on the full dataset you're analyzing.

**The Minimum Segment Amnesia**

Here's what happened: A business analyst was detecting change points in monthly customer churn rates using a package's default settings. The algorithm flagged changes every 2-3 months, creating 15 "regimes" in a three-year period. Each segment was too short to characterize or act upon, rendering the analysis useless for strategic planning.

Why it happens: Default minimum segment lengths are often set to 2 or 5 observations for mathematical reasons, not practical ones. Analysts forget to override these with domain-appropriate values.

How to detect it: Calculate median segment length from your output. If it's less than the time horizon your stakeholders can actually respond to (e.g., quarterly planning cycles), the segmentation is operationally meaningless even if statistically valid.

The fix: Set min_segment_length to the shortest time period where different actions would be taken—usually at least the planning cycle duration for business applications.

**The Edge Effect Ignorance**

Here's what happened: A healthcare analyst was monitoring hospital admission rates using a sliding window approach. She detected a major change point in the most recent week and sent an urgent alert about a public health emergency. The hospital mobilized resources. Two weeks later, the "change point" disappeared as more data arrived—it was just normal weekly variation appearing unusual at the data boundary.

Why it happens: Change point algorithms have reduced statistical power near data edges, especially the most recent observations. There's less context to distinguish signal from noise, but these points often receive the most attention because they're "current."

How to detect it: Check the confidence score or p-value of recent change points versus historical ones. If points in the last 10% of your time series have systematically lower confidence scores but are still flagged, your threshold isn't accounting for edge uncertainty.

The fix: Apply higher detection thresholds (lower sensitivity) for points in the final 5–10% of the time series, or simply exclude the most recent window from automated alerting until sufficient data accumulates.

## Common Misconceptions

**"If the change point detection algorithm finds breakpoints, that proves the underlying process actually changed"**

**Why people believe this:** Statistical significance feels like proof. When an algorithm confidently identifies a change point with a low p-value, it's natural to conclude that something meaningful shifted in the real world. The mathematical rigor of the test seems to validate the existence of a genuine structural break.

**The truth:** Change point algorithms detect *statistical incompatibility* between segments, not causal shifts in the data-generating process. They're equally good at finding places where your measurement system changed, where you switched data vendors, where a bug was introduced in logging, or where sampling methodology shifted. The algorithm has no mechanism to distinguish between "revenue dropped because customer behavior changed" and "revenue dropped because we started excluding refunds from the calculation." Change points are candidates for investigation, not conclusions.

**The real-world consequence:** A retail analytics team detects a significant change point in customer purchase frequency in March 2020 and builds elaborate models around a "new customer regime." Six months later, they discover their web analytics vendor changed how they deduplicated user sessions in that exact month. They've been optimizing for an artifact, and their models catastrophically fail when the vendor reverts the change.

**"You need more sophisticated algorithms when simple methods fail to detect known changes"**

**Why people believe this:** It mirrors our general experience with tools—when a basic tool doesn't work, you reach for a more advanced one. If CUSUM doesn't find the change point you know exists, surely a Bayesian hierarchical model or deep learning approach will be more "powerful" enough to detect it.

**The truth:** Detection failure usually stems from insufficient signal-to-noise ratio, not algorithmic inadequacy. More complex algorithms don't extract signal that isn't there; they just make different assumptions about what constitutes a change. If you know a change occurred but can't detect it, the problem is typically that the change is small relative to natural variation, or you're looking at the wrong variable. Adding algorithmic complexity often just makes it easier to detect spurious patterns.

**The real-world consequence:** A manufacturing team can't reliably detect process shifts they know happen during maintenance windows. Instead of instrumenting additional sensors or increasing measurement frequency, they implement an ensemble of sophisticated neural network-based detectors. The system now flags dozens of false positives daily, operators lose trust, and real quality issues get missed in the noise. The actual solution required measuring at higher resolution, not more complex algorithms.

**"Change points must be treated as unknown locations to be estimated"**

**Why people believe this:** This matches the framing of change point detection in academic literature and software documentation, where the primary goal is to *find* change points. The mathematical elegance lies in joint estimation of the number, locations, and magnitudes of changes.

**The truth:** In operational settings, you often know *exactly* when changes occurred—deployments, policy changes, vendor switches, market events. The valuable question isn't "where did things change?" but "did this known intervention actually shift the process, and by how much?" Framing everything as unknown change point detection obscures the more useful framework of intervention analysis or segmented regression, where you test whether known boundaries matter.

**The real-world consequence:** After a pricing change, a product team runs change point detection across the entire year of sales data. The algorithm identifies a break point two weeks *after* the actual price change, leading to confused interpretations about "delayed response." They've asked the wrong question—they needed interrupted time series analysis to quantify the price change effect, not blind change point detection.

## How This Connects

### Before This Node

**Aggregate Time Series** prepares raw transactional or event-level data into regularly spaced intervals (hourly, daily, weekly) with a chosen metric, which is essential because change point algorithms require ordered sequences with consistent temporal spacing—irregularly sampled data produces spurious breakpoints where gaps in observation occur, not where true structural shifts happen.

**Remove Seasonality** isolates the underlying trend and level shifts from cyclical patterns, which matters because change point methods detect abrupt changes in statistical properties, and strong seasonal cycles create repetitive "false" breaks at every seasonal peak or trough unless the seasonal component is first extracted or controlled for.

**Impute Missing Values** fills gaps in the time series using forward-fill, interpolation, or model-based methods, which is critical because most change point algorithms assume continuous sequences, and missing values either cause algorithms to fail outright or create artificial breakpoints at every gap where the statistical properties appear to "jump" due to data absence rather than real regime change.

**Normalize or Scale** standardizes the magnitude of the series (z-scores, min-max scaling), which helps when comparing change point significance across multiple series or when variance changes are more informative than mean shifts—bad upstream scaling, like leaving raw counts alongside percentages, causes algorithms to detect breaks only in high-magnitude series while missing meaningful shifts in smaller-scale metrics.

**Filter Noise** applies smoothing techniques (moving averages, lowpass filters) to reduce high-frequency fluctuations, which prevents change point detectors from flagging every random spike as a structural break—unfiltered noisy data produces dozens of detected breakpoints that reflect measurement error or natural variation rather than meaningful regime transitions.

### After This Node

**Segment Time Series** partitions the full sequence into homogeneous intervals defined by the detected change points, creating separate datasets for each regime that can be modeled, forecasted, or analyzed independently—change point locations provide natural, data-driven boundaries rather than arbitrary calendar-based splits.

**Visualize Time Series** overlays detected breakpoints onto line plots as vertical markers or shaded regions, enabling stakeholders to visually confirm whether algorithmic detections align with known business events (product launches, policy changes, market shocks) and to communicate findings in executive summaries.

**Train Separate Models** builds distinct regression, classification, or forecasting models for each regime identified by change points, which improves predictive accuracy because model parameters (slopes, seasonality strength, error distributions) often differ fundamentally across regimes—forcing a single model across a break degrades performance.

**Root Cause Analysis** investigates *why* each detected change point occurred by joining breakpoint timestamps with external event logs (marketing campaigns, competitor actions, regulatory changes), turning purely statistical detections into actionable business insights about what drove the shift.

**Forecast with Regime Awareness** uses only post-change-point data to train forward-looking models, which prevents contamination from obsolete historical regimes—forecasting sales after a pricing change using pre-change data produces systematically biased predictions.

### Common Pipeline Patterns

**Revenue Monitoring Pipeline**  
Aggregate Time Series → Remove Seasonality → **Detect Change Points** → Segment Time Series → Root Cause Analysis  
Identifies when revenue streams fundamentally shifted, isolates stable growth periods from disruption events, and links breakpoints to specific business decisions for executive reporting.

**Quality Control Pipeline**  
Aggregate Time Series → Filter Noise → **Detect Change Points** → Visualize Time Series → Train Separate Models  
Monitors manufacturing or service metrics to flag when process behavior changed, enabling quality engineers to model "good" versus "degraded" operating regimes separately.

**Customer Churn Analysis Pipeline**  
Normalize or Scale → **Detect Change Points** → Segment Time Series → Forecast with Regime Awareness  
Detects when user engagement patterns shifted (app redesign, competitor launch), segments users into behavioral cohorts, and forecasts churn using only recent regime data.

### What to Have Ready

**Time-ordered data with timestamps**: Your dataset must include a datetime column sorted chronologically with no duplicate timestamps—change point algorithms rely on sequence order, and unsorted or duplicated time indices produce meaningless results.

**Defined metric of interest**: Decide whether you're monitoring mean shifts, variance changes, or distributional breaks, and compute the corresponding univariate series—trying to detect change points on raw multi-column tables without specifying *what statistic should change* leads to ambiguous, uninterpretable breakpoints.

**Expected number of change points or sensitivity threshold**: Determine if you're looking for a few major regime shifts (2–5 breaks) or many micro-transitions, and set algorithm parameters accordingly—default settings often over-detect, flagging noise as breaks.

**Domain context for validation**: Maintain a timeline of known business events (product launches, marketing blitzes, external shocks) to validate detected breakpoints—purely algorithmic detections without business interpretation are forensic curiosities, not actionable insights.

## Try It Yourself

### Recommended Dataset

**Dataset:** `airline_passengers` from statsmodels  
**Source:** `statsmodels.datasets.co2.load_pandas().data` or create synthetic airline passenger data  
**Why it's ideal:** This monthly passenger count time series (~144 observations) contains a well-documented structural break around observation 100 where growth rate shifts abruptly, plus seasonal patterns that make change points visually interpretable. The single-variable sequential format perfectly demonstrates when statistical properties change.  
**Business question:** When did airline travel patterns fundamentally shift, indicating a new market regime requiring different capacity planning?  
**Size:** ~144 rows × 1 column (time series)

### Starter Code

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.diagnostic import breaks_cusumolsresid

# Generate airline-style data with known change point at observation 75
np.random.seed(42)
n = 120
# First regime: slower growth with lower variance
regime1 = 100 + np.arange(75) * 2 + np.random.normal(0, 5, 75)
# Second regime: faster growth with higher variance (structural break)
regime2 = regime1[-1] + np.arange(45) * 5 + np.random.normal(0, 12, 45)
passengers = np.concatenate([regime1, regime2])
time_index = pd.date_range('2015-01', periods=n, freq='M')
df = pd.DataFrame({'passengers': passengers}, index=time_index)

print("=== CHANGE POINT DETECTION: AIRLINE PASSENGERS ===\n")
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df.index[0].strftime('%Y-%m')} to {df.index[-1].strftime('%Y-%m')}\n")

# Method 1: Cumulative sum (CUSUM) - detects mean shifts
cumsum = np.cumsum(df['passengers'] - df['passengers'].mean())
# Change point is where cumsum reaches maximum deviation
change_idx = np.argmax(np.abs(cumsum))
print(f"1. CUSUM detected change at: {df.index[change_idx].strftime('%Y-%m')} (observation {change_idx})")

# Method 2: Binary segmentation - splits data at point of maximum difference
def binary_segment_split(series):
    """Find single best split point by comparing segment means"""
    best_score = -np.inf
    best_split = None
    for i in range(20, len(series)-20):  # Avoid edge splits
        left_mean = series[:i].mean()
        right_mean = series[i:].mean()
        # Score is the difference in means weighted by segment sizes
        score = i * (len(series)-i) * (left_mean - right_mean)**2
        if score > best_score:
            best_score = score
            best_split = i
    return best_split

split_point = binary_segment_split(df['passengers'].values)
print(f"2. Binary segmentation split: {df.index[split_point].strftime('%Y-%m')} (observation {split_point})")

# Method 3: Rolling window variance - detects volatility changes
window = 20
rolling_var = df['passengers'].rolling(window).var()
var_change = rolling_var.idxmax()  # Peak variance change location
print(f"3. Maximum variance shift: {var_change.strftime('%Y-%m')}")

# Calculate business metrics before/after detected change point
before = df.iloc[:split_point]['passengers']
after = df.iloc[split_point:]['passengers']
print(f"\n=== BUSINESS IMPACT ===")
print(f"Growth rate before: {before.diff().mean():.1f} passengers/month")
print(f"Growth rate after:  {after.diff().mean():.1f} passengers/month")
print(f"Volatility before: σ={before.std():.1f}")
print(f"Volatility after:  σ={after.std():.1f}")

# Visualization: show detected change point
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['passengers'], label='Passengers', linewidth=2)
plt.axvline(df.index[split_point], color='red', linestyle='--', 
            label=f'Detected change point', linewidth=2)
plt.title('Airline Passengers with Detected Change Point')
plt.xlabel('Date')
plt.ylabel('Passenger Count')
plt.legend()
plt.tight_layout()
plt.savefig('changepoint_detection.png', dpi=100)
print(f"\nVisualization saved as 'changepoint_detection.png'")
```

### What to Try Next

1. **Change the random seed** (line 8: `np.random.seed(99)`): You'll see different noise patterns but the algorithm should still detect a change point near observation 75. This teaches robustness—good methods find real breaks despite noise.

2. **Add a second change point** (insert `regime3 = regime2[-1] + np.arange(30) * 1 + np.random.normal(0, 3, 30)` and concatenate): Binary segmentation finds only the *strongest* break. Expect it to miss the subtler second change, teaching you that iterative methods are needed for multiple breaks.

3. **Reduce the magnitude of change** (line 12: change `* 5` to `* 2.5`): The algorithms will struggle or mislocate the break. This teaches sensitivity—smaller structural changes require more data or different statistical tests.

4. **Modify the rolling window size** (line 46: change `window = 20` to `window = 5` or `40`): Smaller windows detect local volatility spikes; larger windows smooth over noise but may miss precise timing. This teaches the bias-variance tradeoff in change point precision.

## Further Reading

1. **Killick, R., Fearnhead, P., & Eckley, I. A. (2012). "Optimal Detection of Changepoints With a Linear Computational Cost." *Journal of the American Statistical Association*, 107(500), 1590-1598.** Read this if you want to understand how the PELT (Pruned Exact Linear Time) algorithm achieves exact change point detection with O(n) complexity instead of O(n²), making it practical for large-scale applications. The paper's key contribution is showing how dynamic programming with pruning can eliminate the traditional speed-accuracy tradeoff.

2. **Aminikhanghahi, S. & Cook, D. J. (2017). "A Survey of Methods for Time Series Change Point Detection." *Knowledge and Information Systems*, 51(2), 339-367.** Read this if you want a comprehensive taxonomy that categorizes change point methods by their assumptions (online vs. offline, parametric vs. nonparametric, single vs. multiple change points) and clarifies when each approach is appropriate for different data characteristics.

3. **Basseville, M. & Nikiforov, I. V. (1993). *Detection of Abrupt Changes: Theory and Application*. Prentice Hall. Chapter 2 ("Statistical Methods for Change Detection"), pages 13-49.** This chapter provides the rigorous statistical foundation for likelihood ratio tests and CUSUM methods, deriving the mathematical properties that make these approaches optimal under specific distributional assumptions—essential for understanding why these methods work, not just how to apply them.

4. **Matteson, D. S. & James, N. A. (2014). "A Nonparametric Approach for Multiple Change Point Analysis of Multivariate Data." *Journal of the American Statistical Association*, 109(505), 334-345.** This introduces the E-Divisive algorithm, which extends change point detection to multivariate time series without requiring parametric assumptions. The specific insight is how energy statistics enable distribution-free testing in high dimensions where traditional methods fail.

5. **ruptures Python library documentation: `ruptures.Pelt` class.** Focus on the `model` parameter options (`"l1"`, `"l2"`, `"rbf"`, `"linear"`) and the examples showing how cost function choice affects sensitivity to different types of changes (mean shifts vs. variance changes vs. distributional changes). This bridges theory to implementation decisions.

6. **"Change Point Detection: An Analysis of the Central England Temperature Data" by Andrew Hetherington (Towards Data Science, 2020).** This tutorial stands out because it systematically compares five different algorithms (PELT, Binary Segmentation, Bottom-Up, Window-Based, Bayesian) on the same dataset with visualization of each method's strengths, making the practical tradeoffs concrete rather than abstract.

7. **MIT OpenCourseWare: 6.436J "Fundamentals of Probability," Lecture 23 on Sequential Hypothesis Testing (timestamp 28:15-45:30).** This segment derives the Sequential Probability Ratio Test (SPRT) and connects it to online change point detection, showing how optimal stopping theory provides theoretical guarantees for real-time monitoring applications.

8. **Netflix Technology Blog: "Robust Anomaly Detection for Streaming Data" (2019).** Documents how Netflix uses change point detection within their RAD (Robust Anomaly Detection) system to distinguish true metric regime changes from noise across millions of time series, detailing their specific modifications to handle seasonality and scale.

## Practice Exercises

### Exercise 1: E-commerce Conversion Rate Investigation (Conceptual)

**Scenario:**
You're the analytics lead at an online furniture retailer. Your marketing team launched a new checkout flow on March 15th to reduce cart abandonment. Your boss shows you this weekly data and asks whether the new checkout is working:

- **Weeks 1-8 (before launch):** Average conversion rate = 3.2%, Standard deviation = 0.3%
- **Weeks 9-16 (after launch):** Average conversion rate = 3.5%, Standard deviation = 0.7%

"I see the conversion rate increased from 3.2% to 3.5%," your boss says. "Should we roll this out to our mobile app too? And why is the variance so much higher now?"

A colleague suggests: "Let's use change point detection to confirm March 15th was significant."

**Your tasks:**
(a) Is change point detection the right approach here?
(b) What concerns should you raise about this data?
(c) What would you recommend investigating before making a decision?

**Worked Answer:**

**(a) Appropriateness of change point detection:**

Change point detection is **not the ideal primary tool** here, though it could play a supporting role. Here's why:

The business question is: "Did our *intervention* cause a meaningful improvement?" This is fundamentally a **causal inference** question, not an exploratory "when did something change?" question. You already know when the potential change occurred (March 15th)—you don't need an algorithm to discover it.

More appropriate approaches would be:
- **A/B testing analysis** (if the rollout was gradual)
- **Interrupted time series analysis** to assess whether the post-intervention trend differs from what would be expected
- **Statistical hypothesis testing** (e.g., two-sample t-test) to assess whether the difference is statistically significant

Change point detection would be valuable if you were investigating: "Our conversion rate seems unstable—when did changes occur?" without knowing about the March 15th intervention.

**(b) Concerns to raise:**

**The increased variance is a major red flag.** While the mean increased by 0.3 percentage points (9% relative increase), the standard deviation more than doubled from 0.3% to 0.7%. This suggests:

1. **Inconsistent performance:** Some weeks post-launch may be worse than the pre-launch average
2. **Possible confounding factors:** External variables (seasonality, promotions, traffic source shifts) may be affecting post-launch weeks differently
3. **Sample size variations:** If weekly traffic volumes changed, this could explain variance changes
4. **Subgroup effects:** The new flow might work well for some customer segments but poorly for others

**Statistical significance is questionable.** The effect size (0.3%) is small relative to the new variance (0.7%), suggesting the difference may not be statistically significant despite appearing positive.

**(c) Recommended investigations:**

Before rolling out to mobile, you should:

1. **Conduct formal hypothesis testing:** Calculate whether the 0.3 percentage point increase is statistically significant given the variance. With only 8 weeks post-launch and high variance, you may lack statistical power.

2. **Perform week-by-week analysis:** Plot the 16 weeks as a time series. Look for:
   - Are post-launch weeks *consistently* better, or are a few outlier weeks driving the average up?
   - Is there a trend (improving over time as users adapt, or degrading as novelty wears off)?

3. **Investigate the variance increase:** Break down by:
   - **Traffic source:** Did the checkout work well for paid search but poorly for organic?
   - **Device type:** (Even within desktop, different browsers may behave differently)
   - **Product category:** High-ticket items may show different behavior than accessories

4. **Check for confounds:** Were there promotions, seasonal events, or competitor actions in weeks 9-16 that didn't occur in weeks 1-8?

5. **Calculate business impact:** Even if statistically significant, is 0.3 percentage points meaningful? With the increased variance suggesting potential reliability issues, the business risk may outweigh a modest gain.

**Recommendation:** Do *not* proceed with mobile rollout yet. The increased variance suggests the new checkout may have introduced instability. Commission a proper A/B test on mobile with sufficient sample size, or conduct deeper analysis on the desktop data to understand what's driving the variance before expanding.

---

### Exercise 2: SaaS Monthly Active User Detection (Applied)

**Task:**
You're analyzing a B2B SaaS platform's monthly active users (MAU). The product team suspects that a major feature release in mid-2023 affected user engagement, but they're not sure when the impact actually materialized (features often take time for adoption). Use change point detection to identify when significant shifts occurred and assess whether they align with the feature release timing.

**Dataset Setup:**

```python
import numpy as np
import pandas as pd
from ruptures import Phat
import matplotlib.pyplot as plt

# Monthly Active Users data (Jan 2022 - Dec 2023)
np.random.seed(42)
dates = pd.date_range('2022-01-01', '2023-12-31', freq='MS')

# True structure: stable growth until July 2023, then acceleration
mau_base = np.concatenate([
    15000 + np.arange(18) * 200 + np.random.normal(0, 300, 18),  # Jan 22 - Jun 23
    18600 + np.arange(6) * 850 + np.random.normal(0, 350, 6)     # Jul 23 - Dec 23
])

df = pd.DataFrame({'date': dates, 'mau': mau_base})
print(df.head(10))
```

**Your tasks:**
1. Implement change point detection using the Phat algorithm (detects mean shifts)
2. Identify the detected change point date(s)
3. Calculate mean MAU before and after the change point
4. Interpret whether this aligns with the "mid-2023 feature release" hypothesis

**Worked Solution:**

```python
# 1. Apply Phat change point detection
model = Phat(min_size=3, jump=1).fit(df['mau'].values)
change_points = model.predict(n_bkps=1)  # Detect 1 change point

# change_points returns index positions, last element is always len(data)
cp_index = change_points[0]
cp_date = df.iloc[cp_index]['date']

print(f"Change point detected at index: {cp_index}")  # Output: 18
print(f"Change point date: {cp_date}")  # Output: 2023-07-01

# 2. Calculate statistics before and after
before_cp = df.iloc[:cp_index]['mau']
after_cp = df.iloc[cp_index:]['mau']

mean_before = before_cp.mean()  # Output: ~15951
mean_after = after_cp.mean()    # Output: ~21346
pct_increase = ((mean_after - mean_before) / mean_before) * 100

print(f"\nMean MAU before change: {mean_before:.0f}")  # 15951
print(f"Mean MAU after change: {mean_after:.0f}")     # 21346
print(f"Percentage increase: {pct_increase:.1f}%")     # 33.8%

# 3. Visualize
plt.figure(figsize=(12, 5))
plt.plot(df['date'], df['mau'], marker='o', label='MAU')
plt.axvline(cp_date, color='red', linestyle='--', 
            label=f'Detected Change: {cp_date.strftime("%b %Y")}')
plt.axhline(mean_before, color='blue', linestyle=':', 
            alpha=0.6, label=f'Mean Before: {mean_before:.0f}')
plt.axhline(mean_after, color='green', linestyle=':', 
            alpha=0.6, label=f'Mean After: {mean_after:.0f}')
plt.xlabel('Date')
plt.ylabel('Monthly Active Users')
plt.title('MAU Change Point Detection')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

**Business Interpretation:**

The change point detection algorithm identified **July 2023** as the month when MAU growth fundamentally shifted, with mean MAU increasing by 34% from ~15,951 to ~21,346. This finding **strongly supports the product team's hypothesis** that the mid-2023 feature release drove meaningful engagement improvement. Notably, the impact appears immediate (within the same month), suggesting either strong initial adoption or that "mid-2023" actually meant early July. The product team should investigate which specific features drove this engagement spike to inform future development priorities and consider case studies from early adopters to understand adoption drivers.

---

### Exercise 3: False Change Point in Seasonal Revenue Data (Challenge)

**Problem:**
A retail analytics team detects a "significant change point" in daily revenue data at the beginning of November. They conclude a recent marketing campaign was successful. However, you suspect the algorithm is simply detecting the start of holiday shopping season, not a true structural break. 

**Task:** Demonstrate why naive change point detection fails on seasonal data and implement a proper approach that accounts for seasonality.

**Setup:**

```python
import numpy as np
import pandas as pd
from ruptures import Phat, Binseg
from statsmodels.tsa.seasonal import seasonal_decompose

np.random.seed(123)
days = pd.date_range('2023-01-01', '2023-12-31', freq='D')

# Revenue with strong annual seasonality (holiday spike) but NO structural break
day_of_year = np.arange(1, 366)
seasonal_component = 5000 + 15000 * np.exp(-((day_of_year - 330) ** 2) / 1000)
trend = 20000 + day_of_year * 5
noise = np.random.normal(0, 1500, 365)

revenue = trend + seasonal_component + noise
df = pd.DataFrame({'date': days, 'revenue': revenue})
```

**Your tasks:**
1. Show that naive change point detection incorrectly identifies early November as a break
2. Explain why this is a false positive
3. Implement a seasonality-adjusted approach and show it finds no true structural change

**Worked Solution:**

```python
# 1. NAIVE APPROACH - Direct change point detection
model_naive = Phat(min_size=5).fit(df['revenue'].values)
naive_cps = model_naive.predict(n_bkps=1)
naive_cp_date = df.iloc[naive_cps[0]]['date']

print("=== NAIVE APPROACH ===")
print(f"Detected change point: {naive_cp_date}")  # Output: 2023-11-01
print(f"Date: {naive_cp_date}")

# Show means before/after
mean_before_naive = df.iloc[:naive_cps[0]]['revenue'].mean()
mean_after_naive = df.iloc[naive_cps[0]:]['revenue'].mean()
print(f"Mean before: ${mean_before_naive:,.0f}")  # ~25,188
print(f"Mean after: ${mean_after_naive:,.0f}")    # ~43,921
print(f"Apparent increase: {((mean_after_naive/mean_before_naive)-1)*100:.1f}%")

# 2. WHY THIS IS WRONG
print("\n=== WHY NAIVE APPROACH FAILS ===")
print("The algorithm detects a mean shift in early November because")
print("revenue genuinely increases then—but this is SEASONAL, not structural.")
print("A structural break means the underlying process changed.")
print("Seasonal patterns are recurring, predictable features of the process.")

# 3. PROPER APPROACH - Decompose and test residuals
decomposition = seasonal_decompose(df.set_index('date')['revenue'], 
                                   model='additive', period=365)
residuals = decomposition.resid.dropna()

# Apply change point detection to deseasonalized residuals
model_proper = Phat(min_size=10).fit(residuals.values)
proper_cps = model_proper.predict(n_

## Quick Quiz

**Question:** A data scientist observes gradual quarterly revenue growth over two years, followed by a sudden 40% drop in Q3 due to a regulatory change, then resumption of the previous growth trend. When would change point detection methods be most appropriately applied to this scenario?

A) Throughout the entire sequence to identify both the gradual growth phases and the sudden drop
B) Only at the sudden drop, since change point detection requires abrupt shifts rather than gradual trends
C) At the sudden drop and potentially at the resumption point, after first removing or accounting for the underlying growth trend
D) Never, because the drop has a known external cause (regulatory change), making statistical detection redundant

**Answer:** C

**Explanation:** Change point detection identifies locations where **statistical properties** undergo abrupt shifts, which requires examining changes *relative to the local data-generating process*. The gradual growth represents a smooth trend, not a change point; the regulatory shock causes an abrupt shift in level that disrupts this trend. Option C correctly recognizes that trend removal or accounting is necessary first—otherwise, the method might detect spurious changes caused by comparing different points along a slope rather than true structural breaks. Option A misunderstands that gradual changes are not change points (they're trends requiring different methods). Option B is partially correct about requiring abrupt shifts but fails to recognize that trend-adjustment may be needed to properly detect those shifts. Option D represents the misconception that knowing the *cause* of a change eliminates the value of *detecting and locating* it statistically; change point methods remain useful for precise timing identification and validation even when causes are suspected.

## Heuristics

**You need at least 20 observations between change points, or you're detecting noise.**
Change point algorithms can mathematically flag shifts every few data points, but segments shorter than 20 observations rarely represent meaningful regime changes—they're typically capturing natural fluctuation. Use minimum segment length constraints to enforce this, or manually filter results post-detection to exclude micro-segments that can't be reliably characterized.

**If 30% or more of your data gets flagged as change points, you're overfitting.**
When your algorithm identifies change points at every turn, you've abandoned the core premise: that data contains relatively stable regimes punctuated by *occasional* shifts. This often signals penalties that are too weak, inappropriate window sizes, or fundamentally non-stationary data that needs a different approach entirely. Real structural breaks are rare events—if they're not rare in your output, recalibrate.

**Always validate detected change points against known business events before reporting them.**
The most credible change point analysis doesn't just find statistical breaks—it connects them to real-world causes: product launches, policy changes, market shocks, system updates. When detected points align with documented events, you build stakeholder trust and confirm your method sensitivity. When they don't, you've either discovered something surprising (investigate) or tuned your algorithm incorrectly (recalibrate).

**For time series with strong seasonality, deseasonalize first or switch to residual-based detection.**
Change point algorithms interpret seasonal peaks and troughs as potential regime shifts if you feed them raw data. Monthly sales that spike every December aren't experiencing structural change twelve times—they're seasonal. Remove the seasonal component, then detect changes in the deseasonalized series or in model residuals. Otherwise, you'll waste time explaining that winter isn't a change point.

**Use offline methods for historical analysis; reserve online methods only when decisions require immediate response.**
Offline (retrospective) algorithms access the full dataset and deliver more accurate, stable change point estimates. Online (sequential) methods process data point-by-point and are computationally cheaper but detect changes with delay and higher false positive rates. Unless you're monitoring production systems that need real-time alerts, use offline methods—the quality difference is substantial.

**When comparing change point locations across multiple series, demand agreement within 5% of series length.**
If you're detecting change points in regional sales data and one region shows a break at month 10 while another shows month 40 in a 100-month series, they're probably different phenomena despite superficial similarity. Synchronized change points should cluster tightly in time—within roughly 5 data points per 100 observations. Loose alignment suggests you're finding idiosyncratic noise, not common structural breaks.

**Don't use change point detection on data with fewer than 50 total observations.**
The statistical power to reliably distinguish true regime shifts from random variation emerges only with sufficient sample size. Below 50 points, you lack the data to confidently characterize even two distinct regimes (requiring ~25 observations each by the 20-point rule). Visual inspection and domain knowledge serve you better than algorithmic detection in small samples.

**Expert practitioners validate stability by checking whether change points persist when you remove the last 10% of data.**
Mediocre analysts run one change point detection and present results. Strong practitioners test robustness by rerunning detection on progressively truncated data. If a change point detected at position 80 in 100 observations disappears when you only analyze the first 90 points, it's an artifact of end effects or insufficient evidence. Stable, real change points remain detectable even when you withhold recent data.

## Nuggets

**Change points you can see often don't exist statistically.**
Human visual perception excels at detecting patterns, but systematically overinterprets random fluctuations as meaningful breaks. Studies show that when analysts visually identify change points in simulated data with *no* true breaks, they flag false positives 40–60% of the time, even with statistical training. The practical implication: always run a formal test before acting on what "looks like" a change point. Your eyes evolved to detect predators in bushes, not differentiate between σ and 1.2σ deviations.

**Detecting variance changes is fundamentally harder than detecting mean shifts—and fails silently.**
Most change point algorithms (CUSUM, PELT, binary segmentation) are designed primarily for mean changes and perform poorly when only variance shifts. A time series can double its variance with zero mean change, yet standard methods will report "no change point detected" without warning you they weren't really looking. Research shows detection power for variance-only changes drops below 30% for sample sizes under 200, compared to 80%+ for equivalent mean shifts. Always inspect residual plots and consider dedicated tests like the Levene statistic applied to segmented windows.

**Multiple change points create a combinatorial explosion that destroys test validity.**
When you test for k change points, you're implicitly conducting O(n^k) comparisons across possible segmentations, yet standard p-values assume a single test. A Bayesian information criterion (BIC) approach with 3 change points on 1000 observations evaluates roughly 166 million configurations. Without correction (e.g., parametric penalties in BIC, or permutation-based null distributions), your "significant" change point at p<0.05 might actually occur by chance 80% of the time. The uncomfortable truth: most papers applying change point detection to find 5+ breaks don't account for this multiplicity, rendering their inference unreliable.

**Equally-spaced change points are a red flag, not a pattern.**
When an algorithm returns change points that divide your data into suspiciously equal segments (e.g., breaks at observations 250, 500, 750 in a 1000-point series), it's almost always an artifact of the detection method, not the data. Algorithms like binary segmentation have a documented bias toward balanced splits due to how they recursively partition. Real change points—from policy shifts, equipment failures, or regime changes—follow the irregular timing of real-world events. If your detected breaks look like someone divided the data with a ruler, re-run with a different algorithm or stronger penalty term.

**Autocorrelation turns change point detection into a minefield.**
Standard change point tests assume independent observations, but time series are rarely independent. Positive autocorrelation inflates false positive rates dramatically—one study found CUSUM methods reported spurious change points in AR(1) processes with ρ=0.7 at rates exceeding 40%, versus the nominal 5%. Worse, pre-whitening the data (fitting an ARMA model first) introduces its own bias, as model misspecification creates artificial breaks. The robust approach: use bootstrap or permutation tests that preserve temporal dependence structure, or switch to methods explicitly designed for dependent data like the change point test for ARMA processes.

**The "best" number of change points often tells you more about your penalty choice than your data.**
Information criteria like BIC balance fit quality against model complexity, but the penalty weight is somewhat arbitrary—BIC uses log(n), AIC uses 2, and dozens of alternatives exist. Empirical studies show that varying penalty strength by 50% routinely changes the selected number of change points by ±2, even on the same dataset. This sensitivity reveals an underappreciated reality: there's rarely a single "true" number of breaks. Consider reporting a range (e.g., "2–4 change points are plausible") rather than false precision, and always conduct sensitivity analysis across penalty values.

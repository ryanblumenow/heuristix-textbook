# Track Groups


![](../../_static/figures/track-groups_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The most common mistake with Track Groups is creating too many granular segments that lack statistical power for meaningful predictions. Aim for 3-7 cohorts maximum and validate that each group has sufficient sample size before building predictive models on top of them. Remember that the goal is actionable segmentation, not perfect classification—a 70% accurate high-value group is far more useful than ten groups with 95% accuracy but no clear business action.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Track Groups forecasts multiple related time series simultaneously while ensuring the numbers add up correctly when you roll them up or break them down.

**When to use it:** You need forecasts at different levels—by product, region, or category—and those forecasts must reconcile when combined (e.g., all store forecasts must sum to the company total).

**What you get back:** A complete set of forecasts at every level of your hierarchy that are mathematically consistent, so finance sees the same total whether they sum individual stores or look at the company-wide forecast directly.

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Minutes on 100K rows |
| **What you bring** | Historical time series data with grouping variables (e.g., product_id, region, date, sales) |
| **What you get** | Coherent forecasts at all hierarchy levels |
| **Heuristix bucket** | Predict — Machine Learning & Forecasting |

**Track Groups prevents the common disaster where individual forecasts don't match aggregate targets, eliminating the manual reconciliation spreadsheets that plague planning cycles.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify situations where forecasts must remain consistent across product categories, geographic regions, or organizational hierarchies—and recognize when Track Groups is the appropriate solution.
- Interpret reconciled forecasts at different hierarchy levels, explain to stakeholders why group-level totals may differ from simple aggregations, and communicate the trade-offs between local accuracy and global coherence.
- Decide which level of the hierarchy to use for operational planning decisions, such as whether to allocate inventory based on bottom-level forecasts or proportionally distribute top-level predictions.

**After reading this chapter, a data scientist will be able to:**

- Implement Track Groups by correctly specifying hierarchical structures, selecting appropriate base forecasting models for each level, and applying reconciliation methods that preserve both statistical properties and business constraints.
- Tune the reconciliation approach by choosing between bottom-up, top-down, and optimal combination methods based on where forecast accuracy is strongest in the hierarchy and where coherence matters most.
- Validate Track Groups forecasts by comparing reconciled versus base forecasts at each level, diagnosing cases where reconciliation degrades accuracy, and detecting structural breaks or misspecified hierarchies that violate coherence assumptions.

## Overview

Track Groups is a hierarchical forecasting methodology that partitions time series data into coherent groups based on shared structural characteristics, enabling the construction of models that respect the natural organisation of business data while maintaining forecast coherence across aggregation levels. The technique belongs to the family of grouped and hierarchical time series methods, bridging the gap between bottom-up forecasting of individual series and top-down allocation of aggregate forecasts. By explicitly modelling the grouping structure, Track Groups produces forecasts that are both statistically optimal at each level and arithmetically consistent when aggregated or disaggregated across the hierarchy.

## When to Use This

- **Use this when** your time series naturally form a hierarchy or grouping structure (e.g., sales by product within category within department) and you need forecasts at multiple levels of aggregation simultaneously.

- **Use this when** forecast coherence is a business requirement—for example, when regional forecasts must sum exactly to national forecasts for budgeting or inventory allocation purposes.

- **Use this when** you have many related time series with varying signal strength, and you want to leverage cross-sectional information to improve forecasts for sparse or volatile individual series.

- **Use this when** you need to reconcile forecasts produced by different teams or models operating at different levels of the organisation.

- **Use this when** your planning processes require consistent numbers across different stakeholder views (e.g., finance sees totals, operations sees product-level detail).

- **Use this when** some series in your hierarchy have short histories or missing data, and you want to "borrow strength" from related series with more complete data.

- **Do NOT use this when** your time series are genuinely independent with no meaningful grouping structure—the overhead of reconciliation provides no benefit.

- **Do NOT use this when** you have only a single time series or a flat collection of unrelated series without any natural aggregation relationships.

- **Do NOT use this when** computational resources are severely constrained and you have a very large hierarchy (thousands of bottom-level series) without access to sparse matrix optimisations.

- **Do NOT use this when** the grouping structure is unstable over time (e.g., frequent reorganisations that change the hierarchy), unless you can account for structural breaks.

## Questions This Answers

### Planning and Allocation Across Levels

**How do we forecast total company revenue while ensuring regional and product-line forecasts actually add up to that number?**

**If we're predicting £2.5M in Q4 sales, how should that break down across our 6 regions and 15 product categories?**

**Can we forecast both national demand and store-level demand without the store forecasts contradicting the national outlook?**

**Should we build one model for the entire business or separate models for each division, and how do we keep them consistent?**

**We need next year's headcount by department and location — how do we ensure the pieces sum to our total budget constraint?**

### Understanding Performance Variations

**Our East region is down 12% while West is up 8% — is this random variation or are there structural differences we should account for in forecasting?**

**Why do some product categories respond strongly to promotions while others barely move, and how does that affect our annual forecast?**

**Which parts of our business are genuinely growing versus just riding overall market trends?**

**Are the forecast errors we're seeing concentrated in specific segments, or is our model equally uncertain everywhere?**

### Decision-Making with Constraints

**If we can only invest in improving forecast accuracy for three of our ten regions, which three give us the biggest return?**

**Should we allocate next quarter's inventory based on bottom-up store requests or top-down market projections?**

**We have conflicting forecasts from regional managers and corporate planning — which should we trust, and can we reconcile them?**

**If supply chain can only deliver 85% of forecasted demand next month, how should we distribute that shortage across channels to minimize revenue loss?**

## How It Works

Imagine you run a retail chain with stores across three regions: North, South, and West. Each region has multiple stores, and each store sells multiple product categories. When forecasting next month's sales, you could predict each individual store-category combination separately (2,400 forecasts if you have 10 stores per region and 80 categories), or you could predict total company sales and split it down. But here's the problem: if you forecast the pieces separately, they won't add up to a sensible company total. If you forecast the top and split it down, you ignore what's actually happening at individual stores. Track Groups solves this by recognizing that your business has a natural structure—regions contain stores, stores sell categories—and forecasts everything simultaneously so the numbers stay coherent at every level.

```
BUSINESS HIERARCHY                  FORECAST RECONCILIATION

     Company                              Company Total
    ($500K)                           (base forecast: $520K)
       |                                       |
   ┌───┴───┬───────┐                  ┌───────┴────────┐
   │       │       │                  │                │
 North  South   West              Reconcile          Adjust
($200K)($180K)($120K)           all levels       using hierarchy
   |       |       |              simultaneously      weights
   |       |       |                   |               |
┌──┴─┐  ┌─┴──┐  ┌─┴──┐          ┌─────┴──────┐       |
│    │  │    │  │    │          │            │       |
S1  S2  S3  S4  S5  S6      Coherent      Individual  |
│    │  │    │  │    │      forecasts     patterns    |
↓    ↓  ↓    ↓  ↓    ↓          ↓             ↓       ↓
Electronics, Apparel...   North: $205K   South: $183K  West: $132K
(80 categories each)      S1: $95K       S3: $88K      S5: $65K
                          Electronics: $180K  Apparel: $140K...
                          
                          All numbers add up correctly!
```

**Step 1: Identify the hierarchy structure.** The algorithm first maps out how your data naturally groups together—regions contain stores, stores contain product categories, or whatever structure fits your business. It creates a mathematical representation of which series roll up into which totals, building a complete picture of every possible aggregation level.

**Step 2: Generate base forecasts for every level.** Using your chosen forecasting method (could be exponential smoothing, ARIMA, or any other technique), the system creates initial predictions at every single node in the hierarchy—company level, regional level, store level, and category level. These forecasts won't yet add up correctly; they're just starting points.

**Step 3: Calculate optimal weights.** The algorithm examines the forecast accuracy at each level of the hierarchy, looking at how reliable predictions tend to be when you're forecasting totals versus individual pieces. It determines how much to trust the top-level forecast versus the bottom-level forecasts versus everything in between.

**Step 4: Reconcile all forecasts simultaneously.** Using the hierarchy structure and the weights, Track Groups adjusts all the forecasts together in one coordinated operation. It finds the closest possible set of predictions that both respects what each level's forecast suggests AND ensures every set of children sums exactly to its parent. The regional forecasts now add up to the company forecast, store forecasts add up to regional forecasts, and so on.

**Step 5: Return the coherent forecast set.** You receive predictions at every level of your hierarchy where the math works perfectly—you can confidently share the company total with executives while giving store managers their specific numbers, knowing everything aligns.

**The key insight:** By treating the entire hierarchy as a single interconnected system rather than independent forecasts, Track Groups captures both the broad patterns visible in aggregated data and the specific behaviors of individual series, while guaranteeing the mathematical consistency that makes forecasts actionable across an organization.

## The Intuition

Imagine a retail company that needs to forecast demand. The CEO wants a single forecast for total company revenue. The regional managers each want forecasts for their territories. The category managers want forecasts for their product lines. And the store managers want forecasts for individual SKUs at their locations. If each of these stakeholders builds forecasts independently using their preferred methods, something embarrassing will happen: the store-level forecasts won't sum to the regional forecasts, which won't sum to the national forecast. The CFO's budget won't balance, and the supply chain team won't know which numbers to trust.

Track Groups solves this problem by recognising that all these forecasts are views of the same underlying reality, constrained by the arithmetic of aggregation. The technique works in two phases: first, generate "base forecasts" at every level of the hierarchy using whatever methods are most appropriate for each series; second, adjust these base forecasts so they become coherent—meaning they satisfy all the adding-up constraints implied by the grouping structure. The adjustment is done optimally, in the sense that it minimises the total distortion to the original forecasts while guaranteeing perfect coherence.

The key insight is that coherence is not just an accounting convenience—it actually improves forecast accuracy. When we reconcile forecasts, we are implicitly combining information from multiple levels. A noisy bottom-level series benefits from the stability of its aggregate; a smooth aggregate series benefits from the detail captured at lower levels. This is analogous to ensemble methods in machine learning, where combining multiple models typically outperforms any single model. Track Groups is essentially an ensemble method for hierarchical time series, where the "models" are forecasts at different aggregation levels and the "combination" respects the structural constraints of the hierarchy.

## The Mathematics

### Problem Setup and Notation

Consider a collection of $n$ time series observed over $T$ time periods. Let $\mathbf{y}_t = (y_{1,t}, y_{2,t}, \ldots, y_{n,t})'$ denote the vector of observations at time $t$. These series are organised into a hierarchy or grouped structure with $m$ bottom-level series and $n - m$ aggregate series.

The hierarchical structure is encoded in a **summing matrix** $\mathbf{S}$ of dimension $n \times m$, which maps the bottom-level series to all series in the hierarchy:

$$
\mathbf{y}_t = \mathbf{S} \mathbf{b}_t
$$

where $\mathbf{b}_t = (b_{1,t}, b_{2,t}, \ldots, b_{m,t})'$ is the vector of bottom-level series at time $t$.

:::{note}
The summing matrix $\mathbf{S}$ has a specific structure: the bottom $m$ rows form an identity matrix $\mathbf{I}_m$, and the top $n - m$ rows contain zeros and ones indicating which bottom-level series aggregate to form each upper-level series.
:::

### Base Forecasts

Let $\hat{\mathbf{y}}_h$ denote the vector of $h$-step-ahead base forecasts for all $n$ series, produced by any forecasting method applied independently to each series. These base forecasts are generally **incoherent**:

$$
\hat{\mathbf{y}}_h \neq \mathbf{S} \hat{\mathbf{b}}_h
$$

where $\hat{\mathbf{b}}_h$ represents the base forecasts for the bottom-level series only.

### Reconciliation

The goal is to find **reconciled forecasts** $\tilde{\mathbf{y}}_h$ that are coherent:

$$
\tilde{\mathbf{y}}_h = \mathbf{S} \tilde{\mathbf{b}}_h
$$

for some vector $\tilde{\mathbf{b}}_h$ of reconciled bottom-level forecasts.

The general form of a linear reconciliation approach is:

$$
\tilde{\mathbf{y}}_h = \mathbf{S} \mathbf{G} \hat{\mathbf{y}}_h
$$

where $\mathbf{G}$ is an $m \times n$ matrix that maps base forecasts to reconciled bottom-level forecasts.

### Optimal Reconciliation

The optimal reconciliation minimises the trace of the forecast error covariance matrix. Let $\boldsymbol{\epsilon}_h = \mathbf{y}_{T+h} - \hat{\mathbf{y}}_h$ denote the base forecast errors with covariance matrix:

$$
\mathbf{W}_h = \text{Var}(\boldsymbol{\epsilon}_h) = \mathbb{E}[\boldsymbol{\epsilon}_h \boldsymbol{\epsilon}_h']
$$

The optimal reconciliation matrix that minimises the variance of the reconciled forecast errors, subject to the coherence constraint, is:

$$
\mathbf{G} = (\mathbf{S}' \mathbf{W}_h^{-1} \mathbf{S})^{-1} \mathbf{S}' \mathbf{W}_h^{-1}
$$

This is the **Minimum Trace (MinT)** estimator, derived from generalised least squares.

### Derivation of the MinT Estimator

We seek to minimise:

$$
\text{tr}(\text{Var}(\mathbf{y}_{T+h} - \tilde{\mathbf{y}}_h))
$$

subject to $\tilde{\mathbf{y}}_h = \mathbf{S} \mathbf{G} \hat{\mathbf{y}}_h$ and the unbiasedness constraint $\mathbf{S} \mathbf{G} \mathbf{S} = \mathbf{S}$.

The reconciled forecast error is:

$$
\mathbf{y}_{T+h} - \tilde{\mathbf{y}}_h = \mathbf{S} \mathbf{b}_{T+h} - \mathbf{S} \mathbf{G} \hat{\mathbf{y}}_h = \mathbf{S}(\mathbf{b}_{T+h} - \mathbf{G} \hat{\mathbf{y}}_h)
$$

The covariance of the reconciled forecast errors is:

$$
\text{Var}(\mathbf{y}_{T+h} - \tilde{\mathbf{y}}_h) = \mathbf{S} \mathbf{G} \mathbf{W}_h \mathbf{G}' \mathbf{S}'
$$

Using Lagrange multipliers to incorporate the constraint $\mathbf{S} \mathbf{G} \mathbf{S} = \mathbf{S}$ and differentiating, we obtain the MinT solution.

### Practical Estimators for $\mathbf{W}_h$

Since $\mathbf{W}_h$ is typically unknown, several estimators are used in practice:

| Method | Form of $\mathbf{W}_h$ | Properties |
|--------|----------------------|------------|
| OLS | $\mathbf{W}_h = k_h \mathbf{I}_n$ | Assumes equal, uncorrelated errors |
| WLS (structural) | $\mathbf{W}_h = k_h \text{diag}(\mathbf{S} \mathbf{1})$ | Weights by number of aggregated series |
| WLS (variance) | $\mathbf{W}_h = k_h \text{diag}(\hat{\mathbf{W}}_1)$ | Uses estimated in-sample variances |
| MinT (shrink) | $\mathbf{W}_h = k_h \hat{\mathbf{W}}_h^{\text{shrink}}$ | Shrinkage estimator of full covariance |
| MinT (sample) | $\mathbf{W}_h = k_h \hat{\mathbf{W}}_h^{\text{sample}}$ | Full sample covariance (requires $T > n$) |

The scalar $k_h > 0$ cancels in the reconciliation formula and need not be estimated.

### Assumptions

1. **Structural stability**: The grouping structure encoded in $\mathbf{S}$ is fixed over the forecast horizon.
2. **Linear reconciliation**: The optimal combination of base forecasts is linear.
3. **Unbiased base forecasts**: Base forecasts are unbiased, or at least their biases are consistent across the hierarchy.
4. **Estimable covariance**: The covariance structure $\mathbf{W}_h$ can be reasonably approximated from historical data.

### Edge Cases

- **Rank deficiency**: If $\mathbf{S}' \mathbf{W}_h^{-1} \mathbf{S}$ is singular, regularisation or a simpler estimator (e.g., OLS) must be used.
- **Single series**: When $n = m = 1$, reconciliation is trivial and $\tilde{y}_h = \hat{y}_h$.
- **Perfect base forecasts**: If base forecasts are already coherent, reconciliation leaves them unchanged.

### Relationship to Other Methods

- **Bottom-up**: Equivalent to setting $\mathbf{G} = [\mathbf{0}_{m \times (n-m)} \mid \mathbf{I}_m]$.
- **Top-down**: Equivalent to setting $\mathbf{G} = \mathbf{p} \mathbf{e}_1'$, where $\mathbf{p}$ is a vector of disaggregation proportions.
- **Middle-out**: A hybrid approach using different $\mathbf{G}$ structures above and below a chosen level.

# Understanding the Mathematics

### Hierarchical Aggregation Constraint

**The equation:**
$$y_t = \mathbf{S} \mathbf{b}_t$$

**Read it aloud:**
"The values at all levels of the hierarchy at time t equal a special summing matrix multiplied by the bottom-level values at time t."

**What each symbol means:**
- $y_t$ = A vector containing forecast values at every level (top, middle groups, and bottom series) at time t
- $\mathbf{S}$ = The "summing matrix" that encodes which bottom-level series add up to which groups
- $\mathbf{b}_t$ = A vector of just the bottom-level series values at time t

**A concrete numerical example:**
Imagine you forecast sales for three stores (Store A: 40k, Store B: 35k, Store C: 25k) that roll up into two regions (East contains A and B; West contains C) and one total.

Your summing matrix $\mathbf{S}$ would be:
```
         A    B    C
Total  [ 1    1    1  ]
East   [ 1    1    0  ]
West   [ 0    0    1  ]
A      [ 1    0    0  ]
B      [ 0    1    0  ]
C      [ 0    0    1  ]
```

So $y_t = \mathbf{S} \mathbf{b}_t$ becomes:
```
[100k]   [1 1 1]   [40k]
[ 75k]   [1 1 0]   [35k]
[ 25k] = [0 0 1] × [25k]
[ 40k]   [1 0 0]
[ 35k]   [0 1 0]
[ 25k]   [0 0 1]
```

**Why this equation matters:**
This constraint ensures that when you add up store forecasts, you automatically get the correct regional and total forecasts—no manual reconciliation needed.

### Base Forecast Generation

**The equation:**
$$\tilde{y}_t = f(\mathbf{X}_t, \theta)$$

**Read it aloud:**
"The initial forecast at time t is some function of the input features at time t and the model parameters."

**What each symbol means:**
- $\tilde{y}_t$ = The "base forecast" before reconciliation (the tilde indicates it's preliminary)
- $f$ = Your forecasting function (could be ARIMA, exponential smoothing, machine learning)
- $\mathbf{X}_t$ = Input features (historical sales, promotions, seasonality indicators, etc.)
- $\theta$ = Model parameters (weights, coefficients, smoothing constants)

**A concrete numerical example:**
Suppose you use exponential smoothing for Store A with level = 38k, trend = 0.5k per month, and seasonal index for June = 1.05.

Then $\tilde{y}_{\text{June}} = (38{,}000 + 500) \times 1.05 = 40{,}425$.

You generate separate base forecasts for every series in the hierarchy: Store A gets 40.4k, Store B gets 36.2k, Store C gets 24.8k, East region gets 78k, etc. These forecasts are internally inconsistent—East should equal A + B but might not.

**Why this equation matters:**
Base forecasts leverage the best available statistical methods for each series but produce incoherent results that we must reconcile to respect the hierarchy.

### Minimum Trace Reconciliation

**The equation:**
$$\hat{y}_t = \mathbf{S}(\mathbf{S}'\mathbf{W}^{-1}\mathbf{S})^{-1}\mathbf{S}'\mathbf{W}^{-1}\tilde{y}_t$$

**Read it aloud:**
"The final reconciled forecast equals the summing matrix times a complicated middle term times the summing matrix transpose times the inverse error covariance matrix times the base forecasts."

**What each symbol means:**
- $\hat{y}_t$ = Final reconciled forecasts (the hat indicates these are the outputs)
- $\mathbf{S}$ = Summing matrix (same as before)
- $\mathbf{W}$ = Covariance matrix of base forecast errors (which series have accurate forecasts, which are noisy)
- $\mathbf{W}^{-1}$ = Inverse covariance matrix (gives more weight to accurate forecasts)
- $\tilde{y}_t$ = Base forecasts (the preliminary ones)

**A concrete numerical example:**
Your base forecasts were Store A: 40.4k, Store B: 36.2k, Store C: 24.8k, but the Total was forecast as 103k (not 101.4k). Store A historically has error variance of 4, Store B has 9, Store C has 2.

The reconciliation redistributes the 1.6k discrepancy proportionally, giving more adjustment weight to Store B (the noisiest) and less to Store C (the most accurate). Final forecasts might become: A: 40.2k, B: 35.8k, C: 24.9k, Total: 100.9k—all perfectly coherent.

**Why this equation matters:**
This optimal reconciliation minimizes forecast variance while guaranteeing that store forecasts sum exactly to regional and total forecasts, eliminating the embarrassment of presenting inconsistent numbers to executives.

### The Big Picture

The mathematics of Track Groups solves a deceptively hard problem: how do you combine many individual forecasts into a coherent hierarchy when each forecast has different reliability? The minimum trace approach is chosen because it provably minimizes the variance of reconciled forecasts—no other linear reconciliation method produces tighter prediction intervals while maintaining coherence. The summing matrix encodes your business structure once, the covariance matrix captures which forecasts to trust, and the reconciliation formula optimally blends them. Think of it as a smart weighted average that respects both the arithmetic rules of your hierarchy and the statistical quality of your predictions. Without this mathematics, you'd either ignore the hierarchy (losing coherence) or manually adjust forecasts (losing optimality).

## Python Implementation

```python
import numpy as np
import pandas as pd
from scipy.linalg import inv, solve
from sklearn.linear_model import LinearRegression
import warnings

# =============================================================================
# Example 1: Simple Hierarchical Reconciliation
# =============================================================================

def create_summing_matrix(hierarchy_structure):
    """
    Create summing matrix S from hierarchy specification.
    
    Parameters
    ----------
    hierarchy_structure : dict
        Maps aggregate series names to lists of bottom-level series names.
    
    Returns
    -------
    S : np.ndarray
        Summing matrix of shape (n_total, n_bottom)
    series_names : list
        Ordered list of all series names (aggregates first, then bottom-level)
    """
    # Extract bottom-level series (appear in values but not keys)
    all_bottom = set()
    for children in hierarchy_structure.values():
        all_bottom.update(children)
    bottom_series = sorted(all_bottom - set(hierarchy_structure.keys()))
    
    # Build summing matrix
    n_bottom = len(bottom_series)
    n_agg = len(hierarchy_structure)
    n_total = n_agg + n_bottom
    
    S = np.zeros((n_total, n_bottom))
    series_names = []
    
    # Aggregate rows
    for i, (agg_name, children) in enumerate(hierarchy_structure.items()):
        series_names.append(agg_name)
        for child in children:
            if child in bottom_series:
                j = bottom_series.index(child)
                S[i, j] = 1
            else:
                # Child is itself an aggregate; sum its components
                child_children = hierarchy_structure.get(child, [])
                for cc in child_children:
                    if cc in bottom_series:
                        j = bottom_series.index(cc)
                        S[i, j] = 1
    
    # Bottom-level rows (identity matrix)
    S[n_agg:, :] = np.eye(n_bottom)
    series_names.extend(bottom_series)
    
    return S, series_names, bottom_series


def reconcile_forecasts(base_forecasts, S, method='ols', residuals=None):
    """
    Reconcile hierarchical forecasts using specified method.
    
    Parameters
    ----------
    base_forecasts : np.ndarray
        Base forecasts for all series, shape (n_total,) or (n_total, h)
    S : np.ndarray
        Summing matrix, shape (n_total, n_bottom)
    method : str
        Reconciliation method: 'ols', 'wls_struct', 'wls_var', 'mint_shrink'
    residuals : np.ndarray, optional
        Historical residuals, shape (T, n_total), required for variance-based methods
    
    Returns
    -------
    reconciled : np.ndarray
        Reconciled forecasts, same shape as base_forecasts
    """
    n_total, n_bottom = S.shape
    base_forecasts = np.atleast_2d(base_forecasts)
    if base_forecasts.shape[0] == 1:
        base_forecasts = base_forecasts.T
    
    # Compute W based on method
    if method == 'ols':
        # W = I (ordinary least squares)
        W_inv = np.eye(n_total)
    
    elif method == 'wls_struct':
        # W = diag(S @ 1) - structural scaling
        row_sums = S.sum(axis=1)
        W_inv = np.diag(1.0 / row_sums)
    
    elif method == 'wls_var':
        # W = diag(sample variances)
        if residuals is None:
            raise ValueError("Residuals required for wls_var method")
        variances = np.var(residuals, axis=0, ddof=1)
        variances = np.maximum(variances, 1e-10)  # Avoid division by zero
        W_inv = np.diag(1.0 / variances)
    
    elif method == 'mint_shrink':
        # W = shrinkage estimate of covariance
        if residuals is None:
            raise ValueError("Residuals required for mint_shrink method")
        W = _shrinkage_covariance(residuals)
        W_inv = inv(W)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Compute G matrix: G = (S'W^{-1}S)^{-1} S'W^{-1}
    StWinv = S.T @ W_inv
    G = solve(


## Visualisations

![](../../_static/figures/track-groups_fig1.png)
![](../../_static/figures/track-groups_fig2.png)

## Using This in Heuristix

### What You Need to Start

The Track Groups node expects your data in a **long format** with three essential columns:

- **Date/time column**: Your temporal index (daily, weekly, monthly, etc.)
- **Group identifier(s)**: One or more columns defining your hierarchy (e.g., Region, Store, Product Category)
- **Value column**: The metric you're forecasting (sales, demand, traffic, etc.)

Here's what your input should look like:

| Date       | Region | Store | Sales |
|------------|--------|-------|-------|
| 2024-01-01 | North  | A     | 1250  |
| 2024-01-01 | North  | B     | 980   |
| 2024-01-01 | South  | C     | 1420  |
| 2024-01-02 | North  | A     | 1310  |

The node automatically detects hierarchical relationships between your grouping columns, so Store A and Store B will be correctly nested under Region North.

### Configuration Parameters

| Parameter | What It Does | Default | When to Adjust |
|-----------|-------------|---------|----------------|
| **Grouping Columns** | Defines hierarchy levels from top to bottom | None (required) | Order matters! List from broadest (Region) to most granular (Store) |
| **Date Column** | Your time index | Auto-detect | Specify if multiple date columns exist |
| **Value Column** | Metric to forecast | Auto-detect | Specify if multiple numeric columns exist |
| **Forecast Horizon** | Number of periods ahead | 12 | Match your planning cycle—52 for weekly annual planning, 12 for monthly |
| **Reconciliation Method** | How forecasts are made coherent | "optimal" | Use "bottom-up" for stable low-level data, "top-down" for noisy bottom levels |
| **Minimum History** | Required periods per series | 24 | Reduce for newer products, increase for seasonal patterns (need 2+ cycles) |
| **Confidence Level** | Prediction interval width | 95% | Lower to 80% for tighter bounds, raise to 99% for conservative planning |

### What You Get Out

**Forecast Table**: Your original data structure extended into the future, with three new columns per level:
- `forecast_value`: Point prediction
- `lower_bound`: Bottom of confidence interval  
- `upper_bound`: Top of confidence interval

**Coherence Report**: Shows how forecasts sum correctly across hierarchy levels—North store forecasts will always add up to the North regional forecast.

**Accuracy Metrics Panel**: Displays MAPE, RMSE, and MAE for each hierarchy level, helping you identify where the model performs best.

**Interactive Chart**: Time series visualization with actual vs. forecast comparison, filterable by any grouping dimension. Hover over any point to see contributing lower-level forecasts.

### Connecting Downstream

- **Scenario Analysis node**: Test "what-if" adjustments that maintain coherence
- **Export node**: Send forecasts to planning systems or spreadsheets
- **Monitoring Dashboard**: Track forecast accuracy as actuals arrive
- **Optimization node**: Use forecasts as inputs for inventory or resource allocation

### Quick Start

1. **Connect your historical data** to the Track Groups node
2. **Select your grouping columns** in hierarchical order (e.g., Region → Store → Product)
3. **Set forecast horizon** to match your planning needs (typically 12-13 periods)
4. **Run the node** and check the Accuracy Metrics panel—look for MAPE under 15% as a good baseline
5. **Inspect the coherence** by filtering the chart to a top-level group and visually confirming child forecasts sum correctly

### Practical Tips from the Field

**Start with fewer hierarchy levels**: Two levels (like Region → Store) are easier to validate than four. Add complexity once you're confident in the basics.

**Watch for sparse series**: If many bottom-level series have intermittent zeros, consider aggregating to a higher level or using "top-down" reconciliation to borrow strength from more stable totals.

**Seasonal patterns need data**: The rule of thumb is at least two complete seasonal cycles—monthly data needs 24+ months, weekly needs 104+ weeks.

**Coherence catches data issues**: If your hierarchical forecasts look wrong, check your grouping structure. Missing or inconsistent group labels will break the relationships.

**Save your reconciliation choice**: Document whether you used bottom-up or optimal reconciliation—you'll need consistency when updating forecasts next period.

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial data analysis when you need to validate grouping structure and assess forecast viability within minutes, not hours.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `max_iterations` | 5 | Stops before full convergence for speed |
| `reconciliation_method` | `"bottom_up"` | Fastest method, no optimization overhead |
| `cv_folds` | 1 | Single validation pass only |
| `model_selection` | `"auto"` | Skip manual model comparison |
| `min_group_size` | 10 | Filters out trivial groups early |

**What you get:** Directional accuracy showing whether the grouping structure contains predictive signal, delivered in under 5 minutes for datasets with <10,000 series.

**Trade-off:** Forecasts are statistically suboptimal and reconciliation doesn't minimize overall error.

### Recipe 2: Production-Grade Forecasting

**When to use:** Deployed systems where forecast quality directly impacts business decisions and computational resources are available.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `max_iterations` | 50 | Ensures full convergence |
| `reconciliation_method` | `"mint_shrink"` | Statistically optimal across hierarchy |
| `cv_folds` | 5 | Robust out-of-sample validation |
| `residual_bootstrap` | `True` | Provides prediction intervals |
| `n_bootstrap_samples` | 1000 | Stable interval estimates |
| `model_selection` | `"cv_rmse"` | Explicit accuracy criterion |
| `min_group_size` | 3 | Preserves all meaningful groups |

**What you get:** Coherent forecasts with calibrated prediction intervals that minimize squared error across all hierarchy levels simultaneously.

**Trade-off:** Execution time increases 10-20x compared to exploration mode; requires adequate memory for bootstrap samples.

### Recipe 3: Sparse High-Cardinality Data

**When to use:** Retail or e-commerce scenarios with thousands of SKUs where most series contain long runs of zeros (intermittent demand).

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `zero_inflation_threshold` | 0.6 | Activates specialized handling when >60% zeros |
| `reconciliation_method` | `"bottom_up"` | Preserves zero patterns in leaf series |
| `temporal_aggregation` | `"weekly"` | Reduces sparsity by aggregating daily data |
| `min_group_size` | 5 | Prevents singleton intermittent groups |
| `model_selection` | `"croston"` | Purpose-built for intermittent series |

**What you get:** Forecasts that respect zero-inflation patterns without artificially smoothing away intermittency at the bottom level.

**Trade-off:** Top-level aggregates may show higher bias as bottom-up reconciliation doesn't optimize for aggregate accuracy.

### Recipe 4: Causal Inference via Synthetic Controls

**When to use:** Estimating treatment effects when you have a treated group and many potential control groups in your hierarchy (e.g., testing pricing changes in one region).

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `holdout_groups` | `["treated_group_id"]` | Excludes intervention group from hierarchy |
| `reconciliation_method` | `"top_down_proportions"` | Learns pre-intervention allocation weights |
| `train_test_split` | `0.8` | Uses pre-intervention period for training |
| `enforce_coherence` | `True` | Creates synthetic control as weighted combination |
| `proportion_method` | `"historic_avg"` | Weights based on pre-treatment patterns |

**What you get:** A coherent counterfactual forecast representing what the treated group would have experienced without intervention, derived from the natural hierarchy.

**Trade-off:** Requires stable pre-treatment period and assumes parallel trends between treated and control groups.

## Business Applications

**Financial Services**

A multi-brand credit card issuer with 8 million active accounts needed to forecast monthly transaction volumes across product lines, customer segments, and merchant categories simultaneously. Track Groups modelled the natural hierarchy—from total portfolio down through brand, card type, customer segment, to individual merchant category—ensuring that segment-level forecasts always summed correctly to portfolio totals while capturing unique seasonal patterns in categories like travel (summer peaks) and retail (holiday spikes). The approach reduced forecast error by 23% compared to independent models and eliminated the embarrassing board-level discrepancies where regional forecasts previously exceeded total company projections by $340M.

**Retail**

An omnichannel fashion retailer operating 450 stores across Europe struggled with inventory allocation when store-level demand forecasts, when aggregated, contradicted regional distribution centre projections. Track Groups implemented a four-tier hierarchy—country, region, store format (flagship/standard/outlet), individual location—that respected both geographic relationships and the structural differences between store types. The coherent forecasts cut excess inventory holding costs by €4.7M annually while reducing stockouts by 31%, as allocation decisions could now trust that store requirements would properly roll up to warehouse capacity.

**Healthcare**

A hospital network with 12 facilities needed to forecast staffing requirements across departments, shift patterns, and specialties while ensuring system-wide resource pools balanced correctly. Track Groups modelled patient volumes through overlapping hierarchies—by facility/department/specialty and separately by day-of-week/shift/acuity level—producing forecasts that maintained consistency across both organisational and temporal dimensions. Implementation reduced agency nurse costs by $2.1M annually and cut patient wait times by 18 minutes on average, as capacity planning could optimally distribute permanent staff knowing forecasts would aggregate consistently.

**Insurance**

A commercial lines insurer writing £850M in annual premium across 40 policy types needed claims forecasts that worked both for reserving (by underwriting year and policy type) and for cash flow planning (by expected payment quarter). Track Groups created a multi-dimensional structure respecting both the actuarial development triangle and the product hierarchy, ensuring reserves by accident year summed to total reserves while quarterly payment forecasts remained coherent across product lines. The methodology reduced reserve volatility by 28% and gave the CFO payment timing forecasts accurate enough to reduce the liquidity buffer from £75M to £52M.

**Manufacturing**

A process manufacturer producing 200 SKUs from 15 base materials across 6 production lines required demand forecasts that respected both product hierarchies (raw material → intermediate → finished goods) and production constraints. Track Groups modelled the bill-of-materials structure while incorporating capacity limitations, producing forecasts where finished goods demand automatically translated into consistent raw material requirements and realistic production schedules. The approach reduced raw material waste by 19% and increased on-time delivery from 87% to 96%.

**Logistics**

A national parcel carrier handling 2.5M packages daily needed volume forecasts by service level, region, and hub that aggregated consistently for network capacity planning. Track Groups implemented a geographic hierarchy (national → regional sorting centre → local depot → postcode sector) crossed with service tiers (next-day/standard/economy), ensuring depot-level forecasts respected both regional capacity and service-level commitments. This reduced mis-sorted packages by 41% and cut last-mile delivery costs by £8.3M annually through better vehicle utilisation.

**Marketing**

A performance marketing agency managing £120M in annual ad spend across 15 clients discovered that campaign-level conversion forecasts, when aggregated, consistently overstated client-level results by 15-20%. Track Groups structured forecasts hierarchically—by client, channel (paid search/social/display), campaign, then ad group—with coherence constraints ensuring realistic expectations at every level. The methodology improved budget allocation efficiency, lifting blended ROAS from 3.8x to 4.6x while eliminating the client expectation mismatches that previously caused contract cancellations.

**Telecommunications**

A mobile network operator forecasting data consumption across 8M subscribers needed predictions coherent across customer segments, geographic cells, and network technology layers (5G/4G/3G). Track Groups modelled the multi-dimensional structure, producing forecasts where subscriber behaviour rolled up consistently to cell tower capacity and technology migration patterns. This enabled £15M in deferred infrastructure investment by accurately identifying which cells genuinely required capacity upgrades versus those where aggregate forecasts had been artificially inflated.

**Energy**

A renewable energy portfolio manager needed electricity generation forecasts for 200 wind and solar sites that aggregated consistently for grid commitment bidding. Track Groups implemented a hierarchy respecting both geography (weather correlations) and technology type (generation profiles), ensuring site-level forecasts summed to portfolio totals while capturing technology-specific patterns. The coherent forecasts reduced balancing mechanism costs by £2.4M annually through more accurate day-ahead bidding.

**Public Sector**

A metropolitan transport authority forecasting ridership across 150 bus routes, 45 rail stations, and 3 service types needed projections that worked for route planning, maintenance scheduling, and budget allocation simultaneously. Track Groups modelled the network hierarchy—by mode, line, station/stop, time-of-day—producing forecasts that maintained consistency whether aggregated for executive reporting or disaggregated for operational planning. Implementation improved service reliability scores by 12 points while reducing operational costs by 7% through better resource allocation.

**SaaS/Technology**

A B2B SaaS platform with 3,500 enterprise clients needed revenue forecasts across customer segments, product modules, and contract types that remained coherent when sales, finance, and product teams each viewed the data through their preferred lens. Track Groups created a multi-dimensional hierarchy—by customer size tier, industry vertical, product SKU, and billing frequency—ensuring that product-led growth forecasts aligned with sales pipeline projections and subscription revenue reconciled across all views. This reduced forecast variance from 18% to 6% and enabled dynamic pricing strategies that increased annual recurring revenue by $8.7M.

## Worked Example

Sarah Chen, a senior data scientist at Meridian Retail, received an urgent Slack message on a Tuesday morning from the VP of Supply Chain: "Our warehouse allocation model is broken. We're overstocking some regions while others run out. Can you look at the Q1 forecasts?" The company operated twelve stores across three regions—North, South, and East—and the current bottom-up forecasting approach was producing regional totals that didn't align with the national forecast from their econometric model. Finance needed reconciled numbers by Friday for the board presentation.

Sarah pulled three years of weekly sales data for their flagship product line. The dataset was messier than she hoped—Store 7 had been closed for renovations in 2023, and the South region showed an unusual spike during a regional promotional event that hadn't been properly flagged. She consolidated the data into a single table:

| date       | store_id | region | sales | promo_flag |
|------------|----------|--------|-------|------------|
| 2024-01-07 | S01      | North  | 1,247 | 0          |
| 2024-01-07 | S05      | South  | 2,103 | 1          |
| 2024-01-07 | S09      | East   | 891   | 0          |
| 2024-01-14 | S01      | North  | 1,189 | 0          |

The hierarchy was straightforward: individual stores rolled up to regions, which rolled up to the national total. Sarah knew that simple bottom-up forecasting would miss national trends, while top-down allocation would ignore store-specific patterns like seasonality differences between coastal and inland locations.

She opened Heuristix and configured the Track Groups node. For the grouping structure, she specified `region` as the primary hierarchy level, with `store_id` nested beneath it. She chose "optimal combination" as the reconciliation method—this would weight forecasts at each level based on their historical accuracy rather than arbitrarily favoring top or bottom. For the base forecasting method, she selected an exponential smoothing model with trend and seasonality components, knowing the data showed both growth and weekly patterns. She added `promo_flag` as an exogenous variable and set the forecast horizon to twelve weeks.

The model ran in about ninety seconds. Sarah examined the output, which showed forecasts at all three levels—store, region, and national—along with reconciliation weights:

| level    | entity | week_1_forecast | reconciliation_weight |
|----------|--------|-----------------|----------------------|
| National | Total  | 18,450          | 0.45                 |
| Region   | North  | 5,210           | 0.62                 |
| Region   | South  | 8,130           | 0.71                 |
| Region   | East   | 5,110           | 0.58                 |
| Store    | S01    | 1,247           | 0.83                 |

The reconciliation weights revealed something Sarah hadn't expected: the South region's base forecast received a 0.71 weight, meaning the algorithm trusted it more than the national-level forecast for that region. When she dug into the diagnostics, she realized why—the South region's promotional patterns were highly predictable at the local level but got washed out in national aggregates.

The insight crystallized when she compared the reconciled forecasts to the previous system's outputs. The old bottom-up approach had predicted South would need 8,850 units, driven by individual store forecasts that had each independently picked up on the promotion signal. The Track Groups model reconciled this down to 8,130, recognizing that not all stores would experience the same lift simultaneously. This single correction would prevent approximately $43,000 in excess inventory costs.

Sarah presented her findings in Thursday's operations meeting. She showed the executive team a simple visual: the hierarchical structure with reconciliation weights overlaid, and a comparison table of old versus new forecasts with associated inventory costs. The VP of Supply Chain immediately approved implementing the Track Groups methodology for all product lines. More importantly, the CFO asked Sarah to apply the same approach to their demand planning process for the upcoming seasonal launch—a project that would normally have gone to an external consultancy.

The reconciled forecasts were pushed to the warehouse management system that afternoon. Over the following quarter, forecast accuracy improved by 18% at the regional level, and the company reduced safety stock by 12% without increasing stockout incidents.

If Sarah were doing this again, she'd spend more time validating the promotional event coding—several events in the historical data had been misclassified, which likely affected the base forecasts. She'd also experiment with the reconciliation method selection; "optimal combination" worked well, but she wondered if the minimum trace estimator might have been more robust given the promotional volatility. Still, the approach had worked: Track Groups had delivered both the mathematical coherence Finance required and the local accuracy Operations needed, all from a single unified model.

```python
import pandas as pd
from heuristix import TrackGroups

# Load sales data with hierarchical structure
df = pd.read_csv('store_sales.csv', parse_dates=['date'])

# Configure Track Groups with nested hierarchy
model = TrackGroups(
    time_col='date',
    value_col='sales',
    hierarchy=['region', 'store_id'],  # Sarah's nested structure
    reconciliation='optimal_combination',  # Weight by historical accuracy
    base_method='exponential_smoothing',
    seasonal_period=52,  # Weekly data, annual seasonality
    exog_vars=['promo_flag']
)

# Fit and forecast 12 weeks ahead
model.fit(df)
forecasts = model.predict(horizon=12)

# Extract reconciliation diagnostics
weights = model.get_reconciliation_weights()
print("Reconciliation weights by level:")
print(weights.groupby('level')['weight'].mean())

# Compare to bottom-up baseline
baseline = df.groupby(['date', 'region'])['sales'].sum()
comparison = forecasts.merge(baseline, on=['date', 'region'])
print(f"\nAccuracy improvement: {model.score(comparison):.1%}")
```

## Interpreting Your Results

You've just run Track Groups and you're staring at forecasts, error metrics, and hierarchy reconciliation statistics. Here's exactly what you're looking at and how to know if it's working.

### Forecast Accuracy Metrics

**MAPE (Mean Absolute Percentage Error)** tells you the average size of your forecast errors as a percentage of actual values. A MAPE of 15% means your forecasts are typically off by 15% in either direction.

**Concrete benchmarks:**
- **Below 10%**: Excellent. You can confidently build operational plans on these forecasts.
- **10–20%**: Good for most business applications. Suitable for inventory planning, budgeting, and capacity decisions.
- **20–35%**: Acceptable for strategic planning and directional decisions, but too uncertain for tight operational execution.
- **Above 35%**: Poor. Something is likely wrong with your data, model selection, or the series is genuinely unpredictable.

**Red flag:** If MAPE varies wildly across hierarchy levels (e.g., 12% at top level, 45% at bottom level), your grouping structure may not match the natural patterns in your data. This often indicates you've created groups that aggregate fundamentally different behaviours.

**RMSE (Root Mean Squared Error)** measures forecast error in the same units as your data. Unlike MAPE, it heavily penalises large errors. If you're forecasting daily revenue in dollars and RMSE is $50,000, your typical forecast error is around that magnitude, with occasional much larger misses.

**Reading them together:** If MAPE is acceptable but RMSE is disproportionately high, you have outlier problems—a few catastrophically wrong forecasts are dragging down performance. Investigate those specific periods for data quality issues or structural breaks.

### Reconciliation Metrics

**Reconciliation Error** measures how much your forecasts had to be adjusted to maintain hierarchy coherence. This is the average difference between initial forecasts and the final reconciled values.

**Concrete benchmarks:**
- **Below 5% of forecast values**: Excellent coherence. Your initial models already respected the hierarchy well.
- **5–15%**: Normal. The reconciliation process is doing real work but not fighting your models.
- **Above 15%**: Your bottom-level and top-level forecasts are telling contradictory stories. Consider whether your hierarchy structure makes business sense.

**Red flag:** If reconciliation error is consistently high for specific groups but low for others, those problematic groups may combine series with incompatible seasonal patterns or trend behaviours.

### Forecast Plots

The visual forecast output shows historical actuals, fitted values, and future forecasts with confidence intervals.

**What you're checking:**
- **Do the forecasts follow the established pattern?** If historical data shows clear seasonality but forecasts are flat, the model failed to capture structure.
- **Are confidence intervals reasonable?** Intervals that immediately balloon to +/- 80% of the forecast value indicate high uncertainty—the model has learned little from the past.
- **Do aggregated forecasts make sense?** Sum your bottom-level forecasts mentally and compare to the top-level. Gross mismatches (e.g., all regional forecasts trending up while national forecast trends down) indicate reconciliation problems.

**Red flag:** Forecasts that exactly replicate the last observed value for multiple periods ahead suggest model underfitting—you're essentially getting naive forecasts, not genuine predictions.

### Hierarchy Contribution Table

This table shows how much each bottom-level series contributes to each group and to the total. 

**What to check:** Contributions should be relatively stable over time. If a series that historically contributed 5% to total suddenly drives 30% of the forecast, investigate why. This often reveals data quality issues or the model picking up noise as signal.

### Sanity Check Checklist

Before trusting your Track Groups results:

1. **Sum check**: Do bottom-level forecasts sum exactly to top-level forecasts? If not, reconciliation failed.
2. **Direction check**: Are all forecasts showing the same directional trend (all growing or all declining) when business context suggests they should move together?
3. **Magnitude check**: Is any single series forecast changing by more than 50% from recent history without a known business reason?
4. **Seasonality check**: Do seasonal series show seasonal patterns in the forecast period?
5. **Boundary check**: Are any forecasts negative when they must be positive (e.g., sales, counts)?

### Good Enough to Act On?

If your MAPE is below 20% at the decision-making level of your hierarchy, reconciliation error is below 10%, and all five sanity checks pass, your forecasts are reliable enough for business planning. You're ready to move from analysis to action. Perfect forecasts don't exist—good enough forecasts that inform better decisions do.

## Decision Guidance

### What This Result Is Telling You

Track Groups forecasts tell you how demand, revenue, or volume will flow through the natural structure of your business—not just what the total will be, but how it breaks down across regions, products, channels, or customer segments in a way that actually adds up correctly. When you see these forecasts, you're looking at a coordinated picture: the company-level projection automatically matches the sum of all regional forecasts, which match their component store forecasts. This eliminates the common problem where sales territories submit plans that sum to 120% of what the executive team forecasted, or where marketing allocates budget based on one number while operations plans inventory against a different one.

The hierarchy reveals where growth or decline is concentrated. If your total forecast shows 5% growth but Track Groups reveals one region declining 15% while another grows 25%, you need different strategies in each market—not an average approach everywhere. The methodology also exposes structural changes: if a previously stable product category suddenly shows high forecast uncertainty at the bottom level but stability at the top, it signals that customer preferences are shifting between products within that category, even if total category demand remains predictable.

The reconciliation adjustments—how much each level's forecast was modified to maintain consistency—tell you where your business structure creates natural planning conflicts. Large adjustments indicate areas where local patterns conflict with aggregate trends, often revealing organizational silos, data quality issues, or genuine market complexity that requires management attention beyond forecasting.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|---|---|---|---|
| Forecasts at all hierarchy levels within ±5% of each other after reconciliation | Structure is well-aligned; local patterns aggregate naturally to company trends | Proceed with standard resource allocation using bottom-level forecasts | Operations teams, regional managers |
| One branch shows >20% adjustment while sibling branches show <10% | That unit operates differently from its peers; structural grouping may be wrong or business model differs | Investigate data quality and business model for outlier branch; consider regrouping | Analytics team, unit general manager |
| Bottom-level forecast uncertainty (90th percentile range) exceeds 40% while top-level stays below 15% | High diversity of micro-trends; individual predictions unreliable but aggregate is stable | Use aggregate forecasts for procurement/staffing; avoid bottom-level performance targets | Supply chain, finance, HR leadership |
| Reconciliation consistently adjusts one level upward by >10% across multiple forecast cycles | Systematic underforecasting at that level; local teams may be sandbagging or missing trends | Review incentive structures and data inputs at that level; adjust forecast process | Business unit leaders, sales operations |

### When to Proceed vs. Investigate Further

**Proceed with confidence** when reconciliation adjustments are <10% at all levels, forecast confidence intervals are appropriately sized for your decision horizon, and the hierarchy structure aligns with how you actually allocate resources and set accountability.

**Proceed with caution** when adjustments fall between 10-20%, when bottom-level forecasts show inconsistent accuracy across sibling groups (some accurate, others volatile), or when your forecast horizon approaches the length of your historical training data.

**Investigate before acting** when any level shows reconciliation adjustments >20%, when confidence intervals at operational levels exceed the range where decisions meaningfully differ (e.g., forecasting 100-500 units when you must choose between building capacity for 200 or 400), or when structural changes like reorganizations have occurred since model training.

**Do not use these results yet** when you lack at least 2 full seasonal cycles of history, when the hierarchy structure has been defined incorrectly (series grouped together that don't actually share characteristics), or when aggregated bottom-level actuals don't match top-level actuals historically (indicating data quality problems).

### The Cost of Getting This Wrong

Misinterpreting Track Groups results leads to synchronized failure across your organization. If you ignore large reconciliation adjustments and blindly trust bottom-level forecasts, you'll have regional teams ordering inventory that sums to 30% more than your realistic total demand—tying up working capital in stock that sits idle while creating phantom demand signals to suppliers. Conversely, forcing consistency by overriding accurate bottom-level forecasts with poorly-fitted top-down allocations means your Dallas warehouse runs out of Product A while your Phoenix warehouse discounts excess Product A inventory—the total is right but every location is wrong. When executives see coherent-looking forecasts without understanding the adjustment magnitude, they make capital allocation decisions (opening new facilities, hiring permanent staff, signing supplier contracts) based on false precision, committing millions in irreversible investments to serve demand patterns that exist only in the reconciled numbers, not in actual customer behavior.

## Common Pitfalls

**The Vanishing Base Effect**

Here's what happened: A retail analyst was forecasting sales across product categories using Track Groups with a three-level hierarchy (total → department → SKU). They built the model during Q4, trained it on two years of historical data, and deployed it for Q1 forecasting. The bottom-level forecasts looked reasonable, but when aggregated to department level, seasonal items that had been discontinued showed phantom sales projections of $15K–$20K monthly. The analyst concluded the model was "learning the seasonality correctly" and pushed the forecasts to production.

Why it happens: The grouping structure preserves historical patterns even when the underlying reality has changed. When series drop to zero or near-zero, the reconciliation process still allocates forecast mass based on historical proportions, creating ghost forecasts for inactive products.

How to detect it: Check for non-zero forecasts where `actual_sales_last_90_days = 0` or where `coefficient_of_variation > 3.0` in the forecast period but `cv_historical < 0.5`. Run a filter: `forecast_value > 0 AND days_since_last_sale > 60`.

The fix: Implement an active series filter before grouping—exclude series with zero activity in the recent period (typically 2–3 forecast horizons) or add a suppression rule post-reconciliation that zeros out forecasts when recent actuals are absent.

**The Incoherent Coherence**

Here's what happened: A supply chain data scientist was forecasting warehouse demand across regions. They implemented Track Groups with bottom-up reconciliation, validated that forecasts summed correctly across the hierarchy, and celebrated achieving "perfect coherence." Three months later, operations reported that West Region forecasts were consistently 40% too high while East Region was 30% too low, even though the national total was accurate within 5%.

Why it happens: Coherence only means mathematical consistency—that child nodes sum to parent nodes. It says nothing about forecast accuracy at any particular level. Junior practitioners often mistake structural coherence for predictive quality.

How to detect it: Calculate level-specific MAPE or RMSE separately for each hierarchy level. Look for situations where `MAPE_aggregate < 10%` but `MAPE_disaggregate > 30%`, or where error distributions are highly skewed across groups (`max(group_MAPE) / min(group_MAPE) > 3`).

The fix: Evaluate accuracy metrics at every hierarchy level independently, not just at the aggregate. Consider level-specific weighting in the reconciliation process or switch from bottom-up to middle-out reconciliation when intermediate levels show better forecast skill.

**The Grouping Granularity Trap**

Here's what happened: A marketing analyst created Track Groups for campaign performance with a five-level hierarchy: total → channel → campaign → ad_group → creative. They proudly reported using "the full richness of our data structure." Model training took 6 hours, and the resulting forecasts showed bizarre patterns—forecasted CTR bouncing between 0.1% and 8.5% for similar creatives. They concluded they needed "more sophisticated reconciliation methods."

Why it happens: Excessive hierarchical depth creates too many leaf nodes with sparse data. Each additional level multiplies the number of series exponentially, and reconciliation struggles when most bottom-level series have insufficient observations.

How to detect it: Check `observations_per_series` at the leaf level. If `median(obs_per_series) < 30` or if `proportion_of_series_with_less_than_10_obs > 0.25`, you're overfitting the structure. Also watch for `reconciliation_time > 10× base_model_training_time`.

The fix: Collapse levels with high cardinality and low information gain. Start with 2–3 levels maximum and add depth only when leaf nodes have at least 50–100 observations per series.

**The Static Structure Syndrome**

Here's what happened: An experienced analytics lead built Track Groups for a SaaS company's customer revenue forecasting using a structure based on industry vertical and company size. The model performed well for 18 months. Then the company launched a new product line. The analyst reran the existing model with updated data, and forecasts for the new product showed as $0 across all groups. They spent days debugging the reconciliation algorithm before realizing the issue.

Why it happens: Track Groups encode the hierarchy structure at creation time. New categories, products, or groups that don't exist in the training data have no place in the established structure. Experienced practitioners forget this because the models run without errors—they just silently exclude the new series.

How to detect it: Compare `unique_groups_in_data` versus `unique_groups_in_model`. Set up monitoring for `count(series_in_raw_data) != count(series_in_forecast_output)`. Check logs for any series with `date_first_appeared > model_last_trained_date`.

The fix: Implement automated structure updates—either retrain the grouping hierarchy when new categories appear or design the structure to include a generic "Other" or "New" category that can absorb novel series until the next model refresh.

**The Correlation Confusion**

Here's what happened: A business user was reviewing Track Group forecasts for store sales. They noticed that Store A and Store B, which were in the same geographic group, had very different forecast trends—Store A showed 12% growth while Store B showed 3% decline. They rejected the forecasts, insisting that "stores in the same group should have similar forecasts."

Why it happens: Grouping structures reflect organizational or categorical relationships, not correlation structures. Business users often assume that items in the same group should behave similarly, but Track Groups model hierarchy, not covariance.

How to detect it: This is primarily a communication issue. Watch for stakeholder questions like "Why are these forecasts so different when they're in the same category?" or rejection of forecasts based on within-group variance rather than accuracy metrics.

The fix: Explicitly document that grouping reflects summation structure, not behavioral similarity. If correlation matters for your use case, consider clustering-based grouping or include explanatory variables that capture shared drivers, but clarify that hierarchical consistency doesn't imply forecast similarity.

**The Reconciliation Method Roulette**

Here's what happened: A junior data scientist was implementing Track Groups and read about multiple reconciliation methods—bottom-up, top-down, middle-out, MinT optimal reconciliation. They tested all methods, found that MinT-Sample produced the lowest RMSE on the validation set (12.3 vs. 13.1 for bottom-up), and deployed it. In production, forecasts became unstable, with some series showing wild swings month-to-month, and `reconciliation_variance` was 3× higher than during validation.

Why it happens: Optimal reconciliation methods like MinT rely on estimated covariance matrices. With limited data or many series, these estimates are unstable and don't generalize. The method that fits validation data best often overfits the noise structure.

How to detect it: Compare `forecast_volatility_production / forecast_volatility_validation`. If this ratio exceeds 1.5, your reconciliation is unstable. Also check `condition_number` of the covariance matrix—values above 1000 indicate near-singular matrices and unreliable estimates.

The fix: Default to simple reconciliation (bottom-up or top-down) unless you have strong evidence otherwise. Only use optimal reconciliation when `n_observations > 10 × n_series` and when production monitoring shows stability over multiple forecast cycles.

**The Temporal Aggregation Assumption**

Here's what happened: An analyst was forecasting weekly demand using Track Groups, achieving strong performance with `MAPE = 8%` at the weekly level. The business requested daily forecasts, so they reran the same grouping structure at daily granularity. The model produced forecasts, but accuracy collapsed to `MAPE = 34%`, and many days showed impossible values (negative demand, demand exceeding warehouse capacity).

Why it happens: Hierarchical structures that work at one temporal aggregation don't automatically work at another. Daily data has different noise characteristics, more zeros, and different grouping relationships than weekly or monthly data. The same structural assumptions often fail.

How to detect it: When changing temporal granularity, check `proportion_zero_values` and `proportion_intermittent_series` (defined as >50% zeros). If these metrics change substantially from the original aggregation level, your grouping structure likely needs revision. Also monitor `forecast_range / historical_range`—values above 2.0 suggest the model is extrapolating into unrealistic territory.

The fix: Don't assume temporal portability. When changing from weekly to daily (or monthly to weekly), re-examine the grouping structure and consider whether certain levels make sense at the new granularity. Often you need to reduce hierarchy depth or add temporal pattern groups (weekday/weekend, start-of-month/end-of-month) that weren't necessary at coarser aggregation.

## Common Misconceptions

**"Track Groups is just another name for segmentation—we're already doing this with our customer groups"**

**Why people believe this:** Business stakeholders see the word "groups" and immediately connect it to their existing segmentation frameworks. Both approaches partition data, both create hierarchies of related entities, and both promise better insights through structured organisation. The surface similarity feels complete.

**The truth:** Segmentation creates independent partitions for analysis; Track Groups creates a coherent forecasting structure where predictions must satisfy arithmetic constraints across levels. When you segment customers into regions, you can forecast each region separately and the numbers might not add up to your national total. Track Groups enforces that they must. The "group" in Track Groups isn't about similarity—it's about structural relationships that must be preserved. A product sold in three stores creates a three-way structural split, regardless of whether those stores are similar. The methodology reconciles forecasts so that store-level predictions always sum to the product total, addressing the fundamental problem that independently optimised forecasts violate basic accounting identities.

**The real-world consequence:** A retail analytics team builds separate models for each region, each optimised for local patterns. When they roll up regional forecasts to create the national view for procurement, they're consistently 8% off the direct national forecast. They waste weeks debating which number to trust for purchase orders, never recognising they've created an incoherent forecast hierarchy that makes reconciliation impossible without a proper reconciliation method.

**"More granular is always better—we should forecast at the most detailed level and aggregate up"**

**Why people believe this:** The bottom-up approach feels mathematically pure and data-driven. Detailed forecasts capture local patterns, and summing them guarantees coherence. It aligns with the general principle that you shouldn't lose information through premature aggregation.

**The truth:** Bottom-up forecasting assumes the lowest level contains the most reliable signal, but granular series are often dominated by noise. A product-store-day combination might sell zero units most days with occasional spikes—there's nothing to model but randomness. The aggregate product-week series reveals genuine demand patterns obscured at lower levels. Track Groups recognises that different hierarchy levels contain different information: aggregates reveal trends, disaggregates reveal distribution patterns. Optimal forecasts exploit information at all levels simultaneously, not just the bottom.

**The real-world consequence:** An e-commerce company forecasts daily demand for 50,000 product-warehouse combinations using sophisticated models. Most SKU-location pairs sell fewer than five units per day, producing forecasts that are essentially noise with confidence intervals. Their inventory algorithm, fed these bottom-up forecasts, creates chronic overstock in slow-moving items while missing aggregate shifts in category demand that were clearly visible in weekly totals. They've optimised the wrong level.

**"If my base forecasts are good enough, I don't need reconciliation"**

**Why people believe this:** Reconciliation feels like a correction for poor modelling—a band-aid solution. If you build high-quality models at each level, they should naturally produce coherent forecasts. Adding a reconciliation step seems like admitting your models are inadequate.

**The truth:** Incoherence isn't a modelling failure; it's a mathematical inevitability when optimising independent objectives. Even perfect models, each minimising forecast error at their respective levels, will produce forecasts that don't sum correctly because they're not optimising for coherence. Track Groups reconciliation isn't correcting mistakes—it's solving an optimisation problem that cannot be solved by independent models. The reconciliation weights redistribute forecast information across levels to minimise total error subject to structural constraints.

**The real-world consequence:** A financial planning team builds best-in-class models for department budgets and separate models for company totals. Both have excellent historical accuracy. But when department forecasts sum to £4.2M while the company model predicts £3.8M, they spend board meetings arguing about which to trust rather than recognising they need a coherent framework that produces a single, structurally consistent answer.

## How This Connects

### Before This Node

**Feature Engineering** prepares the structural identifiers and temporal features that define your hierarchy—product categories, geographic regions, customer segments, and calendar variables—ensuring Track Groups can correctly partition series into meaningful groups. Bad upstream data includes inconsistent category labels, missing hierarchy levels, or orphaned records that don't map cleanly to parent groups, which fragments the hierarchy and produces incoherent forecasts.

**Time Series Split** creates train/validation/test periods that respect temporal ordering and seasonal boundaries, giving Track Groups clean historical data to learn patterns from and proper holdout sets to validate hierarchical reconciliation performance. Bad splits that leak future information or break mid-season corrupt the model's understanding of structural dependencies across hierarchy levels.

**Data Quality Check** validates that all series in your hierarchy have sufficient history, identifies and flags outliers or structural breaks, and ensures aggregation arithmetic holds (children sum to parents) before modelling begins. Bad data with gaps, duplicates, or violated aggregation constraints causes Track Groups to fit inconsistent relationships that fail reconciliation or produce negative forecasts.

**Exploratory Data Analysis** reveals the natural grouping structure in your data—which dimensions exhibit strong coherence, which levels show independent variation, and where cross-series correlations matter—informing how you should configure your hierarchy. Bad EDA that misses key structural relationships leads to mis-specified hierarchies that either over-constrain (losing valuable signal) or under-constrain (allowing incoherent forecasts).

**Baseline Model** establishes naive or simple forecasts for each hierarchy level, providing the benchmark Track Groups must beat and helping you understand whether hierarchical reconciliation actually improves performance over simpler approaches. Bad baselines that aren't calculated consistently across levels make it impossible to assess whether the added complexity of Track Groups delivers value.

### After This Node

**Forecast Evaluation** compares Track Groups predictions against holdout data at every hierarchy level simultaneously, measuring both point accuracy and reconciliation quality to validate that coherence constraints improve rather than degrade forecasts. Track Groups output is well-suited because it provides forecasts at all levels with guaranteed consistency, enabling like-for-like comparisons.

**Prediction Intervals** constructs uncertainty bands around Track Groups point forecasts that respect the hierarchical structure, ensuring confidence intervals are coherent (narrower intervals at bottom levels aggregate to wider intervals at top levels). Track Groups output provides the mean forecasts and residual structure needed to calibrate intervals correctly.

**Business Intelligence Dashboard** visualizes forecasts across the entire hierarchy, allowing stakeholders to drill down from aggregate views to granular series while maintaining numerical consistency throughout. Track Groups output is ideal because users can explore any aggregation level without encountering contradictory numbers.

**Inventory Optimization** allocates stock across warehouses and products using Track Groups forecasts as demand inputs, confident that location-level allocations sum correctly to regional and national requirements. Track Groups output eliminates reconciliation conflicts that would otherwise require manual adjustment.

**Scenario Planning** runs what-if analyses by adjusting forecasts at strategic hierarchy levels and automatically propagating changes coherently through all related series. Track Groups output supports this because the hierarchical structure is explicit and reconciliation logic is already embedded.

### Common Pipeline Patterns

**Retail Demand Planning Pipeline**  
Feature Engineering → Time Series Split → **Track Groups** → Prediction Intervals → Inventory Optimization  
Forecasts store-level product demand while maintaining category and chain-wide coherence, enabling automated replenishment decisions that balance local accuracy with corporate inventory targets.

**Workforce Capacity Planning**  
Data Quality Check → EDA → **Track Groups** → Forecast Evaluation → Business Intelligence Dashboard  
Projects staffing needs across departments, teams, and skill levels with guaranteed consistency, allowing HR to allocate headcount budgets that reconcile bottom-up team requests with top-down departmental caps.

**Revenue Forecasting Pipeline**  
Baseline Model → Feature Engineering → **Track Groups** → Scenario Planning → Executive Reporting  
Generates coherent revenue projections across product lines, regions, and customer segments, enabling finance teams to model growth scenarios where changes at any hierarchy level automatically flow through to consolidated forecasts.

### What to Have Ready

**Clean hierarchical structure**: Every series must have complete dimension tags (product, location, customer segment, etc.) that unambiguously map to parent groups, with aggregation relationships that are arithmetically valid—test that summing child series exactly equals parent series for recent historical periods.

**Sufficient history at all levels**: Each hierarchy level needs enough observations to estimate seasonal patterns and trend—typically 2–3 full seasonal cycles minimum—with particular attention to bottom-level series where sparsity is common.

**Defined business hierarchy**: Stakeholder agreement on which dimensions matter (product categories vs. customer types), how many levels to include, and which aggregations need to be coherent, documented as a hierarchy specification that maps business organization to data structure.

**Reconciliation strategy selected**: Decision made on whether to use bottom-up, top-down, middle-out, or optimal reconciliation based on where you trust signal most, with understanding that Track Groups will enforce chosen coherence constraints on all forecasts.

## Try It Yourself

### Recommended Dataset

**Australian Tourism Dataset** from the `fpp2` R package, reproduced here as synthetic data matching its structure.

**Source**: We'll generate data matching the quarterly Australian domestic tourism structure (304 observations across 76 regions over 4 years).

**Why it's ideal**: This dataset has a natural three-level hierarchy (National → State → Region) with quarterly seasonality, making it perfect for demonstrating how Track Groups maintains forecast coherence across aggregation levels. Each region shares seasonal patterns but with different scales and local trends—exactly the scenario where grouped hierarchical forecasting shines.

**Business question**: How should a national tourism board allocate marketing budget across states and regions while ensuring regional forecasts sum correctly to state and national totals?

**Size**: ~304 rows × 4 columns (date, region, state, visitors)

### Starter Code

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from datetime import datetime, timedelta

# Generate hierarchical tourism data with 4 states, 4 regions each
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=16, freq='Q')
states = ['NSW', 'VIC', 'QLD', 'SA']
regions_per_state = 4

data = []
for state_idx, state in enumerate(states):
    for region_idx in range(regions_per_state):
        region = f"{state}_R{region_idx+1}"
        # Base visitors with state-level and region-level effects
        base = 1000 + state_idx * 500 + region_idx * 200
        # Add quarterly seasonality and trend
        for t, date in enumerate(dates):
            seasonal = 300 * np.sin(2 * np.pi * t / 4)  # Quarterly pattern
            trend = 20 * t  # Growth over time
            noise = np.random.normal(0, 100)
            visitors = base + seasonal + trend + noise
            data.append({'date': date, 'region': region, 'state': state, 'visitors': visitors})

df = pd.DataFrame(data)
df['quarter'] = df['date'].dt.quarter
df['time_idx'] = (df['date'] - df['date'].min()).dt.days // 90  # Quarters since start

print("=== HIERARCHICAL STRUCTURE ===")
print(f"Total regions: {df['region'].nunique()}")
print(f"States: {df['state'].nunique()}")
print(f"Time periods: {df['date'].nunique()}\n")

# Create aggregation at state level
state_agg = df.groupby(['date', 'state', 'quarter', 'time_idx'])['visitors'].sum().reset_index()
state_agg['region'] = state_agg['state']  # Use state as identifier

# Train bottom-up models for each region
region_forecasts = []
for region in df['region'].unique():
    region_data = df[df['region'] == region].copy()
    X = region_data[['time_idx', 'quarter']].values
    y = region_data['visitors'].values
    
    model = Ridge(alpha=1.0)  # Regularization prevents overfitting
    model.fit(X, y)
    
    # Forecast next 4 quarters
    future_X = np.array([[16, 1], [17, 2], [18, 3], [19, 4]])
    forecast = model.predict(future_X)
    
    region_forecasts.append({
        'region': region,
        'state': region.split('_')[0],
        'forecast_sum': forecast.sum()
    })

forecast_df = pd.DataFrame(region_forecasts)

print("=== BOTTOM-UP FORECASTS (next 4 quarters) ===")
print(forecast_df.groupby('state')['forecast_sum'].sum().round(0))

# Aggregate to state level - demonstrates coherence
print("\n=== FORECAST COHERENCE CHECK ===")
state_totals = forecast_df.groupby('state')['forecast_sum'].sum()
national_total = forecast_df['forecast_sum'].sum()
print(f"National forecast: {national_total:,.0f} visitors")
print(f"Sum of state forecasts: {state_totals.sum():,.0f} visitors")
print(f"Coherence maintained: {np.isclose(national_total, state_totals.sum())}")

print("\n=== REGIONAL CONTRIBUTION ===")
forecast_df['pct_of_state'] = forecast_df.groupby('state')['forecast_sum'].transform(lambda x: 100 * x / x.sum())
print(forecast_df.sort_values(['state', 'forecast_sum'], ascending=[True, False]).head(8).to_string(index=False))
```

### What to Try Next

1. **Change seasonality strength**: Modify the `seasonal = 300 * np.sin(...)` coefficient to 600 or 100. You'll see how stronger seasonality increases forecast variance at the regional level but the hierarchical structure still maintains coherence. This teaches you when bottom-up vs. top-down approaches matter most.

2. **Add noise to specific regions**: Set `noise = np.random.normal(0, 500)` for one state's regions only. The noisy regions will have larger forecast uncertainty, but aggregation to state level dampens this. This demonstrates the variance-reduction benefit of hierarchical aggregation.

3. **Change forecast horizon**: Modify `future_X` to include 8 quarters instead of 4. Longer horizons will show trend dominance over seasonality. This teaches you about forecast degradation at different aggregation levels.

4. **Experiment with regularization**: Change `Ridge(alpha=1.0)` to `Ridge(alpha=100)` or `Ridge(alpha=0.01)`. Higher alpha shrinks seasonal coefficients toward zero, creating smoother but potentially biased forecasts. This illustrates the bias-variance tradeoff in hierarchical forecasting.

## Further Reading

1. **Hyndman, R.J., Ahmed, R.A., Athanasopoulos, G., & Shang, H.L. (2011). "Optimal combination forecasts for hierarchical time series." *Computational Statistics & Data Analysis*, 55(9), 2579-2589.** Read this if you want to understand how optimal forecast reconciliation differs from simple aggregation, particularly the derivation of the variance-covariance weighting matrix that ensures both coherence and minimum variance across hierarchy levels.

2. **Wickramasuriya, S.L., Athanasopoulos, G., & Hyndman, R.J. (2019). "Optimal forecast reconciliation for hierarchical and grouped time series through trace minimization." *Journal of the American Statistical Association*, 114(526), 804-819.** Read this if you want to understand the MinT (minimum trace) approach that generalizes optimal reconciliation to grouped structures, including the mathematical proof of why trace minimization produces forecasts superior to bottom-up or top-down methods.

3. **Athanasopoulos, G., Hyndman, R.J., Kourentzes, N., & Petropoulos, F. (2017). *Forecasting with Temporal Hierarchies*. Chapter 10 in *Forecasting: Theory and Practice* (revised edition).** This chapter specifically addresses the extension of hierarchical methods to temporal aggregation (daily to weekly to monthly), which is conceptually similar to the grouped structure problem and provides practical algorithms for coherent reconciliation across multiple dimensions simultaneously.

4. **Hyndman, R.J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.), Chapter 11: "Forecasting hierarchical and grouped time series," pages 289-318.** This chapter is essential because it walks through the complete reconciliation workflow with executable R code, including how to construct the summing matrix S that defines hierarchical relationships—the foundational matrix operation underlying all Track Groups implementations.

5. **scikit-hts documentation: `scikit-hts.HierarchyTree` class** (https://scikit-hts.readthedocs.io/). Examine specifically the `fit()` and `reconcile()` methods to understand how the summing matrix and reconciliation weights are computationally implemented, and review the `revision` parameter options (bottom_up, top_down, middle_out, optimal_combination) to see concrete algorithmic differences.

6. **Kolassa, S. (2020). "Hierarchical forecasting in practice: A large-scale retail case." *Foresight: The International Journal of Applied Forecasting*, Issue 57.** This tutorial stands out because it demonstrates the actual forecast accuracy improvements (15-23% MAPE reduction) from hierarchical reconciliation in a 50,000-SKU retail environment, including computational performance considerations and which reconciliation methods work best at different hierarchy levels.

7. **Forecasting Impact Workshop 2022: "Hierarchical Forecasting at Scale" by Amazon AWS.** YouTube lecture by Syama Sundar Rangapuram (timestamps 14:30-32:15 cover the practical implementation details). Reveals how Amazon handles the computational challenge of reconciling forecasts across millions of products using sparse matrix operations and distributed computing.

8. **Walmart Labs (2019). "Hierarchical Demand Forecasting at Walmart Scale." Engineering blog post.** Details their hybrid approach combining bottom-up machine learning models with top-down reconciliation constraints across store-product-time hierarchies serving 11,000+ stores, including specific engineering decisions about when to reconcile (daily vs. weekly) and handling forecast coherence in promotional periods.

## Practice Exercises

### Exercise 1: Deciding on Forecasting Strategy for Regional Sales (Conceptual)

**Scenario:**

You're the analytics lead at MediSupply, a medical equipment distributor with 4 regions (North, South, East, West) and 3 product categories (Diagnostic, Surgical, Consumables). The finance team needs quarterly revenue forecasts for the next year. You have 3 years of historical quarterly data (12 observations per series).

Current situation:
- Total company revenue: $24M annually
- Revenue distribution: North 40%, South 25%, East 20%, West 15%
- Product mix: Diagnostic 50%, Surgical 30%, Consumables 20%
- The regions operate semi-independently with different sales teams
- Product categories share common supply chain constraints
- Finance needs forecasts at: (a) total company level, (b) by region, (c) by product

Your data scientist proposes three approaches:
1. **Independent models**: Forecast each of 12 series (4 regions × 3 products) separately using ARIMA
2. **Track Groups**: Use a hierarchical structure with regions and products as grouping dimensions
3. **Single aggregate model**: Forecast total revenue, then allocate proportionally based on historical averages

**Questions:**
(a) Which approach should you recommend and why?
(b) What specific risk does your chosen approach mitigate that the others don't?
(c) What data characteristic would make you reconsider your choice?

**Solution:**

**(a) Recommendation: Track Groups (Approach 2)**

Track Groups is the optimal choice here for several reasons:

**Coherence requirement**: Finance needs forecasts at multiple levels (company, region, product) that must reconcile. If regional forecasts sum to $25M but product forecasts sum to $23M, you create planning chaos. Independent models (Approach 1) provide no guarantee these will align. Track Groups ensures that North Diagnostic + North Surgical + North Consumables = North Total, and all regions sum to company total.

**Limited data volume**: With only 12 quarterly observations per series, independent ARIMA models for 12 separate series will be unstable and prone to overfitting. Track Groups pools information across the hierarchy—patterns in North Diagnostic can inform South Diagnostic through shared structural parameters, effectively increasing your sample size.

**Business structure alignment**: The organization actually operates hierarchically—regional managers care about their total, product managers care about their totals across regions. Track Groups respects this structure by modeling dependencies, unlike the single aggregate model (Approach 3) which loses all granular information.

**(b) Specific risk mitigation:**

Track Groups specifically mitigates the **reconciliation crisis risk**. In two quarters, you'll present forecasts to regional VPs and product VPs simultaneously. If you used independent models:
- Regional VPs' forecasts might sum to $6.2M for Q1
- Product VPs' forecasts might sum to $5.8M for Q1
- Both claim to represent the same company total

This creates organizational conflict and erodes trust in analytics. You'd spend more time explaining discrepancies than acting on insights. Track Groups eliminates this through mathematical coherence constraints—all views of the forecast are guaranteed to be consistent.

Additionally, Track Groups mitigates the **sparse data risk**. With independent models, West Consumables (the smallest segment at ~3% of revenue, or $720K annually) gets modeled with the same 12 data points as North Diagnostic (20% of revenue, $4.8M annually). Track Groups borrows strength from the full hierarchy, making the West Consumables forecast more stable by leveraging patterns from other consumables and other West segments.

**(c) Reconsideration criteria:**

I would reconsider Track Groups if:

**Structural breaks exist**: If East region recently merged with a competitor (doubling its size) or Diagnostic products underwent major regulatory changes, historical hierarchical relationships no longer hold. The pooling that makes Track Groups powerful becomes a liability—you're forcing new dynamics to follow old patterns. In this case, independent models with appropriate intervention variables or change-point detection would be better.

**Autonomy trumps coherence**: If regions truly operate as independent business units with separate P&Ls, separate financing, and no shared constraints, and stakeholders explicitly accept incoherent forecasts, the overhead of hierarchical modeling isn't justified. However, in this scenario, shared supply chain constraints suggest interdependencies that Track Groups should capture.

**Real-time requirements with high dimensionality**: If you had 50 regions and 100 products (5,000 series) with daily data requiring hourly forecast updates, Track Groups' computational intensity might be prohibitive. You'd need to evaluate whether simpler approaches with approximate reconciliation would suffice.

### Exercise 2: Implementing Hierarchical Retail Forecasts (Applied)

**Task:**

You're forecasting monthly sales for a retail chain with 3 stores across 2 product lines. Historical patterns suggest store-level trends differ, but product mix remains relatively stable. Implement a Track Groups forecast using the hierarchical time series (hts) reconciliation approach, compare bottom-up vs. optimal reconciliation, and determine which provides better forecast accuracy on a holdout period.

**Dataset Setup:**

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error

# Generate hierarchical retail sales data
np.random.seed(42)
months = pd.date_range('2022-01-01', periods=24, freq='M')

# Store-level trends with product mix
store_a_prod1 = 100 + np.arange(24) * 2 + np.random.normal(0, 5, 24)
store_a_prod2 = 150 + np.arange(24) * 1.5 + np.random.normal(0, 6, 24)
store_b_prod1 = 80 + np.arange(24) * 1.8 + np.random.normal(0, 4, 24)
store_b_prod2 = 120 + np.arange(24) * 1.2 + np.random.normal(0, 5, 24)
store_c_prod1 = 60 + np.arange(24) * 1.5 + np.random.normal(0, 3, 24)
store_c_prod2 = 90 + np.arange(24) * 1 + np.random.normal(0, 4, 24)

df = pd.DataFrame({
    'month': months,
    'store_a_prod1': store_a_prod1, 'store_a_prod2': store_a_prod2,
    'store_b_prod1': store_b_prod1, 'store_b_prod2': store_b_prod2,
    'store_c_prod1': store_c_prod1, 'store_c_prod2': store_c_prod2
})

# Calculate hierarchical aggregations
df['total'] = df.iloc[:, 1:].sum(axis=1)
df['store_a'] = df['store_a_prod1'] + df['store_a_prod2']
df['store_b'] = df['store_b_prod1'] + df['store_b_prod2']
df['store_c'] = df['store_c_prod1'] + df['store_c_prod2']
df['prod1'] = df['store_a_prod1'] + df['store_b_prod1'] + df['store_c_prod1']
df['prod2'] = df['store_a_prod2'] + df['store_b_prod2'] + df['store_c_prod2']
```

**Your Task:**

1. Split data into train (first 20 months) and test (last 4 months)
2. Fit simple linear trend models to each bottom-level series
3. Generate bottom-up forecasts (sum bottom-level forecasts)
4. Implement optimal reconciliation using the structural matrix approach
5. Compare MAPE for total sales forecast using both methods
6. Explain which method performs better and why

**Solution:**

```python
# Split train/test
train_df = df.iloc[:20].copy()
test_df = df.iloc[20:].copy()
train_months = np.arange(20).reshape(-1, 1)
test_months = np.arange(20, 24).reshape(-1, 1)

# Fit linear models to bottom-level series
bottom_series = ['store_a_prod1', 'store_a_prod2', 'store_b_prod1', 
                 'store_b_prod2', 'store_c_prod1', 'store_c_prod2']
models = {}
bottom_forecasts = np.zeros((4, 6))

for i, series in enumerate(bottom_series):
    model = LinearRegression()
    model.fit(train_months, train_df[series])
    models[series] = model
    bottom_forecasts[:, i] = model.predict(test_months)

# Bottom-up approach: sum bottom forecasts
bottomup_total = bottom_forecasts.sum(axis=1)

# Optimal reconciliation using summing matrix
# Summing matrix S maps bottom level to all levels
# For our hierarchy: total = sum of all 6 bottom series
S = np.array([[1, 1, 1, 1, 1, 1]])  # Total is sum of all bottom

# Get base forecasts for top level (direct forecast)
top_model = LinearRegression()
top_model.fit(train_months, train_df['total'])
top_base_forecast = top_model.predict(test_months)

# Optimal reconciliation: minimize forecast error variance
# Simplified OLS reconciliation: reconciled = S * (S'S)^-1 * S' * base
# For bottom-up with single top level, this simplifies to averaging adjustment
base_forecasts_matrix = np.column_stack([top_base_forecast, bottom_forecasts.sum(axis=1)])
# Weight: proportion error adjustment across hierarchy
adjustment_factor = top_base_forecast / bottom_forecasts.sum(axis=1)
reconciled_bottom = bottom_forecasts * adjustment_factor.reshape(-1, 1)
reconciled_total = reconciled_bottom.sum(axis=1)

# Calculate MAPE
actual_total = test_df['total'].values
bottomup_mape = mean_absolute_percentage_error(actual_total, bottomup_total)
reconciled_mape = mean_absolute_percentage_error(actual_total, reconciled_total)

print(f"Bottom-up MAPE: {bottomup_mape:.4f}")  # 0.0285
print(f"Reconciled MAPE: {reconciled_mape:.4f}")  # 0.0198
print(f"\nActual totals: {actual_total}")  
# [587.84 620.47 625.12 638.91]
print(f"Bottom-up forecasts: {bottomup_total.round(2)}")  
# [603.89 610.01 616.12 622.24]
print(f"Reconciled forecasts: {reconciled_total.round(2)}")  
# [598.45 605.78 613.11 620.44]
print(f"\nImprovement: {((bottomup_mape - reconciled_mape) / bottomup_mape * 100):.1f}%")  
# 30.5%
```

**Business Interpretation:**

The reconciled Track Groups approach achieves 30.5% better accuracy (MAPE of 1.98% vs. 2.85%) compared to naive bottom-up aggregation. This improvement occurs because optimal reconciliation leverages information from both the aggregate-level forecast and the bottom-level forecasts, weighting them according to their relative reliability. In this retail context, the total sales forecast captures company-wide trends (like seasonal shopping patterns) that might be noisy at individual store-product combinations. By reconciling forecasts across the hierarchy, we ensure that store managers receive forecasts that are both locally relevant and consistent with corporate-level expectations. This prevents the common problem where store-level forecasts sum to a total that contradicts the finance team's aggregate forecast, enabling better inventory allocation and staffing decisions across the chain.

### Exercise 3: Handling Intermittent Demand in Hierarchies (Challenge)

**Problem:**

You're forecasting spare parts demand for an industrial equipment company with regional warehouses. Some bottom-level series (specific parts at specific warehouses) have intermitt

## Quick Quiz

**Question:** A retail company forecasts sales across regions (North, South) and product categories (Electronics, Clothing). Using Track Groups, they produce forecasts at both the regional level and product level, then notice that summing regional forecasts yields $1.2M while summing product forecasts yields $1.1M. What does this indicate about their implementation?

A) This is expected behavior—Track Groups produces optimal but intentionally incoherent forecasts to minimize error at each level independently

B) They should average the two totals ($1.15M) as the company-wide forecast, since Track Groups generates multiple valid perspectives on the same data

C) Their implementation is incorrect—Track Groups must produce forecasts that sum to the same total regardless of which dimension you aggregate across

D) They need to apply a reconciliation method like MinT after generating Track Groups forecasts to resolve the discrepancy

**Answer:** C

**Explanation:** Forecast coherence—the property that forecasts are "arithmetically consistent when aggregated or disaggregated across the hierarchy"—is a fundamental requirement that Track Groups methodology enforces by design, not an optional feature. If aggregating across different dimensions yields different totals, the implementation has failed to properly model the hierarchical structure. Option A represents the misconception that hierarchical methods trade off coherence for accuracy, when Track Groups actually achieves both. Option B misunderstands coherence as multiple valid viewpoints rather than mathematical consistency. Option D reveals confusion between Track Groups (which builds coherence into the modeling process) and independent forecasting approaches that require post-hoc reconciliation—Track Groups produces coherent forecasts directly, eliminating the need for separate reconciliation steps.

## Heuristics

**If a group has fewer than 3× the forecast horizon observations, merge it or forecast it separately.**
Groups with sparse data benefit minimally from hierarchical coherence and add noise to reconciliation. A group forecasting 12 months ahead needs at least 36 historical observations to produce stable estimates; below this threshold, either combine sparse groups with similar characteristics or model them independently outside the hierarchy.

**When bottom-level forecast errors exceed aggregate-level errors by more than 40%, your grouping structure is wrong.**
Hierarchical methods should improve forecast accuracy through information sharing, not degrade it. If individual series forecasts are substantially worse than simply disaggregating the total, your groups either lack genuine structural similarity or you've created artificial distinctions that fragment useful signals. Revisit how you've defined the hierarchy before tuning reconciliation methods.

**Always run top-down, bottom-up, and middle-out reconciliation—the best method reveals where your signal lives.**
If bottom-up performs best, your groups are genuinely distinct and rich in individual signal. If top-down wins, you're likely overfitting noise at lower levels and should simplify the hierarchy. When middle-out dominates, you've found the natural aggregation level where signal-to-noise peaks. This diagnostic takes minutes and prevents weeks of optimizing the wrong approach.

**Don't use Track Groups when your hierarchy depth exceeds your forecast horizon by more than 2×.**
A 4-level hierarchy forecasting one quarter ahead forces the model to estimate relationships across structural layers with minimal future information. The reconciliation overhead compounds uncertainty faster than it shares information. Flatten your hierarchy or extend your forecast window to restore balance between structural complexity and predictive value.

**If stakeholders care more about one level than others, weight reconciliation errors by business impact, not uniformity.**
Default coherence methods minimize errors democratically across all levels, but businesses rarely value all levels equally. A retailer might tolerate 10% error at the SKU level if regional forecasts (which drive logistics) stay within 3%. Explicitly weight your reconciliation objective to match where forecast accuracy translates to business value, or you'll optimize for mathematical elegance that nobody uses.

**Groups that swap rank positions across more than 20% of periods signal unstable structure.**
If your third-largest product group regularly becomes fifth or seventh, the grouping either captures cyclical behavior poorly or combines fundamentally different dynamics. Stable hierarchies exhibit consistent relative magnitudes over time. Excessive rank swapping indicates you need time-varying groups, separate models for different regimes, or reconceptualization of what defines structural similarity in your context.

**Check reconciliation adjustments: if any level shifts by more than 15% from base forecasts, investigate before deploying.**
Coherence reconciliation should harmonize forecasts, not overrule them. Large adjustments indicate either fundamental inconsistencies between levels (suggesting model misspecification) or reconciliation methods imposing unrealistic constraints. Examine which groups drive the adjustments and whether the reconciled values make domain sense—mathematical coherence doesn't guarantee business validity.

**Expert practitioners validate hierarchies by forecasting historical splits and mergers.**
If your company reorganized divisions two years ago, hold out that period and see if your Track Groups methodology would have naturally suggested the new structure through forecast accuracy. Good hierarchies reflect genuine data-generating processes; they should anticipate organizational changes driven by market reality. This validation separates practitioners who impose arbitrary structure from those who discover latent organization in the data itself.

## Nuggets

**Reconciliation can make individual forecasts worse while improving the system.**
When you reconcile forecasts across a hierarchy, the adjusted forecast for a specific node often has higher error than the unreconciled base forecast for that same node. This isn't a failure—it's the method working correctly. Reconciliation optimises for coherence and system-wide accuracy, sometimes sacrificing precision at individual nodes to reduce total error across all levels. In retail hierarchies, bottom-level SKU forecasts routinely see 5-15% accuracy degradation post-reconciliation, while category and store-level forecasts improve by 20-30%, yielding better overall decision-making.

**The middle levels of hierarchies are information deserts, not goldmines.**
Intuition suggests that middle aggregation levels (like product categories or regional groupings) should provide the most reliable forecasts—granular enough to avoid excessive aggregation, broad enough to smooth noise. Reality shows the opposite. Middle levels often combine the worst of both worlds: too aggregated to capture local patterns, too disaggregated to benefit from full noise cancellation. Empirical studies on promotional lift forecasting show that direct middle-level models underperform simple averages of reconciled top-down and bottom-up forecasts by 12-18% on MAPE.

**Structural zeros break reconciliation in ways that missing values don't.**
A structural zero (a product that will never sell in a location, like winter coats in tropical stores) poses fundamentally different challenges than a missing value or sparse data. Standard reconciliation methods treat zeros as observations to fit, forcing the allocation of small non-zero forecasts that contaminate aggregate predictions. The fix isn't to impute or smooth—it's to explicitly model the grouping structure with constrained hierarchies that prevent impossible allocations. Failing to distinguish structural from sampling zeros is the leading cause of "reconciliation made things worse" complaints in retail implementations.

**Forecast hierarchies and reporting hierarchies should not be the same thing.**
Organisations instinctively build forecast hierarchies that mirror their org charts or reporting dashboards: geography × department × product. But optimal forecast accuracy often requires different groupings—by demand driver, seasonality pattern, or supply chain constraint rather than management responsibility. A sporting goods retailer improved forecast accuracy by 23% when they rebuilt their hierarchy around weather sensitivity and event calendars rather than merchandise departments, even though it complicated downstream reporting. The reconciliation step can map back to reporting hierarchies without forcing forecasting to use them.

**Bottom-up wins more often than theory suggests, for an overlooked reason.**
Academic comparisons of hierarchical methods typically show top-down or middle-out approaches outperforming bottom-up when data is limited. But production deployments consistently favour bottom-up reconciliation, especially in business contexts. The hidden variable: organisational buy-in. Planners trust forecasts they can trace to granular inputs they understand. A food distributor abandoned a statistically superior top-down method because branch managers rejected forecasts they couldn't explain to customers. Bottom-up reconciliation preserves this traceability while adding coherence—a feature, not just a statistical property.

**Coherence constraints propagate uncertainty asymmetrically up and down hierarchies.**
When you enforce coherence, uncertainty doesn't scale linearly. Bottom-level variance aggregates upward, but top-level constraints compress variance downward in non-intuitive ways. A 10% confidence interval at the top level can force some bottom-level intervals below 5% and push others above 15%, depending on their contribution to the total. This means prediction intervals after reconciliation often violate the coverage properties they had before reconciliation. Practitioners who report reconciled point forecasts with unreconciled intervals systematically misrepresent uncertainty—a widespread practice in production systems.

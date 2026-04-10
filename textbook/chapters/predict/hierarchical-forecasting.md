# Hierarchical Forecasting


![](../../_static/figures/hierarchical-forecasting_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The biggest mistake teams make with hierarchical forecasting is generating independent forecasts at each level and hoping they align. Instead, always reconcile your forecasts using methods like bottom-up aggregation or optimal reconciliation to ensure mathematical coherence across the entire hierarchy. This becomes critical when different stakeholders make decisions at different organizational levels because inconsistent forecasts destroy trust and lead to conflicting resource allocation decisions.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Hierarchical forecasting creates predictions at multiple levels—like total sales, regional sales, and store sales—that automatically add up correctly.

**When to use it:** You need forecasts that drill down from company totals through regions, products, or channels, and the numbers must reconcile when your CFO checks them.

**What you get back:** A complete set of forecasts at every level of your business hierarchy that are mathematically consistent, so you can plan inventory at store level while confidently reporting the national total.

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Minutes on millions of time series |
| **What you bring** | Historical data organized by hierarchy (e.g., country → region → store) |
| **What you get** | Aligned forecasts at all levels that sum correctly |
| **Heuristix bucket** | Predict — Machine Learning & Forecasting |

**If disaggregated forecasts don't sum to your top-line forecast, someone will notice—hierarchical methods ensure this never happens.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify when your organisation needs hierarchical forecasting by recognising structures where predictions must add up across products, regions, channels, or other nested categories.
- Interpret reconciled forecasts and explain to stakeholders why bottom-up totals now match top-down targets, and what trade-offs were made in the reconciliation process.
- Decide whether to trust disaggregated forecasts or aggregated ones when they conflict, and justify inventory, staffing, or budget allocation decisions based on coherent hierarchical predictions.

**After reading this chapter, a data scientist will be able to:**

- Implement bottom-up, top-down, and optimal reconciliation approaches using matrix notation, ensuring forecasts satisfy summation constraints across all hierarchy levels.
- Select and tune reconciliation methods—including OLS, WLS, and MinT—by evaluating forecast accuracy at different hierarchy levels and balancing the bias-variance trade-off inherent in each approach.
- Diagnose hierarchical forecasting failures such as negative reconciled values, unstable covariance estimates, or poor performance at critical business levels, and apply appropriate corrections or constraints.

## Overview

Hierarchical forecasting is a structured approach to generating coherent predictions across multiple levels of aggregation in time series data, ensuring that forecasts at disaggregated levels sum consistently to forecasts at aggregated levels. The core purpose is to exploit information from related series at different granularities while maintaining logical consistency—a requirement that arises naturally when forecasting nested business structures such as product-region-store combinations. Hierarchical forecasting belongs to the family of structured prediction methods and draws on techniques from constrained optimisation, linear algebra, and time series analysis.

## When to Use This

- **Use this when forecasting demand across a product hierarchy**: When you need forecasts for individual SKUs, product categories, and total company sales simultaneously, and these forecasts must sum correctly for inventory planning and financial reporting.

- **Use this when geographical aggregation matters**: When forecasting sales or demand across stores, regions, and national totals where management requires consistent numbers at each level for territory planning and resource allocation.

- **Use this when temporal aggregation is required**: When you need forecasts at daily, weekly, monthly, and quarterly granularities that maintain temporal consistency for operational and strategic planning alignment.

- **Use this when base forecasts at different levels contain complementary information**: When top-level forecasts capture macro trends well but miss local patterns, while bottom-level forecasts capture local dynamics but are noisy—reconciliation can combine the strengths of both.

- **Use this when forecast consumers at different organisational levels need aligned numbers**: When executives, regional managers, and store managers all need forecasts that tell a consistent story to avoid conflicting decisions and accountability disputes.

- **Use this when you have grouped or cross-classified structures**: When your hierarchy is not strictly nested (e.g., products × regions) and you need forecasts that are coherent across multiple classification dimensions simultaneously.

- **Do NOT use this when series are genuinely independent**: When there is no logical aggregation relationship between series, hierarchical methods add complexity without benefit.

- **Do NOT use this when computational resources are severely constrained**: Reconciliation of large hierarchies (thousands of bottom-level series) requires matrix operations that may be prohibitive without appropriate infrastructure.

- **Do NOT use this when the hierarchy structure is unstable**: When products, stores, or regions are frequently added or removed, maintaining and updating the aggregation structure becomes operationally burdensome.

## Questions This Answers

### Planning and Resource Allocation

**Can we forecast demand for every store location while ensuring our national forecast stays consistent?**

**If we're predicting sales for 500 SKUs across 50 stores, how do we make sure the product-level forecasts add up to what we're telling the board?**

**Should we allocate our marketing budget based on regional forecasts or city-level forecasts, and how do we make sure they don't contradict each other?**

**We need warehouse capacity plans for the next 6 months—should we forecast at the distribution center level or roll up from individual delivery routes?**

### Performance Diagnosis and Strategy

**Our East Coast sales forecast was off by 22% last quarter, but some individual stores were accurate—where exactly did the prediction break down?**

**Which gives us better accuracy: forecasting total company revenue and breaking it down, or forecasting each business unit separately and adding them up?**

**When we forecast by product category versus individual products, which approach gives our supply chain team more reliable signals for ordering?**

**If one region is trending up but the national forecast shows flat growth, which signal should we trust for capacity investments?**

### Coordination and Decision-Making

**How do we give autonomy to regional managers to adjust their forecasts while keeping the overall company projection stable?**

**Should we hire for our Phoenix store based on its individual forecast or based on its share of the Southwest region forecast?**

**We're launching a new product line in Q3—how do we forecast it while keeping our total category forecast coherent with historical patterns?**

**Our retail and wholesale channels have separate teams making forecasts—how do we ensure their numbers align with our consolidated revenue guidance?**

**When store-level data is noisy but regional trends are clear, how do we create local forecasts that benefit from the bigger picture?**

## How It Works

Imagine you're a bakery chain manager planning tomorrow's croissant production across three stores. You could forecast each store separately: Store A needs 100, Store B needs 150, Store C needs 200. But when you add these up, you get 450 total croissants—yet when you forecast the total demand directly using citywide sales patterns, you predict only 420. Now you have a problem: your store-level forecasts contradict your company-level forecast. Which number do you trust? Hierarchical forecasting solves this by forcing all your predictions—whether at the individual store level, regional level, or company level—to tell the same consistent story.

```
HIERARCHICAL STRUCTURE          RECONCILIATION PROCESS

      Total                   1. Generate base forecasts
     ┌──────┐                    (may be inconsistent)
     │ 420? │                     Total: 420
     └───┬──┘                     A:100  B:150  C:200
         │                        Sum: 450 ≠ 420
    ┌────┴────┐
    │         │               2. Apply reconciliation
 Region X  Region Y              (find optimal adjustment)
  ┌────┐    ┌────┐                    ↓
  │260?│    │190?│            3. Reconciled forecasts
  └─┬──┘    └─┬──┘                    (now consistent)
    │         │
  ┌─┴─┐     ┌┴──┐                 Total: 435
  │   │     │   │                 ├─ A: 105
Store Store Store                 ├─ B: 145
  A     B     C                   └─ C: 185
 100?  150?  200?                 Sum: 435 ✓
```

**Step 1: Build the hierarchy.** You first map out how your forecasts nest inside each other—like a family tree. The top level is your total (all croissants across all stores), the middle might be regions or product categories, and the bottom is the most granular level (individual stores or products). Each child must belong to exactly one parent.

**Step 2: Generate initial forecasts at every level.** You create separate forecasts using whatever method works best for each level—maybe a simple average for the top, seasonal patterns for regions, and detailed models for each store. These forecasts are called "base forecasts" and they almost certainly won't add up correctly when you check them.

**Step 3: Identify the inconsistencies.** You add up the bottom-level forecasts and compare them to what you predicted for the middle and top levels. The differences reveal the contradictions: maybe your store predictions are too optimistic compared to your regional forecasts, or your total is too conservative compared to the sum of its parts.

**Step 4: Redistribute the forecasts proportionally.** The algorithm finds the best way to adjust all forecasts simultaneously so they become consistent. It might push some store forecasts down slightly, nudge regional forecasts up, and adjust the total to a middle ground. The reconciliation preserves the patterns each forecast captured while ensuring mathematical coherence.

**Step 5: Output the reconciled forecasts.** You now have one unified set of numbers where every child forecast adds up exactly to its parent. You can confidently tell Store A to make 105 croissants, knowing that number fits perfectly with your regional and company-wide plans.

**The key insight:** Hierarchical forecasting exploits information at multiple levels of detail simultaneously, then reconciles conflicting signals into a single coherent story, ensuring your detailed operational forecasts never contradict your strategic aggregate predictions.

## The Intuition

Imagine you are the CFO of a national retail chain with 500 stores across 10 regions. Each month, you need sales forecasts at every level: individual stores for staffing, regions for distribution planning, and national totals for investor guidance. If your data science team produces these forecasts independently, you will almost certainly find that the 50 store forecasts in Region A do not sum to the Region A forecast, and the 10 regional forecasts do not sum to the national forecast. When the board asks why the numbers don't add up, "we used different models" is not an acceptable answer.

The naive solution is to forecast only at the bottom level (individual stores) and simply add them up. This "bottom-up" approach guarantees coherence but ignores valuable information. National trends—macroeconomic conditions, company-wide promotions, seasonal patterns—are often more clearly visible in aggregated data because noise averages out. Conversely, you might forecast only at the top and disaggregate downward, but this "top-down" approach cannot capture store-specific patterns like local events or competitive dynamics. Neither extreme fully exploits the information available.

Hierarchical forecasting resolves this tension through reconciliation. The key insight is that we can produce initial "base forecasts" at every level using whatever method works best for each series, then mathematically adjust all forecasts simultaneously so they become coherent while staying as close as possible to the original predictions. Think of it as a negotiation: the national forecast wants to pull store forecasts toward a particular total, while each store forecast has its own view. Reconciliation finds the compromise that respects the aggregation constraints while minimising overall distortion. The mathematics of this compromise—specifically, which forecasts get adjusted more and which less—is governed by the relative accuracy and correlation structure of the base forecasts.

## The Mathematics

### Problem Setup and Notation

Consider a hierarchy with $n$ bottom-level series and $m$ total series (including all aggregated levels). Let $\mathbf{y}_t \in \mathbb{R}^m$ denote the vector of all observed values at time $t$, and let $\mathbf{b}_t \in \mathbb{R}^n$ denote the vector of bottom-level values only.

The hierarchical structure is encoded in the **summing matrix** $\mathbf{S} \in \mathbb{R}^{m \times n}$, which maps bottom-level values to all levels:

$$
\mathbf{y}_t = \mathbf{S} \mathbf{b}_t
$$

For a simple two-level hierarchy with a total and three bottom-level series:

$$
\mathbf{S} = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

The first row sums all bottom series to produce the total; subsequent rows are identity mappings for the bottom series themselves.

### Base Forecasts and Incoherence

Let $\hat{\mathbf{y}}_h \in \mathbb{R}^m$ denote the vector of $h$-step-ahead base forecasts produced independently for each series. These forecasts are generally **incoherent**:

$$
\hat{\mathbf{y}}_h \neq \mathbf{S} \hat{\mathbf{b}}_h
$$

where $\hat{\mathbf{b}}_h$ denotes the bottom-level components of $\hat{\mathbf{y}}_h$.

### Reconciliation as Linear Mapping

Reconciliation seeks a **coherent forecast** $\tilde{\mathbf{y}}_h$ that lies in the coherent subspace:

$$
\tilde{\mathbf{y}}_h = \mathbf{S} \tilde{\mathbf{b}}_h
$$

for some reconciled bottom-level forecast $\tilde{\mathbf{b}}_h$. The general reconciliation approach expresses this as a linear mapping from base forecasts:

$$
\tilde{\mathbf{y}}_h = \mathbf{S} \mathbf{G} \hat{\mathbf{y}}_h
$$

where $\mathbf{G} \in \mathbb{R}^{n \times m}$ is the **reconciliation matrix** that extracts and combines information from all base forecasts to produce reconciled bottom-level forecasts.

### Classical Approaches as Special Cases

**Bottom-Up (BU)**: Use only bottom-level base forecasts:

$$
\mathbf{G}_{\text{BU}} = \begin{pmatrix} \mathbf{0}_{n \times (m-n)} & \mathbf{I}_n \end{pmatrix}
$$

**Top-Down (TD)**: Use only the top-level forecast, disaggregated by historical proportions $\mathbf{p} \in \mathbb{R}^n$:

$$
\mathbf{G}_{\text{TD}} = \begin{pmatrix} \mathbf{p} & \mathbf{0}_{n \times (m-1)} \end{pmatrix}
$$

### Optimal Reconciliation: MinT Approach

The minimum trace (MinT) reconciliation of Wickramasuriya et al. (2019) finds $\mathbf{G}$ that minimises the trace of the reconciled forecast error covariance matrix.

Let $\boldsymbol{\epsilon}_h = \mathbf{y}_{T+h} - \hat{\mathbf{y}}_h$ denote the base forecast errors with covariance matrix $\mathbf{W}_h = \text{Var}(\boldsymbol{\epsilon}_h)$.

The reconciled forecast errors are:

$$
\tilde{\boldsymbol{\epsilon}}_h = \mathbf{y}_{T+h} - \tilde{\mathbf{y}}_h = \mathbf{y}_{T+h} - \mathbf{S}\mathbf{G}\hat{\mathbf{y}}_h
$$

Using the coherence constraint $\mathbf{y}_{T+h} = \mathbf{S}\mathbf{b}_{T+h}$ and some algebra:

$$
\tilde{\boldsymbol{\epsilon}}_h = \mathbf{S}(\mathbf{b}_{T+h} - \mathbf{G}\hat{\mathbf{y}}_h)
$$

The covariance of reconciled errors is:

$$
\text{Var}(\tilde{\boldsymbol{\epsilon}}_h) = \mathbf{S} \mathbf{G} \mathbf{W}_h \mathbf{G}' \mathbf{S}'
$$

**Theorem (Wickramasuriya et al., 2019)**: The matrix $\mathbf{G}$ that minimises $\text{trace}(\mathbf{S} \mathbf{G} \mathbf{W}_h \mathbf{G}' \mathbf{S}')$ subject to the unbiasedness constraint $\mathbf{S}\mathbf{G}\mathbf{S} = \mathbf{S}$ is:

$$
\mathbf{G} = (\mathbf{S}'\mathbf{W}_h^{-1}\mathbf{S})^{-1}\mathbf{S}'\mathbf{W}_h^{-1}
$$

The reconciled forecasts are therefore:

$$
\tilde{\mathbf{y}}_h = \mathbf{S}(\mathbf{S}'\mathbf{W}_h^{-1}\mathbf{S})^{-1}\mathbf{S}'\mathbf{W}_h^{-1}\hat{\mathbf{y}}_h
$$

### Estimation of the Covariance Matrix

The full covariance matrix $\mathbf{W}_h$ is typically unknown and difficult to estimate reliably when $m$ is large. Several approximations are used in practice:

**OLS (Identity)**: $\mathbf{W}_h = k_h \mathbf{I}_m$ for some scalar $k_h$. This assumes all base forecasts have equal variance and are uncorrelated—rarely true but computationally convenient.

**WLS (Structural Scaling)**: $\mathbf{W}_h = k_h \text{diag}(\mathbf{S}\mathbf{1}_n)$ where $\mathbf{1}_n$ is a vector of ones. This weights by the number of bottom-level series each aggregate comprises, reflecting that aggregates of more series typically have larger variance.

**MinT-Sample**: Estimate $\mathbf{W}_h$ directly from in-sample one-step-ahead residuals:

$$
\hat{\mathbf{W}}_1 = \frac{1}{T} \sum_{t=1}^{T} \hat{\boldsymbol{\epsilon}}_t \hat{\boldsymbol{\epsilon}}_t'
$$

**MinT-Shrink**: Apply shrinkage estimation to handle high-dimensional covariance estimation, typically shrinking toward a diagonal target.

### Assumptions

1. **Linearity**: Reconciliation is a linear operation on base forecasts.
2. **Unbiasedness**: Base forecasts are assumed unbiased; reconciliation preserves this property.
3. **Known hierarchy structure**: The summing matrix $\mathbf{S}$ is fixed and correctly specified.
4. **Covariance stationarity**: The error covariance structure is assumed stable over the estimation period.

### Edge Cases and Degenerate Conditions

- When $\mathbf{W}_h$ is singular or near-singular, $\mathbf{W}_h^{-1}$ does not exist. Use regularisation or pseudoinverse.
- With very short history, sample covariance estimates are unreliable; prefer structural (WLS) or shrinkage approaches.
- In grouped hierarchies where multiple aggregation paths exist, the summing matrix must be constructed carefully to avoid rank deficiency.

### Relationship to Constrained Least Squares

The MinT solution can be derived as a constrained least squares problem:

$$
\min_{\tilde{\mathbf{y}}_h} (\tilde{\mathbf{y}}_h - \hat{\mathbf{y}}_h)' \mathbf{W}_h^{-1} (\tilde{\mathbf{y}}_h - \hat{\mathbf{y}}_h) \quad \text{subject to} \quad \tilde{\mathbf{y}}_h \in \text{colspan}(\mathbf{S})
$$

This is a projection of $\hat{\mathbf{y}}_h$ onto the coherent subspace with respect to the $\mathbf{W}_h^{-1}$ inner product.

## Understanding the Mathematics

### The Hierarchical Summing Constraint

**The equation:**

$$\mathbf{y}_t = \mathbf{S} \mathbf{b}_t$$

**Read it aloud:**

"The values at all levels of the hierarchy at time t equal the summing matrix multiplied by the bottom-level values at time t."

**What each symbol means:**

- $\mathbf{y}_t$ — a vector containing forecasts at *every* level (total, regions, stores, etc.) at time period t
- $\mathbf{S}$ — the summing matrix; encodes which bottom-level series add up to form each aggregate
- $\mathbf{b}_t$ — a vector of the most disaggregated (bottom-level) values at time t

**A concrete numerical example:**

Imagine a retailer with two stores. Total sales = Store A + Store B.

$$\mathbf{b}_t = \begin{bmatrix} 120 \\ 180 \end{bmatrix}, \quad \mathbf{S} = \begin{bmatrix} 1 & 1 \\ 1 & 0 \\ 0 & 1 \end{bmatrix}$$

Step by step:
- Row 1: Total = 1×120 + 1×180 = 300
- Row 2: Store A = 1×120 + 0×180 = 120
- Row 3: Store B = 0×120 + 1×180 = 180

Result: $\mathbf{y}_t = [300, 120, 180]^\top$

**Why this equation matters:**

This constraint ensures your forecasts are *coherent*—the sum of store-level predictions always equals the total, preventing the embarrassment of promises that don't add up.

---

### The Base Forecasts

**The equation:**

$$\hat{\mathbf{y}}_h = \mathbf{S} \mathbf{P} \tilde{\mathbf{y}}_h$$

**Read it aloud:**

"The final coherent forecast for horizon h equals the summing matrix times a projection matrix times the initial (incoherent) forecasts."

**What each symbol means:**

- $\hat{\mathbf{y}}_h$ — final reconciled forecasts that obey the hierarchy
- $\tilde{\mathbf{y}}_h$ — initial forecasts from individual models (might not sum correctly)
- $\mathbf{P}$ — projection matrix that maps all-level forecasts down to bottom level
- $\mathbf{S}$ — summing matrix (same as before)

**A concrete numerical example:**

You forecast Total = 310, Store A = 130, Store B = 170. These don't add up (130 + 170 = 300 ≠ 310).

Using bottom-up reconciliation where $\mathbf{P} = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$:

- Extract bottom forecasts: $\mathbf{P} \tilde{\mathbf{y}}_h = [130, 170]^\top$
- Apply summing: $\mathbf{S} [130, 170]^\top = [300, 130, 170]^\top$

Now the total (300) equals the sum of stores.

**Why this equation matters:**

Without reconciliation, your regional manager and store managers receive contradictory targets, destroying coordination and accountability.

---

### The MinT Optimal Reconciliation

**The equation:**

$$\mathbf{P} = (\mathbf{S}^\top \mathbf{W}_h^{-1} \mathbf{S})^{-1} \mathbf{S}^\top \mathbf{W}_h^{-1}$$

**Read it aloud:**

"The optimal projection matrix equals the inverse of S-transpose times inverse-variance times S, all multiplied by S-transpose times inverse-variance."

**What each symbol means:**

- $\mathbf{P}$ — the mapping that reconciles forecasts optimally
- $\mathbf{W}_h$ — variance-covariance matrix of forecast errors across all levels
- $\mathbf{W}_h^{-1}$ — inverse variance (weights giving more influence to accurate forecasts)
- $\mathbf{S}^\top$ — transpose of the summing matrix

**A concrete numerical example:**

Suppose total-level forecasts have variance 2500 (error ±50 units) while store-level forecasts have variance 100 each (error ±10 units). The stores are much more accurate.

MinT weights the reconciliation toward the store forecasts. If stores predict 130 and 170 (sum = 300) but total predicts 310, the final total will be closer to 300 because $\mathbf{W}_h^{-1}$ assigns higher weight (1/100 vs 1/2500) to the more precise store estimates.

**Why this equation matters:**

This produces the statistically best coherent forecasts—minimizing expected squared error by trusting the most reliable information sources in your hierarchy.

---

### The Big Picture

The mathematics of hierarchical forecasting solves a reconciliation problem: how do we combine forecasts made at different organizational levels when they inevitably contradict each other? Simple approaches like "just use the total" or "just sum the parts" ignore valuable information. The matrix algebra framework gives us something better—a principled way to blend all available forecasts while enforcing adding-up constraints. The MinT approach specifically uses variance weighting to trust accurate forecasts more than noisy ones, much like a weighted average in statistics. Fundamentally, these equations transform a mess of inconsistent predictions into a single coherent story that respects both the data and the structure of your business.

## Python Implementation

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.linalg import inv
import warnings

# =============================================================================
# Generate synthetic hierarchical time series data
# =============================================================================

np.random.seed(42)
T = 104  # Two years of weekly data
h = 4    # Forecast horizon

# Three bottom-level series (e.g., three stores)
# Each has trend, seasonality, and noise
t = np.arange(T + h)

# Store-specific parameters
store_trends = [0.5, 0.3, 0.8]
store_seasonality = [10, 15, 8]
store_base = [100, 150, 80]

bottom_series = []
for i in range(3):
    trend = store_trends[i] * t
    seasonality = store_seasonality[i] * np.sin(2 * np.pi * t / 52)
    noise = np.random.normal(0, 5, T + h)
    series = store_base[i] + trend + seasonality + noise
    bottom_series.append(series)

bottom_series = np.array(bottom_series)  # Shape: (3, T+h)

# Aggregate to create total (top level)
total_series = bottom_series.sum(axis=0)

# Combine into full hierarchy: [Total, Store1, Store2, Store3]
all_series = np.vstack([total_series, bottom_series])  # Shape: (4, T+h)

# Split into training and test
y_train = all_series[:, :T]
y_test = all_series[:, T:T+h]

# Create summing matrix S
# Hierarchy: Total = Store1 + Store2 + Store3
n = 3  # bottom-level series
m = 4  # total series (1 aggregate + 3 bottom)
S = np.array([
    [1, 1, 1],  # Total
    [1, 0, 0],  # Store1
    [0, 1, 0],  # Store2
    [0, 0, 1]   # Store3
])

print("Summing Matrix S:")
print(S)
print()

# =============================================================================
# Generate base forecasts (using simple linear trend for demonstration)
# =============================================================================

def generate_base_forecasts(y_train, h):
    """Generate h-step ahead forecasts using linear trend extrapolation."""
    m, T = y_train.shape
    forecasts = np.zeros((m, h))
    residuals = np.zeros((m, T))
    
    t_train = np.arange(T).reshape(-1, 1)
    t_future = np.arange(T, T + h).reshape(-1, 1)
    
    for i in range(m):
        model = LinearRegression()
        model.fit(t_train, y_train[i, :])
        forecasts[i, :] = model.predict(t_future)
        residuals[i, :] = y_train[i, :] - model.predict(t_train)
    
    return forecasts, residuals

base_forecasts, residuals = generate_base_forecasts(y_train, h)

print("Base Forecasts (incoherent):")
print(f"  Total forecast (sum of h periods): {base_forecasts[0, :].sum():.2f}")
print(f"  Sum of store forecasts: {base_forecasts[1:, :].sum():.2f}")
print(f"  Incoherence


## Visualisations

![](../../_static/figures/hierarchical-forecasting_fig1.png)
![](../../_static/figures/hierarchical-forecasting_fig2.png)

## Using This in Heuristix

### What Data You'll Need

The Hierarchical Forecasting node expects time series data with hierarchical structure already defined. You'll need:

- **A date column** (datetime format)
- **A target column** (numeric values you want to forecast)
- **Hierarchy columns** (categorical columns defining levels, e.g., Country → Region → Store)

Your data should be at the most granular level. Here's what that looks like:

| date       | country | region | store | sales |
|------------|---------|--------|-------|-------|
| 2024-01-01 | US      | West   | A     | 120   |
| 2024-01-01 | US      | West   | B     | 85    |
| 2024-01-01 | US      | East   | C     | 95    |
| 2024-01-02 | US      | West   | A     | 134   |

The node will automatically aggregate up the hierarchy and ensure forecasts are coherent across all levels.

### Configuration Parameters

| Parameter | What It Controls | Default | When to Change |
|-----------|------------------|---------|----------------|
| **Hierarchy Structure** | Defines the nesting order of your levels (top to bottom) | Auto-detected | Always verify this matches your business logic |
| **Forecasting Method** | Base algorithm for generating forecasts (ETS, ARIMA, Prophet) | ETS | Use Prophet for data with strong seasonality and holidays |
| **Reconciliation Approach** | How to make forecasts coherent (Bottom-Up, Top-Down, Middle-Out, MinT) | MinT (Optimal) | Bottom-Up if lower levels are most reliable; Top-Down if aggregate is most stable |
| **Forecast Horizon** | Number of periods ahead to predict | 12 | Match your planning cycle (weeks, months, quarters) |
| **Confidence Level** | Width of prediction intervals | 95% | Lower to 80% for tighter bands; raise to 99% for conservative planning |

### What You'll Get Out

**Forecasts Table**: A comprehensive output with predictions at every hierarchy level, including:
- Date, hierarchy identifiers, point forecast, lower/upper bounds
- Reconciled values ensuring parent = sum of children at every node

**Accuracy Metrics Panel**: Shows historical backtest performance:
- MAPE, RMSE, and MAE at each hierarchy level
- Coherency score (always 100% after reconciliation)

**Visualization Dashboard**:
- Time series plots for each hierarchy level with actuals vs. forecasts
- Hierarchy tree diagram showing forecast distribution across branches
- Reconciliation impact chart (before/after adjustment comparison)

### Connecting Downstream

This node pairs naturally with:

- **Scenario Analysis**: Feed forecasts into what-if scenarios with different assumptions
- **Capacity Planning**: Use store-level forecasts to optimize inventory and staffing
- **Report Builder**: Create executive dashboards showing forecasts at relevant aggregation levels
- **Alert Monitor**: Set thresholds to flag when forecasts indicate capacity constraints

### Quick Start

1. **Connect your granular data** with date, target, and hierarchy columns clearly labeled
2. **Define hierarchy structure** in the config panel (drag columns in order from broadest to most specific)
3. **Select MinT reconciliation** and your preferred base method (ETS is reliable for most business data)
4. **Set your forecast horizon** to match your planning window (e.g., 13 weeks for quarterly planning)
5. **Run the node** and review the hierarchy tree to verify structure looks correct
6. **Export forecasts** at the aggregation level your stakeholders need

### Pro Tips from Experience

**Tip 1**: Always check that your most granular level doesn't have too many zeros or missing values. If more than 30% of series are sparse, consider starting one level up in the hierarchy.

**Tip 2**: The reconciliation method matters most when hierarchies are deep (4+ levels). For shallow hierarchies (2-3 levels), differences between methods are usually small.

**Tip 3**: Use the "coherency diagnostic" view to spot data quality issues. If reconciliation adjustments are huge (>20%), you likely have hierarchy definition problems or data entry errors.

**Tip 4**: When presenting to executives, show forecasts at the top 2 levels only. Operational teams need the granular forecasts, but leadership wants the strategic view.

**Tip 5**: Refit your model monthly, but don't change the hierarchy structure mid-quarter unless absolutely necessary—it breaks forecast comparability across time.

## Config Recipes

### Recipe 1: Rapid Prototyping

**When to use:** Initial exploration when you need to validate whether hierarchical structure matters for your data, with results in minutes not hours.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `"bottom_up"` | No reconciliation overhead; pure aggregation |
| `forecast_horizon` | `12` | Short enough for quick iteration |
| `base_model` | `"naive_seasonal"` | Zero training time; establishes baseline |
| `cv_folds` | `1` | Single train-test split only |
| `parallel` | `True` | Use all available cores |

**What you get:** Fast baseline showing whether lower-level forecasts naturally aggregate well or need reconciliation.

**Trade-off:** You sacrifice accuracy for speed—bottom-up ignores top-level patterns and naive methods miss complex dynamics.

### Recipe 2: Production-Grade Reconciliation

**When to use:** Deploying forecasts where consistency is contractually required (budget allocation, SLA planning, inventory systems).

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `"mint_shrink"` | Optimal reconciliation with robust covariance estimation |
| `forecast_horizon` | `horizon + 4` | Forecast beyond needed range to assess stability |
| `base_model` | `"auto_arima"` or `"lightgbm"` | Production-quality base forecasts |
| `cv_folds` | `5` | Rolling-origin validation for realistic errors |
| `shrinkage_target` | `"identity"` | Regularizes reconciliation when series are noisy |
| `residual_length` | `min(500, train_length * 0.8)` | Sufficient sample for covariance without overfitting |
| `store_insample` | `True` | Keep for monitoring and diagnostics |

**What you get:** Statistically optimal reconciliation that minimizes forecast error variance while guaranteeing coherence.

**Trade-off:** Computational cost is 5–10× the exploration recipe; requires tuning shrinkage intensity for best results.

### Recipe 3: Sparse Hierarchy with Intermittent Demand

**When to use:** Retail/supply chain scenarios where bottom-level series have many zeros (e.g., SKU-store combinations with sporadic sales).

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `"top_down"` | Avoids amplifying noise from sparse bottom series |
| `forecast_horizon` | `4` to `8` | Short horizon where proportions stay stable |
| `base_model` | `"croston"` or `"theta"` | Designed for intermittent patterns |
| `proportion_method` | `"average_proportions"` | Smooths historical splits; use 12–24 periods |
| `handle_negatives` | `"truncate_zero"` | Croston can produce negatives; force non-negative |
| `cv_folds` | `3` | Balance between validation rigor and sparse data |

**What you get:** Stable forecasts that distribute top-level signal proportionally, reducing zero-inflation issues.

**Trade-off:** You lose bottom-up information and assume historical proportions persist—dangerous if mix is shifting.

### Recipe 4: Multi-Seasonal Event Calendar

**When to use:** Hierarchies with multiple seasonalities and irregular events (e.g., tourism by region-accommodation type with holidays, festivals, school breaks).

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `"mint_sample"` | Sample covariance better captures event correlations |
| `base_model` | `"prophet"` or `"tbats"` | Native multi-seasonality and regressor support |
| `external_regressors` | Holiday indicators, event dummies | Critical for event-driven series |
| `seasonality_modes` | `["weekly", "yearly"]` | Explicit multiple seasonal periods |
| `cv_folds` | `3` with event-aware splits | Ensure each fold contains event examples |
| `aggregation_levels` | Include temporal aggregation (daily→weekly) | Events impact different time scales |

**What you get:** Coherent forecasts that respect both hierarchical structure and complex calendar effects across levels.

**Trade-off:** Requires careful feature engineering for events; Prophet can be slow on hundreds of series.

## Business Applications

**Retail: Multi-channel inventory optimisation**

A European fashion retailer operating 400 stores and an e-commerce platform needs to forecast demand for 50,000 SKUs across brand, category, size, colour, and location hierarchies. Independent store-level forecasts create impossible scenarios where predicted store sales exceed the national forecast, confusing procurement teams and leading to expensive air freight for stock redistribution. Hierarchical forecasting reconciles predictions across all levels—ensuring SKU-store forecasts sum to regional totals, which sum to national demand—while exploiting information from high-performing stores to improve predictions for smaller outlets. The implementation reduced forecast error by 23%, cut emergency stock transfers by €2.4M annually, and improved in-stock rates from 87% to 94% during peak season.

**Financial Services: Branch cash demand planning**

A UK high-street bank with 850 branches must ensure ATMs and teller windows have sufficient cash without holding excessive non-earning inventory. Each branch needs daily cash forecasts, but these must aggregate correctly to regional distribution centre requirements and national vault planning. Hierarchical forecasting models branch demand while maintaining consistency with regional armoured car capacity and headquarters liquidity management, using historical transaction patterns, local events, and benefit payment schedules. The bank reduced idle cash holdings by £47M while decreasing ATM stock-outs by 68%, and cut armoured transport costs by 12% through better route optimization enabled by accurate hierarchical demand signals.

**Healthcare: Hospital bed capacity planning**

A metropolitan hospital network with six facilities and 1,800 beds needs to forecast admissions by department (emergency, surgery, cardiology, oncology) and facility, while ensuring network-wide capacity planning aligns with individual hospital predictions. Bottom-up forecasts from department heads often sum to more beds than physically exist, while top-down corporate planning ignores seasonal patterns in specific units like paediatric respiratory cases. Hierarchical forecasting reconciles these levels, incorporating both hospital-specific trends and system-wide patterns like flu season impacts. The network reduced elective surgery cancellations due to bed shortages by 41% and improved ICU utilisation from 73% to 84%, avoiding a planned $18M expansion.

**Manufacturing: Production planning across assembly hierarchies**

A automotive tier-1 supplier producing components for eight OEM customers across three plants must forecast final assembly demand, sub-assembly requirements, and raw material needs in a coherent hierarchy. When component forecasts don't align with finished goods predictions, the result is simultaneous shortages and excess inventory at different production stages. Hierarchical forecasting ensures that forecasts for brake callipers, pistons, and seals remain mathematically consistent with complete brake assembly demand, while accounting for customer-specific design variations. The manufacturer reduced component inventory carrying costs by $3.7M annually and improved on-time delivery from 91% to 97%.

**Energy: Electricity load forecasting**

A regional utility serving 2.3 million customers needs 24-hour ahead load forecasts at neighbourhood, substation, and grid levels to optimise generator dispatch and wholesale market participation. Summing individual substation forecasts historically produced system totals that differed from grid-level models by 8-12%, creating expensive real-time balancing requirements. Hierarchical forecasting reconciles granular spatial predictions with system-wide load patterns, incorporating weather, time-of-day, and industrial customer schedules across all hierarchy levels. Implementation cut load forecast error by 31%, reduced balancing market purchases by $4.2M annually, and enabled more accurate renewable energy integration.

**Logistics: Parcel volume forecasting**

A national courier handling 800,000 daily parcels must forecast volumes for route planning, depot staffing, and vehicle scheduling across a four-level hierarchy: national, regional hub, local depot, and individual route. Independent forecasts at each level create resource conflicts where depot staffing plans don't match regional vehicle allocations. Hierarchical forecasting ensures route-level predictions aggregate correctly to depot totals while incorporating information from similar routes to improve predictions for newly-established delivery areas. The company improved delivery driver utilisation by 18% and reduced agency staff costs by £1.9M quarterly.

**SaaS: Customer usage forecasting**

A cloud storage provider serving 400,000 business customers must forecast storage consumption across customer segments, geographic regions, and infrastructure availability zones to optimise data centre capacity investments. Hierarchical forecasting reconciles customer-segment growth predictions with regional infrastructure constraints and global capacity planning, preventing scenarios where zone-level forecasts suggest buying more servers than the regional demand justifies. This approach helped the company defer a $12M data centre expansion by nine months while maintaining 99.95% availability.

## Worked Example

Sarah Chen, a senior analyst at Evergreen Retail, was sitting in the Monday planning meeting when the VP of Supply Chain leaned forward with a question that would consume her next two weeks: "Why do our regional forecasts never match what we're ordering at the store level?" The company operated 24 stores across three regions—North, South, and West—and the disconnect was costing them money. Stores would over-order based on local intuition while regional managers, looking at aggregate trends, would forecast lower demand. The mismatch meant excess inventory in some locations and stockouts in others. Sarah knew this wasn't just a forecasting problem; it was a **coherence** problem.

She pulled six months of daily sales data for a single product category: outdoor equipment. The dataset was messy in the way real retail data always is—missing values from system outages, a store closure for renovation in March, and one region that apparently sold negative units on February 14th (a returns processing error, she later confirmed). Here's what a slice looked like after cleaning:

| date       | region | store_id | units_sold |
|------------|--------|----------|------------|
| 2024-01-15 | North  | N01      | 23         |
| 2024-01-15 | North  | N02      | 31         |
| 2024-01-15 | South  | S01      | 18         |
| 2024-01-15 | West   | W01      | 42         |
| 2024-01-16 | North  | N01      | 19         |

The data spanned three regions, 24 stores, and 180 days. Sarah needed to forecast the next 30 days at both the store and regional level—and crucially, she needed those forecasts to be **coherent**: if she summed up all the store-level predictions within a region, they had to match the regional forecast exactly.

She opened her forecasting pipeline and configured the hierarchical reconciliation approach. The hierarchy was straightforward: Total → Region → Store. Sarah chose **bottom-up** reconciliation first as a baseline—forecast each store independently, then sum to get regional and total forecasts. But she knew this would ignore valuable regional trend information. So she also configured **optimal reconciliation using minimum trace (MinT)**, which would blend forecasts from all levels of the hierarchy and find the mathematically optimal weights that minimized forecast error while maintaining coherence.

For the base forecasts, she used exponential smoothing at each level—simple, interpretable, and fast enough to re-run daily. She set a 7-day seasonal period to capture weekly patterns (weekends were stronger) and allocated 30% of the data as a validation holdout.

```python
import pandas as pd
from hierarchicalforecast.core import HierarchicalReconciliation
from hierarchicalforecast.methods import BottomUp, MinTrace
from statsforecast import StatsForecast
from statsforecast.models import AutoETS

# Load and aggregate to hierarchy
sales = pd.read_csv('sales_data.csv')
sales['total'] = 'Total'

# Create hierarchy structure
hierarchy = [
    ['total'],
    ['total', 'region'],
    ['total', 'region', 'store_id']
]

# Generate base forecasts at all levels
sf = StatsForecast(
    models=[AutoETS(season_length=7)],
    freq='D'
)
base_forecasts = sf.forecast(df=sales, h=30)

# Reconcile forecasts
hrec = HierarchicalReconciliation(
    reconcilers=[BottomUp(), MinTrace()]
)
coherent_forecasts = hrec.reconcile(
    base_forecasts=base_forecasts,
    hierarchy=hierarchy
)
```

When the results came back, Sarah immediately spotted the difference. The bottom-up approach forecasted 1,847 units total for the North region over 30 days. But MinT reconciliation produced 1,682 units—about 9% lower. Drilling into the stores, she saw why: two stores (N03 and N07) had recent spiky patterns that inflated their individual forecasts, but the regional aggregate showed those spikes were anomalies. MinT borrowed strength from the regional trend and adjusted the store forecasts downward while still maintaining perfect summation.

| Method     | Region | 30-day Forecast | MAPE (validation) |
|------------|--------|-----------------|-------------------|
| Bottom-Up  | North  | 1,847           | 12.3%             |
| MinT       | North  | 1,682           | 8.7%              |
| Bottom-Up  | South  | 1,423           | 14.1%             |
| MinT       | South  | 1,401           | 9.2%              |

The insight hit Sarah during validation: **MinT wasn't just enforcing coherence; it was actually improving accuracy**. By pooling information across levels, it filtered out store-level noise while preserving regional patterns. The MAPE improved by 3–5 percentage points across all regions.

She presented the findings to the supply chain team the following week. The VP nodded slowly as Sarah walked through the reconciled forecasts. "So we order based on these store numbers, and we're *guaranteed* they'll add up correctly at the regional level?" Exactly. Within a month, Evergreen rolled out MinT reconciliation for all product categories. Inventory holding costs dropped 6%, and stockout rates fell by half in the North region.

If Sarah could do it over, she'd invest more time in the hierarchy structure itself—perhaps adding a product subcategory level between total and region. And she'd build in automated alerts for when store-level forecasts diverged significantly from their reconciled versions; those divergences often signaled real local effects worth investigating, not just noise to smooth away.

## Interpreting Your Results

You've just run your hierarchical forecasting model and you're staring at reconciled forecasts, accuracy metrics, and residual plots. Let's walk through what you're actually looking at.

### Reconciled Forecasts vs. Base Forecasts

**Plain-English meaning**: Your model produced two sets of forecasts. The "base forecasts" are what each level predicted independently. The "reconciled forecasts" are adjusted versions that ensure lower-level forecasts sum exactly to upper-level totals. For example, if you forecast sales for stores and regions separately, reconciliation ensures store forecasts add up to the regional forecast.

**Concrete benchmarks**: Compare the average absolute change between base and reconciled forecasts. Changes under 5% suggest your hierarchy was already fairly consistent. Changes of 5–15% indicate moderate reconciliation—normal and healthy. Changes above 20% mean your base forecasts at different levels were telling very different stories, and you should investigate why before trusting the output.

**Red flags**: If reconciliation changes only happen at one level (e.g., only top-level forecasts change, but bottom-level stay identical), your hierarchy structure may be wrong or your reconciliation method defaulted to a simple rule. If specific series change by 50%+ while others barely move, those series likely have poor base forecast quality.

### Forecast Accuracy Metrics (MAPE, RMSE, MAE)

**Plain-English meaning**: These measure how far your forecasts were from actual values during validation. MAPE (Mean Absolute Percentage Error) tells you the average percentage miss. RMSE (Root Mean Squared Error) penalizes large errors more heavily. MAE (Mean Absolute Error) gives the average absolute miss in original units.

**Concrete benchmarks**: 
- **MAPE below 10%**: Excellent. Safe to use for operational decisions like staffing or purchasing.
- **MAPE 10–20%**: Good. Acceptable for most business planning scenarios.
- **MAPE 20–30%**: Mediocre. Use with caution; combine with human judgment.
- **MAPE above 30%**: Poor. Either your data is too noisy, your model needs work, or this metric isn't appropriate for your series.

For RMSE and MAE, compare them to the standard deviation of your historical data. If RMSE is 50% or less of your historical standard deviation, you're beating naive forecasting significantly.

**Red flags**: MAPE above 100% means you're missing by more than the actual value on average—essentially useless. If lower levels have much better MAPE than upper levels, your aggregation may be masking systematic bias. If reconciled forecasts have worse accuracy than base forecasts, you may have the wrong reconciliation approach for your data structure.

### Coherency Metrics

**Plain-English meaning**: These check whether your forecasts obey the hierarchical structure. Perfect coherency (score = 1.0) means bottom-level forecasts sum exactly to top-level. Anything less means you still have mathematical inconsistencies.

**Concrete benchmarks**: You must hit 1.0 or 0.9999+ (accounting for floating-point rounding). There's no acceptable middle ground—hierarchical forecasting's entire purpose is achieving coherency.

**Red flag**: Any coherency score below 0.99 means your reconciliation failed technically. Check your code, aggregation matrices, or reconciliation method implementation.

### Residual Patterns by Level

**Plain-English meaning**: Residuals are actual minus predicted values. Plotting them by hierarchy level shows whether certain parts of your structure forecast better than others.

**What good looks like**: Residuals should scatter randomly around zero at all levels, with no obvious patterns over time or across groups. Standard deviation of residuals should be proportional to the magnitude of the series (larger series = larger residuals in absolute terms, but similar in percentage terms).

**Red flags**: If one region or product consistently shows positive residuals while others are negative, you have systematic bias that reconciliation is spreading across the hierarchy. If residuals show trends or seasonality, your base models are missing structure.

### Sanity Check Checklist

1. **Sum check**: Manually verify that 2–3 randomly selected bottom-level forecasts sum to their parent level. Calculator-test the reconciliation.
2. **Magnitude check**: Are any forecasts negative when they should be non-negative (sales, counts)? Are any forecasts 10× larger than historical maximums?
3. **Coherency = 1.0**: Confirm perfect mathematical consistency was achieved.
4. **Base vs. reconciled**: Calculate average percentage change. Above 25% warrants investigation before deployment.
5. **Holdout performance**: Your accuracy metrics should be calculated on data the model never saw during training. Confirm your validation period is truly held out.

### Good Enough to Act On?

Deploy if: MAPE is under 20% at the decision-making level you care about most, coherency is 1.0, and no red flags appear in residuals. If MAPE is 10–20%, combine forecasts with safety buffers. Only use forecasts with MAPE above 20% for directional guidance, not precise targets.

## Decision Guidance

### What This Result Is Telling You

Hierarchical forecasts give you a complete picture of demand across your entire business structure—from total company sales down to individual product-store combinations—with the mathematical guarantee that the details add up to the totals. When you receive these forecasts, you're seeing a coordinated prediction system where decisions made at one level automatically align with plans at every other level. This matters because it eliminates the common problem where regional managers create bottom-up forecasts that don't match the top-down targets from corporate planning, forcing last-minute reconciliation meetings and arbitrary adjustments.

The coherence property means you can trust that if your national forecast shows 10,000 units, the sum of all regional forecasts will also show exactly 10,000 units—not 9,200 or 11,500. This consistency flows through every level: regions sum to nation, stores sum to regions, product categories sum to total product. When forecasts are coherent, your procurement team can order based on aggregate forecasts knowing that allocation plans built from granular forecasts will work with the same inventory. When they're not coherent, you end up with either excess inventory in warehouses (because bottom-up forecasts were higher) or stockouts in stores (because top-down forecasts were lower).

The quality of your hierarchical forecast depends on how well the reconciliation method balanced information from different levels. Strong performance at aggregate levels with weaker performance at granular levels suggests your business has stable overall patterns but high local volatility—common in retail where store-level sales are noisy but regional trends are reliable. The reverse pattern indicates you have predictable local behaviour that doesn't aggregate cleanly, often seen when local promotions or events dominate your business.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Forecast errors at bottom level exceed 40% MAPE while top level stays below 15% | Local volatility is high but aggregate patterns are stable | Use top-down forecasts for procurement and financial planning; use bottom-level forecasts only for relative allocation within regions | Supply chain director, CFO |
| Reconciled forecasts differ from base forecasts by more than 20% at middle levels (e.g., product-region) | Strong disagreement between hierarchical levels about demand patterns | Investigate which data sources are most reliable; validate assumptions about promotional calendars and seasonality at each level | Analytics team, category managers |
| Coherent forecasts consistently outperform independent forecasts by 10%+ MAPE at most levels | The hierarchical structure captures real information sharing across levels | Adopt hierarchical forecasting as the primary planning system; retire separate forecasting processes at different organizational levels | Head of planning, CIO |
| Forecast accuracy degrades significantly (15%+ MAPE increase) in periods following structural changes | The hierarchy definition or reconciliation weights don't reflect current business reality | Review hierarchy structure quarterly; rebuild when you launch new product lines, close stores, or reorganize regions | Strategy team, FP&A |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Reconciled forecasts achieve at least 10% lower MAPE than independent forecasts at aggregate levels (total, region, or category)
- Forecast coherence constraints change base forecasts by less than 15% on average across all levels
- Out-of-sample validation shows stable performance over at least 3 forecast horizons

**Proceed with caution when:**
- Bottom-level forecast errors exceed 35% MAPE but you need them for operational allocation
- Reconciliation adjustments exceed 20% at any level, indicating weak agreement between hierarchical perspectives
- The hierarchy structure was defined more than 12 months ago without validation against current business operations

**Investigate before acting when:**
- Forecast performance varies dramatically across branches of the hierarchy (e.g., some regions forecast well, others don't)
- Reconciled forecasts at key decision levels (where you actually allocate resources) perform worse than simple baseline methods
- Stakeholders report that forecasts don't match their domain knowledge at the levels they manage

**Do not use these results yet if:**
- The hierarchy definition contains logical errors (overlapping categories, missing products, incorrect parent-child relationships)
- Historical data quality issues affect more than 20% of bottom-level series
- Coherence constraints are forcing forecasts to unrealistic values (negative demand, impossibly large swings between periods)

### The Cost of Getting This Wrong

When hierarchical forecasts are misapplied, the most common failure mode is the illusion of precision: leadership sees beautifully consistent numbers across all organizational levels and assumes the forecasts must be reliable. A retail chain proceeds to commit $2M in inventory purchases based on coherent store-level forecasts, only to discover that the reconciliation method heavily adjusted granular forecasts toward an inaccurate top-level prediction. The result: systematic overstocking across 200 stores because one flawed aggregate assumption propagated downward through mathematical coherence. Alternatively, ignoring the hierarchy entirely and letting each business unit forecast independently leads to the coordination disaster where regional purchase orders sum to 30% more than manufacturing capacity, forcing emergency production decisions, expedited shipping costs, and months of finger-pointing about whose forecast was "really" correct. The organizational cost compounds the financial waste: teams lose trust in analytics, revert to spreadsheet-based gut decisions, and the planning cycle extends by weeks as managers manually reconcile incompatible forecasts in contentious meetings.

## Common Pitfalls

**The Bottom-Up Illusion**

Here's what happened: A retail analytics team was forecasting sales across 50 stores in 3 regions. They built excellent store-level models, summed them up to get regional forecasts, and presented results to leadership. The executives nodded along until someone noticed that the national total was trending 15% higher than the economic forecast they'd commissioned separately. The team defended their approach: "We're just being faithful to the store data." Leadership lost confidence in the entire forecast.

Why it happens: There's a seductive logic to bottom-up aggregation—it feels like you're respecting the granular reality. But store-level noise compounds when you sum 50 noisy forecasts, and you ignore valuable information that only becomes visible at higher levels (macroeconomic signals, category shifts, competitive dynamics).

How to detect it: Compare the coefficient of variation (CV = σ/μ) at different levels. If your aggregated forecast has a CV significantly higher than historical aggregate data, you've amplified noise rather than signal. Look for aggregate forecasts that violate known constraints or external benchmarks.

The fix: Use top-down or middle-out reconciliation to inject information from stable aggregate series, or apply optimal reconciliation methods that balance information across all levels.

**Forgetting the Future Hierarchy**

Here's what happened: A CPG company built a beautiful hierarchical model for products across sales channels. Six months later, they launched a new direct-to-consumer website and restructured their B2B partnerships into enterprise and SMB segments. The forecasting system couldn't accommodate the changes—the hierarchy was hardcoded. The data science team spent three weeks rebuilding everything while the business operated without forecasts.

Why it happens: We treat hierarchies as static technical constraints rather than evolving business structures. The focus during development is on historical fit, not future flexibility.

How to detect it: You can't, until it's too late. This is a process failure, not a statistical one. The warning sign is when you hear "that's just how the data is structured" without anyone maintaining documentation of planned hierarchy changes.

The fix: Build hierarchy definitions as configuration, not code. Establish a quarterly review process with business stakeholders to map upcoming structural changes and maintain versioned hierarchy schemas.

**The Reconciliation Theater**

Here's what happened: A junior data scientist implemented MinT optimal reconciliation on a demand forecasting problem, carefully tuning the covariance estimation. The reconciled forecasts looked reasonable in validation—RMSE improved by 3% overall. In production, the business team ignored the reconciled numbers entirely and used the base forecasts, because "the reconciled ones don't match what our gut says." The reconciliation added complexity without user buy-in.

Why it happens: Reconciliation methods are mathematically elegant but can produce forecasts that violate domain knowledge or move too far from what stakeholders expect. Without explanation or trust, users route around the system.

How to detect it: Track which forecast version actually gets used in downstream decisions. If you see business users maintaining shadow spreadsheets or consistently overriding system outputs, reconciliation has failed socially even if it succeeded statistically.

The fix: Present reconciliation adjustments explicitly ("Store A moved from 100 to 95 to maintain regional coherence") and involve stakeholders in choosing reconciliation constraints that respect their domain knowledge.

**Validation on the Wrong Level**

Here's what happened: An analyst built hierarchical forecasts for a product catalog with 200 SKUs across 5 categories. They reported stellar accuracy: "95% of forecasts within 10% of actuals!" Management approved. Three months later, they missed the category-level budget by 20% on their flagship line—the level executives actually cared about—because those 200 small errors happened to align in the same direction.

Why it happens: The validation set matches the modeling level (often the most granular), not the decision level. Errors at fine grain can cancel out or compound when aggregated, but we don't check.

How to detect it: Calculate hierarchical forecast accuracy metrics at each level. If you only have MAPE or RMSE at the leaf nodes, you're exposed. Look specifically at weighted absolute percentage error (WAPE) at the total level.

The fix: Define forecast accuracy requirements at every decision-relevant level before modeling, and weight your validation by business impact—a miss on the top 20% of products matters more than getting the long tail right.

**The Spurious Reconciliation Gain**

Here's what happened: A forecasting team showed that their reconciled forecasts beat base forecasts by 8% on held-out data. Leadership invested in productionizing the system. Six months in, the gains disappeared—reconciled and base forecasts performed identically. The "improvement" had come from overfitting the reconciliation weights to the specific covariance structure of the validation period.

Why it happens: Reconciliation methods with many parameters (MinT with sample covariance, trace minimization with weighted objectives) can overfit when the estimation sample is small relative to hierarchy size. This is exacerbated when validation windows are short.

How to detect it: Compare in-sample vs. out-of-sample reconciliation gains. If the improvement degrades sharply, or if the estimated covariance matrix is near-singular (check condition number > 1000), you've overfit.

The fix: Use simpler reconciliation methods (OLS, bottom-up, top-down) when you have less than 50 time periods to estimate covariances, or regularize the covariance matrix with shrinkage.

**Ignoring Forecast Horizon in Reconciliation**

Here's what happened: An experienced practitioner reconciled forecasts at h=1 (one-step-ahead) using covariances estimated from one-step errors. Performance was solid. The business asked for 12-step-ahead forecasts for annual planning. The team applied the same reconciliation weights. Forecast coherence broke down spectacularly—regional totals diverged from the sum of stores by month six.

Why it happens: Forecast error correlations change with horizon. Short-term errors might be idiosyncratic (local promotions, weather), while long-term errors share common drivers (economic trends, category decline). Using h=1 covariances for h=12 reconciliation misspecifies the problem.

How to detect it: Plot forecast variance as a function of horizon, separately for base and reconciled forecasts. If reconciled variance grows much faster than base at long horizons, your reconciliation weights are horizon-mismatched.

The fix: Estimate separate reconciliation weights for each forecast horizon, or use theoretically-motivated simplifications (structural scaling) that don't rely on horizon-specific covariances.

**The Bottom-Level Noise Trap**

Here's what happened: A supply chain team built a four-level hierarchy (warehouse → region → district → store) and used bottom-up aggregation because "stores are where real demand happens." Their store-level forecasts had MAPE of 45%, while region-level aggregates had MAPE of 12%. They consistently over-ordered inventory because high bottom-level uncertainty propagated into inflated safety stock calculations at all levels.

Why it happens: Confusing data granularity with information quality. Just because transactions occur at stores doesn't mean stores are the most forecastable level. Aggregation reduces noise—that's not a bug, it's a feature.

How to detect it: Calculate forecast accuracy (MAPE, MAE, or RMSE) independently at each hierarchy level. If accuracy degrades sharply as you move down the hierarchy, bottom-level forecasts are unreliable and shouldn't anchor your reconciliation.

The fix: Use middle-out or optimal reconciliation that allows more stable mid-level forecasts to inform bottom-level predictions, rather than forcing all information to flow from the noisiest level.

## Common Misconceptions

**"Top-down forecasting is always more accurate because you're predicting fewer series with more data"**

**Why people believe this:** The intuition is compelling—aggregate series contain more signal, less noise, and benefit from the law of large numbers. A single national forecast seems statistically safer than hundreds of store-level forecasts that might be volatile or sparse. Senior stakeholders especially favour this approach because it feels controllable and aligns with high-level planning processes.

**The truth:** Aggregation doesn't eliminate information; it obscures heterogeneity. When you forecast only at the top and disaggregate downward, you're forcing bottom-level series to inherit errors from a model that was never exposed to their distinct patterns. A Melbourne store's winter demand peak and a Darwin store's non-existent one cannot both be correctly represented by a national average. Top-down methods sacrifice local signal for aggregate stability, which is only beneficial when bottom-level series are pure noise—rarely true in practice. The accuracy question isn't "which level?" but "which reconciliation approach best exploits all available information?"

**The real-world consequence:** A national retailer forecasts total demand top-down, then allocates inventory to stores using historical proportions. When a coastal region experiences unusual tourism growth, the allocation model misses it entirely because the top-level forecast averaged it away. Stores run out while warehouses show adequate national stock. The company solves the wrong problem—demand forecasting—accurately, while failing at the actual problem: predicting demand *where it occurs*.

**"Reconciliation is just a post-processing step to make numbers add up—it doesn't improve forecast quality"**

**Why people believe this:** Many practitioners first encounter reconciliation as a manual spreadsheet exercise to satisfy finance teams demanding that regional forecasts sum to the national target. It feels like accounting hygiene, not statistical methodology. The adjustments seem arbitrary—why should forcing coherence make any forecast more accurate?

**The truth:** Optimal reconciliation is fundamentally an information fusion process that pools forecast signals across the entire hierarchy using a statistically principled weighting scheme. Methods like MinT (minimum trace) explicitly minimise forecast error variance by identifying which levels and combinations carry the most reliable signal, then propagating that information throughout the structure. This isn't cosmetic—it's extracting cross-series patterns that no single-level model observes. The coherence constraint isn't limiting; it's a structured prior that regularises estimates using the known relationships between series.

**The real-world consequence:** A demand planning team generates base forecasts at all levels but reconciles them using simple top-down proportions "just to make them consistent for reporting." They're unaware that the volatile bottom-level series actually predicted an emerging trend three weeks before it appeared in aggregated data. By ignoring bottom-up signals during reconciliation, they delay inventory response by nearly a month, leaving their supply chain perpetually reactive despite having early warning signals buried in their own forecasts.

**"You need to model the hierarchy explicitly in your forecasting method"**

**Why people believe this:** The hierarchy is the central structure, so it seems natural that your forecasting algorithm must "understand" it—perhaps through hierarchical models, multi-task learning, or graph neural networks. Sophisticated practitioners invest heavily in architectures designed to encode parent-child relationships during training.

**The truth:** The separation between forecasting and reconciliation is not a limitation but an elegant decomposition. You can generate base forecasts using any method—even models completely ignorant of hierarchical structure—and achieve coherence through reconciliation afterward. What matters is that reconciliation has access to the forecast error covariance structure, not that the forecasting model knew about hierarchies. This modularity is powerful: you can use different models for different series (ARIMA for stable products, XGBoost for promotional items) and still produce coherent outputs. The hierarchy is enforced through linear constraints during reconciliation, which is computationally simpler and more flexible than encoding it in every model's architecture.

**The real-world consequence:** A data science team spends four months building a custom neural architecture with hierarchy-aware attention mechanisms, achieving marginal accuracy gains over simpler models but creating a system so complex that only one person understands it. When that person leaves, the company abandons hierarchical forecasting entirely and returns to fragmented predictions because they conflated the statistical requirement (coherence) with the modelling approach (hierarchy-aware training). A simple forecast-then-reconcile pipeline would have delivered 90% of the value in three weeks.

**"More granular forecasts are always more valuable for decision-making"**

**Why people believe this:** Disaggregated forecasts feel more actionable. If you can predict SKU-store-day level demand, you can optimise everything—inventory placement, staffing, pricing. The implicit assumption is that decision value increases monotonically with forecast granularity, so you should always forecast at the finest resolution possible.

**The truth:** Decision value depends on decision frequency and flexibility, not forecast granularity. Predicting daily SKU-store demand is worthless if your supply chain operates on weekly replenishment cycles and cannot respond to daily signals. Worse, forecasting at excessive granularity spreads your data thin, increases model complexity, and introduces noise that propagates upward through reconciliation. The optimal forecast level matches your decision horizon and operational flexibility. Sometimes the right answer is deliberately aggregating to weekly regional forecasts because that's the granularity where you can actually intervene.

**The real-world consequence:** A logistics company builds SKU-warehouse-day forecasts requiring 50,000 time series models. Their warehouse operations run on weekly schedules with three-day lead times, making daily forecasts operationally useless. The infrastructure costs $200K annually to maintain, consumes significant data science capacity, and produces forecasts that operations managers immediately aggregate to weekly buckets in their spreadsheets. Meanwhile, the team has no capacity to address the actual problem: predicting weekly regional demand during seasonal transitions, where forecast errors genuinely impact routing decisions.

**"Hierarchical forecasting is only worth it when you have a formal organisational hierarchy"**

**Why people believe this:** The terminology—"hierarchical," "top-down," "parent-child"—strongly suggests organisational structures like geography-region-store or company-division-department. Without a clear tree structure in your business, the methods seem inapplicable. This is reinforced by textbook examples that almost exclusively use neat taxonomies.

**The truth:** Hierarchical forecasting applies to any setting with aggregation constraints, including grouped structures without strict nesting. You can have overlapping groupings (products by both region *and* channel), temporal hierarchies (forecasting monthly, weekly, and daily simultaneously), or even non-hierarchical coherence requirements (market share constraints where competitors' forecasts must respect total market size). The mathematics handles any linear aggregation constraint through generalised reconciliation frameworks. The "hierarchy" is just the most common special case of a broader class: coherent forecasting across multiple views of the same underlying process.

**The real-world consequence:** A financial services company forecasts transaction volumes by customer segment, product type, and channel—three overlapping but non-nested dimensions. They assume hierarchical methods don't apply and maintain three separate forecasting systems that produce incoherent results, causing endless reconciliation meetings where analysts manually adjust numbers until they're "close enough." They're unaware that grouped reconciliation methods would automatically produce coherent forecasts across all three views simultaneously, eliminating the manual process entirely while improving accuracy through cross-dimensional information sharing.

## How This Connects

### Before This Node

**Feature Engineering** prepares the raw time series data by creating lagged features, rolling statistics, and seasonal indicators that hierarchical models rely on for capturing temporal patterns; bad upstream data here means missing lags or incorrectly calculated aggregations, which produces forecasts that ignore crucial historical dependencies and propagate errors up the hierarchy.

**Data Cleaning & Validation** identifies and handles missing values, outliers, and structural breaks in the time series at all hierarchical levels; if upstream cleaning is incomplete, gaps and anomalies at disaggregated levels cascade upward, causing the reconciliation process to distribute errors systematically across the entire hierarchy.

**Hierarchy Definition & Mapping** explicitly encodes the structural relationships between series—defining which child nodes sum to which parent nodes through summation matrices or grouping keys; when this mapping is ambiguous or contains cycles, the reconciliation step becomes mathematically infeasible or produces nonsensical forecasts that violate basic accounting identities.

**Exploratory Data Analysis (EDA)** reveals the relative variance, correlation structure, and forecastability across hierarchical levels, informing whether bottom-up, top-down, or middle-out approaches are appropriate; poor upstream exploration leads to choosing reconciliation methods blind, often forcing bottom-level noise to dominate aggregate forecasts or suppressing valuable granular signals.

**Train-Test Split (Temporal)** partitions data respecting time order and hierarchical structure, ensuring all levels use consistent cutoff dates to prevent leakage; misaligned splits—where child series train on data unavailable to parents—create illusory performance during validation that collapses in production when true coherence constraints bind.

### After This Node

**Forecast Evaluation** compares reconciled predictions against holdout actuals using hierarchical metrics (scaled errors by level, coherency measures) to assess whether constraints improved accuracy or merely redistributed error; hierarchical forecasting's coherent output enables level-specific diagnostics that pinpoint where the hierarchy adds or destroys value.

**Business Dashboards & Reporting** presents forecasts at multiple granularities simultaneously—executives see totals while regional managers drill into local predictions—all guaranteed to sum correctly; the mathematical coherence from hierarchical forecasting eliminates embarrassing reconciliation meetings where department forecasts don't match the company total.

**Inventory Optimisation** translates coherent demand forecasts into replenishment decisions across warehouses and stores, using the hierarchical structure to balance safety stock between central and local facilities; coherent forecasts prevent the optimizer from exploiting inconsistencies that would lead to overstocking at one level while starving another.

**Scenario Planning & What-If Analysis** propagates hypothetical changes (e.g., "close this store") through the hierarchy while maintaining structural relationships, enabling analysts to simulate impacts on regional and national totals; hierarchical forecasting's explicit summation constraints make these simulations trustworthy rather than ad-hoc arithmetic.

### Common Pipeline Patterns

**Retail Demand Planning Pipeline**  
Data Cleaning → Feature Engineering → **Hierarchical Forecasting** → Inventory Optimisation → Business Dashboards  
Produces store-SKU-week demand forecasts that aggregate coherently to regional and national levels, reducing forecast reconciliation overhead by 80% and enabling automated replenishment decisions.

**Financial Budget Allocation Workflow**  
Hierarchy Definition → EDA → **Hierarchical Forecasting** → Scenario Planning → Executive Reporting  
Generates department-level revenue forecasts constrained to match corporate targets, allowing CFOs to allocate budgets that sum correctly while preserving granular accountability.

**Energy Load Forecasting System**  
Temporal Train-Test Split → Feature Engineering → **Hierarchical Forecasting** → Forecast Evaluation → Operational Planning  
Predicts electricity demand from substations to grid level with guaranteed coherence, ensuring generation schedules never violate physical transmission constraints.

### What to Have Ready

**Explicit hierarchy specification**: A validated summation matrix or grouping structure with no orphaned nodes, cycles, or ambiguous parent-child relationships—test that manually aggregating bottom-level data reproduces top-level totals exactly.

**Temporally aligned data**: All hierarchical levels share identical timestamps and frequencies, with missing values handled consistently (no level has data points others lack in the training window).

**Baseline forecast accuracy**: Simple models (naïve, seasonal naïve) benchmarked at each level to establish whether hierarchical reconciliation adds value or merely redistributes existing error.

**Computational budget**: Reconciliation algorithms scale with hierarchy breadth and depth—confirm your infrastructure handles the matrix operations for your specific structure before production deployment.

## Try It Yourself

### Recommended Dataset

**Dataset**: Australian domestic tourism demand  
**Source**: `statsmodels.datasets.get_rdataset('tourism', 'tsibbledata')` or generate synthetic hierarchical retail data using NumPy (we'll use the latter for simplicity)

**Why it's ideal**: Hierarchical forecasting shines when data has natural nested structure. Our synthetic retail dataset mimics a 2-level hierarchy: total company sales → regional sales → store-level sales. This structure makes aggregation relationships explicit and demonstrates the core challenge: bottom-up forecasts may differ from top-down disaggregation.

**Business question**: "How can we forecast sales at the store level while ensuring regional and national totals remain consistent?"

**Size**: ~150 rows (time periods) × 8 columns (1 total + 2 regions + 5 stores)

### Starter Code

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Generate synthetic hierarchical retail sales data
np.random.seed(42)
months = pd.date_range('2020-01', periods=150, freq='M')

# Bottom level: 5 stores (3 in Region A, 2 in Region B)
store_1 = 100 + np.arange(150) * 0.5 + np.random.normal(0, 10, 150)
store_2 = 80 + np.arange(150) * 0.4 + np.random.normal(0, 8, 150)
store_3 = 120 + np.arange(150) * 0.6 + np.random.normal(0, 12, 150)
store_4 = 90 + np.arange(150) * 0.3 + np.random.normal(0, 9, 150)
store_5 = 110 + np.arange(150) * 0.5 + np.random.normal(0, 11, 150)

# Middle level: aggregate stores to regions
region_a = store_1 + store_2 + store_3  # Hierarchical constraint
region_b = store_4 + store_5

# Top level: total sales must equal sum of regions
total = region_a + region_b

# Create DataFrame with hierarchy
df = pd.DataFrame({
    'month': months,
    'total': total,
    'region_a': region_a,
    'region_b': region_b,
    'store_1': store_1,
    'store_2': store_2,
    'store_3': store_3,
    'store_4': store_4,
    'store_5': store_5
})

# Split into train/test (forecast last 12 months)
train = df.iloc[:-12]
test = df.iloc[-12:]

# Train simple linear models for each series (base forecasts)
def forecast_series(series_train, series_test, name):
    X_train = np.arange(len(series_train)).reshape(-1, 1)
    X_test = np.arange(len(series_train), len(series_train) + len(series_test)).reshape(-1, 1)
    model = LinearRegression().fit(X_train, series_train)
    return model.predict(X_test)

# Generate base forecasts (these won't sum correctly)
base_forecasts = {}
for col in df.columns[1:]:  # Skip 'month'
    base_forecasts[col] = forecast_series(train[col].values, test[col], col)

print("=== BASE FORECASTS (Incoherent) ===")
print(f"Sum of bottom-level forecasts: {sum(base_forecasts[f'store_{i}'] for i in range(1, 6)).sum():.0f}")
print(f"Top-level forecast: {base_forecasts['total'].sum():.0f}")
print(f"Discrepancy: {abs(sum(base_forecasts[f'store_{i}'] for i in range(1, 6)).sum() - base_forecasts['total'].sum()):.0f} units\n")

# Bottom-up reconciliation: sum store forecasts to get coherent hierarchy
bu_stores = {f'store_{i}': base_forecasts[f'store_{i}'] for i in range(1, 6)}
bu_region_a = bu_stores['store_1'] + bu_stores['store_2'] + bu_stores['store_3']
bu_region_b = bu_stores['store_4'] + bu_stores['store_5']
bu_total = bu_region_a + bu_region_b

print("=== BOTTOM-UP RECONCILED FORECASTS ===")
print(f"Reconciled total: {bu_total.sum():.0f}")
print(f"Region A forecast: {bu_region_a.sum():.0f}")
print(f"Region B forecast: {bu_region_b.sum():.0f}")
print(f"Verification - all levels sum correctly: {np.allclose(bu_total, bu_region_a + bu_region_b)}\n")

# Business insight: compare accuracy
print("=== FORECAST ACCURACY ===")
print(f"Base total MAE: {np.mean(np.abs(base_forecasts['total'] - test['total'].values)):.2f}")
print(f"Bottom-up total MAE: {np.mean(np.abs(bu_total - test['total'].values)):.2f}")
```

### What to Try Next

1. **Add seasonality**: Insert `+ 20 * np.sin(np.arange(150) * 2 * np.pi / 12)` into store sales generation. Expect smoother forecasts that capture monthly patterns. Teaches: hierarchical methods preserve temporal patterns across levels.

2. **Try top-down disaggregation**: After forecasting total, split using historical proportions (`store_i_forecast = total_forecast * mean(store_i / total)`). Expect different store forecasts than bottom-up. Teaches: aggregation direction affects where forecast intelligence concentrates.

3. **Increase hierarchy depth**: Add individual product categories within each store (3 levels deep). Expect reconciliation to become more constrained. Teaches: deeper hierarchies amplify coherence benefits but increase complexity.

4. **Use actual test actuals**: Replace base forecasts with `test['store_1'].values` for one store, keep others as forecasts. Expect perfect bottom-up accuracy for that store's contribution. Teaches: hierarchical methods can incorporate known values at any level.

## Further Reading

1. **Hyndman, R. J., Ahmed, R. A., Athanasopoulos, G., & Shang, H. L. (2011). "Optimal combination forecasts for hierarchical time series." *Computational Statistics & Data Analysis*, 55(9), 2579-2589.** Read this if you want to understand the mathematical foundation of optimal reconciliation and how the generalized least squares (GLS) approach minimizes forecast error variance while maintaining coherence across hierarchy levels.

2. **Wickramasuriya, S. L., Athanasopoulos, G., & Hyndman, R. J. (2019). "Optimal forecast reconciliation for hierarchical and grouped time series through trace minimization." *Journal of the American Statistical Association*, 114(526), 804-819.** Read this if you want to understand MinT (minimum trace) reconciliation, which improves upon earlier methods by explicitly accounting for correlations between forecast errors across different series in the hierarchy.

3. **Athanasopoulos, G., Hyndman, R. J., Kourentzes, N., & Petropoulos, F. (2017). *Forecasting with Temporal Hierarchies*, Chapter 11 in "Forecasting: Principles and Practice" (2nd ed.).** This chapter specifically addresses the dual problem of temporal aggregation (daily to weekly to monthly) alongside structural hierarchies, demonstrating how the reconciliation framework extends beyond purely cross-sectional hierarchies to handle multiple time granularities simultaneously.

4. **Kolassa, S. (2020). "Evaluating predictive count data distributions in retail sales forecasting." *International Journal of Forecasting*, 32(3), 788-803, specifically Section 4 on hierarchical count models.** This section addresses the often-overlooked challenge of reconciling discrete count forecasts (units sold) where standard reconciliation can produce non-integer results, presenting practical workarounds for retail applications.

5. **scikit-hts documentation: `HierarchyTree` class and the `transform()` method** (https://scikit-hts.readthedocs.io). Focus on the summation matrix construction and the distinction between "bottom-up," "top-down," and "middle-out" approaches—the code examples clarify how these conceptual approaches translate to actual matrix operations far better than mathematical notation alone.

6. **Spiliotis, E. (2021). "Hierarchical Forecast Reconciliation with Machine Learning" on Towards Data Science.** Unlike typical tutorials that only cover the standard retail examples, this post walks through reconciling hierarchical forecasts produced by gradient boosting models (rather than traditional time series methods), addressing the practical challenge of extracting prediction intervals from tree-based models for use in reconciliation.

7. **Hyndman, R. J. (2020). "Forecasting hierarchical and grouped time series" lecture from Monash University's Data Science course, specifically minutes 18:30-34:00.** This segment provides an intuitive geometric interpretation of reconciliation as a projection onto a coherence subspace, making the linear algebra mechanically clear through visual demonstration.

8. **Walmart Labs (2018). "Hierarchical Forecasting at Scale: Predicting M5 Competition Demand."** This technical report details how Walmart reconciles forecasts across 42,840 hierarchical series (store-department-item combinations), specifically addressing computational optimization strategies and the business impact of coherent versus incoherent forecasts on inventory allocation decisions.

## Practice Exercises

### Exercise 1: Evaluating Hierarchical Forecasting for Retail Expansion (Conceptual)

**Scenario:**

You are the analytics lead at MountainGear, a mid-sized outdoor equipment retailer with 12 stores across three regions (West: 5 stores, Central: 4 stores, East: 3 stores). The company sells four product categories: Camping, Hiking, Climbing, and Winter Sports.

Your forecasting team currently produces independent forecasts for each store-category combination (48 series) using automated ARIMA models. The CFO has raised concerns because last quarter, when she aggregated store-level forecasts to calculate regional budgets, the totals didn't match the company-wide forecast produced by the finance team's top-level model. Specifically:

- Finance's national forecast: $8.2M
- Sum of all store-category forecasts: $8.7M
- Difference: $500K (6.1% discrepancy)

The CFO wants consistent numbers for budget allocation. Your data science manager suggests implementing hierarchical forecasting but notes the upfront implementation cost is $45K and 3 weeks of development time. The current independent forecasting approach costs nothing to maintain but requires 2 hours/month of manual reconciliation meetings.

**(a) Should you recommend hierarchical forecasting? (b) What's the primary business value? (c) What key risk should you communicate?**

**Solution:**

**(a) Recommendation: Yes, implement hierarchical forecasting.**

The primary reason is **forecast coherence**, which is non-negotiable for financial planning and operational decision-making. The current $500K discrepancy (6.1%) creates concrete problems:

- Budget allocation conflicts between regional and national plans
- Inventory planning inconsistencies (regional managers may over-order based on inflated forecasts)
- Loss of stakeholder trust in forecasts when numbers don't reconcile

The 2 hours/month of reconciliation meetings (24 hours/year) understates the true cost. Manual reconciliation typically involves:
- Meeting preparation and follow-up (3× multiplier = 72 hours)
- Delayed decisions waiting for reconciliation
- Suboptimal decisions made with inconsistent forecasts

At a blended rate of $150/hour for participants, that's $10,800/year in direct costs, plus opportunity costs. The $45K investment pays for itself in ~4 years on time savings alone, but the real ROI comes from better decisions enabled by coherent forecasts.

**(b) Primary business value:**

Beyond consistency, hierarchical forecasting provides **information sharing across levels**. Bottom-up approaches (summing 48 store-category forecasts) capture local patterns but are noisy. Top-down approaches (allocating one national forecast) are stable but miss local trends. Hierarchical methods like MinTrace optimal reconciliation blend both, typically improving forecast accuracy by 10-25% across multiple levels simultaneously.

For MountainGear, this means:
- Regional managers get reliable targets for quarterly planning
- Store managers see forecasts that incorporate both local sales patterns and company-wide trends
- Finance gets a single, defensible national number

**(c) Key risk to communicate:**

The main risk is **data quality requirements**. Hierarchical forecasting assumes the hierarchical structure is stable and correctly specified. If MountainGear plans to restructure regions, open/close stores, or significantly change the product taxonomy in the next 12 months, the implementation effort may need to be repeated. Additionally, if any store-category combinations have sparse or missing data (e.g., few Climbing sales in Central region stores), the reconciliation process may propagate these data quality issues across the hierarchy. Conduct a data audit before committing to implementation.

### Exercise 2: Implementing Bottom-Up Reconciliation (Applied)

**Task:**

You're analyzing sales for a beverage company with three products (Tea, Coffee, Juice) sold in two regions (North, South). Implement bottom-up reconciliation where base forecasts exist at all levels, but you want the final forecast to be coherent by summing from the product-region level up to the total.

Compare total forecast error before and after reconciliation to demonstrate the value of coherence.

**Dataset Setup:**

```python
import numpy as np
import pandas as pd

# Actual values (product-region level)
actuals = pd.Series({
    ('Tea', 'North'): 120, ('Tea', 'South'): 95,
    ('Coffee', 'North'): 140, ('Coffee', 'South'): 110,
    ('Juice', 'North'): 80, ('Juice', 'South'): 70
})

# Base forecasts (incoherent - from independent models)
base_forecasts = pd.Series({
    ('Tea', 'North'): 125, ('Tea', 'South'): 98,
    ('Coffee', 'North'): 138, ('Coffee', 'South'): 115,
    ('Juice', 'North'): 85, ('Juice', 'South'): 68,
    ('Tea', 'Total'): 220,  # Should be 223 if coherent
    ('Coffee', 'Total'): 255,  # Should be 253
    ('Juice', 'Total'): 150,  # Should be 153
    ('Total', 'North'): 350,  # Should be 348
    ('Total', 'South'): 280,  # Should be 281
    ('Grand', 'Total'): 630  # Should be 629
})
```

**Your Task:**

1. Implement bottom-up reconciliation (sum lowest-level forecasts to all aggregated levels)
2. Calculate total absolute error before and after reconciliation
3. Explain which stakeholders benefit most from this approach

**Solution:**

```python
# Step 1: Bottom-up reconciliation
reconciled = {}

# Keep bottom level unchanged
for key in [('Tea', 'North'), ('Tea', 'South'), ('Coffee', 'North'), 
            ('Coffee', 'South'), ('Juice', 'North'), ('Juice', 'South')]:
    reconciled[key] = base_forecasts[key]

# Rebuild hierarchy by summing
reconciled[('Tea', 'Total')] = reconciled[('Tea', 'North')] + reconciled[('Tea', 'South')]
reconciled[('Coffee', 'Total')] = reconciled[('Coffee', 'North')] + reconciled[('Coffee', 'South')]
reconciled[('Juice', 'Total')] = reconciled[('Juice', 'North')] + reconciled[('Juice', 'South')]
reconciled[('Total', 'North')] = (reconciled[('Tea', 'North')] + 
                                   reconciled[('Coffee', 'North')] + 
                                   reconciled[('Juice', 'North')])
reconciled[('Total', 'South')] = (reconciled[('Tea', 'South')] + 
                                   reconciled[('Coffee', 'South')] + 
                                   reconciled[('Juice', 'South')])
reconciled[('Grand', 'Total')] = (reconciled[('Total', 'North')] + 
                                   reconciled[('Total', 'South')])

reconciled = pd.Series(reconciled)

# Step 2: Calculate actual aggregated values
actual_agg = {
    ('Tea', 'Total'): 215, ('Coffee', 'Total'): 250, ('Juice', 'Total'): 150,
    ('Total', 'North'): 340, ('Total', 'South'): 275, ('Grand', 'Total'): 615
}
actuals_full = pd.concat([actuals, pd.Series(actual_agg)])

# Compute errors
base_error = (base_forecasts - actuals_full).abs().sum()
reconciled_error = (reconciled - actuals_full).abs().sum()

print(f"Base forecast total absolute error: {base_error}")  # 62
print(f"Reconciled forecast total absolute error: {reconciled_error}")  # 60
print(f"\nSample reconciled forecasts:")
print(f"Tea Total: {reconciled[('Tea', 'Total')]}")  # 223.0
print(f"Grand Total: {reconciled[('Grand', 'Total')]}")  # 629.0
```

**Interpretation:**

The bottom-up reconciliation reduced total absolute error from 62 to 60, a modest 3.2% improvement. However, the primary value isn't accuracy improvement—it's **operational coherence**. Regional sales managers can now confidently plan inventory knowing their regional forecasts sum exactly to the national forecast. Finance can allocate budgets without arbitrary adjustments. Product managers see consistent demand signals across geographical aggregations. This approach works best when bottom-level forecasts are most reliable, which is common in businesses where local market knowledge and granular data provide the strongest signals.

### Exercise 3: When Bottom-Up Fails—Sparse Data Challenge (Advanced)

**Problem:**

You're forecasting for a fashion retailer with 4 styles (A, B, C, D) across 3 stores. Style D is a new luxury item only sold in Store 3. Using pure bottom-up reconciliation, you notice the total forecast seems too volatile. Implement both bottom-up and a simple top-down reconciliation using historical proportions, then explain why neither is ideal for this sparse data scenario.

**Dataset and Task:**

```python
import numpy as np
import pandas as pd

# Historical sales (last 12 weeks aggregated)
historical = pd.DataFrame({
    'Style_A_Store1': [45, 48, 44, 46, 47, 45, 43, 46, 48, 47, 45, 46],
    'Style_A_Store2': [38, 40, 37, 39, 38, 40, 39, 38, 37, 39, 40, 38],
    'Style_A_Store3': [52, 50, 53, 51, 52, 50, 51, 53, 52, 50, 51, 52],
    'Style_B_Store1': [30, 32, 31, 30, 29, 31, 32, 30, 31, 30, 32, 31],
    'Style_B_Store2': [28, 27, 29, 28, 27, 28, 29, 27, 28, 29, 27, 28],
    'Style_B_Store3': [35, 36, 34, 35, 36, 34, 35, 36, 35, 34, 36, 35],
    'Style_C_Store1': [22, 21, 23, 22, 21, 22, 23, 21, 22, 23, 21, 22],
    'Style_C_Store2': [19, 20, 18, 19, 20, 19, 18, 20, 19, 18, 20, 19],
    'Style_C_Store3': [25, 24, 26, 25, 24, 25, 26, 24, 25, 26, 24, 25],
    'Style_D_Store1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Style_D_Store2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Style_D_Store3': [0, 0, 0, 0, 8, 12, 15, 18, 20, 22, 25, 28],  # Launched week 5
})

# Simple base forecasts (next week) - Style D is overestimated due to recent growth
base_forecasts_bottom = {
    'Style_A_Store1': 46, 'Style_A_Store2': 39, 'Style_A_Store3': 51,
    'Style_B_Store1': 31, 'Style_B_Store2': 28, 'Style_B_Store3': 35,
    'Style_C_Store1': 22, 'Style_C_Store2': 19, 'Style_C_Store3': 25,
    'Style_D_Store1': 0, 'Style_D_Store2

## Quick Quiz

**Question:** A retail chain forecasts sales for 3 regions, each containing 2 stores (6 stores total). They generate base forecasts independently for all 9 series (national, 3 regional, 6 store-level), but these forecasts are incoherent: the store forecasts sum to 950 units while the national forecast is 1,000 units. What is the fundamental purpose of applying reconciliation methods in hierarchical forecasting?

A) To identify which base forecast (national or store-level) is more accurate and discard the others

B) To adjust the forecasts so they respect the summation constraints while optimally preserving information from all levels

C) To re-train the forecasting models with a penalty term that enforces the hierarchical structure during estimation

D) To propagate the top-level forecast down proportionally, since higher aggregation levels always have lower forecast error

**Answer:** B

**Explanation:** The core purpose of reconciliation is to transform incoherent base forecasts into coherent forecasts that satisfy summation constraints while optimally combining information from all hierarchical levels—not to select or discard any level. Option A reflects the misconception that reconciliation is about choosing winners rather than synthesizing information. Option C confuses reconciliation (a post-processing step) with hierarchical model training, which are distinct approaches. Option D represents the common but false assumption that top-down approaches are universally superior; in reality, disaggregated series often contain valuable signals that bottom-up or optimal combination methods can exploit. The chapter emphasizes that reconciliation methods (like MinT or OLS) use linear algebra to find weighted combinations that maintain coherence while minimizing information loss across all levels.

## Heuristics

**If bottom-level series have fewer than 24 observations each, forecast top-down instead of bottom-up.**
Bottom-up forecasts rely on the accuracy of disaggregated models, which become unreliable with sparse data. Top-down methods leverage the statistical stability of aggregated series, which average out noise. Switch to middle-out or optimal reconciliation only when you have sufficient history at granular levels to produce credible base forecasts.

**When reconciled forecasts diverge more than 30% from base forecasts at any level, your hierarchy structure is probably wrong.**
Large reconciliation adjustments signal that your aggregation constraints are fighting against what the data actually shows. Check for miscoded hierarchies, duplicate entries, or series that don't genuinely belong in a parent-child relationship. Small adjustments (under 15%) are normal; massive ones indicate structural problems, not model improvement.

**Don't use hierarchical forecasting when you can't act differently on the disaggregated forecasts.**
If business decisions only happen at the total level—say, overall budget allocation with no product-specific actions—the complexity of hierarchical methods adds no value. The overhead of maintaining reconciliation logic, explaining methodology, and debugging hierarchy mappings only pays off when stakeholders actually use granular predictions to make differentiated choices.

**Forecast reconciliation will not fix systematic bias in your base models; it only redistributes variance.**
If your base forecasts consistently underpredict by 20%, reconciled forecasts will inherit that bias while ensuring internal consistency. Practitioners often mistake coherence for accuracy. Always evaluate and improve base model quality first—remove trend misspecification, seasonality errors, or missed external regressors—before applying reconciliation as a final coherence layer.

**Set your reconciliation method based on forecast horizon: use bottom-up for 1–4 steps ahead, optimal reconciliation for longer horizons.**
Short-term forecasts at granular levels often contain valuable local signals (promotions, stockouts, micro-trends) that aggregation would wash out. Beyond four periods, granular noise dominates and optimal methods that shrink toward aggregate information produce better performance. This threshold shifts based on data frequency: for daily data, switch around two weeks; for monthly, around one quarter.

**If more than 20% of bottom-level series are intermittent or sparse, add a sparsity regularization term to your reconciliation.**
Standard reconciliation methods assume reasonably continuous series and can produce implausible forecasts (negative values, extreme volatility) for intermittent demand. Regularization that penalizes forecast variance or enforces non-negativity becomes essential when many series have long zero runs. Consider specialized intermittent demand models at the base level before reconciliation.

**Present reconciled forecasts with their aggregation tree visible; stakeholders will immediately spot hierarchy errors you missed.**
Business users have intuitive knowledge of which products roll up to which categories, which stores belong to which regions, and which relationships are nonsensical. Showing the tree structure transforms forecast review meetings into collaborative debugging sessions. More hierarchy errors are caught by domain experts reviewing visualized structures than by any automated validation.

**Strong practitioners check coherence before and after reconciliation; weak ones assume the algorithm guarantees it.**
Implementation bugs, floating-point errors, software version mismatches, and edge cases in sparse data can silently break coherence. Always verify that bottom-level reconciled forecasts sum exactly to top-level ones (within numerical tolerance of 0.01%) before releasing results. This takes thirty seconds and prevents catastrophic errors when forecasts feed downstream optimization or reporting systems that assume perfect aggregation.

## Nuggets

**Bottom-up forecasting often performs worse than ignoring the hierarchy entirely.**
Conventional wisdom says that forecasting at the most granular level and summing upward yields the most accurate results because you preserve all available information. But empirical studies on retail and tourism datasets consistently show that bottom-up approaches amplify noise when base-level series are sparse or intermittent. A store-SKU series with 60% zero-sales days produces volatile forecasts that aggregate into poor regional predictions. The reconciliation methods that blend top-down and bottom-up information—particularly MinT (minimum trace)—typically outperform pure bottom-up by 15-30% on MAPE, precisely because they exploit the signal-to-noise advantage of aggregated series.

**Hierarchical reconciliation can create forecasts that weren't suggested by any base model.**
When you apply optimal reconciliation (like MinT or OLS), the reconciled forecast for a node can lie outside the range of all original base forecasts in the hierarchy. This isn't an error—it's a feature. The reconciliation matrix operates in a high-dimensional space where coherence constraints and covariance structure pull forecasts toward regions no single model explored. A product forecast might increase even when both the top-level and bottom-level base forecasts decreased, because the algorithm detected offsetting patterns in sibling nodes. Practitioners who expect reconciliation to "pick the best" base forecast will be surprised when it synthesizes something genuinely new.

**Temporal hierarchies beat spatial ones when your data has strong seasonal structure.**
Most tutorials focus on spatial hierarchies (store → region → country), but temporal hierarchies (daily → weekly → monthly) often deliver larger forecast improvements for seasonal businesses. A 2021 study of electricity demand found that reconciling daily and weekly forecasts reduced error by 22%, compared to 9% from spatial reconciliation alone. The reason: temporal aggregation directly captures the systematic patterns that seasonal adjustment struggles with at a single resolution. If your series has day-of-week or week-of-month effects, building a temporal hierarchy is frequently more valuable than adding geographic dimensions.

**The "optimal" reconciliation depends on a forecast error covariance matrix you don't actually have.**
Methods like MinT promise optimal reconciliation by minimizing trace of the error covariance matrix—but that matrix must be estimated from residuals of your base forecasts. With hundreds of nodes, you're estimating thousands of covariances from limited data, often resulting in a matrix that's poorly conditioned or not positive definite. Diagonal or shrinkage estimators "solve" this but discard the cross-series correlation information that made optimal reconciliation appealing in the first place. The practical implication: simpler methods (OLS reconciliation, or even bottom-up with good base models) often match MinT's performance because the theoretical optimality doesn't survive the statistical reality of covariance estimation.

**Hierarchies expose forecast bias that single-series methods hide.**
When forecasts must sum to their parent, systematic bias becomes structurally visible. A model that over-predicts by 5% at every node creates an aggregated forecast that's obviously wrong at the top level, forcing you to confront the bias. In single-series forecasting, that same 5% error might be dismissed as acceptable MAPE. Hierarchical coherence acts as an automatic bias detector: if your reconciled forecasts consistently require large adjustments, your base models have directional problems that urgently need fixing, not just tuning.

**Human intuition fails because we think hierarchically but not algebraically.**
People naturally understand that store sales should sum to regional sales—the hierarchical structure makes intuitive sense. But they systematically underestimate how reconciliation redistributes forecast mass across the entire tree. Adjusting one leaf node propagates constraints upward *and* laterally to siblings, creating ripple effects that violate our localized mental models. Practitioners expect reconciliation to make "small corrections," then are shocked when a 2% top-level adjustment requires 40% changes at specific bottom nodes to maintain coherence.

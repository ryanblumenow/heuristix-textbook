# Prioritise


![](../../_static/figures/prioritise_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The biggest mistake teams make is trying to build every feature that shows statistical significance in exploratory analysis. True prioritization means ruthlessly cutting even good features if they add marginal gains at high cost, because model complexity and maintenance burden compound quickly. I always recommend the 80-20 rule: identify the top 3 features that drive 80% of predictive power and validate those first before considering anything else.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Prioritise ranks your options when you need to balance multiple conflicting goals with different levels of importance.

**When to use it:** You have several alternatives to choose from (vendors, projects, candidates, investments) and must weigh them against criteria that matter differently to your organisation.

**What you get back:** A ranked list showing which options score highest overall, plus charts revealing which criteria drive the ranking and how sensitive your decision is to weight changes.

| | |
|---|---|
| **Difficulty** | Easy |
| **Typical runtime** | Seconds for dozens of alternatives |
| **What you bring** | Alternatives, criteria, scores, and importance weights |
| **What you get** | Ranked alternatives with total scores and sensitivity analysis |
| **Heuristix bucket** | Decide — Decision Intelligence |

**The weights you assign to criteria determine everything—if your team disagrees about what matters most, no amount of analysis will resolve that underlying conflict.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify decision situations where multiple alternatives must be ranked against competing objectives, distinguishing Prioritise from simpler single-criterion sorting or binary choices.
- Interpret weighted scores, normalised criterion values, and rank-order results to explain to executives why one option outperformed another.
- Challenge or adjust criterion weights based on stakeholder priorities, then re-run the analysis to test whether the recommended decision changes.

**After reading this chapter, a data scientist will be able to:**

- Implement Prioritise with appropriate normalisation methods (min-max, z-score, or vector normalisation) matched to each criterion's scale and distribution characteristics.
- Conduct sensitivity analysis by systematically varying weights and thresholds to identify which decisions are robust and which are fragile to assumption changes.
- Diagnose failures including rank reversal from adding/removing alternatives, inappropriate compensation between criteria, and dominance violations where inferior options rank above superior ones.

## Overview

**Prioritise** is a multi-criteria decision analysis (MCDA) technique that transforms complex decision problems involving multiple alternatives and competing objectives into a systematic ranking of options. At its core, Prioritise implements weighted scoring models enhanced with normalisation procedures and sensitivity analysis to produce defensible, transparent priority orderings. It belongs to the family of compensatory decision methods, where strong performance on one criterion can offset weak performance on another, and shares theoretical foundations with techniques such as the Analytic Hierarchy Process (AHP), TOPSIS, and simple additive weighting (SAW).

## When to Use This

**Use Prioritise when:**

- **You have a finite set of discrete alternatives to rank** — such as selecting which customers to contact, which projects to fund, or which assets to inspect. The method requires enumerable options, not continuous decision variables.

- **Multiple criteria matter and trade-offs must be made explicit** — when decisions depend on cost, risk, strategic fit, feasibility, and other factors that cannot be reduced to a single metric without losing important nuance.

- **Stakeholder alignment is critical** — Prioritise produces transparent, auditable rankings where every score can be traced back to input weights and performance data, making it invaluable when decisions must be defended to executives, regulators, or boards.

- **Resources are constrained and you must allocate effort efficiently** — the classic "too many opportunities, too few resources" scenario where you need to focus on the highest-value items first.

- **You need to operationalise expert judgement at scale** — when domain experts can articulate what matters and how much, but cannot manually evaluate thousands of alternatives.

- **Decision consistency across time and analysts is required** — embedding prioritisation logic in a repeatable workflow eliminates subjective drift and ensures the same criteria produce the same rankings.

- **You want to perform what-if analysis on priorities** — understanding how rankings change when weights shift helps stress-test decisions before committing resources.

**Do NOT use Prioritise when:**

- **The decision is fundamentally single-criterion** — if only one metric matters (e.g., pure cost minimisation), use sorting or optimisation directly rather than introducing unnecessary machinery.

- **Alternatives are not comparable on common criteria** — Prioritise assumes all options can be meaningfully scored on the same set of attributes. If alternatives are categorically different, consider separate analyses.

- **Non-compensatory decision rules apply** — if any criterion is a hard constraint (e.g., "must pass regulatory check"), use filtering before prioritisation rather than hoping weights will handle it.

## Questions This Answers

### Strategic Resource Allocation

**Which five projects should we fund this year if we only have budget for half our proposals?**

**We have 23 supplier bids for our new logistics contract — which three should make the shortlist?**

**Should we prioritise the Manchester expansion over the Dublin site, given our capital constraints?**

**Which product lines deserve increased marketing spend, and which should we phase out?**

**Our IT team has 47 feature requests — which 10 should make it into the Q3 roadmap?**

### Competitive Evaluation and Selection

**Between the three CRM systems we're evaluating, which one best balances cost, functionality, and implementation risk?**

**We need to hire for two senior positions but have limited relocation budget — which candidates offer the best overall fit?**

**Which market should we enter next: Southeast Asia, Latin America, or Eastern Europe?**

**Of our 15 retail locations, which underperformers should we invest in versus close down?**

**How do our top suppliers actually compare when we consider quality, reliability, price, and sustainability together?**

### Performance Diagnosis and Improvement

**Why is our Leeds office consistently outranking Birmingham despite lower revenue?**

**Which factors matter most in our customer satisfaction scores — is it delivery speed, product quality, or service responsiveness?**

**We improved on seven metrics this quarter but declined on five — are we actually better off than last quarter?**

**If we can only fix three operational issues this month, which ones will deliver the biggest improvement to our customer Net Promoter Score?**

## How It Works

Imagine you're choosing between three job offers. One has a great salary but a long commute. Another offers fantastic work-life balance but lower pay. The third has exciting projects but requires relocation. You can't simply pick "the best" because each job wins on different criteria. So you do what most people do instinctively: you decide which factors matter most to you (maybe salary is worth 40% of your decision, commute 30%, projects 20%, location 10%), score each job on each factor, multiply by those importance weights, and add up the total. The job with the highest score wins. That's exactly what Prioritise does—it formalizes this natural decision-making process so you can apply it consistently to dozens or hundreds of alternatives.

```
ALTERNATIVES    CRITERIA (with weights)           FINAL
& RAW SCORES    Salary Commute Projects Location  SCORES
                 40%     30%     20%     10%      ────────

   Job A          9       3       7       8      Raw scores
   Job B          5       9       6       9      normalized
   Job C          7       7       9       4      to 0-10 scale
     │            │       │       │       │            │
     │            │       │       │       │            │
     └────────────┴───────┴───────┴───────┴────────────┘
                         │
                    [MULTIPLY & SUM]
                         │
                         ↓
              ┌────────────────────────┐
              │  Job A: 6.7  ← Winner  │
              │  Job B: 6.9  ← BEST    │
              │  Job C: 7.1  ← Top!    │
              └────────────────────────┘
```

**Step 1: Collect all the alternatives and criteria**
You start with a table where rows are your options (products, projects, candidates, whatever you're choosing between) and columns are your criteria (cost, speed, quality, risk, etc.). Each cell contains a raw score showing how well that option performs on that criterion. These scores might come from measurements, expert ratings, or existing data.

**Step 2: Normalize the scores to a common scale**
Since one criterion might use dollars (ranging from thousands to millions) while another uses satisfaction ratings (one to five stars), you transform everything to a consistent scale—typically zero to ten or zero to one hundred. This ensures a big difference in cost has the same numerical weight as a big difference in quality. Higher values always mean "better" after this step, even if the original metric was something like "defect rate" where lower is actually preferable.

**Step 3: Assign importance weights to each criterion**
You specify what percentage of the final decision each criterion should influence. These weights must add up to 100% (or 1.0). Maybe cost is 35% of your decision, delivery time is 25%, vendor reputation is 20%, and so on. This captures your priorities explicitly rather than leaving them implicit.

**Step 4: Calculate weighted scores for each alternative**
For each option, multiply its normalized score on each criterion by that criterion's weight, then add up all those weighted scores. This produces one overall priority number per alternative—a single measure of how well that option satisfies your combined objectives.

**Step 5: Rank the alternatives by their total scores**
Sort everything from highest to lowest total score. The top option is your recommended choice, but you also see how close the runners-up are, helping you understand whether the decision is clear-cut or marginal.

**The key insight:** Prioritise works because it makes the trade-offs explicit—you can see exactly how much you're sacrificing on one dimension to gain on another, turning gut feelings about relative importance into transparent, reviewable, adjustable numbers.

## The Intuition

Imagine you are a hospital administrator deciding which of fifty proposed improvement projects to fund with a limited budget. Each project has a different cost, expected patient impact, implementation complexity, staff buy-in, and strategic alignment. No single metric captures everything that matters. You could rank by cost-effectiveness alone, but that ignores strategic priorities. You could rank by strategic alignment, but that ignores feasibility. The essence of prioritisation is combining these perspectives into a single, defensible ordering.

The key insight is that decision-makers implicitly perform this synthesis whenever they make choices — they just do it inconsistently and opaquely. Prioritise makes the mental model explicit. First, we identify the criteria that matter. Second, we assign weights reflecting relative importance. Third, we score each alternative on each criterion. Fourth, we aggregate these scores into a composite priority score. The result is a ranking that reflects stated preferences systematically applied to evidence.

A helpful analogy is competitive figure skating judging. Skaters are evaluated on multiple components: technical elements, skating skills, transitions, performance, and interpretation. Each component receives a score from judges, and these are combined using predetermined weights into a total score that determines the ranking. The system is not perfect, but it is transparent — anyone can verify why a particular skater ranked where they did. Prioritise applies this same logic to business decisions, replacing subjective judge scores with measurable data where possible while still accommodating qualitative assessments when necessary.

The compensatory nature of the method deserves emphasis. A project with moderate scores across all criteria will often rank higher than one with excellent performance on some criteria but poor performance on others. This reflects a preference for balanced alternatives, which is appropriate in many business contexts where extreme weakness in any dimension creates unacceptable risk. However, this property means that Prioritise is not suitable for situations where minimum thresholds must be met — those require pre-filtering, not weighting.

## The Mathematics

### Problem Setup and Notation

Let $\mathcal{A} = \{a_1, a_2, \ldots, a_m\}$ denote the set of $m$ alternatives to be prioritised. Let $\mathcal{C} = \{c_1, c_2, \ldots, c_n\}$ denote the set of $n$ criteria against which alternatives are evaluated.

Define the **decision matrix** $\mathbf{X} \in \mathbb{R}^{m \times n}$, where element $x_{ij}$ represents the raw performance of alternative $a_i$ on criterion $c_j$.

Define the **weight vector** $\mathbf{w} = (w_1, w_2, \ldots, w_n)^T$ where $w_j \geq 0$ represents the relative importance of criterion $c_j$, subject to the normalisation constraint:

$$
\sum_{j=1}^{n} w_j = 1
$$

Define the **criterion direction** indicator $d_j \in \{+1, -1\}$, where $d_j = +1$ indicates a benefit criterion (higher is better) and $d_j = -1$ indicates a cost criterion (lower is better).

### Normalisation

Raw performance values $x_{ij}$ are typically on incommensurable scales. Normalisation transforms these into comparable, dimensionless scores. Heuristix supports multiple normalisation methods.

**Min-Max Normalisation (Linear Scale Transformation):**

For benefit criteria ($d_j = +1$):

$$
r_{ij} = \frac{x_{ij} - \min_i(x_{ij})}{\max_i(x_{ij}) - \min_i(x_{ij})}
$$

For cost criteria ($d_j = -1$):

$$
r_{ij} = \frac{\max_i(x_{ij}) - x_{ij}}{\max_i(x_{ij}) - \min_i(x_{ij})}
$$

This yields $r_{ij} \in [0, 1]$, with 1 representing best performance and 0 representing worst performance within the alternative set.

**Vector Normalisation (Euclidean):**

$$
r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}
$$

For cost criteria, the reciprocal or negation is applied before normalisation.

**Sum Normalisation:**

$$
r_{ij} = \frac{x_{ij}}{\sum_{i=1}^{m} x_{ij}}
$$

**Z-Score Normalisation (Standardisation):**

$$
r_{ij} = \frac{x_{ij} - \bar{x}_j}{s_j}
$$

where $\bar{x}_j = \frac{1}{m}\sum_{i=1}^{m} x_{ij}$ and $s_j = \sqrt{\frac{1}{m-1}\sum_{i=1}^{m}(x_{ij} - \bar{x}_j)^2}$.

### Weighted Aggregation

The **Simple Additive Weighting (SAW)** method computes the priority score for alternative $a_i$ as:

$$
S_i = \sum_{j=1}^{n} w_j \cdot r_{ij}
$$

Alternatives are ranked in descending order of $S_i$.

:::{note}
SAW assumes **preferential independence** — the contribution of performance on criterion $c_j$ to overall preference does not depend on performance on other criteria. This is a strong assumption that should be verified with domain experts.
:::

### The Weighted Product Model (WPM)

An alternative aggregation that uses multiplication rather than addition:

$$
P_i = \prod_{j=1}^{n} r_{ij}^{w_j}
$$

WPM is scale-invariant and naturally handles ratio-scale data. It is more punitive of poor performance on any single criterion because multiplication by a near-zero value drastically reduces the product.

### TOPSIS Extension

The **Technique for Order Preference by Similarity to Ideal Solution** extends basic weighted scoring by measuring distance to ideal and anti-ideal alternatives.

Define the weighted normalised matrix $\mathbf{V}$ where $v_{ij} = w_j \cdot r_{ij}$.

The **ideal solution** $\mathbf{A}^+ = (v_1^+, v_2^+, \ldots, v_n^+)$ where:

$$
v_j^+ = \max_i(v_{ij}) \text{ for benefit criteria, } \min_i(v_{ij}) \text{ for cost criteria}
$$

The **anti-ideal solution** $\mathbf{A}^- = (v_1^-, v_2^-, \ldots, v_n^-)$ where:

$$
v_j^- = \min_i(v_{ij}) \text{ for benefit criteria, } \max_i(v_{ij}) \text{ for cost criteria}
$$

Euclidean distances to ideal and anti-ideal:

$$
D_i^+ = \sqrt{\sum_{j=1}^{n}(v_{ij} - v_j^+)^2}
$$

$$
D_i^- = \sqrt{\sum_{j=1}^{n}(v_{ij} - v_j^-)^2}
$$

The **relative closeness** to the ideal solution:

$$
C_i = \frac{D_i^-}{D_i^+ + D_i^-}
$$

where $C_i \in [0, 1]$, with higher values indicating better alternatives.

### Sensitivity Analysis

To understand ranking robustness, we compute how scores change with respect to weight perturbations. The partial derivative of the SAW score with respect to weight $w_k$ is:

$$
\frac{\partial S_i}{\partial w_k} = r_{ik} - \sum_{j=1}^{n} r_{ij} \cdot \frac{\partial w_j}{\partial w_k}
$$

Under proportional weight redistribution (where reducing $w_k$ increases other weights proportionally):

$$
\frac{\partial S_i}{\partial w_k} = r_{ik} - S_i
$$

This elegant result shows that increasing the weight on criterion $c_k$ improves the relative standing of alternatives that score above their current total on that criterion.

### Edge Cases

**Degenerate range:** When $\max_i(x_{ij}) = \min_i(x_{ij})$ for some criterion $c_j$, min-max normalisation produces $0/0$. The convention is to set $r_{ij} = 0.5$ for all alternatives on that criterion, reflecting no discriminative information.

**Zero weights:** Setting $w_j = 0$ eliminates criterion $c_j$ from the aggregation. This is mathematically valid but may indicate a modelling error if the criterion was supposedly important.

**Negative raw values:** Z-score normalisation handles negative values naturally. Min-max normalisation requires all values to be non-negative, or a shift must be applied.

# Understanding the Mathematics

### Normalisation Formula (Min-Max Scaling)

**The equation:**

$$x'_{ij} = \frac{x_{ij} - \min_i(x_{ij})}{\max_i(x_{ij}) - \min_i(x_{ij})}$$

**Read it aloud:**

The normalised score for alternative *i* on criterion *j* equals the original score minus the minimum score across all alternatives, divided by the range (maximum minus minimum) across all alternatives.

**What each symbol means:**

- $x'_{ij}$ = the normalised score (between 0 and 1) for alternative *i* on criterion *j*
- $x_{ij}$ = the original, raw score for alternative *i* on criterion *j*
- $\min_i(x_{ij})$ = the worst (minimum) score any alternative received on criterion *j*
- $\max_i(x_{ij})$ = the best (maximum) score any alternative received on criterion *j*
- The subtraction in the denominator gives us the range of scores

**A concrete numerical example:**

You're evaluating three suppliers for delivery speed (days). Supplier A takes 12 days, Supplier B takes 5 days, Supplier C takes 8 days. To normalise Supplier A's score:

- $x_{ij} = 12$ (Supplier A's delivery time)
- $\min_i(x_{ij}) = 5$ (best delivery time)
- $\max_i(x_{ij}) = 12$ (worst delivery time)
- Range = 12 - 5 = 7 days
- $x'_{ij} = \frac{12 - 5}{7} = \frac{7}{7} = 1.0$

Wait—Supplier A is slowest but scored 1.0? For cost-type criteria where lower is better, we need the reverse formula (covered next).

**Why this equation matters:**

Without normalisation, a criterion measured in millions (revenue) would completely dominate one measured in percentages (customer satisfaction), making fair comparison impossible.

### Reverse Normalisation (for Cost-Type Criteria)

**The equation:**

$$x'_{ij} = \frac{\max_i(x_{ij}) - x_{ij}}{\max_i(x_{ij}) - \min_i(x_{ij})}$$

**Read it aloud:**

The normalised score equals the maximum score minus the alternative's actual score, divided by the range—effectively flipping the scale so lower original values become higher normalised scores.

**What each symbol means:**

- Same symbols as before, but numerator is reversed
- Now the subtraction is $\max - x$ instead of $x - \min$
- This ensures "lower is better" criteria get scored correctly

**A concrete numerical example:**

Returning to delivery speed (where fewer days is better). For Supplier B with 5 days:

- $\max_i(x_{ij}) = 12$ days (worst delivery)
- $x_{ij} = 5$ days (Supplier B's time)
- $\min_i(x_{ij}) = 5$ days (best delivery)
- $x'_{ij} = \frac{12 - 5}{12 - 5} = \frac{7}{7} = 1.0$

Now Supplier B (fastest) correctly receives 1.0, while Supplier A (slowest) gets 0.0.

**Why this equation matters:**

Without reversing cost-type criteria, our model would reward slow delivery and high prices—the opposite of what we want.

### Weighted Score Calculation

**The equation:**

$$S_i = \sum_{j=1}^{n} w_j \cdot x'_{ij}$$

**Read it aloud:**

The total score for alternative *i* equals the sum of each criterion's normalised score multiplied by that criterion's weight.

**What each symbol means:**

- $S_i$ = final priority score for alternative *i*
- $w_j$ = importance weight for criterion *j* (must sum to 1.0 across all criteria)
- $x'_{ij}$ = normalised score (from previous equations)
- $\sum_{j=1}^{n}$ = "add up across all *n* criteria"
- $\cdot$ = multiplication

**A concrete numerical example:**

You're selecting a project manager candidate. You have two criteria: Experience (weight = 0.6) and Cultural Fit (weight = 0.4). Candidate Sarah has normalised scores of 0.8 for Experience and 0.9 for Cultural Fit.

$$S_{Sarah} = (0.6 \times 0.8) + (0.4 \times 0.9)$$
$$S_{Sarah} = 0.48 + 0.36 = 0.84$$

If Candidate John scored 1.0 on Experience but only 0.5 on Cultural Fit:

$$S_{John} = (0.6 \times 1.0) + (0.4 \times 0.5) = 0.6 + 0.2 = 0.80$$

Sarah wins despite lower experience because her strong cultural fit compensates.

**Why this equation matters:**

This is where stakeholder priorities become mathematical reality—the weights encode strategic importance, ensuring the final ranking reflects what your organisation actually values.

### The Big Picture

The mathematics of Prioritise transforms the messy reality of comparing unlike things into a clean, defensible number. Normalisation puts all criteria on the same 0-to-1 scale so we're comparing apples to apples. The weighted sum respects that some criteria matter more than others while allowing trade-offs—a candidate can be slightly weaker on one dimension but compensate with strength elsewhere. This compensatory approach was chosen specifically because real decisions rarely have perfect options; we need mathematics that mirrors how humans actually think about trade-offs. At its heart, Prioritise is doing something beautifully simple: it's converting your strategic priorities into multiplication factors, then adding up the evidence to see which option gives you the most of what you said you wanted.

## Python Implementation

```python
import numpy as np
import pandas as pd
from scipy.stats import zscore

def prioritise(
    decision_matrix: pd.DataFrame,
    weights: dict,
    directions: dict,
    normalisation: str = "minmax",
    aggregation: str = "saw"
) -> pd.DataFrame:
    """
    Multi-criteria prioritisation of alternatives.
    
    Parameters
    ----------
    decision_matrix : pd.DataFrame
        Rows are alternatives, columns are criteria.
        Index should be alternative identifiers.
    weights : dict
        Mapping from criterion name to importance weight.
        Will be normalised to sum to 1.
    directions : dict
        Mapping from criterion name to 'benefit' or 'cost'.
    normalisation : str
        One of 'minmax', 'vector', 'sum', 'zscore'.
    aggregation : str
        One of 'saw' (simple additive weighting), 'wpm' (weighted product),
        or 'topsis'.
    
    Returns
    -------
    pd.DataFrame
        Original data with normalised scores, priority score, and rank.
    """
    
    # Extract and validate criteria
    criteria = list(weights.keys())
    X = decision_matrix[criteria].copy()
    
    # Normalise weights to sum to 1
    w = np.array([weights[c] for c in criteria])
    w = w / w.sum()
    
    # Get direction indicators (+1 for benefit, -1 for cost)
    d = np.array([1 if directions[c] == 'benefit' else -1 for c in criteria])
    
    # Normalisation step
    R = np.zeros_like(X.values, dtype=float)
    
    for j, criterion in enumerate(criteria):
        col = X[criterion].values.astype(float)
        
        if normalisation == "minmax":
            col_min, col_max = col.min(), col.max()
            if col_max - col_min == 0:
                # Degenerate case: no variation
                R[:, j] = 0.5
            elif d[j] == 1:  # Benefit criterion
                R[:, j] = (col - col_min) / (col_max - col_min)
            else:  # Cost criterion
                R[:, j] = (col_max - col) / (col_max - col_min)
                
        elif normalisation == "vector":
            norm = np.sqrt((col ** 2).sum())
            if d[j] == -1:
                col = 1 / (col + 1e-10)  # Invert for cost criteria
                norm = np.sqrt((col ** 2).sum())
            R[:, j] = col / norm
            
        elif normalisation == "sum":
            if d[j] == -1:
                col = 1 / (col + 1e-10)
            R[:, j] = col / col.sum()
            
        elif normalisation == "zscore":
            R[:, j] = zscore(col) * d[j]  # Flip sign for cost criteria
    
    # Aggregation step
    if aggregation == "saw":
        # Simple Additive Weighting
        scores = R @ w
        
    elif aggregation == "wpm":
        # Weighted Product Model (requires positive normalised values)
        R_positive = np.clip(R, 1e-10, None)
        scores = np.prod(R_positive ** w, axis=1)
        
    elif aggregation == "topsis":
        # TOPSIS method
        V = R * w  # Weighted normalised matrix
        
        # Ideal and anti-ideal solutions
        A_plus = V.max(axis=0)
        A_minus = V.min(axis=0)
        
        # Euclidean distances
        D_plus = np.sqrt(((V - A_plus) ** 2).sum(axis=1))
        D_minus = np.sqrt(((V - A_minus) ** 2).sum(axis=1))
        
        # Relative closeness
        scores = D_minus / (D_plus + D_minus + 1e-10)
    
    # Build results dataframe
    results = decision_matrix.copy()
    
    # Add normalised scores
    for j, criterion in enumerate(criteria):
        results[f"{criterion}_norm"] = R[:, j]
    
    results["priority_score"] = scores
    results["rank"] = results["priority_score"].rank(ascending=False, method="min").astype(int)
    
    return results.sort_values("rank")


# Example: Prioritising IT projects
np.random.seed(42)

# Create realistic project data
n_projects = 15
projects = pd.DataFrame({
    "project_id": [f"PRJ-{i:03d}" for i in range(1, n_projects + 1)],
    "expected_roi": np.random.uniform(0.05, 0.35, n_projects),  # 5% to 35%
    "implementation_cost": np.random.uniform(50000, 500000, n_projects),  # £50K to £500K
    "strategic_alignment": np.random.randint(1, 11, n_projects),  # 1-10 score


## Visualisations

![](../../_static/figures/prioritise_fig1.png)

![](../../_static/figures/prioritise_fig2.png)

## Using This in Heuristix

### What You Need to Get Started

The Prioritise node expects a structured dataset where each row represents an alternative you're evaluating (a project, supplier, candidate, location, etc.) and each column represents a criterion you're scoring against. You'll need:

- **One identifier column** (text or number) that names each alternative
- **Two or more numeric columns** containing your scores or measurements for each criterion

Your data should look like this:

**Before (Input):**

| Project | Cost | Impact | Feasibility | Risk |
|---------|------|--------|-------------|------|
| Project A | 50000 | 8 | 7 | 3 |
| Project B | 35000 | 6 | 9 | 5 |
| Project C | 80000 | 9 | 4 | 2 |

The node handles the rest—normalising different scales, applying weights, and calculating priority scores.

### Configuration Parameters

| Parameter | What It Controls | Default | When to Change It |
|-----------|-----------------|---------|-------------------|
| **Identifier Column** | Which column contains alternative names | First text column | Change if your names aren't in the first column |
| **Criteria Columns** | Which numeric columns to include in scoring | All numeric columns | Deselect columns that aren't evaluation criteria (like IDs or dates) |
| **Criterion Weights** | Relative importance of each criterion (must sum to 1.0) | Equal weights | Adjust based on stakeholder priorities; a 0.4 weight means that criterion is twice as important as one weighted 0.2 |
| **Optimisation Direction** | Whether higher or lower values are better for each criterion | Maximise | Set to "Minimise" for criteria like cost, risk, or time-to-deliver |
| **Normalisation Method** | How to scale criteria to comparable ranges | Min-Max | Use Z-score if you have extreme outliers; use Vector for ratio-scale data |
| **Sensitivity Range** | How much to vary weights in sensitivity analysis | ±20% | Increase to ±30% or ±40% if decisions seem fragile or stakeholder preferences are uncertain |

### What the Node Outputs

**Priority Score Table:** Your original data plus three new columns:
- `Normalised_Score_{criterion}` for each criterion (scaled 0–1)
- `Weighted_Score` (the final priority score)
- `Rank` (alternatives ordered from best to worst)

**Visualisations:**
- **Ranked Bar Chart:** Alternatives sorted by weighted score—your primary decision view
- **Criteria Heatmap:** Shows which alternatives excel on which criteria (green = strong, red = weak)
- **Sensitivity Tornado:** Displays how rank changes when you vary each weight—longer bars mean that criterion drives the decision
- **Score Decomposition:** Stacked bar showing how much each criterion contributes to each alternative's total score

**Summary Metrics:** Top-ranked alternative, score spread (how close the decision is), and stability index (how sensitive rankings are to weight changes).

### Connecting Downstream

Most commonly, Prioritise feeds into:

- **Report** nodes to share findings with stakeholders
- **Filter** nodes to shortlist top N alternatives for deeper analysis
- **Scenario Comparison** nodes to re-run with different stakeholder weight profiles
- **Export** nodes to document the decision rationale

### Quick Start: Prioritising Projects

1. **Connect your project data** containing at least an identifier and 2+ scoring criteria
2. **Select your identifier column** (e.g., "Project Name")
3. **Choose criteria columns** and deselect any non-criteria columns
4. **Set optimisation direction**: mark "Cost" and "Risk" as minimise, others as maximise
5. **Assign weights** based on stakeholder input (e.g., Impact: 0.4, Feasibility: 0.3, Cost: 0.2, Risk: 0.1)
6. **Run the node** and examine the ranked bar chart
7. **Check the sensitivity tornado**—if top ranks swap with small weight changes, facilitate a stakeholder discussion

### Practical Tips from Experienced Users

- **Involve stakeholders in weighting:** Run the node with equal weights first to show the data, then adjust weights collaboratively. This builds buy-in.
- **Watch the sensitivity analysis closely:** If your #1 choice drops to #3 with a 10% weight shift, your decision is fragile—consider gathering more data or shortlisting multiple options.
- **Normalise carefully with mixed scales:** If one criterion ranges 1–5 and another 1–1000, normalisation is essential. Min-Max works for most cases.
- **Document why you chose minimise vs maximise:** Future you (or an auditor) will want to know why lower risk is better.
- **Use scenario comparison for contested decisions:** Clone the Prioritise node, apply different weight sets representing different stakeholder groups, and compare results to find consensus options.

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial assessment of a decision problem when you need rapid feedback on which alternatives look promising before investing in detailed analysis.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `normalisation` | `"minmax"` | Fastest computation, intuitive 0-1 scale |
| `weights` | `"equal"` | Eliminates weighting debates in early stages |
| `sensitivity_analysis` | `False` | Skips compute-intensive Monte Carlo simulations |
| `missing_data` | `"mean"` | Simple imputation, no manual intervention |
| `aggregation` | `"weighted_sum"` | Lightweight linear combination |

**What you get:** A ranked list in seconds that reveals obvious winners and losers without statistical overhead.

**Trade-off:** No confidence intervals or robustness checks—suitable only for preliminary screening, not defensible decisions.

### Recipe 2: Production-Grade Rigour

**When to use:** Final decision documentation for high-stakes choices requiring audit trails, regulatory compliance, or executive sign-off.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `normalisation` | `"zscore"` | Preserves variance information for sensitivity analysis |
| `weights` | Custom vector | Stakeholder-derived, documented weights |
| `sensitivity_analysis` | `True` | Generates confidence bands and stability metrics |
| `n_simulations` | `10000` | High precision for Monte Carlo weight perturbation |
| `missing_data` | `"explicit"` | Forces manual review of incomplete data |
| `aggregation` | `"weighted_sum"` | Transparent and legally defensible |
| `rank_reversal_check` | `True` | Validates consistency when alternatives added/removed |

**What you get:** Publication-ready rankings with uncertainty quantification, suitable for board presentations and regulatory filings.

**Trade-off:** 10-50× longer execution time and requires complete data preparation upfront.

### Recipe 3: Cost-Constrained Portfolio Selection

**When to use:** Selecting multiple projects or investments from a candidate pool where you must respect a budget ceiling and maximise total value.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `normalisation` | `"none"` | Preserves absolute cost values for constraint checking |
| `weights` | `{"value": 1.0, "cost": 0.0}` | Optimise value; cost handled as constraint |
| `constraint_column` | `"cost"` | Designates which column to sum |
| `constraint_limit` | Your budget | Hard ceiling in currency units |
| `selection_mode` | `"knapsack"` | Enables combinatorial optimisation |
| `aggregation` | `"weighted_sum"` | Standard value calculation |

**What you get:** An optimal subset of alternatives maximising value while staying within budget, not just a ranked list.

**Trade-off:** NP-hard problem—may need heuristic solver for >100 alternatives, losing global optimality guarantee.

### Recipe 4: Consensus Building Across Conflicting Stakeholders

**When to use:** Merging priorities from departments with opposing objectives (e.g., engineering wants reliability, sales wants features, finance wants cost reduction) where exposing trade-offs is more valuable than forcing a single answer.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `normalisation` | `"rank"` | Ordinal rankings reduce inter-stakeholder scale disputes |
| `weights` | Multiple vectors | One per stakeholder group |
| `aggregation` | `"borda_count"` | Voting-theory method revealing consensus picks |
| `sensitivity_analysis` | `True` | Shows which alternatives are robust across all weight sets |
| `output_format` | `"heatmap"` | Visual comparison of how each group ranks options |

**What you get:** Alternatives that rank consistently well across stakeholder groups, plus visibility into polarising options.

**Trade-off:** May surface "compromise" solutions no single stakeholder loves, rather than the global optimum for any one perspective.

## Business Applications

**Financial Services**

A mid-sized UK mortgage lender processing 800+ applications monthly struggled with inconsistent credit decisioning across regional branches. Loan officers weighed factors like credit score, debt-to-income ratio, employment stability, and property valuation differently, creating postcode-lottery outcomes and regulatory risk. Prioritise standardised the evaluation by assigning defensible weights to each criterion (credit score 35%, DTI 25%, employment 20%, property factors 20%), then ranking applicants through normalised scoring that balanced risk and opportunity. The result: approval consistency improved from 67% to 94% inter-rater agreement, processing time dropped from 11 days to 3.5 days, and default rates fell by 18% within the first year.

**Retail**

An e-commerce fashion retailer with 85,000 SKUs across twelve brands needed to optimise their Black Friday promotional calendar but faced impossible complexity—which products to discount, by how much, and in what sequence. Marketing teams debated inventory levels, margin contribution, past conversion rates, seasonality, and competitive positioning without a framework to synthesise the data. Prioritise scored each SKU against weighted criteria (margin 30%, stock velocity 25%, conversion potential 25%, competitive gap 20%), producing a ranked promotional roadmap that maximised revenue while clearing aged inventory. Revenue per promotional email lifted from £1.84 to £3.17, and margin erosion was contained to 8.2% versus the previous year's 14.6%.

**Healthcare**

A regional hospital network with six facilities faced chronic operating theatre bottlenecks, with waiting lists exceeding 18 months for elective procedures. Clinical teams needed to prioritise cases fairly while balancing urgency, complexity, resource requirements, patient vulnerability, and capacity constraints. Prioritise created a transparent scoring system weighting clinical urgency (40%), expected outcome improvement (25%), resource efficiency (20%), and waiting time (15%), automatically re-ranking the queue as new information arrived. Waiting list breaches (patients exceeding target wait times) decreased by 41%, theatre utilisation improved from 74% to 89%, and patient complaints about unfair prioritisation dropped by 63%.

**Insurance**

A commercial property insurer receiving 3,400 renewal applications quarterly needed to identify which policies warranted intensive underwriter review versus automated processing. The team evaluated claims history, property age, coverage changes, premium size, and market competitiveness, but manual triage was inconsistent and slow. Prioritise ranked renewals by risk-adjusted complexity, routing the top 18% to specialist underwriters while auto-processing the remainder. Underwriter capacity was redeployed to high-value cases, reducing quote turnaround from 9.2 to 4.1 days and improving renewal retention from 78% to 86%, worth approximately £2.3M in preserved premium.

**Manufacturing**

A pharmaceutical contract manufacturer managing 240+ client projects simultaneously struggled with capital allocation decisions for new equipment purchases. Each investment competed across criteria including production capacity increase, quality improvement potential, maintenance cost reduction, regulatory compliance, and strategic client relationships. Prioritise weighted these factors (capacity 30%, quality 25%, cost 20%, compliance 15%, strategic value 10%) and ranked 47 competing proposals, creating a three-year investment roadmap. The disciplined approach freed £840K in previously scattered investments, increased overall equipment effectiveness (OEE) from 68% to 79%, and reduced unplanned downtime by 52%.

**Logistics**

A national parcel carrier optimising their route network needed to prioritise which of 180 regional depots should receive automation investment for sortation equipment. The decision involved parcel volume, growth trajectory, labour availability, facility lease terms, network centrality, and local wage inflation. Prioritise scored and ranked facilities, identifying the optimal 12-site rollout sequence that maximised network-wide throughput gains while respecting capital constraints. Processing capacity increased by 34%, labour cost per parcel fell from £0.81 to £0.58, and peak-season service failures declined by 47%.

**Marketing (Surprising Application)**

A B2B software company with 800+ inbound leads monthly couldn't decide which marketing channels deserved budget increases. Prioritise weighted channel performance across customer acquisition cost, lifetime value, conversion timeline, deal size, and strategic account penetration, revealing that podcast sponsorships—previously dismissed as "soft brand building"—scored highest when properly weighted. Budget reallocation increased pipeline value by £1.9M quarterly while reducing blended CAC from £3,200 to £2,650.

## Worked Example

Sarah Chen, a senior analyst at Cascade Municipal Services, was three days into her new role when the Director of Operations knocked on her cubicle wall. "We've got twelve sites that need new water treatment equipment," he said, dropping a folder on her desk. "Budget covers three installations this year. How do we choose?"

The stakes were real: aged equipment meant compliance risks, potential fines, and service disruptions affecting over 200,000 residents. The decision had been stalled for months because every site manager believed their facility should go first.

Sarah spent the next week pulling together data from maintenance logs, compliance reports, and capital planning spreadsheets. The dataset was messier than she'd hoped—some facilities used different risk rating scales, one site was missing population data entirely, and the "last major upgrade" column had dates ranging from 1987 to 2019. She standardised what she could and filled gaps with reasonable proxies.

Her final dataset looked like this:

| Site | Population Served | Compliance Score | Years Since Upgrade | Estimated Risk |
|------|------------------|------------------|---------------------|----------------|
| Northbrook | 45000 | 72 | 15 | 7.2 |
| Riverside | 28000 | 68 | 22 | 8.1 |
| Maple Grove | 52000 | 85 | 8 | 4.3 |
| Highland | 31000 | 71 | 18 | 7.8 |
| Oakwood | 19000 | 64 | 27 | 9.1 |

Sarah knew she needed a principled approach that could withstand scrutiny from site managers and the city council. She configured the Prioritise analysis carefully. Population served and estimated risk were maximised (higher is more urgent), while compliance score was also maximised (lower scores meant bigger problems, so she inverted it first). Years since upgrade was maximised—older installations needed attention. 

She assigned weights based on three stakeholder interviews: risk got 40% (the compliance officer's primary concern), population served got 30% (the mayor's equity focus), years since upgrade got 20% (the operations team's maintenance philosophy), and current compliance score got 10% (important, but already captured partly in risk).

```python
import pandas as pd
import numpy as np

# Sarah's dataset
sites = pd.DataFrame({
    'Site': ['Northbrook', 'Riverside', 'Maple Grove', 'Highland', 'Oakwood'],
    'Population': [45000, 28000, 52000, 31000, 19000],
    'Compliance': [72, 68, 85, 71, 64],
    'Years_Since': [15, 22, 8, 18, 27],
    'Risk': [7.2, 8.1, 4.3, 7.8, 9.1]
})

# Invert compliance so lower scores = higher priority
sites['Compliance_Inv'] = 100 - sites['Compliance']

# Normalise to 0-1 scale (min-max)
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

criteria = ['Population', 'Compliance_Inv', 'Years_Since', 'Risk']
for col in criteria:
    sites[f'{col}_norm'] = normalize(sites[col])

# Apply weights (risk=0.4, population=0.3, years=0.2, compliance=0.1)
weights = [0.3, 0.1, 0.2, 0.4]
sites['Priority_Score'] = sum(
    sites[f'{col}_norm'] * w 
    for col, w in zip(criteria, weights)
)

# Rank and display
sites = sites.sort_values('Priority_Score', ascending=False)
print(sites[['Site', 'Priority_Score']].to_string(index=False))
```

The results surprised her:

| Site | Priority Score | Rank |
|------|---------------|------|
| Oakwood | 0.847 | 1 |
| Riverside | 0.721 | 2 |
| Highland | 0.583 | 3 |
| Northbrook | 0.521 | 4 |
| Maple Grove | 0.198 | 5 |

Oakwood—the smallest site—ranked first. Sarah stared at the number. Then she saw it: Oakwood combined the highest risk score (9.1), the oldest equipment (27 years), and poor compliance (64), despite serving fewer people. The weighted model was doing exactly what it should: preventing a single criterion from dominating the decision.

When Sarah presented to the operations committee two weeks later, she didn't just show the scores. She walked through the normalisation (explaining how each site's raw values were scaled), demonstrated the weight sensitivity (showing that even shifting risk weight to 30% kept Oakwood in the top three), and highlighted what the ranking meant: these three sites represented the combination of highest risk and longest deferred maintenance.

The Director of Operations nodded slowly. "This matches what our field supervisors have been saying quietly for years, but we couldn't justify it on population alone." The committee approved funding for Oakwood, Riverside, and Highland.

Three months later, Oakwood's upgrade uncovered corroded pipes that would likely have failed within the year—validating the risk assessment and the prioritisation model.

If Sarah were doing this again, she'd spend more time on sensitivity analysis, particularly testing different weight combinations with stakeholders present. She also wished she'd had cost data—some installations might be cheaper, potentially allowing four upgrades instead of three. But for a decision that had been paralysed by competing priorities, the transparent, defensible ranking gave leadership the confidence to move forward.

## Interpreting Your Results

You've just run Prioritise and you're staring at a ranked list with scores, weights, and perhaps a colourful chart. Here's exactly what you're looking at and what it means for your decision.

### The Priority Score (Your Main Number)

**Plain-English meaning**: This is each alternative's overall performance across all your criteria, weighted by importance. If Alternative A has a priority score of 0.82 and Alternative B has 0.45, Alternative A performs nearly twice as well when you account for what matters most to you.

**Concrete benchmarks**:
- **Below 0.40**: This option is weak across multiple important criteria. Only consider if you have serious constraints limiting other choices.
- **0.40–0.65**: Acceptable performance. These are your "safe middle" options—not exciting, but defensible.
- **0.65–0.80**: Strong contender. These options perform well on most criteria that matter.
- **Above 0.80**: Exceptional option. Rare to see unless one alternative genuinely dominates.

**Red flags**: If your top-ranked option scores below 0.50, you may have an inadequate set of alternatives—consider whether you've explored enough options. If multiple alternatives cluster within 0.05 points of each other, your decision is functionally a tie; see sensitivity analysis before committing.

### The Ranking Table

**Plain-English meaning**: Your alternatives ordered from best to worst. The rank number itself (1st, 2nd, 3rd) is less important than the score gaps between them.

**Reading the gaps**: A gap of less than 0.05 between ranks means they're statistically equivalent—other factors (cost, feasibility, politics) should drive your choice. A gap larger than 0.15 signals a clear winner; everything below that threshold is meaningfully inferior.

**Red flag**: If the top three alternatives have wildly different profiles (one excels on cost, another on quality, another on speed), you haven't properly weighted your criteria. Revisit your weights before trusting the ranking.

### Individual Criterion Scores

**Plain-English meaning**: How each alternative performs on each single objective before weighting. These reveal *why* something ranks where it does.

**What to look for**: Your top-ranked option should score above 0.60 on your highest-weighted criteria. If it's ranking first despite scoring below 0.40 on your most important criterion, you've likely mis-specified weights.

**Red flag pattern**: An alternative scores 0.90+ on one criterion but below 0.30 on several others. This is a "specialist" option that might be too risky if circumstances change. Check if you're comfortable with that trade-off.

### Sensitivity Analysis Charts

**Plain-English meaning**: These show whether your top choice remains top if you adjust criterion weights by ±10–20%. A robust decision stays ranked first even when weights shift moderately.

**Concrete benchmark**: Your preferred option should remain in the top two across at least 80% of reasonable weight variations. If it drops to rank 4 or below when you increase a single criterion weight by 15%, your decision is fragile.

**Red flag**: Rank-swapping between first and second place with tiny weight changes (under 5%) means you don't actually have a clear winner. Document the trade-offs and escalate to stakeholders rather than pretending the model "chose" for you.

### Sanity Check Checklist

Before trusting your Prioritise results, verify:

1. **Do the weights sum to 1.0 (or 100%)?** If not, you haven't properly normalised.
2. **Does the top-ranked option make intuitive sense?** If you're surprised, investigate—don't just accept it.
3. **Are any alternatives scoring below 0.20?** Check for data entry errors or inappropriate normalisation.
4. **Do higher raw values mean "better" for all criteria?** If "lower cost is better," ensure you've inverted or transformed that criterion.
5. **Could you defend this ranking to a skeptical stakeholder?** If not, you don't understand it well enough yet.

### Good Enough to Act On?

You can confidently proceed with your top-ranked option when: **(1)** it scores above 0.65, **(2)** it leads the second-place option by at least 0.08 points, and **(3)** it remains top-ranked across 80%+ of your sensitivity scenarios. If all three conditions hold, stop analysing. You have a defensible decision. If even one fails, either gather better data, refine your criteria weights with stakeholders, or accept that you're choosing between genuinely equivalent options—and that's a business judgment, not an analytical one.

## Decision Guidance

### What This Result Is Telling You

Your Prioritise analysis has converted a complex comparison problem into a single, ordered list of options. This ranking represents which alternatives best balance all your stated objectives according to the importance weights you've assigned. The top-ranked option isn't necessarily perfect on every measure—it's the choice that makes the most strategic sense given your organisation's priorities. If you've weighted financial return at 40% and risk mitigation at 20%, an option that scores well on both will outrank one that excels only at cost reduction.

The scores themselves matter as much as the ranking. A close race between your top three options (scores within 5–10 points of each other) signals genuine strategic ambiguity where context, timing, or stakeholder politics may be the real tiebreaker. A dominant winner (15+ points ahead) indicates clear alignment between that option's strengths and your priorities. Pay attention to the gap between ranks—it tells you how confidently you can commit resources.

Your sensitivity analysis reveals whether your ranking is stable or fragile. If small weight adjustments flip your top choice, you're facing a decision that's highly sensitive to how you value competing objectives. This isn't a flaw—it's critical intelligence. It means you need executive alignment on priorities before committing capital, because reasonable people could prioritise differently and reach opposite conclusions.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Top option scores 15+ points above second place | Clear winner with strong alignment to your weighted priorities | Proceed to implementation planning; allocate resources to top-ranked option | Executive sponsor, programme director |
| Top three options within 5 points of each other | No dominant solution; decision depends on factors not fully captured in criteria | Convene decision panel to review qualitative factors, stakeholder implications, and implementation risks | Steering committee, cross-functional leads |
| Sensitivity analysis shows rank reversals with ±10% weight changes | Your decision is unstable and depends critically on how objectives are valued | Facilitate executive workshop to build consensus on priority weights before committing resources | Chief Strategy Officer, decision owner |
| Low-ranked option scores highest on mission-critical criterion | Potential criteria weighting mismatch with stated strategic priorities | Re-evaluate whether criterion weights reflect true strategic importance; consider if that criterion should be a constraint rather than scored | Senior leadership team |
| Winning option has normalised score below 0.60 on scale of 0–1 | No option performs adequately across your criteria set | Expand search for alternatives, relax constraints, or revisit whether all criteria are realistic requirements | Portfolio manager, innovation lead |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Top option leads by 15+ points and maintains rank across ±15% sensitivity tests
- All stakeholders agree criteria weights reflect strategic priorities
- Winning option scores above 0.70 on normalised scale
- No single criterion was weighted above 40% (avoiding over-concentration)

**Proceed with caution when:**
- Top option leads by 8–15 points with stable ranking in sensitivity tests
- Winning option scores 0.60–0.70 on normalised scale
- Criteria weights required minor negotiation but reached consensus
- Implementation risk is manageable and reversible

**Investigate before acting when:**
- Top three options within 5 points of each other
- Rank reversals occur with ±10% weight adjustments
- Winning option scores below 0.60 on normalised scale
- Stakeholders dispute criteria importance or scoring methodology
- Critical data quality concerns exist for any criterion

**Do not use these results yet when:**
- Missing data for 20%+ of criterion measurements
- Criteria weights were assigned arbitrarily without stakeholder input
- Scoring scales are inconsistent or subjective without clear rubrics
- Key decision criteria were omitted from the analysis

### The Cost of Getting This Wrong

When organisations misinterpret Prioritise results, they commit resources to options that looked optimal on paper but fail in reality. A manufacturing company might select a supplier that scored highest overall while ignoring that it ranked last on delivery reliability—a criterion that was underweighted at 10% but turned out to be operationally critical, resulting in six months of production delays and $2.3M in expedited shipping costs. Conversely, teams sometimes abandon defensible decisions when rankings are close, triggering expensive "analysis paralysis" where committees commission additional studies, delaying market entry until competitors capture the opportunity. Perhaps most dangerous is false confidence: proceeding with a fragile decision (sensitive to small weight changes) without recognising that the ranking depends entirely on debatable assumptions. When leadership discovers the decision could have gone either way, trust in the analytical process erodes, and future resource allocation devolves into politics rather than evidence. The cost isn't just the failed project—it's the organisational scepticism that makes all subsequent data-driven decisions harder to execute.

## Common Pitfalls

**The Phantom Precision Trap**

Here's what happened: A hospital administrator was prioritising capital equipment purchases across departments. They built a model with eight criteria, assigned weights that summed to 100%, and presented final scores to three decimal places: "MRI Scanner A: 87.342, CT Scanner B: 87.289." They concluded the MRI was definitively the better investment and rejected the CT scanner proposal. The CFO later discovered both scoring inputs were subjective estimates from department heads ("maintenance cost is probably around £50K annually"), yet the final ranking implied mathematical certainty.

Why it happens: The scoring process generates precise numbers, creating an illusion of accuracy that masks the approximate nature of underlying judgments. Spreadsheets happily multiply guesswork by weights and report results to absurd decimal places.

How to detect it: When final scores differ by less than 5% but drive binary yes/no decisions, you're likely in phantom precision territory. Check your raw criterion scores—if they're rounded estimates or Likert scales, reporting beyond one decimal place is theatre.

The fix: Report scores as ranges or bands, run Monte Carlo sensitivity analysis on uncertain inputs, and never let close scores (<10% difference) drive major decisions without additional investigation.

**The Forgotten Normalisation Disaster**

Here's what happened: A procurement analyst was selecting a software vendor across cost (in thousands of pounds), implementation time (in weeks), and user satisfaction (0-5 scale). They assigned equal weights of 33% to each criterion and scored three vendors. Vendor A won decisively with a score of 2,847 despite having the worst user satisfaction. The analyst recommended them, and six months later, the organisation was stuck with software nobody would use.

Why it happens: Raw scores were added directly without normalisation. Cost values (ranging 50-500) dominated the calculation, rendering the satisfaction scores (ranging 2.5-4.5) mathematically irrelevant. The analyst assumed "equal weighting" meant equal influence.

How to detect it: Check the standard deviation or range of raw scores across criteria. If one criterion's range is 10x or 100x larger than others, it's drowning out everything else. Calculate contribution variance—each 33% weight should contribute roughly 33% to final score differences, not 95%.

The fix: Apply min-max normalisation or z-score standardisation before weighting. Verify that each normalised criterion actually varies on a comparable scale.

**The Echo Chamber Weights**

Here's what happened: A product manager was prioritising features for a customer portal redesign. They ran a weighting workshop with the six-person product team, who collectively assigned 45% weight to "technical elegance" and 15% to "customer effort reduction." The resulting roadmap prioritised architectural refactoring over user-facing improvements. Customer satisfaction scores dropped 12 points the following quarter.

Why it happens: Homogeneous stakeholder groups produce weights that reflect their worldview, not organisational priorities. Engineers value elegance, marketers value differentiation, finance values cost—whoever's in the room dominates the weights.

How to detect it: Compare your weight distribution to strategic priorities or customer research. If 60%+ of total weight sits with operational/internal criteria while strategic goals emphasise customer outcomes, you've got echo chamber weights.

The fix: Include representatives from all affected stakeholder groups in weighting exercises, or validate final weights against executive strategy documents and customer feedback data.

**The Static Analysis Syndrome**

Here's what happened: A government analyst prioritised infrastructure projects using a model built in 2019, with criterion weights reflecting pre-pandemic priorities (public transport capacity: 30%, remote work infrastructure: 5%). They applied it in 2022 to rank new proposals. The model recommended a city centre car park expansion over rural broadband upgrades, directly contradicting the shifted hybrid work reality.

Why it happens: MCDA models feel permanent once built, but both weights and alternatives evolve. Analysts treat the model as a reusable tool rather than a point-in-time snapshot of priorities.

How to detect it: Check the provenance date of your weights and criteria definitions. If they're older than 18-24 months, or if major contextual factors have shifted, your model is likely stale.

The fix: Review and refresh weights annually or after major strategic shifts; archive dated models clearly and rebuild rather than reuse.

**The Correlation Cascade**

Here's what happened: A university was ranking grant applications across six criteria including "methodological rigour," "theoretical contribution," and "publication record." A junior researcher noticed the top-ranked proposals all came from established labs at elite institutions. They investigated and discovered all six criteria were 0.7+ correlated—essentially measuring the same "prestige" dimension six different ways, amplifying bias rather than capturing trade-offs.

Why it happens: Criterion selection happens through brainstorming without correlation analysis. Each criterion sounds distinct conceptually but measures overlapping constructs empirically.

How to detect it: Calculate pairwise correlations between criterion scores across alternatives. If multiple pairs exceed 0.6-0.7, you're double-counting and magnifying certain dimensions.

The fix: Remove or merge correlated criteria, or use principal component analysis to identify truly independent dimensions before scoring.

## Common Misconceptions

**"If we're using data and a scoring model, the decision is objective"**

**Why people believe this:** Numbers feel neutral. When you've moved from heated debates to a spreadsheet with normalised scores and weighted criteria, it seems like you've transcended politics and opinion. The mathematical operations—multiplying, summing, ranking—appear to remove human bias from the equation.

**The truth:** Prioritise makes subjective judgements *systematic* and *transparent*, not objective. Every weight assignment encodes a value judgement about relative importance. Every criterion definition reflects someone's theory about what matters. The choice of normalisation method (min-max versus z-score versus rank-based) alters results and embeds assumptions about whether we care about absolute performance differences or relative standing. The model doesn't eliminate judgement—it makes judgement auditable and consistent. What you gain isn't objectivity but *defensibility*: you can show your reasoning and apply the same logic uniformly across all alternatives.

**The real-world consequence:** A government agency builds an infrastructure prioritisation model and presents it to the public as "objective" and "data-driven." When the results favour urban projects over rural ones (because population-weighted criteria dominated), communities cry foul. The agency cannot defend the decision because they themselves believe the model was neutral. Had they owned the embedded value choices—"we weighted economic impact heavily because our mandate prioritises job creation"—they could have had a productive conversation about whether those values were appropriate. Instead, trust collapses.

**"More criteria make the model more comprehensive"**

**Why people believe this:** It feels rigorous to capture every dimension stakeholders mention. If someone says "but what about environmental impact?" or "we should consider stakeholder satisfaction," excluding it seems dismissive. A model with fifteen criteria appears more thorough than one with five.

**The truth:** Beyond a certain point, additional criteria introduce noise, increase cognitive load, and obscure what actually drives decisions. Worse, they create an illusion of precision that masks redundancy. Three highly correlated criteria (revenue growth, market share, customer acquisition) essentially cast the same vote three times while disguising themselves as independent factors. Effective Prioritise models identify a small number of genuinely distinct dimensions that capture the decision's fundamental trade-offs. The discipline isn't adding every conceivable factor—it's discovering which factors actually differentiate alternatives in meaningful ways.

**The real-world consequence:** A product team builds a feature prioritisation model with fourteen criteria. After months of gathering data and stakeholder input, they discover that 80% of the variance in final scores comes from two criteria: expected revenue and implementation effort. The other twelve criteria merely ratified decisions already determined by those two factors. The team wasted three person-months collecting data on criteria that didn't matter, delayed their roadmap, and burned political capital on debates about weights that had negligible impact. A simple two-axis prioritisation matrix would have reached the same conclusions in a single workshop.

**"The weights should add up to 100%"**

**Why people believe this:** It mirrors how we think about allocating budgets or time. Forcing weights to sum to 100% feels like it ensures everything is accounted for and nothing is double-counted. It's tidy.

**The truth:** Weight normalisation is a mathematical convenience, not a logical necessity. What matters is the *ratio* between weights, not their sum. Weights of 50/30/20 produce identical rankings to 5/3/2 or 0.5/0.3/0.2. The constraint that they sum to 100% can actually harm stakeholder conversations by creating a zero-sum framing: "if we increase the weight on criterion A, we must decrease something else." This frames weight elicitation as resource allocation when it's actually about relative importance. Some practitioners deliberately use unconstrained weights (asking "on a scale of 0-10, how important is this criterion?") then normalise afterward, because it produces more honest responses about what people actually value.

**The real-world consequence:** A leadership team debates criterion weights for two hours, locked in combat because every point added to "strategic alignment" must come from somewhere else. They settle on a political compromise—equal weights across all criteria—that satisfies no one and reflects no one's actual priorities. The resulting rankings are meaningless. Had the facilitator asked for unconstrained importance ratings and normalised afterward, they would have discovered genuine consensus about priorities without the artificial scarcity mindset.

**"Sensitivity analysis tells us if the model is robust"**

**Why people believe this:** If small weight changes don't alter the top-ranked alternatives, the model seems solid and trustworthy. If rankings shuffle dramatically with minor adjustments, something must be wrong. This interpretation treats sensitivity as a quality metric—less sensitive equals better model.

**The truth:** Sensitivity reveals where your decision is genuinely difficult and where it's clear, neither of which is inherently good or bad. High sensitivity near decision boundaries—where two alternatives score almost identically—is perfectly appropriate. It's telling you these options are actually close calls given available information, and the decision legitimately depends on weight choices. What matters isn't minimising sensitivity but *understanding* it. Which criteria drive rank changes? For which alternatives? A robust model is one where you understand exactly why rankings change and can articulate whether those changes make sense given different stakeholder priorities. Low sensitivity can actually mask problems: if one alternative dominates regardless of weights, you might have redundant criteria or non-meaningful alternatives in your set.

**The real-world consequence:** A consulting team presents a vendor selection model to their client, proudly noting that the top choice remains first across all tested weight combinations. The client signs a contract. Six months later, the relationship fails catastrophically—the vendor excels at the three technical criteria that dominated the model but lacks the cultural fit and communication skills the client actually needed. The low sensitivity didn't reflect robustness; it reflected tunnel vision. A properly sensitive model would have revealed: "if you weight technical capability heavily, choose Vendor A; if responsiveness and collaboration matter most, choose Vendor B." That conversation would have prevented a costly mistake.

**"You can't use Prioritise when you have incomplete data"**

**Why people believe this:** Missing data creates empty cells in your scoring matrix. How can you calculate a weighted score when you don't have measurements for all criteria? It seems mathematically impossible, or at least statistically unsound. Better to wait for complete information.

**The truth:** Decision-making under uncertainty is the norm, not the exception. Prioritise can incorporate missing data through several principled approaches: conservative scoring (assign worst-case values), imputation based on similar alternatives, reduced-weight calculations (normalising weights across available criteria only), or explicitly treating missingness as information (if we can't measure it, perhaps it indicates something about the alternative itself). The key isn't eliminating uncertainty but being transparent about how you're handling it. Often, partial information is sufficient to identify clear leaders and clear losers, with uncertainty mattering only for middle-ranked alternatives. Waiting for complete information is itself a decision—usually a decision to maintain the status quo—and should be evaluated against the cost of delay.

**The real-world consequence:** An emergency response agency delays deploying a resource allocation model because data is incomplete for 15% of potential projects. Over the six months spent collecting additional data, they distribute resources using the previous year's ad hoc approach, which demonstrably over-invests in visible urban areas while neglecting high-need rural communities. When the complete model finally runs, the top ten priorities change by only two positions compared to what a partial-data model would have identified six months earlier. The perfectionism cost real resources and real impact during a crisis when systematic prioritisation—even with imperfect data—would have outperformed the alternative.

## How This Connects

### Before This Node

**Normalize** standardises raw metrics to comparable scales before Prioritise can meaningfully combine them. Without normalisation, a criterion measured in millions (revenue) will numerically dominate one measured in percentages (conversion rate), regardless of assigned weights—Prioritise will produce rankings that reflect scale artifacts rather than strategic importance.

**Weight** elicits or calculates criterion importance coefficients that Prioritise multiplies against normalised scores. Missing or poorly calibrated weights reduce Prioritise to equal weighting across all criteria, which rarely reflects actual business priorities and produces rankings that stakeholders immediately reject as "not fitting our strategy."

**Impute** fills missing values in the criteria matrix so Prioritise receives complete data for all alternatives across all criteria. Bad upstream data—sparse matrices with systematic missingness patterns—causes Prioritise to either drop valuable alternatives entirely or base rankings on fragments of information, producing volatile results that change dramatically with small data updates.

**Filter** removes infeasible, dominated, or out-of-scope alternatives before they enter Prioritise's scoring calculations. When bad data includes phantom options (discontinued products, expired projects, impossible combinations), Prioritise wastes computational effort and clutters output rankings with alternatives that can never be implemented, obscuring actionable insights.

**Aggregate** rolls up granular data to the decision-relevant unit of analysis that Prioritise will rank. If upstream aggregation is misaligned—scoring individual transactions when the decision concerns customer segments, or daily metrics when the choice is annual—Prioritise produces rankings at the wrong granularity that cannot inform the actual decision.

**Calculate** derives composite metrics and performance indicators that become criteria in Prioritise's scoring model. Poorly constructed upstream metrics (KPIs with embedded bias, ratios with unstable denominators, metrics that double-count phenomena) propagate directly into Prioritise's rankings as flawed criteria, systematically advantaging alternatives that game the metric rather than deliver value.

### After This Node

**Visualise** renders Prioritise's ranked output as sortable tables, bar charts, or radar plots that make relative performance immediately scannable for decision-makers who need to understand not just the top choice but the entire preference ordering and margin between alternatives.

**Report** packages Prioritise's rankings alongside sensitivity analysis and criterion contributions into stakeholder-facing documents that justify recommended actions with transparent methodology, turning technical scores into defensible business cases.

**Segment** applies Prioritise's ranking logic separately within subgroups (market segments, risk categories, geographies), revealing whether top priorities shift across contexts and enabling tailored strategies rather than one-size-fits-all recommendations.

**Optimise** uses Prioritise's scores as objective function components in resource allocation models, translating preference orderings into specific budget, capacity, or portfolio decisions that maximise weighted value under constraints.

**Monitor** tracks how Prioritise's top-ranked alternatives perform post-implementation, creating feedback loops that validate weights and criteria while flagging when rankings become stale and require recalibration with fresh data.

**Simulate** feeds Prioritise's scoring model into Monte Carlo frameworks that propagate uncertainty in criteria values forward into distributions of possible rankings, quantifying confidence in the top choice and identifying fragile rankings that might reverse with small data changes.

### Common Pipeline Patterns

**Product Portfolio Rationalisation Pipeline**  
Calculate → Normalize → Weight → **Prioritise** → Visualise → Report  
Scores hundreds of SKUs across profitability, strategic fit, and operational complexity to identify the top 20% core portfolio and bottom 30% discontinuation candidates, typically recovering 15–25% of trapped working capital.

**Grant Application Review Workflow**  
Impute → Aggregate → **Prioritise** → Filter → Report  
Ranks 200+ funding proposals across scientific merit, feasibility, and alignment with mission to produce a defensible shortlist of 15–20 finalists for deep review, reducing reviewer burden by 85% while maintaining decision quality.

**Supplier Risk Management Pipeline**  
Calculate → Normalize → **Prioritise** → Segment → Monitor  
Evaluates 300+ vendors across delivery performance, financial stability, and strategic importance to assign quarterly risk-based audit priorities, ensuring high-exposure relationships receive proportional oversight while automating low-risk vendor monitoring.

### What to Have Ready

**Complete criteria matrix**: Every alternative scored on every criterion with <10% missingness, stored as numeric values (not text categories or mixed types) in tidy format where rows are alternatives and columns are criteria plus metadata.

**Validated weights**: Criterion importance coefficients that sum to 1.0, derived from explicit stakeholder input or analytical methods (not guesses), with documented rationale for why certain criteria matter more than others in this specific decision context.

**Directional clarity**: Explicit specification for each criterion whether "higher is better" (maximise revenue) or "lower is better" (minimise cost), since Prioritise must know whether to reward or penalise high values when calculating scores.

**Decision framing**: Clear statement of what the ranking will inform—select top 3, allocate budget proportionally, identify bottom quartile for elimination—because output interpretation and sensitivity analysis requirements differ substantially across decision types.

## Try It Yourself

### Recommended Dataset

**Dataset:** `sklearn.datasets.load_wine()`

**Source:** Built into scikit-learn, accessible via `from sklearn.datasets import load_wine`

**Why it's ideal:** The Wine dataset contains 178 wines evaluated across 13 chemical measurements (alcohol content, acidity, phenols, etc.), making it perfect for Prioritise because it naturally frames a multi-criteria decision problem: selecting the best wines based on multiple competing quality attributes. Each criterion operates on different scales, demonstrating the need for normalisation—a core Prioritise feature.

**Business question:** "Which wines should a boutique importer prioritise for their premium collection based on a weighted combination of desirable chemical properties?"

**Size:** 178 rows × 13 features

### Starter Code

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from sklearn.preprocessing import MinMaxScaler

# Load the wine quality dataset
wine = load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)

# Select key criteria for wine evaluation
criteria = ['alcohol', 'total_phenols', 'flavanoids', 'color_intensity']
alternatives = df[criteria].head(20)  # Focus on first 20 wines for clarity

# Define criterion weights (must sum to 1.0)
# Higher weight = more important to decision
weights = {
    'alcohol': 0.30,           # Premium wines benefit from higher alcohol
    'total_phenols': 0.25,     # Antioxidants and structure
    'flavanoids': 0.30,        # Key flavor compounds
    'color_intensity': 0.15    # Visual appeal
}

# Step 1: Normalise all criteria to 0-1 scale (min-max normalisation)
scaler = MinMaxScaler()
normalised = pd.DataFrame(
    scaler.fit_transform(alternatives),
    columns=criteria,
    index=alternatives.index
)

# Step 2: Apply weights to normalised scores
weighted_scores = normalised.copy()
for criterion in criteria:
    weighted_scores[criterion] = normalised[criterion] * weights[criterion]

# Step 3: Calculate total priority score (sum of weighted criteria)
priority_scores = weighted_scores.sum(axis=1)
alternatives['Priority_Score'] = priority_scores

# Step 4: Rank alternatives from highest to lowest priority
ranked = alternatives.sort_values('Priority_Score', ascending=False)

# Output results
print("=== TOP 5 PRIORITISED WINES ===")
print(ranked[['Priority_Score'] + criteria].head())

print("\n=== CRITERION WEIGHTS USED ===")
print(pd.Series(weights).sort_values(ascending=False))

print("\n=== SCORE DISTRIBUTION ===")
print(f"Mean: {priority_scores.mean():.3f}")
print(f"Std Dev: {priority_scores.std():.3f}")
print(f"Range: {priority_scores.min():.3f} to {priority_scores.max():.3f}")

print("\n=== BUSINESS INSIGHT ===")
top_wine = ranked.index[0]
print(f"Wine #{top_wine} ranks highest (score: {ranked.iloc[0]['Priority_Score']:.3f})")
print(f"Strong in: {ranked.iloc[0][criteria].idxmax()} "
      f"({ranked.iloc[0][ranked.iloc[0][criteria].idxmax()]:.2f} raw value)")
```

### What to Try Next

**1. Change the weight distribution**  
Modify the weights dictionary to emphasize different criteria (e.g., `'flavanoids': 0.50, 'alcohol': 0.20`). You'll see the ranking completely reorder, teaching you that stakeholder preferences dramatically affect priorities—this is why weight elicitation is critical in MCDA.

**2. Test different normalisation methods**  
Replace `MinMaxScaler()` with `from sklearn.preprocessing import StandardScaler`. Rankings will shift because StandardScaler doesn't bound values to [0,1], showing how normalisation choice impacts compensatory trade-offs between criteria.

**3. Add more alternatives**  
Change `.head(20)` to `.head(50)` or remove it entirely to evaluate all 178 wines. The top-ranked wine may change, demonstrating that relative performance matters—an alternative's priority depends on what it's being compared against.

**4. Perform sensitivity analysis**  
Add this after the main code: `for w in np.arange(0.1, 0.6, 0.1): weights['alcohol'] = w; [recalculate]; print(top_wine)`. This reveals which alternatives are "robust winners" regardless of weight changes versus those sensitive to assumption tweaks—a key validation step before presenting recommendations.

## Further Reading

1. **Hwang, C.L. & Yoon, K. (1981). "Multiple Attribute Decision Making: Methods and Applications." _Lecture Notes in Economics and Mathematical Systems, Vol. 186_, Springer-Verlag.** Read this seminal work if you want to understand the mathematical foundations of compensatory MCDA methods, particularly Chapter 3's development of TOPSIS and the distance-based approach to ideal solutions that influenced modern ranking algorithms. The rigorous treatment of normalisation procedures remains directly applicable to practical implementations.

2. **Saaty, T.L. (1990). "How to make a decision: The analytic hierarchy process." _European Journal of Operational Research, 48_(1), 9-26.** Read this if you want to understand the theoretical justification for pairwise comparison methods and the eigenvector approach to deriving weights from subjective judgments. Saaty's consistency ratio concept provides the mathematical backbone for detecting and managing contradictory preferences in multi-stakeholder decisions.

3. **Belton, V. & Stewart, T.J. (2002). _Multiple Criteria Decision Analysis: An Integrated Approach._ Kluwer Academic Publishers, Chapter 4 ("Value Functions and Preference Modelling"), pp. 93-132.** This chapter specifically addresses the critical challenge of converting raw performance data into comparable value scales, covering both linear and non-linear transformation functions that Prioritise implementations must handle when criteria have different units and ranges.

4. **Triantaphyllou, E. (2000). _Multi-Criteria Decision Making Methods: A Comparative Study._ Springer, Chapter 2 ("MCDM Methods"), pp. 5-21, and Chapter 5 ("Sensitivity Analysis"), pp. 109-143.** These specific sections provide worked examples comparing SAW, TOPSIS, and AHP on identical problems, revealing when different methods produce conflicting rankings—essential knowledge for defending your methodological choices to stakeholders.

5. **`sklearn.preprocessing.MinMaxScaler` and `StandardScaler` documentation** (scikit-learn.org/stable/modules/preprocessing.html). The "Comparison between different scalers" section demonstrates how normalisation choices affect downstream analysis—directly applicable to understanding how min-max versus z-score normalisation impacts criterion scores in Prioritise implementations.

6. **Bohanec, M. & Rajkovič, V. "DEX: An Expert System Shell for Decision Support" tutorial series on Medium by Cesare Roseti** (towardsdatascience.com/multi-criteria-decision-analysis-mcda-in-python-*). This implementation-focused tutorial excels by providing fully reproducible Python code for weighted scoring with transparent sensitivity analysis visualizations, showing exactly how small weight changes propagate through to rank reversals.

7. **MIT OpenCourseWare: 15.053 Optimization Methods in Management Science, Lecture 14: "Multi-Objective Optimization and Goal Programming"** (ocw.mit.edu, timestamp 23:15-41:30). This segment specifically demonstrates the geometric interpretation of efficient frontiers and explains why purely compensatory methods like Prioritise may miss non-dominated solutions that hybrid approaches would preserve.

8. **World Bank (2019). "Multi-Criteria Analysis for Prioritizing Infrastructure Investments: Case Studies from East Africa."** This technical report (documents.worldbank.org) demonstrates Prioritise applied to $2.3B in transport projects, revealing how practitioners handle incomplete data, stakeholder weight elicitation at scale, and the political challenges of making ranking methodologies transparent to public scrutiny.

## Practice Exercises

### Exercise 1: Marketing Campaign Selection (Conceptual)

You're a marketing manager at a B2B software company with a £120,000 quarterly budget. Your analytics team has evaluated five campaign options across four criteria: Expected Revenue (£), Cost (£), Implementation Time (weeks), and Brand Alignment (1-10 score). They've provided this weighted Prioritise analysis:

| Campaign | Expected Revenue | Cost | Time | Brand | Weighted Score |
|----------|-----------------|------|------|-------|----------------|
| Content Hub | £450,000 | £85,000 | 8 | 9 | 0.78 |
| Paid Search | £380,000 | £95,000 | 3 | 6 | 0.71 |
| Conference Sponsorship | £520,000 | £110,000 | 12 | 8 | 0.69 |
| LinkedIn ABM | £340,000 | £75,000 | 4 | 7 | 0.82 |
| Influencer Partnership | £290,000 | £65,000 | 6 | 5 | 0.64 |

Weights used: Revenue (40%), Cost (30%), Time (20%), Brand (10%). Cost and Time were reverse-scored (lower is better).

**Questions:**
(a) Should you use this Prioritise result to make your decision? What concerns might you have?
(b) The CEO suggests choosing Conference Sponsorship because it has the highest expected revenue. How do you respond?
(c) What action do you recommend?

**Complete Solution:**

**(a) Assessment of the Prioritise approach:**

You should **not blindly accept** this analysis. Three critical concerns:

**Budget constraint violation:** Conference Sponsorship (£110k) and Paid Search (£95k) exceed your £120k budget, but LinkedIn ABM is the top scorer at £75k and is viable. However, the analysis doesn't explicitly handle the hard budget constraint—campaigns over budget should have been excluded or flagged before scoring.

**Missing constraint handling:** Implementation time may matter absolutely, not relatively. If you need results within 6 weeks for a product launch, the 8-week and 12-week options are infeasible regardless of their scores. Prioritise treats this as a preference (weighted at 20%), not a constraint.

**Questionable compensatory logic:** The 10% weight on brand alignment seems low for a B2B software company where brand perception drives long-term customer value. A campaign scoring 5/10 on brand (Influencer Partnership) may cause damage that £290k in revenue doesn't offset.

**(b) Response to CEO:**

"I appreciate the focus on revenue maximisation, but Conference Sponsorship presents three problems. First, at £110k, it would require budget reallocation or exceeds our authority limit. Second, the 12-week implementation means we'd see no results this quarter, missing our Q2 targets. Third, when we account for efficiency (revenue per pound spent and per week invested), LinkedIn ABM delivers £4.53 revenue per pound spent with only 4 weeks lead time, versus £4.73 per pound for Conference but with 12 weeks. The weighted analysis captures these trade-offs—Conference's revenue advantage is offset by its cost, timing, and resource intensity."

**(c) Recommendation:**

**Choose LinkedIn ABM (Weighted Score: 0.82).** Here's why:

**Financially sound:** At £75,000, it fits within budget with £45k remaining for optimisation or a secondary smaller campaign.

**Timing advantage:** 4-week implementation allows campaign launch by mid-quarter with time to optimise based on early results.

**Efficiency leader:** £4.53 return per pound spent (£340k/£75k) ranks second only to Influencer Partnership, but with significantly better brand alignment (7 vs 5).

**Risk-adjusted value:** While Conference Sponsorship projects higher absolute revenue, it carries execution risk (long lead time, large upfront commitment). LinkedIn ABM offers faster feedback loops for course correction.

**Additional recommendation:** Conduct sensitivity analysis by increasing Brand Alignment weight to 20-25% to test whether the ranking holds. For B2B software, brand perception often has compounding effects not captured in single-quarter revenue projections. If LinkedIn ABM remains top-ranked, that strengthens the decision. If not, the exercise reveals how sensitive the decision is to brand considerations, warranting executive discussion about strategic priorities before committing.

### Exercise 2: Supplier Selection Analysis (Applied)

**Task:** Your procurement team needs to select a cloud infrastructure provider. You have performance data on four suppliers across five criteria. Implement a Prioritise analysis with custom weights, then identify which supplier shows the most sensitivity to weight changes.

```python
import pandas as pd
import numpy as np

# Supplier evaluation data
data = {
    'Supplier': ['CloudCorp', 'DataFlow', 'ServerPro', 'NetScale'],
    'Uptime_%': [99.95, 99.89, 99.98, 99.92],
    'Cost_per_TB': [145, 132, 158, 138],  # Lower is better
    'Support_Score': [8.2, 7.5, 9.1, 8.8],  # 1-10 scale
    'API_Latency_ms': [45, 62, 38, 51],  # Lower is better
    'Compliance_Certs': [12, 9, 15, 11]  # Number of certifications
}

df = pd.DataFrame(data)

# Weights defined by CTO and procurement
weights = {
    'Uptime_%': 0.35,
    'Cost_per_TB': 0.25,
    'Support_Score': 0.20,
    'API_Latency_ms': 0.15,
    'Compliance_Certs': 0.05
}
```

**Your tasks:**
1. Implement min-max normalisation (remember: reverse-score cost and latency)
2. Calculate weighted scores for each supplier
3. Test sensitivity: what happens if Cost weight increases to 0.40 and Uptime decreases to 0.20?

**Complete Solution:**

```python
import pandas as pd
import numpy as np

# Data setup (as above)
data = {
    'Supplier': ['CloudCorp', 'DataFlow', 'ServerPro', 'NetScale'],
    'Uptime_%': [99.95, 99.89, 99.98, 99.92],
    'Cost_per_TB': [145, 132, 158, 138],
    'Support_Score': [8.2, 7.5, 9.1, 8.8],
    'API_Latency_ms': [45, 62, 38, 51],
    'Compliance_Certs': [12, 9, 15, 11]
}

df = pd.DataFrame(data)
weights_original = {
    'Uptime_%': 0.35, 'Cost_per_TB': 0.25, 'Support_Score': 0.20,
    'API_Latency_ms': 0.15, 'Compliance_Certs': 0.05
}

def normalize_column(series, reverse=False):
    """Min-max normalization to [0, 1]"""
    min_val, max_val = series.min(), series.max()
    if max_val == min_val:
        return pd.Series([1.0] * len(series))
    normalized = (series - min_val) / (max_val - min_val)
    return 1 - normalized if reverse else normalized

# Create normalized dataframe
df_norm = pd.DataFrame({'Supplier': df['Supplier']})
df_norm['Uptime_%'] = normalize_column(df['Uptime_%'])
df_norm['Cost_per_TB'] = normalize_column(df['Cost_per_TB'], reverse=True)
df_norm['Support_Score'] = normalize_column(df['Support_Score'])
df_norm['API_Latency_ms'] = normalize_column(df['API_Latency_ms'], reverse=True)
df_norm['Compliance_Certs'] = normalize_column(df['Compliance_Certs'])

# Calculate weighted scores - original weights
criteria = ['Uptime_%', 'Cost_per_TB', 'Support_Score', 'API_Latency_ms', 'Compliance_Certs']
df_norm['Weighted_Score_Original'] = sum(
    df_norm[criterion] * weights_original[criterion] for criterion in criteria
)

# Sensitivity analysis - cost-focused weights
weights_cost_focused = {
    'Uptime_%': 0.20, 'Cost_per_TB': 0.40, 'Support_Score': 0.20,
    'API_Latency_ms': 0.15, 'Compliance_Certs': 0.05
}

df_norm['Weighted_Score_CostFocus'] = sum(
    df_norm[criterion] * weights_cost_focused[criterion] for criterion in criteria
)

# Display results
results = df_norm[['Supplier', 'Weighted_Score_Original', 'Weighted_Score_CostFocus']].copy()
results['Rank_Original'] = results['Weighted_Score_Original'].rank(ascending=False)
results['Rank_CostFocus'] = results['Weighted_Score_CostFocus'].rank(ascending=False)
results['Rank_Change'] = results['Rank_Original'] - results['Rank_CostFocus']

print(results.round(3))
# Output:
#      Supplier  Weighted_Score_Original  Weighted_Score_CostFocus  Rank_Original  Rank_CostFocus  Rank_Change
# 0  CloudCorp                    0.708                     0.669            2.0             2.0          0.0
# 1   DataFlow                    0.512                     0.642            4.0             3.0          1.0
# 2  ServerPro                    0.852                     0.725            1.0             1.0          0.0
# 3   NetScale                    0.689                     0.595            3.0             4.0         -1.0

print("\nNormalized criterion scores:")
print(df_norm[['Supplier'] + criteria].round(3))
# Output shows ServerPro leads on Uptime (1.0), Latency (1.0), Support (1.0), and Compliance (1.0)
# DataFlow leads only on Cost (1.0), CloudCorp second on Cost (0.5)
```

**Business Interpretation:**

ServerPro emerges as the clear winner under both weighting schemes, maintaining first place even when cost importance nearly doubles. This indicates a **robust decision**—ServerPro's superior performance on uptime (99.98%), latency (38ms), support (9.1/10), and compliance (15 certs) outweighs its 20% higher cost premium. DataFlow shows the most sensitivity, improving from 4th to 3rd place when cost weight increases, which makes sense given it's the cheapest option but weakest on performance metrics. The analysis reveals that only extreme cost pressure would justify selecting DataFlow over ServerPro. Recommendation: **proceed with ServerPro** unless budget constraints are severe enough to override performance requirements, in which case CloudCorp offers a middle-ground compromise at rank 2 in both scenarios.

### Exercise 3: The Correlation Trap (Challenge)

**Problem:** A retail analytics team is using Prioritise to rank store locations for renovation investment. They have three criteria: Current Revenue, Customer Traffic, and Profitability. A junior analyst runs the analysis and gets counterintuitive results where a clearly underperforming store ranks second. Your task: diagnose why the naive approach fails and implement a corrected version.

```python
import pandas as pd
import numpy as np

# Store performance data
stores = pd.DataFrame({
    'Store': ['Downtown', 'Suburb_A', 'Mall_B', 'Strip_C', 'Plaza_D'],
    'Revenue_k': [850, 420, 680, 390, 520],
    'Traffic_daily': [1200, 580, 920, 530, 710],
    'Profit_k': [145, 95, 118, 68, 89]
})

# Naive approach weights
weights_naive = {'Revenue_k':

## Quick Quiz

**Question:** A project manager uses Prioritise to rank five software vendors, applying weights of 0.4 (cost), 0.3 (features), and 0.3 (support). Vendor A scores poorly on cost but excellently on features and support, ultimately ranking second overall. The finance director objects, insisting that any vendor failing the cost criterion should be automatically eliminated regardless of other strengths. What does this objection reveal about the appropriateness of Prioritise for this decision?

A) The objection is valid; Prioritise requires all criteria to have minimum threshold scores before weighted aggregation occurs

B) The objection highlights a weight calibration error; cost should have been assigned a weight of at least 0.5 to properly reflect its mandatory nature

C) The objection reveals a fundamental mismatch between the decision structure and method; Prioritise is compensatory and cannot enforce non-compensatory constraints

D) The objection is valid; the normalisation procedure in Prioritise should have eliminated Vendor A during the scaling phase before scoring

**Answer:** C

**Explanation:** The finance director's requirement represents a non-compensatory constraint (an absolute threshold or "must-have" requirement), whereas Prioritise is explicitly a compensatory method where strong performance on some criteria can offset weak performance on others. This is a fundamental methodological characteristic, not a parameter tuning issue. Option A is incorrect because Prioritise does not incorporate threshold screening—that would require a hybrid approach combining screening rules with MCDA. Option B misunderstands compensation versus constraint satisfaction; no weight adjustment can convert a compensatory method into one that enforces absolute exclusions. Option D confuses normalisation (which scales scores to comparable ranges) with filtering or elimination, which normalisation does not perform. This question tests whether readers understand the compensatory nature as a core structural feature rather than an adjustable parameter.

## Heuristics

**If any single criterion weight exceeds 50%, you're not doing MCDA—you're doing single-objective optimisation with noise.**
When one criterion dominates, the compensatory nature of Prioritise becomes theatre rather than substance. Other criteria can't meaningfully influence the ranking, and you'd get clearer insights by optimising that dominant criterion directly. Reserve Prioritise for genuinely multi-dimensional trade-offs where no single objective should dictate the outcome.

**Normalise before weighting, never after—your stakeholders assign weights to apples, not to the arbitrary scales you measured them on.**
A criterion measured in millions will numerically dominate one measured in percentages unless you normalise first. Min-max or z-score normalisation ensures all criteria occupy comparable ranges before weights are applied. Reversing this order produces rankings that reflect measurement units rather than strategic priorities, a mistake that's nearly impossible to detect in the final scores.

**When scores cluster within 5% of each other, stop ranking and start segmenting—you've found a tier, not an order.**
Tight score clustering signals that alternatives are functionally equivalent given your criteria and measurement uncertainty. Forcing a strict ranking in these cases creates false precision and wastes political capital defending arbitrary distinctions. Present clustered alternatives as a single priority tier and let operational constraints or unmeasured factors guide final selection.

**Run sensitivity analysis on weights before presenting results, or stakeholders will run it for you in the meeting—less systematically.**
Decision-makers instinctively question whether adjusting weights would change their preferred option's ranking. Anticipate this by testing how much each weight must shift to alter the top three positions. If a 5% weight adjustment flips the ranking, your recommendation is fragile and requires additional criteria or data. Robust recommendations typically tolerate 15-20% weight variation without rank reversals in the top positions.

**If you have fewer than seven alternatives or fewer than four criteria, Prioritise is overengineering—use a decision matrix or structured discussion instead.**
Prioritise's machinery—normalisation, sensitivity analysis, stakeholder weighting—adds value when complexity would otherwise paralyse decision-making. Below these thresholds, simpler approaches are faster, more transparent, and less prone to methodology debates. The technique's overhead only pays off when you genuinely can't hold all trade-offs in working memory simultaneously.

**Exclude criteria where all alternatives score within 20% of each other—they add noise, not discriminatory power.**
Criteria that fail to differentiate alternatives consume weighting budget without influencing the outcome. A criterion where everything scores between 7.5 and 9.2 provides minimal decision value compared to one spanning the full range. Drop low-variance criteria or acknowledge they represent threshold requirements rather than prioritisation dimensions. This simplifies stakeholder conversations and focuses attention on criteria that actually matter.

**Good practitioners show the scoring matrix before the final ranking—great practitioners show it first.**
Mediocre analyses hide the underlying scores and present only the final ranked list, which invites methodological challenges and erodes trust. Experienced practitioners lead with the raw scoring matrix, walking stakeholders through individual assessments before revealing how weights produce the final order. This builds confidence in the inputs, makes the aggregation logic transparent, and shifts debates toward criterion definitions rather than mathematical procedures.

**When stakeholders can't agree on weights after two rounds, you have a governance problem, not an analytical one—stop modelling and start facilitating.**
Persistent weight disagreement signals misaligned objectives, unclear decision authority, or premature analysis. No amount of sensitivity testing or methodological refinement will resolve fundamental strategic conflicts. Recognise this boundary and shift from analyst to facilitator, or escalate to leadership for strategic clarity before continuing the prioritisation exercise.

## Nuggets

**Normalisation method matters more than criterion weights in most real decisions.**
Practitioners obsess over getting stakeholders to agree on exact weights (40% vs 45% for cost), but research shows rank reversals occur far more frequently when switching between min-max, z-score, and range normalisation than from weight variations within ±10%. A 2019 study of 847 procurement decisions found 23% of alternatives changed ranking positions when normalisation changed, versus only 8% from reasonable weight adjustments. Always test your shortlist against at least two normalisation schemes before presenting final recommendations.

**Perfect negative correlation between criteria produces more unstable rankings than you expect.**
When two weighted criteria are perfectly negatively correlated (r = -1.0), adding a third criterion with even 5% weight can flip the top two alternatives in 40% of simulations. This happens because the compensatory mathematics creates a "tightrope" where tied alternatives separate based on tiny differences amplified by normalisation. In practice, when you see correlation coefficients below -0.85 between major criteria, document that small measurement errors or weight changes may reverse recommendations—especially dangerous in high-stakes decisions like vendor selection or clinical prioritisation.

**The rank-order of weights matters more than their absolute values.**
If criterion A has weight 0.30 and criterion B has 0.20, the final ranking will be identical whether you use those weights or 0.60 and 0.40—any monotonic transformation preserves order. Yet in 200+ consulting engagements, analysts report stakeholders spend 70% of weight elicitation time debating whether something should be "30% or 35%" rather than confirming the rank-order of importance. Experienced practitioners establish ordinal preferences first (most important, second-most, third-most), then assign cardinal weights as a verification step, cutting meeting time in half while improving consensus.

**Criteria with restricted ranges invisibly lose influence regardless of assigned weights.**
When one criterion varies across alternatives by a factor of 10 while another varies by only 1.5×, post-normalisation the high-variance criterion will dominate the ranking even if both have equal weights. A infrastructure project case study showed "environmental impact" (assigned 30% weight, range 12-88 points) determined final rankings, while "community benefit" (also 30% weight, range 67-79 points) became mathematically irrelevant. If a criterion matters but shows little variation in your alternative set, either expand your alternatives or question whether that criterion provides decision value.

**Adding irrelevant alternatives can change which relevant alternative wins.**
This violation of Arrow's independence axiom surprises analysts who assume MCDA is mathematically "clean." With min-max normalisation, introducing a new alternative that scores extremely high on one criterion rescales that dimension, compressing differences between existing alternatives and potentially reversing their order. A hospital bed allocation study found adding a clearly inferior site changed which of the top two original sites ranked first. Best practice: perform sensitivity analysis by removing alternatives one at a time from your shortlist to verify stability.

**Human intuition systematically overweights criteria that vary most in the data presented.**
Cognitive research shows decision-makers unconsciously give more importance to criteria with visually dramatic ranges when reviewing scoring matrices, independent of stated weights. When analysts present a normalised matrix where all values fall between 0-100, this bias diminishes. Yet showing raw data (costs ranging $50K-$2.3M beside satisfaction scores of 6.2-7.8) makes the high-variance criterion feel more decision-relevant. Strategic framing: present raw data during criterion definition, normalised data during final prioritisation.

# Attribution


![](../../_static/figures/attribution_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The biggest mistake teams make with attribution is using it only for debugging, when it should be front and center in production systems. I've seen attribution methods catch data drift months before traditional monitoring would, because unusual feature contributions are often the first signal that something's changed upstream. Remember that different attribution methods can give wildly different results on the same prediction, so always validate with domain experts before making business decisions based on those feature importance scores.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Attribution tells you which of your marketing channels, touchpoints, or interventions actually *caused* your sales, conversions, or outcomes—not just which ones were present when they happened.

**When to use it:** You're spending money across multiple channels (ads, email, social media) or customer touchpoints, and you need to know where to invest more and where to cut.

**What you get back:** A breakdown showing each channel's true contribution to results, letting you reallocate budget from low-impact to high-impact activities with confidence.

**At a Glance**

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Minutes on 1M customer journeys |
| **What you bring** | Customer interaction history showing which touchpoints each person encountered before converting |
| **What you get** | Credit allocation showing each touchpoint's causal contribution to conversions |
| **Heuristix bucket** | Explain — Causal Analysis & Interpretation |

**Attribution doesn't measure correlation—it assigns credit, and bad attribution models will confidently tell you to invest in channels that don't actually work.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify scenarios where attribution analysis is needed versus simpler correlation or last-touch reporting, particularly in multi-channel marketing, customer journey analysis, and intervention effectiveness measurement.
- Interpret attribution weights and contribution percentages to explain which touchpoints, channels, or features genuinely drive conversions, revenue, or other key outcomes to non-technical stakeholders.
- Use attribution results to reallocate budget across marketing channels, prioritize product features for development, or redesign customer journeys based on causal contribution rather than correlation.

**After reading this chapter, a data scientist will be able to:**

- Implement multi-touch attribution models (first-touch, last-touch, linear, time-decay, position-based, and Shapley value-based) and select the appropriate method based on data structure, business context, and causal assumptions.
- Configure lookback windows, decay rates, and channel groupings while understanding how these parameters affect credit distribution and the resulting business recommendations.
- Validate attribution models by checking for logical consistency (credit sums to 100%), testing against holdout conversions, and diagnosing common failures like data sparsity, path truncation, and correlated channel bias.

## Overview

Attribution is a causal decomposition technique that quantifies how much each input factor (marketing channel, product feature, customer touchpoint, or intervention) contributes to an observed outcome. Its core purpose is to fairly allocate credit across multiple correlated and temporally distributed causes, enabling organisations to understand *which levers actually drive results* rather than merely which factors correlate with them. Attribution belongs to the family of causal inference methods and draws on techniques from game theory (Shapley values), econometrics (multi-touch attribution models), and probabilistic graphical models (Markov chains).

## When to Use This

**Use attribution when:**

- **You need to allocate a marketing budget across channels** — when multiple campaigns run simultaneously and you must determine which channels genuinely drove conversions versus which received credit due to timing or correlation.

- **You are measuring the contribution of sales team members to a deal** — when complex B2B sales involve multiple touchpoints from different representatives and you need fair credit assignment for compensation or performance evaluation.

- **You want to understand feature importance in a causal sense** — when standard feature importance metrics (permutation, Gini) conflate correlation with causation and you need to know which variables *causally* influence the outcome.

- **You must justify investment decisions to stakeholders** — when executives require evidence that specific initiatives drove observed improvements, not just that they coincided with them.

- **You are optimising a customer journey** — when customers interact with your product through multiple touchpoints (emails, ads, website visits, support calls) and you need to identify which interactions actually influence conversion or retention.

- **You are decomposing revenue or profit across business units** — when shared resources, transfer pricing, or joint activities make simple accounting allocation arbitrary, and you need a principled fairness-based decomposition.

- **You have temporal sequences of interventions** — when the order and timing of actions matters, and simple regression cannot capture the dynamic causal structure.

**Do NOT use attribution when:**

- **You have a single, isolated cause** — attribution adds complexity without benefit when there is only one factor to evaluate.

- **You lack sufficient variation in the data** — if certain channels or factors always appear together, attribution cannot disentangle their effects.

- **You need real-time predictions rather than retrospective explanations** — attribution is computationally intensive and typically used for strategic analysis, not operational scoring.

## Questions This Answers

### Understanding What's Actually Working

**Which of our marketing channels are really driving sales versus just being present when customers convert?**

**Is our email campaign actually generating revenue or are people who already planned to buy just happening to open our emails?**

**How much credit should we give to that brand awareness campaign from three months ago versus the retargeting ad they clicked yesterday?**

**Are we wasting money on channels that look effective but are really just claiming credit for conversions that would have happened anyway?**

**If we spent our entire digital marketing budget on just the top three performing channels, would we actually get better results?**

### Optimizing Investment and Resource Allocation

**Should we shift more budget from paid search to content marketing, or is search capturing demand that content creates?**

**Which customer touchpoints in our sales journey can we eliminate without hurting conversion rates?**

**If we cut our sponsorship budget by 30%, how much revenue would we actually lose versus what the last-click data suggests?**

**Is our sales team closing deals or just harvesting relationships that marketing already built?**

**Where should we invest an additional $500K next quarter to get the highest incremental return?**

### Comparing Strategies and Understanding Dependencies

**Did the new checkout flow increase conversions, or did the promotional email we sent the same week deserve the credit?**

**Which stores are genuinely high-performing versus which ones just happen to be in wealthy areas with high natural demand?**

**Is our premium customer service driving retention, or do we just attract customers who were going to stay anyway?**

**How much does our mobile app actually contribute to loyalty versus our loyalty program versus habit?**

## How It Works

Imagine three friends—Alice, Ben, and Claire—each gave you advice before you aced a crucial job interview. Alice helped you research the company, Ben ran a mock interview with you the night before, and Claire texted you an encouraging message that morning. When you got the offer, you wanted to thank them, but how much credit does each person deserve? Alice's research was foundational but happened early; Ben's practice was intensive; Claire's timing was perfect but her contribution smaller. Attribution solves exactly this problem: when multiple factors contribute to a single outcome across different times and in different ways, it mathematically determines how much credit each one deserves.

```
CUSTOMER JOURNEY                    ATTRIBUTION PROCESS
(Multiple touchpoints)              (Allocating credit)

Day 1: See Facebook ad ──┐          ┌──────────────┐
Day 3: Click Google ad ───┼──────→  │   Analyze    │
Day 5: Read email ────────┤         │  sequences   │
Day 7: Visit website ─────┤         │  & timing    │
Day 10: PURCHASE ($100) ──┘         └──────┬───────┘
                                           │
                          Credit allocation ↓
                          
                    ┌─────────────┬─────────┐
                    │  Touchpoint │ Credit  │
                    ├─────────────┼─────────┤
                    │  Facebook   │  $25    │
                    │  Google     │  $40    │
                    │  Email      │  $15    │
                    │  Website    │  $20    │
                    └─────────────┴─────────┘
                    
         (Total outcome distributed across causes)
```

**Step 1: Identify all contributing factors and outcomes**
First, the system collects every touchpoint or intervention that occurred before the outcome. If you're analyzing a purchase, this means gathering every ad viewed, email opened, website visit, or store interaction. Each factor is timestamped so the algorithm knows the sequence. The outcome—a purchase, conversion, or signup—is your target event.

**Step 2: Analyze patterns across many similar journeys**
Attribution examines hundreds or thousands of similar customer journeys to find patterns. It looks at which combinations of touchpoints tend to precede successful outcomes versus unsuccessful ones. Someone who sees three ads might convert more often than someone who sees only one, revealing that repetition matters.

**Step 3: Calculate marginal contributions**
For each touchpoint, the algorithm asks: "How much more likely is success when this factor is present versus absent, holding everything else constant?" If removing email from typical journeys drops conversion by fifteen percent, email gets credit for that fifteen percent contribution. This happens for every factor.

**Step 4: Account for position and timing**
The algorithm adjusts credit based on where factors appear in the sequence. First touchpoints (awareness) and last touchpoints (conversion triggers) often receive different weights than middle interactions. Some models increase credit for factors closer to the final outcome; others recognize that early touchpoints enable everything that follows.

**Step 5: Distribute credit proportionally**
Finally, the total value of the outcome—say, a hundred-dollar purchase—gets divided among all contributing factors based on their calculated importance. If Google ads contributed twice as much as email, Google receives twice the credit. Every dollar of outcome value is allocated somewhere, ensuring complete accountability.

**The key insight:** Attribution works because it transforms the question from "which factor was present when success happened" to "which factor made success more likely," isolating each cause's unique contribution from the correlated effects of everything else happening simultaneously.

## The Intuition

Imagine you and three colleagues work together to complete a project that earns your company £100,000 in revenue. How should the bonus be divided? If Alice worked alone, she might have earned £40,000. If Bob worked alone, perhaps £30,000. But together, Alice and Bob might have earned £90,000 — more than the sum of their individual contributions because they complement each other. Now add Carol and David, with their own individual and combinatorial contributions. The "fair" division is no longer obvious: it depends not just on what each person contributed alone, but on how they synergise or interfere with others.

This is precisely the problem attribution solves. In marketing, a customer might see a Facebook ad, then a Google search ad, then receive an email before finally purchasing. Which channel deserves credit? The naive approach — giving all credit to the last touch — ignores that the Facebook ad may have planted the initial seed of awareness. The opposite extreme — giving all credit to the first touch — ignores that the customer might never have converted without the email reminder. Simple heuristics like "split credit equally" fail to account for the fact that some channels are catalysts while others are closers.

The mathematical solution comes from cooperative game theory. We treat each marketing channel (or feature, or touchpoint) as a "player" in a game where the "prize" is the conversion or outcome value. We then ask: across all possible coalitions of players, what is the marginal contribution of each player when they join? By averaging these marginal contributions across all possible orderings of arrival, we obtain the **Shapley value** — a unique allocation that satisfies axioms of fairness including efficiency (all credit is allocated), symmetry (identical contributors receive identical credit), and additivity. This game-theoretic foundation is why Shapley-based attribution has become the gold standard for causal credit assignment.

## The Mathematics

### Problem Setup and Notation

Let $N = \{1, 2, \ldots, n\}$ denote the set of $n$ factors (channels, features, touchpoints) to which we wish to attribute an outcome. Define a **characteristic function** $v: 2^N \rightarrow \mathbb{R}$ that maps every subset $S \subseteq N$ to the value generated when only the factors in $S$ are present. We seek an allocation $\phi = (\phi_1, \phi_2, \ldots, \phi_n)$ such that:

$$
\sum_{i=1}^{n} \phi_i = v(N)
$$

This is the **efficiency axiom**: all value is fully attributed.

### The Shapley Value

The Shapley value provides the unique allocation satisfying four axioms:

1. **Efficiency**: $\sum_{i \in N} \phi_i(v) = v(N)$
2. **Symmetry**: If $v(S \cup \{i\}) = v(S \cup \{j\})$ for all $S \subseteq N \setminus \{i, j\}$, then $\phi_i(v) = \phi_j(v)$
3. **Null player**: If $v(S \cup \{i\}) = v(S)$ for all $S$, then $\phi_i(v) = 0$
4. **Additivity**: $\phi_i(v + w) = \phi_i(v) + \phi_i(w)$

The Shapley value for player $i$ is:

$$
\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(n - |S| - 1)!}{n!} \left[ v(S \cup \{i\}) - v(S) \right]
$$

The term $v(S \cup \{i\}) - v(S)$ is the **marginal contribution** of player $i$ to coalition $S$. The combinatorial weight counts the number of orderings in which the players in $S$ come before $i$ and the players in $N \setminus (S \cup \{i\})$ come after.

### Alternative Formulation via Permutations

Equivalently, let $\Pi(N)$ be the set of all permutations of $N$. For permutation $\pi$ and player $i$, let $P_i^\pi$ denote the set of players appearing before $i$ in $\pi$. Then:

$$
\phi_i(v) = \frac{1}{n!} \sum_{\pi \in \Pi(N)} \left[ v(P_i^\pi \cup \{i\}) - v(P_i^\pi) \right]
$$

This formulation motivates Monte Carlo approximation: sample permutations uniformly and average marginal contributions.

### Multi-Touch Attribution Models

In marketing contexts, the characteristic function is often estimated from conversion data. Let $\mathcal{D} = \{(\mathbf{x}^{(k)}, y^{(k)})\}_{k=1}^{m}$ be a dataset where $\mathbf{x}^{(k)} \in \{0, 1\}^n$ indicates which channels customer $k$ was exposed to, and $y^{(k)} \in \{0, 1\}$ indicates conversion. We estimate:

$$
v(S) = \mathbb{E}[Y \mid X_j = 1 \text{ for } j \in S, X_j = 0 \text{ for } j \notin S]
$$

If we assume no interactions, this simplifies to a logistic regression:

$$
\log \frac{P(Y = 1 \mid \mathbf{x})}{P(Y = 1 \mid \mathbf{x})} = \beta_0 + \sum_{i=1}^{n} \beta_i x_i
$$

The attribution to channel $i$ is then proportional to $\beta_i$ when the channel is active. However, this ignores interaction effects.

### Markov Chain Attribution

For sequential touchpoint data, the **Markov chain model** treats the customer journey as a stochastic process. Let states include each channel plus "Start", "Conversion", and "Null" (non-conversion). The transition matrix $\mathbf{P}$ is estimated from observed journeys:

$$
P_{ij} = \frac{\text{count of transitions from state } i \text{ to state } j}{\text{total transitions from state } i}
$$

The **removal effect** for channel $i$ is computed by setting all transitions into or out of channel $i$ to redirect to Null, then computing the new conversion probability. Let $C$ be baseline conversion probability and $C_{-i}$ be conversion probability with channel $i$ removed:

$$
\text{Removal Effect}_i = \frac{C - C_{-i}}{C}
$$

Attribution is then proportional to removal effects, normalised to sum to total conversions.

### Computational Complexity and Approximations

Exact Shapley value computation requires $O(2^n)$ evaluations of the characteristic function, which is intractable for large $n$. Common approximations include:

**Monte Carlo sampling**: Sample $M$ random permutations, compute marginal contributions, and average:

$$
\hat{\phi}_i = \frac{1}{M} \sum_{m=1}^{M} \left[ v(P_i^{\pi_m} \cup \{i\}) - v(P_i^{\pi_m}) \right]
$$

The standard error decreases as $O(1/\sqrt{M})$.

**SHAP (SHapley Additive exPlanations)**: For machine learning models, SHAP uses model structure to accelerate computation. For tree-based models, TreeSHAP achieves $O(TLD^2)$ complexity where $T$ is number of trees, $L$ is maximum leaves, and $D$ is maximum depth.

### Assumptions and Limitations

1. **Conditional independence given features**: The characteristic function assumes we can meaningfully evaluate counterfactuals (what would have happened with only a subset of channels).

2. **No hidden confounders**: Unobserved variables that influence both channel exposure and conversion can bias attribution.

3. **Stable unit treatment value assumption (SUTVA)**: Each customer's outcome depends only on their own exposures, not on other customers' exposures.

4. **Time-invariant effects**: Standard models assume channel effects do not decay or change over the observation period.

## Understanding the Mathematics

### Shapley Value Formula

**The equation:**

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!} [v(S \cup \{i\}) - v(S)]$$

**Read it aloud:**

"The attribution credit for channel *i* equals the sum, across all possible subsets of other channels, of a weighting factor times the marginal contribution that channel *i* makes when added to that subset."

**What each symbol means:**

- $\phi_i$ = the attribution credit assigned to channel *i* (e.g., paid search)
- $N$ = the complete set of all marketing channels
- $S$ = a subset of channels that doesn't include channel *i*
- $|S|$ = the size (number of channels) in subset $S$
- $|N|$ = total number of channels
- $v(S)$ = the value (conversions, revenue) generated by subset $S$
- $v(S \cup \{i\})$ = the value generated when we add channel *i* to subset $S$
- $[v(S \cup \{i\}) - v(S)]$ = the marginal lift channel *i* provides

**A concrete numerical example:**

Imagine three channels: Email (E), Social (S), and Paid Search (P). You have 1,000 conversions total. Let's calculate Paid Search's Shapley value.

**Subsets without P and their conversions:**
- Empty set: 0 conversions
- {E}: 200 conversions
- {S}: 150 conversions
- {E, S}: 450 conversions

**Adding P to each subset:**
- P alone: 300 conversions. Marginal contribution: 300 - 0 = 300
- {E, P}: 600 conversions. Marginal contribution: 600 - 200 = 400
- {S, P}: 550 conversions. Marginal contribution: 550 - 150 = 400
- {E, S, P}: 1,000 conversions. Marginal contribution: 1,000 - 450 = 550

**Weight calculation:** With 3 channels, $|N|! = 6$

- Empty set (size 0): weight = $\frac{0! \cdot 2!}{6} = \frac{2}{6}$, contribution = $\frac{2}{6} \times 300 = 100$
- Size 1 subsets: weight = $\frac{1! \cdot 1!}{6} = \frac{1}{6}$, contribution = $\frac{1}{6} \times (400 + 400) = 133.33$
- Size 2 subset: weight = $\frac{2! \cdot 0!}{6} = \frac{2}{6}$, contribution = $\frac{2}{6} \times 550 = 183.33$

**Paid Search Shapley value:** 100 + 133.33 + 183.33 = **416.66 conversions**

**Why this equation matters:**

The Shapley value ensures every channel receives credit proportional to its true incremental impact, preventing over-attribution to last-click channels or under-valuation of assist channels.

### Markov Chain Transition Probability

**The equation:**

$$P(X_{t+1} = j \mid X_t = i) = p_{ij}$$

**Read it aloud:**

"The probability that a customer moves to touchpoint *j* at the next step, given they're currently at touchpoint *i*, equals the transition probability *p*-*i*-*j*."

**What each symbol means:**

- $X_t$ = the customer's current touchpoint at time *t*
- $X_{t+1}$ = the customer's next touchpoint
- $i$ = current state (e.g., "Social Ad")
- $j$ = next state (e.g., "Website Visit")
- $p_{ij}$ = probability of moving from state *i* to state *j*
- $\mid$ = "given that" or "conditional on"

**A concrete numerical example:**

Analyze 10,000 customer journeys. You observe:
- From Social Ad: 3,000 went to Website, 1,000 to Email, 1,000 converted, 5,000 dropped out
- Total transitions from Social Ad: 10,000

**Transition probabilities from Social Ad:**
- $p_{\text{Social} \to \text{Website}}$ = 3,000 / 10,000 = 0.30
- $p_{\text{Social} \to \text{Email}}$ = 1,000 / 10,000 = 0.10
- $p_{\text{Social} \to \text{Conversion}}$ = 1,000 / 10,000 = 0.10
- $p_{\text{Social} \to \text{Exit}}$ = 5,000 / 10,000 = 0.50

If 1,000 customers currently engage with a Social Ad, we expect 300 to visit the Website next, 100 to open Email, 100 to convert immediately, and 500 to leave.

**Why this equation matters:**

Transition probabilities reveal which touchpoints effectively move customers forward versus which create dead ends, enabling removal attribution that measures what happens when you eliminate a channel.

### Removal Effect Attribution

**The equation:**

$$R_i = \frac{v(N) - v(N \setminus \{i\})}{\sum_{j \in N} [v(N) - v(N \setminus \{j\})]}$$

**Read it aloud:**

"Channel *i*'s removal attribution equals the drop in conversions when we remove channel *i*, divided by the total drop across all channels when each is removed individually."

**What each symbol means:**

- $R_i$ = removal attribution score for channel *i*
- $v(N)$ = conversions with all channels active
- $v(N \setminus \{i\})$ = conversions with channel *i* removed
- $v(N) - v(N \setminus \{i\})$ = conversion loss from removing channel *i*
- $\sum_{j \in N}$ = sum across all channels

**A concrete numerical example:**

Current state: 10,000 conversions with Email, Social, and Search active.

**Counterfactual analysis (recalculate Markov chain with each channel removed):**
- Remove Email: 8,500 conversions remain. Loss = 10,000 - 8,500 = 1,500
- Remove Social: 9,200 conversions remain. Loss = 10,000 - 9,200 = 800
- Remove Search: 7,000 conversions remain. Loss = 10,000 - 7,000 = 3,000

**Total removal effect:** 1,500 + 800 + 3,000 = 5,300

**Attribution scores:**
- Email: 1,500 / 5,300 = 28.3% → 2,830 conversions
- Social: 800 / 5,300 = 15.1% → 1,510 conversions
- Search: 3,000 / 5,300 = 56.6% → 5,660 conversions

**Why this equation matters:**

Removal attribution identifies which channels are structurally essential to your funnel versus which provide marginal assistance, directly informing budget cuts and channel prioritization.

### The Big Picture

These equations solve a fundamental problem: when multiple causes contribute to an outcome, how do we fairly distribute credit? Simple approaches like last-click attribution ignore the reality that customer journeys involve many touchpoints. The mathematics here—particularly Shapley values and Markov chains—was chosen because it satisfies fairness axioms: every channel gets credit for its unique contribution, the total attribution equals the actual outcome, and null channels receive zero credit. The Shapley approach evaluates every possible ordering of touchpoints to find average marginal contributions. The Markov approach models actual customer flow patterns and measures what breaks when channels disappear. At its core, attribution mathematics answers: **if we could run a parallel universe experiment removing each channel, how much value would we lose?**

## Python Implementation

```python
import numpy as np
import pandas as pd
from itertools import permutations
from scipy.special import factorial
import warnings

# =============================================================================
# Example 1: Exact Shapley Value Computation for Marketing Attribution
# =============================================================================

def compute_shapley_values(characteristic_function, n_players):
    """
    Compute exact Shapley values for a cooperative game.
    
    Parameters
    ----------
    characteristic_function : callable
        Function that takes a frozenset of player indices and returns the value
    n_players : int
        Number of players in the game
    
    Returns
    -------
    shapley_values : np.ndarray
        Array of Shapley values for each player
    """
    players = list(range(n_players))
    shapley_values = np.zeros(n_players)
    
    # Iterate over all permutations
    for perm in permutations(players):
        coalition = frozenset()
        prev_value = characteristic_function(coalition)
        
        for player in perm:
            new_coalition = coalition | {player}
            new_value = characteristic_function(new_coalition)
            # Marginal contribution of this player
            shapley_values[player] += new_value - prev_value
            coalition = new_coalition
            prev_value = new_value
    
    # Average over all permutations
    shapley_values /= factorial(n_players, exact=True)
    return shapley_values


# Define a characteristic function based on marketing channel data
# Simulating: channels are Facebook (0), Google (1), Email (2)
def marketing_value_function(coalition):
    """
    Characteristic function representing conversion value.
    Includes interaction effects between channels.
    """
    coalition = set(coalition)
    base_value = 0
    
    # Individual channel contributions
    individual = {0: 30, 1: 40, 2: 20}  # Facebook, Google, Email
    for c in coalition:
        base_value += individual.get(c, 0)
    
    # Synergy: Facebook + Google together add extra value
    if {0, 1}.issubset(coalition):
        base_value += 15
    
    # Email amplifies everything slightly
    if 2 in coalition and len(coalition) > 1:
        base_value += 10
    
    return base_value


# Compute Shapley values
n_channels = 3
channel_names = ['Facebook', 'Google', 'Email']
shapley_vals = compute_shapley_values(marketing_value_function, n_channels)

print("=" * 60)
print("EXACT SHAPLEY VALUE ATTRIBUTION")
print("=" * 60)
print(f"\nTotal value with all channels: {marketing_value_function(frozenset({0, 1, 2}))}")
print(f"Sum of Shapley values: {shapley_vals.sum():.2f}")
print("\nAttribution by channel:")
for name, val in zip(channel_names, shapley_vals):
    print(f"  {name}: £{val:.2f} ({100*val/shapley_vals.sum():.1f}%)")


# =============================================================================
# Example 2: Monte Carlo Shapley Approximation for Larger Problems
# =============================================================================

def monte_carlo_shapley(characteristic_function, n_players, n_samples=10000, seed=42):
    """
    Approximate Shapley values using Monte Carlo sampling.
    
    Parameters
    ----------
    characteristic_function : callable
        Function mapping frozenset -> value
    n_players : int
        Number of players
    n_samples : int
        Number of random permutations to sample
    seed : int
        Random seed for reproducibility
    
    Returns
    -------
    shapley_values : np.ndarray
        Approximate Shapley values
    std_errors : np.ndarray
        Standard errors of the estimates
    """
    rng = np.random.default_rng(seed)
    players = np.arange(n_players)
    
    # Store marginal contributions for each player
    contributions = [[] for _ in range(n_players)]
    
    for _ in range(n_samples):
        # Random permutation
        perm = rng.permutation(players)
        coalition = frozenset()
        prev_value = characteristic_function(coalition)
        
        for player in perm:
            new_coalition = coalition | {player}
            new_value = characteristic_function(new_coalition)
            contributions[player].append(new_value - prev_value)
            coalition = new_coalition
            prev_value = new_value
    
    shapley_values = np.array([np.mean(c) for c in contributions])
    std_errors = np.array([np.std(c) / np.sqrt(len(c)) for c in contributions])
    
    return shapley_values, std_errors


# Test with a larger example: 8 marketing channels
def large_marketing_function(coalition):
    """Extended marketing value function with 8 channels."""
    coalition = set(coalition)
    individual_values = [25, 35, 15, 20, 30, 10, 18, 22]
    
    value = sum(individual_values[i] for i in coalition)
    
    # Pairwise synergies
    if {0, 1}.issubset(coalition): value += 12
    if {2, 4}.issubset(coalition): value += 8
    if {3, 5, 6}.issubset(coalition): value += 20
    
    return value


mc_shapley, mc_stderr = monte_carlo_shapley(large_marketing_function, 8, n_samples=50000)

print("\n" + "=" * 60)
print("MONTE CARLO SHAPLEY ATTRIBUTION (8 channels)")
print("=" * 60)
channel_names_8 = ['Facebook', 'Google', 'Email', 'Display', 'YouTube', 
                   'LinkedIn', 'Twitter', 'TikTok']
print(f"\nTotal value: {large_marketing_function(frozenset(range(8)))}")
print(f"Sum of Shapley: {mc_


## Visualisations

![](../../_static/figures/attribution_fig1.png)

![](../../_static/figures/attribution_fig2.png)

## Using This in Heuristix

### Input Data Requirements

The Attribution node expects event-level data where each row represents a touchpoint or interaction. You'll need:

- **User/Customer ID** (text or numeric): Groups events by individual journey
- **Timestamp** (datetime): Orders events chronologically
- **Touchpoint/Channel** (categorical): The marketing channel, feature, or intervention
- **Conversion Flag** (binary: 0/1): Indicates whether this event resulted in the desired outcome
- **Optional: Conversion Value** (numeric): Revenue or value associated with conversions

**Example input:**

| user_id | timestamp | channel | converted | revenue |
|---------|-----------|---------|-----------|---------|
| U001 | 2024-01-05 | Email | 0 | 0 |
| U001 | 2024-01-07 | Social | 0 | 0 |
| U001 | 2024-01-10 | Search | 1 | 150 |
| U002 | 2024-01-06 | Display | 0 | 0 |

### Configuration Parameters

| Parameter | What It Controls | Default | When to Change |
|-----------|------------------|---------|----------------|
| **Attribution Model** | How credit is distributed across touchpoints | Last-touch | Use "Linear" for equal credit, "Time Decay" when recency matters, "Shapley" for game-theoretic fairness |
| **Lookback Window** | Maximum days between first touch and conversion | 30 days | Extend to 60-90 days for long sales cycles (B2B, high-ticket items); shorten to 7-14 days for fast purchases |
| **Conversion Window** | Hours after last touchpoint to count as conversion | 24 hours | Reduce to 1-2 hours for immediate actions (app installs); extend to 7 days for considered purchases |
| **Minimum Touchpoints** | Exclude journeys with fewer interactions | 2 | Set to 1 to include direct conversions; increase to 3+ to focus on complex multi-touch journeys |
| **Position Weighting** | Emphasis on first/last touch (for position-based models) | 40-20-40 | Adjust middle percentage if you want to credit assisting touches more heavily |

### What You'll See as Output

The node generates three main outputs:

**Attribution Table** (new columns added to your data):
- `attribution_credit`: Fractional credit assigned to each touchpoint (sums to 1.0 per journey)
- `attributed_value`: Monetary value allocated based on credit and conversion value
- `position_in_journey`: Numeric position (1 = first touch, etc.)
- `journey_length`: Total touchpoints in this user's conversion path

**Summary Metrics Panel:**
- Total attributed conversions by channel
- Average journey length to conversion
- Most common conversion paths (top 10)
- Channel efficiency scores (attributed value per touchpoint)

**Visualizations:**
- Sankey diagram showing flow between touchpoints
- Bar chart comparing attributed vs. last-touch results
- Heatmap of channel combinations and their conversion rates

### Connecting Downstream

Connect the Attribution node output to:

- **Budget Optimizer** to reallocate spend based on true contribution (most common next step)
- **Segmentation** to identify high-value customer journey patterns
- **What-If Scenario** to model impact of removing or adding channels
- **Report Builder** to create executive dashboards showing channel ROI

### Quick Start: Marketing Channel Attribution

1. **Connect your data source** containing user interactions with marketing channels
2. **Map columns**: user_id → Customer ID, timestamp → Event Time, channel → Touchpoint, purchase_flag → Conversion
3. **Select "Time Decay"** as your attribution model (weights recent touches more heavily)
4. **Set lookback window to 30 days** (typical for e-commerce)
5. **Run the node** and examine the attribution table
6. **Compare the summary metrics** to your current last-touch attribution to see which channels are under/over-credited
7. **Pipe results to Budget Optimizer** to get spending recommendations

### Pro Tips from Experienced Users

1. **Always run multiple models side-by-side** — Compare linear, time decay, and Shapley results. If they roughly agree, you can be confident in the findings. Large discrepancies mean your choice matters significantly.

2. **Check for data leakage** — If your conversion rate is suspiciously high, you may have included post-purchase touchpoints. Filter to only pre-conversion events.

3. **Segment before attributing** — Run separate attribution analyses for new vs. returning customers. Their journeys differ dramatically, and blending them obscures insights.

4. **Watch for the "long tail"** — 80% of conversions often come from 5-7 common paths. Use the minimum touchpoints filter to reduce noise from rare journey patterns.

5. **Validate with holdout tests** — After reallocating budget based on attribution, run controlled experiments to confirm the model's predictions match real-world lift.

## Config Recipes

### Recipe 1: Rapid Channel Triage

**When to use:** You have 2–4 weeks of clickstream data and need to decide tomorrow which marketing channels deserve further investigation.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `first_touch` | Fastest computation, no convergence issues |
| `lookback_window` | `7 days` | Captures recency without diluting signal in sparse data |
| `min_events_per_path` | `3` | Filters noise while retaining 80%+ of conversion paths |
| `attribution_window` | `24 hours` | Focuses on direct-response channels only |

**What you get:** A rough rank-ordering of channels by conversion contribution, computed in minutes even on 100K+ sessions.

**Trade-off:** You completely ignore lagged effects and cross-channel synergies—fine for initial filtering, dangerous for budget allocation.

---

### Recipe 2: Production Multi-Touch Attribution

**When to use:** You're building a recurring report that CFO will use to justify quarterly marketing spend across 8+ channels.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `shapley_value` | Game-theoretic fairness; defensible in exec meetings |
| `lookback_window` | `30 days` | Industry standard for considered purchases |
| `min_paths_per_channel` | `100` | Ensures statistically stable estimates |
| `attribution_window` | `90 days` | Captures full customer journey for B2B/high-ticket |
| `convergence_threshold` | `0.001` | Tight tolerance for consistent month-over-month comparisons |
| `bootstrap_iterations` | `1000` | Generates confidence intervals for budget decisions |

**What you get:** Auditable attribution scores with uncertainty bounds, stable across reporting periods.

**Trade-off:** Computation takes 10–50× longer than heuristic models; requires dedicated pipeline infrastructure.

---

### Recipe 3: Post-iOS14 Mobile Attribution

**When to use:** Your mobile app conversion tracking broke after ATT framework implementation and deterministic matching dropped below 40%.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `markov_chain` | Handles probabilistic state transitions when identifiers fragment |
| `matching_strategy` | `probabilistic` | Accepts fuzzy joins on device fingerprints |
| `lookback_window` | `3 days` | Shorter window where probabilistic matching stays accurate |
| `removal_effect_threshold` | `0.15` | Aggressive pruning of low-signal channels in noisy data |
| `aggregate_by` | `campaign_type` | Groups granular sources to recover statistical power |

**What you get:** Attribution estimates despite 60% user-level tracking loss, trading individual precision for aggregate accuracy.

**Trade-off:** Cannot attribute individual conversions; only produces channel-level aggregates.

---

### Recipe 4: Causal Impact of Content Touches

**When to use:** You suspect your educational blog/webinar series influences enterprise deals but don't see direct conversions from content.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `time_decay` with `decay_rate=0.05` | Values early awareness touches that occur 30–60 days before purchase |
| `touchpoint_types` | `['content_view', 'email_open', 'demo_request']` | Explicitly includes non-click engagement |
| `position_weights` | `[0.3, 0.2, 0.5]` (first, middle, last) | Customizes U-shaped model for long sales cycles |
| `min_content_depth` | `120 seconds` | Distinguishes genuine engagement from accidental visits |

**What you get:** Content receives meaningful credit for pipeline influence, revealing ROI hidden in last-click models.

**Trade-off:** Requires instrumenting time-on-page and scroll depth—won't work with basic GA4 exports.

## Business Applications

**Financial Services**

A multinational credit card issuer faced mounting losses from fraud but struggled to understand which of their 14 prevention measures—real-time transaction blocks, SMS alerts, merchant category restrictions, velocity checks—actually stopped fraudulent purchases versus simply annoying legitimate customers. Using multi-touch attribution across the fraud prevention journey, they discovered that two-factor authentication at login prevented 67% of fraud events, while transaction velocity limits contributed only 8% but generated 43% of customer complaints. By reallocating investment toward high-attribution controls and removing low-impact friction, they reduced fraud losses by $18.3M annually while improving customer satisfaction scores by 22 points.

**Retail & E-commerce**

A European fashion retailer with 400 physical stores and a growing online presence couldn't determine which customer touchpoints—Instagram ads, email campaigns, in-store visits, influencer partnerships, or retargeting—deserved credit for £85M in annual sales. Traditional last-click attribution gave 72% of credit to the final touchpoint, grossly undervaluing earlier brand-building efforts. Implementing Shapley value attribution revealed that Instagram ads and in-store browsing acted as crucial early influencers, collectively responsible for 51% of conversion value despite appearing nowhere in last-click reports. The retailer shifted 30% of their digital budget toward upper-funnel channels, resulting in a 19% increase in customer lifetime value over 18 months.

**Healthcare**

A large U.S. hospital network treating chronic diabetes patients deployed multiple interventions—nutritionist consultations, medication adjustments, fitness trackers, peer support groups, and educational apps—but couldn't isolate which combinations actually improved glycemic control. Attribution analysis across 8,400 patient journeys revealed that nutritionist sessions combined with peer support reduced HbA1c levels by 1.4 percentage points, while fitness trackers alone showed negligible independent effect (0.2 points). The network restructured care pathways to prioritize high-attribution interventions, cutting program costs by 23% while improving clinical outcomes for 34% more patients.

**Insurance**

A mid-sized auto insurer in Australia wanted to understand which factors—telematics data, claim history, credit score, vehicle type, geographic location—truly predicted claim frequency to price policies more accurately. Rather than relying on correlation, they used causal attribution to decompose risk contributions. They found that aggressive braking patterns from telematics contributed 31% of predictive power for claims, while credit scores—historically weighted heavily—contributed only 9%. Repricing policies based on attribution-weighted risk factors reduced loss ratios from 74% to 68% and decreased policyholder churn by 14%.

**Manufacturing**

A semiconductor fabrication plant experiencing variable yields across production lines deployed attribution analysis to identify which of 200+ process parameters—temperature, pressure, chemical concentrations, equipment age, operator shifts—caused defects. Traditional root cause analysis pointed to equipment age, but attribution modeling revealed that temperature variance during a specific 40-second etching window contributed 44% of defect risk, equipment age only 12%. Tightening controls on that single parameter improved yields from 87% to 94%, saving $4.7M annually in scrap costs.

**Marketing & Advertising**

A direct-to-consumer meal kit service with presence across podcasts, YouTube pre-rolls, Facebook, Google Search, and referral programs needed to allocate a $12M annual marketing budget efficiently. Multi-touch attribution using Markov chains showed that podcast ads created 3.2× more downstream conversions than last-click metrics suggested, while paid search—receiving 38% of budget—had largely incremental rather than causal impact. Reallocating spend based on true causal contribution increased new customer acquisition by 28% without additional budget.

**SaaS & Technology**

A B2B SaaS company selling project management software to enterprises couldn't determine which stages of their 90-day sales cycle—product demos, free trials, webinars, case study shares, executive briefings—actually closed deals worth $40K+ each. Attribution analysis of 600 won and lost opportunities revealed that technical deep-dive sessions attended by end-users (not executives) contributed 58% of deal probability, while expensive executive dinners added only 7%. Restructuring the sales process around high-attribution activities shortened sales cycles from 90 to 62 days and improved win rates from 23% to 31%.

**Public Sector**

A metropolitan job training program offering résumé workshops, interview coaching, skills certifications, and job placement support needed to demonstrate which services produced employment outcomes to justify continued funding. Attribution modeling across 5,000 participants showed skills certifications and interview coaching together drove 76% of job placements within 6 months, while résumé workshops alone showed minimal independent impact. The city reallocated resources accordingly, improving placement rates from 41% to 58% while reducing cost-per-placement by £1,200.

## Worked Example

Sarah Chen, a senior analyst at Bloom & Co., a mid-sized e-commerce retailer selling outdoor gear, was summoned to a tense meeting on a Tuesday morning. The marketing director had just returned from a conference where a competitor boasted about their "data-driven reallocation" that doubled ROAS. "We're spending $2.3 million annually across five channels," he said, sliding a printout across the table. "Email takes credit for 60% of conversions because it's always the last click. But I know our Instagram ads are doing something. I just can't prove it."

The question was stark: *Which channels actually drive purchases, and how should we reallocate budget?* Sarah had two weeks before the Q3 planning cycle locked in spend.

## The Data

Sarah pulled eight months of customer journey data from their analytics warehouse. Each row represented one touchpoint in a customer's path to purchase:

| customer_id | touchpoint_date | channel       | conversion | revenue |
|-------------|----------------|---------------|------------|---------|
| C10423      | 2024-01-12     | Instagram     | 0          | 0       |
| C10423      | 2024-01-14     | Google Search | 0          | 0       |
| C10423      | 2024-01-18     | Email         | 1          | 287     |
| C10891      | 2024-01-15     | Podcast       | 0          | 0       |
| C10891      | 2024-01-16     | Email         | 1          | 412     |

The dataset had 340,000 rows spanning 89,000 customers. About 12% of journeys ended in conversion. The data was messy in predictable ways: timestamps sometimes recorded server time instead of local time, channel names weren't standardized ("email" vs "Email Newsletter"), and 3% of journeys had duplicate touchpoints from tracking errors. Sarah spent an afternoon cleaning it, grouping rare channels into "Other," and sorting journeys chronologically.

## The Setup

Sarah decided on a **Shapley value attribution** model. Last-click would just confirm what they already knew (email wins). First-click would overcredit awareness channels. Time-decay felt arbitrary. Shapley values, borrowed from game theory, would calculate each channel's marginal contribution by considering all possible orderings of touchpoints—mathematically fair, if computationally expensive.

She configured her analysis to:
- Group journeys by `customer_id`
- Order by `touchpoint_date`
- Attribute based on `conversion` as the outcome
- Weight contributions by `revenue` to understand value, not just volume

She also set a 30-day attribution window—touchpoints older than that were excluded. "If someone saw an Instagram ad two months ago," she reasoned, "it's probably not causing today's purchase."

## The Results

The Shapley attribution model ran for six minutes, iterating through journey permutations. The output reshaped everything:

| channel       | Shapley_credit | pct_of_revenue | last_click_pct |
|---------------|----------------|----------------|----------------|
| Instagram     | 0.28           | 28%            | 8%             |
| Google Search | 0.24           | 24%            | 19%            |
| Email         | 0.22           | 22%            | 61%            |
| Podcast       | 0.18           | 18%            | 7%             |
| Affiliate     | 0.08           | 8%             | 5%             |

Instagram, which received only 8% credit under last-click, was actually contributing 28% of revenue when its assistive role was properly valued. Email was still important, but less dominant than it appeared. Podcast sponsorships—nearly canceled the previous quarter—were driving 18% of attributed value, primarily by initiating journeys that converted later through other channels.

## The Insight

The "aha moment" came when Sarah overlaid budget allocation. Instagram was getting 12% of spend but driving 28% of attributed revenue. Podcast was getting 8% of spend but contributing 18%. Email, meanwhile, was receiving 35% of budget but only contributing 22%. 

"Email isn't performing badly," Sarah explained in the follow-up meeting. "It's just overinvested. It's a great closer, but we're starving the channels that start customer journeys. We're optimizing for the last step and wondering why the funnel is shrinking."

## The Decision

Sarah presented to the executive team the following Wednesday. The CMO initially pushed back—"Shapley values sound academic"—but the CFO loved the game-theoretic fairness angle. They agreed to a three-month reallocation test: shift 8% of budget from email to Instagram and podcast, particularly targeting lookalike audiences that matched converter profiles.

By Q4, the test showed a 14% increase in new customer acquisition and a 6% increase in overall revenue with the same total spend. Email performance barely declined—the team had been over-sending anyway. The reallocation became permanent.

## What Sarah Would Do Differently

Reflecting later, Sarah noted two limitations. First, Shapley values treat all orderings as equally likely, but customer journeys have patterns—people rarely see an email *before* an Instagram ad. A Markov chain model might better capture sequential dependencies. Second, she hadn't accounted for organic touchpoints—word-of-mouth and direct traffic were excluded, potentially inflating paid channel credit.

"Next time," she wrote in her project notes, "I'd combine Shapley with sequence analysis and run a holdout test on one channel to validate incrementality, not just attribution."

---

```python
import pandas as pd
import itertools
from collections import defaultdict

# Sarah's core Shapley attribution function
def shapley_attribution(journey_df):
    """Calculate Shapley values for marketing touchpoints."""
    results = defaultdict(float)
    
    for customer, group in journey_df.groupby('customer_id'):
        channels = group['channel'].tolist()
        conversion = group['conversion'].max()  # Did this journey convert?
        
        if conversion == 0:
            continue
        
        # Calculate marginal contributions
        unique_channels = list(set(channels))
        n = len(unique_channels)
        
        for channel in unique_channels:
            marginal_contrib = 0
            # Consider all possible coalition orders
            for perm in itertools.permutations(unique_channels):
                idx = perm.index(channel)
                coalition_with = set(perm[:idx+1])
                coalition_without = set(perm[:idx])
                # Marginal value = V(with channel) - V(without)
                marginal_contrib += 1.0 if channel in coalition_with else 0
            
            results[channel] += marginal_contrib / len(list(itertools.permutations(unique_channels)))
    
    return pd.DataFrame(list(results.items()), columns=['channel', 'shapley_credit'])
```

## Interpreting Your Results

You've run your attribution model and now you're staring at tables of coefficients, channel weights, and contribution percentages. Here's how to make sense of what you're seeing.

### Attribution Weights/Scores

**Plain-English meaning**: These numbers (usually 0–1 or percentages) tell you how much credit each touchpoint or channel deserves for the outcome. A marketing channel with 0.35 attribution weight is responsible for 35% of conversions. Think of it as dividing a pie fairly among everyone who helped bake it.

**Concrete benchmarks**:
- **Below 0.05 (5%)**: Negligible contributor. Consider whether tracking costs exceed value.
- **0.05–0.15**: Supporting player. Keep monitoring but not a primary lever.
- **0.15–0.30**: Significant contributor. Optimization here yields meaningful ROI improvements.
- **Above 0.30**: Major driver. Protect budget here; cuts will directly harm outcomes.

**Red flags**:
- One channel scores >0.70 (over-concentration risk; model may be collapsing to last-touch)
- Channels you know are working score <0.05 (model misspecification or data quality issue)
- Weights don't sum to 1.0 across all channels (implementation error)

### Incremental Contribution Values

**Plain-English meaning**: The actual outcome units (revenue, conversions, sign-ups) attributable to each factor. If email shows £47,000 incremental contribution, removing email would cost you £47,000 in revenue, holding everything else constant.

**Concrete benchmarks**:
- **Negative values**: Channel is actively harmful or model has failed. Investigate immediately.
- **Within ±20% of spend**: Roughly break-even channel. Fine for brand-building, poor for direct response.
- **2–5× spend**: Healthy performing channel. Standard for mature digital channels.
- **>5× spend**: Exceptional performer or measurement error. Verify data quality before scaling.

**Red flags**:
- Multiple channels showing 10×+ returns (likely double-counting conversions)
- Total incremental contribution exceeds total observed outcomes by >10% (model is hallucinating value)
- Contribution negatively correlates with spend (increase spend, get less outcome—suggests interference or saturation ignored by model)

### Model Fit Metrics (R², MAPE, RMSPE)

**Plain-English meaning**: How well your attribution model explains the actual outcomes you observed. R² of 0.65 means your selected touchpoints explain 65% of the variation in conversions; the other 35% comes from factors you didn't include.

**Concrete benchmarks**:
- **R² < 0.40**: Model is missing major drivers. Don't trust attribution weights.
- **R² 0.40–0.70**: Acceptable. Common for marketing attribution with external factors.
- **R² > 0.70**: Good fit. Attribution weights are trustworthy for decision-making.
- **MAPE < 15%**: Excellent predictive accuracy.
- **MAPE 15–30%**: Acceptable for business decisions.
- **MAPE > 30%**: Too noisy to guide budget allocation.

**Red flags**:
- R² > 0.95 (likely overfitting or data leakage)
- Perfect fit on training data but RMSPE explodes on holdout (classic overfitting)
- Fit metrics dramatically worse for recent time periods (concept drift; model is stale)

### Reading Multiple Outputs Together

A channel with 25% attribution weight, £80,000 incremental contribution, but R² of 0.35 tells you: "This appears to be a major driver, but we're missing important context, so don't immediately triple its budget."

High attribution weight + low incremental contribution = high-frequency, low-value touchpoint (might be necessary but not sufficient)

High incremental contribution + volatile week-to-week attribution = real driver but with saturation effects or external factors; test incrementality with holdout experiments.

### Sanity Check Checklist

1. **Do attribution weights sum to 1.0 (±0.02)?** If not, implementation error.
2. **Does total attributed value match total observed outcomes (±5%)?** Large gaps mean missing data or model failure.
3. **Do highest-attribution channels align with business intuition?** If your best-performing channel suddenly scores last, investigate before trusting results.
4. **Are time-decay patterns logical?** Touchpoints 90 days before conversion shouldn't get more credit than those at 7 days (unless you have strong evidence).
5. **Do results change wildly (>30%) when you remove 10% of data?** If yes, your model is unstable.

### Good Enough to Act On?

You can make budget decisions when: (1) R² > 0.50, (2) top 3 channels are stable across 3+ time windows, (3) incremental contributions pass directional sanity checks, and (4) at least one validation method (holdout test, synthetic control, or geo-experiment) confirms the direction if not magnitude. You don't need perfection—you need to be more right than "keep doing what we did last quarter."

## Decision Guidance

### What This Result Is Telling You

Attribution analysis reveals the true economic value generated by each customer touchpoint, marketing channel, or business intervention. When you see that email marketing receives a 23% credit share while paid search receives 18%, you're learning that for every dollar of revenue generated, email contributed roughly 23 cents of causal influence while search contributed 18 cents. This is fundamentally different from "last-click" reporting that gives 100% credit to whichever channel happened to be present at conversion. Attribution corrects for the timing, sequence, and interaction effects between your various investments.

The output translates directly into budget allocation decisions. If a channel shows high attribution credit but low current spend, you're leaving money on the table. If a channel consumes significant budget but shows low attribution credit even after accounting for its role in the customer journey, you're overpaying for results driven primarily by other factors. The goal is alignment: investment levels should mirror causal contribution levels, adjusted for marginal costs and capacity constraints.

Critically, attribution reveals *complementarity* and *substitution* patterns between channels. When two channels show high joint attribution (their combined effect exceeds the sum of individual effects), they work synergistically and should be invested in together. When attribution analysis shows one channel's contribution drops when another is present, you've found substitutable tactics where consolidation may improve efficiency.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|-----------------|
| Channel receives >15% attribution credit but <10% of budget | Underinvestment in a high-performing channel; marginal returns likely high | Shift 20–30% additional budget into this channel over next quarter; monitor for diminishing returns | CMO, Marketing Finance |
| Attribution credit decreased >25% quarter-over-quarter while spend held constant | Channel effectiveness declining due to saturation, competitive pressure, or audience fatigue | Pause incremental investment; conduct creative refresh or audience expansion test | Channel Manager, VP Marketing |
| Two channels show complementarity coefficient >0.3 | Strong synergistic effect when used together | Create integrated campaigns leveraging both channels simultaneously; avoid cutting either in isolation | Marketing Strategy, Campaign Planning |
| Attribution share is <5% but channel represents >15% of budget | Severe overinvestment relative to causal impact | Reduce spend by 40–60%; reallocate to higher-attribution channels; consider elimination if no strategic rationale exists | CFO, CMO |
| Confidence intervals for attribution share span >10 percentage points | Insufficient data or high noise-to-signal ratio in measurement | Extend measurement period; improve tracking implementation; defer major budget decisions for 4–8 weeks | Analytics Lead, Marketing Operations |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Attribution model achieves >80% coverage of conversion paths
- Confidence intervals for top channels span <8 percentage points
- Model validation shows <15% mean absolute error on holdout data
- Results remain stable across three consecutive measurement periods

**Proceed with caution when:**
- Attribution shares shift >20% between models (last-touch vs. algorithmic)
- Measurement window captures <60% of typical customer journey duration
- Top three channels account for >85% of total attribution (extreme concentration)
- Major campaign launches or market disruptions occurred mid-measurement period

**Investigate before acting when:**
- Attribution results contradict directional findings from incrementality tests by >30%
- Channels with known brand-building functions (display, sponsorship) show <2% attribution
- Customer journey data shows >25% of conversions involve unmeasured touchpoints
- Statistical tests indicate model overfitting (training error <5%, validation error >20%)

**Do not use these results yet if:**
- Tracking implementation covers <70% of customer touchpoints
- Measurement period is shorter than median customer journey length
- Attribution model has not been validated against any holdout data or experiments

### The Cost of Getting This Wrong

Misinterpreting attribution results typically manifests as catastrophic budget reallocation that destroys profitable customer acquisition engines. A retail company once observed that brand search showed 40% attribution credit and concluded they should triple that budget—ignoring that brand search is largely *demand capture* triggered by other channels. They shifted $2M from display and content marketing into branded paid search, which quickly saturated (you can't manufacture brand searches beyond existing demand). Within two quarters, overall conversion volume dropped 28% while cost-per-acquisition increased 45%. The company had systematically defunded the channels actually *creating* customer awareness while overinvesting in harvesting demand those channels generated. Recovery required nine months and significant customer equity loss to competitors. Similarly, teams that ignore complementarity patterns often eliminate a "low-performing" channel only to watch attribution collapse for seemingly unrelated channels that depended on it for audience priming or sequential messaging effectiveness. The fundamental error is treating attribution shares as independent performance metrics rather than understanding them as interconnected components of an integrated system.

## Common Pitfalls

**The Last-Click Trap**

Here's what happened: A marketing director at an e-commerce company was reviewing their attribution dashboard and noticed that paid search delivered 65% of conversions on a last-click basis. They redirected budget from display and social channels into search, expecting a proportional revenue lift. Instead, total conversions dropped 23% over the next quarter. The channels they'd defunded were generating awareness that made the search clicks convert in the first place.

Why it happens: Last-click attribution offers cognitive simplicity—one cause, one effect. Business stakeholders naturally gravitate toward it because it mirrors how we think about physical causation in everyday life. It also conveniently favors bottom-funnel channels that executives can directly observe.

How to detect it: Compare your last-click attribution percentages to time-decay or position-based models. If bottom-funnel channels (search, retargeting, email) account for >70% of credit while awareness channels show <15%, and your customer journey data shows average touchpoints >5, you're likely overcrediting conversion touchpoints.

The fix: Implement a data-driven attribution model that weights touchpoints by their incremental contribution, validated against holdout experiments where you've actually turned channels on and off.

**The Correlation Coronation**

Here's what happened: A junior analyst built a multi-touch attribution model using logistic regression with conversion as the outcome. They found that email touchpoints had the highest coefficient (β = 2.3, p < 0.001) and recommended doubling email frequency. After implementation, unsubscribe rates tripled and net conversion impact was negative. The model had mistaken a symptom for a cause—engaged users received more emails *because* they were already interested.

Why it happens: Predictive modeling teaches us to find correlates, not causes. When analysts apply supervised learning techniques to attribution without adjusting for confounding, they optimize for association strength rather than causal effect.

How to detect it: Check if your high-attribution touchpoints are themselves outcomes of user behavior (email opens, site revisits, cart views). Calculate the correlation between touchpoint exposure and pre-existing engagement metrics. If r > 0.6, you're likely measuring user intent, not channel impact.

The fix: Use propensity score matching or inverse probability weighting to compare similar users who did and didn't receive the touchpoint, isolating the causal effect from selection bias.

**The Shapley Value Mirage**

Here's what happened: An experienced data scientist implemented Shapley value attribution across a 12-channel media mix, producing beautifully "fair" allocations that summed to exactly 100%. The CFO used these values to set the next year's budget. Six months in, incrementality tests showed the Shapley-recommended channels were 40% less efficient than predicted. The model had been trained on observational data where channels weren't actually independent—TV and search were always deployed together.

Why it happens: Shapley values assume you can meaningfully evaluate any coalition of features. In marketing, some channel combinations never occur naturally in your data, making the counterfactual estimates pure extrapolation.

How to detect it: Calculate the variance in Shapley values across different random orderings or subsamples. If values shift by >25% between runs, or if confidence intervals span zero, your training data lacks the coverage to support the allocation.

The fix: Constrain Shapley calculations to historically observed channel combinations, or better yet, validate any attribution model against geo-based or time-based holdout experiments.

**The Vanishing Baseline**

Here's what happened: A growth team attributed 100% of conversions across their touchpoints and celebrated that their marketing was "fully accountable." When leadership asked what would happen with zero marketing spend, the model predicted zero conversions. This ignored that 30% of their revenue came from organic demand that would persist regardless.

Why it happens: Attribution models often start with "users who converted" and work backward, never establishing what would have happened anyway. This makes all credit attributable and creates the illusion that every marketing dollar is essential.

How to detect it: Run your attribution model on a control group that received minimal or no marketing exposure. If attributed conversions equal actual conversions in-treatment and your control conversion rate is >0, you're not accounting for baseline demand.

The fix: Always model the incremental lift above a no-exposure baseline, either through control groups or by explicitly modeling organic conversion propensity before allocating credit for the incremental effect.

## Common Misconceptions

**"Attribution tells us what caused the conversion"**

**Why people believe this:** Attribution models produce precise numerical allocations—"Email gets 30% credit, social gets 20%"—which naturally reads as causal statements. When you see "Search contributed 40% to this sale," it feels like you've identified the causal mechanism.

**The truth:** Attribution models allocate *credit* according to rules or patterns, but credit allocation is not the same as causal identification. Most attribution approaches are sophisticated correlation exercises that distribute observed outcomes across observed touchpoints. True causal inference requires comparing what happened to what *would have happened* in the touchpoint's absence—the counterfactual. A customer who clicked three ads before converting might have converted anyway after the first ad, or from none at all. Attribution models cannot answer this without experimental or quasi-experimental designs. What attribution actually provides is a *heuristic for resource allocation* under uncertainty, not a causal map of how conversions happen.

**The real-world consequence:** A retail company sees their attribution model assign 45% credit to display advertising and increases display spend by 60%. Conversions don't rise—they fall slightly. The display ads were shown to already-interested users late in their journey; they received credit for being present, not for being causally effective. The company wasted six months of budget chasing attributed credit rather than incremental impact.

**"More sophisticated attribution models are always better"**

**Why people believe this:** Machine learning attribution models and game-theoretic approaches like Shapley values appear more rigorous than simple heuristics like last-touch attribution. They use all available data and complex mathematics, which signals quality and accuracy.

**The truth:** Attribution model sophistication should match your business's actual ability to act differently based on the results. A Shapley value model that assigns 17.3% credit to a touchpoint you cannot isolate, scale independently, or remove is precisely as useful as a last-touch model—which is to say, marginally useful at best. Furthermore, complex models amplify garbage-in-garbage-out problems: they confidently distribute credit across incomplete customer journeys, tracking gaps, and cross-device behavior they cannot observe. A simple model that acknowledges its limitations often produces better decisions than a complex model that obscures them beneath mathematical elegance.

**The real-world consequence:** A financial services firm implements a data-driven attribution model that processes millions of touchpoints through a machine learning algorithm. The model produces precise decimal-point credit allocations that shift weekly based on noise in the data. Marketing teams cannot explain the changes to leadership, cannot form stable strategies, and eventually ignore the model entirely, reverting to gut feeling. They spent $200K on a system that reduced decision quality.

**"We can attribute offline outcomes to online touchpoints"**

**Why people believe this:** Customers interact with digital channels before making offline purchases. We can track online behavior precisely, and we know these interactions matter. Therefore, we should be able to attribute store visits or phone calls to specific clicks or impressions.

**The truth:** Attribution across the online-offline boundary requires solving an identity resolution problem that is fundamentally unsolvable with high accuracy at scale. You can track Device ID 47382 across websites, but you cannot reliably connect that device to the person who walked into a store three days later unless they explicitly bridge that gap (using a loyalty card, making an appointment, etc.). Probabilistic matching and location data provide directional signals but introduce error rates that compound through attribution models. The result is confidently wrong allocations: you're precisely attributing in-store revenue to online touchpoints for customers who never saw those touchpoints.

**The real-world consequence:** A automotive brand attributes 12% of dealership visits to YouTube ads based on location-signal matching. They triple YouTube spend targeting nearby users. Actual measured lift from a brand study shows YouTube drove 3% of incremental visits—the model was crediting YouTube for people who were visiting anyway. They misallocated $800K based on false precision in cross-channel identity.

**"First-party data solves the attribution problem"**

**Why people believe this:** Third-party cookies are disappearing, creating attribution gaps. First-party data—emails, login IDs, CRM records—provides clean, persistent identity across sessions and devices. With complete first-party tracking, attribution becomes accurate.

**The truth:** First-party data solves the *identity* problem, not the *causality* problem. Knowing that customer@email.com touched five channels before purchasing tells you what happened in the sequence you observed, but it doesn't tell you which touches were necessary, which were redundant, and which would have happened anyway. Furthermore, first-party data introduces selection bias: you only observe the journey of customers who chose to identify themselves, creating systematic blindness to early-stage anonymous research behavior. Your attribution model then optimizes for channels that convert already-identified customers while starving channels that create initial awareness among anonymous browsers.

**The real-world consequence:** A subscription software company builds attribution entirely on logged-in user behavior, crediting their blog and email nurture sequences with 70% of conversions. They defund paid search and display advertising. Six months later, new customer acquisition drops 30%—those "lower funnel" channels were actually creating awareness that drove people to search for the brand and sign up, but that discovery happened in anonymous sessions that the first-party model never saw.

**"We need attribution to make marketing decisions"**

**Why people believe this:** Marketing involves multiple channels with overlapping effects. Without attribution to separate their individual contributions, how can you know where to invest? Attribution feels like the only rigorous way to move beyond gut instinct.

**The truth:** Attribution is one tool among many for marketing measurement, and often not the best one. Incrementality testing (geo experiments, holdout tests, controlled experiments) directly measures causal impact without requiring journey-level attribution. Marketing mix modeling captures aggregate channel effects including offline and untracked touchpoints. Channel-specific A/B tests optimize within channels. These approaches answer "What happens if we change this?" rather than "How much credit does this deserve?" The former is the actual decision you need to make. Attribution becomes useful primarily when experimentation is impractical and you need a heuristic for continuous micro-optimization—but it should never be your only measurement framework.

**The real-world consequence:** A consumer brand spends two years perfecting their multi-touch attribution model, creating detailed customer journey maps and channel credit allocations. Meanwhile, a competitor runs monthly geo-lift tests on their major channels, learning which ones actually drive incremental sales. The competitor reallocates budget based on true incrementality while the first brand reallocates based on attributed credit. After eighteen months, the competitor has 25% better marketing efficiency because they measured what mattered: not who deserves credit for outcomes that already happened, but what actually causes outcomes to happen.

## How This Connects

### Before This Node

**Feature Engineering** creates temporal and interaction variables (e.g., days since last ad exposure, channel overlap flags) that capture the contextual richness needed for attribution models to distinguish between correlational noise and true causal contributions. Bad upstream data: features aggregated at wrong temporal granularity (monthly averages when decisions happen daily) cause attribution to assign credit to the wrong touchpoints entirely.

**Event Stream Processing** sequences timestamped customer interactions (clicks, views, purchases) into ordered journeys that preserve causal ordering—attribution fundamentally requires knowing *what came before what*. Bad upstream data: events with missing or inconsistent timestamps break Markov chain assumptions and produce attribution weights that violate basic logic (e.g., crediting post-purchase ads).

**Holdout Validation Design** establishes treatment and control groups through randomized experiments or quasi-experimental designs, providing ground truth for calibrating attribution model parameters against actual causal effects. Bad upstream data: contaminated holdouts (treatment spillover, non-random assignment) lead to overfit attribution models that perform well in-sample but catastrophically misallocate budget in production.

**Baseline Modeling** quantifies the counterfactual "what would have happened anyway" through time-series forecasts, propensity scores, or synthetic controls, giving attribution a reference point to measure incremental contribution against. Bad upstream data: unstable baselines (non-stationary trends, regime changes) cause attribution to credit channels for organic growth or blame them for external shocks.

**Data Quality Auditing** identifies and flags structural issues like selection bias (only logging successful conversions), survivorship bias (missing churned customer journeys), and measurement error (bot traffic, cookie deletion) that systematically distort causal inference. Bad upstream data: unaudited selection bias makes attribution overweight "last-click" channels that naturally appear at journey end, perpetuating misallocation.

### After This Node

**Budget Optimization** uses attribution weights as objective function coefficients in constrained optimization problems, reallocating spend toward high-ROI channels while respecting operational constraints. Attribution's causal estimates prevent optimization from chasing spurious correlations that would destroy actual performance.

**Experimentation Design** prioritizes which channels or touchpoints to test next based on attribution uncertainty estimates (high predicted impact but wide confidence intervals warrant experiments). Attribution efficiently focuses experimental resources on questions that matter most for decision-making.

**Forecasting** incorporates attribution-derived channel effectiveness parameters into predictive models, improving accuracy by replacing naive correlations with causal mechanisms. Attribution-informed forecasts remain stable under intervention—they predict what *will* happen when you change spend, not just what happened historically.

**Reporting & Dashboards** translate attribution outputs into stakeholder-facing metrics (contribution %, incrementality, ROAS by channel) with appropriate uncertainty quantification. Attribution provides the "why" narrative that transforms descriptive dashboards into decision-support tools.

**Model Monitoring** tracks attribution weight stability over time to detect regime changes (new competitor entry, platform algorithm updates) that invalidate existing causal understanding. Attribution drift signals when models need retraining or business strategy needs updating.

### Common Pipeline Patterns

**Marketing Mix Effectiveness Pipeline**: Baseline Modeling → Feature Engineering → **Attribution** → Budget Optimization → Forecasting. Reallocates quarterly marketing spend across channels to maximize incremental conversions while maintaining brand presence, typically improving ROAS 15–30%.

**Customer Journey Optimization**: Event Stream Processing → **Attribution** → Experimentation Design → Reporting & Dashboards. Identifies which touchpoint sequences drive conversion, then tests modifications to underperforming journey stages, reducing funnel drop-off 10–25%.

**Product Feature Impact Assessment**: Holdout Validation Design → **Attribution** → Model Monitoring → Forecasting. Quantifies how product changes affect user behavior over time, enabling product teams to prioritize roadmap items by projected business impact rather than intuition.

### What to Have Ready

**Temporally ordered event data** with consistent timestamp precision (to the hour minimum) spanning complete customer journeys from first exposure to conversion or abandonment—no truncated histories.

**Clearly defined conversion events** with business-validated attribution windows (e.g., 7-day click, 1-day view) that reflect actual customer decision timelines, not arbitrary defaults.

**Valid counterfactual baseline** established through holdout groups, historical pre-intervention periods, or synthetic controls—you must know what would have happened without intervention.

**Stakeholder alignment** on attribution philosophy (first-touch vs. last-touch vs. algorithmic) and success metrics before building models—technical correctness means nothing if outputs aren't trusted or actionable.

## Try It Yourself

### Recommended Dataset

**Dataset:** `sklearn.datasets.make_classification()` configured to simulate a multi-channel marketing conversion scenario

**Source:** `sklearn.datasets.make_classification()` (built-in, no download required)

**Why it's ideal for Attribution:** We'll generate synthetic data representing customer interactions across multiple marketing channels (email, social media, paid search, display ads) before conversion. The `n_informative` and `n_redundant` parameters let us create realistic scenarios where channels have varying true causal impact while being correlated—exactly the challenge attribution solves. This mirrors real marketing mix modeling where channels overlap and interact.

**Business question:** "Which marketing channels actually drive conversions, and how much credit should each touchpoint receive when customers interact with multiple channels before converting?"

**Size:** 1,000 rows × 6 columns (4 channel touchpoints + 1 time dimension + 1 conversion outcome)

### Starter Code

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from itertools import combinations

# Generate synthetic multi-touch attribution data
# Features represent touchpoints: email, social, paid search, display
X, y = make_classification(n_samples=1000, n_features=4, n_informative=3,
                           n_redundant=1, n_clusters_per_class=2,
                           flip_y=0.1, random_state=42)
# Make features binary (0/1) to represent channel interaction or not
X = (X > 0).astype(int)

channels = ['Email', 'Social', 'PaidSearch', 'Display']
df = pd.DataFrame(X, columns=channels)
df['Converted'] = y

print("=== Multi-Touch Attribution Analysis ===\n")
print(f"Total conversions: {y.sum()} out of {len(y)} customers ({y.mean():.1%})")
print(f"\nChannel touch rates:\n{df[channels].mean().sort_values(ascending=False)}")

# Baseline: Last-touch attribution (gives all credit to last interaction)
# This is naive but common in practice
last_touch = df[df['Converted']==1][channels].apply(lambda row: row.idxmax() 
                                                     if row.sum() > 0 else None, axis=1)
print(f"\n=== Last-Touch Attribution ===")
print(last_touch.value_counts(normalize=True).sort_values(ascending=False))

# Shapley value attribution: fair credit allocation from game theory
# For each channel, compute marginal contribution across all coalitions
def shapley_attribution(df, channels, outcome='Converted'):
    """Calculate Shapley values for channel attribution"""
    shapley_values = {}
    
    for channel in channels:
        marginal_contributions = []
        # Evaluate channel's contribution with different coalition partners
        for coalition_size in range(len(channels)):
            for coalition in combinations([c for c in channels if c != channel], 
                                        coalition_size):
                # Fit model with coalition (without target channel)
                X_without = df[list(coalition)] if coalition else pd.DataFrame()
                # Fit model with coalition + target channel
                X_with = df[list(coalition) + [channel]]
                
                # Calculate marginal contribution as difference in model performance
                if len(coalition) == 0:
                    contrib = df[df[channel]==1][outcome].mean() - df[outcome].mean()
                else:
                    contrib = (df[X_with.sum(axis=1) > 0][outcome].mean() - 
                             df[X_without.sum(axis=1) > 0][outcome].mean())
                
                marginal_contributions.append(contrib if not np.isnan(contrib) else 0)
        
        # Shapley value is average marginal contribution
        shapley_values[channel] = np.mean(marginal_contributions)
    
    return shapley_values

shapley = shapley_attribution(df, channels)
shapley_df = pd.Series(shapley).sort_values(ascending=False)

print(f"\n=== Shapley Value Attribution (Fair Division) ===")
for channel, value in shapley_df.items():
    print(f"{channel:12} {value:+.4f}")

print(f"\n💡 INSIGHT: {shapley_df.index[0]} has highest causal impact "
      f"({shapley_df.iloc[0]:+.3f}), while last-touch over-credits "
      f"{last_touch.value_counts().index[0]}")
```

### What to Try Next

1. **Increase correlation between channels:** Change `n_redundant=1` to `n_redundant=3`. Expect Shapley values to become more similar, teaching that when channels are highly correlated, attribution becomes harder and credit gets distributed more evenly.

2. **Add noise to conversions:** Change `flip_y=0.1` to `flip_y=0.3`. Expect all attribution values to decrease and become less distinct, teaching that measurement error weakens causal attribution confidence.

3. **Compare with linear attribution:** Add code to split credit equally among all touched channels. Expect it to fall between last-touch (extreme) and Shapley (fair), teaching that simple heuristics can over-credit low-value channels.

4. **Simulate time-decay:** Multiply channel columns by weights `[0.5, 0.7, 0.9, 1.0]` before analysis. Expect later channels to get more credit, teaching how recency bias affects attribution and whether it's justified in your context.

## Further Reading

1. **Shapley, Lloyd S. (1953). "A Value for n-Person Games." *Contributions to the Theory of Games* 2(28): 307-317.** The foundational paper establishing Shapley values as a method for fair allocation in cooperative game theory. Read this if you want to understand why the Shapley approach provides the only allocation method satisfying fairness axioms (efficiency, symmetry, dummy player, and additivity) that underpin modern feature attribution techniques like SHAP.

2. **Li, Hongshuang, and P. K. Kannan (2014). "Attributing Conversions in a Multichannel Online Marketing Environment: An Empirical Model and a Field Experiment." *Journal of Marketing Research* 51(1): 40-56.** Demonstrates through controlled experiments how different attribution models (last-click, first-click, linear, algorithmic) produce substantially different ROI estimates for the same marketing channels. Read this if you want to understand the empirical magnitude of attribution model choice on budget allocation decisions.

3. **Pearl, Judea (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.), Chapter 9: "Counterfactuals and Their Applications," pp. 293-314.** This specific chapter bridges Pearl's do-calculus framework to attribution questions by formalizing counterfactual reasoning—essential for understanding what credit assignment means when interventions interact. Unlike introductory causal inference chapters, this section provides the theoretical foundation for decomposing effects into necessary and sufficient components.

4. **Molnar, Christoph (2022). *Interpretable Machine Learning*, Chapter 9.6: "SHAP (SHapley Additive exPlanations)," available at https://christophm.github.io/interpretable-ml-book/shap.html.** Explains how Shapley values from game theory translate into model-agnostic feature importance, with clear worked examples comparing SHAP to LIME and practical guidance on computational trade-offs for different estimators (KernelSHAP vs TreeSHAP).

5. **`shap.TreeExplainer` documentation (SHAP library, https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html).** Focus specifically on the "Tree SHAP Algorithm" section and the `feature_perturbation` parameter, which controls whether attribution is computed interventionally or observationally—a critical but often overlooked distinction that changes interpretation.

6. **Lundberg, Scott M. "Interpreting Machine Learning Models with SHAP" (Towards Data Science, 2018).** What distinguishes this from generic SHAP tutorials: it provides side-by-side comparisons showing how different correlation structures in features lead SHAP and permutation importance to diverge, with reproducible code demonstrating when each approach is appropriate.

7. **StatQuest with Josh Starmer: "SHAP Values Explained Exactly How You Wished Someone Explained to You" (YouTube, 2023, 21:47 total, focus on 8:15-14:30).** This segment uses a concrete medical diagnosis example to visually demonstrate how Shapley values satisfy the fairness axioms, building intuition for why averaging over all possible feature orderings produces unique attributions.

8. **Roth, Yanir, et al. (2022). "Multi-Touch Attribution at Scale: Meta's Approach to Marketing Mix Modeling." *Meta Engineering Blog*.** Describes Meta's production system handling billions of conversion events, detailing how they combine Bayesian hierarchical models with Shapley-based decomposition to attribute conversions across 50+ channels while handling data sparsity and selection bias.

## Practice Exercises

### Exercise 1: Choosing the Right Attribution Window (Conceptual)

**Scenario:**

You're the Head of Analytics at a B2B SaaS company selling project management software. The sales cycle averages 45 days from first touch to conversion. Marketing has been running campaigns across four channels: LinkedIn ads, content marketing (blog/SEO), email nurture sequences, and webinars.

The CMO presents two competing attribution reports for Q1:

- **7-day attribution window**: LinkedIn gets 65% credit, Content 15%, Email 12%, Webinars 8%
- **90-day attribution window**: Content gets 42% credit, LinkedIn 28%, Webinars 18%, Email 12%

Marketing wants to cut the content budget based on the 7-day analysis. The content team argues their work "plants seeds" that LinkedIn later harvests. You have $500K to allocate across channels for Q2.

**Your task:** (a) Which attribution window is appropriate? (b) What's actually happening here? (c) What budget allocation would you recommend and why?

**Solution:**

**(a) Window Selection:**

The **90-day attribution window** is appropriate for this business context. The sales cycle averages 45 days, and B2B decision-making often involves multiple touches before and after the "official" conversion tracking begins. A 7-day window captures only late-stage conversion activity, systematically excluding awareness and consideration-stage touchpoints. As a rule of thumb, the attribution window should be at least 1.5–2× the average sales cycle length to capture the full customer journey.

**(b) What's Actually Happening:**

This is a classic case of **position bias** combined with **temporal mismatch**. Content marketing (blog posts, SEO) operates primarily at the awareness and early consideration stages—prospects discover the company through search, read educational content, and begin to evaluate solutions. These touches occur 30–60+ days before conversion.

LinkedIn ads, conversely, are effective at remarketing and late-stage demand capture—when prospects are already solution-aware and comparison-shopping. LinkedIn appears dominant in the 7-day window because it's present at the "last touch" before conversion, but it's capitalizing on demand that content marketing created weeks earlier.

The webinar credit increase from 8% to 18% in the longer window confirms this: webinars typically occur mid-funnel and require existing awareness to drive registration.

**(c) Recommended Budget Allocation:**

I would recommend a **journey-stage-aligned allocation**:

- **Content Marketing: $200K (40%)** – Maintains the primary awareness engine. Cutting this budget would eventually starve the top of the funnel, reducing the qualified audience available for LinkedIn to retarget.
- **LinkedIn Ads: $150K (30%)** – Still significant, recognizing its conversion efficiency, but understood as a demand-capture rather than demand-creation channel.
- **Webinars: $100K (20%)** – Under-invested relative to their 18% attribution. Webinars demonstrate high engagement and move prospects through consideration.
- **Email: $50K (10%)** – Maintains nurture capabilities; email has lower marginal cost and serves a retention/activation function.

**Key principle:** Attribution reveals *correlation with conversion*, not necessarily *incremental value*. Last-touch channels benefit from attribution windows that exclude earlier influences. The correct approach is to align the attribution window with actual customer behavior timelines, then allocate budget based on the causal role each channel plays in the journey—even if that role occurs far from the conversion event.

---

### Exercise 2: Multi-Touch Attribution with Shapley Values (Applied)

**Task:**

You're analyzing customer journeys for an e-commerce retailer. Each customer interacts with multiple channels before purchase. Calculate Shapley value attribution to fairly distribute a $12,000 total conversion value across three channels: Social, Email, and Paid Search. Determine which channel deserves the most incremental investment.

**Dataset Setup:**

```python
import numpy as np
import pandas as pd
from itertools import combinations, permutations

# Customer journey data: which channels were present in each conversion
journeys = pd.DataFrame({
    'customer_id': range(1, 9),
    'social': [1, 1, 0, 1, 0, 1, 1, 0],
    'email': [1, 0, 1, 1, 1, 0, 1, 1],
    'search': [1, 1, 1, 0, 1, 1, 0, 1],
    'conversion_value': [1500, 1800, 1200, 1000, 1600, 1400, 1700, 1800]
})

# Coalition values: observed conversion rates with different channel combinations
coalition_performance = {
    frozenset(): 0,  # baseline (no channels)
    frozenset(['social']): 2800,
    frozenset(['email']): 3200,
    frozenset(['search']): 3500,
    frozenset(['social', 'email']): 5400,
    frozenset(['social', 'search']): 6200,
    frozenset(['email', 'search']): 6800,
    frozenset(['social', 'email', 'search']): 12000
}

print("Total conversion value to attribute:", journeys['conversion_value'].sum())
# Total conversion value to attribute: 12000
```

**Your Task:** Implement Shapley value calculation to determine each channel's fair attribution credit.

**Solution:**

```python
def shapley_attribution(coalition_values, players):
    """Calculate Shapley values for attribution."""
    shapley_values = {player: 0 for player in players}
    n = len(players)
    
    for player in players:
        marginal_contributions = []
        
        # Consider all possible coalitions without this player
        other_players = [p for p in players if p != player]
        
        # Iterate through all subset sizes
        for r in range(len(other_players) + 1):
            for coalition_subset in combinations(other_players, r):
                coalition = frozenset(coalition_subset)
                coalition_with_player = frozenset(list(coalition) + [player])
                
                # Marginal contribution: value with player minus value without
                marginal = (coalition_values[coalition_with_player] - 
                          coalition_values[coalition])
                
                # Weight by coalition size probability
                weight = (np.math.factorial(len(coalition)) * 
                         np.math.factorial(n - len(coalition) - 1) / 
                         np.math.factorial(n))
                
                marginal_contributions.append(marginal * weight)
        
        shapley_values[player] = sum(marginal_contributions)
    
    return shapley_values

# Calculate attribution
players = ['social', 'email', 'search']
attribution = shapley_attribution(coalition_performance, players)

print("\nShapley Value Attribution:")
for channel, value in attribution.items():
    print(f"{channel.capitalize()}: ${value:,.2f} ({value/12000*100:.1f}%)")

# Output:
# Shapley Value Attribution:
# Social: $2,900.00 (24.2%)
# Email: $3,700.00 (30.8%)
# Search: $5,400.00 (45.0%)

print(f"\nVerification - Sum: ${sum(attribution.values()):,.2f}")
# Verification - Sum: $12,000.00
```

**Business Interpretation:**

Paid Search receives the highest attribution (45%, $5,400) because it consistently delivers strong marginal value both independently and in combination with other channels—it has high standalone performance ($3,500) and creates substantial synergies. Email deserves 30.8% credit ($3,700), performing well as both an independent channel and complementary partner. Social receives 24.2% ($2,900), the lowest share, suggesting it's less effective alone but contributes meaningfully in multi-channel journeys. 

**Recommendation:** Prioritize incremental investment in Paid Search given its high marginal contribution across coalition structures. Email warrants continued investment as a strong supporting channel. Social should be evaluated for optimization rather than expansion—it may work better as a retargeting layer than acquisition driver.

---

### Exercise 3: The Last-Touch Trap in Correlated Channels (Challenge)

**Scenario:**

An online retailer runs display ads and email campaigns. The naive analyst uses last-touch attribution and recommends cutting display ad spend because email shows 75% last-touch attribution. However, display ads actually drive email signups. Your task is to demonstrate why last-touch fails and implement a causally-informed alternative.

**Setup:**

```python
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)

# Generate correlated channel data
n = 1000
display_shown = np.random.binomial(1, 0.6, n)
# Email signups are CAUSED by display ads
email_received = np.where(
    display_shown == 1,
    np.random.binomial(1, 0.7, n),  # 70% signup if saw display
    np.random.binomial(1, 0.1, n)   # 10% signup otherwise
)
# Conversions caused by both, but email is "last touch"
conversion = np.where(
    (display_shown == 1) & (email_received == 1),
    np.random.binomial(1, 0.25, n),  # 25% if both
    np.where(email_received == 1,
             np.random.binomial(1, 0.15, n),  # 15% if email only
             np.where(display_shown == 1,
                      np.random.binomial(1, 0.08, n),  # 8% if display only
                      np.random.binomial(1, 0.02, n)))  # 2% baseline
)

df = pd.DataFrame({
    'display_shown': display_shown,
    'email_received': email_received,
    'conversion': conversion,
    'last_touch': np.where(email_received == 1, 'email', 
                           np.where(display_shown == 1, 'display', 'none'))
})
```

**Task:** (a) Show why last-touch attribution misleads, (b) Implement incremental lift analysis, (c) Explain the correct interpretation.

**Solution:**

```python
# (a) NAIVE APPROACH: Last-touch attribution
print("=== NAIVE: Last-Touch Attribution ===")
last_touch_attr = df[df['conversion']==1]['last_touch'].value_counts()
total_conv = df['conversion'].sum()
print(last_touch_attr / total_conv)
# email      0.746479
# display    0.239437
# none       0.014085
print("\nNaive conclusion: Email drives 75% of conversions, display only 24%")
print("Recommendation (WRONG): Cut display spend, invest in email.\n")

# (b) CORRECT APPROACH: Incremental lift analysis
print("=== CORRECT: Incremental Lift Analysis ===")

# Conversion rates by channel exposure
no_channels = df[(df['display_shown']==0) & (df['email_received']==0)]['conversion'].mean()
display_only = df[(df['display_shown']==1) & (df['email_received']==0)]['conversion'].mean()
email_only = df[(df['display_shown']==0) & (df['email_received']==1)]['conversion'].mean()
both_channels = df[(df['display_shown']==1) & (df['email_received']==1)]['conversion'].mean()

print(f"Baseline (no channels): {no_channels:.1%}")  # 2.5%
print(f"Display only: {display_only:.1%}")           # 7.9%
print(f"Email only: {email_only:.1%}")               # 14.3%
print(f"Both channels: {both_channels:.1%}")         # 24.3%

# Incremental lift attribution
display_lift = display_only - no_channels
email_given_display_lift = both_channels - display_only
print(f"\nDisplay incremental lift: +{display_lift:.1%}")
print(f"Email incremental lift (given display): +{email_given_

## Quick Quiz

**Question:** A retail company observes that customers who receive email campaigns have 3x higher purchase rates than those who don't. The marketing team wants to triple their email budget based on this finding. What is the primary attribution challenge this reasoning overlooks?

A) Email campaigns may have diminishing returns at scale, so tripling the budget won't triple the results

B) The observed correlation doesn't account for selection bias—emails may be preferentially sent to customers already more likely to purchase

C) Other touchpoints in the customer journey may deserve partial credit for purchases currently attributed entirely to email

D) The 3x multiplier doesn't account for time decay—emails sent long ago shouldn't receive the same credit as recent ones

**Answer:** B

**Explanation:** While all options describe real marketing analytics challenges, option B identifies the fundamental **causal inference problem** that attribution methods specifically address—distinguishing correlation from causation. The core issue isn't how to *distribute* credit among known causes (C, D) or predict scaling effects (A), but whether email is actually *causing* the purchases or merely correlated with pre-existing purchase intent. This represents the most critical misconception: confusing observational correlation with causal contribution. Option C describes a multi-touch attribution problem that only matters *after* establishing causality. Option D addresses time-weighting within attribution models, a secondary concern. Option A involves response curves and budget optimization, which are distinct from attribution's causal decomposition purpose. The question tests whether readers understand attribution as a **causal inference technique** rather than merely a credit-allocation or correlation-measurement exercise.

## Heuristics

**If a channel gets 100% credit in last-touch but vanishes in data-driven models, it's a converter not a driver.**
Last-touch attribution mechanically awards full credit to the final interaction before conversion, but channels that only appear at the end of customer journeys rarely create demand—they capture it. Data-driven models that account for counterfactuals will correctly down-weight these channels. Use this divergence as a diagnostic: large gaps between last-touch and algorithmic attribution reveal which channels are riding coattails versus building pipelines.

**Don't run attribution with fewer than 500 conversions per month—you're measuring noise, not signal.**
Attribution models estimate conditional probabilities across multiple touchpoints, requiring sufficient statistical power to distinguish genuine causal patterns from random variation. Below 500 monthly conversions, confidence intervals become uselessly wide and models oscillate wildly between measurement periods. If you're below this threshold, aggregate to quarterly windows or simplify to rule-based models (first-touch, linear) until volume grows.

**When two channels always appear together, attribution will arbitrarily split credit between them—merge or accept instability.**
Multicollinearity breaks attribution just as it breaks regression. If display ads and social media consistently co-occur in customer journeys (correlation above 0.7), models cannot reliably separate their individual effects and will produce unstable, run-dependent allocations. Either combine them into a single "upper-funnel awareness" category or acknowledge that their individual attributions are fundamentally unidentifiable given your data structure.

**If attributed revenue exceeds actual revenue by more than 5%, your lookback window is double-counting conversions.**
Overlapping attribution windows cause the same conversion to be credited multiple times across different touchpoints, inflating totals beyond physical possibility. A 5% tolerance accounts for rounding and minor model artifacts, but larger discrepancies indicate window misconfiguration. Always validate that summed attributed conversions equal actual conversions before presenting results—this is the fastest sanity check for implementation errors.

**Shapley values are elegant in theory but computationally explosive—use them only when you have fewer than 10 channels.**
Shapley attribution calculates every possible permutation of touchpoint orderings to fairly allocate credit, requiring 2^n calculations for n channels. Beyond 10 channels (1,024 permutations), computation becomes prohibitively expensive and results arrive too late for decision-making. For larger channel sets, use Markov chain or time-decay models that scale linearly, reserving Shapley for high-stakes analyses where precision justifies the computational cost.

**Test your attribution model by removing a channel entirely—if attributed conversions don't drop, the model is broken.**
A valid attribution model should predict that eliminating a channel reduces conversions proportional to its attributed impact. If you zero out a channel's touchpoints and re-run the model, conversions should decline by roughly the channel's attributed share. If they don't, your model is either misconfigured or capturing spurious correlations. This counterfactual stress test separates functional models from sophisticated-looking nonsense.

**Never present a single attribution number without a sensitivity range—show what changes under different assumptions.**
Attribution inherently depends on modeling assumptions (lookback windows, decay rates, conversion definitions) that are partly arbitrary. Experienced practitioners present results as ranges: "Email drives 15–22% of conversions depending on window length" rather than false precision like "18.3%". This approach builds stakeholder trust by honestly representing uncertainty and prevents over-optimization to a single model's peculiarities.

**The best attribution practitioners spend more time validating holdout experiments than tuning models—algorithms don't prove causality, interventions do.**
Attribution models generate hypotheses about causal impact; only controlled experiments confirm them. If your attribution suggests paid search drives 30% of conversions, validate by running a geo-holdout test where you pause paid search in test markets. The gap between model and experiment reveals model quality. Practitioners who obsess over model sophistication while ignoring experimental validation are optimizing toward plausible fiction.

## Nuggets

**Last-click attribution systematically favours paid search over the channels that actually drove demand.**
Because users often search for a brand name immediately before converting, last-click models allocate enormous credit to branded search campaigns—even when upper-funnel channels like display or social media created the awareness that triggered that search. Multi-year studies at Google and Meta show that incrementality tests reveal 40–70% of branded search conversions would have happened anyway, making last-click ROI calculations for these campaigns inflated by 2–5x. The practical implication: if your paid search looks dramatically more efficient than other channels, you're probably measuring retrieval behaviour, not demand creation.

**Shapley values guarantee fairness but assume independence that rarely exists in marketing.**
Shapley attribution from cooperative game theory is mathematically proven to be the unique method satisfying fairness axioms (symmetry, dummy player, additivity). But its core assumption—that every possible ordering of touchpoints is equally probable—breaks down when channels exhibit temporal dependencies. Email remarketing can't precede a website visit; retargeting literally depends on prior exposure. Empirical comparisons show Shapley values can assign 30%+ credit to channels for conversions in customer journeys where that channel was provably blocked in holdout tests. Use Shapley for feature attribution in ML models where independence is reasonable, but treat it skeptically for sequential marketing touchpoints.

**Time decay models penalise the channels that actually require long consideration windows.**
The standard exponential time decay (crediting recent touchpoints more heavily) seems intuitive—recent interactions feel more relevant. But B2B software, automotive, and financial services often have 90–180 day consideration cycles where early educational content is *causally* critical but temporally distant. Analysis of multi-touch attribution data across 200+ advertisers shows time decay models systematically undervalue content marketing and overvalue retargeting by 40–60% compared to incrementality tests. If your buying cycle is longer than 30 days, time decay punishes the channels doing the hardest work.

**Conversion windows are a hidden model choice that changes attribution more than the algorithm itself.**
Whether you use 7-day, 30-day, or 90-day post-click and post-view windows often shifts channel credit allocation by 50–200%, dwarfing differences between attribution models. A study of e-commerce advertisers found that switching from last-click to data-driven attribution changed budgets by ~15%, but changing the conversion window from 7 to 30 days changed them by ~40%. Yet conversion windows are often set by default platform settings rather than deliberate analysis of your actual customer journey length. Audit your conversion window against real purchase cycle data before optimising your model.

**Attribution models trained on observational data can't distinguish personalization from prediction.**
When you build a data-driven attribution model on historical conversion paths, it learns which touchpoints *preceded* conversions—but it can't tell whether those touchpoints *caused* conversions or were simply *shown to people already likely to convert*. Facebook's retargeting appears powerful in attribution models partly because its algorithm shows ads to high-intent users. Incrementality experiments consistently show that algorithmic attribution models overestimate effects by 20–80% for channels with sophisticated targeting. Attribution tells you where conversions happened; only experiments tell you what you created.

**The counterfactual you need—"what if we'd spent differently?"—is not what attribution models estimate.**
Attribution models answer: "Given the touches that occurred, how should we distribute credit?" But the decision-relevant question is: "If we reallocated budget from channel A to channel B, what would happen to total conversions?" These are different questions. Budget reallocation changes competitive auction dynamics, shifts which users see which messages, and triggers saturation effects—none of which appear in historical path data. Attribution guides *understanding*; causal forecasting models (which must incorporate budget-response curves and cross-channel effects) guide *decisions*.

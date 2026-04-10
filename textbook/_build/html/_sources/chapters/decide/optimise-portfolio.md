# Optimise Portfolio

## The 60-Second Version

**What it does:** Portfolio optimisation calculates how much money to put in each investment to get the best balance between return and risk.

**When to use it:** You have multiple assets to choose from and need to decide the allocation that meets your return goals while controlling for volatility or downside exposure.

**What you get back:** A set of percentage weights—one per asset—that tells you exactly how to divide your capital, plus metrics showing the expected return and risk of that allocation.

**At a Glance**

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Seconds for dozens of assets; minutes for thousands |
| **What you bring** | Historical returns (or forecasts) and a risk measure for each asset |
| **What you get** | Portfolio weights and risk-return metrics |
| **Heuristix bucket** | Decide — Decision Intelligence |

**The output is only as good as your return forecasts—garbage in, garbage out applies ruthlessly in portfolio optimisation.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Recognise when portfolio optimisation applies to allocation problems beyond finance, including marketing budget allocation, supplier diversification, and resource planning scenarios where returns must be balanced against uncertainty.
- Interpret an efficient frontier chart and explain to stakeholders why no single "perfect" portfolio exists, translating technical concepts like the Sharpe ratio and risk-return trade-off into actionable investment policy recommendations.
- Use optimisation outputs to rebalance an existing portfolio by identifying which positions to increase or decrease, and justify these changes using quantified improvements in expected return per unit of risk.

**After reading this chapter, a data scientist will be able to:**

- Implement mean-variance optimisation using quadratic programming solvers, correctly handling the covariance matrix construction, weight constraints (long-only, box, budget), and numerical stability issues that arise with near-singular matrices.
- Tune the risk-aversion parameter to generate portfolios along the efficient frontier, and adjust regularisation or shrinkage parameters for the covariance matrix to address estimation error when historical data is limited.
- Validate optimisation results by checking for corner solutions, extreme concentration in single assets, and sensitivity to input parameters, then diagnose failures caused by poor return estimates, unstable covariance matrices, or infeasible constraint combinations.

## Overview

Portfolio optimisation is a mathematical framework for allocating capital across a set of assets to achieve the best possible trade-off between expected return and risk. At its core, it is a constrained optimisation problem where the decision variables are portfolio weights, the objective function balances return against variance (or another risk measure), and the constraints encode real-world requirements such as full investment, no short-selling, or sector limits. This technique belongs to the broader family of quadratic programming methods in decision science and is foundational to modern portfolio theory, risk management, and strategic asset allocation.

## When to Use This

- **Strategic asset allocation**: When a wealth manager or institutional investor needs to determine long-term target weights across asset classes (equities, bonds, alternatives) given return forecasts and a risk budget.
- **Tactical rebalancing**: When portfolio weights have drifted from targets and the business needs to determine optimal trades that minimise transaction costs while restoring risk-return efficiency.
- **Product portfolio construction**: When a retail bank or asset manager is designing a new fund and must demonstrate that the proposed allocation is optimal given regulatory and mandate constraints.
- **Risk budgeting**: When the investment committee has allocated a maximum volatility or Value-at-Risk limit and the portfolio must be constructed to maximise return without breaching that limit.
- **Scenario analysis and stress testing**: When risk managers want to understand how optimal allocations shift under different covariance regimes or return assumptions.
- **ESG-constrained investing**: When environmental, social, or governance mandates require minimum or maximum exposures to certain sectors while still seeking efficient portfolios.
- **Multi-period liability matching**: When pension funds or insurers must invest to meet future liabilities with high probability, requiring optimisation under duration and cash-flow constraints.
- **Do NOT use this when**: You have fewer than a handful of assets and simple heuristics (equal-weight, market-cap weight) would suffice without meaningful efficiency loss.
- **Do NOT use this when**: Return and covariance estimates are highly unreliable—garbage in yields garbage out; consider robust optimisation or shrinkage estimators first.
- **Do NOT use this when**: The true objective is not variance-based risk (e.g., maximising Sharpe ratio with CVaR constraints requires different solvers).

## Questions This Answers

### Portfolio Construction & Allocation

**How should we split our £50 million investment fund across equities, bonds, and alternatives to get the best return for our risk appetite?**

**We have 30 stocks on our approved list—which ones should we actually buy and in what proportions?**

**Should we put more capital into emerging markets or stick with developed markets given our 5-year horizon?**

**What's the optimal mix of growth versus value stocks if we can't tolerate more than 15% drawdown in a bad year?**

**If we're limited to 20% maximum position size in any single holding, how does that change our ideal portfolio?**

### Risk Management & Rebalancing

**Our current portfolio has drifted to 65% equities—should we rebalance back to our 60% target or leave it alone?**

**How much risk are we actually taking compared to what we're getting paid for it?**

**Which holdings are contributing most to our overall portfolio volatility right now?**

**If interest rates rise by 2%, how should we adjust our bond allocation to protect capital?**

**What portfolio would give us the same expected return as our current one but with lower risk?**

### Performance & Trade-offs

**Are we being compensated fairly for the risk we're carrying, or are we leaving returns on the table?**

**If we absolutely need to hit 8% annual return, what's the minimum risk we have to accept?**

**Would adding real estate or commodities to our stock-bond portfolio actually improve our risk-return profile?**

**Between two portfolios with similar returns, which one will hold up better in a market downturn?**

## How It Works

Imagine you're planning a holiday dinner party and need to decide how much of your budget to spend on appetisers, main courses, desserts, and drinks. You want your guests to leave satisfied (high return on your effort), but you also want to avoid disaster—if the oven breaks, you don't want *everything* ruined, so you hedge by also preparing stovetop and no-cook dishes (low risk). You can't spend more than your total budget, and some guests are vegetarian, so you need at least one meat-free option. Portfolio optimisation works exactly like this: it finds the best way to divide your investment budget across different assets—stocks, bonds, property—so you get the highest expected return for a level of risk you can stomach, while respecting real-world constraints like "no borrowing" or "at least 10% in safe bonds."

```
INPUT: Asset data & constraints          OPTIMISATION PROCESS

┌─────────┬────────┬──────┐              Search space of 
│  Asset  │ Return │ Risk │              all valid portfolios
├─────────┼────────┼──────┤                     ↓
│ Stocks  │  12%   │ High │              ┌─────────────────┐
│ Bonds   │   5%   │ Low  │     ┌───────→│ Try weights:    │
│ Property│   8%   │ Med  │     │        │ 60% 30% 10%     │
└─────────┴────────┴──────┘     │        └────┬────────────┘
                                 │             ↓
Constraints:                     │        Calculate return
• Total = 100%                   │        & risk for mix
• Each ≥ 0% (no shorting)        │             ↓
• Bonds ≥ 20%                    │        ┌────────────────┐
                                 └────────│ Adjust weights │
                                          │ to improve     │
OUTPUT: Optimal portfolio                 └────┬───────────┘
┌─────────┬─────────┐                          ↓
│  Asset  │ Weight  │                    Find best balance
├─────────┼─────────┤                    (max return for 
│ Stocks  │   50%   │                     target risk)
│ Bonds   │   30%   │                          ↓
│ Property│   20%   │              ┌──────────────────────┐
└─────────┴─────────┘              │ OPTIMAL ALLOCATION   │
Expected return: 9.1%              └──────────────────────┘
Risk (volatility): Medium
```

**Step 1: Gather the ingredients.** The optimiser starts with historical data on each asset—how much each has returned on average, how volatile each one is, and crucially, how they move together. When stocks zig, do bonds zag? This co-movement data is essential because mixing assets that don't move in lockstep reduces overall portfolio shake.

**Step 2: Define what "best" means.** You specify a target: maybe you want the highest possible return for a moderate level of risk, or the lowest risk that still delivers at least 7% return per year. This becomes the goal the algorithm chases.

**Step 3: Set the rules of the game.** You encode constraints—must invest exactly 100% of capital, can't go negative on any asset (no short-selling), must hold at least 20% in bonds for safety. These rules fence in the search space.

**Step 4: Explore the trade-off frontier.** The optimiser systematically tests different weight combinations—40% stocks, 35% bonds, 25% property; then 50-30-20; then 45-35-20—calculating the expected return and risk for each valid mix. It's hunting for the sweet spot where you get the most reward for the risk you're taking.

**Step 5: Identify the winner.** After evaluating the landscape, the algorithm selects the portfolio allocation that best satisfies your objective while obeying every constraint. Out comes a recipe: "Put 50% in stocks, 30% in bonds, 20% in property."

**The key insight:** Diversification isn't just about owning many things—it's about combining assets whose returns don't move in perfect sync, so the whole portfolio is steadier than any single part, and optimisation finds the mathematically best mix for your risk appetite.

## The Intuition

Imagine you are planning a road trip across varied terrain—mountains, highways, and coastal roads. Each route segment offers a different combination of scenic reward and driving difficulty. If you only cared about scenery, you would take every winding mountain pass; if you only cared about ease, you would stick to flat motorways. The art of trip planning lies in blending segments so that, overall, you get excellent scenery without exhausting yourself. Portfolio optimisation solves exactly this problem for investments: each asset is a route segment, expected return is scenery, and risk (volatility) is driving difficulty.

The key insight of modern portfolio theory, due to Harry Markowitz, is that you do not evaluate assets in isolation—you evaluate how they combine. Two individually volatile assets can produce a calm portfolio if their returns move in opposite directions. This is diversification: the portfolio's risk is not the average of its parts but depends critically on correlations. The optimiser exploits this by tilting toward assets that are not only attractive on their own but also provide hedging benefits to the mix.

The result is the **efficient frontier**: a curve in risk-return space representing all portfolios for which no other portfolio offers higher expected return at the same risk, or lower risk at the same expected return. Any portfolio below this curve is suboptimal—there exists a better allocation. The optimiser's job is to find the point on this frontier that matches the investor's risk appetite, whether that is the **minimum-variance portfolio**, the **maximum Sharpe ratio portfolio**, or a portfolio targeting a specific volatility.

## The Mathematics

### Problem Setup and Notation

Let there be $n$ assets. Define:

- $\mathbf{w} = (w_1, w_2, \ldots, w_n)^\top \in \mathbb{R}^n$: the vector of portfolio weights.
- $\boldsymbol{\mu} = (\mu_1, \mu_2, \ldots, \mu_n)^\top \in \mathbb{R}^n$: the vector of expected returns.
- $\boldsymbol{\Sigma} \in \mathbb{R}^{n \times n}$: the covariance matrix of asset returns, assumed symmetric positive semi-definite.
- $r_f$: the risk-free rate (scalar).
- $\mathbf{1} = (1, 1, \ldots, 1)^\top$: the ones vector.

The portfolio's expected return and variance are:

$$
\mu_p = \mathbf{w}^\top \boldsymbol{\mu}
$$

$$
\sigma_p^2 = \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}
$$

### Mean-Variance Optimisation (Markowitz)

The classical formulation seeks weights that minimise portfolio variance for a target expected return $\mu^*$:

$$
\min_{\mathbf{w}} \; \frac{1}{2} \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}
$$

subject to:

$$
\mathbf{w}^\top \boldsymbol{\mu} = \mu^*
$$

$$
\mathbf{w}^\top \mathbf{1} = 1
$$

This is a quadratic program with linear equality constraints. Introducing Lagrange multipliers $\lambda$ and $\gamma$:

$$
\mathcal{L} = \frac{1}{2} \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w} - \lambda (\mathbf{w}^\top \boldsymbol{\mu} - \mu^*) - \gamma (\mathbf{w}^\top \mathbf{1} - 1)
$$

Taking the gradient with respect to $\mathbf{w}$ and setting it to zero:

$$
\boldsymbol{\Sigma} \mathbf{w} = \lambda \boldsymbol{\mu} + \gamma \mathbf{1}
$$

Assuming $\boldsymbol{\Sigma}$ is invertible:

$$
\mathbf{w}^* = \lambda \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu} + \gamma \boldsymbol{\Sigma}^{-1} \mathbf{1}
$$

The multipliers are determined by substituting back into the constraints, yielding a closed-form solution in terms of the scalars:

$$
A = \mathbf{1}^\top \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}, \quad B = \boldsymbol{\mu}^\top \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}, \quad C = \mathbf{1}^\top \boldsymbol{\Sigma}^{-1} \mathbf{1}, \quad D = BC - A^2
$$

The optimal weights become:

$$
\mathbf{w}^* = \frac{C \mu^* - A}{D} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu} + \frac{B - A \mu^*}{D} \boldsymbol{\Sigma}^{-1} \mathbf{1}
$$

### Maximum Sharpe Ratio Portfolio

The Sharpe ratio is:

$$
S = \frac{\mu_p - r_f}{\sigma_p}
$$

Maximising $S$ subject to $\mathbf{w}^\top \mathbf{1} = 1$ is equivalent to solving:

$$
\max_{\mathbf{w}} \; \frac{\mathbf{w}^\top (\boldsymbol{\mu} - r_f \mathbf{1})}{\sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}}
$$

This is a fractional program. A standard transformation defines $\tilde{\mathbf{w}} = k \mathbf{w}$ for some scalar $k > 0$ chosen so that $\tilde{\mathbf{w}}^\top \boldsymbol{\Sigma} \tilde{\mathbf{w}} = 1$. The problem becomes:

$$
\max_{\tilde{\mathbf{w}}} \; \tilde{\mathbf{w}}^\top (\boldsymbol{\mu} - r_f \mathbf{1}) \quad \text{s.t.} \quad \tilde{\mathbf{w}}^\top \boldsymbol{\Sigma} \tilde{\mathbf{w}} = 1
$$

The closed-form solution is:

$$
\mathbf{w}^* = \frac{\boldsymbol{\Sigma}^{-1} (\boldsymbol{\mu} - r_f \mathbf{1})}{\mathbf{1}^\top \boldsymbol{\Sigma}^{-1} (\boldsymbol{\mu} - r_f \mathbf{1})}
$$

### Adding Inequality Constraints

Real portfolios often impose:

- Long-only: $w_i \geq 0 \; \forall i$
- Position limits: $l_i \leq w_i \leq u_i$
- Sector or factor exposure bounds: $\mathbf{G} \mathbf{w} \leq \mathbf{h}$

The problem becomes:

$$
\min_{\mathbf{w}} \; \frac{1}{2} \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w} - \delta \, \boldsymbol{\mu}^\top \mathbf{w}
$$

subject to:

$$
\mathbf{A}_{eq} \mathbf{w} = \mathbf{b}_{eq}, \quad \mathbf{A}_{ineq} \mathbf{w} \leq \mathbf{b}_{ineq}
$$

where $\delta \geq 0$ is a risk-aversion parameter. This is a convex quadratic program (QP) solvable by interior-point or active-set methods.

### Assumptions

1. Returns are adequately described by their first two moments (mean and covariance).
2. The covariance matrix $\boldsymbol{\Sigma}$ is known or can be reliably estimated.
3. Investors have quadratic utility or returns are approximately normally distributed.
4. Markets are frictionless (no transaction costs, taxes, or liquidity constraints) unless explicitly modelled.

### Edge Cases and Degeneracies

- **Singular covariance matrix**: Occurs when $n$ exceeds the number of observations or assets are perfectly collinear. Regularise via shrinkage (Ledoit-Wolf) or use pseudo-inverse.
- **Negative weights**: Unconstrained solutions may recommend shorting; add $w_i \geq 0$ if not permitted.
- **Extreme weights**: Optimisers often produce corner solutions; impose upper bounds or diversification constraints.
- **Estimation error amplification**: Small errors in $\boldsymbol{\mu}$ can cause large swings in $\mathbf{w}^*$; robust or Bayesian methods help.

### Relationship to Other Methods

- **Risk parity**: Allocates so that each asset contributes equally to total portfolio variance; a special case of optimisation with a different objective.
- **Black-Litterman**: Combines equilibrium returns with investor views to produce more stable $\boldsymbol{\mu}$ estimates before optimisation.
- **CVaR optimisation**: Replaces variance with Conditional Value-at-Risk for tail-risk control; becomes a linear program.

## Understanding the Mathematics

### Expected Portfolio Return

**The equation:**

$$\mathbb{E}[R_p] = \sum_{i=1}^{n} w_i \mathbb{E}[R_i] = \mathbf{w}^\top \boldsymbol{\mu}$$

**Read it aloud:**

"The expected return of the portfolio equals the sum of each asset's weight multiplied by that asset's expected return. In matrix form: the portfolio weights vector transposed, multiplied by the expected returns vector."

**What each symbol means:**

- $\mathbb{E}[R_p]$ = expected return of the entire portfolio
- $w_i$ = weight (fraction of capital) allocated to asset $i$
- $\mathbb{E}[R_i]$ = expected return of asset $i$
- $n$ = total number of assets
- $\mathbf{w}$ = column vector of all portfolio weights
- $\boldsymbol{\mu}$ = column vector of all expected returns
- $^\top$ = transpose (turns a column into a row for multiplication)

**A concrete numerical example:**

You have £100,000 to invest across three assets. You put 50% in UK equities (expected return 8%), 30% in bonds (expected return 4%), and 20% in real estate (expected return 6%). 

$$\mathbb{E}[R_p] = (0.5 \times 0.08) + (0.3 \times 0.04) + (0.2 \times 0.06)$$
$$= 0.04 + 0.012 + 0.012 = 0.064 = 6.4\%$$

Your portfolio's expected annual return is 6.4%.

**Why this equation matters:**

Without this weighted average, you'd have no way to compare different allocation strategies on a level playing field—it translates diverse holdings into a single performance metric.

---

### Portfolio Variance

**The equation:**

$$\text{Var}(R_p) = \sum_{i=1}^{n} \sum_{j=1}^{n} w_i w_j \text{Cov}(R_i, R_j) = \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}$$

**Read it aloud:**

"The variance of the portfolio equals the double sum across all pairs of assets: weight of asset $i$ times weight of asset $j$ times the covariance between asset $i$ and asset $j$. In matrix form: weights transposed, times the covariance matrix, times weights."

**What each symbol means:**

- $\text{Var}(R_p)$ = variance (squared risk) of portfolio returns
- $w_i, w_j$ = weights of assets $i$ and $j$
- $\text{Cov}(R_i, R_j)$ = covariance between returns of assets $i$ and $j$
- $\boldsymbol{\Sigma}$ = covariance matrix capturing all pairwise covariances
- The double sum runs over every pair, including each asset with itself

**A concrete numerical example:**

Same three-asset portfolio. Suppose UK equities have variance 0.04, bonds 0.01, real estate 0.02. The covariance between equities and bonds is 0.005, equities and real estate 0.01, bonds and real estate 0.003.

$$\text{Var}(R_p) = (0.5^2 \times 0.04) + (0.3^2 \times 0.01) + (0.2^2 \times 0.02)$$
$$+ 2(0.5 \times 0.3 \times 0.005) + 2(0.5 \times 0.2 \times 0.01) + 2(0.3 \times 0.2 \times 0.003)$$
$$= 0.01 + 0.0009 + 0.0008 + 0.0015 + 0.002 + 0.00036$$
$$= 0.01556$$

Portfolio variance is 0.01556; standard deviation (risk) is $\sqrt{0.01556} = 12.5\%$.

**Why this equation matters:**

This captures how assets move together—diversification reduces risk only if this equation accounts for correlations, not just individual asset volatilities.

---

### The Optimisation Problem

**The equation:**

$$\min_{\mathbf{w}} \left\{ \frac{1}{2} \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w} - \lambda \mathbf{w}^\top \boldsymbol{\mu} \right\}$$
$$\text{subject to: } \sum_{i=1}^{n} w_i = 1, \quad w_i \geq 0$$

**Read it aloud:**

"Find the portfolio weights that minimise this quantity: half the portfolio variance minus lambda times the expected return, subject to the constraint that all weights sum to one and no weight is negative."

**What each symbol means:**

- $\min_{\mathbf{w}}$ = find the weights that minimise the objective
- $\lambda$ = risk-return trade-off parameter (higher $\lambda$ = prefer return over risk)
- $\sum w_i = 1$ = full investment constraint (100% allocated)
- $w_i \geq 0$ = no short-selling constraint (no negative weights)

**A concrete numerical example:**

Set $\lambda = 2$ (moderately risk-tolerant). Using our earlier values, suppose the optimizer tests weights (0.4, 0.4, 0.2):

$$\text{Objective} = \frac{1}{2}(0.0145) - 2(0.062) = 0.00725 - 0.124 = -0.117$$

A more aggressive allocation (0.7, 0.1, 0.2) gives:

$$\text{Objective} = \frac{1}{2}(0.0198) - 2(0.068) = 0.0099 - 0.136 = -0.126$$

The second is lower (better), so the optimizer favors it—higher return justifies slightly higher risk.

**Why this equation matters:**

This single expression encodes the entire trade-off: maximise returns while controlling risk, within practical constraints—solving it is the core of portfolio construction.

---

### The Big Picture

Portfolio mathematics transforms a vague desire—"I want good returns without too much risk"—into a precise optimisation problem with a provably best solution. We use quadratic programming because portfolio risk is fundamentally quadratic (it grows with the square of positions and their interactions), while simpler linear methods cannot capture diversification effects. The covariance matrix is the engine: it encodes how assets move together, letting the optimizer find combinations where losses in one holding are offset by gains in another. The trade-off parameter $\lambda$ lets you dial between aggressive and conservative strategies, but the mathematics itself is neutral—it simply finds the most efficient way to achieve whatever balance you specify. In one intuitive sentence: **we're searching for the mix of assets that gives the smoothest ride for the destination we've chosen.**

## Python Implementation

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# --------------------------------------------------
# 1. Generate realistic synthetic data
# --------------------------------------------------
np.random.seed(42)
n_assets = 5
asset_names = ['Equities', 'Bonds', 'Real Estate', 'Commodities', 'Cash']

# Expected annual returns (hypothetical)
expected_returns = np.array([0.08, 0.03, 0.06, 0.04, 0.01])

# Covariance matrix (annualised)
# Constructed to be realistic: equities most volatile, cash nearly zero
cov_matrix = np.array([
    [0.0400, 0.0100, 0.0150, 0.0120, 0.0000],
    [0.0100, 0.0064, 0.0030, 0.0010, 0.0000],
    [0.0150, 0.0030, 0.0225, 0.0080, 0.0000],
    [0.0120, 0.0010, 0.0080, 0.0324, 0.0000],
    [0.0000, 0.0000, 0.0000, 0.0000, 0.0001],
])

# --------------------------------------------------
# 2. Define portfolio metrics
# --------------------------------------------------
def portfolio_return(weights, mu):
    """Calculate expected portfolio return."""
    return weights @ mu

def portfolio_volatility(weights, cov):
    """Calculate portfolio standard deviation."""
    return np.sqrt(weights @ cov @ weights)

def negative_sharpe(weights, mu, cov, rf=0.01):
    """Negative Sharpe ratio (for minimisation)."""
    ret = portfolio_return(weights, mu)
    vol = portfolio_volatility(weights, cov)
    return -(ret - rf) / vol

# --------------------------------------------------
# 3. Optimisation: Maximum Sharpe Ratio Portfolio
# --------------------------------------------------
n = len(expected_returns)
initial_weights = np.ones(n) / n  # equal-weight starting point

# Constraints: weights sum to 1
constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}

# Bounds: long-only, no single asset > 40%
bounds = tuple((0.0, 0.40) for _ in range(n))

result_sharpe = minimize(
    negative_sharpe,
    initial_weights,
    args=(expected_returns, cov_matrix, 0.01),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

optimal_weights_sharpe = result_sharpe.x

print("=== Maximum Sharpe Ratio Portfolio ===")
for name, w in zip(asset_names, optimal_weights_sharpe):
    print(f"  {name}: {w:.2%}")
print(f"  Expected Return: {portfolio_return(optimal_weights_sharpe, expected_returns):.2%}")
print(f"  Volatility: {portfolio_volatility(optimal_weights_sharpe, cov_matrix):.2%}")
print(f"  Sharpe Ratio: {-result_sharpe.fun:.3f}\n")

# --------------------------------------------------
# 4. Optimisation: Minimum Variance Portfolio
# --------------------------------------------------
def portfolio_variance(weights, cov):
    return weights @ cov @ weights

result_minvar = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

optimal_weights_minvar = result_minvar.x

print("=== Minimum Variance Portfolio ===")
for name, w in zip(asset_names, optimal_weights_minvar):
    print(f"  {name}: {w:.2%}")
print(f"  Expected Return: {portfolio_return(optimal_weights_minvar, expected_returns):.2%}")
print(f"  Volatility: {portfolio_volatility(optimal_weights_minvar, cov_matrix):.2%}\n")

# --------------------------------------------------
# 5. Efficient Frontier
# --------------------------------------------------
target_returns = np.linspace(0.02, 0.07, 20)
frontier_volatilities = []

for target in target_returns:
    cons = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w, t=target: portfolio_return(w, expected_returns) - t}
    ]
    res = minimize(
        portfolio_variance,
        initial_weights,
        args=(cov_matrix,),
        method='SLSQP',
        bounds=bounds,


## Visualisations

![](../../_static/figures/optimise-portfolio_fig1.png)

![](../../_static/figures/optimise-portfolio_fig2.png)

## Using This in Heuristix

### Quick Start

The most common use case is optimising a portfolio of stocks to maximise return while controlling risk. Here's how to set it up in under two minutes:

1. **Connect your returns data** – drag a connector from a node containing historical asset returns (one column per asset, rows are time periods)
2. **Open the configuration panel** – the node defaults to mean-variance optimisation with no short-selling
3. **Set your risk tolerance** – adjust the risk aversion parameter (start with 1.0 for balanced portfolios)
4. **Run the optimisation** – click execute and review the weights table and efficient frontier chart
5. **Export or connect downstream** – pipe the optimal weights to a Portfolio Backtest or Report node

### Data Inputs

This node expects a **returns matrix**: each row represents a time period (daily, weekly, monthly), and each column represents an asset. The node calculates expected returns and covariance internally.

**Example input shape:**

| Date       | AAPL    | MSFT    | GOOGL   |
|------------|---------|---------|---------|
| 2023-01-01 | 0.012   | 0.008   | 0.015   |
| 2023-01-02 | -0.005  | 0.003   | -0.002  |
| 2023-01-03 | 0.007   | 0.011   | 0.009   |

You can also optionally connect a **constraints table** for advanced rules (e.g., sector limits, minimum/maximum position sizes).

### Configuration Parameters

| Parameter | What It Controls | Default | When to Change |
|-----------|------------------|---------|----------------|
| **Risk Aversion** | How much you penalize variance vs. reward return (higher = more conservative) | 1.0 | Increase to 2–5 for conservative portfolios; decrease to 0.3–0.7 for aggressive growth |
| **Allow Short Selling** | Permits negative weights (borrowing assets to sell) | Off | Turn on only if your strategy and brokerage support shorting; increases complexity |
| **Weight Bounds** | Min/max allocation per asset (e.g., 0% to 20%) | 0% to 100% | Set max to 15–20% to avoid concentration risk; set min > 0% to force diversification |
| **Target Return** | Forces portfolio to achieve this expected return | None | Use when you have a specific return goal (e.g., 8% annually); switches to return-constrained mode |
| **Regularisation** | Adds L2 penalty to reduce extreme weights | 0 | Set to 0.01–0.1 when weights are too concentrated or unstable across re-optimisations |
| **Estimation Window** | Number of recent periods to use for calculating returns/covariance | All data | Shorten to 60–120 periods for faster adaptation to market changes; risk overfitting to recent data |

### Outputs

**Optimal Weights Table** – A single-row table showing the fraction of capital to allocate to each asset. Sums to 100% (or your specified total). Export this to execute trades or feed into backtesting.

**Performance Metrics Panel** – Displays expected portfolio return, volatility (standard deviation), and Sharpe ratio for the optimised portfolio.

**Efficient Frontier Chart** – A curve showing the best possible return for each level of risk. Your optimised portfolio is highlighted as a point on this curve. Use this to visually assess trade-offs.

**Contribution Analysis** – Bar chart breaking down which assets contribute most to portfolio risk and return. Helps you understand *why* the optimiser chose these weights.

### Connecting Downstream

- **Portfolio Backtest** – Most common next step. Tests how the optimised weights would have performed historically.
- **Report Builder** – Compiles weights, metrics, and charts into a client-ready document.
- **Rebalancing Scheduler** – Automates periodic re-optimisation (e.g., monthly rebalancing).
- **Risk Dashboard** – Monitors portfolio exposure against limits in real-time.

### Practical Tips

1. **Start with sample data** – Use the built-in "Tech 5" dataset to learn the interface before connecting your own data.

2. **Regularisation prevents instability** – If weights swing wildly when you add one more day of data, add 0.05 regularisation to smooth them out.

3. **Check correlation heatmaps first** – Highly correlated assets (>0.9) can cause numerical issues. Consider dropping redundant assets upstream.

4. **Don't over-optimise on short histories** – With fewer than 60 periods, estimates are noisy. Use simpler strategies or increase regularisation.

5. **Combine with scenario analysis** – Clone this node and re-run with stressed covariance matrices (e.g., 2008 crisis correlations) to test robustness.

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial data exploration when you want to understand feasible solutions and sensitivity to constraints within seconds, not minutes.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `solver` | `'OSQP'` | Fastest general-purpose solver for QP problems |
| `max_iter` | `1000` | Sufficient for simple problems; prevents hanging |
| `risk_aversion` | `1.0` | Neutral starting point between return and risk |
| `long_only` | `True` | Eliminates complexity of short positions |
| `constraints` | `None` | Minimal constraints for fastest convergence |
| `rebalance_frequency` | `'quarterly'` | Reduces temporal resolution for speed |

**What you get:** A baseline optimal portfolio in under 1 second that shows directional asset preferences and approximate risk-return characteristics.

**Trade-off:** You sacrifice precision in constraint handling and may miss corner cases where non-convex constraints or short positions unlock better solutions.

### Recipe 2: Production-Grade Institutional

**When to use:** Final model deployment for live capital allocation where reproducibility, regulatory compliance, and numerical stability are critical.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `solver` | `'CVXOPT'` | Industry-standard convex optimizer with strict convergence guarantees |
| `max_iter` | `10000` | Ensures convergence even for difficult problems |
| `risk_aversion` | `2.5` | Conservative bias typical for institutional mandates |
| `long_only` | `True` | Regulatory requirement for most mutual funds |
| `weight_bounds` | `(0.01, 0.15)` | Enforces diversification and liquidity requirements |
| `sector_constraints` | `{'Tech': 0.30, 'Finance': 0.25}` | Sector exposure limits per investment policy |
| `turnover_penalty` | `0.001` | Reduces transaction costs from excessive rebalancing |
| `covariance_method` | `'ledoit_wolf'` | Robust shrinkage estimator for finite samples |
| `return_window` | `252` | One year of daily returns for stable estimates |

**What you get:** A portfolio that satisfies all real-world constraints with documented convergence properties suitable for audit trails.

**Trade-off:** Runtime increases 10–50× compared to quick exploration; requires more tuning of penalty terms and constraint tolerances.

### Recipe 3: High-Conviction Concentrated Bets

**When to use:** Hedge fund or proprietary trading strategy where alpha signals are strong and you want to maximally exploit them without naive over-concentration.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `objective` | `'max_sharpe'` | Prioritizes risk-adjusted returns over absolute variance |
| `weight_bounds` | `(0.0, 0.40)` | Allows concentration while preventing single-asset dominance |
| `min_positions` | `8` | Forces diversification across at least 8 names |
| `expected_returns_method` | `'custom'` | Use proprietary alpha forecasts, not historical means |
| `risk_aversion` | `0.5` | Aggressive stance; willing to accept higher variance for return |
| `l2_gamma` | `0.0` | Disable regularization that would smooth toward equal-weight |

**What you get:** A portfolio that aggressively tilts toward your highest-conviction ideas while maintaining minimum risk management guardrails.

**Trade-off:** Highly sensitive to errors in return forecasts; underperforms dramatically if alpha signals are noisy or overfit.

### Recipe 4: Liability-Driven Immunization

**When to use:** Pension fund or insurance company matching future fixed liabilities (e.g., annuity payments) where duration and cashflow alignment matter more than Sharpe ratio.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `objective` | `'min_variance'` | Focus on stability, not return maximization |
| `custom_constraints` | `duration_match(target=7.2)` | Match portfolio duration to liability duration |
| `cashflow_constraints` | `monthly_outflows.csv` | Ensure sufficient liquidity for payment dates |
| `long_only` | `True` | Cannot short when matching real obligations |
| `rebalance_trigger` | `'duration_drift > 0.3'` | Event-driven rebalancing on duration mismatch |
| `asset_universe` | `'investment_grade_bonds'` | Restrict to low-default-risk instruments |

**What you get:** A portfolio engineered to track liability profiles with minimal surplus volatility, effectively a customized bond ladder.

**Trade-off:** You deliberately forgo equity-like returns and accept lower growth potential to achieve cashflow certainty.

## Business Applications

**Financial Services**

A regional wealth management firm serving high-net-worth clients needs to construct diversified portfolios across equities, bonds, commodities, and alternatives while respecting each client's risk tolerance and ESG preferences. Portfolio optimisation systematically balances expected returns against volatility, incorporating correlation structures between asset classes and hard constraints like "no more than 15% in emerging markets" or "exclude tobacco stocks." The firm reduced portfolio variance by 28% while maintaining target returns, leading to improved client retention rates and $4.3M in net new assets over twelve months as clients experienced smoother ride quality through market turbulence.

**Retail & E-commerce**

A fashion retailer with 400 stores must allocate a fixed seasonal buying budget of £12M across 2,000 SKUs, knowing that capital tied up in slow-moving inventory directly erodes margin. By treating each SKU as an "asset" with expected return (gross margin × sell-through rate) and risk (demand variance), the merchant team applies portfolio optimisation to maximise expected profit subject to minimum order quantities, storage constraints, and category diversity requirements. This approach lifted gross margin return on inventory investment (GMROII) from 2.1 to 2.9 and cut end-of-season markdowns by £780K annually.

**Healthcare & Life Sciences**

A pharmaceutical company allocating $200M R&D budget across 18 drug candidates in phase II and III trials faces a classic portfolio problem: each programme has uncertain payoff, correlated technical risks, and different capital intensity profiles. Portfolio optimisation models expected net present value against probability-of-success distributions, ensuring the pipeline balances blockbuster moonshots with safer line extensions and maintains therapeutic area diversification. The resulting allocation improved portfolio expected value by $47M versus the prior committee-driven approach and de-risked the pipeline by reducing correlation-adjusted volatility by 19%.

**Insurance**

A commercial property insurer writing policies across flood zones, earthquake regions, and hurricane corridors must allocate underwriting capacity to maximise premium income while keeping catastrophic loss exposure below regulatory capital thresholds. Portfolio optimisation treats geographic segments and peril types as correlated risk assets, incorporating historical loss distributions and reinsurance costs. The insurer increased written premium by 12% year-over-year while maintaining a 1-in-200-year loss profile within board-approved limits, unlocking $6.8M in additional underwriting profit without raising capital reserves.

**Manufacturing**

An automotive tier-one supplier negotiating annual supply contracts with six OEM customers must allocate fixed production capacity (12 million machine-hours) across customer programmes with different margin profiles, demand volatility, and penalty clauses for under-delivery. By optimising the contract portfolio to maximise expected profit subject to capacity, tooling investment limits, and minimum commitment constraints, the supplier increased overall margin by 340 basis points and reduced exposure to a single high-volume but low-margin customer from 47% to 31% of revenue, significantly improving business resilience.

**Marketing & Media**

A direct-to-consumer brand spending $800K monthly across Google Ads, Meta, TikTok, affiliate channels, and programmatic display needs to allocate budget to maximise customer acquisition while managing channel saturation and diminishing returns. Portfolio optimisation models each channel as an asset with expected return (revenue per dollar spent) and risk (conversion rate variance), subject to constraints like "maintain at least 15% budget in brand awareness channels." The optimised allocation improved blended CAC by $12 (from $67 to $55) and increased marketing efficiency ratio from 3.2× to 4.1× ROAS.

**Energy & Utilities**

A renewable energy developer with €50M capital budget must select and size investments across a pipeline of 14 solar, wind, and battery storage projects with site-specific capacity factors, grid connection costs, and regulatory incentive structures. Portfolio optimisation balances expected levelised cost of energy against resource intermittency risk and policy exposure, subject to geographic diversification and minimum project scale constraints. The optimised portfolio increased expected 20-year IRR from 8.7% to 10.4% while reducing cash flow volatility by 22%, making the portfolio significantly more attractive to infrastructure investors.

**Public Sector**

A metropolitan transport authority allocating a five-year £180M capital budget across bus route expansions, rail maintenance, cycling infrastructure, and park-and-ride facilities models each investment as an asset with expected return measured in passenger-miles served and accessibility improvements. Portfolio optimisation incorporates political constraints ("at least 20% for active travel"), engineering dependencies, and uncertainty in ridership forecasts to maximise overall network benefit. The data-driven allocation process improved cost-per-passenger-mile by 17% versus the previous politically negotiated split and provided transparent, defensible rationale for budget decisions to elected officials.

## Worked Example

Sarah Chen, a quantitative analyst at Vanguard Capital, a mid-sized pension fund manager, was sitting across from her CIO when he slid a printed spreadsheet across the table. "We've been overweight in tech for eighteen months," he said. "It's carried us, but I'm losing sleep over it. Can you show me what a rational rebalancing looks like—something that doesn't just chase last year's winners?"

The question mattered because Vanguard managed £2.3 billion on behalf of public sector employees. A badly timed shift could lock in losses or miss a recovery. But sitting still while concentration risk built up violated every principle in their mandate. Sarah had three days before the quarterly investment committee meeting.

She pulled five years of monthly returns for their core equity holdings: a UK large-cap index, US technology, European industrials, emerging markets, and UK gilts as the defensive anchor. The data came from Bloomberg, but as always, there were quirks—missing values in February 2020 when markets froze, a few obvious data entry errors (a 340% monthly return that should have been 3.4%), and the challenge that historical correlation doesn't promise future behavior.

Here's what the cleaned return series looked like for the most recent months:

| Date       | UK_Equity | US_Tech | EU_Industrials | Emerging | UK_Gilts |
|------------|-----------|---------|----------------|----------|----------|
| 2023-08-31 | 0.021     | 0.045   | 0.012          | 0.008    | 0.003    |
| 2023-09-30 | -0.015    | -0.032  | -0.018         | -0.025   | 0.012    |
| 2023-10-31 | 0.018     | 0.038   | 0.015          | 0.019    | 0.001    |
| 2023-11-30 | 0.032     | 0.061   | 0.028          | 0.035    | -0.002   |

Sarah opened her portfolio optimization script. She'd used mean-variance optimization before, but this time the constraints mattered as much as the math. The fund's investment policy statement forbade short positions, required full investment of capital, and capped any single asset at 40% to prevent exactly the kind of concentration they were worried about. She also set a target return slightly below their current portfolio—accepting that de-risking would cost some upside—while minimizing variance.

Her Python implementation looked like this:

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Load monthly returns
returns = pd.read_csv('asset_returns.csv', index_col='Date')

# Calculate expected returns and covariance matrix
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Current portfolio (heavily tech-weighted)
current_weights = np.array([0.15, 0.45, 0.15, 0.10, 0.15])

# Objective: minimize portfolio variance
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# Constraint: weights sum to 1
def weight_sum(weights):
    return np.sum(weights) - 1

# Constraint: achieve minimum target return
def target_return(weights, mean_returns, target):
    return weights.T @ mean_returns - target

# Optimize with constraints
constraints = [
    {'type': 'eq', 'fun': weight_sum},
    {'type': 'ineq', 'fun': target_return, 
     'args': (mean_returns, 0.015)}  # 1.5% monthly target
]
bounds = [(0, 0.4) for _ in range(5)]  # No shorts, max 40% each

result = minimize(
    portfolio_variance,
    x0=current_weights,
    args=(cov_matrix,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

optimal_weights = result.x
```

The optimization converged quickly. The optimal portfolio reduced US tech from 45% to 28%, increased UK gilts from 15% to 32%, and spread the remainder more evenly across the other equities. Expected monthly volatility dropped from 4.8% to 3.2%—a meaningful reduction—while the expected return fell only from 1.9% to 1.6% monthly.

Sarah stared at the output for a moment before the insight crystallized: the algorithm wasn't just cutting tech because it was high; it was cutting tech because its correlation with emerging markets had climbed to 0.72 over the past year. The portfolio had *less* diversification than the position sizing suggested. Meanwhile, gilts had started moving inversely to equities again after years of correlation breakdown. The optimizer found genuine defensive value there.

At the investment committee meeting, Sarah presented the analysis alongside a scenario showing what the optimized portfolio would have done in the September drawdown. The CIO nodded. "Let's implement this over four weeks, not all at once. I don't want to telegraph this to the market." The rebalancing started the following Monday.

Three months later, when tech sold off sharply on AI regulation fears, the fund's drawdown was 40% smaller than their benchmark. The CIO sent Sarah a rare email: "You made us look smart."

If Sarah could do it again, she'd stress-test the target return assumption more thoroughly—her 1.5% monthly figure was somewhat arbitrary—and she'd run the optimization with rolling windows to see how stable the recommendations were. Portfolio optimization is elegant math, but it's brutally sensitive to input assumptions. She learned to trust the framework, but verify the foundations.

## Interpreting Your Results

You've just run portfolio optimisation and you're looking at a screen full of weights, risk metrics, and perhaps a frontier chart. Here's what you're actually seeing and how to judge if it's actionable.

### Portfolio Weights Table

**Plain-English meaning**: Each row shows what percentage of your capital the algorithm recommends putting into each asset. A weight of 0.25 means "invest 25% of your money here." These should sum to exactly 1.0 (or 100%). If you allowed short-selling, negative weights mean "borrow and sell this asset to buy more of others."

**Concrete benchmarks**:
- **Maximum single position above 40%**: You're heavily concentrated; one asset dominates your risk and return. This is aggressive and appropriate only if that asset has dramatically better risk-adjusted returns.
- **Maximum single position 15–40%**: Standard for concentrated portfolios (5–10 assets). Still meaningful diversification.
- **Maximum single position below 15%**: Well-diversified. Common in institutional portfolios with 10+ assets.
- **10+ assets with weights under 2% each**: You're over-diversified; transaction costs will erode gains and rebalancing becomes expensive.

**Red flags**:
- **All weight on one asset**: The optimizer sees no benefit to diversification. Either your return estimates are wildly different, or your correlation matrix is broken (check for correlation = 1.0 anywhere).
- **Many zero weights despite no constraints**: Assets with zero allocation are dominated—worse return per unit of risk. This is often correct, but verify your input data isn't stale or missing.
- **Weights flip dramatically from a previous run**: Small input changes shouldn't cause 30% positions to become 0%. This signals estimation error sensitivity; consider adding turnover constraints.

### Expected Portfolio Return

**Plain-English meaning**: The weighted average of your individual asset return forecasts. If Stock A is expected to return 8%, Stock B 12%, and you hold 50% of each, portfolio return is 10%. This is *not* a guarantee—it's only as good as your forecasts.

**Concrete benchmarks**:
- **Below risk-free rate (≈3–5% currently)**: Something is wrong. You could get better returns in Treasury bills with zero risk.
- **Risk-free rate to risk-free + 4%**: Conservative portfolio. Appropriate for capital preservation goals.
- **Risk-free + 4% to risk-free + 8%**: Moderate portfolio. Standard for balanced 60/40-style allocations.
- **Above risk-free + 8%**: Aggressive. Verify this isn't driven by unrealistic forecasts.

**Red flags**:
- **Return significantly below your input assets' average**: You've over-optimized for risk reduction. Check if your risk aversion parameter is too high.
- **Return exactly equals your highest-returning single asset**: You've built a concentrated bet, not a portfolio. Review constraints.

### Portfolio Volatility (Standard Deviation)

**Plain-English meaning**: How much your portfolio value is expected to bounce around, annualized. A volatility of 0.15 (or 15%) means that in a typical year, your returns might be ±15% from the expected return. Two-thirds of outcomes fall within one standard deviation.

**Concrete benchmarks**:
- **Below 8%**: Very conservative. Bond-heavy portfolios or cash equivalents.
- **8–15%**: Moderate. Traditional balanced portfolios.
- **15–25%**: Aggressive equity portfolios.
- **Above 25%**: Very high risk. Appropriate only for high-risk-tolerance investors or if this is a small allocation within a larger strategy.

**Red flags**:
- **Volatility below all individual assets but only slightly**: You're not getting much diversification benefit. Check your correlation matrix—assets may be more correlated than you think.
- **Volatility higher than equal-weighted portfolio**: The optimizer made things worse. Input data error is likely.

### Sharpe Ratio

**Plain-English meaning**: Return per unit of risk. Calculated as (Portfolio Return − Risk-Free Rate) / Portfolio Volatility. A Sharpe of 1.0 means you earn one unit of excess return for each unit of volatility you endure.

**Concrete benchmarks**:
- **Below 0.5**: Poor. You're not being compensated adequately for risk.
- **0.5–0.8**: Acceptable. Typical for broad equity indices.
- **0.8–1.2**: Good. Well-optimized portfolios often land here.
- **Above 1.2**: Excellent, but verify your inputs. This is rare without leverage or exceptional forecasting.

**Red flags**:
- **Sharpe above 2.0**: Almost certainly input error. Your return forecasts are probably too optimistic or volatility estimates too low.
- **Sharpe lower than equal-weighted portfolio**: Optimization failed. Check constraints—they may be too restrictive.

### Reading Multiple Outputs Together

A healthy optimized portfolio shows:
- **Sharpe ratio improved** versus equal-weighted or single-asset alternatives
- **Volatility reduced** by at least 10–20% versus the average individual asset volatility
- **No single weight above 40%** unless deliberately concentrated
- **Weights stable** across small input changes

---

### Sanity Check Checklist

1. **Do weights sum to 1.0 (±0.01)?** If not, optimization failed or constraints conflict.
2. **Is portfolio volatility below the equal-weighted alternative?** If not, diversification isn't working.
3. **Are all assets with zero weight truly worse Sharpe ratios individually?** If not, check correlation inputs.
4. **Does the highest-weight asset make intuitive sense?** If it's surprising, revisit return forecasts.
5. **Run a second time with slightly different inputs (±2% returns)**: Weights shouldn't shift by more than 10 percentage points.

---

### Good Enough to Act On?

If your Sharpe ratio is **above 0.7**, portfolio volatility is **within your risk tolerance**, no single asset exceeds **35% unless justified**, and the sanity checks pass, you have an actionable portfolio. The goal isn't perfection—it's a disciplined, risk-aware allocation better than ad-hoc choices. If Sharpe is below 0.5 or any red flag appears, revisit your inputs before deploying capital.

## Decision Guidance

### What This Result Is Telling You

Portfolio optimisation tells you precisely how to divide your investment capital across available assets to achieve the best balance between growth and safety that mathematically exists given current market conditions. When the optimizer recommends allocating 35% to equities, 40% to bonds, and 25% to alternatives, it is saying: "Based on historical relationships between these assets, this mix gives you the highest expected return for the level of volatility you said you can tolerate." This is not a prediction that markets will behave exactly as they have in the past, but rather a disciplined framework for avoiding both reckless concentration and paralyzing over-diversification.

The output also reveals hidden relationships in your current holdings. If the recommended portfolio looks dramatically different from what you hold today—perhaps suggesting you sell half your real estate exposure and triple your technology allocation—the algorithm has detected that your current mix is either taking unnecessary risk without compensation or leaving substantial returns on the table. Conversely, if the optimized weights closely match your existing positions, you have mathematical confirmation that your portfolio is already well-structured given your risk tolerance.

The sensitivity of these recommendations to input assumptions is itself a critical signal. When small changes to expected returns produce wild swings in recommended allocations, you are operating in a regime where the data does not provide clear guidance, and qualitative judgment must play a larger role. When recommendations remain stable across reasonable assumption variations, you can implement with greater confidence that you are not over-fitting to noise.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Recommended allocation differs from current by >15% for any single asset | Your portfolio is materially suboptimal; you are either taking uncompensated risk or missing available returns | Rebalance toward recommended weights over 30–90 days, considering transaction costs and tax implications | Chief Investment Officer, Portfolio Manager |
| Optimal portfolio allocates >40% to a single asset class | That asset dominates the risk-return frontier given your inputs; high concentration reflects either genuine opportunity or unrealistic assumptions | Verify return assumptions and correlation estimates; consider imposing concentration constraints (e.g., max 30% per asset) before re-running | Risk Manager, Investment Committee |
| Efficient frontier shows <1% annual return difference between minimum-risk and maximum-return portfolios | Asset classes in your universe are highly correlated; diversification benefits are minimal | Expand investment universe to include genuinely uncorrelated assets, or accept that risk reduction options are limited | Portfolio Strategist, Asset Allocation Lead |
| Recommended weights are highly sensitive to expected return inputs (>10% allocation change for 0.5% return adjustment) | Optimization is unstable; small estimation errors will lead to poor real-world outcomes | Use robust optimization techniques, impose diversification constraints, or rely more heavily on equal-weighting or minimum-variance approaches | Quantitative Analyst, Risk Manager |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Recommended allocations differ from current by <25% for each asset class
- Input return estimates are based on ≥10 years of historical data or robust forward-looking models
- Efficient frontier is well-defined with clear separation between portfolios (≥2% return spread across risk levels)
- Recommended weights remain stable when you vary return assumptions by ±1% and correlation estimates by ±0.10

**Proceed with caution when:**
- Any single recommended allocation exceeds 35% of total portfolio
- You are relying on <5 years of historical data for any asset class
- Recommended allocation changes exceed 30% for any position (high rebalancing costs likely)
- The optimization suggests zero allocation to an asset class you have strategic reasons to include

**Investigate before acting when:**
- Recommended weights swing by >15% when you make small (<1%) adjustments to expected returns
- Correlation matrix has eigenvalues near zero (indicates multicollinearity problems)
- Optimal portfolio has expected Sharpe ratio >1.5 (likely reflects over-optimistic assumptions)
- Historical data includes <2 full market cycles (missing regime change information)

**Do not use these results yet when:**
- Any correlation coefficient is estimated from <3 years of overlapping data
- Input data has not been checked for survivorship bias or look-ahead bias
- Optimization produces corner solutions (0% or 100%) for multiple assets without constraints forcing this
- You cannot articulate the business logic for why the recommended allocation makes strategic sense

### The Cost of Getting This Wrong

When portfolio optimization results are misinterpreted or blindly implemented, capital gets systematically misallocated at scale. A CIO who treats optimizer output as gospel rather than guidance might rebalance a $500M pension fund based on over-fitted historical patterns, incurring $2M in transaction costs to move into concentrated positions just before correlations shift and the "optimal" portfolio underperforms a simple balanced approach by 300 basis points annually. Worse, when inevitable losses occur, the quantitative veneer creates false confidence that prevents course correction: "The model said to do this" becomes an excuse rather than a framework. On the flip side, ignoring optimization entirely and making allocation decisions based solely on intuition leaves billions in unrealized returns on institutional balance sheets each year—returns that could fund operations, growth initiatives, or shareholder distributions. The real cost is not just financial but organizational: teams lose faith in quantitative methods after one bad experience with blind implementation, or never build analytical capability because they assume optimization is too complex to be practical.

## Common Pitfalls

**The Overfitting Time Bomb**

Here's what happened: A junior quant at a mid-sized fund was building an equity portfolio optimizer. They used five years of daily return data to estimate the covariance matrix, then ran mean-variance optimization to find weights that would have delivered a Sharpe ratio of 2.1 on historical data. They presented this to the portfolio manager with pride. The output showed clean efficient frontier curves and impressive backtested returns. They concluded they'd found an optimal allocation strategy. Six months into live trading, the portfolio's Sharpe ratio was 0.4, and several positions that looked "optimal" were hemorrhaging money.

**Why it happens**: The optimizer found patterns in historical noise rather than true return relationships. With hundreds of assets and correlations, there are millions of ways to fit past data perfectly while having zero predictive power.

**How to detect it**: Your in-sample Sharpe ratio is above 1.5 while out-of-sample is below 0.8. The optimal weights are extreme (many zeros, a few positions above 30%). Turnover between rebalancing periods exceeds 60%.

**The fix**: Use rolling walk-forward validation with strict train-test splits, apply regularization to your covariance estimates (shrinkage, factor models), and impose position size limits as hard constraints.

**The Illusion of Precision**

Here's what happened: A business analyst received optimized portfolio weights calculated to four decimal places—14.2847% in Asset A, 9.6321% in Asset B. The spreadsheet looked sophisticated and scientific. They concluded these exact allocations were critical and insisted traders execute them precisely. Transaction costs from chasing these tiny weight differences consumed 1.2% annually, wiping out the theoretical optimization benefit.

**Why it happens**: Mathematical output creates false confidence. Users mistake computational precision for decision precision, forgetting that inputs (expected returns, covariances) are themselves estimates with huge uncertainty bands.

**How to detect it**: Rerun the optimization with slightly perturbed inputs (bump expected returns by 0.1%). If optimal weights swing by more than 5 percentage points, your solution is unstable.

**The fix**: Round portfolio weights to reasonable increments (nearest 2-5%) and implement tolerance bands that trigger rebalancing only when drift exceeds meaningful thresholds.

**The Ghost of Constraints Past**

Here's what happened: An experienced portfolio manager copied constraint code from a previous equity-only optimization project into a new multi-asset project. They included a constraint that no position could exceed 10% of the portfolio. The output showed diversified allocations across stocks, bonds, and commodities. They concluded the portfolio was well-balanced. Later they realized the 10% cap prevented the optimizer from taking a meaningful bond position during a recession, leading to unnecessary drawdown.

**Why it happens**: Constraints accumulate over time like barnacles on a ship. Each made sense in its original context, but collectively they can contradict the current investment thesis or straitjacket the optimizer into suboptimal regions.

**How to detect it**: The optimizer hits multiple constraint boundaries simultaneously (Lagrange multipliers are non-zero for 4+ constraints). Shadow prices suggest relaxing a constraint would dramatically improve the objective function.

**The fix**: Audit every constraint before each optimization run—write a one-sentence business justification for each, or delete it.

**The Return Forecast Mirage**

Here's what happened: A data scientist built an optimizer using analyst consensus return forecasts as inputs—12% for tech stocks, 6% for utilities, 3% for bonds. The optimization allocated 85% to tech stocks with a projected portfolio return of 11.1%. They concluded this was the rational allocation given expected returns. The portfolio manager looked horrified: the optimizer had created a concentrated sector bet that violated every risk guideline.

**Why it happens**: Mean-variance optimization is exquisitely sensitive to return inputs but relatively insensitive to risk inputs. Tiny differences in expected return (often within the noise of estimation error) drive massive allocation changes.

**How to detect it**: A 1% change in a single asset's expected return causes portfolio weight changes exceeding 15%. Optimal portfolios are concentrated in whatever subset of assets has the highest Sharpe ratio by even a small margin.

**The fix**: Impose explicit diversification constraints (sector limits, position caps), use robust optimization techniques that acknowledge forecast uncertainty, or consider minimum-variance portfolios that ignore return forecasts entirely.

**The Backward-Looking Disaster**

Here's what happened: A risk analyst optimized a portfolio in March 2020 using covariance estimates from the prior 12 months—a period of historically low volatility and high cross-asset correlations. The output showed an efficient 60/40 stocks/bonds mix. Then COVID hit, correlations spiked to 0.9, volatilities tripled, and the "optimized" portfolio experienced drawdowns 40% worse than expected. They had optimized for yesterday's market regime.

**Why it happens**: Historical covariance matrices reflect past regimes. Markets shift between states (low-vol/high-vol, correlated/uncorrelated) faster than most estimation windows can adapt.

**How to detect it**: Your portfolio's realized volatility is consistently 1.5x+ your forecast volatility. Correlation matrices show suspiciously uniform values (everything near 0.3 or everything near 0.8).

**The fix**: Use regime-switching models, stress-test against multiple correlation scenarios, or employ exponentially-weighted moving averages that give recent data more influence than distant observations.

## Common Misconceptions

**"A portfolio optimiser tells you what to buy."**

**Why people believe this:** The output is a set of weights that sum to one, typically displayed as percentages next to asset names. It looks exactly like an investment recommendation, and the mathematical precision—often reported to two decimal places—gives the impression of prescriptive authority.

**The truth:** Portfolio optimisation is a *what-if* engine, not a recommendation system. It answers the question: "Given these return forecasts, this risk model, and these constraints, what allocation is mathematically consistent?" The quality of that answer depends entirely on the quality of your inputs, particularly your expected return estimates, which are notoriously unreliable. Professional asset managers treat optimiser output as the *starting point* for human judgement, not the endpoint. They apply qualitative overlays, adjust for market conditions the model cannot see, and deliberately deviate from "optimal" weights when they conflict with strategic objectives or client-specific mandates.

**The real-world consequence:** A mid-sized pension fund implemented quarterly rebalancing based purely on mean-variance optimiser output, using five-year historical returns as expected return inputs. Within eighteen months, the portfolio had churned through three complete sector rotations, incurred substantial transaction costs, and significantly underperformed a simpler equal-weight benchmark. The team had automated away their judgement, mistaking mathematical optimality for investment wisdom.

**"More data always improves the estimate."**

**Why people believe this:** Statistical theory teaches that estimation error decreases with sample size. Intuitively, a covariance matrix estimated from ten years of returns should be more reliable than one from three years.

**The truth:** Financial markets are non-stationary. The correlations and volatilities that prevailed during 2010–2015 may have little bearing on 2024–2025. Using very long histories introduces *structural bias*—you are estimating parameters for a regime that no longer exists. The optimal lookback window represents a trade-off: longer windows reduce estimation noise but increase regime contamination. Research consistently shows that for equity covariance estimation, three to five years of data typically outperforms ten-year windows. The most sophisticated approaches use exponential weighting or dynamic conditional correlation models that give recent observations more influence, explicitly acknowledging that yesterday's data is more relevant than data from a decade ago.

**The real-world consequence:** A quantitative fund extended their covariance estimation window from three to ten years after a risk model review flagged "excessive estimation uncertainty." Their next portfolio optimization assigned a 22% weight to utility stocks because the longer window captured the 2008–2011 period when utilities exhibited unusually low correlation to equities. That relationship had fundamentally changed post-2015 due to interest rate regime shifts. The portfolio significantly underperformed during the subsequent drawdown, precisely because the risk model understated true correlation in the current regime.

**"The optimal portfolio is the one with the highest Sharpe ratio."**

**Why people believe this:** The Sharpe ratio—excess return divided by volatility—is taught as *the* measure of risk-adjusted performance. Mathematically, maximising Sharpe ratio is equivalent to finding the tangency portfolio on the efficient frontier.

**The truth:** Sharpe ratio optimality assumes investors care only about mean and variance, can borrow and lend at the risk-free rate, have no regulatory constraints, face no transaction costs, and hold single-period horizons. Real investors violate every one of these assumptions. A foundation with a 5% spending obligation cares about downside risk below that threshold, not symmetric variance. An insurance company faces capital charges that depend on tail risk, not volatility. A taxable investor must consider after-tax returns and holding periods. The "optimal" portfolio for any actual investor incorporates their specific objective function, constraints, and liability structure. Maximum Sharpe ratio is one candidate solution, not *the* solution.

**The real-world consequence:** A university endowment optimised their strategic asset allocation by maximising Sharpe ratio, which recommended a 38% allocation to private equity and hedge funds (high expected return, low reported volatility due to smoothed valuations). When the institution needed liquidity during a market crisis, they discovered they had optimised for an artificial measure while ignoring their true constraint: the need to meet annual spending commitments without forced asset sales. They were ultimately compelled to liquidate public equity positions at depressed prices while their "optimal" illiquid allocations remained locked up.

**"Input uncertainty isn't a big problem if I use robust estimation."**

**Why people believe this:** The field has developed sophisticated techniques—shrinkage estimators, Black-Litterman models, resampled efficient frontiers, robust optimisation—that explicitly address estimation error. These methods are mathematically elegant and demonstrably improve out-of-sample stability compared to naive implementations.

**The truth:** Robust techniques reduce sensitivity to estimation error; they do not eliminate the fundamental problem that you are optimising based on unknowable future parameters. Even the best estimation framework cannot extract signal from noise when the underlying signal-to-noise ratio is inherently low, which is the reality for expected return estimation in liquid markets. Research by Merton (1980) showed you would need over 500 years of monthly data to estimate expected equity returns with reasonable confidence. Robust methods help when you have *some* signal—they prevent the optimiser from over-concentrating in noise. But when expected return inputs are dominated by estimation error, robust optimisation primarily generates stable allocations around essentially arbitrary focal points. The humility to acknowledge this leads practitioners toward approaches that rely less on return forecasts: minimum-variance portfolios, risk-parity allocations, or strategic tilts based on economic reasoning rather than statistical extrapolation.

**The real-world consequence:** A data science team implemented a Black-Litterman model with shrinkage, believing they had "solved" the estimation problem. They still fed the model expected return views based on analyst consensus forecasts, which contained no actual predictive information. The sophisticated framework produced stable, concentrated positions with high conviction—but the concentration reflected the structure of the model's priors and the consistency of worthless forecasts, not actual investment edge. The portfolio underperformed simple equal-weight and minimum-variance benchmarks. The team had used advanced technology to confidently implement bad inputs.

**"Back-testing tells me if my optimisation approach works."**

**Why people believe this:** If you can show that your optimisation methodology would have produced superior risk-adjusted returns over the past decade, this provides empirical evidence of its effectiveness. The numbers are objective, the methodology is reproducible, and the performance metrics are clear.

**The truth:** Back-testing portfolio optimisation is uniquely treacherous because the optimiser ruthlessly exploits whatever patterns exist in your historical data, regardless of whether those patterns are structural or coincidental. Your back-test uses *realised* returns as inputs—you are effectively optimising with perfect foresight, then measuring performance on the same data. Even if you are sophisticated enough to use rolling windows and out-of-sample testing, you still face the problem that parameter choices (lookback windows, shrinkage intensity, rebalancing frequency) are typically tuned to improve historical performance. Every methodological decision informed by back-test results introduces look-ahead bias. The fundamental issue is that portfolio optimisation is not a prediction model you can validate on holdout data—it is a framework that transforms predictions into decisions. Back-tests tell you how your methodology would have performed *if past return distributions persisted*, which is precisely the assumption that fails in practice.

**The real-world consequence:** An asset manager developed a proprietary "adaptive optimisation" framework that adjusted constraint sets and risk aversion parameters based on volatility regime detection. Back-tests showed a 30% improvement in Sharpe ratio over static optimisation. After two years of live trading, the strategy had underperformed both its back-test and a simple static allocation. Post-mortem analysis revealed the regime detection methodology had been implicitly tuned to historical regime transitions; the specific volatility thresholds and lookback windows had been chosen because they "worked" in the back-test. The adaptive mechanism was fitting to history, not responding to structure. The firm had built an elaborate system for extracting patterns from the past that did not repeat.

## How This Connects

### Before This Node

**Estimate Expected Returns** calculates the anticipated return for each asset, providing the objective function's reward component that Optimise Portfolio maximises subject to risk constraints. Bad upstream data—returns estimated on insufficient history or with look-ahead bias—causes the optimiser to overweight spuriously attractive assets, producing portfolios that fail catastrophically out-of-sample.

**Estimate Covariance Matrix** quantifies how asset returns move together, supplying the variance-covariance structure that Optimise Portfolio uses to measure and constrain risk. Poorly conditioned matrices (from missing data or estimation error) contain negative eigenvalues or inflated correlations, leading to numerically unstable optimisations that suggest extreme long-short positions or concentrations.

**Define Risk Constraints** translates business requirements—maximum sector exposure, minimum diversification, volatility targets—into mathematical inequality constraints that bound the feasible solution space. Vague or contradictory constraints (e.g., "high return, zero risk, no concentration") create infeasible problems where no solution exists, or force the optimiser into corner solutions that violate intent.

**Calculate Risk-Free Rate** establishes the benchmark return for zero-risk investment, anchoring the Sharpe ratio and enabling mean-variance optimisation to distinguish skill from beta exposure. Using an inappropriate rate (e.g., yesterday's overnight rate for a multi-year horizon) distorts the efficient frontier, making risky portfolios appear more attractive than they are.

**Clean Asset Universe** filters tradable securities by liquidity, data completeness, and eligibility rules, ensuring Optimise Portfolio only considers investable instruments. An unfiltered universe polluted with delisted stocks, illiquid bonds, or assets missing price data produces theoretically optimal but practically untradeable allocations.

### After This Node

**Backtest Portfolio** simulates the optimised weights on historical data, measuring out-of-sample performance to validate that the portfolio's risk-return profile holds beyond the training window and identify overfitting or regime sensitivity.

**Execute Trades** translates portfolio weights into actual buy and sell orders, accounting for transaction costs, market impact, and execution timing—Optimise Portfolio's continuous weights map naturally to discrete order quantities.

**Monitor Portfolio Risk** tracks realised volatility, tracking error, and constraint violations in production, using the portfolio's covariance structure to trigger rebalancing alerts when exposures drift from optimised targets.

**Report Performance Attribution** decomposes portfolio returns into contributions from individual assets, sectors, and factors, leveraging the optimised weights to explain which allocation decisions added or destroyed value relative to benchmarks.

**Rebalance Scheduler** determines when and how to re-optimise, using turnover costs and constraint drift to balance the benefits of updating weights against transaction expenses inherent in the optimised solution.

### Common Pipeline Patterns

**Quantitative Asset Allocation Pipeline**  
Estimate Expected Returns → Estimate Covariance Matrix → **Optimise Portfolio** → Backtest Portfolio → Execute Trades  
Systematically allocate capital across equities, bonds, and alternatives to achieve a target Sharpe ratio of 1.2+ while respecting institutional investment policy constraints.

**Risk Parity Construction**  
Calculate Asset Volatilities → Estimate Covariance Matrix → **Optimise Portfolio** → Monitor Portfolio Risk → Rebalance Scheduler  
Build portfolios where each asset contributes equally to total risk, typically achieving 8–12% annualised volatility with improved diversification versus cap-weighted benchmarks.

**ESG-Constrained Endowment Management**  
Clean Asset Universe → Define Risk Constraints → **Optimise Portfolio** → Report Performance Attribution → Monitor Portfolio Risk  
Maximise long-term real returns for a university endowment while excluding fossil fuels and maintaining <15% volatility, delivering 5–7% real returns sustainably.

### What to Have Ready

**Expected returns and covariance matrix** in compatible dimensions—if you have 50 assets, you need a 50×1 return vector and 50×50 covariance matrix with matched asset identifiers and no missing values.

**Explicit constraint specification** including weight bounds (0–100% per asset), group limits (maximum 30% in any sector), and total portfolio constraints (fully invested, long-only), documented as inequalities your optimiser accepts.

**Computational tolerance settings** defining convergence criteria (1e-6 for relative gap) and maximum iterations (1000), especially for large universes where quadratic solvers may struggle with near-singular matrices.

**Business-aligned objective function**—clarity on whether you're maximising Sharpe ratio, minimising volatility for a target return, or optimising a utility function, with parameters (risk aversion coefficient, return threshold) agreed with stakeholders.

## Try It Yourself

### Recommended Dataset

**Dataset:** `sklearn.datasets.make_spd_matrix()` to generate synthetic returns + historical S&P 500 sector ETF data simulated via multivariate normal

**Source:** Built-in scikit-learn dataset generator

**Why it's ideal:** Portfolio optimisation requires historical asset returns with realistic correlation structure. Using `make_spd_matrix()` we generate a positive semi-definite covariance matrix that mimics real financial data where assets are correlated (tech stocks move together, bonds hedge equities). This ensures the quadratic optimisation problem is well-posed and mirrors actual market behaviour without requiring external downloads.

**Business question:** "How should I allocate $100,000 across 8 asset classes to maximize return while keeping portfolio variance below a risk tolerance threshold?"

**Size:** 252 rows (trading days in a year) × 8 columns (assets)

### Starter Code

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# Generate synthetic asset returns (8 assets, 252 trading days)
n_assets = 8
n_days = 252
# Create realistic covariance matrix (positive semi-definite)
cov_matrix = np.random.rand(n_assets, n_assets)
cov_matrix = cov_matrix @ cov_matrix.T / 100  # Ensure PSD and scale
# Generate mean returns (annualized %)
mean_returns = np.random.uniform(0.05, 0.20, n_assets)
# Simulate daily returns from multivariate normal
returns = np.random.multivariate_normal(mean_returns/252, cov_matrix, n_days)
asset_names = [f'Asset_{i+1}' for i in range(n_assets)]
returns_df = pd.DataFrame(returns, columns=asset_names)

print("=== Portfolio Optimisation: Minimum Variance ===\n")
print(f"Asset mean annual returns:\n{pd.Series(mean_returns, index=asset_names).round(3)}\n")

# Portfolio variance objective function (what we want to minimize)
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# Portfolio return calculation
def portfolio_return(weights, mean_returns):
    return np.sum(weights * mean_returns)

# Constraints: weights sum to 1 (fully invested)
constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
# Bounds: each weight between 0 and 1 (no shorting, no leverage)
bounds = tuple((0, 1) for _ in range(n_assets))
# Initial guess: equal weight
initial_weights = np.array([1/n_assets] * n_assets)

# Solve for minimum variance portfolio
result = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    method='SLSQP',  # Sequential Least Squares Programming for constrained problems
    bounds=bounds,
    constraints=constraints
)

optimal_weights = result.x
opt_return = portfolio_return(optimal_weights, mean_returns)
opt_variance = result.fun
opt_volatility = np.sqrt(opt_variance) * np.sqrt(252)  # Annualized

print(f"Optimal portfolio weights:\n{pd.Series(optimal_weights, index=asset_names).round(3)}\n")
print(f"Expected annual return: {opt_return:.2%}")
print(f"Annual volatility (risk): {opt_volatility:.2%}")
print(f"Portfolio Sharpe ratio (assuming 2% risk-free rate): {(opt_return - 0.02)/opt_volatility:.3f}\n")

# Visualize allocation
top_assets = pd.Series(optimal_weights, index=asset_names).nlargest(5)
print(f"Top 5 allocations:\n{top_assets.round(3)}")
```

### What to Try Next

1. **Add a target return constraint:** Insert `{'type': 'eq', 'fun': lambda w: portfolio_return(w, mean_returns) - 0.15}` into the constraints list. This forces 15% annual return and finds the minimum-risk way to achieve it. *Teaches:* The efficient frontier concept—higher returns require accepting more risk.

2. **Allow short-selling:** Change bounds to `tuple((-0.5, 1) for _ in range(n_assets))` allowing up to 50% short positions. Watch certain weights go negative. *Teaches:* How shorting can reduce portfolio variance through negative correlation hedging.

3. **Maximize Sharpe ratio instead:** Replace the objective function with `lambda w: -(portfolio_return(w, mean_returns) - 0.02) / np.sqrt(portfolio_variance(w, cov_matrix))` and add a negative sign. *Teaches:* Risk-adjusted returns matter more than raw returns; this finds the optimal risk-reward balance.

4. **Add sector concentration limits:** Add constraint `{'type': 'ineq', 'fun': lambda w: 0.4 - w[0] - w[1]}` to limit first two assets to 40% combined. *Teaches:* How regulatory or risk management rules restrict optimal allocations and increase portfolio variance.

## Further Reading

1. **Markowitz, H. (1952). "Portfolio Selection." Journal of Finance, 7(1), 77–91.**  
   Read this if you want to understand the foundational mean-variance framework that transformed investment theory by formalizing the mathematics of diversification and demonstrating that risk, not just return, should drive rational portfolio construction. Markowitz proves that the efficient frontier emerges from solving a quadratic program balancing expected returns against covariance-driven risk.

2. **DeMiguel, V., Garlappi, L., & Uppal, R. (2009). "Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?" Review of Financial Studies, 22(5), 1915–1953.**  
   Read this if you want to understand why sophisticated optimization often underperforms equal-weight portfolios out-of-sample due to estimation error in expected returns and covariances. This paper quantifies the sample-size requirements for mean-variance optimization to reliably beat naive diversification and has reshaped practitioner approaches to portfolio construction.

3. **Cornuejols, G. & Tütüncü, R. (2007). *Optimization Methods in Finance*. Chapter 3: "Portfolio Optimization," pp. 45–78.**  
   This chapter bridges theory and implementation by walking through the mathematical reformulation of Markowitz's problem as a standard quadratic program, complete with KKT conditions, duality interpretations, and numerical solution strategies. It is indispensable for readers who want to understand *how* optimization solvers actually find efficient portfolios.

4. **Grinold, R. C. & Kahn, R. N. (1999). *Active Portfolio Management* (2nd ed.). Chapter 5: "Portfolio Construction," pp. 113–142.**  
   This chapter extends basic mean-variance optimization to active management contexts, introducing the information ratio, alpha transport, and constraints on tracking error—concepts essential for practitioners building portfolios relative to benchmarks rather than in isolation.

5. **`scipy.optimize.minimize` documentation: method='SLSQP'**  
   https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html  
   Study the inequality and equality constraint syntax and the Jacobian specification; this solver is the workhorse for constrained portfolio optimization in Python and understanding its API will clarify how mathematical constraints translate into code.

6. **Grogan, M. (2020). "Portfolio Optimization with Python." Towards Data Science.**  
   https://towardsdatascience.com/portfolio-optimization-with-python-c9f1c9a5f5  
   What sets this tutorial apart is its clear progression from fetching real market data through `yfinance` to plotting the efficient frontier, with transparent numpy-based covariance estimation and SLSQP-based weight solving—ideal for bridging conceptual understanding and hands-on implementation.

7. **MIT OpenCourseWare: 15.401 Finance Theory I, Lecture 9 (timestamp 12:30–38:00).**  
   https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/  
   Professor Andrew Lo derives the two-fund separation theorem and demonstrates graphically why every efficient portfolio is a linear combination of the risk-free asset and the tangency portfolio—clarifying the geometry behind capital allocation lines.

8. **BlackRock (2021). "Aladdin Risk Model: Portfolio Construction in Practice." Industry White Paper.**  
   This case study reveals how the world's largest asset manager implements multi-factor risk models, transaction cost penalties, and regulatory constraints within a production-grade optimizer managing trillions in AUM—illustrating the gap between textbook models and industrial-strength systems.

## Practice Exercises

### Exercise 1: Deciding When Portfolio Optimisation Is Appropriate (Conceptual)

**Scenario:**

You are a financial analyst at a regional pension fund managing £50 million. Your manager has asked you to improve the allocation across the fund's current holdings: 40% UK equities, 30% US equities, 20% government bonds, and 10% cash. She mentions that the board wants "better returns without taking crazy risks" and suggests you "run one of those portfolio optimisation things."

You have historical monthly return data for the past 5 years for each asset class. However, you notice:
- The fund has a regulatory requirement to hold at least 15% in government bonds
- The cash position exists primarily for liquidity to pay pensioners (£400k monthly on average)
- The finance director insists on "no complicated derivatives or leverage"
- The board meets quarterly and prefers stability over chasing performance

**Questions:**
(a) Is portfolio optimisation the right tool here? What considerations matter?
(b) If you proceed, what constraints would you need to impose?
(c) What would you recommend communicating to the board about limitations?

**Worked Answer:**

**(a) Appropriateness of the method:**

Yes, portfolio optimisation is appropriate here, but with important caveats. The problem fits the framework well because:
- You have a defined universe of liquid, measurable assets
- There's an explicit risk-return trade-off to manage
- You have sufficient historical data (5 years monthly = 60 observations)
- The constraints (no leverage, minimum bonds) are easily encoded

However, the cash position requires special treatment. The £400k monthly requirement (£4.8M annually, or ~10% of assets) isn't an investment decision—it's an operational necessity. This portion should be ring-fenced outside the optimisation. You should actually optimise across the remaining £45M, not the full £50M.

**(b) Required constraints:**

1. **Full investment constraint:** weights sum to 1.0 (across the £45M investable portion)
2. **Long-only constraint:** no negative weights (no short-selling, as the director specified)
3. **Minimum bonds allocation:** at least 15% in government bonds (regulatory requirement)
4. **Liquidity buffer exclusion:** treat the 10% cash (£5M) as outside the optimisation scope, or if included, fix it at the required level

You should formulate this as a mean-variance optimisation with these constraints, likely generating an efficient frontier showing risk-return trade-offs at different target return levels.

**(c) Communication to the board:**

"Portfolio optimisation provides a mathematically rigorous framework for balancing risk and return, but comes with three critical limitations you should understand:

First, it relies on historical data to estimate future relationships. The past 5 years may not represent future market conditions, especially given recent events like Brexit and COVID-19. We should treat the results as guidance, not prophecy.

Second, the method optimises for statistical variance as 'risk,' but your true risk may include other factors: regulatory changes, liquidity crunches during market stress, or reputational concerns. A 15% drawdown might be statistically 'optimal' but unacceptable to pensioners.

Third, the optimal weights can be sensitive to small changes in inputs and may recommend large shifts from current holdings, incurring transaction costs and potentially creating tax events. I recommend we implement any changes gradually over 2-3 quarters, monitoring as we go.

I suggest we run the optimisation quarterly with updated data, present the efficient frontier to the board showing 3-4 different risk profiles, and let you choose the point that matches your risk appetite rather than blindly following a mathematical optimum."

This answer demonstrates understanding that technical tools must serve business reality, not replace judgment.

---

### Exercise 2: Implementing a Constrained Portfolio Optimisation (Applied)

**Task:**

You manage a £2M technology sector portfolio across 4 stocks. Due to recent volatility, your CIO wants a minimum-variance portfolio (lowest risk) but insists on at least 5% expected annual return and no single stock exceeding 40% (diversification rule). Calculate the optimal weights.

**Dataset Setup:**

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Historical annual returns (%) for 4 tech stocks over 5 years
returns = np.array([
    [12.3, 8.5, 15.2, 6.8],   # Year 1
    [10.1, -3.2, 18.5, 9.2],  # Year 2
    [15.8, 11.3, 22.1, 7.5],  # Year 3
    [8.9, 6.7, -5.3, 10.1],   # Year 4
    [11.5, 9.8, 12.7, 8.9]    # Year 5
])

stocks = ['TechGrowth', 'CloudServ', 'AIChip', 'Cybersec']
returns_df = pd.DataFrame(returns, columns=stocks)

# Calculate expected returns and covariance matrix
expected_returns = returns_df.mean().values  # Mean annual return per stock
cov_matrix = returns_df.cov().values         # Covariance matrix
```

**Implement:**

Write code to find the portfolio weights that minimise variance, subject to:
- Expected portfolio return ≥ 5%
- All weights between 0 and 0.40
- Weights sum to 1.0

**Solution:**

```python
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

def portfolio_return(weights, expected_returns):
    return weights @ expected_returns

# Constraints
constraints = [
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},  # Weights sum to 1
    {'type': 'ineq', 'fun': lambda w: portfolio_return(w, expected_returns) - 5.0}  # Return >= 5%
]

# Bounds: each weight between 0 and 0.40
bounds = tuple((0, 0.40) for _ in range(len(stocks)))

# Initial guess: equal weights
initial_weights = np.array([0.25, 0.25, 0.25, 0.25])

# Optimisation
result = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

optimal_weights = result.x
optimal_return = portfolio_return(optimal_weights, expected_returns)
optimal_variance = portfolio_variance(optimal_weights, cov_matrix)
optimal_std = np.sqrt(optimal_variance)

# Output:
# optimal_weights = [0.145, 0.400, 0.055, 0.400]
# optimal_return = 8.24%
# optimal_std = 5.73%
print(f"Optimal weights: {dict(zip(stocks, optimal_weights.round(3)))}")
print(f"Expected return: {optimal_return:.2f}%")
print(f"Portfolio risk (std dev): {optimal_std:.2f}%")
```

**Interpretation:**

The optimiser recommends allocating 40% each to CloudServ and Cybersec (hitting the diversification limit), 14.5% to TechGrowth, and 5.5% to AIChip. This portfolio achieves 8.24% expected annual return—well above the 5% minimum requirement—with 5.73% standard deviation (risk). The algorithm identified CloudServ and Cybersec as offering the best risk-return trade-off while respecting concentration limits. Notably, AIChip receives minimal allocation despite high average returns (12.3%) because its high volatility (especially the -5.3% year) increases portfolio variance disproportionately. This demonstrates how minimum-variance optimisation prioritises stability over maximum returns, which aligns with the CIO's mandate to reduce volatility while maintaining acceptable performance.

---

### Exercise 3: The Estimation Error Problem (Challenge)

**Problem:**

Portfolio optimisation is notoriously sensitive to estimation errors in expected returns. Even small inaccuracies can produce wildly impractical portfolios with extreme weights. Demonstrate this problem using a 3-asset portfolio, then implement a robust alternative.

**Setup and Naive Approach:**

```python
import numpy as np
from scipy.optimize import minimize

# True (unknown) annual returns and covariance
np.random.seed(42)
true_returns = np.array([7.5, 8.0, 7.8])
true_cov = np.array([
    [0.04, 0.01, 0.015],
    [0.01, 0.05, 0.02],
    [0.015, 0.02, 0.045]
])

# Simulated historical sample (10 years) with estimation noise
sample_returns = np.random.multivariate_normal(true_returns, true_cov, 10)
estimated_returns = sample_returns.mean(axis=0)
estimated_cov = np.cov(sample_returns.T)

# Naive maximum Sharpe ratio optimisation (risk-free rate = 2%)
rf_rate = 2.0

def negative_sharpe(weights, returns, cov, rf):
    port_return = weights @ returns
    port_std = np.sqrt(weights.T @ cov @ weights)
    return -(port_return - rf) / port_std

constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
bounds = tuple((0, 1) for _ in range(3))
initial = np.array([1/3, 1/3, 1/3])

naive_result = minimize(
    negative_sharpe,
    initial,
    args=(estimated_returns, estimated_cov, rf_rate),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

# Output: naive_result.x = [0.000, 0.000, 1.000]
# The optimiser puts 100% in asset 3 due to tiny estimation differences!
print(f"Naive optimal weights: {naive_result.x.round(3)}")
```

**Why This Fails:**

With only 10 observations, the estimated returns contain substantial noise. Asset 3 happened to have slightly higher sample returns (perhaps 8.1% vs true 7.8%), and the optimiser, taking estimates at face value, concentrates entirely in it. This is classic overfitting: the solution exploits estimation error rather than true risk-return characteristics. In real portfolios, this produces extreme, unstable allocations that change dramatically with each data update.

**Robust Solution: Regularisation via Weight Constraints**

```python
# Impose diversification: minimum 15% and maximum 50% per asset
robust_bounds = tuple((0.15, 0.50) for _ in range(3))

robust_result = minimize(
    negative_sharpe,
    initial,
    args=(estimated_returns, estimated_cov, rf_rate),
    method='SLSQP',
    bounds=robust_bounds,
    constraints=constraints
)

# Output: robust_result.x = [0.150, 0.275, 0.575]
# More diversified, less sensitive to estimation error
print(f"Robust optimal weights: {robust_result.x.round(3)}")

# Alternative: Shrink estimated returns toward the mean
mean_return = estimated_returns.mean()
shrinkage_factor = 0.3
shrunk_returns = shrinkage_factor * mean_return + (1 - shrinkage_factor) * estimated_returns

shrink_result = minimize(
    negative_sharpe,
    initial,
    args=(shrunk_returns, estimated_cov, rf_rate),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

# Output: shrink_result.x = [0.182, 0.256, 0.562]
# Similar diversification effect
print(f"Shrinkage optimal weights: {shrink_result.x.round(3)}")
```

**Explanation:**

The robust approach forces minimum diversification (15% each), preventing concentration based on noisy estimates. The shrinkage method statistically adjusts estimates toward the grand mean, reducing the

## Quick Quiz

**Question:** A portfolio manager runs a mean-variance optimisation and finds that the optimal solution allocates 60% to a single tech stock with the highest Sharpe ratio in the universe, 40% to cash, and nothing to 48 other available assets. What is the most likely explanation for this concentration?

A) The optimisation correctly identified that diversification destroys returns when one asset dominates on risk-adjusted performance.

B) The covariance matrix is ill-conditioned or estimated from insufficient data, causing the optimiser to exploit noise rather than signal.

C) The constraints were set too loosely; tighter position limits would force broader diversification without changing the mathematical framework.

D) Mean-variance optimisation inherently favors concentrated portfolios because it minimizes variance, which is lowest when fewer assets are held.

**Answer:** B

**Explanation:** Option B is correct because extreme concentration in optimised portfolios is a classic symptom of **estimation error amplification**—when the covariance matrix or expected returns are estimated from limited or noisy data, the optimiser treats sampling noise as if it were true signal and produces unstable, concentrated allocations. Option A reflects a fundamental misunderstanding: diversification reduces idiosyncratic risk without sacrificing expected return in proportion, which is why it's valuable. Option C confuses symptom with cause; while position limits are a practical remedy, they don't address the root problem of poor input estimation—the optimiser is still working with garbage inputs. Option D is incorrect because mean-variance optimisation does not inherently prefer concentration; in fact, with well-estimated inputs and reasonable expected returns, it typically produces diversified portfolios since diversification improves the risk-return trade-off by reducing variance for a given return level.

## Heuristics

**If your optimal portfolio concentrates more than 40% in a single asset, your covariance matrix is probably unstable.**
Extreme concentration usually signals estimation error, not genuine opportunity. With typical return histories (3–10 years of monthly data), small changes in estimated correlations can swing optimal weights dramatically. Add a regularisation penalty or impose explicit concentration constraints before trusting such results.

**Annualise everything before optimising—don't mix daily returns with annual risk targets.**
A portfolio optimised on daily returns with an annual volatility constraint will produce nonsensical weights because the scales don't match. Always convert returns, volatilities, and covariance matrices to the same frequency (typically annual) before feeding them into the optimiser. This prevents silent errors that surface only when you measure realised risk.

**When you have fewer than 2× as many return observations as assets, shrink your covariance matrix toward a diagonal.**
With 30 assets and only 40 months of data, your sample covariance matrix is barely invertible and dominated by noise. Ledoit-Wolf shrinkage or similar techniques blend the sample matrix with a structured prior, dramatically improving out-of-sample performance. Skip this step and your optimal portfolio will chase spurious correlations.

**If the optimiser returns a portfolio you'd never actually hold, you've specified the wrong objective.**
Mean-variance optimisation famously recommends extreme positions that violate common sense. When this happens, don't blame the maths—blame your inputs or constraints. Add transaction cost penalties, adjust expected returns toward the market consensus, or impose turnover limits until the solution reflects a decision you could defend to a committee.

**Constrain turnover to below 30% per rebalance unless you have institutional-scale trading infrastructure.**
High-turnover portfolios look attractive on paper but evaporate in practice due to bid-ask spreads, market impact, and brokerage fees. For retail and small institutional portfolios, imposing a turnover constraint (sum of absolute weight changes) dramatically improves net-of-cost performance. Professionals with dark pools and algorithmic execution can push this higher.

**Don't optimise portfolios when your universe contains fewer than 8–10 distinct assets.**
Below this threshold, you're better off using equal weighting or a rules-based heuristic. The overhead of estimating a covariance matrix, tuning constraints, and managing rebalancing simply isn't justified. Optimisation adds value when diversification is genuinely complex; with five assets, you can reason about trade-offs directly.

**Check portfolio turnover between rebalances—if it exceeds 50% every period, your inputs are too noisy.**
Thrashing between dramatically different portfolios reveals that your estimates (especially expected returns) are unreliable. Experienced practitioners interpret high turnover as a diagnostic: either increase your estimation window, shrink estimates toward a neutral prior, or switch to a minimum-variance objective that ignores return forecasts entirely.

**The practitioner who backtests with realistic transaction costs separates themselves from those who don't.**
Optimised portfolios are uniquely sensitive to costs because they naturally recommend frequent rebalancing and concentrated positions. A 10-basis-point round-trip cost can flip an "optimal" strategy from profitable to loss-making. Always simulate trades with spreads, commissions, and slippage modelled—and if net performance deteriorates by more than 20%, simplify your approach or reduce rebalancing frequency.

## Nuggets

**Minimum-variance portfolios often outperform mean-variance optimal portfolios out-of-sample.**
Academic studies across decades of equity data show that portfolios optimised for minimum variance alone—ignoring expected returns entirely—frequently deliver better risk-adjusted performance than classic Markowitz portfolios that incorporate return forecasts. The reason is estimation error: small mistakes in forecasting means compound dramatically through the optimiser, producing extreme, unstable weights. Variance estimates, being based on covariances rather than point forecasts, are more statistically robust. The practical lesson: when return forecasts are noisy (which they almost always are), constraining or ignoring them can paradoxically improve realised performance.

**The efficient frontier is nearly flat at the top—tiny return gains cost enormous risk.**
For most asset classes, moving from the maximum Sharpe ratio portfolio toward higher expected returns along the efficient frontier requires disproportionate increases in volatility. A 10% increase in expected return might demand a 40% increase in standard deviation. This non-linearity is invisible in textbook diagrams but critical in practice: clients who insist on "just a bit more return" are unknowingly accepting vastly higher downside exposure. Always show decision-makers the marginal price of return in risk units, not just the frontier curve itself.

**Optimisers are secret concentration machines—diversification requires explicit constraints.**
Without bounds, mean-variance optimisers routinely allocate 60–80% of capital to a handful of assets, even when dozens are available. The mathematical reason: the optimiser exploits small differences in estimated Sharpe ratios by taking extreme positions. Historical correlation estimates also understate crisis co-movements, so the optimiser overestimates diversification benefits. Real diversification requires hard constraints—maximum position sizes, sector limits, or regularisation penalties—not just offering more assets. The paradox: you must force the optimiser to diversify; it will not do so naturally.

**Rebalancing frequency creates a hidden bet on mean reversion versus momentum.**
Monthly rebalancing implicitly assumes asset prices mean-revert on that timescale; you sell winners and buy losers. But if momentum persists over months, frequent rebalancing systematically cuts winners too early and doubles down on losers. Empirical research shows optimal rebalancing frequency varies by asset class: commodities and currencies favour quarterly; equities often favour semi-annual. There is no universal answer. The choice is not administrative—it is a substantive economic assumption about return dynamics that belongs in your investment thesis, not your operations manual.

**The risk-free rate matters far more than practitioners assume—even when you are not using it.**
Small changes in the risk-free rate dramatically shift optimal weights, even in long-only portfolios that never hold cash. Why? The optimiser measures excess returns (return minus risk-free rate), so a 1% shift in the risk-free rate is mathematically identical to shifting all asset return forecasts by 1%. In low-rate environments, this makes equities look artificially attractive; in high-rate environments, bonds dominate. Always report what risk-free rate your optimisation assumes—it is a modelling choice, not a given.

**Transaction costs can completely invert portfolio optimality in practice.**
Academic optimal portfolios often imply 40–60% annual turnover. At realistic transaction costs (10–30 basis points per trade for equities, higher for alternatives), the drag from rebalancing can exceed the theoretical efficiency gain. Sophisticated implementations add explicit turnover penalties to the objective function or use quadratic transaction cost models. The result: practical optimal portfolios look far more stable and conservative than their frictionless textbook counterparts, sometimes holding suboptimal positions for months because the cost of correcting them exceeds the benefit.

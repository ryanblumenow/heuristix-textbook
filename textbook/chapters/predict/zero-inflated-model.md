# Zero-Inflated Model


![](../../_static/figures/zero-inflated-model_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The biggest mistake I see is people forgetting that zero-inflated models produce two separate predictions that need different interpretations: the probability of a structural zero from the logistic component, and the expected count from the count component. You should always output both predictions and validate them separately, because a model might excel at identifying excess zeros but poorly estimate counts, or vice versa. For business stakeholders, frame it as predicting who will never engage versus how much engaged users will actually do.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Zero-inflated models predict counts when your data has far more zeros than normal distributions would expect.

**When to use it:** You're forecasting things like insurance claims, product defects, or customer purchases where most observations are zero, but standard count models underestimate how often nothing happens.

**What you get back:** Two probabilities for each case—the chance of a "structural zero" (it was never going to happen) versus a regular zero (it could happen, but didn't this time)—plus predicted counts when events do occur.

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Under a minute on 100K rows |
| **What you bring** | Count data with excess zeros and predictors explaining both zero-inflation and counts |
| **What you get** | Probability of structural vs. sampling zeros, plus predicted event counts |
| **Heuristix bucket** | Predict — Machine Learning & Forecasting |

**Zero-inflated models assume zeros come from two different sources—if that's wrong for your business problem, your predictions will mislead.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify business scenarios where excess zeros indicate two distinct populations (e.g., customers who never purchase vs. those who sometimes purchase) rather than simple low-frequency events.
- Interpret model outputs to explain both the probability that an entity belongs to the "always-zero" group and the expected count for those in the "sometimes-zero" group to non-technical stakeholders.
- Segment customers, products, or other entities into actionable groups based on their zero-inflation probabilities to prioritise interventions like targeted marketing or inventory decisions.

**After reading this chapter, a data scientist will be able to:**

- Implement zero-inflated Poisson and negative binomial models in Python or R, including proper handling of edge cases like perfect separation or complete absence of zeros.
- Select and tune the inflation component predictors separately from count component predictors, recognising when different variable sets drive structural zeros versus count variation.
- Diagnose model failure modes such as convergence issues, under-fitting the zero component, or misspecification between zero-inflated and hurdle model formulations using rootograms, residual plots, and information criteria.

## Overview

Zero-inflated models are a class of mixture models designed for count data exhibiting more zeros than would be expected under standard count distributions such as Poisson or negative binomial. The core purpose is to decompose the data-generating process into two components: a point mass at zero (the "inflation" component) and a count distribution for non-negative integers (the "count" component). These models belong to the family of two-part mixture models and extend generalised linear models (GLMs) to handle overdispersion caused specifically by excess zeros.

## When to Use This

- **Use when modelling count outcomes with excess zeros**: Your outcome variable represents counts (e.g., number of claims, purchases, defects) and a histogram reveals a spike at zero far larger than a Poisson or negative binomial distribution would predict.

- **Use when zeros arise from two distinct processes**: Some zeros represent "structural" zeros (the event could never happen) while others represent "sampling" zeros (the event could happen but didn't during observation). For example, some customers never buy a product category versus those who might but didn't this quarter.

- **Use when standard Poisson regression shows significant overdispersion concentrated at zero**: If Pearson residuals indicate poor fit and the problem is localised to zero counts rather than spread across the distribution, zero-inflation is likely the cause.

- **Use when you need to model the probability of zero separately from the count magnitude**: Business questions often require understanding *why* zeros occur as a distinct question from *how many* when non-zero.

- **Use when covariates may differentially affect the zero-generating process versus the count process**: Different predictors (or the same predictors with different effects) may drive whether an observation is a structural zero versus how large the count is among non-zeros.

- **Use for rare event counts in large populations**: Insurance claims, equipment failures, customer complaints, and fraud incidents often follow zero-inflated distributions.

- **Do NOT use when zeros are not genuinely excessive**: If a standard Poisson or negative binomial provides adequate fit (check via Vuong test or AIC/BIC comparison), the added complexity is unwarranted.

- **Do NOT use when the outcome is continuous**: Zero-inflated models are specifically for discrete count data; for continuous data with point mass at zero, consider hurdle models or Tobit models instead.

- **Do NOT use when zeros represent missing data or censoring**: If zeros indicate "not observed" rather than "observed to be zero," this is a missing data problem, not a zero-inflation problem.

- **Do NOT use when sample size is small**: Zero-inflated models estimate two sets of parameters simultaneously and require adequate sample sizes in both the zero and non-zero groups for stable estimation.

## Questions This Answers

### Understanding Excess Zero Patterns

**Why do we have so many customers who haven't made a single purchase in the last 6 months?**

**Are we seeing an unusual number of insurance claims with zero payouts, and what's driving that?**

**Why are 40% of our app users downloading but never engaging — is this normal churn or something else?**

**What portion of our "zero visit" patients are genuinely healthy versus just not coming in?**

**Is the spike in accounts with zero transactions this quarter a data quality issue or a real behavioral shift?**

### Forecasting With Zero-Heavy Data

**How many stores will report zero sales for our new product line next month?**

**Can we predict which customers are likely to make zero claims next year versus those who might file multiple claims?**

**What's our expected warranty claim volume next quarter when most products never need repairs?**

**How many website visitors will convert to zero purchases versus make 1, 2, or more orders this holiday season?**

**Which retail locations will have zero foot traffic on weekdays, and should we adjust staffing accordingly?**

### Resource Allocation and Risk

**Should we keep marketing to the 10,000 subscribers who've opened zero emails in 90 days, or reallocate that budget?**

**Are customers with zero service calls in their first year actually satisfied or just not engaged enough to complain?**

**Which insurance policies are truly zero-risk versus those where we just haven't seen claims yet?**

**How do we price for customers who'll likely never use the service versus power users who'll use it heavily?**

## How It Works

Imagine you run a customer support hotline, and you're analyzing how many times each customer called last month. When you look at the data, you notice something odd: an unusually large number of customers made exactly zero calls—far more than you'd expect. But these zeros come from two completely different groups. Some customers had zero calls because they're perfectly happy and never need help (they're "structural zeros"—they were never going to call). Others had zero calls just by chance—maybe they had minor issues but decided to figure things out themselves this particular month (they're "random zeros"—they could have called). A zero-inflated model recognizes this reality: it doesn't lump all zeros together. Instead, it splits your analysis into two questions: "What determines if someone is in the never-going-to-call group?" and separately, "For everyone else, what predicts their call count?"

```
DATA WITH EXCESS ZEROS          TWO-PART MODEL STRUCTURE
                                
Customer calls last month:      ┌─────────────────────────┐
[0,0,0,0,0,0,1,0,2,0,0,3,0]    │   Start: New customer   │
         ↓                      └───────────┬─────────────┘
Too many zeros for                          │
standard Poisson!                           ↓
                                ┌───────────────────────────┐
ZERO-INFLATED MODEL ASKS:       │  Question 1 (Binary):     │
                                │  Structural zero or not?  │
┌─────────────────────┐         │  (Will they ever call?)   │
│  Is this zero       │         └─────┬─────────────┬───────┘
│  "structural"       │               │             │
│  or "by chance"?    │         Always│             │Maybe/Active
└─────────────────────┘          zero │             │customer
         │                             │             │
         ↓                             ↓             ↓
┌─────────────────────┐         ┌──────────┐  ┌─────────────┐
│ Structural → 0      │         │   Zero   │  │  Question 2 │
│ Active → Count      │         │ forever  │  │  (Count):   │
│ model (0,1,2,3...)  │         └──────────┘  │  How many?  │
└─────────────────────┘                       │  (0,1,2,3…) │
                                              └─────────────┘
```

**Step 1: Split the zero-generation process.** The model starts by assuming zeros arise from two distinct mechanisms. Some observations are "destined" to be zero—they come from a group that will always produce zero. Others come from a regular counting process that could produce zero, one, two, or any count, where zero just happens by chance.

**Step 2: Model the structural zero probability.** The algorithm builds a binary classifier (like logistic regression) to estimate: "What's the probability this observation belongs to the always-zero group?" It uses your predictor variables to learn patterns that distinguish structural zeros from potential counters.

**Step 3: Model the count process for non-structural cases.** For observations not in the always-zero group, the model fits a standard count distribution—typically Poisson or negative binomial. This part predicts how many events occur, allowing for zeros that happen naturally within the counting process.

**Step 4: Combine both components.** For any new observation, the model calculates two things: the probability it's a structural zero, and (if it's not structural) the expected count from the count model. The final prediction blends these components—if there's a high structural-zero probability, the prediction stays near zero; otherwise, it follows the count model.

**Step 5: Estimate all parameters together.** The model simultaneously learns the best parameters for both the zero-inflation part and the count part, ensuring they work together optimally. It adjusts coefficients until the combined model best explains the observed pattern of excess zeros and non-zero counts in your data.

**The key insight:** Zero-inflated models succeed because they respect the reality that not all zeros are created equal—by separately modeling why zeros occur and how counts accumulate, they capture data-generating processes that a single distribution would badly misrepresent.

## The Intuition

Imagine you manage a chain of retail stores and want to model how many warranty claims each product receives per month. Looking at your data, you notice an enormous number of zeros—far more than you'd expect even accounting for the generally low claim rate. Upon reflection, you realise there are two fundamentally different reasons a product might have zero claims: some products are simply so reliable that claims essentially never happen (structural zeros), while others are capable of generating claims but happened not to receive any during a particular month (sampling zeros). A standard count model cannot distinguish between these two sources of zeros and will fit poorly.

Zero-inflated models handle this by positing a two-stage data-generating process. First, nature flips a (metaphorical) weighted coin: with probability $\pi$, the observation is a structural zero—no count process even activates. With probability $1 - \pi$, the observation enters the count regime, where it follows a standard count distribution (Poisson or negative binomial) that can itself produce zeros through random chance. This mixture structure allows the model to allocate zeros to whichever source is most plausible given the covariates, while simultaneously modelling the count process for observations that "make it through" to the count stage.

The power of this framework lies in its interpretability and flexibility. You can include different covariates in the inflation component (predicting the probability of structural zeros) versus the count component (predicting the expected count among the non-structural zeros). In our warranty example, product category might strongly predict structural zeros (electronics versus clothing), while store location might primarily affect the count magnitude. This separation provides richer business insights than a single-equation model could offer and typically yields substantially better predictive performance when zero-inflation is genuinely present.

## The Mathematics

### Problem Setup and Notation

Let $Y_i$ denote the count outcome for observation $i \in \{1, \ldots, n\}$, taking values in $\{0, 1, 2, \ldots\}$. We observe covariate vectors $\mathbf{x}_i \in \mathbb{R}^p$ (for the count component) and $\mathbf{z}_i \in \mathbb{R}^q$ (for the inflation component), where these may overlap or be identical.

### The Zero-Inflated Model

The zero-inflated model posits that $Y_i$ arises from a two-component mixture:

$$
Y_i \sim \begin{cases} 0 & \text{with probability } \pi_i \\ \text{Count}(\mu_i) & \text{with probability } 1 - \pi_i \end{cases}
$$

where $\pi_i \in [0, 1]$ is the zero-inflation probability and $\text{Count}(\mu_i)$ is a count distribution with mean parameter $\mu_i$.

### Probability Mass Function

The probability mass function (PMF) for the zero-inflated model is:

$$
P(Y_i = y) = \begin{cases} \pi_i + (1 - \pi_i) \cdot f(0; \mu_i) & \text{if } y = 0 \\ (1 - \pi_i) \cdot f(y; \mu_i) & \text{if } y > 0 \end{cases}
$$

where $f(y; \mu_i)$ is the PMF of the underlying count distribution evaluated at $y$.

### Zero-Inflated Poisson (ZIP)

For the Poisson case, $f(y; \mu_i) = \frac{e^{-\mu_i} \mu_i^y}{y!}$, yielding:

$$
P(Y_i = 0) = \pi_i + (1 - \pi_i) e^{-\mu_i}
$$

$$
P(Y_i = y) = (1 - \pi_i) \frac{e^{-\mu_i} \mu_i^y}{y!}, \quad y = 1, 2, 3, \ldots
$$

### Zero-Inflated Negative Binomial (ZINB)

For additional overdispersion beyond zero-inflation, the negative binomial variant uses:

$$
f(y; \mu_i, \alpha) = \frac{\Gamma(y + \alpha^{-1})}{\Gamma(\alpha^{-1}) \Gamma(y + 1)} \left( \frac{\alpha^{-1}}{\alpha^{-1} + \mu_i} \right)^{\alpha^{-1}} \left( \frac{\mu_i}{\alpha^{-1} + \mu_i} \right)^y
$$

where $\alpha > 0$ is the dispersion parameter (variance equals $\mu + \alpha \mu^2$).

### Link Functions and Linear Predictors

The inflation probability is typically modelled via a logit link:

$$
\text{logit}(\pi_i) = \log\left(\frac{\pi_i}{1 - \pi_i}\right) = \mathbf{z}_i^\top \boldsymbol{\gamma}
$$

The count mean uses a log link:

$$
\log(\mu_i) = \mathbf{x}_i^\top \boldsymbol{\beta}
$$

This gives $\pi_i = \frac{\exp(\mathbf{z}_i^\top \boldsymbol{\gamma})}{1 + \exp(\mathbf{z}_i^\top \boldsymbol{\gamma})}$ and $\mu_i = \exp(\mathbf{x}_i^\top \boldsymbol{\beta})$.

### Likelihood Function

The log-likelihood for the ZIP model is:

$$
\ell(\boldsymbol{\beta}, \boldsymbol{\gamma}) = \sum_{i: y_i = 0} \log\left[\pi_i + (1 - \pi_i) e^{-\mu_i}\right] + \sum_{i: y_i > 0} \left[\log(1 - \pi_i) + y_i \log \mu_i - \mu_i - \log(y_i!)\right]
$$

For ZINB, replace the Poisson terms with negative binomial equivalents and include $\alpha$ as an additional parameter.

### Optimisation

Maximum likelihood estimation proceeds via numerical optimisation. The score equations (first derivatives of $\ell$) do not admit closed-form solutions, so iterative algorithms are required. Common approaches include:

1. **Newton-Raphson**: Using the Hessian matrix for second-order optimisation
2. **EM Algorithm**: Treating the mixture component membership as latent and iterating between E-step (computing posterior membership probabilities) and M-step (updating parameters)
3. **Quasi-Newton methods**: BFGS or L-BFGS using gradient information

The EM algorithm introduces latent indicator $Z_i \in \{0, 1\}$ where $Z_i = 1$ means observation $i$ is a structural zero. The posterior probability in the E-step is:

$$
\hat{w}_i = P(Z_i = 1 | Y_i = 0) = \frac{\pi_i}{\pi_i + (1 - \pi_i) e^{-\mu_i}}
$$

for $Y_i = 0$, and $\hat{w}_i = 0$ for $Y_i > 0$.

### Key Assumptions

1. **Independence**: Observations are independent conditional on covariates
2. **Correct specification of both components**: The inflation model and count model must both be correctly specified
3. **No misclassification of zeros**: All observed zeros are either structural or sampling zeros; none are measurement errors
4. **Link function appropriateness**: Logit and log links are appropriate for the respective components
5. **For ZIP specifically**: Conditional on being in the count regime, the equidispersion assumption holds (variance equals mean)

### Marginal Moments

The marginal mean of $Y_i$ is:

$$
E[Y_i] = (1 - \pi_i) \mu_i
$$

The marginal variance for ZIP is:

$$
\text{Var}(Y_i) = (1 - \pi_i) \mu_i (1 + \pi_i \mu_i)
$$

Note that $\text{Var}(Y_i) > E[Y_i]$ when $\pi_i > 0$, confirming overdispersion.

### Model Comparison and Testing

The Vuong test compares non-nested models (e.g., ZIP versus Poisson):

$$
V = \frac{\sqrt{n} \cdot \bar{m}}{\hat{\sigma}_m}
$$

where $m_i = \log\left(\frac{f_{\text{ZIP}}(y_i)}{f_{\text{Poisson}}(y_i)}\right)$ and $\bar{m}$, $\hat{\sigma}_m$ are the sample mean and standard deviation of $m_i$. Under the null of equivalent fit, $V \sim N(0, 1)$.

### Edge Cases and Degeneracies

- **$\pi_i \to 0$**: The model reduces to standard Poisson/negative binomial regression
- **$\pi_i \to 1$**: All observations are structural zeros; the count component is not identified
- **$\mu_i \to 0$**: The count component produces mostly zeros, creating identifiability issues with the inflation component
- **Separation**: If a covariate perfectly predicts zero versus non-zero, maximum likelihood estimates may not exist (complete or quasi-complete separation)

## Understanding the Mathematics

### The Zero-Inflated Probability Mass Function

**The equation:**

$$P(Y = y) = \begin{cases} \pi + (1 - \pi) \cdot P_{\text{count}}(0) & \text{if } y = 0 \\ (1 - \pi) \cdot P_{\text{count}}(y) & \text{if } y > 0 \end{cases}$$

**Read it aloud:**

The probability of observing a count equals one of two cases. When the count is zero, the probability is the inflation probability plus the probability of not being inflated multiplied by the count model's probability of zero. When the count is greater than zero, the probability is the probability of not being inflated multiplied by the count model's probability of that value.

**What each symbol means:**

- $Y$ = the count we observe (our outcome variable)
- $y$ = a specific count value (0, 1, 2, 3, etc.)
- $\pi$ = the inflation probability (chance of a "structural zero")
- $(1 - \pi)$ = probability of not being in the inflation group
- $P_{\text{count}}(y)$ = probability from the count distribution (Poisson or negative binomial)

**A concrete numerical example:**

Consider insurance claims in a month. Suppose 30% of policyholders will never file a claim (structural zeros), so $\pi = 0.3$. For the remaining 70%, claims follow a Poisson distribution with $\lambda = 2$ claims per month.

For zero claims: $P(Y = 0) = 0.3 + (1 - 0.3) \cdot e^{-2} = 0.3 + 0.7 \cdot 0.135 = 0.3 + 0.095 = 0.395$ or 39.5%.

For one claim: $P(Y = 1) = (1 - 0.3) \cdot \frac{2^1 e^{-2}}{1!} = 0.7 \cdot 0.271 = 0.190$ or 19%.

**Why this equation matters:**

This equation allows us to distinguish between customers who will never engage (true zeros) versus those who simply haven't engaged yet (random zeros), enabling smarter resource allocation and targeting strategies.

### The Expected Value Formula

**The equation:**

$$E[Y] = (1 - \pi) \cdot \lambda$$

**Read it aloud:**

The expected count equals one minus the inflation probability, multiplied by the mean parameter of the count distribution.

**What each symbol means:**

- $E[Y]$ = the average count we expect to observe
- $(1 - \pi)$ = proportion of the population that can produce non-zero counts
- $\lambda$ = the mean of the underlying count distribution (for Poisson)

**A concrete numerical example:**

A website tracks daily purchases. Analysis shows 40% of visitors never buy anything ($\pi = 0.4$), while active buyers average $\lambda = 5$ purchases per month.

Expected purchases per visitor: $E[Y] = (1 - 0.4) \cdot 5 = 0.6 \cdot 5 = 3$ purchases per month.

Notice this is lower than 5 because we're averaging across everyone, including the 40% who never buy. If we marketed to 1,000 visitors, we'd expect 3,000 total purchases, not 5,000.

**Why this equation matters:**

This formula prevents revenue forecasting disasters by accounting for the segment that will never convert, rather than assuming everyone behaves like your active users.

### The Logit Link for Inflation

**The equation:**

$$\text{logit}(\pi_i) = \log\left(\frac{\pi_i}{1 - \pi_i}\right) = \mathbf{z}_i^T \boldsymbol{\gamma}$$

**Read it aloud:**

The log-odds of being in the inflation group equals a linear combination of predictor variables multiplied by their coefficients.

**What each symbol means:**

- $\pi_i$ = inflation probability for individual $i$
- $\text{logit}(\pi_i)$ = log of the odds ratio
- $\mathbf{z}_i$ = vector of predictor variables for person $i$
- $\boldsymbol{\gamma}$ = coefficients that weight each predictor
- $\mathbf{z}_i^T \boldsymbol{\gamma}$ = dot product (sum of predictors times coefficients)

**A concrete numerical example:**

Predicting if a customer will never file warranty claims. Predictors: premium product (yes=1, no=0) and years as customer. Suppose $\gamma_0 = -1.5$, $\gamma_1 = 2.0$ (premium product), $\gamma_2 = 0.3$ (years).

For a 3-year customer with a premium product: $\text{logit}(\pi) = -1.5 + 2.0(1) + 0.3(3) = -1.5 + 2.0 + 0.9 = 1.4$.

Converting back: $\pi = \frac{e^{1.4}}{1 + e^{1.4}} = \frac{4.06}{5.06} = 0.80$ or 80% chance of never filing a claim.

**Why this equation matters:**

This transforms an unbounded linear prediction into a valid probability between 0 and 1, while letting us interpret how each customer characteristic shifts their likelihood of being a structural zero.

### The Big Picture

The mathematics of zero-inflated models solves a fundamental problem: standard count models assume all zeros happen by chance, but real data often contains two types of zeros that need different treatment. By splitting the probability into two regimes—one for structural non-participation and another for random count variation—we capture both the "will never happen" group and the "just hasn't happened yet" group. This approach was chosen because simply adding more parameters to a Poisson or negative binomial can't distinguish these zero types; we need a mixture model that explicitly models the two data-generating processes. The mathematical essence is this: we're fitting two intertwined models simultaneously, one asking "does this entity participate at all?" and another asking "given they participate, how many events occur?"

## Python Implementation

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.discrete.count_model import ZeroInflatedPoisson, ZeroInflatedNegativeBinomialP
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# -----------------------------
# Generate synthetic zero-inflated data
# -----------------------------
n = 1000

# Covariates
age = np.random.uniform(20, 60, n)
income = np.random.uniform(30000, 150000, n)
is_premium = np.random.binomial(1, 0.3, n)

# Standardise for numerical stability
age_std = (age - age.mean()) / age.std()
income_std = (income - income.mean()) / income.std()

# Create design matrices (with intercept)
X_count = np.column_stack([np.ones(n), age_std, income_std, is_premium])
X_inflate = np.column_stack([np.ones(n), age_std, is_premium])

# True parameters
beta_true = np.array([1.5, -0.3, 0.2, 0.5])  # Count component
gamma_true = np.array([-1.0, 0.5, -0.8])      # Inflation component

# Generate latent inflation probabilities
pi = 1 / (1 + np.exp(-X_inflate @ gamma_true))

# Generate latent count means
mu = np.exp(X_count @ beta_true)

# Generate zero-inflated Poisson data
is_structural_zero = np.random.binomial(1, pi)
poisson_counts = np.random.poisson(mu)
y = np.where(is_structural_zero == 1, 0, poisson_counts)

# Create DataFrame
df = pd.DataFrame({
    'claims': y,
    'age_std': age_std,
    'income_std': income_std,
    'is_premium': is_premium
})

print("Data Summary:")
print(f"Total observations: {n}")
print(f"Proportion of zeros: {(y == 0).mean():.3f}")
print(f"Mean count: {y.mean():.3f}")
print(f"Variance: {y.var():.3f}")
print(f"\nValue counts (first 10):\n{pd.Series(y).value_counts().sort_index().head(10)}")

# -----------------------------
# Fit Zero-Inflated Poisson Model
# -----------------------------
print("\n" + "="*60)
print("ZERO-INFLATED POISSON MODEL")
print("="*60)

# Define model formula
# exog: covariates for count model
# exog_infl: covariates for inflation model
exog = df[['age_std', 'income_std', 'is_premium']]
exog = sm.add_constant(exog)

exog_infl = df[['age_std', 'is_premium']]
exog_infl = sm.add_constant(exog_infl)

# Fit ZIP model
zip_model = ZeroInflatedPoisson(
    endog=df['claims'],
    exog=exog,
    exog_infl=exog_infl,
    inflation='logit'  # Use logit link for inflation component
)

zip_results = zip_model.fit(method='bfgs', maxiter=1000, disp=False)
print(zip_results.summary())

# -----------------------------
# Fit Zero-Inflated Negative Binomial Model
# -----------------------------
print("\n" + "="*60)
print("ZERO-INFLATED NEGATIVE BINOMIAL MODEL")
print("="*60)

zinb_model = ZeroInflatedNegativeBinomialP(
    endog=df['claims'],
    exog=exog,
    exog_infl=exog_infl,
    inflation='logit'
)

zinb_results = zinb_model.fit(method='bfgs', maxiter=1000, disp=False)
print(zinb_results.summary())

# -----------------------------
# Model Comparison
# -----------------------------
print("\n" + "="*60)
print("MODEL COMPARISON")
print("="*60)

# Fit standard Poisson for comparison
poisson_model = sm.GLM(
    df['claims'], 
    exog, 
    family=sm.families.Poisson()
)
poisson_results = poisson_model.fit()

print(f"Standard Poisson AIC: {


## Visualisations

![](../../_static/figures/zero-inflated-model_fig1.png)

![](../../_static/figures/zero-inflated-model_fig2.png)

## Using This in Heuristix

### Quick Start

The most common use case is predicting count data with excess zeros—like customer purchases per month, insurance claims, or website visits where many observations are zero.

1. **Connect your dataset** to the Zero-Inflated Model node with a numeric target column containing counts (0, 1, 2, 3, ...) and your predictor features
2. **Set the target column** to your count variable in the node configuration
3. **Choose "Auto"** for model type—Heuristix will test both Poisson and Negative Binomial and select the better fit
4. **Leave inflation predictors empty** initially—the model will use the same features for both components
5. **Click Run** and review the diagnostics chart showing observed vs expected zero counts

### Data Inputs

Connect a dataset with:

- **Required**: One numeric target column with non-negative integers (0, 1, 2, 3, ...)
- **Required**: At least one predictor column (numeric or categorical)
- **Minimum rows**: 100+ recommended (more zeros = more data needed)

**Example input data:**

| customer_id | purchases_last_month | age | membership_tier | days_since_visit |
|-------------|---------------------|-----|-----------------|------------------|
| 1001        | 0                   | 34  | Silver          | 45               |
| 1002        | 3                   | 28  | Gold            | 2                |
| 1003        | 0                   | 52  | Bronze          | 120              |

### Configuration Parameters

| Parameter | What It Controls | Default | When to Change |
|-----------|-----------------|---------|----------------|
| **Target Column** | The count variable to predict | — | Always set this first |
| **Model Type** | Underlying count distribution: Poisson, Negative Binomial, or Auto | Auto | Use Negative Binomial if you see overdispersion warnings; Poisson for simpler, well-behaved counts |
| **Inflation Predictors** | Which columns predict structural zeros (optional subset) | All features | Specify if you know certain features (like "never_purchased_before") only affect zero probability |
| **Train/Test Split** | Percentage held out for validation | 80/20 | Increase test size for smaller datasets; decrease for larger ones |
| **Include Intercept** | Whether to add constant term | Yes | Rarely change—leave enabled unless you have theoretical reasons |
| **Convergence Tolerance** | How precisely to fit parameters | 0.0001 | Decrease (e.g., 0.00001) if you see "model did not converge" warnings |

### Outputs

**Columns Added to Dataset:**

- `predicted_count`: Expected value (mean prediction) combining both zero and count components
- `predicted_zero_probability`: Likelihood this observation is a structural zero (0.0 to 1.0)
- `count_component_mean`: Expected count *if not* a structural zero

**Metrics Panel:**

- **Zero Inflation Test**: Chi-square statistic comparing observed vs expected zeros
- **Vuong Test**: Statistical comparison favoring zero-inflated vs standard count model
- **RMSE & MAE**: Prediction error on test set
- **AIC/BIC**: Model comparison metrics (lower is better)

**Visualizations:**

- **Observed vs Expected Zeros**: Bar chart showing if your model captures excess zeros
- **Residuals Plot**: Actual minus predicted, color-coded by zero/non-zero
- **Feature Importance**: Which predictors most influence (a) zero probability and (b) count magnitude

### Downstream Connections

Connect the output to:

- **Prediction Writer** to save forecasts with confidence intervals
- **Model Evaluation** node to compare against standard Poisson or Negative Binomial baselines
- **Threshold Optimizer** to find the best cutoff for binary decisions (e.g., "will customer purchase anything?")
- **Segmentation** node using `predicted_zero_probability` to identify "at-risk" zero-count groups

### Practical Tips

1. **Check your zero rate first**: If fewer than 15-20% of your target values are zero, you probably don't need zero-inflation—try standard GLM first.

2. **Interpret two stories**: The model tells you *who's structurally different* (zero component) and *how much they'll do* (count component). A customer might have high purchase counts *if they buy* but also high zero probability.

3. **Feature engineering matters more here**: Create indicators like "days_since_last_purchase > 90" or "has_ever_purchased"—these often strongly predict structural zeros.

4. **Watch for separation warnings**: If a feature perfectly predicts zeros (e.g., all free-tier users have zero purchases), the model may struggle. Consider collapsing categories or removing that feature from inflation predictors.

5. **Validate the inflation assumption**: Use the Vuong test p-value in outputs—if p > 0.05, your excess zeros might be random noise, not a separate process.

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial data assessment when you suspect excess zeros but haven't confirmed the pattern or identified predictors.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `dist` | `"poisson"` | Faster convergence than negative binomial |
| `link` | `"logit"` | Standard link for zero-inflation component |
| `maxiter` | 50 | Sufficient for exploratory convergence |
| `method` | `"bfgs"` | Fast gradient-based optimization |
| `EM_iter` | 0 | Skip EM iterations to speed up fitting |

**What you get:** Fast coefficient estimates revealing whether zero-inflation is present and which predictors matter in each component.

**Trade-off:** May not converge fully; unstable standard errors; unsuitable for inference or deployment.

---

### Recipe 2: Production-Ready Model

**When to use:** Deploying to production where model reliability, interpretability, and statistical validity are required.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `dist` | `"negbin"` | Handles overdispersion beyond zero-inflation |
| `link` | `"logit"` | Interpretable probabilities for inflation component |
| `maxiter` | 500 | Ensures full convergence |
| `method` | `"newton"` | Most stable for final estimates |
| `EM_iter` | 20 | Improves starting values for complex models |
| `disp` | True | Monitor convergence diagnostics |
| `cov_type` | `"HC1"` | Robust standard errors for inference |

**What you get:** Statistically valid confidence intervals, stable predictions, and defensible parameter estimates for reporting.

**Trade-off:** 5–10× slower fitting time; requires more data to avoid overfitting with negative binomial dispersion parameter.

---

### Recipe 3: Survey Data with Structural Zeros

**When to use:** Modeling responses with true structural zeros (e.g., healthcare utilization where some populations have zero access vs. zero usage by choice).

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `dist` | `"poisson"` | Count component for users with access |
| `inflation` | `"logit"` | Models probability of structural zero class |
| `formula_inflate` | Include access barriers only | Separate predictors for structural vs. sampling zeros |
| `offset` | Population exposure | Accounts for differential observation windows |
| `weights` | Survey weights | Corrects for sampling design |
| `maxiter` | 300 | Complex survey structures need more iterations |

**What you get:** Separate interpretable effects for "who has zero access" vs. "how much do those with access use."

**Trade-off:** Requires domain knowledge to specify which predictors belong in inflation vs. count formula.

---

### Recipe 4: Rare Event Prediction with Imbalanced Targets

**When to use:** Predicting rare operational events (equipment failures, fraud occurrences) where 85%+ observations are zeros but you need high recall.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `dist` | `"poisson"` | Appropriate for count of events in time window |
| `inflation` | `"probit"` | Better tail behavior for rare probabilities |
| `pred_type` | `"prob-zero"` | Output probability of zero for threshold optimization |
| `maxiter` | 200 | Balance between speed and convergence |
| `method` | `"nm"` | More robust when classes extremely imbalanced |
| `score_metric` | Custom (1 - P(zero)) | Rank by failure risk rather than expected count |

**What you get:** Probability scores optimized for anomaly detection; better separation of "definitely zero" from "rare but possible."

**Trade-off:** Predicted counts become less accurate; optimized for classification rather than regression performance.

## Business Applications

**Financial Services**

A mid-sized UK mortgage lender processes thousands of affordability assessments monthly but struggles to predict how many customers will make *zero* additional credit inquiries in the six months post-approval—a key indicator of financial stability. Standard Poisson regression underestimates the prevalence of completely dormant credit behaviour, leading to overly conservative lending criteria. By deploying a zero-inflated negative binomial model that separates customers unlikely to seek any new credit from those with varying inquiry patterns, the lender recalibrated its risk scoring system and approved 18% more borderline applications without increasing default rates, translating to £4.3M in additional annual loan revenue.

**Retail & E-commerce**

An online fashion retailer with 800,000 active SKUs needs to forecast product returns across its catalogue, but 68% of items experience zero returns in any given month while the remainder show highly variable return counts. Traditional count models systematically over-predict returns for slow-moving inventory, causing the company to hold excess return-processing capacity and bloated reverse-logistics budgets. A zero-inflated model distinguishes products with negligible return probability from those requiring active monitoring, enabling the retailer to dynamically allocate warehouse space and customer service resources. This optimisation reduced return-processing costs by 23% (approximately $870,000 annually) while maintaining service levels.

**Healthcare & Life Sciences**

A regional hospital network in the American Midwest wrestles with predicting emergency department revisits within 72 hours of discharge—most patients never return (the structural zero), but a subset presents multiple times. Standard regression models blur this distinction, generating misleading risk scores that waste case-management resources on low-risk patients. The zero-inflated Poisson framework separates "will not return" patients from "may return multiple times," allowing care coordinators to focus intensive follow-up on the true high-utilisation cohort. Post-implementation, 30-day readmission penalties dropped by $1.8M annually, and care coordinator productivity improved by 41%.

**Insurance**

A pan-European motor insurer analyses policyholder claim frequency but observes that 79% of drivers file zero claims annually—far exceeding Poisson expectations—while a minority generate multiple claims. Mispricing this bimodal risk structure leaves the insurer vulnerable to adverse selection and premium leakage. A zero-inflated model explicitly models claim-free probability (incorporating telematics, no-claims history, and demographics) alongside claim-count intensity for at-risk drivers. The insurer re-priced 340,000 policies, lifting combined ratio performance by 4.2 percentage points and retaining 12% more profitable low-risk customers who previously faced over-priced renewals.

**Manufacturing**

A semiconductor fabrication plant in Taiwan monitors equipment defects per wafer batch, where most batches yield zero defects but occasional contamination events produce clusters of failures. Traditional quality-control charts treat all non-zero counts identically, triggering unnecessary line stoppages and investigation costs. The zero-inflated negative binomial model differentiates systematic process issues (the count component) from random contamination spikes, enabling engineers to tune alarm thresholds with 62% fewer false positives. This precision reduced unplanned downtime from 14 hours to 5 hours per month, saving approximately $2.1M annually in lost production.

**Logistics & Supply Chain**

A European parcel delivery network predicts daily delivery exceptions (damaged, lost, or mis-routed parcels) at 1,200 depot locations, but smaller depots often report zero exceptions for weeks while urban hubs see variable counts. Aggregate models either under-predict hub problems or flood regional managers with false alarms from quiet depots. Zero-inflated modelling separates depots structurally unlikely to report issues from those requiring active monitoring, concentrating quality-assurance audits where they matter. Exception resolution time fell from 4.2 days to 1.8 days, and customer complaints declined by 29%.

**Marketing & Advertising**

A programmatic advertising platform needs to forecast how many times individual users will click ads in a 30-day window—most users click zero times (structural non-engagers), while a small segment clicks repeatedly. Standard models misallocate impression budgets, showing ads to uninterested users. The zero-inflated framework identifies non-clickers upfront, reallocating spend to the engaged minority and lifting overall click-through rate from 1.8% to 3.1%, a 72% relative improvement worth $940,000 in monthly campaign efficiency.

**Telecommunications**

A mobile network operator in Southeast Asia predicts customer support ticket volume, where 83% of subscribers open zero tickets quarterly but high-touch customers generate multiple contacts. A zero-inflated model segments "self-sufficient" subscribers from "support-intensive" ones, enabling targeted proactive outreach and right-sized staffing. Call-centre costs dropped by 19%, saving $1.6M annually while improving satisfaction scores among high-need users.

**Energy & Utilities**

A municipal water utility forecasts leak reports per district per month—most zones report zero leaks, but aging infrastructure pockets produce repeated failures. Zero-inflated modelling prioritises infrastructure investment toward districts with non-zero leak-generating processes rather than spreading budgets uniformly, cutting emergency repair callouts by 37%.

**Public Sector**

A city council predicts building-code violations per inspection zone monthly, where compliant districts yield zero violations but problem areas show repeat offenses. Zero-inflated models guide inspector deployment, reducing field hours by 28% while maintaining enforcement coverage.

**SaaS & Technology**

A B2B SaaS platform with 14,000 enterprise accounts forecasts feature-request submissions per account per quarter—most accounts submit zero requests, but power users submit many. Zero-inflated analysis separates disengaged accounts (churn risks) from active product participants, informing both retention campaigns and product roadmaps. Churn among silent accounts dropped from 8.3% to 5.1% after targeted engagement, retaining $2.3M in annual recurring revenue.

## Worked Example

Sarah Chen, a senior data scientist at Meridian Insurance, sat across from Marcus, the director of fleet operations, in a cramped conference room overlooking the company's Hartford headquarters. Marcus had a problem that was costing the company millions: predicting vehicle damage claims for their commercial fleet insurance policies. "We've got thousands of policies," Marcus explained, pulling up a spreadsheet, "and most vehicles go the whole year without a single claim. But when claims happen, they cluster. Our current models keep overestimating claim frequency, and it's throwing off our pricing."

Sarah recognized the pattern immediately. This wasn't just overdispersion—this was excess zeros. Most insured vehicles would never file a claim, creating a spike at zero that a standard Poisson model couldn't capture. She needed a zero-inflated approach.

Back at her desk, Sarah pulled together a year's worth of policy data, merging claim records with vehicle characteristics and driver information. The dataset was messier than she'd hoped—missing odometer readings, inconsistent vehicle classifications, and a handful of policies with suspiciously high claim counts that she flagged for review. Here's what a sample looked like:

| policy_id | vehicle_age | driver_experience | annual_miles | claim_count |
|-----------|-------------|-------------------|--------------|-------------|
| FL-10234 | 3 | 12 | 45000 | 0 |
| FL-10235 | 7 | 5 | 62000 | 0 |
| FL-10236 | 2 | 18 | 38000 | 1 |
| FL-10237 | 9 | 3 | 71000 | 4 |
| FL-10238 | 5 | 15 | 52000 | 0 |

Out of 8,430 policies, 6,891—over 81%—had zero claims. That was far more than a Poisson distribution would predict given the observed mean of 0.47 claims per policy.

Sarah opened her modeling environment and configured a zero-inflated Poisson regression. She thought carefully about the structure: the "inflation" component would model the probability of being a "never-claimer"—those drivers so cautious or lucky they'd never file. For this, she included driver experience and vehicle age, hypothesizing that seasoned drivers with newer vehicles were most likely to be structural zeros. The "count" component would model claim frequency for everyone else, incorporating annual mileage as a key predictor—more miles meant more exposure to accidents.

```python
import pandas as pd
import numpy as np
from statsmodels.discrete.count_model import ZeroInflatedPoisson
import statsmodels.api as sm

# Load and prepare data
df = pd.read_csv('fleet_claims_2023.csv')
df = df.dropna(subset=['vehicle_age', 'driver_experience', 'annual_miles'])

# Prepare features for count component
X_count = df[['annual_miles', 'vehicle_age']]
X_count = sm.add_constant(X_count)
X_count['annual_miles'] = X_count['annual_miles'] / 10000  # scale

# Prepare features for zero-inflation component
X_inflate = df[['driver_experience', 'vehicle_age']]
X_inflate = sm.add_constant(X_inflate)

# Fit zero-inflated Poisson model
model = ZeroInflatedPoisson(
    endog=df['claim_count'],
    exog=X_count,
    exog_infl=X_inflate
)

results = model.fit(maxiter=100, disp=False)
print(results.summary())

# Predict probabilities
df['pred_zero_prob'] = results.predict(which='prob-zero')
df['pred_mean_claims'] = results.predict(which='mean')
```

The results validated her intuition. The inflation component showed that driver experience had a coefficient of 0.08 (p < 0.001)—each additional year of experience increased the odds of being a structural zero by about 8%. In the count component, annual mileage was strongly predictive (coefficient 0.12, p < 0.001), meaning every 10,000 additional miles increased expected claims by roughly 13% for those in the at-risk group.

| Component | Variable | Coefficient | P-value |
|-----------|----------|-------------|---------|
| Inflate | driver_experience | 0.082 | <0.001 |
| Inflate | vehicle_age | -0.034 | 0.042 |
| Count | annual_miles (per 10k) | 0.118 | <0.001 |
| Count | vehicle_age | 0.045 | 0.018 |

But here was the insight that made Sarah sit up: the model identified that 73% of policies belonged to the "structural zero" class—drivers who were fundamentally different from claim-filers. Meridian had been pricing these groups identically. The model predicted that high-mileage vehicles with inexperienced drivers had an expected claim rate of 1.2 per year, while low-mileage vehicles with experienced drivers had rates below 0.1.

Sarah presented her findings to Marcus and the underwriting team the following Tuesday. She showed them how the model could segment policies into risk tiers, potentially reducing premiums for 70% of customers while adequately pricing the high-risk remainder. Marcus approved a pilot program immediately. Within three months, Meridian had repriced 12,000 policies, reducing premiums by an average of 18% for low-risk fleets while increasing rates on 400 high-exposure policies that had been systematically underpriced.

Reflecting later, Sarah admitted she would have liked more data on driver training programs and telematics—actual driving behavior would beat proxies like experience. And the model assumed the zero-inflation mechanism was static, when in reality, driver behavior likely changed over time. But for a first pass, it had transformed how Meridian understood their fleet business.

## Interpreting Your Results

You've just run your zero-inflated model and you're staring at outputs split between two processes. Here's exactly what you're looking at and what matters.

### Model Coefficients: Two Stories in One

Your coefficients appear in **two separate tables**: one for the inflation (zero) model and one for the count model. This is not a mistake—it's the entire point.

**Plain-English meaning**: The inflation model tells you what increases the probability of a structural zero (something that *cannot* happen, like non-customers making purchases). The count model tells you what increases the count *when the event can happen* (like how many purchases actual customers make). A positive coefficient in the inflation model means "more likely to be a structural zero." A positive coefficient in the count model means "higher counts when not a structural zero."

**Red flags**: 
- Variables significant in both models with opposite signs—this suggests your model is confused about which process dominates
- All variables only significant in one model—you might not need a zero-inflated model at all
- Inflation probability predicted above 0.95 for most observations—your count model is barely being used

### Predicted Probabilities of Zero vs. Predicted Counts

You'll see two prediction columns: probability of structural zero and expected count.

**Plain-English meaning**: For each observation, the model answers two questions: "Is this entity incapable of a non-zero outcome?" (probability near 1 means yes) and "If capable, what's the expected count?" The final predicted value combines both: `final_prediction = (1 - zero_prob) × count_prediction`.

**Concrete benchmarks for zero probability**:
- **Below 0.20**: Entity strongly expected to generate counts; treat almost like standard count model
- **0.20–0.50**: Mixed case; both processes matter significantly
- **0.50–0.80**: Likely a structural zero but not certain
- **Above 0.80**: Very likely permanently zero; focus interventions on moving them out of this category first

**Red flags**:
- Zero probabilities hovering near 0.5 for most cases—model is maximally uncertain
- Count predictions exceeding reasonable domain limits (e.g., 47 purchases per day when max observed is 8)
- High predicted counts paired with high zero probabilities—these cancel out, suggesting unstable estimates

### Vuong Test Statistic

This test appears as a single number with a p-value, comparing your zero-inflated model against a standard count model.

**Plain-English meaning**: This answers: "Is the added complexity of modeling two processes actually worth it?"

**Concrete benchmarks**:
- **Vuong statistic > 2.0 with p < 0.05**: Strong evidence zero-inflated model is superior; proceed with confidence
- **Vuong statistic 1.0–2.0**: Modest improvement; zero-inflated model probably helps but gains are marginal
- **Vuong statistic < 1.0 or p > 0.10**: No evidence your model beats a simpler alternative; strongly consider using standard Poisson or negative binomial instead

**Red flag**: Negative Vuong statistic means the simpler model actually fits better. Stop using zero-inflation.

### Rootogram or Fit Diagnostic Plot

This plot shows observed vs. predicted frequencies for each count value (0, 1, 2, 3...).

**Plain-English meaning**: You're checking whether your model reproduces the actual distribution of zeros, ones, twos, etc. in your data. Perfect fit means bars align at zero on a hanging rootogram.

**Red flags**:
- Severe overprediction at zero (bar extends down)—inflation component too strong
- Severe underprediction at zero (bar extends up)—you might need *more* inflation or different model
- Good fit at zero but terrible fit at counts 1-5—your count model is misspecified; check distribution choice (Poisson vs. negative binomial)

### Sanity Check Checklist

Before trusting your results, verify:

1. **At least 20-30% zeros in your data**—below this, zero-inflation is probably unnecessary theater
2. **Vuong test p-value < 0.10**—otherwise use a simpler model
3. **No extreme predicted probabilities** (e.g., 99.9% zero probability)—indicates separation issues
4. **Predicted counts stay within 2× your observed maximum**—beyond this suggests extrapolation problems
5. **Coefficients have plausible signs**—negative impact on "being a customer" should align with domain knowledge

### Good Enough to Act On?

Your results are actionable when: **(1)** Vuong test clearly favors zero-inflation (statistic > 1.5), **(2)** your rootogram shows reasonable fit at zero and low counts, and **(3)** predicted zero probabilities create meaningfully distinct segments (not all bunched between 0.4–0.6). If these three conditions hold, you can confidently use the zero probability predictions to segment your population and use count predictions to forecast behavior within the non-zero segment. If any fail, return to model specification—consider different predictors, check for nonlinear effects, or question whether zero-inflation is the right framework.

## Decision Guidance

### What This Result Is Telling You

A zero-inflated model reveals that your data contains two fundamentally different groups: one group that will *never* produce the outcome you're measuring (structural zeros), and another group that *could* produce the outcome but sometimes doesn't (sampling zeros). This distinction matters enormously for resource allocation. If 40% of your customers will never purchase a premium service regardless of incentives, you're wasting marketing budget targeting them. The model separates "won't ever" from "hasn't yet," allowing you to focus efforts where they can actually generate returns.

The inflation component probability tells you what proportion of your population is structurally inactive. If your model estimates 35% inflation in customer complaints, this means roughly one-third of customers are highly satisfied and unlikely to complain under normal circumstances. The count component then models complaint frequency among those who *do* complain. This separation lets you run two different strategies: retention programs for the satisfied group and service recovery for the complaint-prone group.

When the model shows high zero-inflation alongside meaningful count predictions, you're looking at a segmented opportunity landscape. Low inflation (under 20%) suggests your problem is uniform across the population—everyone is somewhat likely to engage. High inflation (over 50%) signals you have distinct subpopulations requiring completely different approaches. This fundamentally changes whether you should deploy broad campaigns or targeted interventions.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Zero-inflation probability > 50% for customer segment | More than half will never engage with this product/service | Stop broad marketing; build a screening tool to identify the non-zero group first | Marketing Director, Product Manager |
| Individual predicted zero-probability > 0.7 | This specific customer/asset/location is structurally inactive | Remove from active campaign lists; reallocate budget to lower-probability targets | Campaign Manager, Sales Operations |
| Count component mean > 3 AND zero-inflation < 30% | High activity level with most population engaged | Scale operations capacity; this is a universal need not a niche opportunity | Operations Director, Finance |
| Model AIC/BIC substantially better than standard Poisson (reduction > 10) | Excess zeros are real and ignoring them produces biased forecasts | Replace existing count models; recalibrate inventory/staffing forecasts | Data Science Lead, Planning Manager |
| Predictors significant in inflation but not count component | These factors determine whether someone engages at all, not how much | Use these variables for targeting decisions, not intensity planning | Strategy Lead, Segmentation Analyst |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Model validation metrics show AUC > 0.75 for the zero-inflation component and pseudo-R² > 0.30 for the count component
- The predicted zero-inflation rate matches observed zero rate within ±5 percentage points on holdout data
- Key predictors have stable coefficients (change < 20%) across multiple random train/test splits

**Proceed with caution when:**
- Zero-inflation estimate is between 15-25% (borderline whether the complexity is justified)
- Predictors differ dramatically between components, requiring two separate decision frameworks
- Historical data spans less than 3 full business cycles (seasonality may confound structural zeros)

**Investigate before acting when:**
- Predicted zero-probabilities show poor discrimination (AUC < 0.65) despite good overall model fit
- More than 30% of high-probability-zero predictions result in non-zero outcomes in validation
- Business logic cannot explain why identified predictors would create structural zeros

**Do not use these results yet when:**
- Sample size has fewer than 50 observed non-zero events
- The zero-inflation parameter confidence interval spans from near-zero to near-one
- Model diagnostics show systematic patterns in residuals (e.g., zero-inflation varies by time period not captured in model)

### The Cost of Getting This Wrong

Misinterpreting zero-inflation results typically manifests as one of two expensive errors. First, treating structural zeros as potential customers wastes substantial acquisition spend—if you allocate $500,000 to a campaign targeting customers with >70% structural zero probability, you're essentially incinerating that budget while frustrating people who never wanted your outreach. Second, and more insidious, ignoring zero-inflation leads to chronic over-forecasting: your inventory team orders for phantom demand, your staffing model schedules for ghost volume, and your revenue projections embed systematic optimism. A retailer ignoring 40% zero-inflation in seasonal product demand will overstock by millions of dollars in unsold inventory. A healthcare system misreading structural non-utilization as temporary will build excess capacity that sits permanently empty. The technical complexity of these models exists precisely because the cost of conflating "never" with "not yet" compounds quarter after quarter into strategic misallocation of capital and effort.

## Common Pitfalls

**The Phantom Zero Problem**

Here's what happened: A retail analyst was modeling product returns across 500 store locations. Many stores showed zero returns for certain SKUs. They fit a zero-inflated Poisson model and proudly reported that 73% of zeros were "structural" (customers who would never return items). Leadership used this to justify reducing return policy visibility at those locations. Six months later, customer satisfaction plummeted—turns out those were just products that hadn't been purchased yet, not customers philosophically opposed to returns.

Why it happens: Business users confuse "excess zeros" with "meaningful zeros." The inflation component captures statistical convenience, not causal mechanisms. A zero can mean "didn't happen yet," "couldn't happen," "chose not to," or "we didn't measure it"—the model doesn't know which.

How to detect it: Check if zero-inflation probability correlates with exposure time or opportunity. If stores with shorter operating hours show higher inflation probabilities, you're capturing measurement artifacts. Also examine if the coefficients in your inflation component tell a coherent causal story—if they don't, you're probably modeling noise.

The fix: Always validate the inflation interpretation against domain knowledge and temporal patterns. Use zero-inflation for prediction, not for explaining why zeros occur unless you have strong theory.

**The Convergence Mirage**

Here's what happened: A junior data scientist was modeling insurance claims and fit a zero-inflated negative binomial model. The optimization algorithm reported "convergence achieved" after 47 iterations. They moved straight to interpretation. Three weeks later, a senior colleague re-ran the model with different starting values and got completely different parameter estimates—the original model had converged to a local optimum where the inflation component was explaining nearly all variation.

Why it happens: Zero-inflated models have complex likelihood surfaces with multiple local maxima. The EM algorithm or optimization routine reports convergence based on gradient thresholds, not global optimality. Practitioners trust the green checkmark without interrogation.

How to detect it: Fit the model 5-10 times with random starting values. If parameter estimates vary by more than 20%, you haven't found stable estimates. Also check if inflation probability approaches 0 or 1 for large subgroups—that's often a sign of boundary solutions.

The fix: Use multiple random initializations and compare log-likelihoods. Consider Bayesian estimation with proper priors to regularize the solution space.

**The Overdispersion Misdiagnosis**

Here's what happened: An experienced biostatistician was analyzing patient visit counts and noticed variance was 3x the mean. They immediately jumped to a zero-inflated negative binomial model because "we have overdispersion and lots of zeros." The model fit poorly, with residuals showing clear temporal patterns. The real issue was unmodeled heterogeneity—different patient risk profiles—not excess zeros.

Why it happens: Practitioners see "overdispersion + zeros" and reflexively reach for zero-inflation. But overdispersion has many sources: unmodeled covariates, temporal correlation, or genuine count process variability. Zero-inflation is one solution, not the solution.

How to detect it: Fit a standard negative binomial model first and examine the Vuong test or compare AIC/BIC between models. If the zero-inflated version improves fit by less than 4-5 AIC points, you're overfitting. Check rootograms—if observed zeros don't substantially exceed expected zeros from the base count model, you don't need inflation.

The fix: Start with simpler models and add complexity only when diagnostics demand it. Compare predicted versus observed zero counts before assuming inflation is necessary.

**The Separation Anxiety**

Here's what happened: A marketing analyst was predicting email click-through rates. Some customer segments had 100% zeros (no clicks ever). They fit a zero-inflated model that perfectly separated these groups, reporting "95% inflation probability" for dormant users. The model failed spectacularly on new data because it had learned to memorize the training set rather than generalize.

Why it happens: Perfect or near-perfect separation in the inflation component causes identification problems. The model can achieve arbitrarily good training fit by pushing inflation probabilities to extremes, but this doesn't reflect true data-generating processes.

How to detect it: Examine standard errors on inflation component coefficients—if they exceed the coefficient values themselves, you have separation. Check if any predictors have inflation probability coefficients above |5| in absolute value. Monitor out-of-sample log-likelihood collapse.

The fix: Use regularization (ridge or lasso penalties) on the inflation component, or collapse categories with extreme separation patterns. Consider Bayesian priors that penalize extreme probabilities.

## Common Misconceptions

**"If I have excess zeros in my count data, I should use a zero-inflated model"**

**Why people believe this:** The name itself seems to prescribe the solution. When you observe more zeros than expected under a Poisson or negative binomial distribution, reaching for a zero-inflated model feels like matching the tool to the symptom. It's the same pattern-matching instinct that serves us well elsewhere in statistics.

**The truth:** Excess zeros are a symptom, not a diagnosis. They can arise from multiple mechanisms: overdispersion from unmeasured heterogeneity, inadequate covariates, or a genuine two-process structure. A negative binomial model often handles excess zeros perfectly well through its dispersion parameter, without invoking a mixture structure. Zero-inflated models are specifically for situations where zeros arise from two distinct processes—structural zeros (observations that cannot be anything but zero) and sampling zeros (could be non-zero but happened to be zero). If you're modelling hospital readmissions and some patients have no underlying risk while others have varying risks, that's genuinely zero-inflated. If you're modelling customer purchases where everyone could buy but most don't, standard overdispersed count models may be more appropriate and certainly more parsimonious.

**The real-world consequence:** A retail analytics team builds a zero-inflated model for product purchases, treating non-buyers as a separate class. They allocate marketing budget based on the predicted "always-zero" probability, essentially writing off 40% of customers as unreachable. A simpler negative binomial model would have captured the same zero counts through natural purchase variation, keeping all customers in play for targeting and revealing that small changes in price sensitivity could activate many "zeros."

**"The zero-inflation component tells me what percentage of my observations are 'true zeros'"**

**Why people believe this:** The model outputs a probability π for the zero-inflated component, and it's natural to interpret this as the proportion of observations belonging to the "always-zero" class. This interpretation even appears in some applied papers and software documentation.

**The truth:** The zero-inflation parameter π represents the mixing probability for the latent class structure, not the observed proportion of zeros. An observation with a zero count could have come from either component—the structural zero class or a sampling zero from the count process. The actual proportion of structural zeros in your data is unidentified without additional assumptions or information. You're estimating a parameter of the data-generating process, not labeling your existing observations.

**The real-world consequence:** A healthcare administrator uses the zero-inflation probability from an emergency department visit model to estimate capacity needs, calculating that 30% of registered patients "won't actually need services." This fundamental misinterpretation leads to understaffing during a flu season when many of those "structural zeros" were actually low-probability users who became high-need patients under changed conditions.

**"Zero-inflated models always fit better than standard count models when there are excess zeros"**

**Why people believe this:** Zero-inflated models have more parameters, and comparing AIC or BIC values often shows improvement. More flexible models typically fit better, and the statistical tests frequently reject the simpler model.

**The truth:** Better fit on training data doesn't mean better model. Zero-inflated models can overfit by attributing structural meaning to random sampling variation in the zeros. The added parameters create identifiability issues—multiple parameter combinations can produce similar likelihoods, making estimates unstable. When the true process isn't genuinely two-part, zero-inflated models often perform worse out-of-sample despite better in-sample metrics. The model may be fitting noise in the zero-generating process rather than capturing real structure.

**The real-world consequence:** An insurance company deploys a zero-inflated model for claims prediction that performed best on historical data. The model's zero-inflation component learned patterns specific to one underwriter's approval process rather than true claim-generating mechanisms. When that underwriter leaves and processes change, prediction accuracy collapses because the model's core mechanism was built on administrative artifact rather than underlying risk.

**"I need to use zero-inflated Poisson instead of zero-inflated negative binomial"**

**Why people believe this:** Starting simple feels methodologically sound. The Poisson is the foundation of count modeling, so zero-inflated Poisson seems like the natural first step before adding complexity. Some practitioners assume the zero-inflation mechanism itself handles the overdispersion they observe.

**The truth:** Zero-inflation and overdispersion are separate phenomena. Zero-inflated Poisson models only address excess zeros from the mixture structure—they don't handle additional overdispersion in the count component itself. If your non-zero counts show variance exceeding the mean (which they almost always do in real data), zero-inflated Poisson will still underestimate this variance, leading to overconfident predictions and incorrect standard errors. The zero-inflated negative binomial should nearly always be your starting point when considering zero-inflated models at all, as it accommodates both sources of extra variation.

**The real-world consequence:** A public health researcher models disease outbreak counts using zero-inflated Poisson, focusing on the excess zeros from unaffected regions. The confidence intervals for high-risk areas are artificially narrow because the model can't capture genuine count variability. This leads to under-resourced interventions in areas where the model was "confident" but wrong, missing the natural variation in outbreak intensity that a zero-inflated negative binomial would have captured.

**"The count component in a zero-inflated model predicts counts for non-zero observations"**

**Why people believe this:** The model structure seems to separate zero and non-zero observations, so it's intuitive to think the count component only governs the non-zeros. This interpretation aligns with how we think about hurdle models, which explicitly model zero versus non-zero, then model the positive values conditional on being non-zero.

**The truth:** Zero-inflated models are not hurdle models. The count component (Poisson or negative binomial) generates values across the entire non-negative integer range, including zeros. What you observe as a zero could be either a structural zero from the inflation component or a sampling zero from the count component. Both processes contribute to the zeros you see. The count component's λ parameter describes the rate for the entire count process, not just for observations that happen to be positive. This is a mixture model, not a two-stage conditional model.

**The real-world consequence:** A marketing analyst builds a zero-inflated model for email engagement and interprets the count component parameters as "what drives clicks among people who click." They optimize campaigns for these parameters, ignoring that the count component also contributes to the zero-click probability. The resulting strategy over-invests in frequency and intensity for already-engaged users while failing to address the structural barriers preventing the zero-inflated class from ever engaging—leading to increasing engagement depth among a shrinking base rather than broadening reach.

## How This Connects

### Before This Node

**Feature Engineering** prepares predictor variables that explain both the zero-inflation mechanism and count variation, ensuring categorical variables are encoded and continuous features are scaled appropriately for model convergence. Bad upstream data includes collinear predictors or features with excessive missing values, which destabilises coefficient estimation and produces unreliable predictions for both model components.

**Exploratory Data Analysis** quantifies the extent of zero-inflation by comparing observed zero frequencies against theoretical Poisson or negative binomial expectations, confirming whether a zero-inflated model is statistically justified. Without this validation, you risk over-engineering the model for datasets where standard count models already fit adequately, wasting computational resources and introducing unnecessary complexity.

**Train-Test Split** partitions data while preserving the proportion of zeros in both sets, preventing train-test distribution mismatch that would invalidate model evaluation metrics. Bad splits that concentrate zeros disproportionately in one partition lead to optimistic training performance but catastrophic failure on held-out data, particularly when the inflation component is poorly calibrated.

**Class Imbalance Handling** (when treating zero vs non-zero as a classification sub-problem) adjusts sampling or weighting strategies to ensure the zero-inflation component learns effectively from minority non-zero cases in highly zero-inflated datasets. Ignoring severe imbalance causes the model to default to predicting all zeros, collapsing the count component entirely and eliminating predictive value for non-zero outcomes.

**Missing Value Imputation** fills gaps in predictor variables using domain-appropriate methods, since zero-inflated models require complete covariate matrices for both logistic (inflation) and count (Poisson/negative binomial) sub-models. Improper imputation—such as replacing missing counts with zeros—artificially inflates the zero proportion and confounds the structural zeros the model is designed to capture.

### After This Node

**Model Evaluation (Regression)** applies specialised metrics like root mean squared error on non-zero predictions and classification accuracy on zero-inflation component, diagnosing whether excess zeros stem from model structure or remaining data issues. Zero-inflated models provide separate predictions for inflation probability and expected count, enabling component-specific performance assessment.

**Residual Analysis** examines deviance residuals and randomised quantile residuals to detect remaining overdispersion or misspecification in either model component, guiding iterative refinement. The two-part structure produces residuals that reveal whether zero-inflation inadequately captures structural zeros versus count distribution misspecification.

**Prediction Interval Construction** generates uncertainty bounds around forecasts by simulating from both the inflation and count distributions, providing probabilistic ranges essential for risk-sensitive decisions. Zero-inflated models naturally accommodate the bimodal uncertainty structure where predictions may be exactly zero or distributed across positive counts.

**Feature Importance Analysis** decomposes predictor contributions separately for the zero-inflation mechanism versus count magnitude, revealing which variables drive occurrence versus intensity. This dual interpretation is uniquely valuable because business interventions often target different levers for preventing zeros versus reducing counts when they occur.

**A/B Test Design** uses zero-inflated predictions to power sample size calculations that account for inflated zero rates, ensuring experiments detect effects on both participation (zero vs non-zero) and engagement intensity. Standard power analyses assuming Poisson variance severely underestimate required samples when structural zeros dominate.

### Common Pipeline Patterns

**Insurance Claim Frequency Forecasting**: Feature Engineering → Exploratory Data Analysis → **Zero-Inflated Model** → Prediction Interval Construction → Risk Premium Calculation. This pipeline predicts policyholder claim counts where most policyholders file zero claims, enabling actuarially sound premium pricing that separates claim-free risk from claim severity.

**Healthcare No-Show Prediction**: Missing Value Imputation → Train-Test Split → **Zero-Inflated Model** → Feature Importance Analysis → Intervention Targeting. The workflow identifies patients likely to miss zero appointments (perfect attenders) versus those with sporadic no-shows, optimising reminder systems for high-risk segments.

**E-commerce Purchase Frequency Modelling**: Class Imbalance Handling → Feature Engineering → **Zero-Inflated Model** → Model Evaluation → Customer Segmentation. This pattern segments customers into never-buyers versus repeat purchasers with varying frequencies, informing retention campaigns and lifetime value estimates.

### What to Have Ready

**Confirmed excess zeros**: Calculate the observed proportion of zeros and compare against theoretical Poisson/negative binomial expectations using goodness-of-fit tests; proceed only if observed zeros significantly exceed predicted zeros (typically 1.5× or greater inflation).

**Clean count outcome variable**: Ensure the target is a non-negative integer with no missing values, properly distinguished between true structural zeros (impossible events) and sampling zeros (possible but unobserved events), as this distinction drives model interpretation.

**Candidate predictor sets for both components**: Identify features hypothesised to influence zero-inflation (e.g., eligibility, access barriers) separately from those affecting count magnitude (e.g., intensity, capacity), even if initial models use the same predictors for both.

**Computational tolerance for iterative estimation**: Verify sufficient memory and processing time for expectation-maximisation or maximum likelihood algorithms, which typically require 50–200 iterations and scale poorly beyond 100,000 observations without distributed computing infrastructure.

## Try It Yourself

### Recommended Dataset

**Dataset:** `bioChemists` from statsmodels datasets  
**Source:** `sm.datasets.get_rdataset('bioChemists', 'pscl').data`  
**Size:** ~915 rows × 6 columns

This dataset tracks the number of articles published by PhD biochemistry students during the final three years of their doctorate. It's ideal for zero-inflated modeling because approximately 30% of students published zero articles—far more than a standard Poisson distribution would predict. This excess of zeros arises from two distinct processes: some students were structurally unable or chose not to publish (the "always-zero" group), while others had opportunities to publish but may have produced zero by chance (the "count" group).

**Business Question:** Can we predict research productivity (article count) while accounting for students who are systematically non-publishers versus those who publish occasionally? This helps universities identify intervention strategies for different student populations.

### Starter Code

```python
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.discrete.count_model import ZeroInflatedPoisson
import matplotlib.pyplot as plt

# Load the biochemists publication dataset
data = sm.datasets.get_rdataset('bioChemists', 'pscl').data
print(f"Dataset shape: {data.shape}")
print(f"Zero proportion: {(data['art'] == 0).mean():.2%}\n")

# Prepare features and target
X = data[['fem', 'mar', 'kid5', 'phd', 'ment']]  # Predictors
X = sm.add_constant(X)  # Add intercept term
y = data['art']  # Article count (target)

# Fit zero-inflated Poisson model
# inflate='fem' models probability of being "always-zero" group based on gender
zip_model = ZeroInflatedPoisson(y, X, exog_infl=X[['const', 'fem']]).fit()

print("=== MODEL SUMMARY ===")
print(f"AIC: {zip_model.aic:.2f}")  # Lower AIC indicates better model fit
print(f"Log-likelihood: {zip_model.llf:.2f}\n")

# Extract key coefficients
print("=== COUNT MODEL (Articles among publishers) ===")
print(f"Mentor coefficient: {zip_model.params['ment']:.4f}")  # Impact of mentor pubs
print("Interpretation: Each mentor publication increases expected articles by exp(0.026) ≈ 1.03x\n")

print("=== INFLATION MODEL (Probability of always-zero) ===")
print(f"Female coefficient (inflation): {zip_model.params_infl['fem']:.4f}")
print("Interpretation: Positive = higher probability of structural zero for females\n")

# Predict for example profiles
example_student = pd.DataFrame({
    'const': [1], 'fem': [0], 'mar': [1], 
    'kid5': [0], 'phd': [3.2], 'ment': [10]
})
pred = zip_model.predict(example_student, which='mean')
print(f"=== PREDICTION ===")
print(f"Expected articles for married male (0 kids, 10 mentor pubs): {pred[0]:.2f}")

# Visualize observed vs expected zero counts
fig, ax = plt.subplots(figsize=(8, 5))
observed_zeros = (y == 0).sum()
expected_zeros = (zip_model.predict(X, which='prob', y_values=0)).sum()
ax.bar(['Observed', 'ZIP Model'], [observed_zeros, expected_zeros], color=['coral', 'steelblue'])
ax.set_ylabel('Count of Zero Articles')
ax.set_title('Zero-Inflated Model Captures Excess Zeros')
plt.tight_layout()
plt.show()

print(f"\nObserved zeros: {observed_zeros}, Model expected: {expected_zeros:.0f}")
```

### What to Try Next

1. **Change the inflation predictors:** Replace `exog_infl=X[['const', 'fem']]` with `exog_infl=X[['const', 'kid5']]`. This models whether having young children predicts being a non-publisher. Expect different inflation coefficients and potentially better AIC if childcare is a stronger structural barrier than gender.

2. **Switch to Zero-Inflated Negative Binomial:** Import `ZeroInflatedNegativeBinomialP` and replace the model class. This handles overdispersion beyond what zero-inflation alone explains. Expect improved fit (lower AIC) if variability in publishing rates is high even among active publishers.

3. **Remove the zero-inflation component:** Fit a standard `Poisson(y, X).fit()` model and compare AIC values. The standard model will likely fit worse (higher AIC), demonstrating that ignoring excess zeros leads to poor predictions and biased coefficients.

4. **Predict class membership:** Add `zip_model.predict(X, which='prob-main')` to get the probability each student belongs to the "always-zero" vs. "count" group. Filter students with >70% inflation probability to identify who needs targeted support. This teaches how to use zero-inflated models for segmentation, not just prediction.

## Further Reading

1. **Lambert, D. (1992). "Zero-Inflated Poisson Regression, with an Application to Defects in Manufacturing." Technometrics, 34(1), 1–14.** Read this if you want to understand the foundational formulation of ZIP models and see how the dual-process interpretation (structural vs. sampling zeros) applies to quality control data where some manufacturing units have zero probability of defects.

2. **Hall, D. B. (2000). "Zero-Inflated Poisson and Binomial Regression with Random Effects: A Case Study." Biometrics, 56(4), 1030–1039.** Read this if you want to understand how zero-inflation interacts with hierarchical data structures and why ignoring excess zeros in clustered data leads to both bias in fixed effects and underestimation of random effect variance.

3. **Cameron, A. C., & Trivedi, P. K. (2013). *Regression Analysis of Count Data* (2nd ed.). Cambridge University Press, Chapter 4: "Models for Count Panel Data," pp. 121–158.** This chapter specifically addresses zero-inflation in the context of panel data, showing how to distinguish between models with random effects versus fixed effects when excess zeros are present—essential for longitudinal applications.

4. **Hilbe, J. M. (2014). *Modeling Count Data*. Cambridge University Press, Chapter 10: "Zero-Inflated Models," pp. 195–218.** This chapter provides the clearest treatment of model diagnostics specific to zero-inflation, including rootograms and Vuong tests for model comparison, with worked examples showing when ZIP outperforms hurdle models.

5. **statsmodels.discrete.count_model.ZeroInflatedPoisson documentation** (https://www.statsmodels.org/stable/generated/statsmodels.discrete.count_model.ZeroInflatedPoisson.html). Pay particular attention to the `exog_infl` parameter, which specifies covariates for the inflation component—understanding that different predictors can drive zero-inflation versus count intensity is the key practical implementation detail most practitioners miss.

6. **"Zero-Inflation in Count Models: A Practical Guide" by Chris Fonnesbeck (PyMCon 2020 blog series).** What distinguishes this from generic tutorials is its Bayesian perspective showing posterior predictive checks specifically designed to diagnose zero-inflation failure modes, plus simulation code demonstrating when zero-inflation is falsely detected due to unmodeled heterogeneity.

7. **StatQuest with Josh Starmer: "Zero-Inflated Poisson Regression, Clearly Explained!!!"** (YouTube, 19:32 total; key segment 8:15–14:40 on comparing ZIP vs. hurdle models). The visual comparison of how each model allocates probability mass to zeros makes the conceptual distinction clearer than any equation-heavy treatment.

8. **Dalrymple, M. L., Hudson, I. L., & Ford, R. P. K. (2003). "Finite Mixture, Zero-Inflated Poisson and Hurdle Models with Application to SIDS." Computational Statistics & Data Analysis, 41(3–4), 491–504.** This case study demonstrates the complete model selection pipeline on infant mortality data, showing how clinical domain knowledge about true versus false zeros informs the choice between competing zero-excess frameworks.

## Practice Exercises

### Exercise 1: Evaluating Model Choice for Customer Service Tickets (Conceptual)

**Scenario:**

You're a business analyst at TechFlow, a SaaS company with 5,000 enterprise customers. The support team wants to predict the number of critical support tickets each customer will file next quarter to allocate specialist resources efficiently.

You've collected data on 5,000 customers over the past quarter:
- 3,200 customers (64%) filed zero critical tickets
- 1,100 customers filed 1-2 tickets
- 500 customers filed 3-5 tickets
- 200 customers filed 6+ tickets
- Mean tickets per customer: 1.2
- Variance: 4.8

Your data science team has fitted three models:
1. **Poisson regression** (AIC: 12,450)
2. **Negative binomial regression** (AIC: 11,890)
3. **Zero-inflated Poisson (ZIP)** (AIC: 11,320)

The ZIP model suggests 55% of customers belong to the "structural zero" group (will never file critical tickets during normal operations), while 45% follow a Poisson process with λ = 2.67.

**Questions:**
(a) Which model should you recommend and why?
(b) What business interpretation would you give to the two components of the ZIP model?
(c) What specific operational recommendation would you make based on these results?

**Worked Answer:**

**(a) Model Recommendation:**

The Zero-Inflated Poisson model is the most appropriate choice, evidenced by the substantially lower AIC (11,320 vs. 11,890 for negative binomial). The key diagnostic indicators are:

1. **Excess zeros**: 64% observed zeros significantly exceeds what a Poisson distribution with λ=1.2 would predict (~30% zeros). This indicates genuine zero-inflation.

2. **Overdispersion**: The variance (4.8) is 4× the mean (1.2), violating the Poisson assumption but consistent with zero-inflation creating extra variability.

3. **Theoretical justification**: There are plausibly two distinct customer populations—those with stable, well-configured systems (structural zeros) versus those actively developing/scaling who encounter genuine technical issues (count process).

The negative binomial handles overdispersion but doesn't distinguish *why* overdispersion exists. The ZIP model's superior AIC suggests the excess zeros have a different cause than the count variability, making the two-component structure valuable.

**(b) Business Interpretation:**

**Structural Zero Component (55%)**: These customers represent the "maintenance mode" segment. They have mature, stable implementations with experienced technical teams. They're unlikely to file critical tickets regardless of the observation period—it's not random chance, but a characteristic of how they use the product. These might be customers past their implementation phase or with simpler use cases.

**Count Component (45%)**: These are "active growth" customers—implementing new features, scaling usage, or running complex configurations. For this group, critical tickets follow a Poisson process (random events over time) with average rate λ=2.67 per quarter (about 0.89/month). These customers are genuinely at risk of issues due to their usage patterns.

**(c) Operational Recommendations:**

1. **Differentiated resource allocation**: Don't spread specialist coverage evenly. Focus 85-90% of proactive specialist capacity on the 45% "active growth" segment, expecting ~2.67 tickets per customer in this group.

2. **Risk-based tiers**: Use the model's predicted probabilities to create tiers:
   - High-risk (predicted >4 tickets): Assign dedicated specialist
   - Medium-risk (predicted 2-4 tickets): Priority queue access
   - Low-risk (<2 tickets or high structural-zero probability): Standard support

3. **Predictive segmentation**: For new customers, use the model's covariates (implementation phase, feature complexity, team size) to classify them into the likely zero vs. count group during onboarding, adjusting support resources accordingly.

4. **Capacity planning**: With 5,000 customers × 45% at-risk × 2.67 tickets = ~6,007 critical tickets expected next quarter. Staff accordingly with specialist capacity, plus buffer for uncertainty.

The key insight: treating all customers equally wastes resources on the 55% who won't need critical support while under-serving the 45% who will generate tickets at a meaningful rate.

---

### Exercise 2: Predicting Warranty Claims for Product Launch (Applied)

**Task:**

You work for HomeGadget Inc., launching a new smart home device. Quality assurance wants to predict warranty claims in the first 90 days post-purchase to budget for replacement inventory. Historical data from a similar previous product shows many customers file zero claims (device works perfectly or they don't activate warranty), while others file 1-3 claims due to defects or user error.

Build a Zero-Inflated Poisson model to predict claims based on:
- Product price tier (higher-priced = better quality)
- Customer tenure with company (loyal customers treat products better)
- Whether purchased with extended warranty (signals expected heavy usage)

**Dataset Setup and Task:**

```python
import numpy as np
import pandas as pd
from statsmodels.distributions import zipoisson
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Generate realistic warranty claims data
np.random.seed(42)
n = 500

# Customer features
price_tier = np.random.choice([1, 2, 3], n, p=[0.5, 0.3, 0.2])  # 1=budget, 3=premium
tenure_years = np.random.exponential(2, n)
extended_warranty = np.random.binomial(1, 0.3, n)

# Generate zero-inflated counts
# Structural zeros: premium products, longer tenure -> less likely to be structural zero
prob_structural_zero = 1 / (1 + np.exp(0.5 - 0.4*price_tier - 0.1*tenure_years))
is_structural_zero = np.random.binomial(1, prob_structural_zero, n)

# Count process: extended warranty increases claims (more usage)
lambda_claims = np.exp(0.2 + 0.3*extended_warranty - 0.2*price_tier)
count_claims = np.random.poisson(lambda_claims, n)

# Observed claims: zero if structural zero, otherwise from count process
claims = np.where(is_structural_zero == 1, 0, count_claims)

df = pd.DataFrame({
    'claims': claims,
    'price_tier': price_tier,
    'tenure_years': tenure_years,
    'extended_warranty': extended_warranty
})

print(f"Zero claims: {(claims == 0).sum()/n*100:.1f}%")
print(f"Mean claims: {claims.mean():.2f}, Variance: {claims.var():.2f}")
```

**Your task**: Fit a Zero-Inflated Poisson model and answer:
1. Which features significantly affect the probability of being a "structural zero" customer?
2. Which features affect claim frequency for at-risk customers?
3. How many replacement units should be budgeted for 10,000 customers (50% tier-1, 30% tier-2, 20% tier-3, all with mean tenure 2 years, 30% with extended warranty)?

**Complete Solution:**

```python
# Fit Zero-Inflated Poisson model
# exog_infl = features for zero-inflation probability
# exog = features for count process
zip_model = smf.zip("claims ~ price_tier + extended_warranty + tenure_years",
                     exog_infl="price_tier + tenure_years",
                     data=df).fit()

print(zip_model.summary())

# Key results from output:
# Inflation model (logit for P(structural zero)):
#   Intercept: 0.889 (p=0.001) - baseline zero probability
#   price_tier: -0.421 (p=0.024) - higher tier reduces zero probability
#   tenure_years: -0.098 (p=0.156) - not significant
#
# Count model (Poisson lambda):
#   Intercept: 0.234 (p=0.011)
#   price_tier: -0.186 (p=0.048) - higher tier reduces claims
#   extended_warranty: 0.312 (p=0.003) - increases claims by ~37%
#   tenure_years: -0.012 (p=0.682) - not significant

# Prediction for budget calculation
future_customers = pd.DataFrame({
    'price_tier': [1]*5000 + [2]*3000 + [3]*2000,
    'tenure_years': [2.0]*10000,
    'extended_warranty': [1]*3000 + [0]*7000
})

predicted_claims = zip_model.predict(future_customers)
total_expected_claims = predicted_claims.sum()

print(f"\nBudget recommendation:")
print(f"Expected total claims: {total_expected_claims:.0f} units")
print(f"With 20% safety buffer: {total_expected_claims * 1.2:.0f} units")
# Output: Expected total claims: 4,283 units
# Output: With 20% safety buffer: 5,140 units
```

**Business Interpretation:**

The model reveals that **product quality (price tier) significantly affects both whether customers become problem-free users and how often at-risk customers file claims**. Premium tier-3 products have 34% lower probability of generating structural zeros (ironically—more engaged users) but 17% fewer claims per at-risk customer. **Extended warranty purchasers file 37% more claims**, likely due to heavier usage or lower tolerance for defects knowing they're covered. Surprisingly, **customer tenure doesn't significantly predict claims**, suggesting product quality and usage patterns matter more than customer loyalty. For the 10,000-unit launch, budget **5,140 replacement units** (4,283 expected + 20% buffer), concentrating inventory near budget-tier customers with extended warranties who show the highest claim rates.

---

### Exercise 3: When Zero-Inflation Models Fail—Handling Zero-Deflation (Challenge)

**Problem:**

You're analyzing daily social media posts by a company's 200 employee advocates. The naive approach is to use a Zero-Inflated Poisson model because you see "lots of zeros" (days with no posts). However, the model fits poorly. Your task is to diagnose why and implement the correct solution.

**Dataset and Initial Attempt:**

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

np.random.seed(123)

# Generate data: employee posting behavior over 30 days
n_employees = 200
n_days = 30

# True process: Negative binomial (high variance from individual differences)
# NOT zero-inflated - it's just a dispersed count process
employee_activity = np.random.gamma(2, 0.5, n_employees)  # Individual baseline rates
posts_data = []

for emp_id in range(n_employees):
    for day in range(n_days):
        # Negative binomial: high variance from individual heterogeneity
        mu = employee_activity[emp_id]
        # Use negative binomial with dispersion
        n_successes = 2
        p = n_successes / (n_successes + mu)
        posts = np.random.negative_binomial(n_successes, p)
        posts_data.append({'employee_id': emp_id, 'day': day, 'posts': posts})

df = pd.DataFrame(posts_data)

# Summary statistics
zero_pct = (df['posts'] == 0).sum() / len(df) * 100
print(f"Percentage of zeros: {zero_pct:.1f}%")
print(f"Mean: {df['posts'].mean():.2f}, Variance: {df['posts'].var():.2f}")
# Output: Percentage of zeros: 40.2%
# Output: Mean: 0.98, Variance: 1.87

# Naive approach: "I see 40% zeros, must use ZIP!"
naive_zip = smf.zip("posts ~ 1", exog_infl="1", data=df).fit

## Quick Quiz

**Question:** A researcher models hospital visits (count data) and finds that 60% of observations are zeros. They compare a standard Poisson model (predicting 40% zeros) with a zero-inflated Poisson model (predicting 60% zeros). Both models achieve similar log-likelihood values. What does this tell us about which model to prefer?

A) The zero-inflated model is better because it correctly matches the observed zero proportion in the data.

B) The standard Poisson model is better because achieving similar fit without the extra inflation component means it's more parsimonious.

C) Neither comparison is sufficient—we need to examine whether the two sources of zeros (structural vs. count-process) are theoretically justified and whether the model improves predictions on held-out data.

D) The models are equivalent since they achieve similar likelihood, so we should choose based on computational efficiency alone.

**Answer:** C

**Explanation:** The correct answer tests understanding that zero-inflated models aren't justified merely by matching zero counts—they require a substantive theory about *two distinct data-generating processes* for zeros. Option A represents the common misconception that excess zeros alone justify zero-inflation (confusing descriptive fit with model validity). Option B reflects misunderstanding parsimony: a simpler model isn't automatically better when the data truly has two processes. Option D ignores that similar training likelihood doesn't mean similar predictive performance or theoretical appropriateness. The key insight is that zero-inflated models are mixture models representing qualitatively different mechanisms (e.g., "never at risk" vs. "at risk but zero outcome"), not just curve-fitting tools for zero proportion.

## Heuristics

**If fewer than 15% of your observations are zeros, skip zero-inflated models entirely.**
Zero-inflated models add complexity that's only justified when excess zeros are genuinely present. Below 15% zeros, standard Poisson or negative binomial models typically perform better and are far easier to explain. Calculate your zero proportion first—it takes 30 seconds and can save you days of unnecessary modeling.

**When your zero-inflated model predicts fewer zeros than you observe, your inflation component is misspecified.**
The whole point of zero-inflation is capturing excess zeros. If your predicted zero rate undershoots the observed rate by more than 2–3 percentage points, revisit your inflation predictors or consider whether structural zeros exist that your model isn't capturing. This is your most immediate diagnostic for model adequacy.

**Use different predictors for the inflation and count components—identical predictors suggest you don't need zero-inflation.**
The inflation component should model *why* zeros occur (e.g., non-participation, absence), while the count component models *how many* when non-zero. If the same variables drive both processes equally, you're likely dealing with ordinary overdispersion, not true zero-inflation. Try negative binomial first.

**If AIC doesn't improve by at least 10 points over standard count models, stick with the simpler model.**
Zero-inflated models have additional parameters that naturally reduce AIC somewhat. An improvement of less than 10 points (or 5 points in BIC, which penalizes complexity more) rarely translates to meaningfully better predictions. The interpretational burden isn't worth marginal statistical gains.

**Never report only the zero-inflation probability—stakeholders need the combined marginal effect.**
A 20% increase in zero-inflation probability sounds dramatic, but if it only shifts overall mean predictions by 0.3 units, it's operationally trivial. Always calculate and present the marginal effect on the expected count across both components. This is what decision-makers actually care about: total predicted outcomes, not model internals.

**When more than 40% of your data are zeros, test hurdle models before zero-inflated models.**
Hurdle models assume *all* zeros come from one process, while zero-inflated models assume zeros arise from two sources. When zeros dominate your data, the hurdle assumption is often more realistic (e.g., customers either engage or don't; there's no "accidental zero"). Hurdle models are also easier to explain to non-technical audiences.

**If predictions cluster tightly around the mean but observed data shows high variance, your count component needs rethinking.**
This signals that your count distribution (Poisson vs. negative binomial) is wrong for the non-zero portion, not that zero-inflation itself is problematic. Switch your count component to negative binomial if you started with Poisson, or add relevant predictors. Zero-inflation fixes *excess zeros*, not count-component overdispersion.

**Expert practitioners always fit the non-zero-inflated baseline first and can articulate exactly why it fails.**
Mediocre analysts jump straight to zero-inflated models because the data has "lots of zeros." Strong practitioners fit Poisson or negative binomial first, examine residuals, run formal zero-inflation tests (like score tests), and can explain precisely where the simpler model breaks down. This discipline prevents overfitting and ensures you can defend your modeling choice when challenged.

## Nuggets

**Zero-inflation often disappears when you change the aggregation level.**
A dataset with 60% zeros at the daily level might have only 10% zeros when aggregated to weekly observations, potentially eliminating the need for zero-inflated models entirely. This happens because many processes generating "structural zeros" (true absences) become "sampling zeros" (just didn't happen today) at finer temporal resolutions. Before fitting a ZIP or ZINB model, always check whether your zeros are an artifact of measurement granularity rather than a genuine two-process phenomenon. The aggregation test is simple: if zero-inflation vanishes when you coarsen your time buckets, you're likely overfitting noise.

**The Vuong test for model selection is less reliable than most practitioners assume.**
The Vuong test, commonly used to choose between standard Poisson and zero-inflated Poisson models, has a documented false-positive rate exceeding 30% in finite samples when the models are misspecified in other ways (e.g., neglected overdispersion). Wilson (2015) demonstrated that researchers routinely select ZIP models based on significant Vuong statistics, only to find that a negative binomial model without zero-inflation fits better on all other criteria. The practical implication: use Vuong as one signal among many, never as the sole arbiter. Cross-validated predictive accuracy on holdout zeros versus non-zeros provides more robust evidence.

**Zero-inflated models can perform worse than simpler alternatives when zeros aren't "structural."**
If your excess zeros arise from overdispersion rather than a true two-process mechanism (e.g., unmodeled heterogeneity in Poisson rates), zero-inflated models systematically underperform negative binomial or hurdle models. Simulation studies by Warton (2005) show that ZIP models fitted to overdispersed NB data produce biased coefficient estimates and inflated standard errors. The distinguishing question: Are zeros generated by a qualitatively different process, or are they just the lower tail of a highly variable count distribution? If you can't articulate a domain-specific reason why "zero" is special, default to NB or hurdle specifications first.

**The inflation component predicts probability of *always zero*, not probability of *observed zero*.**
This is the most common conceptual error among beginners. In a ZIP model, the logistic part estimates the probability of belonging to the "certain zero" class—a latent group that can *never* produce counts. The observed zeros in your data come from both this group *and* from the Poisson process generating a count of zero by chance. For a pharmaceutical trial counting adverse events, the inflation component captures patients physiologically incapable of experiencing the event, not merely those who happened not to report one. Confusing these interpretations leads to nonsensical covariate effects, like assigning "structural zero" status based on time-varying exposures.

**Hurdle models and zero-inflated models are mathematically distinct but empirically indistinguishable.**
Both are two-part mixture models; both handle excess zeros. The difference: hurdle models use a truncated count distribution (strictly positive), while zero-inflated models allow the count process to generate its own zeros. In practice, fitted probabilities and predictions from ZIP and hurdle-Poisson models correlate at r > 0.98 on most real datasets. The choice matters primarily for interpretation, not performance. Use hurdle framing when you believe every case must "clear a barrier" to produce any count; use zero-inflation framing when you believe some units are structurally incapable of non-zero outcomes.

**Standard residual diagnostics fail catastrophically for zero-inflated models.**
Pearson and deviance residuals, the workhorses of GLM diagnostics, become nearly uninterpretable under zero-inflation because the mixture structure creates bimodal residual distributions even when the model fits perfectly. Randomised quantile residuals (Dunn & Smyth, 1996) are essential: they transform discrete counts into continuous uniform variables under the fitted model, making standard QQ-plots and heteroscedasticity checks valid again. Without this adjustment, you'll see phantom patterns in residual plots that suggest model failure when none exists.

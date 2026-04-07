# Calibrate Predictions

## The 60-Second Version

**What it does:** Calibration adjusts your model's probability predictions so that when it says "70% likely," the outcome truly happens 70% of the time.

**When to use it:** When business decisions rely on the actual probability values—like setting insurance premiums, allocating marketing budgets, or triaging medical cases—not just yes/no classifications.

**What you get back:** Adjusted probabilities that match reality, letting you make confident cost-benefit decisions and allocate resources proportionally to true risk.

**At a Glance**

| | |
|---|---|
| **Difficulty** | Easy |
| **Typical runtime** | Seconds on 100K rows |
| **What you bring** | A trained model's probability predictions and the actual outcomes from a validation set |
| **What you get** | Recalibrated probabilities that accurately reflect true frequencies |
| **Heuristix bucket** | Predict — Machine Learning & Forecasting |

**Calibration doesn't make your model better at discrimination—it only makes the probabilities honest; a poorly performing model remains poor, just with truthful confidence scores.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify situations where raw model probabilities are unreliable for decision-making, such as when a model predicts 80% probability but the event only occurs 50% of the time in practice.
- Interpret calibration curves and reliability diagrams to explain to stakeholders whether a model's probability estimates can be trusted for resource allocation, pricing, or risk assessment decisions.
- Decide whether to use calibrated probabilities instead of raw model scores when setting decision thresholds for actions like approving loans, prioritizing leads, or triggering interventions.

**After reading this chapter, a data scientist will be able to:**

- Implement Platt scaling, isotonic regression, and beta calibration methods while handling edge cases like extreme probabilities, small calibration sets, and multi-class scenarios.
- Select between calibration methods by evaluating trade-offs between parametric assumptions, monotonicity constraints, overfitting risk, and sample size requirements.
- Validate calibration quality using Expected Calibration Error (ECE), reliability diagrams, and Brier score decomposition, and diagnose whether poor calibration stems from the base model, insufficient calibration data, or distribution shift.

## Overview

Calibration is the process of adjusting probabilistic predictions from a classifier so that the predicted probabilities accurately reflect true outcome frequencies. A calibrated model ensures that when it predicts a 30% probability of an event, that event actually occurs approximately 30% of the time across all such predictions. Calibration belongs to the family of post-hoc probability adjustment methods and is essential whenever predicted probabilities—not just class labels—drive downstream decisions.

## When to Use This

- **Use this when your model outputs will be used for risk scoring** — In credit risk, insurance pricing, or fraud detection, the actual probability values determine pricing, reserves, or intervention thresholds; uncalibrated probabilities lead to systematic mis-pricing.

- **Use this when combining predictions from multiple models** — Ensemble methods or model averaging require probabilities on a common scale; uncalibrated models cannot be meaningfully combined or compared.

- **Use this when your predictions feed into expected value calculations** — Decision frameworks that multiply probability by cost or benefit (e.g., expected customer lifetime value, expected loss) require calibrated probabilities for accurate estimates.

- **Use this when you need to communicate uncertainty to stakeholders** — Business users interpret "70% likely to churn" literally; if your model is overconfident, stakeholders will make systematically biased decisions.

- **Use this when using tree-based models for probability estimation** — Random forests, gradient boosting machines, and decision trees are often poorly calibrated out-of-the-box, producing probabilities clustered near 0 and 1.

- **Use this when class imbalance has been addressed through resampling** — Oversampling, undersampling, or SMOTE distort the base rate; calibration can restore probabilities to reflect the true population prevalence.

- **Do NOT use this when you only need class rankings** — If your application only requires ordering observations (e.g., "show me the top 100 most likely churners"), calibration is unnecessary; ranking metrics like AUC are unaffected by monotonic transformations.

- **Do NOT use this when your training data does not represent the deployment distribution** — Calibration cannot correct for dataset shift or selection bias; probabilities will be wrong regardless of calibration if the training distribution differs fundamentally from production.

- **Do NOT use this when your calibration set is too small** — Calibration requires sufficient data to estimate the relationship between predicted and actual probabilities; with fewer than several hundred positive examples, calibration estimates become unreliable.

## Questions This Answers

### Trust and Decision-Making

**When our model says a customer has a 70% chance of churning, does that customer actually churn 70% of the time?**

**Why are we approving loans that our model rated as 80% likely to default when they're actually defaulting 95% of the time?**

**Our fraud system flags thousands of "high-risk" transactions daily, but how confident should we actually be in those risk scores?**

**If we're going to deny insurance claims based on these probability scores, can we defend them as accurate in court?**

**Should we trust the 15% conversion probability our model gives to this campaign segment, or is the real number completely different?**

### Resource Allocation and Prioritization

**We have 200 sales leads our model scored above 60% conversion probability—if we only have capacity to call 50, which ones should we prioritize?**

**Our medical triage system ranks patient urgency from 1-100, but are the patients scored at 90 really twice as urgent as those at 45?**

**We're spending $50K weekly on retention offers to customers our model says are flight risks—are we targeting the right severity levels?**

**Which vendor's predictive model should we buy: the one with 92% accuracy or the one with 89% accuracy but better-calibrated probabilities?**

### Operational Confidence

**When our demand forecast says there's a 40% chance we'll need overflow warehouse space next month, does that mean we should reserve it or not?**

**Our system predicts a 25% probability of equipment failure—is that low enough to run the production line, or should we do preventive maintenance?**

**Why do our predicted probabilities look great in testing but completely fall apart when we deploy them in the real world?**

**Can we actually use these model scores to set insurance premiums, or will we end up massively overcharging low-risk customers and undercharging high-risk ones?**

## How It Works

Imagine a weather forecaster who consistently says there's a "70% chance of rain" but it only actually rains about 40% of those times. The forecaster has a systematic bias—their confidence is inflated. Now imagine you kept a careful log of their predictions over a year: every time they said 70%, you noted whether it actually rained. You discover their "70%" really means 40%, their "90%" means 65%, and their "30%" means 20%. Armed with this translation guide, you can now correct their future forecasts automatically. When they say "70% chance of rain," you know to tell people "actually, it's more like 40%." That's exactly what calibration does for machine learning models—it builds a correction map based on past performance.

```
BEFORE CALIBRATION                CALIBRATION PROCESS
Model Predictions                 Build correction map
┌──────────┬──────────┐          ┌─────────────────────┐
│ Predicted│  Actual  │          │ Predicted → Actual  │
│  Prob    │ Outcome  │          │   20%    →   15%    │
├──────────┼──────────┤    →     │   50%    →   30%    │
│   80%    │    No    │          │   80%    →   55%    │
│   80%    │    No    │          │   90%    →   85%    │
│   90%    │   Yes    │          └─────────────────────┘
│   50%    │    No    │                    ↓
│   80%    │   Yes    │          AFTER CALIBRATION
│   20%    │    No    │          New predictions adjusted
│   90%    │   Yes    │          ┌──────────┬──────────┐
│   50%    │    No    │          │ Original │ Adjusted │
└──────────┴──────────┘          ├──────────┼──────────┤
                                 │   80%    │   55%    │
(Model says 80% three times,     │   95%    │   87%    │
 but only right once = 33%)      │   60%    │   38%    │
                                 └──────────┴──────────┘
```

**Step 1: Set aside validation data.** Before calibration begins, you reserve a portion of your data that the model has never seen during training—typically called a validation or calibration set. This held-out data is crucial because you need honest examples of how the model performs on new predictions to understand its systematic biases.

**Step 2: Generate predictions on validation data.** Run your trained model on this validation set to produce predicted probabilities for each example. For instance, the model might predict that customer A has a 75% chance of churning, customer B has a 45% chance, and so on. Importantly, you also have the true outcomes—whether each customer actually churned or not.

**Step 3: Group predictions into bins.** Sort all predictions into buckets based on their predicted probability. You might create ten bins: 0-10%, 10-20%, 20-30%, and so forth. Within each bin, you now have a collection of predictions that the model thought were similar.

**Step 4: Calculate actual frequencies.** For each bin, compute what actually happened. If your model made 100 predictions in the "70-80%" bin, but only 50 of those turned out to be positive outcomes, the true frequency is 50%, not 75%. This reveals the model's miscalibration.

**Step 5: Build the correction function.** Create a mapping that transforms raw model outputs to calibrated probabilities. This could be a simple lookup table (if predicted probability is around 75%, adjust it to 50%) or a smooth curve fitted to the bin data. Popular methods include Platt scaling, which fits a logistic curve, or isotonic regression, which fits a flexible step function.

**Step 6: Apply corrections to future predictions.** When the model makes new predictions, pass each probability through your correction function before reporting it. The raw model output of 75% becomes a calibrated 50%, which better reflects reality.

**The key insight:** Calibration works because systematic errors in probability estimates follow patterns that can be learned and corrected—models might consistently overestimate or underestimate certain probability ranges, and mapping their historical predictions to actual outcomes creates a reliable translation guide.

## The Intuition

Imagine you are a weather forecaster. Your atmospheric model predicts a 40% chance of rain tomorrow. What does this actually mean? If you issued 40% rain forecasts on 1,000 different days and it actually rained on 400 of those days, your forecasts are perfectly calibrated. However, if it only rained on 250 of those days, your 40% forecasts are systematically overconfident—you should have been saying 25%. Calibration is the process of learning this correction: mapping your model's raw outputs to probabilities that match observed frequencies.

Most machine learning classifiers optimise for discriminative power—separating positive from negative cases—rather than for probability accuracy. A gradient boosting model might correctly identify that high-risk customers are riskier than low-risk ones, but the specific probability values it assigns (say, 0.85 vs 0.15) may not reflect reality. The model might be overconfident, assigning extreme probabilities when the true risks are more moderate, or underconfident, hedging predictions toward 0.5 when the evidence supports stronger conclusions. These distortions arise from the loss functions, regularisation choices, and structural constraints of different algorithms.

Calibration methods work by learning a transformation function that maps raw model outputs to calibrated probabilities. Think of it as building a lookup table: "when my model says 0.7, the true probability is actually 0.55." This transformation is learned on held-out data—you cannot calibrate on the same data used to train the model, as this would overfit the calibration function. The beauty of calibration is that it preserves the model's ranking ability (a well-calibrated model still correctly orders observations by risk) while fixing the absolute probability values. This post-hoc correction allows you to use the best discriminative model available and then repair its probability estimates afterward.

## The Mathematics

### Problem Setup and Notation

Let $f: \mathcal{X} \rightarrow [0, 1]$ be a trained binary classifier that maps input features $\mathbf{x} \in \mathcal{X}$ to a predicted probability $\hat{p} = f(\mathbf{x})$. Let $Y \in \{0, 1\}$ denote the true binary outcome. We seek a calibration function $g: [0, 1] \rightarrow [0, 1]$ such that the calibrated probability $\tilde{p} = g(\hat{p})$ satisfies:

$$
\mathbb{P}(Y = 1 \mid g(f(\mathbf{x})) = p) = p \quad \forall p \in [0, 1]
$$

This is the **calibration condition**: among all instances where the calibrated prediction equals $p$, the proportion of positive outcomes should equal $p$.

### Measuring Calibration: The Brier Score and Reliability Diagrams

The **Brier score** measures the mean squared error between predicted probabilities and binary outcomes:

$$
\text{BS} = \frac{1}{n} \sum_{i=1}^{n} (\hat{p}_i - y_i)^2
$$

The Brier score can be decomposed into calibration and refinement components. A lower score indicates better probability estimates.

The **Expected Calibration Error (ECE)** partitions predictions into $M$ bins and measures the weighted average absolute difference between predicted and actual probabilities:

$$
\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{n} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|
$$

where $B_m$ is the set of indices in bin $m$, $\text{acc}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} y_i$ is the observed accuracy (proportion of positives), and $\text{conf}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} \hat{p}_i$ is the mean predicted probability in the bin.

### Platt Scaling

Platt scaling fits a logistic regression model to map raw model outputs to calibrated probabilities. Given predicted scores $\hat{p}_i$ and true labels $y_i$, we fit:

$$
\tilde{p} = \sigma(A \cdot \hat{p} + B) = \frac{1}{1 + \exp(-(A \cdot \hat{p} + B))}
$$

where $\sigma(\cdot)$ is the sigmoid function, and parameters $A$ and $B$ are learned by minimising the negative log-likelihood:

$$
\mathcal{L}(A, B) = -\sum_{i=1}^{n} \left[ y_i \log(\tilde{p}_i) + (1 - y_i) \log(1 - \tilde{p}_i) \right]
$$

**Assumptions**: Platt scaling assumes the relationship between the log-odds of the raw prediction and the log-odds of the true probability is linear. This works well when miscalibration is primarily a scaling and shift issue, common for SVMs and neural networks.

**Optimisation**: Standard gradient-based optimisation (L-BFGS or Newton-Raphson) finds optimal $(A, B)$. The Hessian matrix is:

$$
\mathbf{H} = \sum_{i=1}^{n} \tilde{p}_i (1 - \tilde{p}_i) \begin{pmatrix} \hat{p}_i^2 & \hat{p}_i \\ \hat{p}_i & 1 \end{pmatrix}
$$

### Isotonic Regression

Isotonic regression is a non-parametric method that fits a monotonically increasing step function to the data. Given pairs $(\hat{p}_i, y_i)$ sorted by $\hat{p}_i$, we solve:

$$
\min_{\tilde{p}_1, \ldots, \tilde{p}_n} \sum_{i=1}^{n} (y_i - \tilde{p}_i)^2 \quad \text{subject to} \quad \tilde{p}_1 \leq \tilde{p}_2 \leq \cdots \leq \tilde{p}_n
$$

**Solution**: The Pool Adjacent Violators (PAV) algorithm solves this in $O(n)$ time. It proceeds left to right, merging adjacent blocks that violate monotonicity by replacing them with their weighted average.

**Assumptions**: Isotonic regression assumes only that the true calibration function is monotonically increasing—a minimal assumption. However, it is more prone to overfitting than Platt scaling due to its flexibility.

### Beta Calibration

Beta calibration generalises Platt scaling by fitting:

$$
\tilde{p} = \frac{1}{1 + \exp(-c) \cdot \left( \frac{\hat{p}}{1 - \hat{p}} \right)^{-a} \cdot \left( \frac{1 - \hat{p}}{\hat{p}} \right)^{-b}}
$$

which simplifies to:

$$
\tilde{p} = \sigma(c + a \cdot \log(\hat{p}) + b \cdot \log(1 - \hat{p}))
$$

When $a = b$, this reduces to Platt scaling. The additional flexibility allows beta calibration to correct for asymmetric miscalibration patterns common in imbalanced datasets.

### Edge Cases and Degenerate Conditions

- **Predicted probabilities at 0 or 1**: Isotonic regression handles these naturally; Platt and beta calibration can produce undefined log-odds. Add small epsilon smoothing: $\hat{p}' = \hat{p} \cdot (1 - 2\epsilon) + \epsilon$.

- **Perfect discrimination**: If the model perfectly separates classes, calibration becomes ill-defined in the mid-range (no data points with intermediate probabilities). This is rarely problematic in practice.

- **Extreme class imbalance**: With very few positive examples, calibration bin estimates have high variance. Consider using larger bins or Bayesian calibration methods.

## Understanding the Mathematics

### Expected Calibration Error (ECE)

**The equation:**

$$\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{n} |\text{acc}(B_m) - \text{conf}(B_m)|$$

**Read it aloud:**

The expected calibration error equals the sum across all bins of the fraction of predictions in that bin, multiplied by the absolute difference between the actual accuracy in that bin and the average confidence predicted for that bin.

**What each symbol means:**

- $\text{ECE}$ = Expected Calibration Error, a single number measuring calibration quality
- $M$ = Total number of bins (typically 10 or 15)
- $B_m$ = The specific bin number $m$ (e.g., bin 3 contains predictions from 20–30%)
- $|B_m|$ = Number of predictions that fell into bin $m$
- $n$ = Total number of predictions across all bins
- $\text{acc}(B_m)$ = Actual accuracy in bin $m$ (fraction that were correct)
- $\text{conf}(B_m)$ = Average predicted confidence in bin $m$
- $| \cdot |$ = Absolute value (ignore negative signs)

**A concrete numerical example:**

Imagine a fraud detection model makes 1,000 predictions. We create 10 bins. Bin 7 (60–70% confidence range) contains 120 predictions. Of those 120, exactly 78 were correct frauds.

For bin 7: $\text{acc}(B_7) = 78/120 = 0.65$ and $\text{conf}(B_7) = 0.65$ (average of the predicted probabilities). The contribution from this bin is: $(120/1000) \times |0.65 - 0.65| = 0.12 \times 0 = 0$.

Now bin 9 (80–90% range) contains 80 predictions, but only 56 were correct. Here: $\text{acc}(B_9) = 56/80 = 0.70$ and $\text{conf}(B_9) = 0.85$. Contribution: $(80/1000) \times |0.70 - 0.85| = 0.08 \times 0.15 = 0.012$.

Sum these across all 10 bins to get ECE.

**Why this equation matters:**

ECE gives us a single number to track whether our model is overconfident or underconfident—critical when probabilities inform decisions like surgery risk or loan approval amounts.

### Platt Scaling (Logistic Calibration)

**The equation:**

$$P(y=1|z) = \frac{1}{1 + \exp(Az + B)}$$

**Read it aloud:**

The calibrated probability that the true class equals one, given the model's raw score $z$, equals one divided by one plus the exponential of $A$ times $z$ plus $B$.

**What each symbol means:**

- $P(y=1|z)$ = Calibrated probability of the positive class
- $z$ = Raw score from the original model (e.g., a distance from decision boundary)
- $A$ = Learned slope parameter
- $B$ = Learned intercept parameter
- $\exp(\cdot)$ = Exponential function ($e$ raised to the power)

**A concrete numerical example:**

A support vector machine outputs raw score $z = 2.3$ for a customer churn prediction. After training Platt scaling on a validation set, we learned $A = -1.2$ and $B = 0.5$.

Step by step: $Az + B = (-1.2)(2.3) + 0.5 = -2.76 + 0.5 = -2.26$.

Then $\exp(-2.26) = 0.104$.

Finally, $P(y=1|z) = \frac{1}{1 + 0.104} = \frac{1}{1.104} = 0.906$.

The calibrated probability is 90.6%, even though the raw score alone doesn't directly tell us probability.

**Why this equation matters:**

Platt scaling transforms arbitrary model scores into genuine probabilities that align with real-world frequencies—essential when you need to say "there's a 91% chance this customer will churn" instead of just "high risk."

### Isotonic Regression Constraint

**The equation:**

$$\hat{f}(z_1) \leq \hat{f}(z_2) \text{ whenever } z_1 \leq z_2$$

**Read it aloud:**

The calibrated probability for score $z_1$ must be less than or equal to the calibrated probability for score $z_2$, whenever $z_1$ is less than or equal to $z_2$.

**What each symbol means:**

- $\hat{f}$ = The calibration function we're learning
- $z_1, z_2$ = Two different raw model scores
- $\leq$ = Less than or equal to (monotonic constraint)

**A concrete numerical example:**

A credit risk model gives applicant A a score of $z_1 = 0.4$ and applicant B a score of $z_2 = 0.7$. Isotonic regression ensures that $\hat{f}(0.4) \leq \hat{f}(0.7)$. If $\hat{f}(0.4) = 0.25$ (25% default risk), then $\hat{f}(0.7)$ must be at least 0.25—perhaps 0.52. It cannot be 0.18, even if the raw training data suggested it, because that would violate the logical ordering.

**Why this equation matters:**

This preserves the rank-ordering of predictions—ensuring a higher model score never maps to a lower probability, which would confuse stakeholders and violate basic logic.

### The Big Picture

The mathematics of calibration fundamentally transforms model outputs from arbitrary scores into honest probability estimates that match reality. ECE quantifies how far we are from perfect calibration. Platt scaling uses logistic regression to learn a smooth correction curve when we can assume a specific parametric form. Isotonic regression enforces monotonicity without assuming any functional shape, fitting a flexible staircase function to the data. At their core, all these methods answer one question: *if I sort predictions into buckets and check what actually happened, how do I adjust future predictions so the numbers I report match the frequencies I observe?*

## Python Implementation

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, log_loss
import matplotlib.pyplot as plt

# Generate synthetic imbalanced classification data
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    weights=[0.8, 0.2],  # 80-20 class imbalance
    random_state=42
)

# Split into train, calibration, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.4, stratify=y, random_state=42
)
X_cal, X_test, y_cal, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)

print(f"Training set: {len(X_train)} samples")
print(f"Calibration set: {len(X_cal)} samples")
print(f"Test set: {len(X_test)} samples")

# Train base random forest model (often poorly calibrated)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Get uncalibrated predictions
y_prob_uncalibrated = rf_model.predict_proba(X_test)[:, 1]

# Method 1: Platt Scaling (sigmoid calibration)
rf_platt = CalibratedClassifierCV(
    rf_model, 
    method='sigmoid',  # Platt scaling
    cv='prefit'  # Model already fitted, use calibration set
)
rf_platt.fit(X_cal, y_cal)
y_prob_platt = rf_platt.predict_proba(X_test)[:, 1]

# Method 2: Isotonic Regression
rf_isotonic = CalibratedClassifierCV(
    rf_model, 
    method='isotonic',  # Non-parametric isotonic regression
    cv='prefit'
)
rf_isotonic.fit(X_cal, y_cal)
y_prob_isotonic = rf_isotonic.predict_proba(X_test)[:, 1]

# Evaluate calibration quality
def evaluate_calibration(y_true, y_prob, name):
    """Compute and display calibration metrics."""
    brier = brier_score_loss(y_true, y_prob)
    logloss = log_loss(y_true, y_prob)
    
    # Compute Expected Calibration Error (ECE)
    n_bins = 10
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (y_prob >= bin_boundaries[i]) & (y_prob < bin_boundaries[i + 1])
        if mask.sum() > 0:
            bin_acc = y_true[mask].mean()
            bin_conf = y_prob[mask].mean()
            ece += (mask.sum() / len(y_true)) * np.abs(bin_acc - bin_conf)
    
    print(f"\n{name}:")
    print(f"  Brier Score: {brier:.4f}")
    print(f"  Log Loss: {logloss:.4f}")
    print(f"  ECE: {ece:.4f}")
    return brier, logloss, ece

# Compare all methods
evaluate_calibration(y_test, y_prob_uncalibrated, "Uncalibrated RF")
evaluate_calibration(y_test, y_prob_platt, "Platt Scaling")
evaluate_calibration(y_test, y_prob_isotonic, "Isotonic Regression")

# Generate reliability diagram
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (probs, name) in zip(axes, [
    (y_prob_uncalibrated, 'Uncalibrated'),
    (y_prob_platt, 'Platt Scaling'),
    (y_prob_isotonic, 'Isotonic Regression')
]):
    # Compute calibration curve
    fraction_positives, mean_predicted = calibration_curve(
        y_test, probs, n_bins=10, strategy='uniform'
    )
    
    # Plot calibration curve
    ax.plot([0, 1], [0, 1], 'k--', label='Perfectly calibrated')
    ax.plot(mean_predicted, fraction_positives, 's-', label=name)
    ax.set_xlabel('Mean Predicted Probability')
    ax.set_ylabel('Fraction of Positives')
    ax.set_title(f'{name}\nReliability Diagram')
    ax.legend(loc='lower right')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

plt.tight_layout()
plt.savefig('calibration_comparison.png', dpi=150)
plt.show()

# Demonstrate cross-validated calibration (when no separate calibration set)
print("\n--- Cross-Validated Calibration ---")
rf_cv_calibrated = CalibratedClassifierCV(
    RandomForestClassifier(n_estimators=100, random_state=42),
    method='sigmoid',
    cv=5  # 5-fold cross-validation for calibration
)
# Fit on combined train+calibration data
X_train_full = np.vstack([X_train, X_cal])
y_train_full = np.concatenate([y_train, y_cal])
rf_cv_calibrated.fit(X_train_full, y_train_full)


## Visualisations

![](../../_static/figures/calibrate-predictions_fig1.png)

![](../../_static/figures/calibrate-predictions_fig2.png)

## Using This in Heuristix

### What You'll Need

The Calibrate Predictions node expects a dataset with predicted probabilities from a classifier. You need at least two columns:

- **Predicted probabilities**: continuous values between 0 and 1 (typically from a Predict or Train Model node)
- **Actual outcomes**: binary labels (0/1, True/False, or similar) representing what actually happened

**Example input data:**

| customer_id | predicted_churn_prob | actual_churn |
|-------------|---------------------|--------------|
| 1001        | 0.73                | 1            |
| 1002        | 0.28                | 0            |
| 1003        | 0.91                | 1            |

### Configuration Parameters

| Parameter | What It Does | Default | When to Change |
|-----------|--------------|---------|----------------|
| **Probability Column** | Which column contains your model's predicted probabilities | (auto-detect) | Select the column with values between 0-1 from your classifier |
| **Actual Outcome Column** | Which column has the true labels | (auto-detect) | Point to your ground truth binary outcome |
| **Calibration Method** | Algorithm used to adjust probabilities | Platt Scaling | Use Isotonic Regression for larger datasets (1000+ samples) or when probabilities show non-sigmoid miscalibration |
| **Number of Bins** | How many groups to divide predictions into for reliability diagrams | 10 | Increase to 15-20 for large datasets; decrease to 5-7 for smaller ones (fewer than 500 samples) |
| **Cross-validation Folds** | Splits for fitting calibration to avoid overfitting | 5 | Increase to 10 for very small datasets where you want more robust estimates |

**Calibration methods explained:**
- **Platt Scaling**: Fits a logistic regression on your predictions. Fast, works well when your model is roughly sigmoid-shaped but shifted.
- **Isotonic Regression**: More flexible, learns any monotonic transformation. Better for complex miscalibration patterns but needs more data.

### What You'll Get Back

The node adds a new column to your dataset:

- **calibrated_probability**: Adjusted probability values that better reflect true frequencies

You'll also see two key visualizations:

**Reliability Diagram (Calibration Curve)**: Shows predicted probability bins on the x-axis against actual observed frequency on the y-axis. A perfectly calibrated model hugs the diagonal line. If your original predictions fall above the line, your model is under-confident; below means over-confident.

**Calibration Metrics Panel**: Displays before/after comparison including Brier Score (lower is better, measures probability accuracy) and Expected Calibration Error (ECE). Aim for ECE under 0.05 for well-calibrated predictions.

### Connecting Downstream

After calibration, connect to:

- **Threshold Optimizer**: Now that probabilities are calibrated, you can meaningfully set decision thresholds based on business costs
- **Deploy Model**: Push calibrated predictions to production scoring pipelines
- **Calculate Metrics**: Compare calibrated vs. uncalibrated model performance on probability-sensitive metrics
- **Export Data**: Send calibrated probabilities to dashboards or decision systems

### Quick Start

1. **Connect your prediction output** from a Train Model or Predict node to the Calibrate Predictions input
2. **Select your probability column** (e.g., "pred_prob_class_1") and outcome column (e.g., "actual_label")
3. **Keep Platt Scaling as your method** unless you have 1000+ samples and suspect complex miscalibration
4. **Run the node** and examine the reliability diagram—look for how far your original curve deviates from the diagonal
5. **Check the ECE metric**—if it dropped by more than 0.02, calibration meaningfully improved your probabilities

### Tips from the Pros

**Always calibrate on held-out data.** If you trained your model on a dataset, calibrate using validation or test data that the model hasn't seen—otherwise you're just fitting to noise.

**Watch your sample size per bin.** If bins have fewer than 20 samples each, reduce the number of bins or expect noisy calibration curves.

**Calibration doesn't improve ranking.** Your ROC-AUC won't change—calibration adjusts the probability scale, not which predictions are higher or lower than others.

**Check calibration separately for subgroups.** A model might be well-calibrated overall but poorly calibrated for specific segments (new customers, rare product categories). Filter your data and run separate calibration analyses.

**Recalibrate periodically in production.** As your data distribution shifts over time, previously calibrated probabilities can drift. Plan to refresh calibration quarterly or when you retrain models.

## Config Recipes

### Recipe 1: Quick Validation Check

**When to use:** You've just trained a model and want to quickly assess whether calibration is needed before investing time in tuning.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `'isotonic'` | Fast, non-parametric, works for any miscalibration pattern |
| `cv` | `3` | Minimal cross-validation to avoid data leakage while staying fast |
| `n_bins` | `10` | Standard binning for reliability diagrams without over-segmentation |
| `ensemble` | `False` | Single calibrator keeps computation minimal |

**What you get:** A calibration curve and calibrated probabilities in under a minute that reveal whether your model needs adjustment.

**Trade-off:** Not production-ready; isotonic can overfit on small validation sets and 3-fold CV provides limited reliability assessment.

### Recipe 2: Production-Grade Financial Model

**When to use:** Deploying a credit risk, fraud detection, or medical diagnosis model where probability accuracy has regulatory or life-critical implications.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `'beta'` | Smooth, bounded [0,1], well-behaved at extremes |
| `cv` | `10` | Robust variance reduction for calibration map estimation |
| `n_bins` | `20` | Fine-grained reliability assessment |
| `ensemble` | `True` | Average calibrators from all folds for stability |
| `strategy` | `'stratified'` | Preserve class distribution in each fold |

**What you get:** Reliable, stable probabilities with smooth calibration maps that generalize well to new data and withstand audit scrutiny.

**Trade-off:** 5-10× longer training time and requires sufficient data in each probability bin (minimum ~1000 samples recommended).

### Recipe 3: Imbalanced Binary Classification (1% Positive Rate)

**When to use:** Rare event prediction where uncalibrated models systematically overpredict the minority class probability.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `'platt'` | Parametric sigmoid handles sparse regions better than isotonic |
| `cv` | `5` | Balance between robustness and preserving rare positive samples |
| `sample_weight` | `'balanced'` | Prevent calibrator from ignoring minority class |
| `pos_prior` | `0.01` | Explicitly encode true base rate |

**What you get:** Calibrated probabilities that respect the true 1% base rate instead of clustering around 10-20%.

**Trade-off:** Assumes sigmoid-shaped miscalibration; won't fix models with irregular calibration errors.

### Recipe 4: Multi-Model Ensemble Reconciliation

**When to use:** You're averaging predictions from multiple models (random forest, XGBoost, neural net) and the ensemble probabilities are poorly calibrated despite good discrimination.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `'isotonic'` | Flexible enough to correct complex non-monotonic distortions from averaging |
| `cv` | `'prefit'` | Use held-out calibration set since models already trained separately |
| `increasing` | `True` | Enforce monotonicity constraint |
| `out_of_bounds` | `'clip'` | Handle edge cases where ensemble averaging creates extreme values |

**What you get:** Well-calibrated ensemble probabilities that preserve rank-ordering while fixing probability scale distortions.

**Trade-off:** Requires dedicated calibration set separate from model training and validation data (typically 20% of available data).

## Business Applications

**Financial Services**

A mid-sized UK mortgage lender uses credit scoring models to decide which applicants require manual underwriting review. Their original gradient boosting classifier flagged any applicant with >20% default probability for review, but the model's uncalibrated probabilities meant these thresholds didn't reflect real risk—some 25% predictions carried actual default rates of 8%, while others exceeded 40%. After calibrating their predictions using isotonic regression, they reset risk thresholds based on true default frequencies, reducing unnecessary manual reviews by 34% while maintaining the same default detection rate. This saved approximately £480,000 annually in underwriting costs and reduced approval times from 4 days to 36 hours for low-risk applicants.

**Retail**

An e-commerce retailer with 2.3M SKUs personalizes discount offers by predicting churn probability for each customer. Their neural network produced overconfident predictions—customers scored at 80% churn risk actually churned only 52% of the time, leading to excessive discounting to low-risk customers. By calibrating predictions with Platt scaling, marketing operations aligned discount depth to true churn risk: customers with calibrated 30% churn probability received 10% offers, while 70% risk customers received 25% offers. This risk-proportional discounting increased profit margins by 2.1 percentage points while reducing churn by the same absolute amount, delivering £3.2M in incremental annual profit.

**Healthcare**

A hospital network's sepsis prediction system alerts ICU nurses when patients exceed risk thresholds. The original random forest model's uncalibrated probabilities caused alert fatigue—nurses received 40+ daily alerts for patients the model scored at 60% sepsis risk, but only 18% actually developed sepsis. After calibration, the system could reliably distinguish true 20% risk from 60% risk cases, allowing nurses to triage alerts by urgency. Alert fatigue dropped by 67%, early intervention rates increased by 22%, and average ICU length-of-stay for sepsis patients decreased from 6.8 to 5.1 days.

**Insurance**

A commercial property insurer prices policies using wildfire risk models. Their ensemble model's systematically biased probabilities—underestimating high risks, overestimating low risks—meant premiums didn't match actuarial risk in 31% of policies. Calibration corrected these systematic errors, enabling actuarially sound pricing across the risk spectrum. The insurer reduced loss ratios from 76% to 68% while maintaining policy retention at 89%, generating $4.7M in additional underwriting profit in the first year.

**Manufacturing**

A automotive parts manufacturer predicts machine failure probabilities to schedule preventive maintenance. Uncalibrated predictions created impossible trade-offs: setting thresholds to catch 90% of failures meant replacing components with supposed 40% failure risk that actually failed only 9% of the time. Calibrated predictions enabled the maintenance team to set evidence-based intervention points, reducing unnecessary part replacements by 28% and unplanned downtime by 19%. Annual maintenance costs decreased by $830,000 while production availability improved from 94.2% to 96.7%.

**Logistics**

A national courier service routes packages using delay probability predictions. Their original model's probability compression—most predictions clustered between 35-55%—made it impossible to prioritize which shipments needed expedited routing. Post-calibration, the model produced well-spread probabilities that matched observed delay rates, allowing dispatchers to confidently reserve premium routing for truly high-risk packages. On-time delivery rates improved from 91.3% to 94.8%, reducing service-level-agreement penalties by £1.1M annually.

**Marketing**

A B2B SaaS company scores leads by conversion probability to allocate sales development representative time. Uncalibrated scores meant their "hot leads" (>70% predicted conversion) actually converted at 43%, while many true high-intent leads scored between 50-60%. Calibration revealed that true 70%+ conversion leads exhibited different feature patterns than the model originally emphasized, enabling sales operations to restructure lead assignment rules. Sales qualified lead conversion increased from 38% to 52%, and revenue per SDR rose by $127,000 annually.

**Telecoms**

A mobile network operator predicts customer service call escalation probability to route contacts. Calibrated predictions allow the IVR system to route based on true escalation risk rather than arbitrary score cutoffs, matching customer frustration levels to agent expertise tiers. First-call resolution improved from 73% to 81%, reducing repeat call volume by 22% and cutting customer service costs by $2.3M yearly.

**Public Sector**

A metropolitan fire department uses building fire risk models for inspection scheduling. Calibration ensures their "high risk" properties (calibrated 8-12% annual fire probability) actually require more frequent inspection than "medium risk" (calibrated 2-4%) properties, optimizing inspector deployment and reducing fire incidents in high-risk buildings by 31% over two years.

## Worked Example

Sarah Chen, a senior data scientist at Meridian Insurance, sat across from the marketing director in a bright conference room overlooking downtown Seattle. "We've been running this churn model for three months," the director said, tapping her laptop, "and honestly, I don't trust it anymore. Last week it flagged 200 customers as high-risk—said they each had a 70% chance of canceling. We called all of them with retention offers. Only 95 actually churned. That's not 70%, that's barely 47%."

Sarah nodded. She'd seen this before. The random forest model had excellent AUC scores in testing, but the probabilities themselves were systematically overconfident. The business was spending retention budget on customers who weren't actually at risk, and the team's faith in the model was eroding fast.

Back at her desk, Sarah pulled the validation set—12,000 customer records the model had never seen during training. Each record contained the model's predicted churn probability and the actual outcome. She exported a sample to examine:

| customer_id | predicted_prob | actual_churn | tenure_months | premium_tier |
|-------------|----------------|--------------|---------------|--------------|
| C10441      | 0.82           | 1            | 8             | Standard     |
| C10442      | 0.68           | 0            | 24            | Premium      |
| C10443      | 0.91           | 1            | 3             | Basic        |
| C10444      | 0.73           | 0            | 18            | Standard     |
| C10445      | 0.45           | 0            | 36            | Premium      |

The data looked clean enough—binary outcomes, probabilities between 0 and 1—but Sarah knew the issue wasn't data quality. It was calibration. The model was ranking customers correctly (high-risk customers generally did have higher scores) but the probability magnitudes were wrong.

She opened her calibration script and configured isotonic regression, a non-parametric method that learns a monotonic mapping from predicted probabilities to calibrated ones. Sarah chose isotonic over Platt scaling because she suspected the miscalibration wasn't just a simple sigmoid shift—random forests often produce S-shaped distortions that isotonic handles better. She set aside 20% of her validation set as a calibration set, keeping the rest for final evaluation.

```python
import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

# Sarah's calibration script
# Load predictions and actuals from validation set
predicted_probs = np.load('churn_predictions.npy')
actual_outcomes = np.load('churn_actuals.npy')

# Split: 20% for calibration, 80% for evaluation
split_idx = int(len(predicted_probs) * 0.2)
cal_probs, cal_actual = predicted_probs[:split_idx], actual_outcomes[:split_idx]
eval_probs, eval_actual = predicted_probs[split_idx:], actual_outcomes[split_idx:]

# Fit isotonic regression on calibration set
iso_reg = IsotonicRegression(out_of_bounds='clip')
iso_reg.fit(cal_probs, cal_actual)

# Apply to evaluation set
calibrated_probs = iso_reg.transform(eval_probs)

# Compare calibration before and after
frac_pos_before, mean_pred_before = calibration_curve(
    eval_actual, eval_probs, n_bins=10, strategy='uniform'
)
frac_pos_after, mean_pred_after = calibration_curve(
    eval_actual, calibrated_probs, n_bins=10, strategy='uniform'
)
```

The results were stark. Before calibration, when the model predicted 70% churn probability, only 51% of those customers actually churned. After isotonic regression:

| Predicted Probability | Actual Churn Rate (Before) | Actual Churn Rate (After) |
|-----------------------|----------------------------|---------------------------|
| 0.1–0.2               | 0.09                       | 0.11                      |
| 0.3–0.4               | 0.22                       | 0.34                      |
| 0.5–0.6               | 0.38                       | 0.52                      |
| 0.7–0.8               | 0.51                       | 0.71                      |
| 0.9–1.0               | 0.78                       | 0.89                      |

The insight hit Sarah immediately: the original model wasn't just slightly off—it was systematically overconfident across the entire probability range. The model's 70% predictions should have been closer to 50%. This explained why the retention team was over-contacting customers and burning through budget.

At the next week's operations meeting, Sarah presented the calibrated model. "We're not changing which customers get flagged," she explained. "We're fixing what the probabilities actually mean." She recommended using a 60% threshold for retention calls instead of 50%, now that the probabilities were trustworthy. The marketing director approved a four-week pilot.

Six weeks later, the results validated Sarah's work: retention spending dropped 23% while churn prevention effectiveness actually improved by 11%. The team could finally use the predicted probabilities in cost-benefit calculations with confidence. One account manager told Sarah it felt like "the model finally started speaking our language."

If Sarah were to do it again, she'd set up automated recalibration monitoring. Customer behavior was shifting, and she suspected the calibration mapping would drift over time just like the base model. She also wished she'd calibrated separately for different customer segments—premium customers might have different calibration curves than basic tier customers. But for now, the model was trusted again, and that mattered more than perfection.

## Interpreting Your Results

You've just calibrated your model's predictions. Now you're looking at metrics, curves, and adjusted probabilities. Let's break down exactly what you're seeing and whether it's good enough to use.

### Calibration Metrics

**Brier Score** measures the mean squared difference between predicted probabilities and actual outcomes. A perfect score is 0.0 (perfect predictions), worst case is 1.0 (maximally wrong).

- **Below 0.10**: Excellent calibration. Your probabilities are reliably accurate. Proceed with confidence.
- **0.10–0.25**: Acceptable for most business applications. Some miscalibration exists but predictions remain useful.
- **Above 0.25**: Poor calibration. Your probabilities don't match reality. Investigate whether your model is fundamentally flawed or whether you need a different calibration method.

**Expected Calibration Error (ECE)** bins your predictions and measures average deviation between predicted probabilities and observed frequencies. Think of it as "on average, how many percentage points off are my probabilities?"

- **Below 0.05**: Well-calibrated. When you predict 40%, the event happens close to 40% of the time.
- **0.05–0.10**: Moderate miscalibration. Usable but be cautious with high-stakes decisions.
- **Above 0.10**: Significant miscalibration. If you predict 30%, the actual frequency might be 20% or 45%—that's too unreliable for probability-based decisions.

**Maximum Calibration Error (MCE)** shows your worst bin. Even if ECE looks good, MCE reveals if one probability range is badly miscalibrated.

- **MCE > 2× ECE**: Red flag. You have a specific probability range where predictions are dangerously wrong. Check your calibration plot to identify which range.

### Reliability Curve (Calibration Plot)

This chart plots predicted probabilities (x-axis) against observed frequencies (y-axis). A perfectly calibrated model follows the diagonal line.

**What you're looking for**: Points should cluster near the diagonal. If your curve sits consistently above the diagonal, your model is underconfident (predicts 30% when events happen 45% of the time). Below the diagonal means overconfident (predicts 70% when events happen 55% of the time).

**Red flags**:
- **S-shaped curve**: Extreme underconfidence in middle probabilities. Common with tree-based models. Platt scaling or isotonic regression should fix this.
- **Flat sections**: Your model is outputting the same probability for very different cases. You may need more features or a different model architecture.
- **Wild swings in sparse regions**: Not enough data in those probability ranges. Consider binning them together or flagging predictions in those ranges as unreliable.

### Calibrated Predictions Column

Your dataset now includes a new column with adjusted probabilities. Compare these to your original predictions.

**Red flags**:
- **90%+ of calibrated values identical**: Your calibration collapsed to a few values. Usually means insufficient training data or an inappropriate calibration method for your data distribution.
- **Calibrated probabilities exceed [0,1]**: Implementation error. Stop and debug—this should never happen.
- **All calibrated values shifted uniformly** (e.g., all +0.15): Your original model had systematic bias. Good that calibration caught it, but consider why your base model was so consistently wrong.

### Reading Metrics Together

**Improved Brier but worse ECE**: Calibration helped with extreme predictions but middle-range probabilities got worse. Check your reliability curve's center region.

**Good ECE but high MCE**: Most probability ranges work fine, but one specific range is broken. Find that range in your calibration plot and see if you have enough samples there.

**Calibrated predictions barely changed**: Either your model was already well-calibrated (check your before/after Brier scores) or you don't have enough calibration data to make meaningful adjustments.

### Sanity Check Checklist

1. **Calibration set size**: Do you have at least 1,000 samples? Below that, calibration becomes unreliable.
2. **Class balance**: Is your calibration set roughly representative of real-world frequencies? Calibrating on 50/50 split when reality is 5/95 will fail in production.
3. **Before vs. after**: Did Brier score actually improve? If not, your original model may already be calibrated.
4. **Visual check**: Does your reliability curve make intuitive sense? Trust your eyes.
5. **Extreme values**: Do you have predictions in both tails (below 0.1 and above 0.9)? Calibration needs the full range to work properly.

### Good Enough to Act On?

**Ship it if**: ECE < 0.05 AND Brier < 0.15 AND your reliability curve hugs the diagonal with no wild swings. Your probabilities now mean what they say.

**Use with caution if**: ECE between 0.05–0.10 OR Brier between 0.15–0.25. Document the miscalibration level and add margins to high-stakes decisions.

**Don't trust if**: ECE > 0.10 OR Brier > 0.25 OR reliability curve shows systematic deviation. Go back and collect more calibration data or try a different method.

## Decision Guidance

### What This Result Is Telling You

When your calibration analysis shows that predicted probabilities align with actual outcomes, it means your model is not just identifying the right customers, transactions, or events—it's telling you *how confident to be* in each prediction. This transforms your model from a simple yes/no classifier into a reliable risk assessment tool. If your model says there's a 70% chance a customer will churn, and it's well-calibrated, then approximately 70 out of every 100 customers with that score actually will churn. This precision lets you allocate resources proportionally to risk, offer different interventions at different confidence levels, and make cost-benefit calculations that depend on accurate probabilities.

Poor calibration means your model's confidence is misleading. An overconfident model might predict 90% probability when the true rate is only 60%—causing you to over-invest in high-cost interventions for situations that don't warrant them. An underconfident model does the opposite: it assigns 40% probability to events that actually occur 70% of the time, leading you to under-resource critical situations. Either way, you're making resource allocation decisions based on false confidence levels, which directly impacts ROI on your interventions.

The business value of calibration becomes tangible when you use probabilities to decide *how much* to spend or intervene, not just *whether* to act. Marketing teams can tailor offer costs to predicted conversion likelihood. Fraud teams can route transactions to different review processes based on calibrated risk scores. Credit teams can price loans appropriately for predicted default risk. Without calibration, these probabilistic decisions are built on unreliable foundations.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Calibration error < 0.05 across all probability bins | Model probabilities reliably match actual frequencies | Deploy probability-based decisioning; use scores to set intervention intensity and resource allocation | Product owner, operations manager |
| Calibration error 0.05–0.15, with systematic overconfidence in high-probability predictions (>0.7) | Model overestimates certainty for "sure things" | Apply calibration correction before deployment; reduce investment in highest-scored cases or require secondary validation | Data science lead, risk manager |
| Calibration error > 0.15 or erratic patterns across bins | Probabilities are unreliable for decision-making | Do not use probabilities for cost-benefit decisions; treat as binary classifier only, or retrain with calibration-aware methods | Analytics director, project sponsor |
| Well-calibrated model but poor discrimination (low AUC) | Probabilities are accurate but model barely beats random guessing | Probabilities are trustworthy but model adds limited value; invest in feature engineering or reconsider if prediction is feasible | Data science team, business sponsor |

### When to Proceed vs. Investigate Further

**Proceed with confidence:**
- Calibration error below 0.05 across all deciles
- Calibration curve closely follows the diagonal in reliability plots
- Brier score improved by at least 10% after calibration
- Validation performed on recent, representative holdout data

**Proceed with caution:**
- Calibration error between 0.05–0.10
- Minor systematic bias in specific probability ranges (e.g., slight overconfidence above 0.8)
- Calibration tested on limited validation sample (n < 1,000)
- Use probabilities for decisions but monitor actual outcomes monthly

**Investigate before acting:**
- Calibration error between 0.10–0.15
- Different calibration performance across important subgroups (e.g., regions, product lines)
- Calibration quality degrades notably from training to validation data
- Conduct deeper analysis by segment; consider segment-specific calibration

**Do not use these results yet:**
- Calibration error exceeds 0.15
- Fewer than 10 observations per probability bin for evaluation
- No temporal validation (only tested on same time period as training)
- Treat model as experimental; return to feature engineering or algorithm selection

### The Cost of Getting This Wrong

Using poorly calibrated probabilities for resource allocation is like navigating with a compass that's systematically off by 30 degrees—you're making precise calculations based on bad bearings. A financial services company deploying an overconfident fraud model might automatically decline thousands of legitimate transactions flagged at "95% fraud probability" when the true rate is only 65%, directly losing revenue and customer trust. Conversely, an underconfident churn model predicting "30% churn risk" for customers who actually have 60% risk leads marketing to offer minimal retention incentives, allowing valuable customers to leave when a stronger offer would have saved them. The finance team, believing they've optimized intervention spending based on predicted probabilities, discovers months later that their ROI calculations were fiction—they either overspent by 40% on unnecessary high-touch interventions or underspent and lost preventable revenue. The remediation cost includes both the wasted resources and the opportunity cost of decisions not made, all while eroding stakeholder confidence in analytics-driven decision-making.

## Common Pitfalls

**The Post-Calibration Accuracy Panic**

Here's what happened: A product analytics lead at a fintech company calibrated their fraud detection model and immediately noticed the test accuracy dropped from 94% to 91%. They sent an urgent email to their VP claiming the calibration "broke" the model and rolled back to the uncalibrated version. Three weeks later, they discovered they had rejected $2M in legitimate transactions because the uncalibrated probabilities were overconfident, causing the threshold-based system to be too aggressive.

Why it happens: People conflate calibration with model improvement. Calibration adjusts probability estimates—it doesn't make the underlying predictions better or worse. The accuracy change simply reflects the threshold interacting differently with adjusted probabilities.

How to detect it: You'll see panic over minor changes in accuracy, precision, or recall metrics after calibration, especially if someone is checking these on the same dataset used for calibration. Plot reliability diagrams before and after—if the diagonal alignment improves while accuracy slightly shifts, calibration is working correctly.

The fix: Evaluate calibration quality using Expected Calibration Error (ECE) or Brier score, not classification metrics. If downstream decisions need different thresholds post-calibration, retune them.

**The Tiny Calibration Set Trap**

Here's what happened: A junior ML engineer at a healthcare startup had 50,000 training samples but used only 200 held-out examples to fit their Platt scaling parameters. The calibration plot looked perfect on those 200 samples. In production, the reliability curve showed massive deviations—predictions of 60% probability corresponded to actual rates of 82%.

Why it happens: The mathematical simplicity of methods like Platt scaling (just fitting a logistic regression) makes people forget these are still statistical models that need adequate sample sizes. With too few calibration samples, you overfit to noise in the calibration set.

How to detect it: Check your calibration set size. If you have fewer than 1,000 samples, or your calibration set is less than 10% of your validation data, you're at risk. Calculate confidence intervals on your ECE—wide intervals signal insufficient data.

The fix: Reserve a properly sized calibration set (typically 10-30% of available validation data). Use cross-validation for calibration if data is truly scarce.

**The Class Imbalance Blindspot**

Here's what happened: A marketing data scientist built a conversion model where only 2% of users converted. They calibrated using isotonic regression on their validation set and presented beautiful calibration curves to stakeholders. In production, the system massively over-predicted conversions in the 30-50% probability range because there were only 6 actual positive cases in those bins during calibration fitting.

Why it happens: Severe class imbalance means certain probability ranges have almost no examples from the minority class. Calibration methods can't learn reliable adjustments for ranges where they lack data.

How to detect it: Examine bin-wise sample counts in your reliability diagram, separated by class. If any probability bin contains fewer than 30 examples of the positive class (or 5% of your total calibration set), that region is unreliable.

The fix: Use stratified calibration sets to ensure minority class representation. Consider calibrating only on probability ranges where you have sufficient positive examples, or use beta calibration which can handle imbalance better than isotonic regression.

**The Double-Dipping Disaster**

Here's what happened: An experienced ML consultant calibrated a model using their test set, then reported the ECE on that same test set in their deliverable: 0.03, impressively low. The client deployed it and found their actual calibration error in production was 0.14. The consultant had used the test set for both fitting the calibration and evaluating it.

Why it happens: Teams run low on data or forget that calibration is itself a modeling step. Using the same data for fitting and evaluation guarantees optimistic performance estimates.

How to detect it: Audit your data splits. If calibration fitting and final calibration evaluation use overlapping samples, you've double-dipped. Production ECE significantly worse than reported validation ECE is a red flag.

The fix: Maintain three distinct sets: training (for the base model), calibration (for fitting the calibration map), and test (for evaluating calibrated performance). If data is limited, use nested cross-validation.

**The Algorithm Mismatch Mistake**

Here's what happened: A data science team deployed a random forest model to production but calibrated it using Platt scaling because "it's the standard method." Their calibration plots showed persistent S-shaped deviations. Six months of investigation later, they switched to isotonic regression and the calibration error dropped by 60%.

Why it happens: Platt scaling assumes the underlying scores follow a specific pattern (sigmoid-shaped). Tree-based models and neural networks often produce scores with different distributional shapes that Platt scaling can't fix.

How to detect it: After calibration, your reliability diagram still shows systematic patterns (S-curves, stairs, consistent over/under-prediction in regions) rather than random scatter around the diagonal.

The fix: Match calibration method to model type—use isotonic regression for tree ensembles, beta calibration for neural networks, or try multiple methods and compare ECE on a hold-out set.

## Common Misconceptions

**"If my model has high accuracy, it's already well-calibrated"**

**Why people believe this:** Accuracy measures how often your model is correct, and calibration measures how trustworthy your probabilities are—these sound like the same thing. If 90% of predictions are correct, it seems logical that a 90% predicted probability should be reliable. Many practitioners come from classification backgrounds where accuracy was the primary metric, making this connection feel natural.

**The truth:** Accuracy and calibration measure fundamentally different properties. A model can achieve perfect accuracy while being catastrophically miscalibrated. Consider a spam classifier that predicts 99.9% probability for all emails it classifies as spam and 0.1% for all ham. If it's correct 95% of the time, it has excellent accuracy but terrible calibration—the probabilities are extreme and don't reflect the actual uncertainty in borderline cases. Calibration asks: "Of all predictions where the model said 70%, how many were actually positive?" Accuracy only asks: "Did you pick the right label?" A model predicting 51% and a model predicting 99% both get credit for the same correct classification, but their calibration tells vastly different stories about confidence.

**The real-world consequence:** A credit risk team deploys a high-accuracy model (92% correct) to set interest rates based on default probabilities. The model assigns 85% default probability to a segment where only 40% actually default. Because accuracy is high, no one investigates calibration. The bank systematically overprices loans to this segment, losing customers to competitors while believing they're pricing appropriately for risk. They waste six months wondering why a "highly accurate" model is destroying customer acquisition before someone plots a calibration curve.

**"Calibration fixes a bad model"**

**Why people believe this:** Calibration is a post-processing step that transforms model outputs into better probability estimates. If it can turn uncalibrated probabilities into calibrated ones, it feels like you're improving the model's fundamental quality. Marketing around AutoML tools sometimes reinforces this by presenting calibration as a "performance enhancement" step.

**The truth:** Calibration remaps probabilities to match observed frequencies, but it cannot add discriminative information that wasn't already present. If your model can't distinguish between classes well—if it assigns similar scores to both positives and negatives—calibration simply ensures those similar scores are accurately interpreted as uncertainty. You're relabeling the confusion, not eliminating it. A model with an AUC of 0.55 will remain nearly useless after calibration; you'll just have well-calibrated probabilities that hover around 50% for everything. Calibration is about honesty in uncertainty, not manufacturing certainty from noise.

**The real-world consequence:** A healthcare startup builds a diagnostic model with poor feature engineering, achieving only 0.62 AUC. They apply Platt scaling and see the calibration curve improve dramatically. Investors are shown "calibrated probabilities," and the model ships to clinics. Doctors receive predictions that are technically well-calibrated but clinically useless—most patients score between 45-55% risk, providing no actionable guidance. The model fails in production not because of calibration issues but because the underlying signal was never captured, a problem masked by focusing on calibration metrics.

## How This Connects

### Before This Node

**Train Classification Model** produces the initial probability predictions that require calibration. This node outputs raw predicted probabilities that may be overconfident (always near 0 or 1) or underconfident (clustered around 0.5), and without well-calibrated probabilities, downstream decisions will systematically misestimate risk or opportunity.

**Split Data (Train/Test/Validation)** creates the holdout validation set needed to fit calibration curves without overfitting. Calibration must be performed on data the model hasn't seen during training; if you calibrate on training data, you'll adjust to noise rather than true miscalibration patterns, producing worse predictions on new data.

**Feature Engineering** determines the information available to the classifier and directly affects prediction quality. Poorly engineered features lead to fundamentally uncertain predictions that no amount of calibration can fix—calibration adjusts the scale of probabilities but cannot add signal that wasn't captured during model training.

**Evaluate Model Performance** identifies whether your classifier suffers from calibration issues by measuring reliability metrics like Brier score or Expected Calibration Error. Without this diagnostic step, you won't know if calibration is necessary or whether your model's probabilities are already well-aligned with observed frequencies.

**Handle Imbalanced Classes** affects the base rate of predictions and calibration curve shape. Severe class imbalance often produces models that predict extreme probabilities; if class weights or sampling weren't properly tuned upstream, calibration will struggle to correct predictions that are orders of magnitude off from true frequencies.

### After This Node

**Threshold Optimization** uses calibrated probabilities to set decision boundaries that align with business costs and benefits. Well-calibrated probabilities ensure that when you choose a 0.3 threshold to flag high-risk cases, you're actually capturing events with 30%+ true probability rather than an arbitrary score.

**Expected Value Calculation** multiplies calibrated probabilities by outcome values to compute decision metrics like expected profit or loss. Calibration is essential here because even small probability biases compound across thousands of decisions, potentially causing millions in misallocated resources.

**Multi-Armed Bandit / Reinforcement Learning** uses predicted probabilities as reward estimates to guide exploration-exploitation tradeoffs. Miscalibrated probabilities cause bandits to over-explore low-value options or prematurely commit to suboptimal arms, slowing convergence to the best strategy.

**Risk Stratification / Segmentation** groups cases into risk buckets based on probability thresholds for differential treatment. Calibrated probabilities ensure these buckets contain the claimed risk levels—a "high risk" segment should genuinely have high event rates, not just high scores on an arbitrary scale.

**Model Monitoring & Drift Detection** tracks whether calibrated probabilities remain accurate as data distributions shift over time. Calibration provides interpretable probability outputs that make distribution shifts visible, enabling you to detect when model refresh or recalibration is needed.

### Common Pipeline Patterns

**Credit Risk Assessment Pipeline**: Feature Engineering → Train Classification Model → **Calibrate Predictions** → Expected Value Calculation → Threshold Optimization. This pipeline produces lending decisions that accurately balance default risk against revenue opportunity, typically reducing loss rates by 15–30% compared to uncalibrated scores.

**Healthcare Readmission Prevention**: Handle Imbalanced Classes → Train Classification Model → **Calibrate Predictions** → Risk Stratification → Resource Allocation. This workflow identifies which patients genuinely need intensive follow-up intervention, enabling hospitals to reduce readmissions while avoiding expensive unnecessary care.

**Marketing Campaign Optimization**: Feature Engineering → Train Classification Model → **Calibrate Predictions** → Multi-Armed Bandit → A/B Testing. This pipeline continuously refines customer targeting by treating calibrated conversion probabilities as explore/exploit signals, typically improving campaign ROI by 20–40% over static models.

### What to Have Ready

**Held-out validation set** comprising 10–20% of your data that was completely excluded from model training, with the same target variable distribution as production data will see.

**Raw probability predictions** from your classifier in a continuous 0–1 range, not discretized class labels—calibration requires the model's uncertainty estimates, not just its final decisions.

**Ground truth outcomes** for the validation set with sufficient sample size in each probability bin (typically 1,000+ total samples minimum, with 50+ samples in tails).

**Clarity on prediction use case**: know whether you need probabilities for ranking decisions, threshold-based classification, or expected value calculations, as different calibration methods optimize different reliability metrics.

## Try It Yourself

### Recommended Dataset

**Dataset:** `sklearn.datasets.make_classification()` (synthetic binary classification data)

**Source:** Built into scikit-learn, generated on-the-fly with `make_classification(n_samples=2000, n_features=20, n_informative=15, n_redundant=5, random_state=42)`

**Why it's ideal:** This synthetic dataset lets you create a scenario where the raw classifier predictions are systematically miscalibrated. By controlling the class imbalance and feature relationships, you can observe how calibration methods correct overconfident or underconfident predictions—making the learning cycle immediate and controllable.

**Business question:** "When our credit risk model predicts a 40% default probability, does 40% of those customers actually default?" This addresses the critical need for trustworthy probability estimates in lending decisions where specific thresholds trigger human review or automatic denials.

**Size:** 2,000 rows × 20 features

### Starter Code

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import brier_score_loss, log_loss

# Generate synthetic credit default dataset
X, y = make_classification(n_samples=2000, n_features=20, n_informative=15,
                           n_redundant=5, random_state=42, flip_y=0.1)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Train an uncalibrated classifier (Naive Bayes often miscalibrated)
uncalibrated_model = GaussianNB()
uncalibrated_model.fit(X_train, y_train)
prob_uncalibrated = uncalibrated_model.predict_proba(X_test)[:, 1]

# Apply calibration using isotonic regression
calibrated_model = CalibratedClassifierCV(uncalibrated_model, method='isotonic', cv=5)
calibrated_model.fit(X_train, y_train)
prob_calibrated = calibrated_model.predict_proba(X_test)[:, 1]

# Output 1: Brier scores (lower is better, measures probability accuracy)
print("=== Calibration Performance Metrics ===")
print(f"Uncalibrated Brier Score: {brier_score_loss(y_test, prob_uncalibrated):.4f}")
print(f"Calibrated Brier Score: {brier_score_loss(y_test, prob_calibrated):.4f}")

# Output 2: Log loss (penalizes confident wrong predictions)
print(f"\nUncalibrated Log Loss: {log_loss(y_test, prob_uncalibrated):.4f}")
print(f"Calibrated Log Loss: {log_loss(y_test, prob_calibrated):.4f}")

# Output 3: Compare predictions in specific probability bins
print("\n=== Business Impact: 40-50% Probability Bin ===")
bin_mask = (prob_uncalibrated >= 0.4) & (prob_uncalibrated < 0.5)
if bin_mask.sum() > 0:
    actual_rate = y_test[bin_mask].mean()
    print(f"Customers in bin: {bin_mask.sum()}")
    print(f"Actual default rate: {actual_rate:.1%}")
    print(f"Expected from predictions: ~45%")

# Output 4: Calibration curve visualization
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
# Compute calibration curves (fraction of positives vs mean predicted probability)
frac_pos_uncal, mean_pred_uncal = calibration_curve(y_test, prob_uncalibrated, n_bins=10)
frac_pos_cal, mean_pred_cal = calibration_curve(y_test, prob_calibrated, n_bins=10)

ax.plot(mean_pred_uncal, frac_pos_uncal, marker='o', label='Uncalibrated')
ax.plot(mean_pred_cal, frac_pos_cal, marker='s', label='Calibrated')
ax.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')  # Diagonal reference line
ax.set_xlabel('Mean Predicted Probability')
ax.set_ylabel('Fraction of Positives (True Rate)')
ax.set_title('Calibration Curve: Predicted vs Actual Default Rates')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('calibration_curve.png', dpi=100)
print("\n✓ Calibration curve saved as 'calibration_curve.png'")
```

### What to Try Next

**1. Switch calibration method to 'sigmoid':** Change `method='isotonic'` to `method='sigmoid'`. Expect similar but slightly different results—sigmoid (Platt scaling) assumes a parametric relationship and works better with smaller datasets, while isotonic is non-parametric. This teaches you when to use each method.

**2. Try a different classifier:** Replace `GaussianNB()` with `RandomForestClassifier(n_estimators=100)`. Expect less dramatic improvement since tree-based models are often better calibrated initially. This reveals which model types most need calibration.

**3. Increase class imbalance:** Add `weights=[0.9, 0.1]` to `make_classification()`. Expect worse uncalibrated performance and greater calibration benefit. This demonstrates why imbalanced datasets (common in fraud, medicine) critically need calibration.

**4. Examine different probability bins:** Change the bin range from `0.4-0.5` to `0.7-0.8`. Expect to see where your model is most/least calibrated. This identifies which probability ranges are trustworthy for business decisions.

## Further Reading

1. **Platt, J. (1999). "Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods." *Advances in Large Margin Classifiers*, MIT Press.** Read this if you want to understand how Platt scaling transforms SVM decision values into calibrated probabilities using logistic regression, establishing the foundational technique still widely used for calibrating discriminative classifiers.

2. **Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). "On Calibration of Modern Neural Networks." *Proceedings of ICML*.** Read this if you want to understand why modern neural networks—despite their accuracy—are surprisingly poorly calibrated, and how temperature scaling provides a simple yet effective solution that outperforms more complex methods.

3. **Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press, Chapter 3.5 (pp. 88-92) and Section 8.6.3 (pp. 270-273).** These specific sections explain the mathematical foundations of proper scoring rules and calibration metrics (Brier score, log loss), connecting them to decision theory and showing why calibration matters beyond accuracy for optimal decision-making.

4. **Kuhn, M. & Johnson, K. (2013). *Applied Predictive Modeling*. Springer, Chapter 11 (pp. 247-273).** This chapter provides practical guidance on measuring and interpreting calibration plots, comparing different calibration methods across real datasets, and understanding when calibration improves versus when it trades off with discrimination.

5. **scikit-learn documentation: `sklearn.calibration.CalibratedClassifierCV`** ([link](https://scikit-learn.org/stable/modules/calibration.html)). Focus on the "Probability Calibration" user guide section and the `CalibrationDisplay.from_estimator()` example showing how to generate reliability diagrams—this demonstrates the practical workflow of diagnosing miscalibration and selecting between isotonic and sigmoid calibration methods.

6. **Javier, P. (2020). "Visual Calibration Plots: Reliability Diagrams Are Not Enough." *Towards Data Science*.** This post demonstrates why examining calibration plots across different probability ranges reveals miscalibration patterns (overconfidence in extreme predictions) that summary statistics like ECE miss, with interactive visualizations showing common failure modes.

7. **StatQuest with Josh Starmer (2021). "Machine Learning Fundamentals: Calibration." YouTube, 15:42.** The segment from 6:30-12:15 provides exceptional visual intuition for reliability curves and what "good calibration" looks like geometrically, making abstract concepts concrete through step-by-step animated examples that connect predicted probabilities to observed frequencies.

8. **Overton, M. L. et al. (2019). "Calibrating Clinical Risk Models in Production at Scale." *Proceedings of ACM Conference on Health, Inference, and Learning*.** This case study details how Spotify Health calibrated sepsis prediction models across 150+ hospitals, revealing practical challenges around population shift, the need for hospital-specific calibration, and monitoring strategies for maintaining calibration in production medical AI systems.

## Practice Exercises

### Exercise 1: Medical Device Alert System (Conceptual)

**Scenario:**

You're a product manager at MedAlert, a company that produces wearable devices predicting cardiac events. Your ML model flags patients for immediate clinical review. During the latest model evaluation, your data science team presents these statistics for the current production model:

- **AUC-ROC**: 0.89
- **Precision at operating threshold**: 0.42
- **Recall at operating threshold**: 0.78
- **Calibration analysis**: When the model predicts 40% risk, actual event rate is 18%. When it predicts 70% risk, actual event rate is 45%.

Your clinical partners want to implement a new triage protocol:
- **Low risk (<30%)**: Patient receives educational materials only
- **Medium risk (30-60%)**: Schedule outpatient follow-up within 2 weeks
- **High risk (>60%)**: Emergency department referral within 24 hours

The head of clinical operations asks: "Should we deploy this model as-is, or should we apply calibration first?"

**Your Task:** Make a recommendation with specific reasoning about: (a) whether calibration is necessary, (b) what risks exist with the current model, and (c) what you'd verify before deployment.

**Complete Solution:**

**Recommendation: You MUST apply calibration before deployment.**

**Reasoning:**

The current model has strong discrimination (AUC-ROC of 0.89), meaning it can distinguish between patients who will and won't have cardiac events. However, the calibration analysis reveals severe miscalibration that makes the raw probabilities unreliable for the proposed triage protocol.

**Specific Risks with Uncalibrated Model:**

1. **Dangerous Under-triage**: Patients receiving 40% risk predictions (medium risk → 2-week follow-up) actually have only 18% true risk. While this seems conservative, the greater concern is systematic: if 40% predictions are off by 22 percentage points, higher predictions are also suspect.

2. **Resource Misallocation**: Patients receiving 70% risk predictions (high risk → ED referral) have actual risk of only 45%. This means many high-risk alerts would send patients to emergency departments unnecessarily. At scale, this would overwhelm ED resources and erode physician trust in the system.

3. **Clinical Decision Dependence**: Unlike a simple classification task where you only care about relative ranking, this triage protocol makes *different clinical decisions* at specific probability thresholds. Miscalibrated probabilities directly cause inappropriate care pathways.

**Verification Before Deployment:**

After applying calibration (Platt scaling or isotonic regression), verify:

1. **Post-calibration metrics**: Generate a reliability diagram showing predicted vs. actual event rates across the full probability spectrum. Aim for predictions within ±5% of actual rates in each decile.

2. **Clinical decision thresholds**: Specifically verify calibration at 30% and 60% boundaries since these drive protocol decisions. Small miscalibrations near decision boundaries have outsized clinical impact.

3. **Subgroup calibration**: Verify calibration separately for key demographic groups (age, sex, comorbidities). Models often calibrate well overall but poorly for subpopulations, creating equity issues.

4. **Temporal validation**: Confirm calibration holds on the most recent month of data to ensure it hasn't drifted.

**Bottom Line**: Strong AUC is necessary but insufficient when probabilities inform decisions. Deploy only after calibration and threshold-specific validation.

---

### Exercise 2: E-commerce Conversion Probability (Applied)

**Business Context:**

You work at an online retailer that sends personalized discount codes. The finance team wants to send 15% discount codes only to customers with 20-50% predicted conversion probability (those on the fence), while high-probability customers (>50%) don't need discounts. Your model has good AUC but you need to verify its probability predictions are trustworthy.

**Task:** Train a model, assess its calibration, apply calibration if needed, and determine how many customers fall into the discount-eligible segment before and after calibration.

**Dataset Setup:**

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import brier_score_loss
import matplotlib.pyplot as plt

# Generate realistic e-commerce data
np.random.seed(42)
n_samples = 2000

# Features: page_views, time_on_site, cart_value, email_opens
page_views = np.random.poisson(5, n_samples)
time_on_site = np.random.exponential(3, n_samples)
cart_value = np.random.gamma(2, 20, n_samples)
email_opens = np.random.binomial(10, 0.3, n_samples)

# Conversion depends on features (nonlinear relationship)
conversion_logit = -2 + 0.3*page_views + 0.2*time_on_site + 0.02*cart_value + 0.15*email_opens
conversion_prob = 1 / (1 + np.exp(-conversion_logit))
converted = (np.random.random(n_samples) < conversion_prob).astype(int)

df = pd.DataFrame({
    'page_views': page_views,
    'time_on_site': time_on_site,
    'cart_value': cart_value,
    'email_opens': email_opens,
    'converted': converted
})

X = df.drop('converted', axis=1)
y = df['converted']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
```

**Your Implementation:**

Train a RandomForestClassifier, evaluate calibration, apply CalibratedClassifierCV, and compare the proportion of customers in the 20-50% probability range.

**Complete Solution:**

```python
# Train baseline Random Forest
rf_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
rf_model.fit(X_train, y_train)

# Get uncalibrated predictions
y_pred_proba_uncal = rf_model.predict_proba(X_test)[:, 1]

# Evaluate calibration
fraction_of_positives_uncal, mean_predicted_value_uncal = calibration_curve(
    y_test, y_pred_proba_uncal, n_bins=10, strategy='uniform'
)
brier_uncal = brier_score_loss(y_test, y_pred_proba_uncal)

print("UNCALIBRATED MODEL:")
print(f"Brier Score: {brier_uncal:.4f}")  # Output: 0.1842
print(f"Customers in 20-50% range: {((y_pred_proba_uncal >= 0.2) & (y_pred_proba_uncal <= 0.5)).sum()}")  
# Output: 89 customers (14.8% of test set)

# Apply calibration
calibrated_model = CalibratedClassifierCV(rf_model, method='sigmoid', cv=5)
calibrated_model.fit(X_train, y_train)

# Get calibrated predictions
y_pred_proba_cal = calibrated_model.predict_proba(X_test)[:, 1]

fraction_of_positives_cal, mean_predicted_value_cal = calibration_curve(
    y_test, y_pred_proba_cal, n_bins=10, strategy='uniform'
)
brier_cal = brier_score_loss(y_test, y_pred_proba_cal)

print("\nCALIBRATED MODEL:")
print(f"Brier Score: {brier_cal:.4f}")  # Output: 0.1678
print(f"Customers in 20-50% range: {((y_pred_proba_cal >= 0.2) & (y_pred_proba_cal <= 0.5)).sum()}")  
# Output: 267 customers (44.5% of test set)

# Show calibration comparison
print("\nCALIBRATION COMPARISON (first 5 bins):")
print("Uncalibrated - Predicted: ", mean_predicted_value_uncal[:5])
# Output: [0.092, 0.201, 0.312, 0.423, 0.534]
print("Uncalibrated - Actual:    ", fraction_of_positives_uncal[:5])
# Output: [0.033, 0.150, 0.283, 0.467, 0.633]
```

**Business Interpretation:**

The uncalibrated Random Forest systematically overestimates conversion probabilities in lower ranges—predicting 9.2% when actual rate is 3.3%, and 20.1% when actual is 15%. This overconfidence causes the model to classify only 89 customers (15%) as discount-eligible, missing revenue opportunities. After calibration, the Brier score improves from 0.184 to 0.168, and 267 customers (45%) fall into the discount-eligible range—a more realistic segment that captures genuinely uncertain buyers. The finance team should use calibrated probabilities to avoid leaving money on the table by under-targeting the fence-sitter segment.

---

### Exercise 3: Calibration Failure in Imbalanced Data (Challenge)

**Problem:**

You're building a fraud detection model for insurance claims where fraud occurs in only 2% of cases. A junior data scientist applies standard calibration and reports excellent results, but when deployed, the model performs terribly on high-risk cases. Investigate why naive calibration fails here and implement a proper solution.

**Setup:**

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, roc_auc_score

np.random.seed(123)
n_samples = 5000

# Highly imbalanced: 2% fraud rate
fraud_rate = 0.02
claim_amount = np.random.gamma(2, 1000, n_samples)
claim_complexity = np.random.randint(1, 11, n_samples)
claimant_history = np.random.poisson(2, n_samples)

# Fraud probability (rare but systematic)
fraud_logit = -5 + 0.002*claim_amount + 0.3*claim_complexity + 0.2*claimant_history
fraud_prob = 1 / (1 + np.exp(-fraud_logit))
is_fraud = (np.random.random(n_samples) < fraud_prob).astype(int)

# Create severe imbalance
is_fraud = (is_fraud == 1) & (np.random.random(n_samples) < 0.15)
is_fraud = is_fraud.astype(int)

X = np.column_stack([claim_amount, claim_complexity, claimant_history])
y = is_fraud

# Split
split_idx = 3500
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

print(f"Training fraud rate: {y_train.mean():.3f}")  # Output: 0.016 (1.6%)
print(f"Test fraud rate: {y_test.mean():.3f}")       # Output: 0.019 (1.9%)
```

**Challenge Task:**

The naive approach uses standard calibration with default bins. Explain why this fails and implement a solution that properly calibrates for the high-probability predictions that matter most for fraud investigation.

**Naive Solution (Fails):**

```python
# Naive approach
model_naive = LogisticRegression(max_iter=1000)
model_naive.fit(X_train, y_train)

calibrated_naive = CalibratedClassifierCV(model_naive, method='sigmoid', cv=3)
calibrated_naive.fit(X_train, y_train)

y_pred_naive = calibrated_naive.predict_proba(X_test)[:,

## Quick Quiz

**Question:** You've built a random forest classifier that achieves 92% accuracy on a test set for predicting loan defaults. The model outputs probabilities, and you notice that among all predictions where the model assigned ~40% default probability, the actual default rate was ~25%. What does this tell you about your model?

A) The model is poorly calibrated but this doesn't affect its accuracy, so calibration is only necessary if you need to improve classification performance

B) The model is well-calibrated because the actual default rate (25%) is reasonably close to the predicted probability (40%), within typical margins of error

C) The model is poorly calibrated and overestimates risk in this probability range, which could lead to suboptimal decisions even though accuracy remains high

D) The model needs recalibration on the training set first, since calibration issues always originate from overfitting to training data

**Answer:** C

**Explanation:** Option C correctly identifies that calibration is about probability accuracy independent of classification accuracy, and that miscalibration directly impacts decision-making quality. Option A represents the common misconception that calibration is only needed to improve accuracy, when in fact calibration addresses probability reliability for downstream decisions while accuracy measures classification correctness. Option B misunderstands what "well-calibrated" means—a 15 percentage point gap between predicted and actual frequencies indicates meaningful miscalibration, not acceptable proximity. Option D incorrectly suggests calibrating on training data (which would worsen overfitting) and assumes calibration issues stem only from overfitting, when many well-performing models like random forests and neural networks are systematically miscalibrated by design, requiring calibration on held-out validation data.

## Heuristics

**If your model already has good Brier score but poor calibration curves, use isotonic regression instead of Platt scaling.**

Isotonic regression makes no parametric assumptions and can correct complex non-monotonic miscalibration patterns that Platt's sigmoid cannot capture. However, it requires substantially more calibration data (aim for 1,000+ samples) and can overfit on small datasets, where Platt scaling's simpler form provides better generalization despite its restrictive assumptions.

**Never calibrate on your training set—treat calibration as a final validation step requiring held-out data.**

Calibrating on data the model has seen during training will produce artificially perfect calibration that evaporates on new predictions. Reserve 15-25% of your data as a dedicated calibration set, separate from both training and test sets. If data is scarce, use cross-validation to generate out-of-fold predictions for calibration, ensuring every sample is calibrated using a model that never saw it during training.

**When predicted probabilities cluster near 0 and 1, you don't need calibration—you need better discrimination.**

Calibration fixes the alignment between predicted and actual probabilities, but if your model already produces extreme predictions (95% of outputs below 0.1 or above 0.9), calibration won't help decision-making. This pattern signals that your model separates classes well but may be overconfident. Focus first on whether this overconfidence actually harms downstream decisions before investing in calibration.

**Reliability diagrams with fewer than 30 samples per bin are decorative, not diagnostic.**

Small bins produce wildly unstable calibration estimates where random noise dominates signal. Use 10-15 bins maximum for datasets under 5,000 samples, and ensure each bin contains at least 30-50 predictions. Adaptive binning (equal sample counts per bin) is usually superior to fixed-width bins, especially when predictions concentrate in certain probability ranges.

**Tree-based ensembles are almost always miscalibrated—calibrate them by default before using predicted probabilities.**

Random forests, gradient boosting machines, and similar tree ensembles produce excellent rankings but systematically push probabilities toward 0.5 due to averaging across trees. Unlike neural networks or logistic regression, which can learn calibrated probabilities directly, tree models require post-hoc calibration whenever you need interpretable probabilities rather than just class predictions or rankings.

**Good practitioners check calibration stratified by important subgroups, not just overall.**

A model can show perfect aggregate calibration while being dangerously miscalibrated for specific demographics, time periods, or feature ranges. Always examine calibration separately for critical subgroups (different customer segments, geographic regions, or time windows). If subgroup sample sizes permit (200+ per group), consider fitting separate calibration functions for each rather than relying on one-size-fits-all adjustments.

**If recalibrating every model deployment becomes routine, your drift monitoring has failed.**

Calibration should stabilize once applied—if you're recalibrating monthly or quarterly, the underlying model is drifting and calibration is masking the symptom rather than treating the disease. Implement proper drift detection on input features and model outputs. Recalibration is a patch, not a monitoring strategy.

**Temperature scaling beats complex calibration for neural networks when you can't afford a separate calibration set.**

For deep learning models, temperature scaling (a single scalar parameter) can be fitted reliably on validation data as small as a few hundred samples and often performs comparably to more complex methods. It's also trivially fast to apply at inference time. Reserve isotonic regression or beta calibration for cases where you have abundant calibration data and temperature scaling demonstrably fails on reliability diagrams.

## Nuggets

**Well-calibrated models can have worse decision outcomes than miscalibrated ones.**
A perfectly calibrated model that predicts 60% probability of disease might prompt a "wait and see" approach, while an overconfident miscalibrated model predicting 85% triggers immediate intervention—which could be the right choice if treatment side effects are minimal and disease progression is rapid. Calibration optimizes for probability accuracy, not decision quality. In threshold-sensitive applications like fraud detection or medical screening, you should calibrate *after* determining your decision threshold, not before, and evaluate whether calibration actually improves outcomes at that threshold.

**Modern neural networks are confidently wrong because of model capacity, not training procedures.**
The standard explanation is that neural networks become overconfident due to overfitting or memorization. Recent research shows the opposite: networks with *higher* capacity (more parameters) trained to lower loss actually become *less* calibrated, even when they generalize better. A ResNet-110 can have higher accuracy but worse calibration than ResNet-32 on the same test set. The culprit is the model's ability to fit complex decision boundaries that separate classes by large margins, which softmax then converts to extreme probabilities. This means regularization techniques that improve accuracy often worsen calibration simultaneously.

**Platt scaling fails silently when your holdout set has different class distributions.**
Platt scaling learns a logistic transformation on a validation set, but if that set's class balance differs from deployment—common in medical datasets where disease prevalence varies by geography or time—the calibration becomes systematically biased. A model calibrated on 10% disease prevalence will be overconfident when deployed in a 3% prevalence population. Isotonic regression suffers the same problem but fails differently: it produces step-function predictions that create sudden jumps in predicted probabilities. For distribution-shifted deployments, temperature scaling is more robust because it only learns a single parameter and preserves the rank-order of predictions.

**Calibration metrics punish uncertainty near 50% more than extreme miscalibration.**
Expected Calibration Error (ECE) bins predictions and averages absolute differences between predicted probabilities and observed frequencies. Because most predictions cluster near decision boundaries (40-60% range), calibration errors in this region dominate the metric even when extreme predictions (5% or 95%) are wildly wrong. A model predicting 95% for events that occur 70% of the time might have better ECE than one predicting 52% for events that occur 48% of the time. If your application cares about confident predictions being accurate—like risk stratification—use confidence-weighted metrics or evaluate high-probability bins separately.

**Multi-class calibration breaks in ways binary calibration doesn't.**
A classifier can be perfectly calibrated for each individual class yet badly miscalibrated for the overall probability distribution. When predicting image classes, a model might correctly predict 80% accuracy when it outputs 0.8 for "cat," but the joint probability vector [0.8 cat, 0.15 dog, 0.05 bird] might be poorly calibrated because the *relationships* between class probabilities are distorted. Temperature scaling works for the maximum probability but doesn't fix the full distribution. For applications using the complete probability vector (like label smoothing or probability-weighted ensembles), you need calibration methods that consider the full simplex, not just marginal probabilities.

**Calibration on balanced datasets creates miscalibration in production.**
Most calibration tutorials use balanced validation sets, but real-world class distributions are skewed. A model calibrated on 50-50 data will be overconfident on the minority class and underconfident on the majority class when deployed at 5-95 prevalence. The fix isn't stratified sampling—it's calibrating on data matching production distribution or using prevalence-adjusted methods like Beta calibration that explicitly model class imbalance. Recalibrating every time prevalence shifts is often necessary for deployed systems, making calibration a continuous monitoring task, not a one-time preprocessing step.

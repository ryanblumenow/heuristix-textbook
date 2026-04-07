# Model Rare Events

## The 60-Second Version

**What it does:** Model Rare Events adjusts your prediction models to find needles in haystacks—accurately identifying uncommon but critical outcomes like fraud, equipment failures, or customer churn when they represent less than 5% of your data.

**When to use it:** When the event you're trying to predict almost never happens, but catching it when it does is far more valuable than being right about all the times it doesn't.

**What you get back:** A prediction model that actually flags rare events before they occur, rather than one that simply predicts "nothing will happen" and achieves 95%+ accuracy while missing everything that matters.

| | |
|---|---|
| **Difficulty** | Moderate |
| **Typical runtime** | Minutes on 100K rows (varies by technique) |
| **What you bring** | Historical data where the outcome rarely occurs |
| **What you get** | Calibrated predictions that catch rare events |
| **Heuristix bucket** | Understand — Statistical Analysis & Profiling |

**Standard models optimised for accuracy will systematically ignore your rare events because they've learned that "never happens" is usually correct.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify business scenarios where rare event modeling is essential—such as fraud detection, equipment failure prediction, customer churn in low-attrition environments, and loan default forecasting—and distinguish them from standard classification problems.

- Interpret precision-recall curves, lift charts, and class-specific performance metrics to explain to stakeholders why a model that appears "only 85% accurate" may actually be performing exceptionally well for rare events.

- Set decision thresholds that balance false alarms against missed events based on the specific business costs of Type I versus Type II errors in contexts like medical diagnosis, safety incidents, or credit risk.

**After reading this chapter, a data scientist will be able to:**

- Implement appropriate resampling strategies (SMOTE, ADASYN, Tomek links, or hybrid approaches) while avoiding data leakage by applying them only within cross-validation folds and on training data exclusively.

- Tune class weights, sampling ratios, and probability thresholds by systematically evaluating trade-offs between sensitivity and specificity using stratified validation sets that preserve the rare event base rate.

- Diagnose model failures specific to imbalanced data—including majority class collapse, probability miscalibration, and overfitting to synthetic samples—using calibration plots, confusion matrices at multiple thresholds, and performance stability across time windows.

## Overview

Model Rare Events encompasses a family of statistical and machine learning techniques specifically designed to handle classification and prediction tasks where the outcome of interest occurs with very low frequency—typically less than 5% of observations, and often below 1%. These methods address the fundamental challenge that standard modelling approaches systematically underpredict rare outcomes because they optimise for overall accuracy, which is dominated by the majority class. The techniques span resampling strategies (oversampling, undersampling, hybrid methods), cost-sensitive learning, specialised algorithms, and calibration procedures that together enable reliable inference and prediction when the signal is sparse.

## When to Use This

**Use this when:**

- **Fraud detection in financial transactions** — Fraudulent transactions typically represent 0.1–1% of all transactions; standard classifiers will learn to predict "not fraud" almost universally, missing the cases that matter most.

- **Medical diagnosis of rare conditions** — When screening for diseases with low prevalence, you need models that maintain high sensitivity without generating unacceptable false positive rates.

- **Churn prediction in low-attrition industries** — In sectors like utilities or insurance where annual churn may be 2–3%, the minority class contains all the actionable intelligence.

- **Manufacturing defect detection** — Quality control processes where defect rates are engineered to be very low (Six Sigma aims for 3.4 defects per million) require specialised modelling to identify failure patterns.

- **Insurance claims for catastrophic events** — Predicting total losses, large claims, or specific peril types that occur infrequently but carry enormous financial consequences.

- **Cybersecurity intrusion detection** — Malicious network events are vastly outnumbered by legitimate traffic, yet missing a single intrusion can be catastrophic.

- **Customer conversion in low-engagement contexts** — When conversion rates are below 1% (e.g., cold outreach campaigns), standard models provide little discriminative value.

**Do NOT use this when:**

- **Class balance is moderate** — If your minority class represents 20–40% of observations, standard techniques with appropriate evaluation metrics are typically sufficient.

- **You have extremely small datasets** — With fewer than a few hundred minority class examples, even rare event techniques may not extract reliable signal; consider Bayesian approaches or expert systems instead.

- **The rare event is definitionally uninteresting** — If the business problem does not weight the minority class more heavily than the majority, artificially rebalancing distorts the decision boundary in unhelpful ways.

## Questions This Answers

### Detection and Prevention

**Why are we missing the fraudulent transactions that end up costing us millions, even though they're only 0.3% of all transactions?**

**Can we identify which of our 50,000 active customers are actually going to default in the next 90 days when historically only 1-2% do?**

**How do we predict which equipment failures will cause production shutdowns when they happen less than once per thousand operating hours?**

**What patterns separate the 0.5% of insurance claims that turn out to be fraudulent from the 99.5% that are legitimate?**

**Why does our current churn model keep saying everyone will stay when we know 2-3% will leave each month?**

### Resource Allocation and Intervention

**If we can only audit 500 tax returns out of 100,000 submissions, which ones should we prioritize to catch the most non-compliance?**

**Should we deploy our limited fraud investigation team to review all flagged transactions or focus only on high-confidence cases?**

**Which 1% of our patient population is most likely to be readmitted within 30 days so we can intervene early?**

**How do we allocate our quality inspection resources when defects occur in less than 0.8% of production runs?**

### Performance and Optimization

**Why does our model say it's 98% accurate but still misses almost every critical event we care about?**

**Is it better to contact 1,000 customers and catch 60% of potential churners, or contact 5,000 and catch 85%?**

**What's the ROI of improving our rare event detection from 40% to 70% when each missed event costs us $50,000?**

**How much should we invest in prevention systems when the events we're trying to stop only happen 200 times per year across millions of transactions?**

## How It Works

Imagine you're a security analyst at an airport screening 10,000 passengers daily, trying to catch the roughly 5 people who might pose a threat. If you built a system that simply flagged nobody and said "all clear" every single day, you'd be right 99.95% of the time—an impressive accuracy rate by conventional standards. But you'd be catastrophically wrong where it matters most, missing every actual threat. This is exactly the trap standard prediction models fall into with rare events: they achieve high overall accuracy by essentially ignoring the rare outcome, because predicting "no" all the time keeps their error rate low when measured across all cases.

```
ORIGINAL IMBALANCED DATASET
┌─────────────────────────────────────┐
│ ○○○○○○○○○○○○○○○○○○○○ (950 normal)  │
│ ●●                    (50 rare)     │
└─────────────────────────────────────┘
        ↓
MODEL SEES OVERWHELMING MAJORITY
  learns: "just predict normal"
        ↓
┌─────────────────────────────────────┐
│         REBALANCING                 │
│  ┌──────────┬──────────────────┐   │
│  │ Oversample│  Undersample     │   │
│  │  rare ●  │   normal ○       │   │
│  └──────────┴──────────────────┘   │
└─────────────────────────────────────┘
        ↓
BALANCED TRAINING SET
┌─────────────────────────────────────┐
│ ○○○○○○○○○○         (500 normal)     │
│ ●●●●●●●●●●         (500 rare)       │
└─────────────────────────────────────┘
   Model now pays equal attention
   to both outcomes when learning
```

**Identify the imbalance.** The process starts by measuring how skewed your dataset is. If fraudulent transactions represent just 0.5% of your data, standard models will optimize for the 99.5%—essentially learning to predict "not fraud" nearly every time. Rare events modeling recognizes this numerical tyranny of the majority and prepares to correct it.

**Rebalance the training data.** The algorithm adjusts what the model sees during learning. This happens through oversampling (creating synthetic copies of rare cases, or generating new similar examples), undersampling (randomly removing majority cases), or hybrid approaches that do both. If you had 100 rare events and 9,900 common ones, you might oversample the rare cases to 4,000 and undersample the common ones to 6,000, giving the model a more balanced view.

**Apply cost-sensitive weights.** Rather than treating all mistakes equally, the algorithm can assign different penalties. Missing a rare event might cost 100 times more than a false alarm. The model then optimizes not for overall accuracy, but for minimizing this weighted cost. It's like telling the system: "I'd rather flag 50 false positives than miss 1 true case."

**Train with specialized algorithms.** Some techniques like SMOTE (Synthetic Minority Over-sampling Technique) create intelligent synthetic examples by finding rare cases that are similar and generating new points between them. Others use ensemble methods, training multiple models on different balanced samples and combining their predictions to catch rare events that individual models might miss.

**Calibrate prediction thresholds.** Standard models use a 50% probability cutoff—if the predicted chance exceeds 50%, classify as the event. Rare event models adjust this, perhaps flagging anything above 10% as worth investigating, dramatically improving detection rates while accepting more false positives where the cost is lower.

**The key insight:** Rare events modeling works because it forces the algorithm to care about the minority class by either changing what it sees during training or changing what it values in its predictions, overriding the natural tendency to optimize for the numerically dominant outcome.

## The Intuition

Imagine you are training a new airport security screener. You show them one million bags, of which 999,000 are perfectly innocent and 1,000 contain contraband. If the screener simply learns to say "innocent" to every bag, they achieve 99.9% accuracy—a number that looks excellent on paper but represents complete operational failure. The screener has learned nothing useful about identifying threats; they have merely learned the base rate.

This is precisely the challenge with rare event modelling. Standard learning algorithms minimise some measure of overall prediction error, and when one class dominates, the algorithm can achieve impressive error rates by essentially ignoring the minority class. The mathematics of optimisation do not care about your business priorities—they care about the objective function you specify. If your objective treats all errors equally, and 99% of your data belongs to one class, the algorithm will rationally focus on getting that 99% correct.

Rare event techniques intervene at various points in the modelling pipeline to rebalance this calculus. Resampling methods alter the training data distribution so that the algorithm sees a more balanced picture during learning. Cost-sensitive methods modify the objective function itself, penalising minority-class errors more heavily than majority-class errors. Algorithmic approaches build models that are structurally better suited to finding rare patterns—ensemble methods that specifically seek out minority examples, or anomaly detection frameworks that treat the problem as finding deviations from normality rather than classification per se.

The key insight is that "accuracy" is the wrong goal when events are rare. What matters is discrimination—the model's ability to rank observations by their likelihood of belonging to the minority class—and calibration—the model's ability to produce probability estimates that reflect true underlying frequencies. A model might have lower accuracy than a naive baseline but vastly superior discrimination, making it far more valuable for targeting interventions, setting thresholds, or understanding risk factors.

## The Mathematics

### Problem Setup and Notation

Let $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^{n}$ be a training dataset where $\mathbf{x}_i \in \mathbb{R}^p$ is a feature vector and $y_i \in \{0, 1\}$ is a binary outcome. Define:

- $n_1 = \sum_{i=1}^{n} y_i$ as the count of minority class observations
- $n_0 = n - n_1$ as the count of majority class observations
- $\pi = n_1 / n$ as the empirical minority class proportion

We consider the rare event setting where $\pi \ll 0.5$, typically $\pi < 0.05$.

### The Class Imbalance Problem

Consider logistic regression with maximum likelihood estimation. The log-likelihood is:

$$
\ell(\boldsymbol{\beta}) = \sum_{i=1}^{n} \left[ y_i \log p_i + (1 - y_i) \log(1 - p_i) \right]
$$

where $p_i = \sigma(\mathbf{x}_i^T \boldsymbol{\beta})$ and $\sigma(z) = (1 + e^{-z})^{-1}$.

When $n_0 \gg n_1$, the likelihood is dominated by the $(1 - y_i) \log(1 - p_i)$ terms. The MLE will favour parameter values that push $p_i$ toward zero for most observations, including many true positives.

### Resampling Methods

#### Random Oversampling

Replicate minority class observations to achieve target ratio $\pi^* > \pi$:

$$
w_i = \begin{cases} 1 & \text{if } y_i = 0 \\ k & \text{if } y_i = 1 \end{cases}
$$

where $k = \frac{n_0 \pi^*}{n_1 (1 - \pi^*)}$ achieves the desired balance.

#### SMOTE (Synthetic Minority Oversampling Technique)

For each minority observation $\mathbf{x}_i$ with $y_i = 1$:

1. Find $K$ nearest neighbours among minority class: $\{\mathbf{x}_{i_1}, \ldots, \mathbf{x}_{i_K}\}$
2. Randomly select neighbour $\mathbf{x}_{i_j}$
3. Generate synthetic example:

$$
\mathbf{x}_{\text{new}} = \mathbf{x}_i + \lambda (\mathbf{x}_{i_j} - \mathbf{x}_i)
$$

where $\lambda \sim \text{Uniform}(0, 1)$.

#### Random Undersampling

Sample majority class to match minority:

$$
\mathcal{D}_{\text{under}} = \mathcal{D}_1 \cup \text{Sample}(\mathcal{D}_0, n_1)
$$

This discards information but creates computational efficiency and can reduce overfitting to majority class patterns.

### Cost-Sensitive Learning

Modify the loss function to weight errors asymmetrically. For logistic regression with class weights $w_0, w_1$:

$$
\ell_{\text{weighted}}(\boldsymbol{\beta}) = \sum_{i=1}^{n} \left[ w_1 y_i \log p_i + w_0 (1 - y_i) \log(1 - p_i) \right]
$$

The standard choice is inverse frequency weighting:

$$
w_1 = \frac{n}{2 n_1}, \quad w_0 = \frac{n}{2 n_0}
$$

This makes the total weight contribution of each class equal.

### Rare Events Logistic Regression (King & Zeng)

King and Zeng (2001) demonstrated that logistic regression coefficients are consistent but the intercept $\beta_0$ is biased when events are rare. The bias-corrected intercept is:

$$
\tilde{\beta}_0 = \hat{\beta}_0 - \ln\left[\frac{(1-\tau)\pi}{\tau(1-\pi)}\right]
$$

where $\tau$ is the true population proportion and $\pi$ is the sample proportion. Additionally, they propose a correction to the variance-covariance matrix:

$$
\tilde{V}(\hat{\boldsymbol{\beta}}) = V(\hat{\boldsymbol{\beta}}) + \frac{1}{n}Q(\hat{\boldsymbol{\beta}})
$$

where $Q$ is a correction matrix accounting for the finite-sample bias.

### Evaluation Metrics for Rare Events

Standard accuracy is inappropriate. Define the confusion matrix elements: TP, FP, TN, FN.

**Precision and Recall:**

$$
\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}
$$

**F-beta Score** (weighing recall $\beta$ times as important as precision):

$$
F_\beta = (1 + \beta^2) \cdot \frac{\text{Precision} \cdot \text{Recall}}{\beta^2 \cdot \text{Precision} + \text{Recall}}
$$

**Area Under the Precision-Recall Curve (AUPRC):**

More informative than AUROC for imbalanced data. A random classifier achieves AUPRC $\approx \pi$, providing a meaningful baseline.

**Matthews Correlation Coefficient:**

$$
\text{MCC} = \frac{\text{TP} \cdot \text{TN} - \text{FP} \cdot \text{FN}}{\sqrt{(\text{TP}+\text{FP})(\text{TP}+\text{FN})(\text{TN}+\text{FP})(\text{TN}+\text{FN})}}
$$

This metric is balanced and informative even when classes are highly imbalanced.

### Probability Calibration

After resampling or cost-sensitive training, predicted probabilities no longer reflect true frequencies. Platt scaling fits a logistic transformation:

$$
P_{\text{calibrated}}(y=1|\hat{p}) = \sigma(A\hat{p} + B)
$$

where $A$ and $B$ are fit on a held-out calibration set.

## Understanding the Mathematics

### Imbalance Ratio

**The equation:**
$$IR = \frac{n_{majority}}{n_{minority}}$$

**Read it aloud:**
The imbalance ratio equals the number of majority class observations divided by the number of minority class observations.

**What each symbol means:**
- $IR$ = imbalance ratio, a measure of how skewed your dataset is
- $n_{majority}$ = count of observations in the majority (common) class
- $n_{minority}$ = count of observations in the minority (rare) class

**A concrete numerical example:**
A fraud detection system monitors 100,000 credit card transactions. Of these, 99,500 are legitimate and 500 are fraudulent. The imbalance ratio is:
$$IR = \frac{99,500}{500} = 199$$

This means legitimate transactions outnumber fraudulent ones by 199 to 1.

**Why this equation matters:**
Without quantifying the imbalance, we cannot select appropriate techniques or interpret model performance—a 99% accurate model that predicts "no fraud" for every transaction is useless but looks impressive.

### Precision and Recall Trade-off

**The equations:**
$$Precision = \frac{TP}{TP + FP}$$
$$Recall = \frac{TP}{TP + FN}$$

**Read it aloud:**
Precision equals true positives divided by the sum of true positives and false positives. Recall equals true positives divided by the sum of true positives and false negatives.

**What each symbol means:**
- $Precision$ = proportion of predicted rare events that were actually rare events
- $Recall$ = proportion of actual rare events that we successfully identified
- $TP$ = true positives (correctly predicted rare events)
- $FP$ = false positives (wrongly predicted rare events)
- $FN$ = false negatives (missed rare events)

**A concrete numerical example:**
A hospital screening system evaluates 1,000 patients for a rare disease. It flags 80 patients as high-risk. Of those 80, only 60 actually have the disease (TP = 60, FP = 20). Meanwhile, 15 diseased patients weren't flagged (FN = 15).

$$Precision = \frac{60}{60 + 20} = \frac{60}{80} = 0.75$$
$$Recall = \frac{60}{60 + 15} = \frac{60}{75} = 0.80$$

The system correctly identifies 75% of its predictions and catches 80% of all disease cases.

**Why this equation matters:**
Accuracy is meaningless for rare events—these metrics reveal whether you're catching the rare cases (recall) without flooding operations with false alarms (precision).

### SMOTE Synthetic Sample Generation

**The equation:**
$$x_{synthetic} = x_i + \lambda \times (x_{neighbor} - x_i)$$

**Read it aloud:**
A synthetic sample equals an original minority sample plus a random fraction multiplied by the difference between a neighboring minority sample and the original sample.

**What each symbol means:**
- $x_{synthetic}$ = new artificial minority class observation
- $x_i$ = an existing minority class observation
- $x_{neighbor}$ = a nearby minority class observation (one of its k-nearest neighbors)
- $\lambda$ = random number between 0 and 1

**A concrete numerical example:**
A bank has few loan default examples. One defaulter had income = $45,000 and debt = $30,000. A nearby defaulter had income = $50,000 and debt = $35,000. With $\lambda = 0.6$:

For income:
$$x_{synthetic} = 45,000 + 0.6 \times (50,000 - 45,000) = 45,000 + 0.6 \times 5,000 = 48,000$$

For debt:
$$x_{synthetic} = 30,000 + 0.6 \times (35,000 - 30,000) = 30,000 + 3,000 = 33,000$$

The synthetic defaulter has income = $48,000 and debt = $33,000.

**Why this equation matters:**
This creates plausible new minority examples without simply copying existing ones, giving models more patterns to learn from while avoiding overfitting to the handful of rare observations.

### The Big Picture

The mathematics of rare event modeling fundamentally tries to rebalance the learning process so that infrequent outcomes receive proportional attention despite their scarcity. Traditional methods optimize for overall correctness, which statistically drowns out the rare signal—the imbalance ratio quantifies this drowning effect. Precision and recall replace accuracy because they force us to evaluate performance specifically on the minority class we care about, not the easy-to-predict majority. SMOTE's interpolation approach creates training diversity without naive duplication, allowing algorithms to develop richer decision boundaries around sparse regions of feature space. At its core, rare event mathematics transforms a needle-in-haystack problem into one where the needle is amplified, weighted, or synthesized until standard algorithms can finally see it.

## Python Implementation

```python
"""
Rare Event Modelling: Complete Implementation Example
Demonstrates resampling, cost-sensitive learning, and proper evaluation
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, precision_recall_curve, 
    average_precision_score, roc_auc_score, confusion_matrix,
    f1_score, matthews_corrcoef
)
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek
from imblearn.pipeline import Pipeline as ImbPipeline
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. Generate Realistic Imbalanced Dataset
# ============================================================
# Simulating fraud detection: 2% positive rate
X, y = make_classification(
    n_samples=50000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    n_clusters_per_class=3,
    weights=[0.98, 0.02],  # 2% minority class
    flip_y=0.01,           # Small label noise
    random_state=42
)

# Convert to DataFrame for realistic handling
feature_names = [f'feature_{i}' for i in range(20)]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

print("Dataset Overview:")
print(f"Total samples: {len(df):,}")
print(f"Positive class: {df['target'].sum():,} ({df['target'].mean():.2%})")
print(f"Negative class: {(1-df['target']).sum():,} ({1-df['target'].mean():.2%})")

# Train/test split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

print(f"\nTraining set positive rate: {y_train.mean():.2%}")
print(f"Test set positive rate: {y_test.mean():.2%}")

# ============================================================
# 2. Baseline Model (No Rare Event Handling)
# ============================================================
print("\n" + "="*60)
print("BASELINE MODEL (No imbalance handling)")
print("="*60)

baseline_model = LogisticRegression(max_iter=1000, random_state=42)
baseline_model.fit(X_train, y_train)

y_pred_baseline = baseline_model.predict(X_test)
y_prob_baseline = baseline_model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred_baseline, digits=3))
print(f"AUROC: {roc_auc_score(y_test, y_prob_baseline):.3f}")
print(f"AUPRC: {average_precision_score(y_test, y_prob_baseline):.3f}")
print(f"MCC: {matthews_corrcoef(y_test, y_pred_baseline):.3f}")

# ============================================================
# 3. Cost-Sensitive Learning
# ============================================================
print("\n" + "="*60)
print("COST-SENSITIVE LOGISTIC REGRESSION")
print("="*60)

# Using 'balanced' automatically computes inverse frequency weights
cost_sensitive_model = LogisticRegression(
    class_weight='balanced',  # Key parameter for rare events
    max_iter=1000,
    random_state=42
)
cost_sensitive_model.fit(X_train, y_train)

y_pred_cs = cost_sensitive_model.predict(X_test)
y_prob_cs = cost_sensitive_model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred_cs, digits=3))
print(f"AUROC: {roc_auc_score(y_test, y_prob_cs):.3f}")
print(f"AUPRC: {average_precision_score(y_test, y_prob_cs):.3f}")
print(f"MCC: {matthews_corrcoef(y_test, y_pred_cs):.3f}")

# ============================================================
# 4. SMOTE Oversampling
# ============================================================
print("\n" + "="*60)
print("SMOTE OVERSAMPLING + LOGISTIC REGRESSION")
print("="*60)

# Apply SMOTE to training data only
smote = SMOTE(sampling_strategy=0.5, k_neighbors=5, random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f"Original training size: {len(y_train):,}")
print(f"After SMOTE: {len(y_train_smote):,}")
print(f"New positive rate: {y_train_smote.mean():.2%}")

smote_model = LogisticRegression(max_iter=1000, random_state=42)
smote_model.fit(X_train_smote, y_train_smote)

y_pred_smote = smote_model.predict(X_test)
y_prob_smote = smote_model


## Visualisations

![](../../_static/figures/model-rare-events_fig1.png)
![](../../_static/figures/model-rare-events_fig2.png)

## Using This in Heuristix

### What Data You'll Need

The **Model Rare Events** node expects a prepared dataset with your outcome variable already defined. You'll need:

- **Target column**: Binary (0/1, Yes/No, True/False) with the rare event typically representing less than 5% of cases
- **Feature columns**: Numeric or categorical predictors that help explain the rare event
- **Minimum rows**: At least 1,000 observations recommended, with at least 30-50 instances of the rare event

**Example input data:**

| customer_id | transaction_amount | account_age_days | previous_disputes | is_fraud |
|-------------|-------------------|------------------|-------------------|----------|
| 10234 | 156.32 | 892 | 0 | 0 |
| 10235 | 8943.21 | 45 | 2 | 1 |
| 10236 | 67.89 | 1205 | 0 | 0 |

The node will use `is_fraud` as the target (rare event = 1) and the other columns as predictors.

### Configuration Parameters

| Parameter | What It Controls | Sensible Default | When to Change It |
|-----------|-----------------|------------------|-------------------|
| **Target Column** | Which column contains the rare event | First binary column | Always specify this explicitly |
| **Sampling Strategy** | How to balance classes: "oversample", "undersample", "hybrid", "SMOTE" | "hybrid" | Use SMOTE for very small datasets; undersample if you have millions of rows |
| **Sampling Ratio** | Target ratio of minority to majority class | 0.3 (30%) | Increase to 0.5 for extremely rare events (<0.5%); decrease if model overcompensates |
| **Cost Sensitivity** | Penalty multiplier for misclassifying rare events | 10 | Increase to 20-50 when false negatives are very costly (medical diagnosis, fraud) |
| **Algorithm** | Model type: "logistic", "random_forest", "xgboost", "ensemble" | "ensemble" | Use logistic for interpretability; xgboost for maximum performance |
| **Calibration Method** | Post-processing to fix probability estimates: "platt", "isotonic", "none" | "isotonic" | Switch to Platt if you have <1,000 rare event samples |
| **Validation Method** | "stratified_cv", "time_series", "holdout" | "stratified_cv" | Use time_series if event timing matters; holdout for very large datasets |

### What You'll Get Back

The node produces several outputs to help you understand and deploy your rare event model:

**New columns added to your data:**
- `predicted_probability`: Likelihood score (0-1) for each observation
- `predicted_class`: Binary prediction using optimized threshold
- `prediction_confidence`: Model certainty in the prediction

**Model Performance Metrics:**
- Standard metrics (precision, recall, F1-score, AUC-ROC)
- **Precision-Recall curve**: Critical for rare events—shows the tradeoff better than ROC
- **Confusion matrix** at the optimized threshold
- **Cost-benefit analysis**: Expected value based on your cost sensitivity setting

**Visualizations:**
- Feature importance chart showing which predictors matter most
- Threshold analysis plot to help you choose different cutoffs for different use cases
- Calibration plot showing if probabilities are trustworthy

### Connecting Downstream

This node pairs naturally with:

- **Score New Data** node: Apply your trained model to fresh observations
- **Threshold Optimizer** node: Fine-tune the decision boundary for specific business goals
- **Model Explainer** node: Generate interpretable explanations for individual predictions
- **Monitor Model Drift** node: Track if your rare event patterns change over time

### Quick Start

1. **Connect your prepared dataset** to the Model Rare Events node input
2. **Select your target column** from the dropdown (the rare event you're predicting)
3. **Keep the default "hybrid" sampling strategy** and "ensemble" algorithm for your first run
4. **Set the cost sensitivity** based on business impact—start with 10, increase if false negatives are very expensive
5. **Run the node** and examine the Precision-Recall curve first
6. **Adjust the sampling ratio** if your model is too conservative or aggressive
7. **Connect to Score New Data** once you're satisfied with performance

### Practical Tips from the Field

**Tip 1**: Don't trust overall accuracy—a model that predicts "no fraud" for everyone gets 99% accuracy when fraud is 1%, but it's useless. Focus on precision, recall, and F1-score instead.

**Tip 2**: The optimized threshold is rarely 0.5. Your model might predict best at 0.15 or 0.73—let the node find this for you based on your cost sensitivity.

**Tip 3**: If you have time-ordered data (fraud over months, equipment failures over years), always use time_series validation. Standard cross-validation will leak future information and give falsely optimistic results.

**Tip 4**: Start with fewer features rather than more. With rare events, complex models easily overfit to noise. Try 5-10 strong predictors before adding everything.

**Tip 5**: Save the probability scores, not just the binary predictions. Downstream teams can create different rules (flag top 2% for manual review, auto-block top 0.1%) using the same model.

## Config Recipes

### Recipe 1: Quick Exploration with Severe Imbalance

**When to use:** Initial exploration of datasets with extreme imbalance (< 1% positive class) where you need fast feedback on whether signal exists before investing in elaborate pipelines.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `sampling_strategy` | 0.1 | Undersample majority to 10:1 ratio—fast while preserving some context |
| `model` | `LogisticRegression(max_iter=100)` | Simplest baseline; terminates quickly |
| `cv` | 3 | Minimal cross-validation for speed |
| `scoring` | `'average_precision'` | Robust to imbalance without threshold dependence |
| `class_weight` | `None` | Resampling handles imbalance; no double-correction |

**What you get:** A 5-minute runtime checkpoint revealing whether predictive signal exists and which features show promise in initial coefficients.

**Trade-off:** Aggressive undersampling discards majority-class information that might contain critical boundary cases.

### Recipe 2: Production-Grade Fraud Detection

**When to use:** Deploying a rare event model (0.1–2% fraud rate) in production where false positives have quantifiable costs and regulatory audit is likely.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `sampling_strategy` | `'auto'` with SMOTE | Synthetic oversampling preserves all real cases |
| `model` | `LGBMClassifier(n_estimators=500, max_depth=6, scale_pos_weight=50)` | Gradient boosting with explicit class weighting for double protection |
| `cv` | `StratifiedKFold(n_splits=10)` | Maximum stability for confidence intervals |
| `scoring` | Custom F-beta (β=2) | Prioritizes recall over precision per business requirements |
| `calibration` | `CalibratedClassifierCV(method='isotonic', cv=5)` | Produces interpretable probabilities for threshold tuning |
| `threshold` | Business-optimized | Set via cost matrix, not default 0.5 |

**What you get:** Calibrated probabilities enabling cost-based decision rules with documented performance across multiple validation folds.

**Trade-off:** Training time increases 10–15× compared to exploration recipe; requires careful SMOTE parameter tuning to avoid overfitting to synthetic examples.

### Recipe 3: Seasonal Events with Temporal Leakage Risk

**When to use:** Predicting rare annual events (product recalls, flash sales, equipment failures) where temporal ordering matters and standard CV would leak future information.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `sampling_strategy` | 0.3 | Conservative ratio preserves temporal patterns in majority class |
| `model` | `RandomForestClassifier(n_estimators=300, min_samples_leaf=10)` | Captures non-linear interactions without extrapolation risk |
| `cv` | `TimeSeriesSplit(n_splits=5, gap=30)` | Respects temporal order with 30-day gap preventing leakage |
| `scoring` | `'roc_auc'` | Time-ordered predictions need rank quality, not precision/recall |

**What you get:** Validated performance reflecting true forward-prediction capability without optimistic bias from temporal leakage.

**Trade-off:** Severely reduced training data per fold (only past available); early folds may have zero positive cases requiring careful fold design.

### Recipe 4: Ultra-Rare Catastrophic Events (Anomaly Detection Alternative)

**When to use:** Events occurring in < 0.01% of cases (system failures, sentinel diagnoses) where you have rich features but unsupervised anomaly detection has failed due to normal operational variation.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `sampling_strategy` | `{0: 500, 1: 'all'}` | Cap majority at fixed count; use every rare example |
| `model` | `XGBClassifier(n_estimators=1000, learning_rate=0.01, subsample=0.8, scale_pos_weight=100)` | Slow learning prevents memorization of tiny positive class |
| `ensemble` | 50 bootstrap replicates | Stability through aggregation when positive class = dozens |
| `cv` | Leave-one-out on positives | With n=20 positives, stratified K-fold fails |

**What you get:** Ensemble predictions stable enough for monitoring despite training on perhaps 20–100 positive examples total.

**Trade-off:** Model is fundamentally a highly-regularized pattern matcher, not a probability estimator; requires domain validation that discovered patterns are causal.

## Business Applications

**Financial Services**

A mid-sized UK mortgage lender processes 45,000 loan applications annually, of which fewer than 0.8% result in fraud. Standard credit-scoring models flagged legitimate applications as suspicious at four times the rate of actual fraud, creating backlogs and customer friction. By implementing cost-sensitive random forests with SMOTE oversampling, the lender reduced false positives by 34% while maintaining 92% fraud detection accuracy, translating to £780,000 in annual savings from reduced manual review costs and 2.3 fewer days in average application processing time.

**Retail**

An e-commerce fashion retailer with 1.2M SKUs faced a persistent problem: only 1.4% of launched products became bestsellers (top 5% revenue), yet inventory decisions were made months in advance. Traditional regression models optimised for average performance missed the signal entirely, predicting bestsellers no better than random chance. Rare event logistic regression with stratified sampling identified early indicators—social media engagement velocity, micro-influencer pickup, and search trend acceleration—lifting bestseller prediction accuracy from 18% to 61%, which prevented £2.1M in excess inventory write-downs over one season.

**Healthcare**

A regional hospital network serving 340,000 patients annually needed to predict which emergency department visitors would require ICU admission within 72 hours—an outcome occurring in just 2.1% of cases. Standard triage protocols caught only 54% of these patients early enough to improve outcomes. An ensemble model combining weighted logistic regression and balanced bagging increased early identification to 81% sensitivity while reducing unnecessary ICU alerts by 29%, enabling targeted intervention that reduced average ICU length-of-stay by 1.8 days and contributed to an estimated $4.3M in cost avoidance.

**Insurance**

A commercial property insurer writing 23,000 policies discovered that catastrophic claims (exceeding £500K) represented 0.6% of incidents but 41% of total payouts. Actuarial models calibrated on frequency underpriced high-severity risks by an average of 18%. Cost-sensitive gradient boosting with asymmetric loss functions recalibrated pricing for rare-but-severe events, identifying 14 previously unrecognised risk factors including supplier concentration and ageing HVAC systems. The revised pricing strategy reduced loss ratio on high-value policies from 89% to 71% within two renewal cycles.

**Manufacturing**

A automotive component manufacturer operating six factories experienced critical equipment failures—complete line stoppages—in only 0.3% of operating shifts, yet each failure cost $47,000 in lost production and emergency repairs. Time-series sensor data from 340 variables produced overwhelming noise that masked failure signatures. One-class SVM combined with undersampled neural networks identified pre-failure patterns 6-18 hours in advance with 73% accuracy, enabling preventive intervention that cut unplanned downtime by 220 hours annually and saved an estimated $1.8M.

**Logistics**

A national parcel carrier handling 8M packages weekly faced delivery exceptions (damaged, lost, or refused) in 0.9% of shipments—small percentage, enormous cost. Standard quality models optimised overall delivery rates but failed to predict exceptions. Weighted XGBoost with focal loss identified that exceptions clustered around specific route-driver-weather-packaging combinations, enabling targeted interventions that reduced exception rates to 0.61%, saving $3.2M annually in redelivery costs and customer compensation.

**Marketing**

A B2B SaaS company with 140,000 freemium users saw only 1.2% convert to paid enterprise contracts, yet these conversions represented 78% of revenue. Lead scoring models trained on overall conversion optimised for small-business upgrades while missing enterprise signals entirely. Rare event modelling with synthetic minority oversampling revealed that API usage patterns and team collaboration metrics predicted enterprise conversion 11 days earlier than traditional scoring, lifting conversion rates from 1.2% to 1.9%—a seemingly modest increase worth $4.7M in additional ARR.

**Telecommunications**

A mobile network operator discovered that customer complaints escalating to regulatory intervention occurred in just 0.4% of support interactions but generated 94% of compliance costs. Rare event classification using cost-proportionate weighting identified complaint escalation risk from transcript sentiment, resolution time, and repeat-contact patterns, flagging high-risk cases for senior agent assignment and reducing regulatory escalations by 58%.

**Energy**

A wind farm operator managing 340 turbines across twelve sites needed to predict blade failures occurring in 0.7% of inspections. Imbalanced learning techniques combining oversampling with ensemble methods improved prediction accuracy from 31% to 76%, enabling condition-based maintenance that extended blade life by an average 14 months and avoided $890,000 in emergency replacements annually.

**Public Sector**

A metropolitan fire service responding to 28,000 calls yearly needed to predict which incidents would require mutual aid (multiple stations)—just 2.3% of calls but resource-critical for response planning. Calibrated rare event models using incident type, location, time, and weather data improved mutual-aid prediction from 41% to 79% accuracy, optimising station positioning and reducing average response time to major incidents by four minutes.

**SaaS/Tech**

A cybersecurity platform monitoring 2.4M daily authentication events across client networks detected genuine account takeovers in only 0.05% of flagged anomalies. Alert fatigue led security teams to ignore 83% of warnings. Precision-focused rare event detection using asymmetric penalty matrices reduced false positives by 91% while maintaining 94% breach detection, transforming the platform from liability to competitive advantage and supporting a 340% increase in enterprise client retention.

## Worked Example

Sarah Chen, a senior data scientist at Meridian Insurance, was already halfway through her morning coffee when the Slack message arrived from the fraud prevention team: "We're missing millions in fraudulent claims. Can you help us predict them better?" The current rule-based system flagged only 12% of actual fraud cases, and the executive team wanted to know if machine learning could do better. The stakes were clear—Meridian was processing 50,000 claims monthly, with fraud occurring in roughly 0.8% of cases but costing an average of $15,000 per incident.

Sarah pulled together six months of historical claims data, joining transaction records with investigator outcomes. The dataset wasn't pretty—typical insurance data never is. Some claim amounts were missing, timestamps were in three different formats, and the fraud investigation team had used inconsistent coding for their final determinations until three months ago when someone finally standardized it.

| claim_id | claim_amount | claimant_age | prior_claims | same_day_filing | is_fraud |
|----------|--------------|--------------|--------------|-----------------|----------|
| C10447   | 8500         | 34           | 0            | 0               | 0        |
| C10448   | 22000        | 52           | 2            | 0               | 0        |
| C10449   | 3200         | 29           | 1            | 1               | 1        |
| C10450   | 95000        | 41           | 0            | 0               | 0        |
| C10451   | 15500        | 38           | 4            | 1               | 1        |

After cleaning and feature engineering, Sarah had 31,000 usable claims with 248 confirmed fraud cases—exactly 0.8%. She knew from experience that feeding this directly into a standard logistic regression or random forest would produce a model that simply predicted "not fraud" for almost everything, achieving 99.2% accuracy while being completely useless.

She configured her rare events modeling pipeline carefully. First, she chose SMOTE (Synthetic Minority Over-sampling Technique) for the training set, generating synthetic fraud cases to balance the classes during model fitting. She paired this with random undersampling of legitimate claims at a 1:3 ratio—not fully balanced, which she'd learned could introduce too much noise, but enough to give the model a fighting chance. For the algorithm itself, she selected a random forest with 200 trees, increasing `min_samples_leaf` to 20 to prevent overfitting on the synthetic samples. Critically, she configured cost-sensitive learning with a misclassification cost ratio of 30:1 for missing fraud versus false positives, reflecting the business reality that one missed fraud case cost more than investigating thirty legitimate claims.

```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import pandas as pd

# Sarah's preprocessing and modeling script
# Data already cleaned and split into train/test

# Configure resampling pipeline
smote = SMOTE(sampling_strategy=0.5, random_state=42)
undersample = RandomUnderSampler(sampling_strategy=0.7, random_state=42)
resampler = Pipeline([('smote', smote), ('under', undersample)])

# Resample training data only
X_train_resampled, y_train_resampled = resampler.fit_resample(X_train, y_train)

# Cost-sensitive random forest
# Class weight of 30 based on business cost analysis
rf_model = RandomForestClassifier(
    n_estimators=200,
    min_samples_leaf=20,
    class_weight={0: 1, 1: 30},
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train_resampled, y_train_resampled)

# Evaluate on original unbalanced test set
y_pred = rf_model.predict(X_test)
y_pred_proba = rf_model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")
```

The results transformed the conversation completely. On the holdout test set of 9,000 claims with 72 actual fraud cases, Sarah's model achieved a recall of 68% while maintaining precision at 22%—meaning for every three claims flagged for investigation, one was actually fraudulent, and the model caught two-thirds of all fraud. The ROC-AUC score of 0.83 indicated strong discriminative ability. More importantly, at the 0.3 probability threshold she recommended, the model would flag roughly 220 claims monthly for investigation—a manageable workload that would catch an estimated 34 fraud cases versus the 8 their current system found.

The insight that surprised even Sarah was which features mattered most. While everyone expected claim amount to dominate, the model revealed that temporal patterns—particularly the combination of same-day filing with prior claims history and claimant age under 35—were far stronger fraud signals. Several mid-size claims that looked completely normal in isolation were being filed in suspicious patterns.

Sarah presented these findings to the VP of Claims Operations on a Wednesday afternoon. By Friday, they'd approved a three-month pilot program. The fraud investigation team would receive daily model scores for all new claims above the 0.3 threshold. Within that pilot period, they caught $4.2 million in fraudulent claims, representing a 285% improvement over baseline.

If Sarah were doing this again, she'd spend more time on threshold optimization—the 0.3 cutoff was based on quick analysis, but a formal cost-benefit optimization might have found an even better operating point. She'd also push harder for weekly model retraining; fraud patterns shift quickly, and the quarterly retraining schedule they initially agreed to felt too slow even one month in.

## Interpreting Your Results

You've just trained a rare event model and the output looks nothing like standard classification results. The accuracy is lower, there are metrics you've never heard of, and you're not sure if a recall of 0.42 is cause for celebration or concern. Let's decode exactly what you're looking at.

### Precision-Recall Trade-off

**Plain-English meaning**: Precision tells you "of the cases I flagged as rare events, what percentage actually were?" Recall tells you "of all the actual rare events in my data, what percentage did I catch?" With rare events, you cannot optimise both simultaneously—catching more events (higher recall) means accepting more false alarms (lower precision).

**Concrete benchmarks**:
- **Precision below 0.10**: You're flagging so many false positives that most alerts are noise. Unusable except for initial screening.
- **Precision 0.10–0.30**: Acceptable for high-stakes situations where missing an event is catastrophic (fraud detection, equipment failure). Means 70–90% false alarm rate.
- **Precision above 0.30**: Strong performance for rare events—you're getting signal above noise.
- **Recall below 0.30**: You're missing most events. Only acceptable if follow-up investigation is extremely expensive.
- **Recall 0.30–0.60**: Typical range for rare event models. You're catching a meaningful portion.
- **Recall above 0.60**: Excellent—you're identifying most occurrences while maintaining some precision.

**Red flags**: Precision above 0.70 with recall above 0.70 suggests your event isn't actually rare (check your base rate), or you have data leakage. Precision below 0.05 means your model is barely better than random flagging.

### PR-AUC (Precision-Recall Area Under Curve)

**Plain-English meaning**: This single number summarises model quality across all possible threshold settings. Unlike regular AUC, PR-AUC accounts for class imbalance. It represents the average precision across all recall levels.

**Concrete benchmarks**:
- **PR-AUC below 0.20**: Model is struggling to distinguish events from non-events. For a 1% base rate, random guessing gives ~0.01, so you have weak signal.
- **PR-AUC 0.20–0.50**: Moderate performance. The model has learned meaningful patterns but is far from reliable.
- **PR-AUC above 0.50**: Strong performance for rare events. Actionable for most business contexts.
- **PR-AUC above 0.75**: Exceptional—either you have excellent data or the problem is easier than expected.

**Red flags**: PR-AUC within 0.05 of your base rate means the model has learned almost nothing. PR-AUC above 0.90 with a base rate below 1% warrants leakage investigation.

### Confusion Matrix at Optimal Threshold

**Plain-English meaning**: This shows actual counts of true positives (TP), false positives (FP), true negatives (TN), and false negatives (FN) at the threshold that balances precision and recall.

**Reading the pattern**: With rare events, TN will dominate (typically 90%+ of all cases). Focus on the ratio of TP to FP (precision) and TP to FN (recall). If FP >> TP (false positives vastly outnumber true positives), your precision is too low for most operational use.

**Red flags**: If TP < 10, you have too few positive cases to validate model performance—collect more data or this is exploratory only. If FN = 0 (you caught everything), you've likely overfit or have leakage.

### Feature Importance for Rare Class

**Plain-English meaning**: Which variables most strongly predict the rare event occurring? This differs from standard feature importance, which optimises for majority class accuracy.

**Red flags**: Top feature is an ID, timestamp, or exact-match categorical with thousands of levels—likely leakage. Top features are all highly correlated—you may have redundancy masking interpretability. No features show importance above 0.05—model is relying on noise.

### Reading Multiple Outputs Together

A PR-AUC of 0.45 with precision 0.25 at recall 0.50 tells you: "The model has learned real patterns (decent AUC), and at a practical threshold, I'll catch half the events but deal with 3 false alarms for every real event." That's actionable for fraud screening, weak for medical diagnosis.

High recall (0.70) but PR-AUC below 0.30 means you're catching events by flagging almost everything—check if your threshold is too loose.

### Sanity Check Checklist

1. **Base rate validation**: Does your test set rare event percentage match your training set within 20%?
2. **Baseline beat**: Is PR-AUC at least 3× your base rate? (1% base rate → PR-AUC > 0.03)
3. **Threshold reasonableness**: Are you flagging between 2–20% of cases? Outside this, review threshold selection.
4. **Temporal stability**: If you have time-ordered data, does performance hold in the most recent 20% of data?
5. **Top feature sanity**: Can you explain in plain English why your top 3 features would predict the event?

### Good Enough to Act On?

**Act with confidence** if: PR-AUC > 0.40 AND (precision > 0.20 at recall > 0.40) AND you pass all sanity checks. **Proceed cautiously** if PR-AUC 0.20–0.40—useful for prioritisation but validate with domain experts. **Return to feature engineering** if PR-AUC < 0.20—your signal is too weak for reliable decisions.

## Decision Guidance

### What This Result Is Telling You

When your rare event model produces predictions, it's answering a fundamentally different question than a typical forecasting tool. Instead of telling you "what usually happens," it's identifying the small fraction of cases where something unusual and important is about to occur—fraud, equipment failure, customer churn in a high-value segment, or supply chain disruption. The model is effectively a filtering mechanism: from tens of thousands of normal cases, it's surfacing the handful that deserve immediate human attention or intervention. The quality of this filter determines whether your team spends their time preventing real problems or chasing false alarms.

The predictions come with two critical metrics that reveal the model's reliability. Precision tells you what percentage of the cases the model flags as high-risk actually turn out to be problems—this controls your false alarm rate. Recall tells you what percentage of all actual problems the model successfully catches—this measures what you're missing. A model with 40% precision and 70% recall means that when you investigate 100 flagged cases, 40 will be genuine problems (and you'll waste effort on 60 false positives), but you're still missing 30% of all problems that exist. These aren't academic statistics; they directly determine staffing requirements, intervention costs, and the residual risk your organization carries.

The decision to deploy a rare event model is a resource allocation choice. You're committing people, budget, and attention to investigate or intervene on flagged cases. If the model performs well, you're concentrating resources where they generate maximum impact—preventing losses, protecting customers, or avoiding operational failures. If it performs poorly, you're either burning resources on false alarms, missing critical events, or both. The model's performance metrics tell you exactly what trade-off you're accepting.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Precision >60% and recall >70% | The model reliably identifies rare events with manageable false positives | Deploy to production with standard monitoring; allocate investigation resources based on volume of flagged cases | Operations Manager, Risk Director |
| Precision 30–60% and recall >70% | You're catching most problems but generating significant false alarms | Implement two-tier response: automated handling for moderate-risk flags, human review for high-confidence predictions only | Analytics Lead, Process Owner |
| Recall <50% regardless of precision | You're missing more than half of actual events | Do not deploy for critical decisions; use only as one input among multiple signals or return to model development | Chief Risk Officer, Head of Data Science |
| F1-score improved by >15 percentage points versus baseline | The rare event techniques are delivering material value | Invest in expanding coverage to related use cases and enhancing data collection for flagged cases | VP Analytics, Business Unit Leader |
| Model flags <0.1% or >20% of cases | Detection rate outside expected range suggests miscalibration or data shift | Investigate data quality, recent business changes, or threshold settings before acting on predictions | Data Engineering Lead, Domain Expert |

### When to Proceed vs. Investigate Further

**Proceed with confidence** when precision exceeds 60%, recall exceeds 70%, model has been validated on out-of-time holdout data from the last 3–6 months, and volume of flagged cases aligns with available intervention capacity (typically 2–10% of total cases).

**Proceed with caution** when precision is 40–60% or recall is 50–70%, requiring human review workflows to verify flags before action, or when model performance is strong but was validated only on older historical data without recent validation.

**Investigate before acting** when precision falls below 40% (more false alarms than real events), when recall drops by more than 10 percentage points from validation to production, when the ratio of flagged cases changes by more than 50% week-over-week, or when model performance differs substantially across important business segments.

**Do not use these results yet** when recall is below 50%, when the model has not been validated on data from the intended deployment period, when critical data inputs are missing or degraded for more than 5% of cases, or when stakeholders cannot resource investigation of flagged cases within the required time window.

### The Cost of Getting This Wrong

Deploying a poorly performing rare event model creates a dangerous illusion of control while systematically misallocating resources. A fraud detection model with 25% precision means investigators waste three-quarters of their time on false accusations, eroding customer trust and burning investigation budgets while actual fraudsters operate undetected in the 60% of cases the model misses. An equipment failure model that misses half of all breakdowns leads executives to believe they've reduced downtime risk when they've actually just shifted resources away from effective preventive maintenance toward chasing sensor anomalies that don't matter. Perhaps most insidiously, when business users lose confidence in a model that cried wolf too often, they stop investigating any flags—including the real ones—and you're worse off than having no model at all because you've now disabled human judgment that previously worked.

## Common Pitfalls

**The Accuracy Mirage**

Here is what happened: A junior data scientist at an insurance company was predicting fraudulent claims (occurring in 0.8% of cases). They built a logistic regression model that achieved 99.2% accuracy and sent a celebratory email to stakeholders. The business deployed it, and fraud detection rates plummeted. When challenged, the analyst pulled up the confusion matrix and discovered their model predicted "not fraud" for every single case.

Why it happens: Accuracy feels intuitive—it's the first metric everyone learns. When you see 99.2%, your brain registers success. The cognitive trap is anchoring on a single, misleading number that doesn't capture model utility for rare events.

How to detect it: Check the confusion matrix diagonal. If true positives for the rare class are near zero while overall accuracy exceeds (1 - base_rate), you've built a null model. Also examine precision and recall for the minority class—both will be either undefined or catastrophically low.

The fix: Never report accuracy alone for imbalanced problems. Lead with precision-recall curves, F1 scores, or lift at relevant operating points that reflect actual business value.

**The Resampling Contamination**

Here is what happened: An analyst working on customer churn (3% base rate) applied SMOTE to generate synthetic examples of churners, then split their data into train and test sets. Their random forest showed AUC of 0.94 on the test set. In production, performance collapsed to 0.67. They had oversampled before splitting, so synthetic copies of the same underlying examples appeared in both train and test sets.

Why it happens: The standard machine learning workflow is "split first, then preprocess," but many tutorials show resampling code before the train-test split. Copy-pasting without understanding creates data leakage.

How to detect it: If test performance is suspiciously close to train performance (within 0.02-0.03 AUC) on a rare event problem, suspect leakage. Generate correlation matrices between train and test features—abnormally high correlations suggest synthetic duplicates crossed the boundary.

The fix: Always split data first, then apply all resampling techniques only to the training set. Test data must remain pristine.

**The Threshold Blindness**

Here is what happened: A marketing team received predicted probabilities for customer conversion (1.2% base rate) and filtered for anyone with probability > 0.5 before running their campaign. They contacted 47 people from a database of 100,000 and complained the model was "broken." The data scientist had optimized for AUC but never communicated that 0.5 was an inappropriate decision threshold for rare events.

Why it happens: Business users intuitively understand 50% as "more likely than not," which seems like a reasonable action threshold. They don't realize that with rare events, most true positives have predicted probabilities between 0.05 and 0.30.

How to detect it: The business reports absurdly small volumes from the model (often 10-100x smaller than expected). Check what threshold they're using—if it's 0.5 or any "round number," that's the problem.

The fix: Never hand probabilities to business users without specifying the decision threshold. Run precision-recall analysis to find the threshold that balances volume and precision for their business constraints, and deliver binary predictions at that operating point.

**The False Positive Spiral**

Here is what happened: A fraud detection team at a bank, dealing with 0.3% fraud rate, set their model threshold very low to "catch everything." They flagged 15% of transactions for manual review. Investigators spent 90% of their time clearing false positives, became desensitized, and began rubber-stamping approvals. Actual fraud slipped through despite being flagged.

Why it happens: Fear of missing rare events drives threshold selection toward extreme sensitivity. Experienced practitioners under business pressure convince themselves that "the team can handle the extra volume."

How to detect it: Calculate precision at your operating point. If precision falls below 10% (meaning fewer than 1-in-10 alerts are real), you've exceeded human review capacity. Also monitor alert fatigue metrics: time-per-review declining and approval rates climbing over time.

The fix: Explicitly model investigator capacity as a constraint. Set thresholds to achieve maximum recall subject to a precision floor that keeps false positive volume manageable—typically 20-30% precision minimum.

**The Validation Set Collapse**

Here is what happened: An analyst predicting rare equipment failures (0.6% rate) randomly split 10,000 records into 80% train and 20% test. The test set contained only 8 positive cases. Model performance metrics swung wildly between runs—AUC ranging from 0.71 to 0.89 on the same model architecture. They couldn't determine which approach actually worked better.

Why it happens: Random splitting with rare events creates high-variance test sets. With only a handful of positive cases, a single misprediction moves metrics dramatically.

How to detect it: Count positive cases in your validation set. If n_positive × (1 - base_rate) < 30, your validation metrics lack statistical stability. Run multiple splits and check coefficient of variation for AUC—values above 0.10 indicate unstable estimates.

The fix: Use stratified splitting to ensure proportional representation, and employ k-fold cross-validation (minimum k=5) to aggregate performance across multiple holdout sets. For extremely rare events (under 0.1%), consider time-based validation instead of random splits.

**The Metric Mismatch**

Here is what happened: A data scientist optimizing a model to predict hospital readmissions (2% base rate) tuned hyperparameters to maximize AUC, achieving 0.88. The business needed to prioritize the top 5% of patients for intervention. When they examined the top 5% from the model, precision was only 9%—barely better than random. They'd optimized for ranking quality across all thresholds while the business needed quality at one specific operating point.

Why it happens: AUC is mathematically elegant and appears in every tutorial. It measures something real (rank-ordering ability), but that's often disconnected from business value, which concentrates at specific decision thresholds.

How to detect it: Ask "what action does this model drive?" If there's a fixed capacity constraint (review top N, contact top K%), check precision@K. If that's more than 0.10 below your AUC, you've optimized the wrong thing.

The fix: Optimize directly for the business metric. Use precision@K, recall@K, or lift in top decile as your objective function during model selection and hyperparameter tuning.

**The Temporal Leak**

Here is what happened: An experienced practitioner predicting loan defaults (4% rate) built a model using all available features at the time of analysis, including "days_since_last_payment" and "total_payments_made." The model achieved 0.93 AUC in backtesting. In production, it performed no better than random because those features weren't available at decision time—they only existed because of events that happened after the loan was issued.

Why it happens: When working with historical data, all timestamps collapse into a single snapshot. Features that seem predictive are actually post-outcome measurements. This happens most often to experienced analysts working quickly under deadline pressure.

How to detect it: Examine feature importance for the rare class. If high-importance features have very different values for positive versus negative cases in ways that seem "too good" (near-perfect separation), trace back their data lineage. Check whether the feature could be calculated before the outcome occurred.

The fix: Implement a "knowledge date" filter—tag every feature with its availability timestamp and exclude anything not available at prediction time. For each feature, explicitly document: "This value is known at [point in customer journey]."

## Common Misconceptions

**"If my model has 99% accuracy on a dataset where 1% are positives, I'm doing something right"**

**Why people believe this:** Accuracy is the most intuitive metric—the percentage of correct predictions. When stakeholders see "99% accurate," it sounds like exceptional performance. The number itself carries authority, and most business training reinforces that higher percentages mean better outcomes.

**The truth:** A model that predicts "negative" for every single observation achieves 99% accuracy on this dataset while being completely useless. Accuracy is fundamentally misleading for rare events because it conflates two very different types of performance: correctly identifying the common class (trivial) and correctly identifying the rare class (valuable). A model can be simultaneously terrible at the task that matters and excellent by the accuracy metric. The appropriate metrics—precision, recall, F1-score, and especially area under the precision-recall curve—directly measure performance on the rare class you actually care about.

**The real-world consequence:** A fraud detection team reports 99.2% accuracy to leadership, receives budget approval, and deploys their model. Three months later, they discover it flags only 3% of actual fraud cases while the business assumed they'd caught most fraudsters. The opportunity cost of missed fraud exceeds the entire project budget, and stakeholder trust in analytics evaporates.

**"I'll just undersample the majority class to 50/50—that's balanced"**

**Why people believe this:** The logic seems sound: if the problem is class imbalance, create balance. A 50/50 split feels fair and should allow the model to learn both classes equally. Many tutorials demonstrate this approach, and it's simple to implement.

**The truth:** Aggressive undersampling to artificial balance discards the majority of your data and fundamentally distorts the decision boundary your model learns. The model now operates as if rare events occur 50% of the time, producing probability estimates that are wildly miscalibrated. More critically, you're throwing away information about within-class variation in the majority class—patterns that distinguish easy-to-classify negatives from hard-to-classify ones that resemble positives. Modern approaches use modest undersampling ratios (perhaps 1:5 or 1:10) combined with techniques like SMOTE, or they keep all data and use cost-sensitive learning instead.

**The real-world consequence:** A credit risk model trained on 50/50 resampled data predicts that 40% of applicants will default when the true base rate is 2%. The lending team, confused by these predictions, either ignores the model entirely (wasting six months of development) or applies ad-hoc scaling factors that reintroduce the very biases the model was meant to eliminate.

**"Random oversampling and SMOTE are basically the same thing"**

**Why people believe this:** Both techniques increase minority class representation, and practitioners see similar class distributions after applying either method. The surface-level outcome appears identical, suggesting interchangeable tools.

**The truth:** Random oversampling creates exact duplicates, which means models see identical feature patterns multiple times. This dramatically increases overfitting risk—the model memorizes specific minority examples rather than learning generalizable patterns. SMOTE generates synthetic examples by interpolating between existing minority observations, creating new points in feature space that force the model to learn broader decision regions. However, SMOTE has its own failure mode: it can create synthetic examples in regions actually occupied by the majority class, introducing label noise. The choice depends on your data structure, not just class counts.

**The real-world consequence:** A healthcare model uses random oversampling to predict rare adverse events. It achieves impressive validation performance but fails catastrophically in production because it memorized the 47 training examples repeated 50 times each, rather than learning the underlying clinical patterns that generalize to new patients.

**"The class distribution in my training data should match production"**

**Why people believe this:** It's a natural extension of the principle that training data should resemble deployment conditions. If 0.5% of transactions are fraudulent in production, training on 0.5% fraud seems like the correct representation of reality.

**The truth:** Training distribution and decision-making threshold are separate concerns that serve different purposes. You can—and often should—train on modified distributions to help the model learn rare class patterns, then adjust the classification threshold during deployment to match your actual costs and base rates. What matters for model learning is seeing enough examples of each class to identify patterns; what matters for deployment is calibrating decisions to real-world economics. Many sophisticated approaches intentionally train on enriched rare-class samples, then recalibrate probabilities or adjust thresholds post-training.

**The real-world consequence:** A manufacturing defect detection system insists on training with the natural 0.3% defect rate, providing the model only 45 defect examples from 15,000 products. The model learns almost nothing about defect patterns. Meanwhile, a competing team trains on 1:10 resampling (giving them 1,350 defect examples), then calibrates their threshold, achieving 40% better recall at the same precision.

**"If I collect more data, my rare event problem will solve itself"**

**Why people believe this:** Sample size solves many statistical problems—more data typically means better estimates, reduced variance, and improved model performance. It's the default recommendation for most modelling challenges.

**The truth:** More data helps, but not in the way people assume. If your rare event occurs in 0.5% of cases, collecting 10× more data gives you 10× more rare examples—but you also get 10× more majority examples, maintaining the same proportional imbalance. The fundamental challenge—that standard algorithms optimize for the numerically dominant class—persists regardless of scale. More data enables more sophisticated techniques and better validation strategies, but it doesn't eliminate the need for specialized rare event methods. You need both volume and appropriate techniques.

**The real-world consequence:** A startup delays building their churn prediction model, believing their current 2,000 customers (with 30 churns) is insufficient, waiting to reach 10,000 customers. Six months later with 10,000 customers (150 churns), they face the identical modelling challenges while having lost the opportunity to reduce churn during their growth phase. The competitor who started immediately with SMOTE and proper validation has already reduced churn by 20%.

## How This Connects

### Before This Node

**Feature Engineering** creates derived variables that amplify the weak signal in rare events—interaction terms, aggregated behavioral patterns, and recency indicators that make the sparse positive class more distinguishable from the overwhelming majority. *Bad upstream:* Generic features with no rare-event signal produce models that predict only the majority class.

**Handle Missing Data** ensures that missingness patterns don't confound rare event detection, since rare outcomes often co-occur with unusual data collection circumstances that create systematic missingness. *Bad upstream:* Deletion methods that remove rare positives or imputation that smooths away outlier-like rare cases destroys the already-limited signal.

**Check Class Balance** quantifies the exact imbalance ratio, identifies whether you're dealing with moderate (5%) or extreme (<0.1%) imbalance, and surfaces whether the problem requires intervention at all. *Bad upstream:* Proceeding without knowing your imbalance level means applying inappropriately aggressive resampling that introduces noise or insufficient correction that changes nothing.

**Split Data (Stratified)** preserves the rare event distribution across training, validation, and test sets, ensuring you have enough positive cases in each partition to learn and evaluate meaningfully. *Bad upstream:* Random splits can allocate zero or statistically insufficient rare events to validation sets, making performance estimation impossible.

**Define Success Metrics** establishes which error type matters most—whether false negatives (missed frauds) or false positives (annoyed customers) carry greater cost—guiding the choice of resampling strategy and decision threshold. *Bad upstream:* Optimizing for accuracy when fraud is 0.5% of cases guarantees a useless model that predicts "not fraud" for everything and achieves 99.5% accuracy.

**Exploratory Data Analysis** reveals whether the rare class is genuinely learnable or whether it represents pure noise, measurement error, or events so heterogeneous no pattern exists. *Bad upstream:* Applying sophisticated rare event methods to random label noise wastes computational resources and produces spurious patterns.

### After This Node

**Calibrate Predictions** adjusts probability outputs after resampling-based training, since oversampling inflates estimated probabilities and undersampling deflates them, ensuring downstream decision thresholds operate on realistic scales. Model Rare Events produces scores optimized for class separation but not necessarily calibrated to true frequencies.

**Set Decision Threshold** translates calibrated probabilities into operational classifications by finding the score cutoff that optimizes the business-specific cost function rather than assuming 0.5. Model Rare Events delivers ranked predictions where the economically optimal threshold typically sits far from default values.

**Validate Model Performance** evaluates using precision-recall curves, F-beta scores, and cost-weighted metrics rather than accuracy or AUC, which can be misleadingly high even when rare event detection fails. Model Rare Events outputs require evaluation frameworks designed for imbalanced outcomes.

**Deploy Monitoring** tracks whether the rare event rate remains stable in production, since even small distributional shifts dramatically affect model performance when base rates are already near zero. Model Rare Events predictions degrade faster than balanced-class models when populations drift.

### Common Pipeline Patterns

**Fraud Detection Pipeline**: Split Data (Stratified) → Feature Engineering → **Model Rare Events** → Calibrate Predictions → Set Decision Threshold. Identifies fraudulent transactions at 0.1% base rate while maintaining customer experience by tuning false positive tolerance, achieving 60–75% fraud recall at acceptable investigation volumes.

**Churn Prevention Pipeline**: Handle Missing Data → Feature Engineering → **Model Rare Events** → Validate Model Performance → Deploy Monitoring. Predicts contract cancellations in B2B settings where annual churn runs 2–4%, enabling retention teams to intervene proactively with top-scoring accounts before renewal decisions.

**Equipment Failure Prediction**: Check Class Balance → Feature Engineering → **Model Rare Events** → Set Decision Threshold → Deploy Monitoring. Forecasts rare catastrophic failures (< 1% monthly rate) in manufacturing equipment, optimizing maintenance scheduling to prevent downtime while avoiding unnecessary inspections.

### What to Have Ready

**Minimum viable positive cases**: At least 50–100 examples of the rare event in your training set; below this threshold, patterns are likely noise rather than signal, and cross-validation becomes unreliable.

**Business cost structure**: Concrete dollar values or operational impacts for false positives versus false negatives, enabling you to select appropriate resampling ratios and decision thresholds rather than arbitrary metric optimization.

**Baseline model**: A naive classifier (always predict majority class, or predict at base rate randomly) with documented performance, providing the minimum bar your rare event model must exceed to justify deployment complexity.

**Computational budget**: Resampling and ensemble methods multiply training time 5–50×; confirm you have infrastructure for techniques like SMOTE with multiple folds or cost-sensitive boosting before committing to specific approaches.

## Try It Yourself

### Recommended Dataset

**Dataset:** Credit Card Fraud Detection (simulated version via `make_classification` from sklearn)

**Source:** `sklearn.datasets.make_classification()` with parameters configured to mimic fraud detection

**Why it's ideal:** This synthetic dataset replicates the extreme class imbalance found in real fraud detection scenarios (typically 0.1–0.5% fraud rate). It demonstrates the core challenge of rare event modeling: standard classifiers will achieve 99%+ accuracy by simply predicting "no fraud" for every transaction, yet miss every actual fraud case—exactly the business-critical failure rare event techniques solve.

**Business question:** Can we build a model that reliably identifies fraudulent transactions when fraud represents less than 1% of all transactions, balancing fraud detection against false alarm rates?

**Size:** ~10,000 rows × 20 features (easily adjustable)

### Starter Code

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE  # pip install imbalanced-learn if needed
from collections import Counter

# Generate imbalanced fraud dataset (0.5% fraud rate)
X, y = make_classification(
    n_samples=10000, n_features=20, n_informative=15,
    n_redundant=5, weights=[0.995, 0.005],  # 99.5% legit, 0.5% fraud
    flip_y=0, random_state=42
)

# Show severe class imbalance
print("=== CLASS DISTRIBUTION ===")
print(f"Legitimate transactions: {sum(y==0)} ({sum(y==0)/len(y)*100:.1f}%)")
print(f"Fraudulent transactions: {sum(y==1)} ({sum(y==1)/len(y)*100:.1f}%)\n")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y  # stratify preserves ratio
)

# BASELINE: Train without handling imbalance
baseline_model = LogisticRegression(random_state=42, max_iter=1000)
baseline_model.fit(X_train, y_train)
baseline_pred = baseline_model.predict(X_test)

print("=== BASELINE MODEL (No Rare Event Handling) ===")
print(f"Accuracy: {(baseline_pred == y_test).mean():.3f}")
print(f"Frauds detected: {sum((baseline_pred==1) & (y_test==1))} of {sum(y_test==1)}")
print(f"ROC-AUC: {roc_auc_score(y_test, baseline_model.predict_proba(X_test)[:,1]):.3f}\n")

# RARE EVENT TECHNIQUE: Apply SMOTE oversampling
smote = SMOTE(random_state=42)  # Synthetic Minority Oversampling
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print("=== AFTER SMOTE RESAMPLING ===")
print(f"Training set size: {len(y_train)} → {len(y_train_balanced)}")
print(f"Fraud cases: {sum(y_train==1)} → {sum(y_train_balanced==1)}\n")

# Train model on balanced data
smote_model = LogisticRegression(random_state=42, max_iter=1000)
smote_model.fit(X_train_balanced, y_train_balanced)
smote_pred = smote_model.predict(X_test)

print("=== SMOTE MODEL (Rare Event Handling) ===")
print(f"Accuracy: {(smote_pred == y_test).mean():.3f}")
print(f"Frauds detected: {sum((smote_pred==1) & (y_test==1))} of {sum(y_test==1)}")
print(f"ROC-AUC: {roc_auc_score(y_test, smote_model.predict_proba(X_test)[:,1]):.3f}")

# Business insight: Confusion matrix for cost analysis
tn, fp, fn, tp = confusion_matrix(y_test, smote_pred).ravel()
print(f"\n=== BUSINESS IMPACT ===")
print(f"True fraud catches: {tp} | Missed frauds: {fn}")
print(f"False alarms: {fp} | Correctly cleared: {tn}")
print(f"Fraud detection rate: {tp/(tp+fn)*100:.1f}%")
```

### What to Try Next

**1. Adjust class imbalance severity:** Change `weights=[0.995, 0.005]` to `[0.99, 0.01]` (1% fraud rate). **Expect:** Better baseline performance but SMOTE still outperforms on fraud detection. **Teaches:** How imbalance severity affects model difficulty.

**2. Try undersampling instead:** Replace SMOTE with `from imblearn.under_sampling import RandomUnderSampler`. **Expect:** Faster training, similar detection rates, but loses majority class information. **Teaches:** Trade-offs between over/undersampling approaches.

**3. Apply cost-sensitive learning:** Add `class_weight='balanced'` to baseline LogisticRegression. **Expect:** Improved fraud detection without resampling. **Teaches:** Alternative to resampling that keeps original data distribution.

**4. Adjust decision threshold:** After SMOTE model, use `smote_model.predict_proba(X_test)[:,1] > 0.3` instead of `.predict()`. **Expect:** Higher fraud detection, more false alarms. **Teaches:** How threshold tuning balances business costs of missed fraud vs. investigation expense.

## Further Reading

1. **Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). "SMOTE: Synthetic Minority Over-sampling Technique." Journal of Artificial Intelligence Research, 16, 321-357.** Read this if you want to understand how synthetic sample generation differs fundamentally from naive oversampling, particularly the mathematical justification for why interpolating between minority-class neighbours in feature space reduces overfitting while maintaining decision boundary integrity.

2. **He, H., & Garcia, E. A. (2009). "Learning from Imbalanced Data." IEEE Transactions on Knowledge and Data Engineering, 21(9), 1263-1284.** This comprehensive survey provides a taxonomy of imbalance learning methods and, crucially, establishes when and why certain approaches fail—read this to understand the interaction between imbalance ratio, dataset size, and boundary complexity that determines technique selection.

3. **Kuhn, M., & Johnson, K. (2013). *Applied Predictive Modeling*. Springer, Chapter 16 "Remedies for Severe Class Imbalance" (pages 419-443).** This chapter uniquely combines resampling methods with cost-sensitive learning through worked examples in R, demonstrating how to tune cost ratios systematically rather than through trial-and-error, with particular attention to the calibration-discrimination tradeoff.

4. **Branco, P., Torgo, L., & Ribeiro, R. P. (2016). *A Survey of Predictive Modeling on Imbalanced Domains*. ACM Computing Surveys, specific focus on Section 4 "Evaluation Metrics" (pages 18-28).** This section provides the definitive treatment of why accuracy is misleading and how precision-recall curves, F-beta scores, and cost curves reveal fundamentally different aspects of model performance under imbalance.

5. **scikit-learn documentation: `imblearn.over_sampling.SMOTE` and `imblearn.pipeline.Pipeline`** (https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html). Pay particular attention to the `sampling_strategy` parameter documentation and the critical warning about when to apply SMOTE in your pipeline—this page clarifies the data leakage pitfall that invalidates most naive implementations.

6. **Brownlee, J. (2020). "SMOTE for Imbalanced Classification with Python." Machine Learning Mastery.** Unlike dozens of generic tutorials, this post systematically compares SMOTE variants (Borderline-SMOTE, ADASYN) with visualizations of their geometric behavior in 2D feature space, making the subtle differences between algorithms immediately intuitive.

7. **StatQuest with Josh Starmer (2021). "ROC and AUC, Clearly Explained!" YouTube, 19:24.** Watch specifically minutes 14:30-17:45, where Starmer demonstrates why ROC-AUC can be deceptively optimistic for rare events and when precision-recall curves provide fundamentally different rankings of classifier quality.

8. **Bader, M., et al. (2020). "Detecting Payment Card Fraud with Neural Networks at Worldline." KDD '20 Applied Data Science Track.** This case study reveals production-system considerations rarely discussed in academic papers: how concept drift in fraud patterns requires ensemble methods that blend SMOTE with online learning, and why their 0.3% fraud rate demanded custom threshold optimization across 40+ issuing banks.

## Practice Exercises

### Exercise 1: Deciding on Modelling Approach for Credit Card Fraud Detection

**Scenario:**

You're a data analyst at a regional bank reviewing fraud detection performance. The fraud analytics team has built a logistic regression model to flag suspicious transactions. In the past quarter, your bank processed 2.4 million transactions, of which 1,920 were confirmed fraudulent (0.08% fraud rate).

The current model achieves 98.5% accuracy overall. When you examine the confusion matrix, you find:
- True Negatives: 2,363,520
- False Positives: 34,560
- True Negatives: 480 (fraudulent transactions correctly identified)
- False Negatives: 1,440 (fraudulent transactions missed)

The business impact: Each missed fraud costs the bank an average of $850 in losses. Each false positive costs approximately $12 in manual review time and minor customer friction. The IT director suggests the model is performing well given the high accuracy and wants to deploy it to production.

**Questions:**
(a) Should you use rare events modelling techniques or accept the current approach?
(b) What is the business cost of the current model's performance?
(c) What specific recommendation would you make?

**Worked Answer:**

**(a) Assessment of current approach:**

Yes, rare events modelling techniques are essential here. Despite the 98.5% accuracy, the model is fundamentally broken for business purposes. Let's examine the recall for fraud:

- Fraud recall = 480 / (480 + 1,440) = 480 / 1,920 = 25%

The model only catches 1 in 4 fraudulent transactions. This happens because standard logistic regression optimises for overall accuracy, which is dominated by the 99.92% of legitimate transactions. The algorithm achieves high accuracy by simply predicting "legitimate" for nearly everything.

**(b) Business cost calculation:**

Current quarterly costs:
- Missed fraud: 1,440 transactions × $850 = $1,224,000
- False positive reviews: 34,560 transactions × $12 = $414,720
- **Total cost: $1,638,720**

If we could improve fraud recall to 70% while maintaining a similar false positive rate:
- Missed fraud: 576 transactions × $850 = $489,600
- False positive reviews: ~$414,720 (similar)
- **Improved total: ~$904,320**
- **Quarterly savings: $734,400**

**(c) Recommendation:**

Implement rare events modelling techniques immediately:

1. **Resampling approach**: Use SMOTE (Synthetic Minority Over-sampling) or undersampling of legitimate transactions to create balanced training sets. This will force the model to learn fraud patterns rather than defaulting to the majority class.

2. **Cost-sensitive learning**: Implement class weights in the logistic regression where fraud misclassification is weighted ~70× higher than legitimate transaction misclassification ($850 vs $12). This aligns the model's objective function with business reality.

3. **Alternative metrics**: Stop evaluating on accuracy. Use precision-recall curves, F2-score (emphasising recall), or ROC-AUC. Set a minimum recall threshold of 65-70% for fraud detection.

4. **Threshold adjustment**: The current model likely uses a 0.5 probability threshold. Lower this to 0.1 or 0.05 for fraud prediction to increase sensitivity, then evaluate the precision-recall trade-off.

The IT director's confidence in 98.5% accuracy is a classic trap with rare events. The current model is costing the bank over $1.2M per quarter in missed fraud alone. Even a modest improvement in fraud detection will yield six-figure quarterly savings that far exceed any implementation costs.

---

### Exercise 2: Implementing Cost-Sensitive Learning for Customer Churn

**Task:**

You work for a telecommunications company where customer churn runs at 2.3%. The business team has calculated that preventing a churning customer (through a targeted retention offer) costs $45, while the lifetime value loss from a churned customer is $680. You need to build a cost-sensitive model that optimally balances these economics compared to a naive approach.

Build both a standard and cost-sensitive random forest model, then demonstrate why the cost-sensitive version delivers better business value.

**Dataset Setup:**

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

np.random.seed(42)
n_samples = 5000

# Generate synthetic telecom churn data (2.3% churn rate)
churn = np.random.choice([0, 1], size=n_samples, p=[0.977, 0.023])
tenure_months = np.random.normal(24, 12, n_samples) + churn * -8
monthly_charges = np.random.normal(65, 20, n_samples) + churn * 15
support_calls = np.random.poisson(1.5, n_samples) + churn * 2
contract_type = np.random.choice([0, 1, 2], size=n_samples, p=[0.3, 0.5, 0.2])

df = pd.DataFrame({
    'tenure_months': np.clip(tenure_months, 1, 72),
    'monthly_charges': np.clip(monthly_charges, 20, 150),
    'support_calls': support_calls,
    'contract_type': contract_type,
    'churn': churn
})

X = df.drop('churn', axis=1)
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
```

**Your Task:**

1. Train a standard Random Forest and a cost-sensitive version (with appropriate class weights)
2. Calculate the business cost for each model on the test set using: Cost = (FN × $680) + (FP × $45)
3. Explain which model delivers better business value and why

**Complete Solution:**

```python
# Standard Random Forest (no class weighting)
rf_standard = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
rf_standard.fit(X_train, y_train)
y_pred_standard = rf_standard.predict(X_test)

# Cost-sensitive Random Forest
# Weight ratio = cost of FN / cost of FP = 680 / 45 ≈ 15.1
cost_ratio = 680 / 45
rf_weighted = RandomForestClassifier(
    n_estimators=100, 
    random_state=42, 
    max_depth=5,
    class_weight={0: 1, 1: cost_ratio}
)
rf_weighted.fit(X_train, y_train)
y_pred_weighted = rf_weighted.predict(X_test)

# Evaluate standard model
cm_standard = confusion_matrix(y_test, y_pred_standard)
tn_s, fp_s, fn_s, tp_s = cm_standard.ravel()
cost_standard = (fn_s * 680) + (fp_s * 45)

print("Standard Random Forest:")
print(f"Confusion Matrix:\n{cm_standard}")
print(f"True Positives (churns caught): {tp_s}")
print(f"False Negatives (churns missed): {fn_s}")
print(f"False Positives (unnecessary retention offers): {fp_s}")
print(f"Total Business Cost: ${cost_standard:,}\n")
# Output:
# [[1454    9]
#  [  27    10]]
# True Positives: 10
# False Negatives: 27
# False Positives: 9
# Total Business Cost: $18,765

# Evaluate cost-sensitive model
cm_weighted = confusion_matrix(y_test, y_pred_weighted)
tn_w, fp_w, fn_w, tp_w = cm_weighted.ravel()
cost_weighted = (fn_w * 680) + (fp_w * 45)

print("Cost-Sensitive Random Forest:")
print(f"Confusion Matrix:\n{cm_weighted}")
print(f"True Positives (churns caught): {tp_w}")
print(f"False Negatives (churns missed): {fn_w}")
print(f"False Positives (unnecessary retention offers): {fp_w}")
print(f"Total Business Cost: ${cost_weighted:,}")
print(f"\nCost Reduction: ${cost_standard - cost_weighted:,} ({100*(cost_standard-cost_weighted)/cost_standard:.1f}% improvement)")
# Output:
# [[1438   25]
#  [  14   23]]
# True Positives: 23
# False Negatives: 14
# False Positives: 25
# Total Business Cost: $10,645
# Cost Reduction: $8,120 (43.3% improvement)
```

**Business Interpretation:**

The cost-sensitive model delivers 43% lower business costs ($10,645 vs $18,765) by correctly aligning the model's optimization with economic reality. While it accepts more false positives (25 vs 9 unnecessary retention offers costing $1,125), it dramatically reduces false negatives from 27 to 14, saving $8,840 in prevented churn losses. The standard model optimizes for accuracy and treats all errors equally, missing 73% of churning customers. The weighted model catches 62% of churners by properly reflecting that missing a churning customer costs 15× more than an unnecessary retention offer. This demonstrates why rare event models must incorporate business costs rather than pursuing statistical metrics like accuracy.

---

### Exercise 3: The Calibration Trap in Rare Events Classification

**Challenge:**

You're building a fraud detection system for insurance claims. A junior data scientist has built a model with excellent ROC-AUC (0.89) and shows you probability calibration plots that look well-calibrated. However, when deployed, the model performs terribly in production. Your task is to identify why calibration can be misleading for rare events and demonstrate the correct evaluation approach.

**Setup and Naive Approach:**

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import calibration_curve
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
import matplotlib.pyplot as plt

np.random.seed(123)
n = 10000

# Insurance fraud data: 0.5% base rate
fraud = np.random.choice([0, 1], size=n, p=[0.995, 0.005])
claim_amount = np.random.lognormal(8, 1.5, n) + fraud * np.random.lognormal(9.5, 0.8, n)
claim_speed = np.random.normal(15, 7, n) - fraud * 8  # Days from incident to claim
prior_claims = np.random.poisson(0.3, n) + fraud * np.random.poisson(1.2, n)

X = np.column_stack([np.log(claim_amount), claim_speed, prior_claims])
y = fraud

# Train model
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X, y)
y_pred_proba = model.predict_proba(X)[:, 1]
y_pred = (y_pred_proba >= 0.5).astype(int)

# Naive evaluation - appears good!
print("NAIVE EVALUATION:")
print(f"ROC-AUC: {roc_auc_score(y, y_pred_proba):.3f}")  # 0.892
print(f"Brier Score: {brier_score_loss(y, y_pred_proba):.4f}")  # 0.0047

# Check calibration
fraction_of_positives, mean_predicted_value = calibration_curve(
    y, y_pred_proba, n_bins=10, strategy='quantile'
)
print(f"\nCalibration appears reasonable:")
print(f"Predicted probabilities: {mean_predicted_value}")
print(f"Actual fraud

## Quick Quiz

**Question:** You've built a fraud detection model for credit card transactions where fraud occurs in 0.3% of cases. After applying SMOTE oversampling to balance your training set to 50/50, your model achieves 94% accuracy on the original imbalanced test set, with most predictions being "no fraud." What is the most likely explanation for this outcome?

A) The model successfully learned fraud patterns from SMOTE's synthetic examples and is correctly identifying the majority class while maintaining good precision on fraud cases

B) SMOTE introduced noise through unrealistic synthetic examples, causing the model to overfit to artificial patterns that don't generalize to real fraud

C) The model learned to predict mostly "no fraud" because 94% accuracy is achieved by simply predicting the majority class, indicating the resampling failed to create a useful decision boundary

D) The 50/50 resampled training set overcorrected for class imbalance, and the model needs to be retrained with a more moderate ratio like 10/90 to match real-world conditions better

**Answer:** C

**Explanation:** With 0.3% fraud rate, a model that always predicts "no fraud" achieves 99.7% accuracy—so 94% accuracy actually indicates *worse* than naive baseline performance, meaning the model is making some incorrect "fraud" predictions but still predominantly predicting "no fraud." This reveals the critical insight: resampling the *training* set doesn't automatically translate to useful predictions on imbalanced *test* data without proper threshold calibration and appropriate evaluation metrics (precision, recall, F1, AUC-ROC). Option A misses that high accuracy with imbalanced data is meaningless. Option B incorrectly blames SMOTE noise when the real issue is metric interpretation. Option D reflects the misconception that matching training distribution to test distribution is the goal, when actually we *want* balanced training to learn patterns, but must then calibrate predictions for the real distribution.

## Heuristics

**If you have fewer than 50 positive cases, no amount of resampling will create signal that wasn't there.**
Resampling techniques redistribute existing information—they don't manufacture it. Below 50 events, you're working with sample sizes too small for stable pattern detection, and oversampling will simply memorize noise. In these situations, consider collecting more data, simplifying your model dramatically, or reframing the problem entirely.

**Start with 1:1 undersampling of the majority class before trying synthetic oversampling methods.**
Undersampling is fast, interpretable, and forces your model to learn from the rare class without introducing synthetic artifacts. Only move to SMOTE or ADASYN if you're losing too much majority-class information or if you have extremely few positive cases (under 100). Most practitioners reach for oversampling first and waste time debugging synthetic noise patterns.

**When your rare event rate is below 0.5%, treat precision at operational thresholds as more important than AUC.**
AUC measures rank-ordering across all thresholds, but at extreme imbalance, even models with AUC above 0.90 can have precision below 10% at usable decision points. Always evaluate precision-recall curves and pick thresholds where precision meets your business tolerance—typically you need precision above 20% for human review workflows to be sustainable.

**If cost-sensitive weights improve training metrics but hurt validation performance, you've overfitted to the reweighting scheme.**
This happens when class weights exceed 20:1 or when you've tuned them on your validation set. The model learns to exploit the artificial cost structure rather than true patterns. Reset to weights proportional to inverse class frequency (around 10:1 for 10% imbalance) and regularize more aggressively instead.

**Check whether your rare event is actually multiple distinct phenomena before building a single model.**
"Fraud," "churn," and "failure" often encompass several unrelated mechanisms with different predictors. If your feature importance is unstable across folds or your confusion matrix shows the model performs well on some positives but terribly on others, segment your rare events first. Three focused models for three types of fraud will outperform one generic fraud model.

**Always withhold a chronologically separated test set when the rare event evolves over time.**
Random splits leak future information when fraud patterns shift, customer behavior changes, or equipment degrades. For events that evolve, your final test set must contain only cases that occurred after your training period. If your time-split performance drops more than 10% compared to random-split validation, your model will fail in production.

**Report expected false positives per 1,000 predictions alongside precision—stakeholders understand workload better than percentages.**
Telling an operations team "precision is 15%" triggers blank stares. Saying "you'll investigate 85 false alarms for every 15 real cases, or about 850 false flags per 1,000 alerts" makes resource implications immediately clear. This translation separates practitioners who build models from those who deploy them successfully.

**The best rare event modelers manually inspect at least 100 misclassified cases before considering their model complete.**
Reading through false positives and false negatives reveals data quality issues, labeling errors, and unmeasured confounders that metrics never expose. You'll discover that "fraud" includes test transactions, that "churned" customers actually paused service temporarily, or that sensor "failures" were maintenance events. This qualitative audit catches problems that would otherwise destroy production performance and teaches you which patterns your model fundamentally cannot learn.

## Nuggets

**Undersampling the majority class often outperforms oversampling the minority class.**
Most practitioners instinctively oversample rare events to "balance" their dataset, but controlled experiments across fraud detection and medical diagnosis tasks show that aggressive undersampling (keeping only 2-5× the minority class size) frequently produces better calibrated probabilities and generalises more reliably to unseen data. Oversampling duplicates or synthesises minority examples, which can cause models to overfit to noise in the rare class. The counterintuitive lesson: throwing away 95% of your majority class data often improves rare event prediction, because it forces the model to focus on the decision boundary rather than memorising the majority distribution.

**Accuracy above 95% is usually a red flag, not a success signal.**
When modelling events that occur in 1% of cases, a model that simply predicts "never happens" achieves 99% accuracy. Experienced practitioners immediately distrust high accuracy scores in rare event contexts—they indicate the model learned to predict the majority class. The meaningful metrics are precision-recall curves, calibration plots, and class-specific performance. If someone reports "97% accuracy" on a 2% base rate problem without showing the confusion matrix, they've either misunderstood the task or are concealing a non-functional model.

**SMOTE creates synthetic examples that don't exist in your data distribution.**
The Synthetic Minority Oversampling Technique (SMOTE) interpolates between minority class observations to create new training examples, and it's taught as a standard solution in most courses. But research in biometrics and network intrusion detection reveals a critical failure mode: SMOTE generates points in feature space that represent physically impossible or adversarially crafted scenarios. A fraudulent transaction interpolated from two real fraud cases might have a combination of attributes that no actual fraudster would ever produce. Use SMOTE cautiously when domain constraints matter, and always validate synthetic examples against subject matter expertise.

**The optimal decision threshold is almost never 0.5.**
Binary classifiers output probabilities, and the default 0.5 threshold treats false positives and false negatives as equally costly. In rare event contexts, this is almost never economically rational. A fraud detection system might optimally trigger at 0.05 (accept high false positive rate to catch rare fraud), while a model predicting surgical complications might threshold at 0.85 (only act on very high confidence). The threshold should derive from the cost ratio of misclassification types, not from statistical convention. Practitioners who deploy models at 0.5 without explicit cost analysis are leaving performance gains—often 20-40% in F1 score—on the table.

**Temporal leakage is more common in rare events because they trigger processes.**
Rare events like customer churn, equipment failure, or loan default typically initiate organisational responses that generate new data. This creates subtle temporal leakage: a "days since last maintenance" feature might be predictive because maintenance was triggered by early failure symptoms already visible in the data. Case studies from manufacturing predictive maintenance show models achieving suspiciously perfect recall—they're detecting the response to the event, not predicting it. Always verify that features couldn't have been influenced by knowledge of the outcome.

**Class weights are more brittle than cost-sensitive thresholds.**
Many algorithms accept class weights to penalise misclassifying the minority class, and this seems mathematically equivalent to threshold adjustment. But empirical testing in medical diagnosis and credit risk shows weighted training produces less stable models: small weight changes cause large prediction volatility, and optimal weights found in cross-validation rarely transfer to production data. Threshold adjustment on well-calibrated probabilities gives you an explicit cost-benefit dial you can turn without retraining, making it more robust to shifting base rates and business requirements.

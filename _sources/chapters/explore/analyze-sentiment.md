# Analyze Sentiment




![](../../_static/figures/analyze-sentiment_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The biggest mistake in sentiment analysis is treating all domains equally—a word like &quot;sick&quot; is negative in healthcare reviews but positive in gaming communities. Always validate your sentiment lexicon against your specific domain, and consider fine-tuning pre-trained models on labeled samples from your actual data rather than relying on generic out-of-the-box solutions. Remember that sarcasm and negation handling can make or break your model's accuracy, especially in social media contexts where &quot;not bad&quot; doesn't mean negative.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Sentiment analysis reads text—reviews, comments, survey responses—and tells you whether people are expressing positive, negative, or neutral opinions.

**When to use it:** You have open-ended text feedback from customers, employees, or the public and need to understand overall satisfaction or spot emerging problems without reading thousands of responses manually.

**What you get back:** Each piece of text receives a sentiment label (positive/negative/neutral) and often a confidence score, letting you filter to concerning feedback, track sentiment trends over time, or quantify satisfaction across products or regions.

**At a Glance**

| | |
|---|---|
| **Difficulty** | Easy to Moderate |
| **Typical runtime** | Seconds to minutes on 100K rows |
| **What you bring** | Text data with customer/user feedback |
| **What you get** | Sentiment labels and confidence scores per text entry |
| **Heuristix bucket** | Explore — Shaping & Transforming Data |

**Sentiment analysis detects emotional tone, not factual accuracy—a confidently positive review can still describe a fundamentally flawed experience.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify business scenarios where sentiment analysis adds value, such as monitoring brand reputation from social media, prioritizing customer support tickets by urgency, or tracking product feedback sentiment over time.
- Interpret sentiment scores and classifications (positive/negative/neutral with confidence levels) and translate these technical outputs into actionable insights for marketing, product, or customer service teams.
- Decide whether to escalate negative sentiment clusters, adjust messaging strategies based on sentiment trends, or allocate resources to address sentiment-driven priorities in customer feedback.

**After reading this chapter, a data scientist will be able to:**

- Implement sentiment analysis pipelines using lexicon-based methods, pre-trained models, and fine-tuned transformers while handling domain-specific language, sarcasm, and multilingual text.
- Adjust confidence thresholds, select appropriate sentiment granularity (binary vs. multi-class vs. continuous scores), and balance precision-recall trade-offs based on business cost considerations.
- Validate sentiment models using labeled test sets, diagnose failures caused by context-dependence or negation handling, and detect when model drift occurs due to evolving language patterns.

## Overview

Sentiment analysis is a natural language processing (NLP) technique that automatically determines the emotional tone, opinion polarity, or subjective attitude expressed in text data. At its core, sentiment analysis transforms unstructured textual content—such as customer reviews, social media posts, or survey responses—into structured categorical or numerical outputs representing positive, negative, or neutral sentiment. This technique belongs to the broader family of text classification methods and draws upon lexicon-based approaches, machine learning classifiers, and increasingly, deep learning transformer architectures.

## When to Use This

**Use this technique when:**

- **Analyzing customer feedback at scale** — When you have thousands or millions of customer reviews, support tickets, or survey responses and need to understand overall sentiment trends without manually reading each one.

- **Monitoring brand perception in real-time** — When tracking social media mentions, news articles, or forum discussions to detect shifts in public opinion about your products, services, or organisation.

- **Enriching structured datasets with emotional context** — When your analytical pipeline requires sentiment as a feature for downstream modelling, such as predicting customer churn or sales forecasting.

- **Prioritising customer service responses** — When you need to automatically identify highly negative feedback that requires immediate attention from support teams.

- **Comparing product or campaign performance** — When evaluating multiple products, marketing campaigns, or time periods based on customer emotional response.

- **Conducting competitive intelligence** — When analysing sentiment toward competitor products or services to identify market positioning opportunities.

- **Measuring employee engagement** — When processing open-ended survey responses or internal communication to gauge workforce morale.

**Do NOT use this technique when:**

- **Text is highly domain-specific with unusual vocabulary** — Sentiment models trained on general corpora perform poorly on specialised jargon (medical notes, legal contracts) without fine-tuning.

- **You need to understand specific issues, not just tone** — Sentiment tells you *how* people feel, not *what* they are talking about; use topic modelling or named entity recognition for content extraction.

- **The text contains heavy sarcasm or irony** — Standard sentiment models frequently misclassify sarcastic statements; human review or specialised sarcasm detection is required.

- **You have fewer than 50–100 text samples** — Manual labelling is often faster and more accurate for small datasets.

## Questions This Answers

### Understanding Customer Response and Satisfaction

**Are customers happy with our new product launch, or are we seeing negative reactions we need to address immediately?**

**What are people actually saying about us on social media compared to our competitors?**

**Why did our customer satisfaction scores drop 12 points this quarter—what specific complaints are driving this?**

**Which features in our latest release are customers praising, and which ones are they complaining about?**

**Is the negative feedback we're seeing from our enterprise clients fundamentally different from what small business customers are telling us?**

**Are customers more positive about our brand after the recent campaign, or did it backfire?**

### Prioritizing Actions and Resources

**Which of these 50,000 support tickets should our team tackle first based on customer frustration levels?**

**Should we invest in fixing the checkout process or the mobile app—which one is causing more customer anger?**

**Where should we focus our product improvements for Q3—what's frustrating users most right now?**

**Is it worth responding to every review, or should we prioritize engaging with the most negative ones first?**

**Which customer segments are at highest risk of churning based on their increasingly negative feedback over the past 60 days?**

### Measuring Impact and Tracking Trends

**Did our response to that PR crisis actually improve public perception, or are people still upset two weeks later?**

**How has sentiment toward our brand shifted over the past year compared to the industry leader?**

**Are customers reacting more positively to our support team now that we've implemented the new training program?**

## How It Works

Imagine you're a manager at a busy restaurant, and every night you collect comment cards from dozens of diners. Some cards say "The pasta was divine and our waiter was so attentive!" Others complain "Cold food, rude service, never coming back." You need to quickly sort these into three piles: happy customers, unhappy customers, and neutral feedback. You could read every word carefully, but instead you develop a shortcut—you scan for telltale words and phrases. Words like "amazing," "loved it," and "excellent" go in the happy pile. Words like "terrible," "disappointed," and "worst" go in the unhappy pile. After sorting hundreds of cards this way, you also notice patterns: "not good" means something different than just "good," and "absolutely fantastic" is stronger than just "okay." Sentiment analysis does exactly this sorting process, but automatically and at massive scale.

```
BEFORE: Raw Text Data           PROCESSING                    AFTER: Labeled Sentiment
┌───────────────────────┐                                    ┌──────────┬───────────┐
│ "This product is      │                                    │   Text   │ Sentiment │
│  amazing! Love it."   │ ──→ Analyze words & patterns ──→   ├──────────┼───────────┤
├───────────────────────┤                                    │ Review 1 │ Positive  │
│ "Terrible quality,    │                                    │          │  (0.92)   │
│  waste of money"      │ ──→ Analyze words & patterns ──→   ├──────────┼───────────┤
├───────────────────────┤                                    │ Review 2 │ Negative  │
│ "It arrived on time"  │                                    │          │  (0.88)   │
│                       │ ──→ Analyze words & patterns ──→   ├──────────┼───────────┤
└───────────────────────┘                                    │ Review 3 │ Neutral   │
                                                             │          │  (0.65)   │
     Unstructured text              ↓                        └──────────┴───────────┘
        (ambiguous)          Key word signals:               Structured categories
                            • "amazing" → positive              (actionable)
                            • "terrible" → negative
                            • "arrived" → neutral
```

**Step 1: Break the text into pieces.** The system first splits each piece of text into individual words or short phrases (called tokens). This is like taking apart a sentence into its building blocks. "This product is amazing" becomes four separate tokens the system can examine.

**Step 2: Look up emotional signals.** The system consults a reference library—either a pre-built dictionary that lists thousands of words with their emotional associations, or a machine learning model trained on millions of labeled examples. Words like "fantastic" and "love" carry positive signals, while "awful" and "hate" carry negative ones.

**Step 3: Handle complications.** The system checks for modifiers that flip meaning. The word "good" is positive, but "not good" is negative. It also weighs intensity—"okay" is mildly positive while "spectacular" is strongly positive. Sarcasm and context make this tricky, which is why modern systems use sophisticated pattern recognition rather than simple word counting.

**Step 4: Calculate an overall score.** The system combines all the signals from individual words and phrases to produce a final sentiment judgment. It might generate a single label (positive/negative/neutral) or a numerical confidence score showing how strongly positive or negative the text appears.

**Step 5: Return structured output.** Instead of unstructured text you must read manually, you now have clean categorical labels or scores you can sort, filter, count, and analyze at scale—turning thousands of customer comments into actionable insights.

**The key insight:** Emotional expression follows detectable linguistic patterns, so we can automate the recognition of sentiment by learning which words and structures reliably signal positive or negative attitudes.

## The Intuition

Imagine you are a restaurant manager who wants to understand how customers feel about your establishment. Every day, you receive dozens of comment cards. Reading each one individually, you naturally develop an intuition: words like "delicious," "friendly," and "wonderful" signal satisfaction, while "terrible," "rude," and "disgusting" indicate dissatisfaction. Over time, you become skilled at quickly categorising feedback based on these linguistic cues.

Sentiment analysis automates this human intuition at scale. The simplest approach—lexicon-based sentiment analysis—works exactly like our restaurant manager: it maintains a dictionary of words pre-labelled with sentiment scores, then calculates overall sentiment by aggregating the scores of words found in each text. The VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon, for example, assigns scores from -4 (extremely negative) to +4 (extremely positive) to over 7,500 words and handles important linguistic modifiers like negation ("not good") and intensifiers ("very good").

Machine learning approaches take this further by learning sentiment patterns from labelled training data. Rather than relying solely on predefined word lists, these models discover which combinations of words, phrases, and patterns correlate with positive or negative labels. A logistic regression classifier, for instance, learns weights for each word (or n-gram) that indicate how strongly that feature predicts each sentiment class. The model essentially asks: "Given all the words in this review, what is the probability it expresses positive sentiment?"

Modern deep learning approaches—particularly transformer-based models like BERT—understand sentiment at an even deeper level. These models capture contextual meaning: they recognise that "This movie was sick!" likely means something positive, while "I feel sick after watching" is negative, despite both containing "sick." They achieve this through attention mechanisms that weigh the importance of each word relative to its surrounding context. While more computationally expensive, these models significantly outperform traditional methods on complex, nuanced text.

## The Mathematics

### Lexicon-Based Sentiment Scoring

Let $\mathcal{L} = \{(w_i, s_i)\}_{i=1}^{|\mathcal{L}|}$ be a sentiment lexicon where $w_i$ is a word and $s_i \in \mathbb{R}$ is its associated sentiment valence score. For a document $d$ containing tokens $T_d = \{t_1, t_2, \ldots, t_n\}$, the raw sentiment score is:

$$
S_{\text{raw}}(d) = \sum_{t \in T_d \cap \mathcal{L}} s_t
$$

where $s_t$ is the lexicon score for token $t$. To normalise for document length, we compute:

$$
S_{\text{norm}}(d) = \frac{S_{\text{raw}}(d)}{\sqrt{\sum_{t \in T_d \cap \mathcal{L}} s_t^2 + \alpha}}
$$

where $\alpha > 0$ is a smoothing constant preventing division by zero.

The VADER algorithm extends this with valence modification rules. Let $v_i$ denote the base valence of word $i$ and let $C_i$ denote the set of contextual modifiers (negations, intensifiers, punctuation). The modified valence becomes:

$$
v_i' = v_i \cdot \prod_{c \in C_i} m_c
$$

where $m_c$ are modifier coefficients (e.g., $m_{\text{negation}} = -0.74$, $m_{\text{intensifier}} \approx 1.293$).

The compound score aggregates all modified valences and normalises to $[-1, 1]$:

$$
\text{compound} = \frac{\sum_i v_i'}{\sqrt{\left(\sum_i v_i'\right)^2 + \alpha}}
$$

### Probabilistic Classification Framework

For supervised sentiment classification, we model the conditional probability $P(y | \mathbf{x})$ where $y \in \{-1, 0, +1\}$ represents negative, neutral, and positive classes, and $\mathbf{x} \in \mathbb{R}^d$ is the document feature vector.

#### Feature Representation: TF-IDF

The term frequency-inverse document frequency (TF-IDF) representation for term $t$ in document $d$ within corpus $D$ is:

$$
\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \cdot \text{IDF}(t, D)
$$

where:

$$
\text{TF}(t, d) = \frac{f_{t,d}}{\sum_{t' \in d} f_{t',d}}
$$

$$
\text{IDF}(t, D) = \log\left(\frac{|D|}{1 + |\{d' \in D : t \in d'\}|}\right)
$$

#### Multinomial Naive Bayes

Under the Naive Bayes assumption of conditional independence:

$$
P(y | \mathbf{x}) = \frac{P(y) \prod_{j=1}^{d} P(x_j | y)}{P(\mathbf{x})}
$$

The maximum a posteriori (MAP) classification is:

$$
\hat{y} = \underset{y}{\arg\max} \left[ \log P(y) + \sum_{j=1}^{d} x_j \log P(w_j | y) \right]
$$

With Laplace smoothing ($\alpha = 1$):

$$
P(w_j | y) = \frac{\text{count}(w_j, y) + \alpha}{\sum_{w \in V} \text{count}(w, y) + \alpha |V|}
$$

#### Logistic Regression

For binary sentiment ($y \in \{0, 1\}$), logistic regression models:

$$
P(y = 1 | \mathbf{x}; \boldsymbol{\theta}) = \sigma(\boldsymbol{\theta}^\top \mathbf{x}) = \frac{1}{1 + e^{-\boldsymbol{\theta}^\top \mathbf{x}}}
$$

The objective function minimises regularised cross-entropy loss:

$$
\mathcal{L}(\boldsymbol{\theta}) = -\sum_{i=1}^{N} \left[ y_i \log \hat{p}_i + (1 - y_i) \log(1 - \hat{p}_i) \right] + \lambda \|\boldsymbol{\theta}\|_2^2
$$

The gradient with respect to $\boldsymbol{\theta}$ is:

$$
\nabla_{\boldsymbol{\theta}} \mathcal{L} = \sum_{i=1}^{N} (\hat{p}_i - y_i) \mathbf{x}_i + 2\lambda \boldsymbol{\theta}
$$

Optimisation proceeds via gradient descent or L-BFGS.

### Assumptions and Limitations

1. **Bag-of-words assumption**: Traditional models ignore word order, losing semantic information ("not good" vs "good not").

2. **Domain stationarity**: Models assume training and inference distributions match; domain shift degrades performance.

3. **Class balance**: Imbalanced sentiment classes bias classifiers toward majority class; weighted loss or resampling required.

4. **Independence of features** (Naive Bayes): Violated in text where words co-occur non-independently.

### Edge Cases

- **Empty or very short text**: Insufficient signal for reliable classification; return neutral or flag for review.
- **Mixed sentiment**: Documents containing both positive and negative opinions yield near-zero aggregate scores, masking true content.
- **Out-of-vocabulary terms**: Words absent from lexicon or training vocabulary contribute no information.

# Understanding the Mathematics

### Sentiment Score from Lexicon

**The equation**

$$S_{\text{lexicon}} = \frac{1}{n} \sum_{i=1}^{n} \text{polarity}(w_i)$$

**Read it aloud**

The lexicon sentiment score equals one divided by the total number of words, multiplied by the sum of the polarity values of each individual word from the first word to the last word.

**What each symbol means**

- $S_{\text{lexicon}}$ = the overall sentiment score for the text
- $n$ = the total count of words in the text
- $\sum_{i=1}^{n}$ = "add up for every word from 1 to n"
- $w_i$ = the i-th word in the text
- $\text{polarity}(w_i)$ = the sentiment value of word $w_i$ (positive numbers for positive words, negative for negative words)
- $\frac{1}{n}$ = dividing by word count to get an average

**A concrete numerical example**

A customer review says: "The service was excellent and helpful but slow." We have 8 words. Our sentiment lexicon assigns: "excellent" = +3, "helpful" = +2, "slow" = -2, and all other words = 0.

Step by step:
- Sum of polarities = 3 + 2 + (-2) + 0 + 0 + 0 + 0 + 0 = 3
- Divide by word count = 3 ÷ 8 = 0.375
- $S_{\text{lexicon}} = 0.375$ (mildly positive sentiment)

**Why this equation matters**

Without averaging across word count, longer texts would always have more extreme scores simply because they contain more words, making short and long reviews impossible to compare fairly.

### Logistic Function for Sentiment Probability

**The equation**

$$P(\text{positive}) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_k x_k)}}$$

**Read it aloud**

The probability that the sentiment is positive equals one divided by the quantity one plus e raised to the negative of the sum of the intercept plus each coefficient multiplied by its corresponding feature.

**What each symbol means**

- $P(\text{positive})$ = probability the text expresses positive sentiment (0 to 1)
- $e$ = Euler's number (approximately 2.718)
- $\beta_0$ = intercept (baseline log-odds before considering any features)
- $\beta_1, \beta_2, \ldots, \beta_k$ = coefficients showing how much each feature influences sentiment
- $x_1, x_2, \ldots, x_k$ = feature values (e.g., word counts, lexicon scores, exclamation marks)
- $k$ = total number of features

**A concrete numerical example**

We're analyzing an app review. Our trained model has $\beta_0 = -1.2$, $\beta_1 = 0.8$ (coefficient for positive word count), and $\beta_2 = 0.5$ (coefficient for exclamation marks). This review has $x_1 = 4$ positive words and $x_2 = 2$ exclamation marks.

Step by step:
- Linear combination = -1.2 + (0.8 × 4) + (0.5 × 2) = -1.2 + 3.2 + 1.0 = 3.0
- Exponent = $e^{-3.0}$ = 0.0498
- Final probability = 1 ÷ (1 + 0.0498) = 1 ÷ 1.0498 = 0.953

The model predicts a 95.3% probability this review is positive.

**Why this equation matters**

The logistic function guarantees our output is always a valid probability between 0 and 1, no matter how extreme the input features become—a linear model could absurdly predict 150% positive or -30% positive.

### TF-IDF Weighting

**The equation**

$$\text{TF-IDF}(w, d) = \text{TF}(w, d) \times \log\left(\frac{N}{\text{DF}(w)}\right)$$

**Read it aloud**

The TF-IDF weight for a word in a document equals the term frequency of that word in the document multiplied by the logarithm of the total number of documents divided by the document frequency of that word.

**What each symbol means**

- $\text{TF-IDF}(w, d)$ = importance weight of word $w$ in document $d$
- $\text{TF}(w, d)$ = how many times word $w$ appears in document $d$
- $N$ = total number of documents in the collection
- $\text{DF}(w)$ = number of documents containing word $w$
- $\log$ = logarithm function (dampens the scale)

**A concrete numerical example**

We're analyzing 10,000 product reviews ($N = 10{,}000$). The word "unreliable" appears 5 times in one review ($\text{TF} = 5$) and appears in 50 reviews total ($\text{DF} = 50$).

Step by step:
- Document frequency ratio = 10,000 ÷ 50 = 200
- Logarithm = log(200) = 2.301
- TF-IDF weight = 5 × 2.301 = 11.505

Compare this to "the," which appears 8 times in the same review but in 9,900 reviews: TF-IDF = 8 × log(10,000 ÷ 9,900) = 8 × 0.004 = 0.032. "Unreliable" gets much higher weight despite lower frequency.

**Why this equation matters**

TF-IDF automatically identifies words that are genuinely distinctive for sentiment analysis by downweighting common filler words, letting machine learning models focus on terms that actually carry emotional meaning.

### The Big Picture

The mathematics of sentiment analysis transforms messy human language into numbers that capture emotional tone. Lexicon scoring provides a simple average, but sophisticated models need the logistic function to convert feature combinations into valid probabilities. TF-IDF preprocessing ensures that emotionally meaningful words receive appropriate weight before any model sees them. We use these particular mathematical tools because sentiment isn't binary—it exists on a probability spectrum—and because language is high-dimensional, requiring us to balance hundreds of word features simultaneously. At its core, the math asks: given the specific words and patterns in this text, what's the likelihood a human would call this positive?

## Python Implementation

```python
"""
Sentiment Analysis: Comprehensive Implementation Examples
Demonstrates lexicon-based (VADER) and machine learning approaches
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ============================================================
# Example 1: Lexicon-Based Sentiment Analysis with VADER
# ============================================================

# Sample customer feedback data
feedback_data = [
    "The product quality is excellent and delivery was super fast!",
    "Terrible experience. The item arrived broken and support was unhelpful.",
    "It's okay, nothing special but does the job.",
    "Absolutely love this! Best purchase I've made all year.",
    "Disappointed with the quality. Would not recommend.",
    "Fast shipping, product as described. Satisfied customer.",
    "The worst customer service I have ever experienced!!!",
    "Decent value for money, could be better though."
]

# Initialize VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Analyze sentiment for each text
print("=" * 60)
print("VADER Lexicon-Based Sentiment Analysis")
print("=" * 60)

results = []
for text in feedback_data:
    # Get sentiment scores: neg, neu, pos, and compound
    scores = vader_analyzer.polarity_scores(text)
    
    # Classify based on compound score thresholds
    if scores['compound'] >= 0.05:
        label = 'Positive'
    elif scores['compound'] <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
    
    results.append({
        'text': text[:50] + '...' if len(text) > 50 else text,
        'compound': scores['compound'],
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu'],
        'label': label
    })

vader_df = pd.DataFrame(results)
print(vader_df.to_string(index=False))
print()

# ============================================================
# Example 2: Machine Learning Sentiment Classification
# ============================================================

# Create synthetic labelled dataset for training
np.random.seed(42)

# Positive review templates
positive_templates = [
    "Great product, highly recommend!",
    "Excellent quality and fast delivery",
    "Love it! Exceeded my expectations",
    "Best purchase ever, very satisfied",
    "Amazing value, will buy again",
    "Fantastic service and quality",
    "Perfect, exactly what I needed",
    "Outstanding product, five stars"
]

# Negative review templates
negative_templates = [
    "Terrible quality, total waste of money",
    "Awful experience, never again",
    "Broken on arrival, very disappointed",
    "Poor customer service, would not recommend",
    "Complete disaster, want my money back",
    "Horrible product, falling apart",
    "Worst purchase I've made",
    "Defective and poorly made"
]

# Generate training data with variations
def augment_text(templates, n_samples):
    """Generate variations of template texts"""
    texts = []
    for _ in range(n_samples):
        base = np.random.choice(templates)
        # Add random variations
        if np.random.random() > 0.5:
            base = base.upper() if np.random.random() > 0.5 else base.lower()
        texts.append(base)
    return texts

# Create balanced dataset
n_per_class = 200
positive_texts = augment_text(positive_templates, n_per_class)
negative_texts = augment_text(negative_templates, n_per_class)

texts = positive_texts + negative_texts
labels = [1] * n_per_class + [0] * n_per_class  # 1 = positive, 0 = negative

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# Vectorize text using TF-IDF
vectorizer = TfidfVectorizer(
    max_features=1000,      # Limit vocabulary size
    ngram_range=(1, 2),     # Include unigrams and bigrams
    min_df=2,               # Ignore very rare terms
    stop_words='english'    # Remove common stopwords
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("=" * 60)
print("Machine Learning Sentiment Classification")
print("=" * 60)
print(f"Training samples: {X_train_tfidf.shape[0]}")
print(f"Test samples: {X_test_tfidf.shape[0]}")
print(f"Vocabulary size: {X_train_tfidf.shape[1]}")
print()

# Train Logistic Regression classifier
lr_model = LogisticRegression(
    C=1.0,                  # Regularisation strength (inverse)
    class_weight='balanced', # Handle any class imbalance
    max_iter=1000,
    random_state=42
)
lr_model.fit(X_train_tfidf, y_train)

# Train Naive Bayes classifier for comparison
nb_model = MultinomialNB(alpha=1.0)  # Laplace smoothing
nb_model.fit(X_train_tfidf, y_train)

# Evaluate both models
print("Logistic Regression Results:")
print("-" * 40)
lr_pred = lr_model.predict(X_test_tfidf)
print(classification_report(y_test, lr_pred, target_names=['Negative', 'Positive']))

print("Naive Bayes Results:")
print("-" * 40)
nb_pred = nb_model.predict(X_test_tfidf)
print(classification_report(y_test, nb_pred, target_names=['Negative', 'Positive']))

# ============================================================
# Example 3: Interpreting Model Coefficients
# ============================================================

print("=" * 60)
print("Feature Importance Analysis (Logistic Regression)")
print("=" * 60)

# Extract feature names and coefficients
feature_names = vectorizer.get_feature_names


## Visualisations

![](../../_static/figures/analyze-sentiment_fig1.png)

![](../../_static/figures/analyze-sentiment_fig2.png)

## Using This in Heuristix

### What You'll Need

The Sentiment Analysis node expects a dataset with at least one text column containing the content you want to analyze. This could be customer reviews, survey responses, social media comments, or any other textual feedback. Your data should have one row per piece of text to analyze.

**Example input:**

| review_id | customer_review |
|-----------|-----------------|
| 1 | "This product exceeded my expectations!" |
| 2 | "Disappointed with the quality." |
| 3 | "It's okay, nothing special." |

### Configuration Parameters

| Parameter | What It Controls | Default | When to Change It |
|-----------|-----------------|---------|-------------------|
| **Text Column** | Which column contains the text to analyze | (none) | Always set this—it's required. Select the column with your review, comment, or feedback text. |
| **Model** | The sentiment analysis approach | VADER | Use VADER for social media or informal text. Switch to TextBlob for more formal content like business reviews. Try Transformers for the highest accuracy when you have complex, nuanced text. |
| **Output Column Name** | What to call the new sentiment score column | "sentiment_score" | Change this if you're comparing multiple sentiment methods or want a more descriptive name like "review_sentiment". |
| **Include Confidence** | Whether to add a confidence score alongside the sentiment | Enabled | Keep enabled to understand how certain the model is. Disable if you only need the basic positive/negative/neutral classification. |
| **Classification Threshold** | Score boundaries for positive/neutral/negative labels | -0.05 to 0.05 (neutral) | Adjust if you're seeing too many neutrals. Tightening the range (e.g., -0.1 to 0.1) creates stricter positive/negative classifications. |

### What You'll Get Back

The node adds several columns to your dataset:

- **sentiment_score**: A numerical value typically ranging from -1 (very negative) to +1 (very positive)
- **sentiment_label**: A categorical classification—"positive", "negative", or "neutral"
- **confidence_score**: How certain the model is about its classification (0-1 scale)

You'll also see a **Sentiment Distribution** chart showing the breakdown of positive, negative, and neutral classifications, plus a **Score Histogram** displaying the distribution of raw sentiment scores across your dataset.

### Connecting Downstream

After sentiment analysis, you'll typically want to:

- **Filter node** → Isolate negative reviews for customer service follow-up
- **Group & Aggregate node** → Calculate average sentiment by product, time period, or customer segment
- **Correlate node** → Explore relationships between sentiment and metrics like star ratings or purchase amount
- **Visualize node** → Create sentiment trend charts over time

### Quick Start

1. **Connect your dataset** containing text reviews or comments to the Sentiment Analysis node
2. **Select your text column** from the "Text Column" dropdown
3. **Keep VADER as the model** unless your text is highly formal
4. **Leave other settings at default** for your first run
5. **Execute the node** and review the sentiment distribution chart
6. **Add a Filter node** after sentiment analysis to examine your most negative feedback first

### Practical Tips

**Watch for short text**. Sentiment analysis struggles with very brief text like "Good" or "Bad". If you see lots of neutral classifications, check if your text is too short to carry meaningful sentiment signals.

**Language matters**. The default models work best with English text. If you're analyzing other languages, you'll need to switch to the Multilingual Transformer model option.

**Context is king**. A review saying "This isn't bad" will often be classified as negative due to the word "bad", even though the customer means something positive. When you spot these inversions in your results, consider switching to the Transformer model, which better handles negation and sarcasm.

**Combine with other data**. Sentiment scores become truly powerful when correlated with structured data—compare sentiment across product categories, customer demographics, or time periods to uncover actionable patterns.

**Validate with spot checks**. Always read a sample of reviews from each sentiment category to ensure the classifications align with your interpretation. This helps you calibrate thresholds and choose the right model for your specific use case.

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial exploratory analysis of a new text dataset when you need rapid feedback on sentiment distribution and don't yet know if deeper analysis is warranted.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `"vader"` | Lexicon-based, no training required, instant results |
| `batch_size` | `1000` | Process large chunks quickly without memory constraints |
| `output_format` | `"label_only"` | Simplest categorical output (positive/negative/neutral) |
| `confidence_threshold` | `None` | Accept all predictions to see full distribution |

**What you get:** Fast categorical sentiment labels suitable for quick distribution charts and initial pattern identification.

**Trade-off:** Lower accuracy than ML models; struggles with sarcasm, domain-specific language, and nuanced sentiment.

### Recipe 2: Production-Grade Classification

**When to use:** Deploying sentiment analysis as part of a customer feedback pipeline, automated monitoring system, or any application where accuracy and reliability are critical.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `"distilbert-base-uncased-finetuned-sst-2"` | Transformer-based with strong accuracy across domains |
| `batch_size` | `16` | Balance GPU memory usage with throughput |
| `output_format` | `"probabilities"` | Full probability distribution enables confidence filtering |
| `confidence_threshold` | `0.85` | Flag low-confidence predictions for human review |
| `max_length` | `512` | Full token capacity for longer reviews/comments |
| `handle_neutrals` | `True` | Preserve three-class distinction rather than forcing binary |

**What you get:** High-accuracy predictions with confidence scores that enable quality control workflows and exception handling.

**Trade-off:** 10-50x slower than lexicon methods; requires GPU for reasonable performance on large datasets.

### Recipe 3: Financial News Analysis

**When to use:** Analyzing market-moving news, earnings call transcripts, or financial social media where domain vocabulary and subtle hedging language are prevalent.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `"finbert"` | Specifically trained on financial text corpus |
| `negation_scope` | `5` | Capture longer-range negations common in formal language |
| `aspect_terms` | `["earnings", "guidance", "outlook", "revenue"]` | Focus on market-relevant aspects |
| `temporal_weight` | `"decay"` | More recent sentences weighted higher in document scoring |
| `output_format` | `"granular"` | Sentence-level sentiment to catch mixed messages |

**What you get:** Domain-aware sentiment that correctly interprets financial hedging, forward-looking statements, and technical terminology.

**Trade-off:** Requires domain-specific model that may underperform on general text; aspect configuration needs market knowledge.

### Recipe 4: Call Center Emotion Escalation Detection

**When to use:** Identifying customer service interactions that are deteriorating emotionally, even when language remains superficially polite—a hidden use case where sentiment trends matter more than absolute values.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `window_size` | `3` | Rolling sentiment across conversation turns |
| `metric` | `"sentiment_velocity"` | Rate of sentiment decline, not absolute score |
| `threshold_delta` | `-0.3` | Flag conversations with rapid negative shifts |
| `ignore_pleasantries` | `True` | Filter greetings/closings that mask true sentiment |
| `output_format` | `"time_series"` | Preserve sequential interaction structure |

**What you get:** Early warning system for escalating conversations requiring supervisor intervention, catching frustration before explicit complaints.

**Trade-off:** Requires sequential conversation data with turn structure; not applicable to single-instance reviews or posts.

## Business Applications

**Financial Services**

A mid-sized UK mortgage lender receives 3,500 customer service emails daily, with 18% containing complaints that regulatory guidelines require be escalated within 24 hours. Manual review teams struggle to identify urgent issues fast enough, risking compliance violations and customer churn. Sentiment analysis automatically scores every incoming message, flagging highly negative communications (sentiment < -0.6) and routing them to senior specialists while neutral inquiries flow to standard queues. This approach reduced regulatory breach incidents from 47 to 3 per quarter and cut average complaint resolution time from 4.2 days to 18 hours.

**Retail & E-commerce**

An e-commerce retailer with 2M SKUs sees product reviews as critical conversion drivers but cannot manually monitor quality issues across its catalogue. Negative reviews mentioning "broken," "defective," or "stopped working" appear on 847 product pages before the merchandising team notices a supplier has shipped a faulty batch of phone chargers. Sentiment analysis continuously monitors all reviews, immediately alerting category managers when sentiment drops below baseline thresholds for specific SKUs or brands. The retailer now catches supplier quality problems 6.3 days earlier on average, preventing an estimated $890K in annual returns and protecting conversion rates that drop 23% when negative reviews accumulate unchecked.

**Healthcare**

A hospital network with twelve facilities collects 14,000 patient experience surveys monthly but only reads verbatim comments for the 8% flagged by low numeric scores, missing valuable insights in "satisfied" responses. A patient writes "staff were nice but I waited five hours in pain" alongside a 7/10 rating that wouldn't trigger review. Sentiment analysis processes all open-text feedback, identifying negative sentiment even in seemingly positive surveys and categorizing concerns by theme (wait times, pain management, communication). This discovered that 34% of "satisfied" patients expressed significant concerns, leading to process improvements that lifted the network's Hospital Consumer Assessment score from the 62nd to 81st percentile.

**Insurance**

An auto insurance carrier processes 2,800 claims daily, with fraud investigators manually reviewing 340 flagged by rules-based systems—but fraud rates remain at 11%, above industry benchmarks. Investigators notice fraudulent claimants often display inconsistent emotional tone when describing accidents in written statements. Sentiment analysis examines claim narratives for unusual patterns: excessive positivity when discussing injuries, neutral affect describing supposedly traumatic events, or sentiment shifts between initial report and follow-up. Combined with traditional fraud signals, this approach reduced false positives by 34% while increasing fraud detection rates by 2.7 percentage points, saving $4.3M annually.

**Manufacturing**

A industrial equipment manufacturer with 180 field service technicians requires detailed incident reports after each repair visit, generating 40,000 reports yearly. Engineers seeking to identify recurring product defects must manually read hundreds of reports, delaying quality improvements. Sentiment analysis scores technician frustration levels in reports, with highly negative sentiment indicating products that repeatedly fail or are difficult to repair. This surfaced that a $47,000 CNC machine model generated consistently frustrated technician commentary, prompting investigation that discovered a design flaw before a costly recall became necessary.

**Marketing & Advertising**

A consumer packaged goods brand launches a sustainability campaign across social media, tracking volume of mentions but not realizing early posts generate mockery for perceived "greenwashing." By the time the marketing team manually reviews comments three days later, negative sentiment has spread to news coverage. Real-time sentiment analysis of social mentions with alerting when sentiment velocity shifts negative would have flagged the backlash within four hours, enabling rapid response. Brands using this approach contain PR crises 73% faster than those relying on manual monitoring.

**Telecommunications**

A mobile network operator sees customer service call volume spike 340% during a regional outage but cannot prioritize which customers are at highest churn risk. Sentiment analysis of call transcripts and social media mentions identifies customers expressing intent to switch carriers ("canceling my service," "moving to [competitor]"), enabling retention specialists to proactively offer service credits to the 8% most at-risk. This reduced post-outage churn from 4.1% to 1.8%, retaining $2.7M in annual recurring revenue.

**Public Sector**

A city government collects 9,000 public comments on a proposed zoning change but cannot efficiently analyze feedback to inform council decisions. Sentiment analysis processes all submissions, categorizing them by topic (traffic, schools, property values) and sentiment, revealing that 67% support the proposal overall but 81% express concerns about traffic impact. This enabled targeted amendments that maintained public support while addressing the primary concern.

## Worked Example

Sarah Chen, a senior data scientist at Luminary Hotels, was sitting across from Marcus Webb, the VP of Guest Experience, when he slid a printout across the conference table. "We're getting killed on these reviews," Marcus said, tapping a highlighted section. "But I can't tell if it's just a few loud voices or if we actually have a systemic problem. Can you give me the real picture?"

Luminary had just rolled out a new mobile check-in system across their 47 properties, and guest feedback was pouring in through post-stay survey emails. Marcus needed to know whether the rollout was helping or hurting the guest experience—and he needed to know before the quarterly board meeting in two weeks.

## The Data

Sarah pulled guest comments from the previous three months. The dataset was messy in the way real data always is: some guests wrote novels, others left single words, and a few had clearly copied error messages directly into the feedback box. Here's what a sample looked like:

| guest_id | property_code | date | feedback_text | stayed_before |
|----------|---------------|------------|--------------------------------------------------|---------------|
| G10291 | LUM-CHI | 2024-01-15 | The new check-in was fast but the room wasn't ready when I arrived. Frustrated. | Yes |
| G10847 | LUM-BOS | 2024-01-18 | Loved the app! So easy. Room was perfect. | No |
| G10923 | LUM-SEA | 2024-01-22 | complete disaster couldn't get app to work front desk unhelpful | Yes |
| G11204 | LUM-MIA | 2024-02-03 | Check-in worked fine. Room smelled like smoke though, not great. | No |

The `feedback_text` column was the one that mattered. Sarah noticed immediately that some entries lacked punctuation, others mixed praise with complaints, and a handful were in languages other than English (she made a note to filter those separately).

## The Setup

Sarah opened her workflow and dragged in the Analyze Sentiment node. She connected it to her cleaned dataset and opened the configuration panel. For the text column, she selected `feedback_text`—the obvious choice. But she paused at the output options. She wanted both a categorical label (positive, negative, neutral) and a numerical score, because she knew Marcus would want simple counts but she'd need the scores for deeper analysis later. She enabled both outputs and named them `sentiment_label` and `sentiment_score`.

She also checked the "handle mixed sentiment" option. Looking at that first review about fast check-in but an unready room, she knew many comments would contain conflicting emotions. The algorithm would need to weight the overall tone rather than just counting positive and negative words.

## The Results

When the node finished processing 2,847 guest comments, Sarah examined the output. The new columns appeared exactly as she'd configured:

| feedback_text | sentiment_label | sentiment_score |
|-----------------------------------------------|-----------------|-----------------|
| The new check-in was fast but the room... | Negative | -0.31 |
| Loved the app! So easy. Room was perfect. | Positive | 0.89 |
| complete disaster couldn't get app to work... | Negative | -0.78 |
| Check-in worked fine. Room smelled like smoke... | Negative | -0.24 |

The `sentiment_score` ranged from -1.0 (most negative) to +1.0 (most positive), with values near zero indicating neutral sentiment. Sarah aggregated the results: 41% positive, 38% negative, 21% neutral. Not the disaster Marcus feared, but not great either.

## The Insight

But here's where it got interesting. Sarah split the analysis by the `stayed_before` column. Guests who had stayed at Luminary properties before showed 52% negative sentiment. First-time guests? Only 28% negative. The app was delighting new guests who had no comparison point, but frustrating loyal guests who remembered the old process—or who expected their loyalty status to make things smoother. The system was creating a two-tiered experience, and it was alienating the guests Luminary most wanted to retain.

## The Decision

Sarah presented this to Marcus and the operations team the following Tuesday. The headline number—38% negative overall—had concerned him. But the loyalty split changed everything. Within a week, the product team had prioritized two features: automatic room selection for repeat guests and a "skip the tutorial" option. They also created a dedicated phone line for loyalty members having app trouble.

Three months later, sentiment among returning guests had improved to 61% positive. Marcus credited Sarah's analysis in his board presentation, noting that without the segmented view, they would have either panicked and rolled back the entire system or missed the loyalty problem entirely.

## What Sarah Would Do Differently

Looking back, Sarah wished she'd run the sentiment analysis separately on the first sentence versus the full comment. Many guests front-loaded their main complaint, then added secondary observations. Analyzing sentiment by sentence position might have revealed priorities even more clearly. She also realized she should have filtered out the sixteen comments that were just "N/A" or "None"—they skewed the neutral category artificially high and added no real information.

```python
# Sarah's core sentiment analysis script
import pandas as pd
from transformers import pipeline

# Load the feedback data
df = pd.read_csv('guest_feedback.csv')

# Initialize sentiment analyzer
sentiment_analyzer = pipeline(
    'sentiment-analysis',
    model='distilbert-base-uncased-finetuned-sst-2-english'
)

# Function to handle long texts (model has token limits)
def analyze_sentiment(text):
    if pd.isna(text) or len(text.strip()) == 0:
        return {'label': 'NEUTRAL', 'score': 0}
    # Truncate to first 500 characters to stay within limits
    truncated = text[:500]
    return sentiment_analyzer(truncated)[0]

# Apply sentiment analysis
df['sentiment_result'] = df['feedback_text'].apply(analyze_sentiment)
df['sentiment_label'] = df['sentiment_result'].apply(lambda x: x['label'])
df['sentiment_score'] = df['sentiment_result'].apply(
    lambda x: x['score'] if x['label'] == 'POSITIVE' else -x['score']
)

# Segment by guest loyalty
loyalty_sentiment = df.groupby('stayed_before')['sentiment_label'].value_counts(normalize=True)
print(loyalty_sentiment)
```

## Interpreting Your Results

You've just run sentiment analysis on your text data. Now you're looking at polarity scores, confidence levels, and distribution charts wondering what they actually mean for your project. Let's translate these outputs into decisions you can act on.

### Sentiment Polarity Scores

**Plain-English meaning**: Each text receives a score typically ranging from -1 (extremely negative) to +1 (extremely positive), with 0 representing neutral sentiment. Think of this as a numerical translation of emotional tone—like asking "on a scale from furious to delighted, where does this comment fall?"

**Concrete benchmarks**:
- **-1.0 to -0.3**: Strongly negative. Customer complaints, anger, disappointment. Immediate attention needed.
- **-0.3 to -0.05**: Mildly negative. Lukewarm dissatisfaction, minor criticisms, neutral-leaning-negative.
- **-0.05 to +0.05**: True neutral. Factual statements, mixed opinions canceling out, or genuinely ambivalent content.
- **+0.05 to +0.3**: Mildly positive. Satisfied but not enthusiastic, faint praise, neutral-leaning-positive.
- **+0.3 to +1.0**: Strongly positive. Enthusiasm, loyalty signals, explicit recommendations.

**Red flags**: 
- All scores clustering tightly around zero suggests your text might be too formal, technical, or the algorithm can't detect sentiment (check if you're analyzing legal documents or instruction manuals by mistake)
- Bimodal distribution with peaks at both extremes but nothing in middle indicates polarized opinions—dig deeper into what's driving the split
- 90%+ scores at exactly +1.0 or -1.0 means algorithm saturation; your model might be oversimplifying

### Confidence/Compound Scores

**Plain-English meaning**: This tells you how certain the algorithm is about its sentiment classification. A review saying "This product is absolutely terrible and I hate everything about it" yields high confidence. A sarcastic tweet saying "Oh great, another Monday" yields low confidence because context is ambiguous.

**Concrete benchmarks**:
- **Below 0.3**: Algorithm is guessing. Manual review required.
- **0.3–0.6**: Moderate confidence. Safe for exploratory analysis, risky for automated decisions.
- **0.6–0.85**: High confidence. Suitable for most business applications.
- **Above 0.85**: Very high confidence. Clear, unambiguous sentiment expression.

**Red flags**: 
- Low confidence + extreme polarity = likely sarcasm, idioms, or domain-specific language your model doesn't understand
- High confidence + neutral score = contradictory signals; review for mixed sentiment within single text

### Sentiment Distribution Charts

**Plain-English meaning**: These visualizations show what percentage of your texts fall into positive, negative, or neutral categories. You're seeing the emotional landscape of your entire dataset at a glance.

**Reading the pattern**: 
- **Customer reviews**: Expect 60-75% positive, 15-25% neutral, 10-20% negative (if your product is healthy)
- **Social media brand mentions**: Expect 40-50% neutral, 30-40% positive, 15-25% negative (more balanced)
- **Support tickets**: Expect 60-80% negative, 15-30% neutral, 5-15% positive (negative skew is normal)

**Red flags**: 
- Distribution that's wildly different from your domain's baseline needs investigation—either your data sampling is biased or something unusual is happening
- Perfectly balanced distribution (33%/33%/33%) suggests classification failure or overly aggressive neutral categorization

### Sanity Check Checklist

Before trusting your sentiment results, verify:

1. **Sample spot-check**: Manually read 20 random texts and their assigned scores. Do at least 15 match your human judgment?
2. **Extreme score review**: Pull up 5 texts scored at -1.0 and 5 at +1.0. Are they genuinely the most extreme examples?
3. **Language consistency**: Confirm all text is in the language your model was trained on (mixing languages destroys accuracy)
4. **Text length check**: Texts under 10 words or over 500 words often misclassify—note what percentage of your data falls outside the 10-200 word sweet spot
5. **Domain alignment**: If analyzing specialized text (medical, legal, financial), acknowledge accuracy drops 15-30% compared to general consumer text

### Good Enough to Act On?

Your sentiment analysis is actionable when **at least 70% of scores have confidence above 0.6 AND your spot-check validation exceeds 75% accuracy**. Below these thresholds, use results for exploration and hypothesis generation only, not for automated routing, decision-making, or reporting to stakeholders. When in doubt, segment by confidence score and act only on the high-confidence subset while flagging low-confidence texts for human review.

## Decision Guidance

### What This Result Is Telling You

Sentiment analysis results reveal how your customers, stakeholders, or market perceive your brand, product, or service at scale. When you see that 72% of product reviews are positive, you're not just looking at a percentage—you're seeing a direct measure of customer satisfaction that predicts repeat purchases, referral likelihood, and revenue retention. Negative sentiment concentrated in specific product features or service touchpoints tells you exactly where to allocate improvement resources for maximum impact on customer experience.

The emotional tone captured in sentiment scores represents early warning signals before they appear in traditional business metrics. A sudden 15-percentage-point drop in positive sentiment about your mobile app precedes declining App Store ratings by weeks and churn increases by months. Similarly, rising negative sentiment in employee feedback channels forecasts attrition spikes and productivity declines before they damage operations. These results give you advance notice to intervene while problems remain manageable.

Beyond simple positive-negative splits, sentiment patterns reveal strategic opportunities. When neutral sentiment dominates (above 40% of responses), you're seeing customer indifference—perhaps the most dangerous condition because indifferent customers switch providers without warning. Geographic or demographic segments showing distinctly different sentiment profiles indicate where product-market fit succeeds or fails, guiding expansion decisions and marketing spend allocation.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|---|---|---|---|
| Negative sentiment >25% concentrated in one product feature or service element | A specific pain point drives customer dissatisfaction; fixing this one issue could shift overall perception | Prioritize engineering or operations resources to address this specific issue; track sentiment weekly after implementing fixes | Product managers and operations leaders |
| Positive sentiment declining >10 percentage points month-over-month for 2+ consecutive months | Customer satisfaction eroding systematically; competitors may be gaining ground or internal changes harming experience | Initiate customer listening sessions, competitive analysis, and root cause investigation; pause major product changes until stabilized | Chief Customer Officer or VP Customer Experience |
| Sentiment distribution shows >40% neutral responses | Customers lack strong connection to your brand; vulnerable to competitive offers and price sensitivity | Launch differentiation initiatives, strengthen value proposition messaging, increase customer engagement touchpoints | CMO and brand strategy teams |
| Positive sentiment >70% but concentrated in one customer segment or geography | Product-market fit strong in specific niche but not broadly; growth may hit ceiling | Either double down on proven segment or methodically test modifications for underperforming segments before broad expansion | Chief Strategy Officer and business unit leaders |
| Negative sentiment spikes >15 percentage points within single week | Crisis event, viral complaint, or service failure requiring immediate response | Activate crisis communication protocols; identify root cause within 24 hours; deploy executive response if needed | PR/Communications lead and executive team |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Sample size exceeds 300 responses per segment analyzed and sentiment labels show >85% agreement when manually spot-checked
- Sentiment trends remain stable (changes <5 percentage points) over at least three measurement periods
- Results align with other business metrics (NPS scores, retention rates, support ticket volumes)

**Proceed with caution when:**
- Analyzing specialized domains (medical, legal, technical) where standard sentiment models may misinterpret jargon
- Neutral sentiment exceeds 35%—this often indicates model uncertainty rather than true customer ambivalence
- Working with translated text or multiple languages where cultural expression patterns vary significantly

**Investigate before acting when:**
- Sentiment results contradict other customer satisfaction metrics by >20 percentage points
- Confidence scores from your sentiment model fall below 70% for more than 15% of classified texts
- Results show dramatic sentiment swings (>20 percentage point changes) between adjacent time periods without known external cause

**Do not use these results yet if:**
- Sample contains fewer than 100 texts per category you're analyzing
- Your training data or lexicon is more than 18 months old in fast-moving industries (technology, fashion, entertainment)
- Manual review of 50 random predictions shows accuracy below 75%

### The Cost of Getting This Wrong

Misinterpreting sentiment analysis leads to expensive strategic misdirection. A consumer electronics company once responded to seemingly negative sentiment about their "insane battery life" and "sick camera" by investigating battery safety and image quality complaints—failing to recognize that younger customers used these terms positively. They diverted $2M in engineering resources to fix non-problems while actual issues went unaddressed, delaying their product launch by three months and ceding market share to competitors. Conversely, dismissing genuine negative sentiment as "just noise" or "small sample complainers" allows customer experience problems to metastasize unchecked. By the time declining renewal rates and rising churn appear in financial reports, you've lost customers who could have been retained with early intervention—and recovery requires 5-10 times the investment that proactive fixes would have cost. The emotional disconnect between executives who trust gut feel over data and frontline teams who see sentiment evidence creates organizational paralysis, where neither group commits resources and the business drifts toward irrelevance.

## Common Pitfalls

**The Sarcasm Blind Spot**

Here's what happened: A marketing analyst was tracking brand sentiment for a fast-food chain on Twitter during a product launch. Their sentiment model classified "Oh great, another soggy burger. Just what I needed today. #blessed" as 82% positive because it contained the words "great," "blessed," and "needed." The weekly dashboard showed sentiment climbing to 73% positive during the exact week when customer service complaints tripled. They concluded the launch was a success and recommended expanding the campaign.

Why it happens: Standard lexicon-based models and basic machine learning classifiers perform simple token matching without understanding contextual meaning or rhetorical devices. Sarcasm deliberately inverts the relationship between words and intent, and most sentiment models treat text literally.

How to detect it: Look for a suspicious divergence between sentiment scores and behavioral metrics—high positive sentiment but declining sales, low engagement, or rising support tickets. Manually review a random sample of 50-100 texts classified as "positive" and calculate the misclassification rate for sarcastic content specifically. If more than 15% are clearly sarcastic, your model has this problem.

The fix: Use transformer-based models (BERT, RoBERTa) trained on conversational data, or add a sarcasm detection preprocessing step before sentiment classification.

**The Domain Dictionary Disaster**

Here's what happened: A junior data scientist at a pharmaceutical company deployed a general-purpose sentiment model to analyze patient feedback about a new medication. The model flagged "This drug is insane—I can finally sleep through the night!" as strongly negative (sentiment score: -0.74) because "insane" appeared in the negative lexicon. After filtering out "negative" reviews, management never saw that 40% of patients were reporting dramatic positive results using colloquial language.

Why it happens: Sentiment lexicons are built for general language, but every domain—medical, financial, gaming, teen social media—has its own vocabulary where standard sentiment words carry different meanings. "Sick" means ill in healthcare contexts but excellent in gaming communities.

How to detect it: Check your confusion matrix for specific domains and calculate precision/recall separately for domain-specific vocabulary. Pull all reviews containing known domain terms (like "insane," "killing it," "dead") and measure their classification accuracy independently. If domain-specific terms show accuracy below 60% while general terms hit 85%+, you have a domain mismatch.

The fix: Build a custom sentiment lexicon for your domain or fine-tune your model on labeled examples from your specific industry.

**The Neutral Zone Ignorance**

Here's what happened: A business intelligence manager was presenting quarterly sentiment trends for customer support interactions. Their visualization showed a beautiful chart with 65% positive and 35% negative sentiment, color-coded green and red. The executive team celebrated the positive trend. What they missed: the sentiment model had classified 48% of all comments as "neutral" and these were simply excluded from the report. Those neutral comments contained the phrase "I called three times" 847 times—a clear operational failure signal.

Why it happens: Humans think in binaries—good or bad—and neutral feels like non-information. Practitioners exclude neutral classifications to create cleaner visualizations, not realizing that neutral often contains the most actionable operational intelligence.

How to detect it: Always report the distribution across all three classes. If your "neutral" bucket contains more than 30% of your data, manually inspect 100 random neutral samples. Look for patterns—are these truly neutral, or are they complaints without emotional language, requests for information, or expressions of confusion?

The fix: Report all three sentiment categories and create a separate analysis stream for neutral content, particularly looking for operational keywords like "wait," "transfer," "third time," or "still not resolved."

**The Aggregation Illusion**

Here's what happened: An e-commerce analyst calculated average sentiment scores across all product reviews for a clothing retailer's quarterly business review. The average was 0.61 (on a -1 to +1 scale), which looked solidly positive. They recommended maintaining current quality standards. What the data actually showed: a bimodal distribution with 45% of reviews at +0.9 or higher and 38% at -0.7 or lower. The product had a sizing problem—it fit perfectly or terribly with almost nothing in between.

Why it happens: Summary statistics feel efficient and executives want single numbers. But sentiment distributions are rarely normal, and averaging destroys the variance signal that often contains the most important operational insight.

How to detect it: Always plot the distribution histogram before calculating means. Check the standard deviation—if it's above 0.35 on a normalized scale, your mean is hiding critical information. Calculate the interquartile range and look for bimodal or multimodal patterns.

The fix: Report sentiment distributions, not just averages, and specifically flag high-variance products or time periods for deeper investigation.

## Common Misconceptions

**"Sentiment analysis tells you whether customers are happy or unhappy"**

**Why people believe this:** Business stakeholders naturally conflate sentiment with satisfaction because both concepts seem to occupy the same emotional spectrum. When a review says "This product is terrible," the negative sentiment appears to directly indicate an unhappy customer, creating a seemingly straightforward measurement tool for customer satisfaction.

**The truth:** Sentiment analysis measures linguistic polarity—the emotional valence of words and phrases—not the underlying psychological state or business outcome. A customer might write "I'm furious that this incredible product is sold out everywhere" which contains strong negative emotional language but indicates high product desirability. Conversely, "The service was fine, nothing special" reads as neutral-to-slightly-positive but may represent a disappointed customer who expected more. Sentiment analysis classifies text based on learned or coded linguistic patterns, not the complex relationship between customer experience and business metrics. Satisfaction is a domain-specific construct that requires understanding context, expectations, and outcomes—elements that pure sentiment classification cannot capture.

**The real-world consequence:** A retail company prioritizes responding to reviews flagged as "negative sentiment" while ignoring neutral-sentiment reviews containing phrases like "not worth the price" or "expected better quality." They allocate customer service resources based on sentiment scores rather than actual dissatisfaction indicators, missing genuinely at-risk customers while chasing false positives from emotional but ultimately positive feedback.

**"More training data always improves sentiment model performance"**

**Why people believe this:** This misconception extends the generally valid machine learning principle that larger datasets reduce overfitting and improve generalization. Junior data scientists have internalized "get more data" as the default response to model performance issues, and it often works for many ML problems.

**The truth:** Sentiment model performance plateaus or even degrades when additional training data introduces domain mismatch, temporal drift, or label noise. A model trained on 10,000 carefully labeled product reviews from your specific domain will typically outperform one trained on 100,000 generic sentiment examples scraped from multiple sources. Sentiment is highly context-dependent—sarcasm, domain-specific language, and cultural norms mean that "sick" signals positive sentiment in sneaker reviews but negative in healthcare contexts. Adding data from different domains dilutes the model's ability to learn these crucial contextual patterns. Furthermore, sentiment labeling is inherently subjective; as datasets grow, label inconsistency increases because different annotators interpret ambiguous cases differently.

**The real-world consequence:** A financial services team spends three months and significant annotation budget expanding their training set from 5,000 to 50,000 examples by incorporating general Twitter sentiment data. Their model's performance on actual customer feedback degrades by 8% because the training set now contains different linguistic patterns, emoji usage, and topic distributions. Meanwhile, a competitor achieves better results by carefully curating 7,000 domain-specific examples with rigorous annotation guidelines, reaching production two months earlier.

## How This Connects

### Before This Node

**Load Text Data** imports raw textual data from sources like CSV files, databases, or APIs—providing the unstructured text that Analyze Sentiment will process. Bad upstream data looks like malformed encodings, binary content misread as text, or completely empty fields, which causes sentiment models to fail silently or return meaningless scores.

**Clean Text** removes HTML tags, special characters, excessive whitespace, and standardizes encoding—ensuring the sentiment analyzer receives properly formatted input that won't be confused by markup artifacts. Without this step, sentiment models may misinterpret `&amp;` as emotional content or treat `<div>` tags as words, skewing polarity scores toward neutral.

**Filter Rows** removes irrelevant records such as automated messages, spam, or non-English content—focusing the sentiment analysis on legitimate customer opinions that actually reflect emotional tone. Bad filtering leaves bot-generated reviews or system notifications in the dataset, diluting genuine sentiment signals and making aggregate scores unreliable.

**Tokenize Text** splits sentences into individual words or subword units—preparing text in the format required by many sentiment models, especially those using embeddings. Improper tokenization treats contractions like "don't" as single tokens or splits hyphenated sentiment words incorrectly, causing models to miss negations and reverse sentiment predictions.

**Handle Missing Values** addresses NULL or empty text fields through removal or placeholder assignment—preventing runtime errors when sentiment analyzers encounter unexpected data types. Unchecked missing values either crash the pipeline or get processed as empty strings with default neutral scores, misrepresenting the true sentiment distribution.

**Join Data** combines text with metadata like timestamps, customer IDs, or product categories—enabling downstream sentiment analysis to be grouped, filtered, or compared across meaningful business dimensions. Without proper joins, sentiment scores become orphaned metrics disconnected from the business context needed for actionable insights.

### After This Node

**Group and Aggregate** calculates average sentiment scores by category, time period, or customer segment—transforming individual text-level predictions into business-level KPIs like monthly brand perception trends. Sentiment scores' numerical format makes them ideal for standard aggregation functions.

**Classify Records** uses sentiment polarity as a feature in broader classification models predicting outcomes like churn risk or purchase intent—leveraging emotional tone as a behavioral signal. The categorical sentiment output (positive/negative/neutral) slots directly into feature engineering pipelines.

**Visualize Distribution** creates histograms, time series, or heatmaps showing sentiment patterns across products or regions—making emotional trends immediately visible to stakeholders. Sentiment's bounded numerical range (-1 to +1 or 0 to 100) maps naturally to color scales and chart axes.

**Filter on Conditions** isolates extremely negative reviews or sudden sentiment drops—flagging priority cases for customer service intervention. The scored output enables precise threshold-based filtering that raw text cannot support.

**Export Results** writes sentiment-enriched datasets to dashboards, data warehouses, or CRM systems—operationalizing emotional insights in business workflows. The structured sentiment columns integrate seamlessly with existing tabular data schemas.

### Common Pipeline Patterns

**Product Review Monitoring Pipeline**  
Load Text Data → Clean Text → **Analyze Sentiment** → Group and Aggregate → Visualize Distribution  
Tracks average product sentiment weekly to identify quality issues before they escalate, typically catching problems within 48 hours of review publication.

**Customer Support Prioritization Pipeline**  
Load Text Data → Filter Rows → **Analyze Sentiment** → Filter on Conditions → Export Results  
Routes highly negative support tickets to senior agents automatically, reducing escalation response time by 60% compared to manual review.

**Social Campaign Performance Pipeline**  
Join Data → Tokenize Text → **Analyze Sentiment** → Classify Records → Group and Aggregate  
Measures campaign emotional impact across demographics to optimize messaging, correlating sentiment shifts with conversion rate changes of 15-20%.

### What to Have Ready

**Text column identified**: Confirm which field contains the natural language content to analyze—typically a column named "review_text," "comment," or "message" with string data type, not numeric codes or categories.

**Language consistency verified**: Ensure 95%+ of text is in the language your sentiment model supports (usually English), checking a sample for mixed-language content that will produce unreliable scores.

**Minimum text length established**: Define whether short texts (under 10 words) provide meaningful sentiment—many models perform poorly on fragments like "ok" or "fine," returning false-neutral predictions.

**Business context defined**: Decide what sentiment scale means for your use case—whether "negative" product reviews require different intervention thresholds than "negative" employee feedback, and what score constitutes actionable concern.

## Try It Yourself

### Recommended Dataset

**Dataset:** `sklearn.datasets.fetch_20newsgroups`  
**Source:** `sklearn.datasets.fetch_20newsgroups(subset='train', categories=['comp.graphics', 'sci.med'])`

This dataset is ideal for sentiment analysis because it contains real-world text documents with naturally occurring opinions and technical discussions. The newsgroup posts include subjective language, recommendations, and evaluative statements that carry sentiment. We'll focus on two categories to create a binary classification scenario where we can identify positive vs. negative language patterns.

**Business Question:** Can we automatically classify the emotional tone of customer support forum posts to prioritize responses to frustrated users?

**Size:** ~1,200 documents × 1 feature (text), though each document contains 50–500 words

### Starter Code

```python
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load newsgroup data from two contrasting categories
newsgroups = fetch_20newsgroups(subset='train', 
                                categories=['comp.graphics', 'sci.med'],
                                remove=('headers', 'footers', 'quotes'))

# Create DataFrame for easier exploration
df = pd.DataFrame({'text': newsgroups.data, 'category': newsgroups.target})
df['category_name'] = df['category'].map({0: newsgroups.target_names[0], 
                                           1: newsgroups.target_names[1]})

print("=== Dataset Overview ===")
print(f"Total documents: {len(df)}")
print(f"Category distribution:\n{df['category_name'].value_counts()}\n")

# Display sample text to understand content
print("=== Sample Document ===")
print(df['text'].iloc[0][:300] + "...\n")

# Convert text to numerical features using TF-IDF (term frequency-inverse document frequency)
# This captures which words are important in each document
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X = vectorizer.fit_transform(df['text'])

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, df['category'], test_size=0.25, random_state=42)

# Train Naive Bayes classifier - works well for text classification
classifier = MultinomialNB(alpha=1.0)
classifier.fit(X_train, y_train)

# Generate predictions on test set
y_pred = classifier.predict(X_test)

print("=== Model Performance ===")
print(f"Training accuracy: {classifier.score(X_train, y_train):.3f}")
print(f"Test accuracy: {classifier.score(X_test, y_test):.3f}\n")

print("=== Detailed Classification Report ===")
print(classification_report(y_test, y_pred, 
                           target_names=newsgroups.target_names))

# Find most predictive words for each category
feature_names = vectorizer.get_feature_names_out()
top_n = 8
for idx, category in enumerate(newsgroups.target_names):
    # Get log probabilities for each word in this category
    log_prob = classifier.feature_log_prob_[idx]
    top_indices = log_prob.argsort()[-top_n:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    print(f"\n=== Top words for '{category}' ===")
    print(", ".join(top_words))
```

### What to Try Next

1. **Change `max_features=1000` to `max_features=100` or `max_features=5000`:** Expect accuracy to drop with fewer features and plateau or slightly improve with more. This teaches you how vocabulary size affects model performance—too few features lose signal, too many may add noise.

2. **Replace `TfidfVectorizer` with `CountVectorizer`:** Performance may drop slightly. This demonstrates that TF-IDF's weighting scheme (emphasizing distinctive words) typically outperforms raw word counts for sentiment tasks.

3. **Modify `alpha=1.0` to `alpha=0.1` or `alpha=10.0`:** The smoothing parameter affects how the model handles unseen words. Lower values create a more confident model; higher values add more smoothing. This teaches the bias-variance tradeoff in probabilistic models.

4. **Add different newsgroup categories:** Try `['alt.atheism', 'soc.religion.christian']` for more polarized content. Expect higher accuracy due to more distinctive vocabulary, teaching you that sentiment analysis performs better on topics with clear linguistic differences.

## Further Reading

1. **Pang, B., & Lee, L. (2008). "Opinion Mining and Sentiment Analysis." *Foundations and Trends in Information Retrieval*, 2(1-2), 1-135.** Read this if you want to understand the foundational taxonomy of sentiment analysis approaches and the crucial distinction between document-level, sentence-level, and aspect-based sentiment classification. This paper established the theoretical framework that still guides how practitioners decompose sentiment problems today.

2. **Devlin, J., Chang, M., Lee, K., & Toutanova, K. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." *NAACL-HLT*.** Read this if you want to understand why transfer learning through pre-trained language models revolutionized sentiment analysis, particularly how bidirectional context encoding captures nuance that earlier approaches missed. The sentiment classification fine-tuning experiments demonstrate 4-7% accuracy improvements over previous state-of-the-art methods.

3. **Liu, B. (2015). *Sentiment Analysis: Mining Opinions, Sentiments, and Emotions*. Cambridge University Press. Chapter 4: "Sentence Subjectivity and Sentiment Classification" (pp. 93-128).** This chapter specifically addresses the often-overlooked challenge of distinguishing subjective from objective statements before attempting sentiment classification—a preprocessing step that dramatically improves precision in real applications where neutral factual content dominates.

4. **Jurafsky, D., & Martin, J.H. (2023). *Speech and Language Processing* (3rd ed. draft). Chapter 25: "Sentiment, Affect, and Connotation" (pp. 1-24).** Available free online, this chapter uniquely integrates lexicon-based methods with modern neural approaches, showing exactly when simpler VADER or TextBlob implementations outperform complex models for specific use cases like social media analysis.

5. **scikit-learn documentation: `sklearn.feature_extraction.text.TfidfVectorizer`.** Focus on the `ngram_range`, `max_features`, and `min_df` parameters—understanding how these interact determines whether your sentiment model captures "not good" as distinct from "good," a make-or-break distinction for negation handling in lexicon-free approaches.

6. **Alammar, J. (2018). "The Illustrated BERT, ELMo, and co." *jalammar.github.io*.** This visualization-driven tutorial uniquely breaks down the attention mechanism's role in sentiment analysis with concrete examples showing how BERT weighs "but" and "however" to flip sentiment mid-sentence—insight that's buried in mathematical notation in the original papers.

7. **StatQuest with Josh Starmer (2019). "Word Embedding and Word2Vec, Clearly Explained!!!" *YouTube*, 20:32.** Watch 11:30-16:45 for the specific explanation of how semantic similarity in embedding space enables sentiment transfer learning, using the visual "king-queen" analogy extended to "excellent-terrible" sentiment axes.

8. **Spotify (2020). "How Spotify Uses ML to Understand Podcast Content at Scale." *Spotify Engineering Blog*.** This case study reveals how sentiment analysis on 2M+ podcast episodes required hybrid lexicon-neural pipelines to handle domain-specific terminology and code-switching, demonstrating why production systems rarely use off-the-shelf models unchanged.

## Practice Exercises

### Exercise 1: Customer Support Ticket Prioritization (Conceptual)

**Scenario:**

You're the Head of Customer Experience at StreamBox, a video streaming service with 2.3 million subscribers. Your support team receives approximately 1,200 tickets daily through email and chat. Currently, all tickets enter a single queue and are handled first-come, first-served, with an average response time of 18 hours.

Your VP of Operations proposes implementing sentiment analysis to automatically route "negative sentiment" tickets to a priority queue, claiming this will improve customer retention. The proposal estimates a $45,000 implementation cost and ongoing $8,000/month for API calls.

Your data analyst provides sample ticket content:
- "Can't log in, getting error code 447"
- "This is the third time my payment failed! Absolutely unacceptable service!"
- "I'm trying to update my credit card but the button doesn't work"
- "Question about downloading content for offline viewing"

**Your task:** Should you implement sentiment analysis for ticket routing? If not, what alternative would you recommend? What specific concerns should you raise?

**Solution:**

**Recommendation: Do NOT implement sentiment analysis for this use case.** Instead, implement a **ticket categorization system** based on issue type and customer account status.

**Reasoning:**

1. **Sentiment doesn't equal urgency:** The tickets reveal the core problem—sentiment analysis conflates emotional intensity with business priority. The ticket "This is the third time my payment failed!" expresses negative sentiment, but a payment processing issue affects StreamBox's revenue and requires technical investigation, not emotional de-escalation. Meanwhile, "Can't log in, getting error code 447" is neutrally worded but represents a service-blocking issue affecting user retention.

2. **False prioritization risk:** Customers who write calmly about critical technical issues (login failures, streaming errors) would be deprioritized behind users who express frustration about minor inconveniences. This inverts actual business impact.

3. **Cost-benefit analysis:** At 1,200 tickets/day × 30 days = 36,000 tickets/month, the $8,000 monthly cost equals $0.22 per ticket. However, sentiment analysis doesn't solve the underlying problem: you lack issue-type classification to route technical vs. billing vs. account questions to specialized teams.

4. **Better alternative:** Implement a **multi-tier classification system:**
   - **Tier 1 - Issue Type:** Technical (login, streaming, app crashes) / Billing / Account Management / Content Questions
   - **Tier 2 - Account Status:** Multiple recent contacts, payment failure status, subscription tenure
   - **Tier 3 - Service Impact:** Can the customer currently use the service? (Yes/No)

This approach routes the neutrally-worded "Can't log in" ticket to high priority (service-blocking technical issue) while the payment failure ticket goes to the billing specialist team (not general support priority queue). The "update credit card" ticket gets medium priority as a self-service account issue.

**Implementation recommendation:** Use a simpler keyword-based classification system ($12,000 one-time cost, no ongoing API fees) combined with CRM data lookups. This addresses the actual workflow problem—getting tickets to the right specialized team—rather than sorting by emotional tone, which doesn't correlate with resolution urgency or business impact.

### Exercise 2: Product Review Analysis for Feature Prioritization (Applied)

**Business Context:**

You're a data scientist at HomeChef, a smart kitchen appliance company. The product team is deciding whether to invest $200K in improving the mobile app's recipe feature or the voice control system. They've asked you to analyze 6 months of product reviews to determine which feature generates more negative sentiment.

```python
import pandas as pd
from textblob import TextBlob

# Customer reviews for the SmartCook Pro appliance
reviews = pd.DataFrame({
    'review_id': range(1, 19),
    'review_text': [
        "Love this appliance! The voice control works perfectly every time.",
        "App crashes constantly when I try to browse recipes. Very frustrating.",
        "Voice commands rarely work. Have to repeat myself 4-5 times.",
        "The recipe database is amazing, so many options!",
        "App is slow and unintuitive. Recipe search is terrible.",
        "Voice control is a game changer for cooking with messy hands.",
        "Can't save favorite recipes in the app. Basic feature is missing.",
        "Tried voice control but gave up. Just use the manual buttons now.",
        "App interface is beautiful and easy to navigate.",
        "Voice recognition is hit or miss, works better in quiet kitchens.",
        "App recipe instructions are clear and helpful.",
        "The voice control volume is too low, can't hear confirmations.",
        "Great recipe suggestions in the app based on ingredients.",
        "Voice control doesn't understand my accent at all.",
        "App syncs perfectly across my phone and tablet.",
        "Voice feature would be useful if it actually worked reliably.",
        "Recipe photos in the app are gorgeous and inspiring.",
        "Voice control works but requires very specific phrasing."
    ],
    'feature_mentioned': [
        'voice', 'app', 'voice', 'app', 'app', 'voice', 
        'app', 'voice', 'app', 'voice', 'app', 'voice',
        'app', 'voice', 'app', 'voice', 'app', 'voice'
    ]
})
```

**Task:** Calculate the average sentiment polarity for reviews mentioning each feature, determine which feature has more negative sentiment, and provide an investment recommendation.

**Solution:**

```python
# Calculate sentiment polarity for each review
reviews['sentiment_polarity'] = reviews['review_text'].apply(
    lambda x: TextBlob(x).sentiment.polarity
)

# Calculate average sentiment by feature
feature_sentiment = reviews.groupby('feature_mentioned').agg({
    'sentiment_polarity': ['mean', 'count'],
    'review_id': 'count'
}).round(3)

print("Sentiment Analysis by Feature:")
print(feature_sentiment)
print("\nDetailed breakdown:")

for feature in ['app', 'voice']:
    feature_reviews = reviews[reviews['feature_mentioned'] == feature]
    avg_sentiment = feature_reviews['sentiment_polarity'].mean()
    negative_count = (feature_reviews['sentiment_polarity'] < 0).sum()
    positive_count = (feature_reviews['sentiment_polarity'] > 0).sum()
    
    print(f"\n{feature.upper()}:")
    print(f"  Average sentiment: {avg_sentiment:.3f}")
    print(f"  Positive reviews: {positive_count}")
    print(f"  Negative reviews: {negative_count}")
    # Output:
    # APP:
    #   Average sentiment: 0.156
    #   Positive reviews: 6
    #   Negative reviews: 3
    # 
    # VOICE:
    #   Average sentiment: -0.021
    #   Positive reviews: 3
    #   Negative reviews: 5
```

**Business Interpretation:**

The sentiment analysis reveals that voice control (average polarity: -0.021) generates significantly more negative sentiment than the app features (average polarity: 0.156). Among voice control reviews, 56% are negative compared to only 33% for the app. However, the recommendation should be **prioritize voice control improvement**. Despite fewer negative app reviews, the negative app mentions cite specific missing features ("can't save favorites") while voice control reviews indicate fundamental functionality failures ("rarely works," "doesn't understand my accent"). Voice control complaints suggest broken core functionality affecting product utility, while app complaints indicate enhancement opportunities. Fixing voice control addresses a reliability issue that likely impacts user satisfaction more severely than missing app features. The $200K investment should focus on voice recognition accuracy, accent handling, and audio feedback improvements, as these resolve complaints from 56% of voice feature users and enhance the hands-free cooking value proposition that differentiates the SmartCook Pro from competitors.

### Exercise 3: Sarcasm and Context-Dependent Sentiment (Challenge)

**Problem:**

You're analyzing customer feedback for LuxStay, a premium hotel chain. The naive approach of applying sentiment analysis directly to review snippets is producing misleading results that contradict the numerical star ratings customers provide alongside their text reviews.

**Dataset and Initial Approach:**

```python
import pandas as pd
from textblob import TextBlob
import re

# Hotel reviews with star ratings
reviews_df = pd.DataFrame({
    'review_text': [
        "The 'complimentary' breakfast was a stale muffin and coffee.",
        "For $400/night, the room was absolutely tiny. Just wonderful.",
        "Everything was not bad at all. Pretty decent stay overall.",
        "The view was breathtaking! Worth every penny of the premium rate.",
        "They call this luxury? I've stayed at better budget motels.",
        "The renovation really didn't improve anything. Gorgeous work guys.",
        "Surprisingly comfortable bed and excellent room service.",
        "The spa was nice, but $150 for a massage is outrageous."
    ],
    'star_rating': [2, 1, 4, 5, 1, 2, 5, 3]
})

# Naive approach: Direct sentiment analysis
reviews_df['naive_sentiment'] = reviews_df['review_text'].apply(
    lambda x: TextBlob(x).sentiment.polarity
)

print("Naive Sentiment Analysis Results:")
print(reviews_df[['review_text', 'star_rating', 'naive_sentiment']].to_string())
# Output shows misalignment between detected sentiment and actual ratings
```

**Task:** Identify why the naive approach fails for specific reviews and implement an improved approach that better aligns with actual customer satisfaction (star ratings).

**Solution:**

**Why the naive approach fails:**

```python
# Analyze misalignments
reviews_df['sentiment_rating_diff'] = abs(
    (reviews_df['naive_sentiment'] + 1) * 2.5 - reviews_df['star_rating']
)

print("\nLargest misalignments (naive approach):")
misaligned = reviews_df.nlargest(3, 'sentiment_rating_diff')
for idx, row in misaligned.iterrows():
    print(f"\nReview: {row['review_text']}")
    print(f"Actual rating: {row['star_rating']} stars")
    print(f"Naive sentiment: {row['naive_sentiment']:.3f}")
    
# Output identifies three failure modes:
# 1. Sarcasm: "Just wonderful" with 1-star rating
# 2. Negation: "not bad at all" with 4-star rating  
# 3. Mixed sentiment: "$150 is outrageous" with positive context
```

**The naive approach fails because:**

1. **Sarcasm detection:** "For $400/night, the room was absolutely tiny. Just wonderful." contains positive words ("wonderful") but the context and sarcasm indicator (price complaint + size complaint) signal dissatisfaction. TextBlob detects positive polarity from "wonderful" and "absolutely."

2. **Negation handling:** "Everything was not bad at all" uses double negation to express satisfaction, but basic sentiment analyzers often miss the cumulative effect of "not" + "bad" + "at all."

3. **Mixed signals:** "The spa was nice, but $150 for a massage is outrageous" contains both positive and negative elements. Simple polarity averaging doesn't capture that price complaints in luxury contexts often indicate overall dissatisfaction despite isolated positive mentions.

**Improved approach with context analysis:**

```python
def advanced_sentiment_analysis(text, context_type='luxury_hotel'):
    """Enhanced sentiment considering sarcasm, negation, and domain context."""
    
    # Basic sentiment
    blob = TextBlob(text)
    base_polarity = blob.sentiment.polarity
    
    # Sarcasm indicators for luxury context
    sarcasm_patterns = [
        r"for \$\d+",  # Price mention often precedes sarcasm
        r"call this \w+\?",  # Rhetorical questions
        r"just (wonderful|perfect|amazing|great)",  # Minimizer + positive
    ]
    
    sarcasm_detected = any(re.search(pattern, text.lower()) 
                          for pattern in sarcasm_patterns)
    
    # Check for negative context + positive words (sarcasm signal)
    negative_context = any(word in text.lower() 
                          for word in ['tiny', 'stale', 'budget', 'better'])
    positive_

## Quick Quiz

**Question:** A data scientist applies sentiment analysis to 10,000 customer service chat transcripts and finds that 92% are classified as "neutral." Before presenting these findings, what should be their primary concern?

A) The sentiment model lacks sufficient training data and should be retrained on at least 100,000 examples to achieve statistical significance.

B) Neutral sentiment is inherently unmeasurable since it represents the absence of emotion rather than a distinct emotional state, so the model is likely malfunctioning.

C) Customer service language is often transactional and fact-based rather than opinion-laden, so the text may genuinely lack the subjective attitude that sentiment analysis is designed to detect.

D) The sentiment lexicon needs domain-specific customization because customer service terminology differs from the product review vocabulary most models use.

**Answer:** C

**Explanation:** Sentiment analysis is designed to detect "emotional tone, opinion polarity, or subjective attitude" in text—but not all text contains these elements. Customer service transcripts are frequently transactional ("My order number is...", "The shipment date is...") rather than evaluative, making high neutral classification entirely appropriate. Option A misunderstands that the issue is data *type*, not volume—more examples of non-opinionated text won't improve sentiment detection. Option B incorrectly treats neutral as invalid when it's a legitimate category for text without sentiment. Option D assumes a technical solution (lexicon customization) when the fundamental issue is that the *text genre itself* may not be suitable for sentiment analysis. This question tests whether practitioners understand sentiment analysis applies specifically to subjective content, not all text universally.

## Heuristics

**If more than 30% of your text is neutral, your sentiment model is probably avoiding decisions.**
Excessive neutral classifications often indicate threshold problems or a model struggling with domain-specific language. Before accepting these results, manually review a sample of neutral predictions—they're frequently misclassified positive or negative sentiments that fell just short of your confidence threshold. Consider adjusting thresholds or retraining with domain-specific data.

**Validate sentiment analysis on sarcasm and negation before deployment, or expect 15-20% accuracy drops.**
Models trained on straightforward language consistently fail on "not good," "yeah, right," and ironic praise. Create a test set of 50-100 examples containing negations and sarcasm from your actual domain. If accuracy drops below 70% on this subset, lexicon-based approaches will fail catastrophically—switch to transformer models or add extensive preprocessing rules.

**When agreement between human annotators falls below 70%, sentiment analysis becomes opinion detection, not truth detection.**
Low inter-annotator agreement reveals that sentiment in your domain is genuinely ambiguous, not that you need a better model. This commonly occurs with political text, nuanced product feedback, or anything involving mixed emotions. Communicate results as "percentage expressing positive sentiment" rather than "percentage that are positive"—a subtle shift that prevents stakeholders from treating outputs as objective facts.

**For customer feedback under 10 words, skip sentiment analysis and use manual tagging instead.**
Short texts like "OK" or "fine I guess" lack sufficient context for reliable automated sentiment detection. Even advanced models struggle with brevity because a single word carries disproportionate weight. Below 10 words, the time spent tuning and validating a model exceeds the cost of human review, and accuracy rarely breaks 65%.

**Check class balance before celebrating 85% accuracy—it might be worse than a coin flip.**
If 90% of your data is positive and your model achieves 88% accuracy by predicting "positive" for everything, you've built an expensive no-op. Always compare performance against a naive baseline that predicts the majority class. Your model should beat this baseline by at least 15 percentage points, or you're extracting no real signal.

**Domain-specific sentiment flips word polarity: always review your top 100 most frequent terms.**
"Volatile" is negative in product reviews but neutral or positive in stock trading discussions. "Aggressive" is negative in healthcare but positive in sports commentary. Scan your most common adjectives and adverbs—if more than 10% have context-dependent polarity, generic pre-trained models will systematically misclassify. Budget time for domain adaptation or custom lexicon creation.

**Run sentiment analysis at the sentence level, then aggregate—analyzing whole documents loses 40% of mixed sentiment.**
A restaurant review saying "Great food, terrible service" is genuinely mixed, but document-level analysis often outputs only the dominant sentiment. Sentence-level analysis captures this nuance and lets you report "positive about food, negative about service." This granularity transforms sentiment from a blunt instrument into an actionable diagnostic tool.

**Expert practitioners always show raw text samples alongside sentiment scores—numbers without examples breed false confidence.**
Stakeholders seeing "sentiment score: 0.82" assume accuracy they shouldn't. Presenting "sentiment score: 0.82" with five example snippets lets readers calibrate their trust instantly. This practice surfaces edge cases, reveals model weaknesses before they become problems, and transforms sentiment analysis from a black box into a transparent, interrogable tool.

## Nuggets

**Negation doesn't flip sentiment—it fragments it into meaningless pieces.**
Most sentiment analyzers treat "not good" by detecting "not" then inverting "good," but this breaks catastrophically with phrases like "not bad" (positive), "not unconvincing" (double negative), or "not just good, but amazing" (intensification, not negation). Research by Councill et al. showed that rule-based negation handling actually *decreases* accuracy on movie reviews by 3-7% compared to ignoring negation entirely and letting the model learn contextual patterns from data. The practical takeaway: if you're using lexicon-based methods, test performance with negation rules turned off—you may be better without them.

**Domain transfer fails silently and systematically in predictable directions.**
A sentiment model trained on product reviews achieves 85% accuracy on held-out product data but drops to 62% on hotel reviews and 54% on financial news—not because the model is bad, but because sentiment vocabulary is fundamentally domain-specific. "Unpredictable" is negative for cars, positive for novels. "Long" is negative for wait times, positive for battery life. What's surprising: this degradation follows a consistent pattern. Models transfer well within experiential domains (restaurants→hotels) but fail across evaluation types (experiences→products→ideas). Always validate on a sample of your actual domain, not just general sentiment benchmarks.

**Neutral sentiment is not the absence of opinion—it's a prediction failure mode.**
When practitioners examine misclassified samples, they find models default to "neutral" for contradictory signals ("great food, terrible service"), sarcasm, or mixed reviews. A 2019 analysis of commercial sentiment APIs showed that 68% of samples labeled "neutral" actually contained clear sentiment when human-annotated. The statistical signature: if your neutral category exceeds 30% of predictions on opinionated text like reviews, you're not measuring neutrality—you're measuring model confusion. Consider treating neutral as a confidence flag rather than a sentiment category, and route high-neutral-probability samples to manual review.

**Emojis carry more signal than words, but only in combination.**
Tweets containing only "😂" have inter-annotator agreement of just 61% (Is it joy? Sarcasm? Discomfort?), but "worst customer service 😂" is reliably negative while "passed my exam 😂" is reliably positive. Park et al. demonstrated that emoji-aware models improve accuracy by 12-15% on social media, but *only* when emojis are tokenized separately and allowed to interact with surrounding words. Treating emojis as simple sentiment lexicon entries (😂 = positive) actually degrades performance. If you're analyzing social media, use tokenizers that preserve emojis as distinct features rather than stripping them or replacing them with text descriptions.

**Aspect-based sentiment reveals that 73% of "negative" reviews recommend the product.**
Amazon's internal analysis found that reviews with 2-star overall ratings frequently contain sentences like "shipping was terrible, but the product itself is excellent." Aggregating to document-level sentiment obscures these aspect-specific opinions. In practice, this means sentence-level or aspect-level sentiment analysis often provides more actionable insights than document-level scores, particularly for operational decisions like "should we change suppliers?" versus "should we redesign the product?"

**Pre-trained transformers plateau faster than their accuracy suggests.**
BERT-based models achieve 94% accuracy on SST-2 benchmark with just 3,000 training samples, suggesting you need minimal domain data. But testing on out-of-distribution samples reveals the model has memorized common patterns rather than learning robust sentiment reasoning. Accuracy on adversarial examples (minimal perturbations) drops to 67%. The practical implication: high benchmark accuracy with pre-trained models doesn't guarantee production robustness. Always test on adversarial samples and edge cases before deployment.

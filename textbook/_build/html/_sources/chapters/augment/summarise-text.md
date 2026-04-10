# Summarise Text


![](../../_static/figures/summarise-text_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The biggest mistake teams make with text summarisation is treating it as a pure compression problem when it's actually about information prioritisation. You need to explicitly define what matters to your use case—whether that's extracting action items, preserving technical details, or maintaining narrative flow—because a generic 20% summary will almost always discard something critical. Always validate your summaries against domain experts before automating at scale, especially in regulated industries where missing a single compliance clause can be catastrophic.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Summarise Text automatically condenses long documents into short versions that capture the essential points.

**When to use it:** You're drowning in reports, customer feedback, research papers, or meeting transcripts and need to extract key insights without reading everything word-for-word.

**What you get back:** A shortened version of each document that you can scan quickly to decide what deserves deeper attention or to share with stakeholders who need the headline story.

**At a Glance**

| | |
|---|---|
| **Difficulty** | Easy to Moderate |
| **Typical runtime** | Seconds to minutes for hundreds of documents |
| **What you bring** | Text documents of any length (emails, reports, articles, transcripts) |
| **What you get** | Condensed versions highlighting key information, typically 10-30% of original length |
| **Heuristix bucket** | Augment — AI & Language Intelligence |

**Summaries are interpretations, not truth—always verify that critical details haven't been lost or distorted before making high-stakes decisions.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify which business scenarios justify text summarization over manual reading, including triage of customer feedback, executive briefings from long reports, and monitoring high-volume content streams.
- Interpret summarization outputs by distinguishing between extractive snippets and abstractive rewrites, and explain to stakeholders which information was preserved, compressed, or potentially lost.
- Decide whether a generated summary meets quality thresholds for a specific use case by evaluating it against completeness, accuracy, and readability criteria before deploying it in workflows.

**After reading this chapter, a data scientist will be able to:**

- Implement both extractive and abstractive summarization pipelines, including preprocessing steps for different document types, handling of multi-document inputs, and strategies for extremely long texts that exceed model context windows.
- Tune critical parameters such as summary length ratios, temperature settings for generation models, and extractive sentence selection thresholds while understanding their impact on coverage versus conciseness trade-offs.
- Validate summarization quality using automated metrics (ROUGE, BERTScore) and human evaluation protocols, and diagnose common failure modes including factual hallucinations, loss of critical details, and poor coherence in abstractive outputs.

## Overview

**Summarise Text** is a natural language processing (NLP) technique that automatically generates concise, coherent representations of longer documents while preserving their essential meaning and key information. The core purpose is to reduce cognitive load on human readers and enable scalable information extraction from large text corpora that would be impractical to read manually. This technique belongs to the family of **text generation** and **sequence-to-sequence transformation** methods, encompassing both extractive approaches (selecting salient sentences from source text) and abstractive approaches (generating novel text that captures document meaning).

## When to Use This

**Use this when:**

- **Processing high-volume customer feedback** — When your organisation receives thousands of support tickets, reviews, or survey responses daily and needs to quickly identify themes and sentiment without manual reading
- **Condensing research reports for executive briefings** — When lengthy technical documents, market research, or regulatory filings must be distilled into actionable summaries for time-constrained decision makers
- **Creating document previews for search systems** — When building internal knowledge management systems that need to display meaningful snippets to help users assess document relevance before opening
- **Automating meeting notes and call transcriptions** — When sales calls, customer service interactions, or internal meetings are recorded and require consistent, structured summaries for CRM integration
- **Monitoring news and social media at scale** — When tracking brand mentions, competitor activity, or market events across thousands of daily articles requires rapid digestion of content
- **Standardising medical or legal case summaries** — When clinical notes, legal briefs, or insurance claims need consistent summarisation for downstream processing or human review

**Do NOT use this when:**

- **Exact wording carries legal or regulatory significance** — Summarisation necessarily loses information; for contracts, compliance documents, or evidence, always preserve original text alongside any summary
- **Documents are already concise** — Text shorter than 100-150 words typically cannot be meaningfully condensed; summarisation may introduce distortion rather than value
- **Quantitative precision is paramount** — Numerical facts, dates, and figures may be altered or omitted; use entity extraction instead when precise data points matter more than narrative understanding
- **Source attribution must be preserved** — Abstractive summarisation generates new text that cannot be directly traced to specific source passages; use extractive methods or quotation systems for audit requirements

## Questions This Answers

### Information Overload and Knowledge Extraction

**How can we quickly understand what's in these 400 customer feedback forms without reading every single one?**

**What are the main themes coming out of this 80-page market research report our consultants delivered?**

**Can someone give me the key points from all the earnings call transcripts our competitors published this quarter?**

**We have 10,000 support tickets from last month — what are customers actually complaining about?**

**What did our legal team's 50-page contract review actually conclude, in plain English?**

### Content Production and Communication Efficiency

**How do we turn these technical product specifications into executive summaries our sales team can actually use?**

**Can we automatically generate brief versions of our weekly status reports for the leadership team?**

**What's the fastest way to create meeting notes from these hour-long stakeholder session transcripts?**

**How do we produce engaging social media snippets from our long-form blog content without hiring more writers?**

**Is there a way to give our customers article previews that help them decide what's worth reading?**

### Decision Support and Competitive Intelligence

**Which three vendor proposals should we focus on reviewing in detail out of the 15 we received?**

**What are the critical action items buried in this 30-page audit report that we need to address immediately?**

**How can we monitor what's being said about our brand across thousands of online reviews without a team of analysts?**

**What should I know before going into this client meeting based on our entire email history with them?**

## How It Works

Imagine you're Sarah, a journalist who needs to brief her editor on a 50-page government report before the 9am meeting—it's now 8:30am. She can't read every page, so she uses a highlighter to mark the most important sentences: the core findings, key statistics, and main recommendations. Then she either copies those exact highlighted sentences into an email (the quick approach), or she rewrites them in her own words to make them flow better (the thoughtful approach). Either way, her editor gets the essence of that 50-page document in just five paragraphs. Text summarisation does exactly this, but automatically, and at a scale where it can process thousands of reports in seconds.

```
ORIGINAL DOCUMENT (500 words)                SUMMARY (50 words)
┌─────────────────────────────────┐         ┌──────────────────┐
│ Para 1: Background context and  │         │                  │
│         historical details...    │    ┌───→│ Key finding from │
│                                  │    │    │ Para 3 (핵심)    │
│ Para 2: Minor supporting point   │    │    │                  │
│         with examples...         │    │    │ Main conclusion  │
│                                  │    │    │ from Para 4 (핵심)│
│ Para 3: MAIN FINDING - critical  │────┘    │                  │
│         insight about...     (핵심)│         │ Action item from │
│                                  │    ┌────→│ Para 5 (핵심)    │
│ Para 4: CONCLUSION - primary     │────┘    │                  │
│         outcome...           (핵심)│         └──────────────────┘
│                                  │              ↑
│ Para 5: ACTION REQUIRED - next   │───────┐      │
│         steps...             (핵심)│       └──────┘
│                                  │
│ Para 6: Tangential discussion... │    EXTRACTIVE: Select key
└─────────────────────────────────┘    sentences directly
                                       
                                       ABSTRACTIVE: Rewrite in
                                       new words, same meaning
```

**Step 1: Break the document into units.** The system first divides the text into manageable pieces—usually sentences, but sometimes paragraphs or phrases. Think of this as separating a long scroll into individual index cards, each containing one complete thought.

**Step 2: Score each unit for importance.** Now the algorithm examines every card and assigns it a relevance score. In extractive approaches, it might count how many important keywords appear, or how similar the sentence is to the overall document theme. In abstractive approaches, it identifies which concepts carry the most semantic weight—which ideas would leave the biggest hole if removed.

**Step 3: Select or generate the summary content.** For extractive summarisation, the system simply picks the highest-scoring sentences, like choosing the top 10% of cards from our stack. For abstractive summarisation, it generates entirely new sentences that capture the meaning of high-scoring concepts, similar to how you'd explain a complex article to a friend in your own words rather than reading quotes.

**Step 4: Assemble and polish the output.** The selected or generated content gets arranged in a logical order—often following the original document's sequence—and transition words may be added to improve flow. The result is a shorter text that preserves the document's core message while eliminating redundancy and low-value details.

**The key insight:** Summarisation works because information in documents isn't uniformly distributed—a small fraction of sentences carry most of the meaning, and identifying those high-signal portions through statistical or semantic analysis lets us safely discard the rest without losing what matters.

## The Intuition

Imagine you are a newspaper editor who must condense a 3,000-word investigative report into a 150-word summary for the front page. You would not simply select random sentences or truncate at the 150th word. Instead, you would read the entire piece, identify the most important claims, understand the causal relationships between events, and then *rewrite* a condensed version that preserves what matters while eliminating redundancy and tangential detail. This is precisely what abstractive text summarisation attempts to automate.

The challenge lies in the fact that "importance" is context-dependent and subjective. A sentence about quarterly revenue might be critical in an earnings report but irrelevant in a product announcement. Effective summarisation therefore requires the system to model document structure, identify topical salience, and understand which information serves the likely reader's purpose. Modern approaches accomplish this through neural architectures that learn these salience patterns from large corpora of document-summary pairs, developing implicit representations of what constitutes "summary-worthy" content.

There exists a fundamental tension between **fidelity** and **compression**. A perfect summary would preserve all meaning while using fewer words—but meaning is not infinitely compressible. Every summarisation involves information loss, and the art lies in losing the *right* information. Extractive methods sidestep some of this difficulty by constraining outputs to sentences present in the source, guaranteeing faithfulness at the cost of fluency and compression ratio. Abstractive methods gain expressive freedom but risk **hallucination**—generating plausible-sounding content not supported by the source document. Understanding this tradeoff is essential for appropriate application of summarisation in business contexts.

## The Mathematics

### Formal Problem Setup

Let $D = (w_1, w_2, \ldots, w_n)$ denote a source document as a sequence of $n$ tokens drawn from vocabulary $\mathcal{V}$. Our objective is to generate a summary $S = (s_1, s_2, \ldots, s_m)$ where $m \ll n$ and $S$ maximises some measure of content preservation while satisfying length constraints.

We distinguish two fundamental paradigms:

**Extractive Summarisation:** Select a subset of sentences $\{e_1, e_2, \ldots, e_k\}$ from the document's sentence set $\mathcal{E}(D)$ such that:

$$
S^* = \arg\max_{S \subseteq \mathcal{E}(D)} \sum_{e \in S} \text{Importance}(e \mid D) - \lambda \cdot \text{Redundancy}(S)
$$

subject to $|S| \leq L$ for some length budget $L$.

**Abstractive Summarisation:** Generate novel text by modelling the conditional probability:

$$
P(S \mid D) = \prod_{t=1}^{m} P(s_t \mid s_1, \ldots, s_{t-1}, D)
$$

### Extractive Methods: Sentence Scoring

The classical approach scores sentences independently then selects top-ranked ones. For a sentence $e_i$ containing tokens $(w_{i,1}, \ldots, w_{i,k})$, common scoring functions include:

**TF-IDF Centroid Method:**

$$
\text{score}(e_i) = \cos(\mathbf{v}_{e_i}, \mathbf{v}_D)
$$

where $\mathbf{v}_{e_i}$ and $\mathbf{v}_D$ are TF-IDF weighted vector representations of the sentence and document respectively.

**TextRank (Graph-Based):** Construct a graph $G = (\mathcal{E}, W)$ where vertices are sentences and edge weights $w_{ij}$ measure sentence similarity:

$$
w_{ij} = \frac{|\{w : w \in e_i \cap e_j\}|}{\log|e_i| + \log|e_j|}
$$

Sentence importance is then the stationary distribution of the random walk:

$$
\text{TR}(e_i) = (1 - d) + d \sum_{e_j \in \text{In}(e_i)} \frac{w_{ji}}{\sum_{e_k \in \text{Out}(e_j)} w_{jk}} \cdot \text{TR}(e_j)
$$

where $d \in [0,1]$ is the damping factor (typically 0.85).

### Abstractive Methods: Sequence-to-Sequence Models

Modern abstractive summarisation employs the **encoder-decoder** architecture with attention. Let $\mathbf{H} = (\mathbf{h}_1, \ldots, \mathbf{h}_n)$ denote encoder hidden states for the source document.

**Attention Mechanism:**

At each decoder timestep $t$, attention weights $\alpha_t$ are computed:

$$
\alpha_{t,i} = \frac{\exp(e_{t,i})}{\sum_{j=1}^{n} \exp(e_{t,j})}
$$

where the alignment scores are:

$$
e_{t,i} = \mathbf{v}^T \tanh(\mathbf{W}_h \mathbf{h}_i + \mathbf{W}_s \mathbf{s}_t + \mathbf{b})
$$

The context vector is then:

$$
\mathbf{c}_t = \sum_{i=1}^{n} \alpha_{t,i} \mathbf{h}_i
$$

**Transformer Architecture:**

Self-attention computes:

$$
\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}
$$

where $\mathbf{Q}, \mathbf{K}, \mathbf{V} \in \mathbb{R}^{n \times d_k}$ are query, key, and value projections and $d_k$ is the key dimension.

### Objective Function and Training

The standard training objective is cross-entropy loss against reference summaries:

$$
\mathcal{L}(\theta) = -\sum_{t=1}^{m} \log P_\theta(s_t^* \mid s_1^*, \ldots, s_{t-1}^*, D)
$$

This suffers from **exposure bias** since the model trains on ground-truth prefixes but must decode from its own predictions at inference. Reinforcement learning fine-tuning addresses this by directly optimising evaluation metrics:

$$
\mathcal{L}_{RL}(\theta) = -\mathbb{E}_{S \sim P_\theta}[r(S)]
$$

where $r(S)$ is typically ROUGE score against reference summaries.

### Evaluation Metrics

**ROUGE-N** (Recall-Oriented Understudy for Gisting Evaluation) measures n-gram overlap:

$$
\text{ROUGE-N} = \frac{\sum_{S \in \text{Ref}} \sum_{\text{gram}_n \in S} \text{Count}_{\text{match}}(\text{gram}_n)}{\sum_{S \in \text{Ref}} \sum_{\text{gram}_n \in S} \text{Count}(\text{gram}_n)}
$$

**ROUGE-L** uses longest common subsequence:

$$
\text{ROUGE-L} = \frac{(1 + \beta^2) \cdot R_{lcs} \cdot P_{lcs}}{R_{lcs} + \beta^2 \cdot P_{lcs}}
$$

where $R_{lcs} = \frac{\text{LCS}(X, Y)}{m}$ and $P_{lcs} = \frac{\text{LCS}(X, Y)}{n}$.

### Assumptions and Limitations

1. **Single-document focus**: The mathematics above assumes a single document; multi-document summarisation requires additional aggregation mechanisms
2. **Reference summary quality**: Training assumes reference summaries capture optimal content selection
3. **Length independence**: Standard models do not explicitly model compression ratio requirements
4. **Faithfulness**: Cross-entropy training does not penalise factual inconsistency with source

## Understanding the Mathematics

### Token Embedding Representation

**The equation:**
$$\mathbf{e}_i = \mathbf{W}_e \cdot \text{onehot}(w_i)$$

**Read it aloud:**
"The embedding vector for token i equals the embedding weight matrix multiplied by the one-hot encoded representation of word i."

**What each symbol means:**
- $\mathbf{e}_i$ = dense vector representation of the i-th word (typically 300-768 numbers)
- $\mathbf{W}_e$ = learned embedding matrix storing vector representations for all vocabulary words
- $\text{onehot}(w_i)$ = binary vector with 1 at position matching word $w_i$, zeros elsewhere
- $w_i$ = the actual word token at position i in the text

**A concrete numerical example:**
Suppose we're summarizing customer feedback. The word "excellent" is the 5,000th word in our 10,000-word vocabulary. Its one-hot vector is all zeros except position 5,000 (which is 1). Our embedding matrix $\mathbf{W}_e$ has 10,000 rows and 512 columns. When we multiply, we extract row 5,000 from $\mathbf{W}_e$, giving us a 512-dimensional vector like [0.23, -0.41, 0.67, ..., 0.15]. This dense vector now represents "excellent" in a way that captures its semantic meaning.

**Why this equation matters:**
Without converting words to dense vectors, the model cannot measure semantic similarity or understand that "excellent" and "outstanding" mean similar things—it would treat all words as equally different.

### Attention Score Calculation

**The equation:**
$$\text{score}(h_i, h_j) = \frac{(\mathbf{W}_Q h_i)^T (\mathbf{W}_K h_j)}{\sqrt{d_k}}$$

**Read it aloud:**
"The attention score between hidden state i and hidden state j equals the dot product of the query transformation of state i with the key transformation of state j, divided by the square root of the key dimension."

**What each symbol means:**
- $\text{score}(h_i, h_j)$ = importance of word j when processing word i
- $h_i, h_j$ = hidden state vectors for words at positions i and j
- $\mathbf{W}_Q$ = learned query weight matrix
- $\mathbf{W}_K$ = learned key weight matrix
- $d_k$ = dimensionality of key vectors (typically 64)
- $\sqrt{d_k}$ = scaling factor to prevent extremely large scores

**A concrete numerical example:**
We're generating a summary and deciding which words matter most. Word $h_i$ is "customer" and word $h_j$ is "satisfaction." After applying transformations, $\mathbf{W}_Q h_i$ gives us [2.1, 3.4, -1.2] and $\mathbf{W}_K h_j$ gives us [1.8, 3.1, -0.9]. The dot product is $2.1(1.8) + 3.4(3.1) + (-1.2)(-0.9) = 3.78 + 10.54 + 1.08 = 15.40$. With $d_k = 64$, we divide: $15.40 / 8 = 1.925$. This high score tells the model that "satisfaction" is relevant when processing "customer."

**Why this equation matters:**
Attention scores determine which parts of the source document the model focuses on when generating each summary word—without this, the model would treat all input words as equally important, producing incoherent summaries.

### Softmax Normalization

**The equation:**
$$\alpha_{ij} = \frac{\exp(\text{score}(h_i, h_j))}{\sum_{k=1}^{n} \exp(\text{score}(h_i, h_k))}$$

**Read it aloud:**
"The attention weight from word i to word j equals the exponential of their score divided by the sum of exponentials of all scores from word i to every word in the sequence."

**What each symbol means:**
- $\alpha_{ij}$ = normalized attention weight (between 0 and 1)
- $\exp(\cdot)$ = exponential function (e raised to the power)
- $n$ = total number of words in the input document
- $\sum_{k=1}^{n}$ = sum over all positions k from 1 to n

**A concrete numerical example:**
While generating a summary, word i has raw attention scores to three context words: 1.925, 0.6, and -0.3. We compute $\exp(1.925) = 6.86$, $\exp(0.6) = 1.82$, $\exp(-0.3) = 0.74$. The sum is $6.86 + 1.82 + 0.74 = 9.42$. So $\alpha_{i1} = 6.86/9.42 = 0.73$, $\alpha_{i2} = 1.82/9.42 = 0.19$, $\alpha_{i3} = 0.74/9.42 = 0.08$. These sum to 1.0 and tell us to focus 73% on the first word, 19% on the second, 8% on the third.

**Why this equation matters:**
Softmax converts arbitrary scores into valid probabilities that sum to one, enabling the model to create weighted combinations of information rather than making hard binary choices about what to include.

### The Big Picture

The mathematics of text summarization is fundamentally trying to learn which information deserves attention and how to compress it without losing meaning. Embeddings convert discrete words into continuous spaces where semantic similarity becomes measurable. Attention mechanisms then solve the core challenge: when generating each summary token, the model must selectively focus on relevant portions of a potentially very long source document while ignoring irrelevant details. We use this particular mathematical approach—transformations plus dot products plus softmax—because it's differentiable (trainable via backpropagation), computationally parallelizable (unlike sequential approaches), and naturally captures long-range dependencies between words that might be hundreds of tokens apart. In essence, the mathematics teaches a neural network to read like a human analyst: scanning the entire document, recognizing what's important, and expressing those key points concisely.

## Python Implementation

```python
# Summarise Text Implementation Examples
# Demonstrates both extractive and abstractive approaches

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# =============================================================================
# Example 1: Extractive Summarisation using TextRank
# =============================================================================

def textrank_summarise(text, num_sentences=3, damping=0.85, max_iter=100):
    """
    Extractive summarisation using TextRank algorithm.
    
    Parameters:
    -----------
    text : str
        Source document to summarise
    num_sentences : int
        Number of sentences to extract
    damping : float
        Random walk damping factor (0-1)
    max_iter : int
        Maximum iterations for PageRank convergence
        
    Returns:
    --------
    str : Extracted summary
    """
    # Split document into sentences (simplified; production use nltk.sent_tokenize)
    sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') 
                 if len(s.strip()) > 10]
    
    if len(sentences) <= num_sentences:
        return text
    
    # Create TF-IDF matrix for sentence similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # Build graph and compute PageRank scores
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph, alpha=damping, max_iter=max_iter)
    
    # Rank sentences by score
    ranked_indices = sorted(scores, key=scores.get, reverse=True)
    
    # Select top sentences, maintaining original order
    selected_indices = sorted(ranked_indices[:num_sentences])
    summary_sentences = [sentences[i] for i in selected_indices]
    
    return '. '.join(summary_sentences) + '.'


# Sample document for demonstration
sample_document = """
Artificial intelligence has transformed numerous industries over the past decade.
Machine learning algorithms now power recommendation systems, fraud detection,
and autonomous vehicles. The healthcare sector has seen particularly significant
advances, with AI systems achieving human-level performance in medical imaging
diagnosis. However, concerns about algorithmic bias and job displacement remain
significant challenges. Regulatory frameworks are struggling to keep pace with
technological advancement. Many experts advocate for responsible AI development
practices that prioritise transparency and fairness. The economic impact of AI
adoption is projected to add trillions of dollars to global GDP by 2030.
Investment in AI research continues to accelerate, with both public and private
sectors committing substantial resources. Education systems worldwide are adapting
curricula to prepare workers for an AI-augmented economy.
"""

# Run extractive summarisation
extractive_summary = textrank_summarise(sample_document, num_sentences=3)
print("=== Extractive Summary (TextRank) ===")
print(extractive_summary)
print(f"\nOriginal length: {len(sample_document.split())} words")
print(f"Summary length: {len(extractive_summary.split())} words")


# =============================================================================
# Example 2: Abstractive Summarisation using Hugging Face Transformers
# =============================================================================

print("\n" + "="*60)
print("=== Abstractive Summary (Transformer Model) ===")

# Note: Requires transformers library (pip install transformers)
try:
    from transformers import pipeline
    
    # Initialize summarisation pipeline with a pre-trained model
    summariser = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",  # Production-quality summarisation model
        device=-1  # CPU; use 0 for GPU
    )
    
    # Configure summarisation parameters
    abstractive_summary = summariser(
        sample_document,
        max_length=80,      # Maximum tokens in summary
        min_length=30,      # Minimum tokens in summary
        do_sample=False,    # Use greedy decoding for deterministic output
        truncation=True     # Handle documents exceeding model's max input length
    )[0]['summary_text']
    
    print(abstractive_summary)
    print(f"\nSummary length: {len(abstractive_summary.split())} words")

except ImportError:
    print("Install transformers library for abstractive summarisation:")
    print("pip install transformers torch")


# =============================================================================
# Example 3: Batch Processing Multiple Documents
# =============================================================================

print("\n" + "="*60)
print("=== Batch Processing Example ===")

# Create sample dataset of customer feedback
feedback_data = pd.DataFrame({
    'ticket_id': [1001, 1002, 1003],
    'feedback': [
        "I've been a customer for five years and this is the worst experience I've had. The delivery was delayed by two weeks with no communication. When I finally received the package it was damaged. Customer service took three days to respond and offered no compensation. Very disappointed.",
        "Excellent product quality and fast shipping. The item arrived well-packaged and exactly as described. Will definitely order again. The new website interface is also much easier to navigate than before.",
        "Mixed feelings about my purchase. The product itself works well but the instruction manual was confusing. Had to watch YouTube tutorials to set it up. Price was competitive though."
    ]
})

# Apply extractive summarisation to each feedback entry
feedback_data['summary'] = feedback_data['feedback'].apply(
    lambda x: textrank_summarise(x, num_sentences=2)
)

# Display results
print(feedback_data[['ticket_id', 'summary']].to_string(index=False))
```


## Visualisations

![](../../_static/figures/summarise-text_fig1.png)

![](../../_static/figures/summarise-text_fig2.png)

## Using This in Heuristix

### Input Requirements

The **Summarise Text** node accepts a dataset with a text column containing the documents to be summarised.

| Input Column | Type | Description |
|-------------|------|-------------|
| `text_column` | String/Text | The source document(s) to summarise. Each row represents one document. |
| `id_column` (optional) | String/Integer | Unique identifier for each document, passed through

## Config Recipes

### Recipe 1: Quick Exploration

**When to use:** Initial document triage when you have hundreds of articles, reports, or emails and need to understand what's worth reading in detail.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `extractive` | No model loading; uses sentence ranking only |
| `num_sentences` | `3` | Bare minimum for coherence; reads in ~10 seconds |
| `model` | `None` | Skips transformer initialization |
| `sentence_scorer` | `textrank` | Fast graph-based ranking; no GPU needed |
| `batch_size` | `32` | Irrelevant for extractive, but set high if switching |

**What you get:** Three sentences pulled verbatim from the source, readable in seconds, giving you the gist to decide if full reading is warranted.

**Trade-off:** No paraphrasing or compression; may include redundant information or miss narrative flow that abstractive methods would smooth out.

---

### Recipe 2: Production Report Generation

**When to use:** Automated weekly executive summaries from company documentation where accuracy, consistency, and auditability matter more than speed.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `abstractive` | Generates fluent, compressed text |
| `model` | `facebook/bart-large-cnn` | State-of-art on CNN/DailyMail; well-validated |
| `max_length` | `150` | Standard executive summary length |
| `min_length` | `50` | Prevents degenerate short outputs |
| `length_penalty` | `2.0` | Strongly rewards longer outputs within max_length |
| `num_beams` | `4` | Beam search for quality over speed |
| `temperature` | `1.0` | Default; production needs determinism not creativity |
| `no_repeat_ngram_size` | `3` | Prevents awkward repetition in output |

**What you get:** Fluent, human-readable paragraph that rephrases key points, suitable for direct inclusion in stakeholder communications.

**Trade-off:** 10-20x slower than extractive; requires GPU for reasonable throughput; occasional hallucination of minor details not in source.

---

### Recipe 3: Legal/Compliance Summarization

**When to use:** Summarizing contracts, regulations, or medical documents where every fact must be verifiable and directly traceable to source text.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `extractive` | Sentences are verbatim; no risk of hallucination |
| `num_sentences` | `10` | Higher coverage for complex documents |
| `sentence_scorer` | `embeddings` | Semantic understanding beats keyword matching |
| `embedding_model` | `sentence-transformers/all-mpnet-base-v2` | Best balance of quality and speed for semantic tasks |
| `diversity_penalty` | `0.7` | Ensures coverage of distinct clauses, not repetition |
| `preserve_order` | `True` | Maintains logical flow from source document |

**What you get:** Ten sentences in original sequence, each directly quotable with line references, covering distinct sections of the document.

**Trade-off:** Longer than abstractive equivalents; may feel choppy since sentences aren't rewritten to connect smoothly.

---

### Recipe 4: Meeting Notes from Transcripts

**When to use:** Converting spoken conversation transcripts (sales calls, user interviews, team standups) into action items and decisions.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `method` | `abstractive` | Cleans up disfluencies and repetition inherent in speech |
| `model` | `google/pegasus-multi_news` | Trained on multi-document input; handles dialogue turns |
| `max_length` | `100` | Tight summaries for actionability |
| `repetition_penalty` | `1.5` | Spoken text has high repetition; aggressively suppress |
| `prompt` | `"Key decisions and action items:"` | Steers model toward actionable extraction |

**What you get:** Clean bullet-point-ready summary focusing on decisions and tasks, stripping conversational filler.

**Trade-off:** May miss important context or rationale that was discussed but not explicitly stated as a decision.

## Business Applications

**Financial Services**

A multinational investment bank processes over 50,000 equity research reports, earnings call transcripts, and regulatory filings each quarter that analysts must review to inform trading decisions. Summarise Text automatically condenses each 40-page analyst report into a structured 2-page brief highlighting price targets, risk factors, and catalysts, with separate summaries for different trading desks. This reduced analyst reading time by 67% while maintaining decision quality, enabling the bank to cover 40% more securities with the same headcount and capture an estimated $12M in additional alpha annually.

**Retail & E-commerce**

An e-commerce marketplace with 8M product listings faces customer confusion when sellers upload verbose, poorly-structured product descriptions that bury key specifications. Automated abstractive summarisation generates clean, scannable product summaries that highlight dimensions, materials, compatibility, and unique features in a consistent format across all categories. A/B testing showed that enhanced product pages lifted conversion rates from 2.3% to 3.7% and reduced returns by 18% as customers better understood what they were purchasing before checkout.

**Healthcare**

A large US hospital network struggles with physician burnout partly driven by documentation burden—clinicians spend 2–3 hours per shift writing patient encounter notes. Clinical summarisation models trained on medical terminology automatically generate draft progress notes from patient conversations (captured via ambient listening), lab results, and imaging reports, requiring only physician review and sign-off. This cut documentation time by 45 minutes per shift, allowing physicians to see two additional patients daily while improving note completeness for downstream billing and care coordination.

**Insurance**

A commercial insurance underwriter receives 3,000+ liability claims monthly, each accompanied by police reports, witness statements, adjuster notes, and correspondence spanning 20–100 pages. Summarise Text extracts and synthesises the incident timeline, involved parties, damages claimed, and coverage questions into a 1-page executive summary for each claim. Processing time per claim dropped from 4.5 days to 6 hours, enabling the carrier to reduce loss adjustment expense by $2.8M annually and settle straightforward claims 73% faster.

**Manufacturing**

A global automotive parts manufacturer conducts daily quality inspections across 14 factories, generating thousands of defect reports, maintenance logs, and shift handover documents. Multi-document summarisation aggregates insights across facilities to produce daily executive briefings that surface recurring failure modes, supplier issues, and process deviations. Plant managers now identify systemic quality problems 8× faster, reducing warranty claims by 22% within nine months of implementation.

**Logistics & Supply Chain**

A freight forwarding company managing 200,000 annual shipments receives constant updates via email, SMS, and partner portals about delays, customs holds, route changes, and delivery exceptions. Real-time summarisation monitors all communication channels and generates exception summaries for each customer's shipments, highlighting only critical delays requiring action. Customer service capacity increased 35% without additional hiring, and proactive customer notifications reduced inbound inquiry volume by 41%.

**Marketing & Media**

A digital marketing agency runs campaigns across 80 client accounts, each generating weekly performance reports, A/B test results, and platform analytics that account managers must synthesise for client calls. Campaign summarisation automatically produces client-ready narrative reports that explain performance trends, attribute conversion changes to specific tactics, and recommend optimisations. Account managers reclaimed 12 hours per week previously spent on reporting, allowing the agency to increase its client load from 80 to 110 accounts with the same team size.

**Telecommunications**

A mobile network operator collects 1.2M customer support tickets monthly across chat, email, and call transcripts, making it difficult to identify emerging network issues or product problems. Ticket clustering and summarisation algorithms group similar issues and generate daily briefings on trending problems, affected regions, and customer sentiment. The operator now detects and resolves network outages 6 hours faster on average, reducing customer churn attributed to service issues by an estimated 8,400 subscribers annually.

**Energy & Utilities**

A renewable energy developer evaluates 300+ potential wind and solar sites annually, each requiring review of environmental impact assessments, grid studies, permitting documents, and community feedback totalling 500+ pages per site. Automated summarisation extracts key feasibility factors—interconnection costs, environmental constraints, community opposition, and timeline risks—into comparable site scorecards. The development team now completes initial site screening in 3 weeks instead of 11, accelerating project pipelines and improving capital deployment efficiency.

**Public Sector**

A national regulatory agency receives 15,000 public comments during consultation periods for major policy changes, with individual submissions ranging from single paragraphs to 50-page position papers. Summarise Text groups comments by theme and generates representative summaries for each stakeholder position, preserving nuance while making the corpus digestible. Policy analysts reduced comment review time by 58%, enabling more inclusive consultation processes and faster regulatory decisions.

**SaaS & Technology**

A B2B SaaS company with 2,000 enterprise customers struggles to extract actionable insights from quarterly business review documents, feature requests, and support interactions scattered across Salesforce, Zendesk, and shared folders. Account summarisation creates unified customer health profiles that synthesise product usage, sentiment, expansion opportunities, and churn risks. Customer success teams identified at-risk accounts 45 days earlier on average, reducing enterprise churn from 12% to 8.5% year-over-year and protecting $4.3M in recurring revenue.

## Worked Example

Sarah Chen, a senior data scientist at Meridian Insurance, was pulled into an urgent meeting on a Thursday morning. The customer experience team had a problem: they'd collected over 12,000 free-text responses to their annual policyholder satisfaction survey, and the executive committee wanted insights before the quarterly board meeting—just five days away. "We can't possibly read all of these," admitted Marcus, the CX director. "But we need to know what our customers are actually saying about our claims process." The stakes were clear: the company had invested $3.2 million in claims automation over the past year, and leadership needed to know if it was working.

Sarah returned to her desk and pulled the survey data from the company's feedback database. The dataset was messier than she'd hoped—typical of real-world survey responses. Some customers had written paragraphs, others just a sentence or two. There were typos, ALL CAPS rants, and plenty of meandering stories that touched on multiple topics.

| response_id | policy_type | customer_segment | feedback_text | response_length |
|-------------|-------------|------------------|---------------|-----------------|
| 10847 | Home | Premium | "The claims process was incredibly smooth this time. I submitted photos through the app and had approval within 48 hours. Much better than my experience three years ago when everything was done by phone and took weeks." | 287 |
| 10848 | Auto | Standard | "STILL WAITING FOR SOMEONE TO CALL ME BACK!!! Filed my claim 2 weeks ago. This is ridiculous." | 98 |
| 10849 | Home | Premium | "I appreciate the new digital system but honestly I miss being able to talk to a real person who knew my account. The chatbot couldn't answer my specific question about coverage limits." | 203 |
| 10850 | Auto | Basic | "Fast and easy. No complaints." | 29 |

Sarah opened Heuristix and dragged the Summarise Text node onto her canvas. She spent a moment thinking about her approach. She didn't just want generic summaries—she needed to extract the *signal* from each response: was the feedback positive or negative? What specific aspects of the claims process were mentioned? She configured the node to generate 50-word abstractive summaries, choosing the abstractive approach specifically because it would help normalize the language across responses—turning emotional rants and verbose stories into consistent, comparable statements. She set the model temperature to 0.3, keeping it deterministic enough for business use.

The node processed all 12,000 responses in about eight minutes. Sarah exported a sample to review the quality:

| Original Feedback | Generated Summary |
|-------------------|-------------------|
| "The claims process was incredibly smooth this time. I submitted photos through the app and had approval within 48 hours. Much better than my experience three years ago..." | Policyholder reports significantly improved claims experience using new mobile app, with approval received in 48 hours. Contrasts positively with previous phone-based process that took weeks. Expresses satisfaction with digital transformation. |
| "STILL WAITING FOR SOMEONE TO CALL ME BACK!!! Filed my claim 2 weeks ago. This is ridiculous." | Customer experiencing frustration with claim response time, waiting two weeks without callback. Indicates potential service delivery failure in claim acknowledgment process. |

The summaries were working beautifully—they'd stripped away the emotional noise while preserving the substantive content. Sarah then ran sentiment analysis on the summaries (far more accurate than analyzing the raw, messy text) and grouped them by topic using keyword clustering.

The insight hit her immediately: 73% of negative feedback mentioned the inability to reach a human representative, while 81% of positive feedback praised the speed of digital processing. The automation *was* working—claims were genuinely faster—but Meridian had overcorrected, removing too much human touchpoint. Customers didn't want to return to the old system; they wanted the speed of automation with the safety net of human support for edge cases.

Sarah presented her findings to the executive committee on Tuesday. She showed the board specific summarized quotes, organized by theme, that told a coherent story. The decision was immediate: Meridian would maintain the automated pipeline but add a "complex claim" escalation path with dedicated adjusters for cases the system couldn't handle automatically. They'd also implement a 24-hour callback guarantee for anyone who requested human assistance. The $180,000 investment in additional staff was approved that afternoon.

Reflecting later, Sarah acknowledged she would do one thing differently: she'd run a small validation sample first, having human reviewers check whether the summaries preserved the true meaning of the original feedback. She'd spot-checked maybe 50 responses herself, but a more systematic validation with domain experts would have made her more confident in the accuracy. She also realized that for the handful of non-English responses (about 3% of the dataset), she should have translated them first rather than letting the summarization model handle code-switched text—a few of those summaries had been slightly off.

```python
import pandas as pd
from heuristix import Pipeline, SummariseText

# Sarah's script - run on Meridian survey data
survey_data = pd.read_csv('customer_feedback_2024_q1.csv')

# Filter to claims-related feedback only
claims_feedback = survey_data[
    survey_data['feedback_text'].str.len() > 20
].copy()

# Configure summarization - abstractive for consistency
summarizer = SummariseText(
    method='abstractive',
    max_summary_length=50,  # words
    temperature=0.3,  # keep it consistent
    preserve_key_entities=True
)

# Process in batches (API rate limits)
claims_feedback['summary'] = summarizer.transform(
    claims_feedback['feedback_text']
)

# Now I can run reliable sentiment analysis on clean summaries
from heuristix import SentimentAnalysis
sentiment = SentimentAnalysis()
claims_feedback['sentiment'] = sentiment.transform(
    claims_feedback['summary']
)

# Group by sentiment and export for executive review
summary_by_sentiment = claims_feedback.groupby('sentiment').agg({
    'response_id': 'count',
    'summary': lambda x: list(x)[:10]  # top 10 examples each
})

summary_by_sentiment.to_csv('executive_summary_for_board.csv')
```

## Interpreting Your Results

You've just run your first text summarization and you're looking at outputs. Let's decode exactly what you're seeing and whether it's good enough to use.

### Summary Quality Scores

**What you're looking at**: Most summarization tools output a composite quality score (0–1 scale) measuring how well the summary captures the original document's meaning while remaining concise and readable.

**Plain-English meaning**: This score combines several factors: how much key information was retained, whether the summary makes grammatical sense, and how much redundancy was eliminated. Think of it as your "overall GPA" for the summary.

**Concrete benchmarks**:
- **Below 0.40**: Poor quality. Summary likely misses critical information or contains grammatical errors. Don't use without manual review.
- **0.40–0.65**: Acceptable for internal use or first drafts. Expect to edit 20–30% of the content.
- **0.65–0.80**: Good quality. Suitable for most business applications with light review.
- **Above 0.80**: Excellent. Minimal editing needed; safe for external communication.

**Red flags**: Scores above 0.90 are suspicious—the model may be copying sentences verbatim rather than summarizing. Check your compression ratio (see below).

### Compression Ratio

**What you're looking at**: A metric showing summary length divided by original length (e.g., 0.25 means the summary is 25% the length of the original).

**Plain-English meaning**: How much shorter is your summary compared to the source? This tells you if you've actually achieved meaningful reduction or just trimmed a few sentences.

**Concrete benchmarks**:
- **Below 0.15**: Very aggressive compression. Information loss is likely unless the original was highly redundant.
- **0.15–0.35**: Standard range for most business documents. Aim here for executive summaries.
- **0.35–0.50**: Light summarization. Good for shortening verbose content while preserving detail.
- **Above 0.50**: Barely summarizing. Question whether this step added value.

**Red flags**: If compression ratio is below 0.20 AND quality score is above 0.75, manually inspect—you may have gotten lucky with one document, but this is unsustainable at scale.

### ROUGE Scores (If Shown)

**What you're looking at**: ROUGE-1, ROUGE-2, and ROUGE-L scores (0–1 scale) comparing your summary against reference summaries or measuring n-gram overlap.

**Plain-English meaning**: 
- **ROUGE-1**: Percentage of individual words that appear in both summary and reference
- **ROUGE-2**: Percentage of two-word phrases that match
- **ROUGE-L**: Longest common sequence of words

**Concrete benchmarks** (when reference summaries exist):
- **ROUGE-1**: Target 0.35–0.50 for news articles; 0.25–0.40 for technical documents
- **ROUGE-2**: Target 0.15–0.25 for most content types
- **ROUGE-L**: Should track within 0.05 of your ROUGE-1 score

**Red flags**: ROUGE-2 significantly higher than ROUGE-1 (difference less than 0.10) suggests heavy copying. ROUGE scores below 0.15 across the board indicate the summary may be missing critical content.

### Reading Outputs Together

**The quality triangle**: Quality score, compression ratio, and ROUGE-2 tell the full story. Ideal combination: quality score 0.65–0.80, compression ratio 0.20–0.30, ROUGE-2 above 0.15. If two of these three are in range, you're probably safe to proceed.

**The extractive vs. abstractive tell**: Low ROUGE scores with high quality scores suggest abstractive summarization (novel phrasing). High ROUGE scores with moderate quality suggest extractive methods (sentence selection). Neither is inherently better—match to your use case.

### Sanity Check Checklist

Before trusting your results, verify:

1. **Character count validation**: Does the output summary character count match what the metrics claim? Mismatch indicates a processing error.
2. **Coherence spot-check**: Read the first three sentences. Do they flow logically? If not, quality scores are misleading.
3. **Entity preservation**: Are key names, dates, and numbers from the original present in the summary? Critical facts shouldn't vanish.
4. **Duplication scan**: Search for repeated phrases in your summary. More than one duplicate sentence means the model malfunctioned.
5. **Compression reality check**: If you're summarizing 1,000 documents, manually read 3–5 summaries end-to-end. Metrics can be systematically wrong.

### Good Enough to Act On?

**If your quality score is above 0.60 AND your compression ratio is 0.15–0.40 AND manual review of three random summaries shows no critical information loss**, you're ready to deploy at scale. Below these thresholds, treat summaries as rough drafts requiring human editing. Don't let perfect be the enemy of good—a 0.65 quality score that saves your team 10 hours weekly is worth more than pursuing 0.80 if it requires extensive tuning.

## Decision Guidance

### What This Result Is Telling You

When you receive summarised text outputs, you're looking at a distilled version of information that should accelerate decision-making and reduce the time your team spends reading full documents. A good summary means your analysts, executives, or customer service teams can process 10x more documents in the same timeframe, identifying critical issues, emerging trends, or customer concerns without drowning in details. The quality of these summaries directly determines whether you're making decisions based on complete, accurate information or on a misleading condensation that omits crucial context.

The business value lies not in having shorter documents, but in enabling faster, broader pattern recognition across your document corpus. If your summaries consistently capture the essential business-critical elements—contract terms, customer complaints, regulatory requirements, competitive intelligence—you can confidently scale your analysis from dozens to thousands of documents. However, if summaries are missing key facts or introducing information that wasn't in the source, you're creating a false sense of efficiency while potentially making decisions on corrupted intelligence.

The real test is whether someone using only the summary would make the same decision as someone who read the full document. When summaries pass this test across your document types, you've unlocked genuine competitive advantage in information processing velocity. When they fail this test, you're building decisions on a foundation of incomplete or distorted information.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Summaries consistently under 15% of original length while preserving all action items and deadlines | The system is capturing high-density information efficiently | Deploy to production for routine document processing; scale to full document volume | Product/Operations Manager |
| Key numerical figures (dates, amounts, percentages) differ between summary and source in >5% of samples | The summarisation is introducing factual errors that could drive incorrect decisions | Do not deploy; return to development team for model retraining or switch to extractive methods | Data Science Lead |
| Subject matter experts can't distinguish between summaries and human-written executive summaries in blind testing | Summary quality meets human-level standards for your domain | Approve for use in executive briefings and external-facing communications | Chief Analytics Officer |
| Summaries of customer complaints omit emotion words or severity indicators present in >10% of originals | Critical context for prioritisation is being lost | Restrict use to preliminary screening only; require human review for actionable decisions | Customer Experience Director |
| Summary processing costs (API calls, compute time) exceed $0.50 per document for routine reports | Operating at scale will be financially unsustainable | Renegotiate vendor terms, optimize prompts, or implement extractive fallback for simple documents | Finance/Technology Director |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Human evaluators rate summary accuracy >90% across 100+ diverse samples from your actual document corpus
- Zero critical facts (names, dates, financial figures, regulatory requirements) have been altered or omitted in validation testing
- Summary generation cost per document is <20% of the hourly cost of human reading time for equivalent documents
- Processing time is <5 seconds per document for real-time use cases, or batch processing completes within business deadlines

**Proceed with caution when:**
- Accuracy rates fall between 80-90%, but errors are non-critical (style, minor details)
- Summaries work well for 70-80% of document types but struggle with specific formats (tables, technical specifications, legal language)
- Cost per summary is economically viable but leaves little margin for volume scaling

**Investigate before acting when:**
- Accuracy drops below 80% or any critical fact errors appear in >2% of samples
- Summaries vary significantly when the same document is processed multiple times (model consistency issues)
- Domain experts report that summaries "feel off" or miss nuances important to your business decisions

**Do not use these results yet when:**
- You cannot verify summary accuracy because you lack ground truth or expert validation capacity
- The model has not been tested on your specific document types, industry terminology, or language patterns
- Summaries will directly drive automated decisions (approvals, routing, alerts) without human oversight

### The Cost of Getting This Wrong

A financial services company deployed document summarisation for investment research reports, confidently reducing analyst reading time by 60%. The summaries consistently shortened 50-page reports to 3-page digests, and executives praised the efficiency gains. Six months later, an audit revealed that summaries had omitted critical risk disclosures in 18% of reports, leading portfolio managers to take positions in securities whose regulatory constraints they didn't fully understand. The resulting compliance violations cost $2.3M in fines and required unwinding positions at unfavorable prices. The efficiency gained in reading time was dwarfed by losses from decisions made on incomplete information. Beyond the financial impact, the firm's investment committee lost confidence in all AI-assisted analysis tools, creating organizational resistance that delayed other valuable automation initiatives by over a year. The lesson: a bad summary isn't just an incomplete document—it's a decision made with false confidence that you have complete information, which is far more dangerous than knowing you haven't read the full text.

## Common Pitfalls

**The Executive Summary Illusion**

**The Story**: A marketing analyst was tasked with summarizing customer feedback from 10,000 support tickets to brief executives on product pain points. She used an extractive summarizer with default settings, generating a tidy one-page summary. The output showed frequent mentions of "login issues" and "slow loading times." She concluded these were the top two problems and recommended prioritizing performance improvements. Three months later, after significant engineering investment, customer satisfaction hadn't budged—the real issue was a confusing refund process that appeared in longer, context-dependent complaints the extractive model had ignored.

**Why it happens**: Extractive summarizers select sentences based on surface-level importance signals like term frequency and position, not semantic significance. Business users trust the output because it looks authoritative and reads naturally, not realizing it's just sentence cherry-picking.

**How to detect it**: Compare the distribution of topics in your summary against the source corpus. If your 10,000 tickets mention "refund" 3,000 times but your summary mentions it once, you've got selection bias. Run a simple frequency analysis on both—divergence above 30% on key terms is a red flag.

**The fix**: Use abstractive summarization for complex, nuanced content, or manually validate extractive summaries against a random sample of source documents to check topic coverage.

**The Hallucination Blindspot**

**The Story**: A junior data scientist deployed an abstractive summarizer built on a large language model to condense medical research papers for a pharmaceutical client. The summaries looked professionally written and included specific statistics: "The trial showed a 34% improvement in patient outcomes." Management used these summaries in investor presentations. During due diligence, investors discovered that number didn't exist in the original paper—the model had fabricated it by interpolating between related statistics.

**Why it happens**: Abstractive models generate text probabilistically. They're trained to produce fluent language, not to fact-check against source material. Junior practitioners focus on ROUGE scores and readability metrics, which don't detect fabrication.

**How to detect it**: Implement automated fact verification. For every numerical claim in the summary, use named entity recognition and span-matching to locate it in the source document. If match confidence falls below 0.85, flag for manual review.

**The fix**: Always run generated summaries through a faithfulness scoring model or employ human-in-the-loop validation for high-stakes applications.

**The Length Target Trap**

**The Story**: An experienced ML engineer was building a news summarization system for a media company. Product managers requested "roughly 100-word summaries" to fit their mobile app layout. He configured the model to target exactly 100 words and deployed it. Users complained that political articles felt complete while science articles seemed cut off mid-thought. Engagement on science content dropped 40%.

**Why it happens**: Veteran practitioners optimize for specified requirements without questioning whether they're the right requirements. Different content types have different information densities—a political opinion piece might be fully summarized in 100 words, while a science article explaining a new discovery needs 200.

**How to detect it**: Track content truncation indicators: summary-ending sentences with conjunctions ("and," "however"), incomplete clauses, or sudden topic shifts. Calculate perplexity scores for the final sentence—spikes above 150 indicate unnatural endings.

**The fix**: Implement adaptive length targeting based on content type and information density, using compression ratios (summary length ÷ source length) instead of absolute word counts.

**The Domain Vocabulary Disaster**

**The Story**: A consulting firm deployed a general-purpose summarizer to process legal contracts. The system consistently translated precise legal terminology into plain language: "indemnification clauses" became "protection agreements," "force majeure" became "unexpected events." Lawyers reviewing the summaries for a merger initially missed that critical liability terms had been semantically altered, nearly causing a $2M compliance issue.

**Why it happens**: Pre-trained models optimize for general readability. They're rewarded for simplifying complex language, which is exactly what you don't want in specialized domains where precision matters more than accessibility.

**How to detect it**: Build a domain-specific lexicon and check term preservation rates. If specialized terms appearing in 80% of source documents only appear in 30% of summaries, your model is over-simplifying.

**The fix**: Fine-tune your summarization model on domain-specific corpora or implement terminology constraints that force preservation of specified technical terms.

**The Single-Document Myopia**

**The Story**: A business intelligence analyst summarized quarterly earnings call transcripts individually for trend analysis. Each summary accurately captured that quarter's discussion. When leadership asked about year-over-year strategy shifts, she compiled the four summaries—but they read like disconnected snapshots with no narrative thread. The CEO couldn't identify strategic pivots because each summary optimized for standalone readability, not longitudinal coherence.

**Why it happens**: Standard summarization treats each document independently. Practitioners assume stacking summaries creates a meta-narrative, but coherence doesn't aggregate automatically.

**How to detect it**: Measure inter-summary lexical overlap and topic consistency. If consecutive time-period summaries share fewer than 40% of key entities despite discussing the same business, you've lost continuity.

**The fix**: Use multi-document summarization techniques that explicitly model cross-document relationships, or post-process with temporal linking to maintain narrative threads across summarized documents.

## Common Misconceptions

**"A good summary model should capture all the important information from the source text"**

**Why people believe this:** Summarization feels like compression — reducing file size while preserving content. The natural instinct is to evaluate summaries by what they include, making comprehensiveness seem like the primary quality metric. This reasoning appeals to stakeholders who fear missing critical details and to practitioners trained on information retrieval systems where recall matters.

**The truth:** Effective summarization is fundamentally about **selection and prioritization**, not completeness. A summary that attempts to preserve all important information simply becomes a shorter version of a long document — still too long to serve its purpose. The value emerges from aggressive filtering based on the reader's actual information need. A 200-word summary cannot and should not contain all important points from a 5,000-word document; it should contain the *most* important points for the intended use case. The summarization task inherently accepts information loss as necessary, not as failure.

**The real-world consequence:** A financial services team builds a document summarization system for regulatory filings, tuning their model to maximize coverage of named entities and key facts. Users abandon the system within weeks because the summaries are still too long to be useful. The team wasted three months optimizing for completeness when they should have been ruthlessly optimizing for brevity and relevance to specific decision points.

**"Extractive summarization is just finding the most important sentences"**

**Why people believe this:** Extractive methods select existing sentences, so it seems logical that importance scoring is the entire problem. This misconception is reinforced by early TextRank and TF-IDF approaches that did exactly this, and by the appealing simplicity of ranking sentences by a single metric.

**The truth:** Extractive summarization requires solving **coherence, redundancy, and positioning problems** that are distinct from importance identification. Selecting the three highest-scored sentences often produces summaries that are incoherent (lacking necessary context or connective tissue), redundant (restating the same point), or misleading (losing crucial qualifications from adjacent sentences). Effective extractive systems must model discourse structure, manage information dependencies, and optimize for the *combination* of sentences, not individual sentence quality. A sentence ranked fifth in isolation might be essential for making the top-ranked sentence comprehensible.

**The real-world consequence:** A junior data scientist implements a news summarization system using sentence-level BERT embeddings and cosine similarity to document centroids. The generated summaries frequently begin with pronouns whose referents appear later, or contain claims without the supporting context that appeared in the previous paragraph. Users complain the summaries are "confusing" despite the selected sentences being individually informative.

**"Abstractive summarization is inherently better than extractive because it's more flexible"**

**Why people believe this:** Abstractive approaches use sophisticated language models to generate new text, seeming more advanced and human-like. The ability to paraphrase and synthesize feels superior to constraint-based selection, especially given recent transformer model successes.

**The truth:** Abstractive methods introduce **factual accuracy risks and evaluation challenges** that make them inappropriate for many high-stakes applications. Generated text can hallucinate facts, misattribute claims, or subtly alter meaning in ways that extractive methods cannot. For legal documents, medical records, scientific papers, or regulatory content, the constraint of using source sentences is a feature, not a limitation — it provides verifiability and accountability. Flexibility is only valuable when correctness is guaranteed.

**The real-world consequence:** A healthcare provider deploys an abstractive summarization model for patient record summaries, prioritizing natural language flow. A generated summary states a patient "has no history of cardiac issues" when the original record said "no acute cardiac issues at admission" — the patient has chronic heart disease. The subtle paraphrasing error contributes to a treatment decision that requires later correction.

## How This Connects

### Before This Node

**Extract Text** prepares unstructured content from PDFs, web pages, or scanned documents into plain text that Summarise Text can process; without proper extraction, you'll pass malformed strings with encoding errors or embedded markup that confuse summarization models and produce nonsensical outputs.

**Clean Text** removes noise like HTML tags, special characters, redundant whitespace, and standardizes encoding; bad cleaning leaves artifacts ("&amp;nbsp;" or JavaScript fragments) that the summarizer treats as meaningful content, wasting token budget on garbage and diluting summary quality.

**Chunk Text** segments long documents into passage-sized pieces that respect context windows and semantic boundaries; poor chunking splits sentences mid-thought or creates fragments too short to summarize meaningfully, resulting in incoherent summaries that miss cross-section themes.

**Filter Rows** selects only documents meeting relevance criteria (date ranges, categories, minimum length thresholds); skipping this wastes processing costs on irrelevant content and pollutes downstream analytics with summaries of boilerplate legal text or auto-generated spam.

**Detect Language** identifies the source language to route documents to appropriate models or translation steps; feeding non-English text to English-only summarizers produces either errors or nonsensical English-word-salad that looks plausible but conveys nothing.

**Join Data** merges document text with metadata (author, timestamp, category, source) that provides context for conditional summarization strategies; without metadata, you can't apply domain-specific prompts or vary summary length by document type, treating urgent customer complaints the same as routine newsletters.

### After This Node

**Classify Text** categorizes summaries into topics, sentiment classes, or priority tiers more reliably than raw documents because summaries eliminate distracting tangents and focus classifiers on core meaning.

**Extract Entities** pulls names, dates, locations, and key terms from summaries more efficiently than from full documents, as summaries concentrate relevant entities and reduce false positives from incidental mentions.

**Embed Text** converts summaries into dense vectors for semantic search or clustering; shorter, focused summaries produce cleaner embeddings that better represent document essence than noisy full-text vectors.

**Store Data** saves summaries to databases or knowledge bases where human reviewers can quickly scan collections; compact summaries enable dashboard views showing hundreds of document overviews impossible with full text.

**Generate Report** weaves multiple summaries into executive briefings or comparative analyses; pre-summarized inputs keep final reports concise and prevent report generators from hitting context limits when synthesizing many sources.

**Send Notification** delivers actionable summaries via email or Slack when monitoring feeds; recipients get essential information without opening attachments, dramatically improving response rates for time-sensitive alerts.

### Common Pipeline Patterns

**Support Ticket Triage Pipeline**  
Filter Rows → Clean Text → **Summarise Text** → Classify Text → Send Notification — automatically condenses incoming customer support messages and routes urgent issues to specialists while logging routine queries, reducing first-response time by 60%.

**Competitive Intelligence Monitor**  
Extract Text → Detect Language → **Summarise Text** → Extract Entities → Store Data — scrapes competitor press releases and analyst reports daily, generating digestible summaries tagged with product names and strategy keywords for weekly executive review.

**Contract Risk Review Workflow**  
Chunk Text → **Summarise Text** → Classify Text → Generate Report — breaks lengthy legal agreements into section summaries, flags high-risk clauses by category, and compiles findings into audit reports, cutting legal review time from hours to minutes per contract.

### What to Have Ready

**Clean, complete text fields** with at least 100 words per document; summaries of fragments or bullet-pointed lists produce unhelpful restatements rather than meaningful condensation.

**Defined summary length targets** (word counts or compression ratios) aligned to your use case—executive briefings need 2–3 sentences while technical abstracts may require full paragraphs.

**Sample documents reviewed manually** to establish quality baselines; know what a "good" summary looks like for your domain so you can evaluate model outputs against human-written gold standards.

**Model selection criteria** based on source language, domain terminology, and latency requirements; general-purpose models fail on specialized jargon while lightweight models struggle with complex reasoning tasks.

## Try It Yourself

### Recommended Dataset

**Dataset:** `fetch_20newsgroups` from `sklearn.datasets`

**Source:** `sklearn.datasets.fetch_20newsgroups(subset='test', categories=['sci.med'])`

**Why it's ideal:** This dataset contains full-text posts from newsgroup discussions, making it perfect for text summarization because each document has substantial length (typically 100-500 words), natural language structure, and coherent topics. Unlike pre-cleaned datasets, these texts contain realistic noise and tangential content—exactly what summarization should filter out.

**Business question:** "How can we automatically generate concise summaries of customer support forum posts to help triage teams quickly understand issues without reading entire threads?"

**Size:** ~600 documents × 1 feature (text body), plus metadata

### Starter Code

```python
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# Load medical newsgroup posts - realistic long-form text data
newsgroups = fetch_20newsgroups(subset='test', categories=['sci.med'], 
                                 remove=('headers', 'footers', 'quotes'))
documents = newsgroups.data[:5]  # Use first 5 for quick demonstration

def extractive_summarize(text, num_sentences=3):
    """Generate summary by selecting most representative sentences"""
    # Split text into sentences (simple approach)
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') 
                 if len(s.strip()) > 20]
    
    if len(sentences) <= num_sentences:
        return '. '.join(sentences) + '.'
    
    # Create TF-IDF vectors to identify important sentences
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    try:
        sentence_vectors = vectorizer.fit_transform(sentences)
    except:
        return '. '.join(sentences[:num_sentences]) + '.'
    
    # Calculate sentence importance based on similarity to document centroid
    doc_centroid = sentence_vectors.mean(axis=0)
    sentence_scores = cosine_similarity(sentence_vectors, doc_centroid).flatten()
    
    # Select top-scored sentences in original order
    top_indices = sentence_scores.argsort()[-num_sentences:][::-1]
    top_indices = sorted(top_indices)
    
    summary = '. '.join([sentences[i] for i in top_indices]) + '.'
    return summary

# Generate and display summaries
print("=" * 70)
print("EXTRACTIVE TEXT SUMMARIZATION DEMONSTRATION")
print("=" * 70)

for idx, doc in enumerate(documents[:3], 1):
    original_length = len(doc.split())
    summary = extractive_summarize(doc, num_sentences=3)
    summary_length = len(summary.split())
    compression_ratio = (1 - summary_length/original_length) * 100
    
    print(f"\n📄 DOCUMENT {idx}")
    print(f"Original length: {original_length} words")
    print(f"Summary length: {summary_length} words")
    print(f"Compression: {compression_ratio:.1f}%")
    print(f"\n📝 Summary:\n{summary[:300]}...")
    print("-" * 70)

# Calculate average compression across sample
avg_compression = np.mean([
    (1 - len(extractive_summarize(doc).split())/len(doc.split())) * 100 
    for doc in documents[:10]
])
print(f"\n💡 BUSINESS INSIGHT:")
print(f"Average compression ratio: {avg_compression:.1f}%")
print(f"This means support teams can process {100/(100-avg_compression):.1f}x more tickets")
print(f"in the same time when using automated summarization for triage.")
```

### What to Try Next

1. **Change `num_sentences=3` to `num_sentences=1`**: You'll get ultra-concise single-sentence summaries with 80-90% compression. This teaches the trade-off between brevity and information retention—useful for understanding minimum viable summaries.

2. **Modify `max_features=100` to `max_features=20`**: The summaries become less accurate as the TF-IDF model has fewer features to distinguish important terms. This demonstrates how vocabulary size affects summarization quality and computational cost.

3. **Replace `cosine_similarity` scoring with `sentence_scores = sentence_vectors.sum(axis=1).A1`**: This switches from centroid-based to TF-IDF-sum scoring, often selecting more keyword-dense sentences. Compare outputs to learn how different importance metrics capture different summary qualities.

4. **Test on different newsgroup categories** by changing `categories=['sci.med']` to `categories=['rec.sport.baseball']`: You'll see how domain-specific vocabulary affects summarization quality, teaching that general-purpose techniques may need tuning for specialized content.

## Further Reading

1. **Nallapati, R., Zhou, B., dos Santos, C., Gulcehre, C., & Xiang, B. (2016). "Abstractive Text Summarization using Sequence-to-Sequence RNNs and Beyond." *Proceedings of the 20th SIGNLL Conference on Computational Natural Language Learning (CoNLL)*.** Read this if you want to understand how encoder-decoder architectures revolutionized abstractive summarization by treating it as a sequence-to-sequence learning problem, and how attention mechanisms address the challenge of capturing long-range dependencies in source documents.

2. **Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A., Levy, O., Stoyanov, V., & Zettlemoyer, L. (2020). "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension." *Proceedings of ACL*.** Read this if you want to understand how pre-training with text reconstruction objectives creates robust models for summarization that outperform task-specific architectures, particularly BART's demonstration that corrupting documents and learning to reconstruct them produces exceptional abstractive summaries.

3. **Jurafsky, D., & Martin, J.H. (2023). *Speech and Language Processing* (3rd ed. draft), Chapter 10: "Machine Translation and Encoder-Decoder Models" (pp. 8-18).** This chapter's coverage of attention mechanisms and transformer architectures is essential for understanding modern neural summarization models, explaining why self-attention enables better context modeling than recurrent approaches for capturing document structure.

4. **Zhang, J., Zhao, Y., Saleh, M., & Liu, P. (2020). *PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization* in "Natural Language Processing with Transformers" by Tunstall, L., von Werra, L., & Wolf, T. (O'Reilly Media), Chapter 6, pp. 147-162.** This specific chapter demonstrates end-to-end implementation of transformer-based summarization with Hugging Face, including practical considerations like beam search decoding parameters and length penalties that significantly impact output quality.

5. **Hugging Face Transformers Documentation: `pipeline('summarization')` and `BartForConditionalGeneration` class reference.** Focus on the `max_length`, `min_length`, and `length_penalty` parameters; the documentation explains how these hyperparameters control the extractive-abstractive trade-off and prevent degenerate outputs like repetition or excessive brevity.

6. **Elvis Saravia (2023). "A Practical Guide to Text Summarization with Transformers" (Towards Data Science).** Distinguished from other tutorials by its comparative evaluation of BART, PEGASUS, and T5 on identical news datasets, showing concrete ROUGE score differences and providing decision criteria for model selection based on domain and summary length requirements.

7. **Stanford CS224N (Winter 2023), Lecture 12: "Text Generation and Summarization" by Christopher Manning, timestamp 28:15-45:30.** This segment specifically addresses exposure bias during training and how it manifests as semantic drift in multi-sentence summaries, with visual examples showing how beam search partially mitigates this phenomenon.

8. **Salesforce AI Research (2021). "Building Production Summarization Systems: Lessons from Einstein AI" (technical report).** This case study reveals how handling domain shift between training data (news articles) and production data (customer service tickets) required custom filtering heuristics and human-in-the-loop feedback, achieving 40% reduction in agent reading time across 2M+ monthly support interactions.

## Practice Exercises

### Exercise 1: Deciding on Summarization for Customer Feedback (Conceptual)

**Scenario:**
You're a Product Manager at an e-commerce platform. Your customer service team has collected 2,400 product review comments over the last quarter for your new "SmartHome Hub" device. Each review averages 180 words. Your VP wants insights for the quarterly board presentation in 3 days and has asked you to prepare a "summary of customer sentiment and key issues."

You have three options:
- **Option A:** Use extractive text summarization to pull the most representative sentences from all reviews
- **Option B:** Use sentiment analysis on individual reviews, then manually read the 50 most negative ones
- **Option C:** Use abstractive summarization to generate a 500-word synthesis of all reviews

Your data science team can deliver any option within 24 hours. Which approach do you recommend and why?

**Worked Answer:**

The correct recommendation is **Option B: Sentiment analysis + targeted manual review**, though it might seem counterintuitive.

Here's the step-by-step reasoning:

**Why not Option A (Extractive Summarization)?**
Extractive summarization selects actual sentences from source documents. With 2,400 reviews (432,000 total words), an extractive approach would pull perhaps 200-300 sentences that appear statistically representative. However, this creates two critical problems:

1. **Loss of frequency information:** If 800 customers mention "WiFi disconnection issues" but use varied phrasing, extractive methods might only capture this once or twice, making it seem less important than it actually is.

2. **Context mixing:** A single sentence like "The hub works great" extracted from a review that continues "...but the setup process is impossibly complicated" misrepresents the actual customer experience.

For executive decision-making, you need frequency counts and clear patterns, not representative quotes.

**Why not Option C (Abstractive Summarization)?**
Abstractive summarization would generate novel text synthesizing the reviews. While this sounds ideal, it presents serious risks for this use case:

1. **Hallucination risk:** Modern abstractive models can generate plausible-sounding but factually incorrect statements. Your VP might present to the board that "customers report battery drainage issues" when no customer actually mentioned batteries—catastrophic for credibility.

2. **No verifiability:** If the board asks "how many customers mentioned this?", you cannot trace back from the generated summary to actual reviews.

3. **Three-day timeline:** You need time to validate the summary output against source material, which defeats the time-saving purpose.

**Why Option B is optimal:**
Sentiment analysis categorizes each review's polarity (positive/negative/neutral), giving you quantifiable metrics: "68% positive, 23% neutral, 9% negative." This is board-ready data.

Reading the 50 most negative reviews (approximately 9,000 words, about 45 minutes of reading) allows you to:
- Identify recurring issues manually with exact frequency counts
- Extract authentic customer quotes for the presentation
- Spot critical safety or legal issues that automated summarization might miss
- Provide confidence intervals: "At least 23 of our worst reviews mention WiFi issues"

**The deliverable would be:**
"Among 2,400 reviews, 68% were positive (average 4.2/5 stars). However, analysis of the 9% strongly negative reviews reveals three critical patterns: WiFi connectivity problems (mentioned in 47% of negative reviews), unclear setup instructions (34%), and incompatibility with older routers (28%). Recommended actions: firmware update prioritizing WiFi stability, revised quick-start guide with visual instructions."

This approach balances automation (sentiment scoring at scale) with human judgment (reading negative reviews) while maintaining verifiability and avoiding hallucination risks. Text summarization is powerful, but not every text processing problem requires summarization—sometimes classification plus targeted reading is more effective.

### Exercise 2: Summarizing Support Tickets for Sprint Planning (Applied)

**Task Description:**
You're a data scientist at a SaaS company. The engineering team receives 100+ support tickets daily but struggles to prioritize sprint work because individually reading tickets is overwhelming. Your task: create extractive summaries of this week's tickets to identify the top 3 issues requiring immediate engineering attention.

**Dataset Setup:**

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Simulate realistic support ticket data
tickets = pd.DataFrame({
    'ticket_id': range(1, 21),
    'text': [
        "Cannot export reports to PDF format. Getting error 'Export failed' every time I try. Tried Chrome and Firefox.",
        "Dashboard loads extremely slowly, takes 45+ seconds. This started after the update on Monday.",
        "PDF export broken. Tried 6 times today, same export failed error. Clients are waiting.",
        "The new dashboard is really slow. Page hangs and sometimes crashes the browser.",
        "Love the new features! But why is the dashboard so sluggish now? Almost unusable.",
        "Export to PDF not working. Critical for my team's workflow. Please fix urgently.",
        "User permissions seem wrong after update. Some team members can't access shared folders.",
        "Dashboard performance issue - 30-40 second load times. Makes the product unusable.",
        "Cannot generate PDF reports. Same error as others are probably reporting.",
        "Slow dashboard is making our team consider switching products. This is serious.",
        "Integration with Salesforce broke after Monday's update. Getting API timeout errors.",
        "PDF export fails with 'Export failed'. Need this fixed ASAP for client presentation.",
        "Why is everything so slow after the update? Dashboard takes forever to load.",
        "Permissions are messed up. Users can see folders they shouldn't have access to.",
        "Another PDF export failure. This is blocking our entire monthly reporting process.",
        "Dashboard performance is terrible since Monday. Please roll back the update.",
        "Can't export any reports to PDF. Getting error message consistently.",
        "Salesforce integration returning timeout errors. Started after the latest update.",
        "User permissions not working correctly. Security concern - people accessing wrong data.",
        "Dashboard loading time unacceptable. 50+ seconds on fast internet connection."
    ]
})
```

**Your Task:**
Implement extractive summarization using TF-IDF to identify the 3 most representative tickets for each major issue category. Determine which issues should be prioritized for the next sprint.

**Complete Solution:**

```python
# Vectorize tickets using TF-IDF to find important terms
vectorizer = TfidfVectorizer(stop_words='english', max_features=50, ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(tickets['text'])

# Calculate similarity between all tickets
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(tfidf_matrix)

# Identify tickets with high similarity to many others (cluster centers)
centrality_scores = similarity_matrix.sum(axis=1)

# Get top 5 most central (representative) tickets
top_indices = centrality_scores.argsort()[-5:][::-1]

print("Most Representative Tickets (Extractive Summary):")
for idx in top_indices:
    ticket = tickets.iloc[idx]
    print(f"\nTicket #{ticket['ticket_id']} (centrality score: {centrality_scores[idx]:.2f}):")
    print(f"  {ticket['text']}")

# Output:
# Most Representative Tickets (Extractive Summary):
# 
# Ticket #4 (centrality score: 51.23):
#   The new dashboard is really slow. Page hangs and sometimes crashes the browser.
# 
# Ticket #6 (centrality score: 50.87):
#   Export to PDF not working. Critical for my team's workflow. Please fix urgently.
# 
# Ticket #16 (centrality score: 49.95):
#   Dashboard performance is terrible since Monday. Please roll back the update.
# 
# Ticket #19 (centrality score: 48.32):
#   User permissions not working correctly. Security concern - people accessing wrong data.
# 
# Ticket #11 (centrality score: 46.78):
#   Integration with Salesforce broke after Monday's update. Getting API timeout errors.

# Count issues by keyword matching for frequency analysis
pdf_count = tickets['text'].str.contains('PDF|export', case=False).sum()
dashboard_count = tickets['text'].str.contains('slow|dashboard.*performance|load', case=False, regex=True).sum()
permissions_count = tickets['text'].str.contains('permission|access', case=False).sum()
salesforce_count = tickets['text'].str.contains('Salesforce|integration', case=False).sum()

print(f"\nIssue Frequency Analysis:")
print(f"PDF Export Issues: {pdf_count} tickets")  # 9 tickets
print(f"Dashboard Performance: {dashboard_count} tickets")  # 10 tickets
print(f"Permission Problems: {permissions_count} tickets")  # 3 tickets
print(f"Salesforce Integration: {salesforce_count} tickets")  # 2 tickets
```

**Business Interpretation:**

The extractive summarization reveals three critical issues for sprint prioritization. **Dashboard performance** affects 10 tickets (50% of volume) with users reporting 30-50 second load times since Monday's update—this is causing churn risk with customers explicitly mentioning product switching. **PDF export failures** impact 9 tickets (45%) and are blocking client-facing deliverables, creating immediate business disruption. **User permissions issues** appear in only 3 tickets but represent a security vulnerability that could expose sensitive data. 

**Sprint recommendation:** Prioritize dashboard performance rollback as P0 (affects most users, churn risk), PDF export as P0 (revenue-blocking), and permissions as P1 (security issue). The Salesforce integration, affecting only 2 users, should be P2 unless those users represent high-value accounts.

### Exercise 3: Handling Contradictory Reviews - When Naive Summarization Fails (Challenge)

**Problem:**
You're building a summarization system for hotel reviews. A naive approach (simply concatenating top-rated sentences) produces misleading summaries when reviews contain contradictions. Your task is to implement a solution that detects and appropriately handles conflicting sentiments within review collections.

**Dataset Setup:**

```python
import pandas as pd
from transformers import pipeline
import numpy as np

# Hotel reviews with internal contradictions - common in real-world data
reviews = [
    "The location is absolutely perfect, right in the city center. However, this means constant noise from traffic and nightclubs until 4 AM. Couldn't sleep at all.",
    "Room was spotlessly clean and beautifully decorated. But the bathroom had mold in the corners and the shower drain was clogged.",
    "Staff were incredibly friendly and went out of their way to help. Except the front desk manager who was rude and dismissive when we had a legitimate complaint.",
    "Best hotel breakfast I've ever had - amazing variety and quality. The dinner restaurant was overpriced and the food was mediocre at best.",
    "The pool area is gorgeous with comfortable loungers. Unfortunately it's only 3 feet deep and closes at 6 PM, making it pretty useless.",
    "Excellent value for money, great amenities for the price. Though they nickel-and-dime you with $15 daily 'resort fees' and $8 bottles of water."
]

def naive_extractive_summary(reviews, top_n=3):
    """Naive approach: just extract the most positive-sounding sentences"""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
    all_text = " ".join(reviews)
    # Truncate to model's max length
    summary = summarizer(all_text[:1024], max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def sentiment_aware_summary(reviews):
    """Better approach: identify and preserve contradictions"""
    sentiment_analyzer = pipeline("sentiment-analysis", device=-1)
    
    summary_points = []
    
    for review in reviews:
        # Split each review into sentences to detect internal contradictions
        sentences = [s.strip() for s in review.split('.') if len(s.strip()) > 10]
        
        if len(sentences) < 2:
            continue
            
        sentiments = []
        for sent in sentences:
            try:
                result = sentiment_analyzer(sent[:512])[0]
                sentiments.

## Quick Quiz

**Question:** A pharmaceutical company needs to process 10,000 clinical trial reports to identify adverse drug reactions. They're deciding between extractive and abstractive summarization. Which consideration should most strongly guide their choice?

A) Abstractive summarization is always preferable because it produces more concise outputs and reduces storage requirements

B) Extractive summarization is safer because it preserves exact medical terminology and prevents the model from hallucinating clinical facts

C) The choice depends on whether they need verbatim regulatory compliance or interpretive synthesis—extractive guarantees source fidelity while abstractive enables cross-document insight generation

D) Extractive summarization should be used first to reduce document length, then abstractive summarization applied to generate the final summary

**Answer:** C

**Explanation:** The core distinction between extractive and abstractive approaches is not about quality or efficiency, but about the fundamental trade-off between **fidelity to source text** versus **generative flexibility**. Option C correctly identifies that extractive methods select actual sentences (critical for regulatory/legal contexts requiring exact phrasing), while abstractive methods can synthesize information across documents but risk introducing errors. Option A represents the misconception that "newer/fancier = better" without considering use-case requirements. Option B contains a kernel of truth about hallucination risk but oversimplifies by declaring extractive "always safer"—many applications benefit from abstractive synthesis despite this risk. Option D suggests a sequential hybrid approach that sounds sophisticated but misunderstands that these are alternative strategies for different goals, not sequential processing steps.

## Heuristics

**If your summary is shorter than 10% or longer than 40% of the original, recalibrate your compression target.**
Summaries below 10% compression typically sacrifice critical context and nuance, while those above 40% fail to meaningfully reduce cognitive load. The sweet spot for most business documents sits between 15-25% of original length, balancing information preservation with genuine brevity.

**When ROUGE scores exceed 0.6 on extractive summaries, you're just copying sentences—switch to abstractive methods.**
High ROUGE scores on extractive approaches indicate your model is selecting near-verbatim passages rather than distilling meaning. This works for news articles with self-contained sentences but fails for technical documents or narratives requiring synthesis. If extraction feels sufficient, question whether you need ML at all—simple lead-based selection might suffice.

**Don't summarise text shorter than 500 words unless you're building sentence-level abstracts for search.**
The overhead of summary generation—both computational and cognitive—rarely justifies itself on short content. Humans can skim 300-word emails faster than they can evaluate whether an AI summary is trustworthy. Reserve summarisation for documents where manual reading genuinely bottlenecks workflow.

**Evaluate summaries with domain experts on 30-50 documents before deployment; automated metrics lie convincingly.**
ROUGE, BLEU, and BERTScore correlate poorly with human judgments of summary quality, especially for factual accuracy and coherence. A model scoring 0.45 ROUGE-L might produce more useful summaries than one scoring 0.52 if it better captures causal relationships or avoids subtle hallucinations. Budget 2-3 hours of expert time for proper validation.

**If extractive and abstractive summaries disagree on key facts, your source document is probably ambiguous or contradictory.**
Treat divergence between methods as a signal rather than noise. Extractive methods anchor to specific sentences while abstractive methods synthesize across passages—when they conflict on main points, the underlying text likely contains unresolved tensions that human readers would also struggle with. Flag these for manual review rather than forcing consensus.

**Set maximum output length to 3x your target summary length to prevent truncation hallucinations.**
When models hit hard token limits mid-generation, they often fabricate conclusions or introduce incomplete thoughts. Configure decoders with comfortable headroom (e.g., 384-token max for 128-token target summaries), then trim post-generation. The computational cost is negligible compared to the risk of confident-sounding fabrications.

**For stakeholder reports, lead with what was removed, not just what remains.**
Non-technical audiences struggle to trust "black box" summaries without transparency about the compression process. A simple statement like "This 15-page report was reduced to 2 pages by removing detailed methodology, removing redundant examples, and condensing background context" builds more confidence than presenting summary output alone.

**Master practitioners maintain a rejection log—documents where summaries failed and why.**
Good practitioners chase higher ROUGE scores; great ones build institutional knowledge about model failure modes. Track documents where summaries missed critical information, hallucinated facts, or produced misleading emphasis patterns. Common failure categories include heavy use of pronouns without clear antecedents, sarcasm or irony, and documents where key information appears only in tables or footnotes. This log becomes your guard rail for production systems.

## Nuggets

**Extractive summarisation often outperforms abstractive on factual accuracy metrics.**
Large language models can generate fluent, coherent summaries that sound authoritative but introduce hallucinations—claims not present in the source text. A 2023 evaluation of GPT-3.5 and GPT-4 on news articles found factual error rates of 14-18% compared to 3-5% for extractive methods using sentence ranking algorithms. If you're summarising medical records, legal documents, or financial reports where precision matters more than readability, extractive approaches remain the safer default despite appearing less sophisticated.

**The "lead bias" in news data has crippled summarisation benchmarks for a decade.**
Most news articles follow the inverted pyramid structure, placing key information in opening sentences. Models trained on CNN/DailyMail or similar datasets learned to simply extract the first 2-3 sentences, achieving surprisingly high ROUGE scores without understanding document structure. When researchers tested these same models on scientific papers or narrative texts where conclusions appear at the end, performance collapsed by 30-40%. If your use case involves non-news text, benchmark results from standard datasets will mislead you about model capability.

**ROUGE score correlation with human judgement reverses above 0.4.**
ROUGE (the dominant automatic evaluation metric) measures n-gram overlap between generated and reference summaries. Below ROUGE-L scores of ~0.4, improvements correlate strongly with human preference ratings. But beyond this threshold, the relationship inverts: systems optimising for ROUGE start producing summaries packed with keyword matches but lacking coherent narrative flow. This happens because ROUGE cannot measure semantic cohesion or logical ordering. Deploy human evaluation before trusting any model claiming ROUGE-L > 0.45 on your specific domain.

**Compression ratio is not a hyperparameter—it's a domain-dependent constraint.**
Beginners treat target summary length as a tunable parameter. But research on cross-domain summarisation shows that different content types have inherent "information densities." Legal contracts require 15-20% compression ratios to preserve binding language; news articles can compress to 5% without losing core facts. Forcing a fixed compression ratio across document types either bloats trivial summaries or strips essential nuance from complex ones. Estimate appropriate ratios empirically from your domain before building production systems.

**Multi-document summarisation is qualitatively different, not just "harder" single-document summarisation.**
When summarising multiple sources, the core challenge shifts from content selection to contradiction resolution and perspective attribution. A 2022 study found that systems achieving 0.42 ROUGE on single documents dropped to 0.28 on multi-document tasks—not because documents were longer, but because models lacked mechanisms to track source provenance and reconcile conflicting claims. If your use case involves synthesising multiple viewpoints, you need architectures with explicit cross-document attention mechanisms, not just larger context windows.

**Human "reference summaries" are low-agreement, making supervised learning fundamentally noisy.**
When five humans independently summarise the same article, inter-annotator agreement (measured by ROUGE) typically falls between 0.35-0.50. This means even perfectly learning from one human's summary would score poorly against another's. This ceiling limits supervised approaches and explains why pre-trained models fine-tuned on small datasets often underperform prompt-engineered large language models that never saw task-specific training data.

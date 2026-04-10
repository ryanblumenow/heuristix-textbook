#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║       Heuristix Textbook — Chapter Enrichment Script (Pass 4)               ║
║                                                                              ║
║  Enriches all 173 chapters by detecting and adding any missing sections.    ║
║  Also adds three new sections not in the original generation pass:          ║
║    • Learning Objectives  — 3 clear outcomes per chapter                    ║
║    • Practice Exercises   — 2 hands-on exercises with solutions              ║
║    • Quick Quiz           — 1 concept-check question with explanation       ║
║                                                                              ║
║  For the 7 original sections often truncated in Pass 1:                     ║
║    • Using This in Heuristix                                                 ║
║    • Business Applications                                                   ║
║    • Worked Example                                                          ║
║    • Interpreting Your Results                                               ║
║    • Decision Guidance                                                       ║
║    • Common Pitfalls                                                         ║
║    • Further Reading                                                         ║
║                                                                              ║
║  Usage:                                                                      ║
║    python enrich_chapters.py                                                 ║
║                                                                              ║
║  Progress saved to .enrichment_progress.json — safe to Ctrl+C and resume.  ║
║  Estimated cost: ~$15–25 USD (Claude Sonnet, ~3 missing sections/chapter).  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os, json, time, re, sys

# Force UTF-8 stdout/stderr so em-dashes, bullets, box chars don't crash on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import anthropic

# ── Node registry (same as generate_chapters.py) ─────────────────────────────

NODES: dict[str, list[str]] = {
    "connect": ["Import Data", "Export Data"],
    "explore": [
        "Join", "Stack", "Multi Stack", "Filter Rows", "Pivot", "Clone",
        "Split", "Explode", "Union", "Append", "Aggregate", "Interaction",
        "Ratio", "Date Features", "Summarize Data", "Formula", "Rename",
        "Sort", "Deduplicate", "Drop Features", "Fill Missing",
        "Missing Imputation", "Type Cast", "Assign Unique ID", "Fixed Value",
        "Extract Substrings", "Replace Values", "Select Columns",
        "Window Features", "Conditional Features", "Value Mapping",
        "Collapse", "Padding", "Cleansing", "Observation Window",
        "Trend Recipe", "Shift", "Performance Window", "Event Target",
        "PySpark", "Text Features", "Analyze Sentiment",
        "Generate Synthetic Data", "Match Records", "Bin Features",
        "Select Features",
    ],
    "understand": [
        "Profile Data", "Detect Drift", "Ensemble Compete",
        "Identify Segments", "Analyze Trend", "Detect Anomaly",
        "Test Hypothesis", "Validate Model", "Compress Features",
        "Visualise Clusters", "Long-Run Relationship", "Model Rare Events",
        "Group Effects", "Decompose Trends", "Find Latent Factors",
        "Resample Confidence", "Analyse Networks", "Check Fairness",
        "Decompose Cycle", "Correct for Trends", "Find Co-occurrences",
        "Detect Change Points", "Analyse Geography", "Survival Curves",
        "Measure Correlation", "Model Elasticity", "Map Dependencies",
        "Model Distribution", "Find Hidden Groups", "Power Analysis",
        "Run Meta-Analysis",
    ],
    "predict": [
        "Predict", "Forecast", "Score", "Estimate Propensity",
        "Model a Value", "Linear Regression", "Polynomial Regression",
        "LSTM", "Time to Event", "Track Groups", "Combine Predictors",
        "Classify Records", "Deep Learning", "Find Similar",
        "Estimate Uncertainty", "Explain Predictions", "Tune Model",
        "Validate Reliability", "Uplift Model", "Recommend",
        "Forecast with Drivers", "Structural Break", "State Space",
        "Smart Forecast", "Detect Regimes", "Find Best Model",
        "Balance Classes", "Calibrate Predictions", "Model Response Curve",
        "Generalised Estimation", "Model Event Counts", "Model Volatility",
        "Gaussian Process", "Rank Items", "Estimate Lifetime Value",
        "Ordinal Outcome", "Detect Time Anomaly", "Conformal Predict",
        "Hierarchical Forecasting", "Nowcast", "Zero-Inflated Model",
        "Score Anomalies",
    ],
    "decide": [
        "Decision Rule", "Scenario", "Scenario Analysis", "Optimise",
        "Prioritise", "Simulate Risk", "Design Experiment", "Run Bandit Test",
        "Optimise Portfolio", "Quantify Risk", "Control Chart",
        "Model Transitions",
    ],
    "explain": [
        "Driver Analysis", "Attribution", "Compare", "Prove Causation",
        "Test Causation", "Counterfactual Analysis", "Cutoff Impact",
        "Measure Impact", "Remove Confounding", "Match Groups",
        "Correct Selection Bias", "Discover Causal Structure", "Event Study",
        "Build Synthetic Control", "Attribute Marketing Spend",
        "Spatial Regression", "Dynamic Panel", "Interrupted Time Series",
        "Trace Effect Over Time", "Heterogeneous Effects",
        "Unpack the Pathway", "Moderation Analysis", "Visualize",
    ],
    "augment": [
        "LLM Transform", "Encode Meaning", "Vector Search", "Ask Your Data",
        "Discover Topics", "Extract Entities", "Classify Text",
        "Fine-tune Model", "Manage Prompts", "Evaluate AI Output",
        "Extract Structure", "Analyse Images", "Summarise Text",
        "Analyse Documents",
    ],
    "act": ["Schedule", "Alert", "Report"],
}

BUCKET_TITLES: dict[str, str] = {
    "connect":    "Connect — Getting Data In & Out",
    "explore":    "Explore — Shaping & Transforming Data",
    "understand": "Understand — Statistical Analysis & Profiling",
    "predict":    "Predict — Machine Learning & Forecasting",
    "decide":     "Decide — Decision Intelligence",
    "explain":    "Explain — Causal Analysis & Interpretation",
    "augment":    "Augment — AI & Language Intelligence",
    "act":        "Act — Operationalising Results",
}

# ── Sections: which to detect + how to generate each ─────────────────────────

# Ordered list of (section_heading, prompt_template)
# The heading must match EXACTLY what appears in the chapter (## Heading)
SECTIONS: list[tuple[str, str]] = [

    # ── Understanding the Mathematics — plain-English equation explainer ────────

    ("## Understanding the Mathematics", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Understanding the Mathematics"** — a plain-English companion to the \
## The Mathematics section that appears earlier in this chapter. \
Your goal: a reader who felt lost reading the equations should finish this section feeling \
they genuinely understand what the maths is doing and why.

For EACH major equation or mathematical concept from the ## The Mathematics section, write \
a subsection (### heading) covering:

1. **The equation** — quote it exactly as written in the chapter (in LaTeX/markdown format)
2. **Read it aloud** — translate every symbol into words. Write out the full equation as a \
   sentence a non-mathematician could follow. For example: "This says: the predicted value \
   equals the intercept plus the slope multiplied by the input, plus some random noise."
3. **What each symbol means** — a brief table or bullet list mapping each variable/operator \
   to its plain-English meaning in the context of __NODE__
4. **A concrete numerical example** — plug in realistic numbers. Show the arithmetic \
   step by step (e.g., "If intercept = 50,000, slope = 150, and house size = 1,200 sqft, \
   then predicted price = 50,000 + 150 × 1,200 = 230,000"). \
   The numbers should come from a realistic business scenario.
5. **Why this equation matters** — one sentence connecting the equation to a practical \
   outcome: what would go wrong if we ignored this, or what does solving it enable us to do?

After covering all key equations, end with:

### The Big Picture
A paragraph (4–6 sentences) stepping back from the individual equations to explain: \
(1) what the mathematics is fundamentally trying to achieve for __NODE__, \
(2) why this particular mathematical approach was chosen (what property does it have that \
simpler alternatives lack?), and (3) one intuitive sentence that captures the mathematical \
essence without any symbols at all.

IMPORTANT RULES:
- Do NOT simplify or omit important equations — explain them, don't avoid them
- Use concrete numbers in every example — abstract "let x=a" examples are not acceptable
- Short sentences. Active voice. Write as a brilliant teacher, not a textbook.
- Assume the reader is intelligent but unfamiliar with the specific notation
- Write as ## Understanding the Mathematics (H2), with ### subsections per equation/concept
- Target 600–900 words. Start directly with the heading line."""),

    # ── How It Works — NEW visual/narrative section ───────────────────────────

    ("## How It Works", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## How It Works"** — a visual, step-by-step explanation of what __NODE__ does, \
written in plain English. This section must be the most accessible, engaging section in the chapter. \
A motivated non-technical manager should finish it feeling they truly understand the concept.

REQUIREMENTS (every single one must appear — these are not optional):

**1. Opening analogy (a short, vivid paragraph)**
Start with one powerful everyday analogy that makes the concept immediately click. \
Be creative and specific — avoid generic analogies. Give the analogy a full paragraph (3–5 sentences). \
Make it concrete: use names, numbers, familiar situations.

**2. ASCII art diagram (wrapped in a ``` code block, 10–20 lines)**
Create a diagram that visually shows what __NODE__ does — either the data transformation, \
the algorithm's search process, or the structure of the model. \
Use box-drawing characters (┌─┐│└┘├┤┬┴┼), arrows (→ ↓ ↑ ←), and clear labels. \
The diagram should show a before state, the process, and an after state wherever applicable.

Example style for a Join operation:
```
BEFORE                              AFTER (INNER JOIN on id)
Table A          Table B            ┌──────┬─────┬────────┐
┌──────┬─────┐  ┌──────┬────────┐  │  id  │ age │ salary │
│  id  │ age │  │  id  │ salary │  ├──────┼─────┼────────┤
├──────┼─────┤  ├──────┼────────┤  │   1  │ 25  │  50K   │
│  1   │ 25  │  │  1   │  50K   │  │   2  │ 30  │  60K   │
│  2   │ 30  │  │  2   │  60K   │  └──────┴─────┴────────┘
│  3   │ 22  │  │  4   │  45K   │  (row 3 and 4 dropped —
└──────┴─────┘  └──────┴────────┘   no matching id in both)
```

**3. Step-by-step walkthrough (numbered steps, plain English only)**
Walk through exactly what happens when __NODE__ runs, step by step (4–8 steps). \
Each step is one short paragraph. No equations — describe the computation as if explaining \
to a smart non-programmer. Start each step with an action verb.

**4. The key insight (bold, one sentence)**
End with: "**The key insight:** [one sentence capturing WHY this technique works, \
what fundamental principle it exploits, what makes it elegant or powerful]"

STRICT RULES:
- NO mathematical notation anywhere in this section
- NO jargon without immediate plain-English explanation
- Use short sentences and active voice throughout
- Write as ## How It Works (H2 heading)
- Target 400–550 words. Start directly with the heading line."""),

    # ── Original enrichment sections ─────────────────────────────────────────

    ("## Using This in Heuristix", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Using This in Heuristix"** — a practical, friendly platform guide. \
Write as if you are a helpful colleague walking someone through the tool for the first time. \
Be warm, specific, and practical — not a dry reference manual.

Cover:
- What data inputs to connect to this node (required column types, expected data shape — \
  with a small before/after table showing example data if helpful)
- Every configurable parameter: name, what it controls in plain English, sensible defaults, \
  when to change it and why. Use a markdown table.
- What the node outputs: columns added, metrics displayed, charts shown — describe each output \
  so the reader knows exactly what they will see
- How to connect this node to downstream nodes (which nodes typically follow, and why)
- 3–5 practical tips: things an experienced user knows that a beginner would not

Write as ## Using This in Heuristix (H2 heading), with ### subsections as needed.
Use markdown tables for parameter descriptions. Include a "Quick Start" subsection with \
a step-by-step recipe for the most common use case (numbered, action-oriented steps).
Target 500–700 words. Start directly with the heading line."""),

    ("## Business Applications", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Business Applications"** — 10–12 concrete, vivid, real-world use cases \
that make a business leader or aspiring data scientist think "I need this right now."

REQUIREMENTS:
- Organise by industry: financial services, retail, healthcare, insurance, manufacturing, \
  logistics, marketing, telecoms, energy, public sector, SaaS/tech
- Each application: 3–4 sentences covering (1) the business problem in plain language, \
  (2) exactly how __NODE__ solves it, (3) the quantified business outcome — include actual \
  numbers for at least 7 of the 10–12 use cases (e.g., "reduced false positives by 34%", \
  "$1.2M annual savings", "cut processing time from 4 days to 20 minutes", "lifted \
  click-through rate from 1.8% to 3.1%")
- Name a specific type of company (e.g., "a mid-sized UK mortgage lender", "an e-commerce \
  retailer with 2M SKUs") rather than generic "a company"
- Cover both the obvious applications and 2–3 surprising ones practitioners might not think of

Write as ## Business Applications (H2 heading). Use **bold industry subheadings**.
Be inspiring and specific — this section should make a business user think "we should be doing this."
Target 600–800 words. Start directly with the heading line."""),

    ("## Worked Example", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Worked Example"** as a NARRATIVE STORY — not a structured list. \
This should read like a Harvard Business School case study crossed with a data science tutorial. \
The reader should feel like they are watching an expert analyst solve a real problem.

Story structure:
1. **The Meeting** — open with a specific business scenario. Give the analyst a name \
   (e.g., "Sarah, a senior data scientist at Meridian Insurance"). Describe the business problem \
   as it was raised — what question was asked, why it mattered, what was at stake.
2. **The Data** — describe the dataset Sarah pulled together. Show a small example table \
   (4–5 rows, 4–5 columns) formatted in markdown. Mention the quirks and messiness of real data.
3. **The Setup** — walk through how Sarah configured the __NODE__ node. Make this feel natural, \
   not mechanical — include her thinking about why she chose certain settings.
4. **The Results** — show actual output numbers, formatted clearly. Walk through what the \
   numbers mean one by one. Use a markdown table or formatted output where it helps.
5. **The Insight** — the "aha moment": what did the analysis reveal that wasn't obvious before?
6. **The Decision** — what did the business actually do with this? What meeting did Sarah present \
   in? What decision was made? What happened next? Be specific about the outcome.
7. **What Sarah Would Do Differently** — one or two honest reflections on limitations or \
   things she would change if doing this again.

Include a SHORT Python code snippet (15–25 lines) that reproduces the core analysis.
The code should feel like Sarah's actual script, with her comments in it.
Target 700–900 words. Write as ## Worked Example (H2). Start directly with the heading line."""),

    ("## Interpreting Your Results", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Interpreting Your Results"** — the most practical section in the chapter. \
Imagine the reader has just run __NODE__ for the first time and is staring at a page of numbers \
and charts. They are asking: "What am I looking at? Is this good or bad? What do I do now?" \
Answer those questions directly, warmly, and specifically.

For EACH key output this node produces (metrics, scores, tables, charts, columns):
- **Plain-English meaning**: what is this number/chart actually telling you? Explain as if \
  you are talking to a smart colleague who has never seen this before.
- **Concrete benchmarks**: "Below 0.5 means... | 0.5–0.75 means... | Above 0.75 means..." \
  Give actual thresholds based on industry practice, not vague "higher is better" statements.
- **Red flags**: specific values, patterns, or combinations that should make you stop and \
  investigate. Name the actual problem each red flag indicates.
- **Reading multiple outputs together**: what combinations of metrics tell a more complete story?

Also include:
- A "**Sanity Check Checklist**" — 5 quick checks to run before trusting any result from this node
- A "**Good Enough to Act On?**" paragraph — the specific threshold at which you should stop \
  analysing and start deciding

Write as ## Interpreting Your Results (H2), with ### per major output type.
Be direct and specific — use actual numbers, actual thresholds, actual examples. No vagueness.
Target 600–800 words. Start directly with the heading line."""),

    ("## Decision Guidance", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Decision Guidance"** — translating results into action that a business \
leader or senior analyst can immediately use.

Structure:
### What This Result Is Telling You
2–3 paragraphs. Translate the technical output into a clear business message that a CEO or \
department head could understand. Use the language of business outcomes, not statistics.

### Decision Points
A markdown table (3–5 rows) mapping results to decisions:
| If you see this... | It means... | Recommended action | Who acts on this |
(be specific about thresholds and conditions — not "if the score is high")

### When to Proceed vs. Investigate Further
Bullet list of explicit criteria. Give concrete conditions for: "proceed with confidence", \
"proceed with caution", "investigate before acting", "do not use these results yet". \
Assign specific metric thresholds to each condition.

### The Cost of Getting This Wrong
A paragraph on what bad things actually happen when someone misinterprets these results. \
Be specific: what decision gets made, what resources get wasted, what opportunity gets missed. \
This should feel like a cautionary tale that makes the reader want to be careful.

Write as ## Decision Guidance (H2), with the ### subsections above.
Target 450–600 words. Start directly with the heading line."""),

    ("## Common Pitfalls", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Common Pitfalls"** — 7–9 mistakes told as cautionary tales from the field.

For each pitfall, structure it as a MINI CASE STUDY:
- **The Pitfall Name** (bold) — a memorable name for this mistake
- **The Story**: "Here is what happened: [analyst type] was working on [scenario]. They [made \
  mistake X]. The output showed [Y]. They concluded [Z]." Keep it concrete and specific.
- **Why it happens** — the cognitive trap or technical misunderstanding that causes this
- **How to detect it** — the specific signal that tells you this has happened (reference \
  actual metric names and values)
- **The fix** — one or two sentences on how to correct course

Cover mistakes from: (a) business users who misread charts, (b) junior data scientists who \
know the theory but skip validation, (c) experienced practitioners who cut corners.

Write as ## Common Pitfalls (H2). Use bold pitfall names as subheadings. \
Make this section feel like war stories from a senior mentor — practical wisdom, not textbook rules.
Target 600–800 words. Start directly with the heading line."""),

    ("## Further Reading", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Further Reading"** — 8 carefully curated references that will \
genuinely deepen a reader's understanding.

Include a mix of:
- 2 seminal academic papers (author, year, venue — and a sentence on the specific insight \
  they contribute, written as "Read this if you want to understand [X]")
- 2 textbook references (title, author, specific chapter/pages — why THIS chapter in \
  particular, not just "the whole book")
- 1 sklearn/statsmodels/scipy documentation page (the most relevant class or function, \
  with the specific thing to look at)
- 1 high-quality blog post or tutorial (Towards Data Science, fast.ai, StatQuest, etc. — \
  describe what makes this one better than the dozens of others on the topic)
- 1 video lecture or course (with timestamps if a specific segment is most relevant)
- 1 real-world case study or industry report showing this technique applied at scale

For each: cite it in a consistent format and write 1–2 sentences on what specific insight \
the reader will gain — not just "this covers the topic" but "this will teach you [specific thing]".

Write as ## Further Reading (H2). Use a numbered list.
Target 350–450 words. Start directly with the heading line."""),

    # ── New sections not in original Pass 1 ───────────────────────────────────

    ("## Learning Objectives", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Learning Objectives"** — a clear, honest roadmap of what this chapter \
teaches. Write it in a way that makes the reader feel motivated to read on: frame objectives as \
skills and capabilities they will gain, not abstract learning outcomes.

List exactly 6 learning objectives in two groups:

**After reading this chapter, a business user will be able to:**
- [Objective 1: recognise when __NODE__ applies to their problem — specific business scenarios]
- [Objective 2: interpret the outputs and explain what they mean to stakeholders]
- [Objective 3: make a specific type of decision or take a specific action using results]

**After reading this chapter, a data scientist will be able to:**
- [Objective 4: implement __NODE__ correctly, including handling edge cases]
- [Objective 5: tune the key parameters with understanding of the trade-offs]
- [Objective 6: validate results and diagnose common failure modes]

Each objective must start with an action verb and be specific enough that you could design \
a test question to verify it. Avoid vague verbs like "understand" or "know about".

Write as ## Learning Objectives (H2). Keep each bullet to one clear sentence.
Start directly with the heading line."""),

    ("## Practice Exercises", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Practice Exercises"** — 3 exercises that build genuine skill.

**Exercise 1 (Conceptual — Business User, no code required)**
Present a realistic business scenario with specific numbers and context. \
The reader must decide: (a) whether to use __NODE__ or an alternative, (b) how to interpret \
a given result, or (c) what action to recommend. \
Provide a complete, detailed worked answer that explains the reasoning step by step. \
The scenario should feel like something from a real job.

**Exercise 2 (Applied — Data Scientist)**
A coding exercise with a complete setup. Provide:
(a) A clear, specific task description with a real business motivation
(b) A self-contained Python dataset setup (15–20 lines, runnable immediately)
(c) Exactly what the student must implement, analyse, or answer
(d) A complete worked solution with actual output values shown in comments, \
    followed by a 3–5 sentence interpretation of the results in business terms.

**Exercise 3 (Challenge — Advanced)**
A harder problem that requires genuine understanding: a tricky edge case that breaks naive \
approaches, a comparison between two competing methods, or an application to messy/realistic \
data. Full solution with explanation of why the naive approach fails and the correct approach works.

Write as ## Practice Exercises (H2), with ### Exercise 1, 2, 3 subheadings.
Include complete solutions — not hints. Use python code blocks. \
Target 700–900 words. Start directly with the heading line."""),

    ("## Quick Quiz", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Quick Quiz"** — one carefully crafted question that tests real understanding.

**Question design requirements:**
- The question must be answerable ONLY if the reader genuinely understood the chapter — \
  not solvable by Googling the term or guessing by elimination
- Ideally, it tests the most common misconception about __NODE__, or the insight that \
  separates competent practitioners from novices
- All four options must be plausible — a reader who half-understood the chapter should \
  genuinely pause on 2–3 of them

**Format:**
**Question:** [The question]

A) [Plausible distractor]
B) [Plausible distractor]
C) [Correct answer]
D) [Plausible distractor]

**Answer:** C

**Explanation:** [3–4 sentences. Explain WHY C is correct with specifics. Explain why \
each distractor is wrong and what misconception it represents. Reference the key concept \
from the chapter that the question is testing.]

Write as ## Quick Quiz (H2). Start directly with the heading line."""),

    # ── Pass 5 sections — deeper enrichment ───────────────────────────────────

    ("## The 60-Second Version", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## The 60-Second Version"** — the entry point for time-pressed readers. \
Write this as if you had 60 seconds in a lift to explain __NODE__ to an intelligent but \
non-technical executive. Every word must earn its place.

Answer these three questions in plain English:
1. **What it does:** One sentence. No jargon. No qualifications.
2. **When to use it:** One sentence describing the business situation that triggers this.
3. **What you get back:** One sentence on the output and how you act on it.

Then an "At a Glance" table:
| | |
|---|---|
| **Difficulty** | [Easy / Moderate / Advanced] |
| **Typical runtime** | [e.g., seconds on 100K rows] |
| **What you bring** | [a brief description of required input] |
| **What you get** | [a brief description of output] |
| **Heuristix bucket** | __BUCKET__ |

End with one bold sentence: the single thing a non-technical stakeholder MUST understand \
about __NODE__ to use it responsibly.

Write as ## The 60-Second Version (H2). Target 130–170 words. Start directly with the heading line."""),

    ("## Questions This Answers", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Questions This Answers"** — a list of the business questions \
__NODE__ was built to answer, written exactly as a real business person would ask them.

Requirements:
- 10–14 questions total
- Phrased as someone would actually say them in a board meeting or strategy session — \
  not as a data scientist would frame them
- Concrete and specific: include relevant numbers, timeframes, or contexts where it helps
- Cover: diagnostic questions (what happened?), predictive questions (what will happen?), \
  prescriptive questions (what should we do?), and comparative questions (which is better?)

Good: "Why did our South region underperform by 18% last quarter — is it a market issue or a team issue?"
Bad: "What are the significant predictor variables for the target column?"

Group under 2–3 meaningful theme headings.

Write as ## Questions This Answers (H2). Use bold for each question, no explanations needed.
Target 270–380 words. Start directly with the heading line."""),

    ("## How This Connects", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## How This Connects"** — a workflow guide helping the reader build \
__NODE__ into complete, working pipelines.

Structure:
### Before This Node
List 4–6 specific Heuristix nodes that commonly feed into __NODE__. For each, write one sentence: \
what does that upstream node contribute, and why does it matter for __NODE__ to work correctly? \
Include a note on what BAD upstream data looks like and what goes wrong.

### After This Node
List 4–6 specific Heuristix nodes that commonly follow __NODE__. For each, write one sentence: \
what does that downstream node do with __NODE__'s output, and why is __NODE__'s output \
well-suited to feeding into it?

### Common Pipeline Patterns
Three named, realistic workflows. Each should be:
- **Pattern name** (e.g., "Customer Lifetime Value Pipeline")
- Node chain: Node A → Node B → **__NODE__** → Node C → Node D (bold the __NODE__ step)
- One sentence: the business goal and approximate outcome this pipeline achieves

### What to Have Ready
A "Prerequisites checklist" — 3–4 specific things a user should have sorted before running \
__NODE__ (data quality, column types, business question defined, baseline model, etc.). \
Be concrete about what "ready" actually means.

Write as ## How This Connects (H2) with the ### subsections above.
Target 400–550 words. Start directly with the heading line."""),

    ("## Common Misconceptions", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Common Misconceptions"** — 5 beliefs about __NODE__ that are confidently \
held but dangerously wrong. This section should feel like the most experienced person in the room \
quietly correcting years of accumulated bad thinking.

For each misconception:
- **"[State the wrong belief as someone would actually say it — in quotes]"** (bold)
- **Why people believe this:** The logical-seeming but incorrect reasoning behind it. \
  Acknowledge why it feels right — do not dismiss the person holding it.
- **The truth:** The correct understanding, explained with enough depth that it actually changes \
  how someone thinks. Do not just contradict — explain the underlying principle.
- **The real-world consequence:** A specific example of what goes wrong when someone acts on \
  this misconception. What decision do they make? What resource do they waste? What do they miss?

Cover misconceptions from: business stakeholders, junior data scientists, and experienced \
practitioners who have internalised bad habits from years of practice.

Write as ## Common Misconceptions (H2) with bold misconception quotes as subheadings.
Target 450–600 words. Start directly with the heading line."""),

    ("## Try It Yourself", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Try It Yourself"** — a hands-on starter that gets the reader from zero \
to working results in under 10 minutes.

### Recommended Dataset
Name one specific, freely available dataset ideal for exploring __NODE__. Specify:
- Dataset name and exact source (sklearn.datasets.load_X(), seaborn.load_dataset('X'), \
  a UCI repo link, or Kaggle dataset name)
- Why it is a particularly good fit for __NODE__ — what property of the data makes it ideal?
- The business question this dataset lets you explore with __NODE__
- Size (approximate rows × columns)

### Starter Code
A complete, self-contained Python script (35–55 lines) that:
- Loads or generates the dataset (use sklearn/seaborn built-ins wherever possible — \
  avoid requiring downloads)
- Runs __NODE__'s core technique end-to-end
- Prints 4–6 meaningful outputs with clear labels
- Has a comment on every non-obvious line explaining what it does and why
- Shows at least one output the reader can interpret as a business insight

All imports from standard DS libraries only (pandas, numpy, sklearn, scipy, matplotlib, statsmodels).

### What to Try Next
4 specific experiments the reader can do by changing one thing in the code. For each: \
what to change, what to expect, and what that experiment teaches.

Write as ## Try It Yourself (H2) with the ### subsections above.
Target 450–600 words. Start directly with the heading line."""),

    ("## Config Recipes", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Config Recipes"** — a practical configuration guide for common scenarios. \
Think of this as the "cookbook" section: no explanation of theory, just "here is exactly what \
to set and when."

Provide 4 named recipes, each representing a genuinely different use case:

**Recipe 1: [Descriptive name — e.g., "Quick Exploration"]**
- **When to use:** [One specific scenario this is designed for]
- **Settings:** A small markdown table with parameter → value → why for each setting
- **What you get:** One sentence on the output characteristics
- **Trade-off:** One sentence on what you give up

[Repeat for Recipes 2, 3, 4]

Make the four recipes cover: (a) fastest/lightest for exploration, (b) most rigorous for \
production, (c) a specific use case where defaults would be wrong, (d) a scenario most \
practitioners would not think of but where __NODE__ is surprisingly effective.

Give ACTUAL parameter values — not "increase this" but "set to 0.01" or "use n_estimators=500".

Write as ## Config Recipes (H2) with ### subheadings per recipe.
Target 400–550 words. Start directly with the heading line."""),

    # ── Pass 6 sections — heuristics and nuggets ──────────────────────────────

    ("## Heuristics", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Heuristics"** — the distilled practical wisdom of experienced practitioners. \
These are the mental shortcuts, rules of thumb, and hard-won principles that experts carry in their \
heads and reach for automatically. Not theory — instinct that has been calibrated by experience.

Write 8 heuristics. Each one must be:
- **Memorable** — phrased as a short, crisp rule someone could repeat in a meeting from memory \
  (e.g., "If your AUC is above 0.95 on the first try, check for data leakage before celebrating.")
- **Specific to __NODE__** — not generic data science advice, but a rule that is uniquely relevant \
  to this particular technique
- **Actionable** — a practitioner should know exactly what to do (or not do) based on this heuristic
- **Calibrated** — include concrete thresholds, ratios, or magnitudes wherever possible \
  (e.g., "Start with at least 30 observations per group before trusting group-level estimates")

Format for each heuristic:
**[Short memorable rule — one sentence, max 20 words]**
[2–3 sentences explaining the intuition behind the rule, when it applies, and any important exceptions.]

The 8 heuristics should collectively cover: choosing settings/parameters, recognising when results \
are trustworthy vs. suspect, knowing when NOT to use __NODE__, reading results quickly, \
communicating findings to stakeholders, computational efficiency, and at least one heuristic \
about what separates a good practitioner from a mediocre one.

Write as ## Heuristics (H2). Start directly with the heading line.
Target 500–650 words."""),

    ("## Nuggets", """\
You are writing a section of the Heuristix Data Science Textbook for the chapter on **__NODE__** \
(__BUCKET__).

Write the section **"## Nuggets"** — surprising, counterintuitive, and underappreciated facts \
about __NODE__ that separate experts from beginners. These are the things experienced practitioners \
wish someone had told them early in their career. The insights that make a reader stop and think \
"I did not know that."

Write 6 nuggets. Each one must be:
- **Genuinely surprising** — not obvious, not what a careful reader of the documentation would \
  immediately infer. If a thoughtful beginner would already know it, it is not a nugget.
- **Specific** — grounded in a particular behaviour, result, dataset type, or real-world observation. \
  No generalities.
- **Intellectually honest** — if the nugget challenges a popular belief, be specific about \
  the evidence or reasoning. Do not manufacture controversy.
- **Practically relevant** — the reader should be able to use this insight to do something \
  better, avoid a mistake, or make a better decision

Good example style (for a different topic): \
"**More data beats better models — until it doesn't.** Studies on benchmark datasets consistently \
show that doubling training data improves accuracy more than switching from logistic regression to \
gradient boosting. But beyond ~50K samples, the relationship inverts: careful feature engineering \
and regularisation start to matter more than raw data volume."

Format for each nugget:
**[Short, punchy title — the claim that surprises, 5–12 words]**
[3–5 sentences expanding on the claim: the evidence or reasoning behind it, the practical \
implication, and any nuance or caveat a careful thinker would want to know.]

The 6 nuggets should collectively span: counterintuitive mathematical properties, surprising \
empirical results from research, underappreciated edge cases, common assumptions that are wrong, \
historical context that changes how you see the technique, and something about how human \
intuition specifically fails with __NODE__.

Write as ## Nuggets (H2). Start directly with the heading line.
Target 450–600 words."""),
]

SECTION_HEADINGS = [s[0] for s in SECTIONS]

# ── Utilities ─────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def chapter_path(bucket: str, node: str) -> str:
    return os.path.join(
        os.path.dirname(__file__), "chapters", bucket, f"{slugify(node)}.md"
    )


def get_api_key() -> str | None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    for secrets_path in [
        os.path.join(os.path.dirname(__file__), "..", ".streamlit", "secrets.toml"),
        os.path.expanduser("~/.streamlit/secrets.toml"),
    ]:
        try:
            if not os.path.exists(secrets_path):
                continue
            content = open(secrets_path).read()
            for line in content.splitlines():
                line = line.strip()
                if line.upper().startswith("ANTHROPIC_API_KEY"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
        except Exception:
            pass
    try:
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("ANTHROPIC_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return None


def load_progress(path: str) -> set[str]:
    try:
        with open(path) as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_progress(path: str, done: set[str]) -> None:
    with open(path, "w") as f:
        json.dump(sorted(done), f, indent=2)


def sections_present(content: str) -> set[str]:
    """Return the set of section headings (## ...) present in the chapter."""
    found = set()
    for heading in SECTION_HEADINGS:
        # Match heading at start of line, case-insensitively, with or without trailing spaces
        pattern = r"(?m)^" + re.escape(heading.strip()) + r"\s*$"
        if re.search(pattern, content, re.IGNORECASE):
            found.add(heading)
    return found


def generate_section(
    client: anthropic.Anthropic,
    node_name: str,
    bucket: str,
    section_heading: str,
    prompt_template: str,
    existing_overview: str,
) -> str:
    """Generate a single missing section for a chapter."""
    prompt = (
        prompt_template
        .replace("__NODE__", node_name)
        .replace("__BUCKET__", BUCKET_TITLES[bucket])
    )
    # Add existing overview as context so Claude knows what the chapter is about
    if existing_overview:
        context = f"\n\nFor context, here is the Overview section of the chapter:\n\n{existing_overview}\n\n---\n\n"
        prompt = prompt.replace("You are writing", context + "You are writing")

    for attempt in range(3):
        try:
            resp = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text.strip()
        except Exception as e:
            err = str(e)
            if "rate_limit" in err.lower() or "529" in err or "overloaded" in err.lower():
                wait = 60 * (attempt + 1)
                print(f"      Rate limit/overload — waiting {wait}s …")
                time.sleep(wait)
            elif attempt < 2:
                print(f"      Error (attempt {attempt+1}): {e} — retrying in 15s …")
                time.sleep(15)
            else:
                print(f"      Failed after 3 attempts: {e}")
                return ""
    return ""


def extract_overview(content: str) -> str:
    """Pull out the ## Overview section to use as context."""
    m = re.search(r"## Overview\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if m:
        return m.group(1).strip()[:800]  # cap at 800 chars for prompt economy
    return ""


# ── Insertion logic ───────────────────────────────────────────────────────────

# The order sections should appear in the final chapter
SECTION_ORDER = [
    "## The 60-Second Version",
    "## Learning Objectives",
    "## Overview",
    "## When to Use This",
    "## Questions This Answers",
    "## How It Works",
    "## The Intuition",
    "## The Mathematics",
    "## Understanding the Mathematics",
    "## Python Implementation",
    "## Visualisations",
    "## Using This in Heuristix",
    "## Config Recipes",
    "## Business Applications",
    "## Worked Example",
    "## Interpreting Your Results",
    "## Decision Guidance",
    "## Common Pitfalls",
    "## Common Misconceptions",
    "## How This Connects",
    "## Try It Yourself",
    "## Further Reading",
    "## Practice Exercises",
    "## Quick Quiz",
]


def insert_section(content: str, new_heading: str, new_body: str) -> str:
    """Insert a new section at the correct position in the chapter."""
    # Determine the target index in SECTION_ORDER
    try:
        target_idx = SECTION_ORDER.index(new_heading)
    except ValueError:
        # Unknown section — just append
        return content.rstrip() + "\n\n" + new_body + "\n"

    # Find the first existing section that comes AFTER target in SECTION_ORDER
    insert_before = None
    for later_heading in SECTION_ORDER[target_idx + 1:]:
        pattern = r"(?m)^" + re.escape(later_heading.strip()) + r"\s*$"
        m = re.search(pattern, content, re.IGNORECASE)
        if m:
            insert_before = m.start()
            break

    if insert_before is not None:
        return content[:insert_before].rstrip() + "\n\n" + new_body + "\n\n" + content[insert_before:]
    else:
        return content.rstrip() + "\n\n" + new_body + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    api_key = get_api_key()
    if not api_key:
        print("ERROR: No Anthropic API key found.")
        print("Set ANTHROPIC_API_KEY environment variable or add to .streamlit/secrets.toml")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    progress_path = os.path.join(os.path.dirname(__file__), ".enrichment_progress.json")
    done: set[str] = load_progress(progress_path)

    # Count totals
    total_nodes = sum(len(v) for v in NODES.values())
    total_tasks = total_nodes * len(SECTIONS)
    completed_tasks = len(done)
    print(f"\n{'='*70}")
    print(f"  Heuristix Textbook Enrichment — Pass 4")
    print(f"  {total_nodes} chapters × {len(SECTIONS)} sections = {total_tasks} tasks")
    print(f"  Already done: {completed_tasks} / {total_tasks}")
    print(f"{'='*70}\n")

    errors: list[str] = []
    chapters_updated = 0

    for bucket, nodes in NODES.items():
        for node_name in nodes:
            slug = slugify(node_name)
            path = chapter_path(bucket, node_name)

            if not os.path.exists(path):
                print(f"  [SKIP] {bucket}/{slug} — file not found")
                continue

            with open(path, encoding="utf-8") as f:
                original = f.read()

            present = sections_present(original)
            overview = extract_overview(original)
            content = original
            chapter_updated = False

            for section_heading, prompt_template in SECTIONS:
                task_key = f"{bucket}/{slug}/{section_heading}"
                if task_key in done:
                    continue  # already enriched
                if section_heading in present:
                    # Section exists — mark as done, skip
                    done.add(task_key)
                    save_progress(progress_path, done)
                    continue

                # Generate the missing section
                print(f"  [{bucket}] {node_name} — generating {section_heading} …")
                new_body = generate_section(
                    client, node_name, bucket, section_heading,
                    prompt_template, overview
                )

                if not new_body:
                    errors.append(f"{bucket}/{slug} — {section_heading}")
                    continue

                # Insert into chapter at correct position
                content = insert_section(content, section_heading, new_body)
                done.add(task_key)
                chapter_updated = True
                save_progress(progress_path, done)

                time.sleep(1.0)  # be polite to the API

            if chapter_updated:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                chapters_updated += 1
                print(f"    [OK] Saved {bucket}/{slug}.md")

    print(f"\n{'='*70}")
    print(f"  Enrichment complete.")
    print(f"  Chapters updated: {chapters_updated}")
    if errors:
        print(f"  Failed sections ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")
    print(f"{'='*70}\n")
    print("Next step: rebuild the book with:")
    print("  cd textbook && jupyter-book build . --all")


if __name__ == "__main__":
    main()

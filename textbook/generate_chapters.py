#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           Heuristix Data Science Textbook — Chapter Generator               ║
║                                                                              ║
║  Generates all 174 textbook chapters using the Anthropic Claude API.         ║
║  Each chapter is a publication-quality Jupyter Book markdown file covering:  ║
║    • Overview & when to use                                                   ║
║    • Plain-English intuition with analogies                                   ║
║    • Full mathematical treatment with LaTeX                                   ║
║    • Complete Python implementation (runnable code)                           ║
║    • Heuristix platform configuration guide                                   ║
║    • Real-world business applications across industries                       ║
║    • End-to-end worked example                                                ║
║    • Interpreting your results (what does it all mean?)                       ║
║    • Decision guidance (what do I do about it?)                               ║
║    • Common pitfalls                                                          ║
║    • Further reading                                                          ║
║                                                                              ║
║  Usage:                                                                       ║
║    pip install anthropic                                                      ║
║    export ANTHROPIC_API_KEY=sk-ant-...                                        ║
║    python generate_chapters.py                                                ║
║                                                                              ║
║  Progress is saved to .generation_progress.json — safe to Ctrl+C and resume. ║
║  Estimated cost: ~$25–45 USD for all 174 chapters (Claude Opus, 8k tokens).  ║
║  Estimated time: ~3–5 hours.                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import re
import sys
import anthropic

# ── Complete node registry, organised by bucket ──────────────────────────────

NODES: dict[str, list[str]] = {
    "connect": [
        "Import Data",
        "Export Data",
    ],
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
    "act": [
        "Schedule", "Alert", "Report",
    ],
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

# ── Chapter prompt template ───────────────────────────────────────────────────

CHAPTER_PROMPT = """\
You are a world-class data science educator and author writing a chapter for the \
**Heuristix Data Science Platform Textbook** — a professional reference and training \
resource used by:

- Business analysts and data professionals using the Heuristix platform in production
- Junior data scientists and academy students learning the craft on live business problems
- Senior practitioners who need a concise, authoritative reference

Write a **comprehensive, publication-quality** chapter on **__NODE_NAME__** for the \
**__BUCKET_TITLE__** section of the textbook.

This is a serious academic and professional textbook. Do NOT simplify or skip the \
mathematics. Do NOT write a blog post. Write as a textbook author who respects their \
reader's intelligence.

---

## Structure

Write the chapter with the following sections in order. Each section must be thorough.

### 1. Overview (H2: `## Overview`)
2–3 sentences. What does this technique do? What is its core purpose? What family of \
methods does it belong to?

### 2. When to Use This (H2: `## When to Use This`)
A bulleted list of 6–10 concrete scenarios where this is the right tool. Each bullet \
should have a brief business context explanation, not just a one-word label. Include \
both "use this when..." and "do NOT use this when..." guidance.

### 3. The Intuition (H2: `## The Intuition`)
Plain-English explanation with a memorable real-world analogy. Build genuine conceptual \
understanding before introducing any maths. This section should make the reader feel \
they truly understand *why* the technique works. Minimum 3 paragraphs.

### 4. The Mathematics (H2: `## The Mathematics`)
Full formal mathematical treatment. This section must include:
- Formal problem setup and notation definitions
- All key equations in LaTeX display math ($$...$$)
- Assumptions of the method — explicit and stated clearly
- The objective function and how it is optimised (if applicable)
- Derivations of key results where they are illuminating
- Edge cases and degenerate conditions
- Relationships to other methods where relevant

Write for a reader with undergraduate-level statistics and linear algebra. Do not skip \
steps in derivations. This section should be genuinely rigorous.

### 5. Python Implementation (H2: `## Python Implementation`)
A complete, self-contained, runnable Python code example using standard libraries \
(scikit-learn, statsmodels, pandas, numpy, scipy, etc.). The code must:
- Include realistic synthetic or standard dataset setup
- Fit the model / run the procedure end-to-end
- Print or display meaningful output
- Include inline comments explaining each key step
- Demonstrate how to interpret the outputs

Use triple-backtick python code blocks. Include multiple examples where the method \
has meaningfully different configurations.

### 6. Using This in Heuristix (H2: `## Using This in Heuristix`)
Practical platform guide:
- What data inputs to connect to this node (and required column types)
- What configuration parameters exist and what each one controls
- What to expect in the output (columns, metrics, charts)
- How to connect this node to downstream nodes effectively
- Platform-specific tips, warnings, and best practices
- Example configuration for a typical use case

### 7. Business Applications (H2: `## Business Applications`)
8–12 concrete real-world use cases, organised by industry where possible. Each \
application should be 2–3 sentences describing: the business problem, how this \
technique solves it, and what the business outcome is. Cover diverse industries: \
financial services, retail, healthcare, insurance, manufacturing, logistics, \
marketing, telecommunications, energy, public sector.

### 8. Worked Example (H2: `## Worked Example`)
A complete, realistic end-to-end example:
1. **Business Problem** — describe the real business question being answered
2. **Dataset** — describe the data (can be hypothetical but must be realistic and specific)
3. **Analysis Setup** — how to configure and connect the node
4. **Running the Analysis** — what happens when the workflow executes
5. **Interpreting the Results** — walk through the output carefully
6. **Business Decision** — what action does the business take based on this analysis?
7. **Caveats** — what assumptions are we making? what could go wrong?

### 9. Interpreting Your Results (H2: `## Interpreting Your Results`)
This is one of the most important sections. After running this node, the user will see \
output metrics, tables, or charts. Walk them through exactly what those outputs mean.

For EACH key output this node produces (metrics, scores, tables, plots):
- **What the number/output actually means** — not a technical definition, a plain-English \
  explanation. If the output is an accuracy score of 0.87, explain what 87 correct predictions \
  in 100 actually means for a business user.
- **What "good" looks like** — provide concrete benchmarks or thresholds that distinguish \
  excellent, acceptable, and poor results for this type of analysis.
- **Red flags to watch for** — what output values or patterns should make the user suspicious? \
  (e.g., accuracy = 1.00 usually means data leakage, not perfection)
- **How to read the outputs in combination** — many nodes produce multiple metrics that must \
  be interpreted together, not in isolation.

This section must be highly practical. Imagine the user is looking at their results right now \
and asking: *"What does this all mean? What am I looking at?"* Answer that question directly.

### 10. Decision Guidance (H2: `## Decision Guidance`)
The purpose of every analysis is a decision. This section answers: *"What do I do about it?"*

Structure this section as follows:

#### What this result is telling you
1–2 paragraphs translating the technical output into a clear business message. What is the \
analysis saying, in the language of someone who needs to act on it?

#### Decision points
A table or structured list covering 3–5 key decision points this node enables. For each:
- **The decision** — what choice the analyst or business must make
- **The signal to look for** — what specific output value or pattern indicates each path
- **The recommended action** — what to do next (including what Heuristix node to connect next)
- **Who owns this decision** — which stakeholder should be involved

#### When to proceed vs. investigate further
Explicit guidance on when the results are "good enough to act on" versus when the analyst \
should go back and investigate further. This is critical — overconfidence in weak results \
is a major source of business risk.

#### The business impact of getting this wrong
What is the cost of misinterpreting this result? What decisions made on incorrect outputs \
could lead to? Be concrete about the stakes.

### 11. Common Pitfalls (H2: `## Common Pitfalls`)
6–9 things that commonly go wrong. For each, explain:
- What the mistake is
- Why it happens
- How to detect it
- How to fix it

Format as a numbered or bulleted list with clear subheadings.

### 12. Further Reading (H2: `## Further Reading`)
5–7 references: seminal papers, textbook chapters, documentation, and online courses. \
Format as a proper reference list. Include the year, authors, and a one-sentence \
description of why it is worth reading.

---

## Formatting Requirements

- Write as **MyST Markdown** for Jupyter Book
- Use `$$...$$` for LaTeX display math (one expression per block)
- Use `$...$` for inline math
- Use triple-backtick `python` for code blocks
- Use `:::{note} ... :::` for notes
- Use `:::{warning} ... :::` for warnings
- Use `:::{tip} ... :::` for tips
- Use `# __NODE_NAME__` as the top-level title
- Use `##` for the section headers listed above
- Use `###` for subsections within sections
- Tables where appropriate (especially for parameter descriptions)
- This is a long chapter — target **3,000–4,500 words** of content (the two new sections \
  on interpreting results and decision guidance are essential and must be thorough)
- Do not include a table of contents — Jupyter Book generates this automatically

---

Now write the complete, publication-quality chapter for **__NODE_NAME__**, starting with \
`# __NODE_NAME__`.
"""

# ── Utilities ─────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """Convert a node name to a URL-safe slug."""
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def chapter_path(bucket: str, node: str) -> str:
    return os.path.join(
        os.path.dirname(__file__), "chapters", bucket, f"{slugify(node)}.md"
    )


def get_api_key() -> str | None:
    """Try several common locations for the Anthropic API key."""
    # 1. Environment variable
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    # 2. Streamlit secrets — check both project-local and user-level
    for secrets_path in [
        os.path.join(os.path.dirname(__file__), "..", ".streamlit", "secrets.toml"),
        os.path.expanduser("~/.streamlit/secrets.toml"),
    ]:
        try:
            if not os.path.exists(secrets_path):
                continue
            content = open(secrets_path).read()
            # Simple key=value parse (handles both toml and plain text)
            for line in content.splitlines():
                line = line.strip()
                if line.upper().startswith("ANTHROPIC_API_KEY"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
        except Exception:
            pass
    # 3. .env file in repo root
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


# ── Main generator ────────────────────────────────────────────────────────────

def generate_chapter(client: anthropic.Anthropic, node_name: str, bucket: str) -> str:
    """Call Claude to generate a full textbook chapter for a node."""
    # Use simple string replacement instead of .format() to avoid conflicts
    # with MyST markdown curly-brace syntax like {note}, {warning}, {tip}
    prompt = (
        CHAPTER_PROMPT
        .replace("__NODE_NAME__", node_name)
        .replace("__BUCKET_TITLE__", BUCKET_TITLES[bucket])
    )
    response = client.messages.create(
        model="claude-opus-4-5",       # Opus for publication-quality content
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def main() -> None:
    api_key = get_api_key()
    if not api_key:
        print(
            "ERROR: Anthropic API key not found.\n"
            "Set ANTHROPIC_API_KEY environment variable:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...\n"
            "Or add it to ~/.streamlit/secrets.toml as ANTHROPIC_API_KEY = '...'"
        )
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Load progress tracking
    progress_file = os.path.join(os.path.dirname(__file__), ".generation_progress.json")
    if os.path.exists(progress_file):
        with open(progress_file) as f:
            completed: set[str] = set(json.load(f))
        print(f"Resuming from previous run — {len(completed)} chapters already done.")
    else:
        completed = set()

    # Count totals
    total = sum(len(nodes) for nodes in NODES.values())
    remaining = total - len(completed)

    print(f"\nHeuristix Textbook Generator")
    print("-" * 50)
    print(f"Total chapters:     {total}")
    print(f"Already generated:  {len(completed)}")
    print(f"To generate:        {remaining}")
    print(f"Model:              claude-opus-4-5")
    print(f"Est. cost:          ~${remaining * 0.20:.0f}-${remaining * 0.30:.0f} USD")
    print(f"Est. time:          ~{remaining * 60 // 60}-{remaining * 100 // 60} minutes")
    print("-" * 50 + "\n")

    if remaining == 0:
        print("All chapters already generated!")
        print("Run:  jupyter-book build textbook/")
        return

    errors: list[str] = []

    for bucket, node_list in NODES.items():
        bucket_dir = os.path.join(os.path.dirname(__file__), "chapters", bucket)
        os.makedirs(bucket_dir, exist_ok=True)

        print(f"\n{'=' * 50}")
        print(f"  {BUCKET_TITLES[bucket]}")
        print(f"{'=' * 50}")

        for node_name in node_list:
            key = f"{bucket}/{slugify(node_name)}"
            path = chapter_path(bucket, node_name)

            if key in completed:
                print(f"  [done] __NODE_NAME__")
                continue

            print(f"  [...] __NODE_NAME__...", end=" ", flush=True)

            try:
                content = generate_chapter(client, node_name, bucket)

                # Ensure the file starts with the correct H1 title
                if not content.startswith(f"# __NODE_NAME__"):
                    # Strip any leading ```markdown fence if Claude added one
                    content = re.sub(r"^```[a-z]*\n?", "", content)
                    content = re.sub(r"\n?```$", "", content).strip()

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                    f.write("\n")

                completed.add(key)
                with open(progress_file, "w") as pf:
                    json.dump(sorted(completed), pf, indent=2)

                print("✓")
                time.sleep(1.5)  # Polite pause between API calls

            except anthropic.RateLimitError:
                print("RATE LIMITED — waiting 60s…")
                time.sleep(60)
                # Retry once
                try:
                    content = generate_chapter(client, node_name, bucket)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    completed.add(key)
                    with open(progress_file, "w") as pf:
                        json.dump(sorted(completed), pf, indent=2)
                    print("  ✓ (after retry)")
                except Exception as exc2:
                    print(f"  ✗ FAILED after retry: {exc2}")
                    errors.append(f"{key}: {exc2}")

            except Exception as exc:
                print(f"  ✗ ERROR: {exc}")
                errors.append(f"{key}: {exc}")
                time.sleep(5.0)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'=' * 50}")
    print(f"Generation complete: {len(completed)}/{total} chapters")

    if errors:
        print(f"\n⚠  {len(errors)} errors — these chapters need to be regenerated:")
        for e in errors:
            print(f"   • {e}")

    print(f"\nNext steps:")
    print(f"  1. pip install jupyter-book sphinx-proof sphinx-exercise")
    print(f"  2. jupyter-book build textbook/")
    print(f"  3. Open textbook/_build/html/index.html to preview")
    print(f"  4. git push — GitHub Actions will publish to GitHub Pages")


if __name__ == "__main__":
    main()

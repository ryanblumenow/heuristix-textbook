#!/usr/bin/env python3
"""
Heuristix Textbook — Concept Art + Alisen Insight Generator (Pass 3 v2)

For each chapter:
  1. Generates a flat-vector header illustration (matplotlib) in per-bucket colours
  2. Generates Alisen's Key Insight text (2-3 sentences)
  3. Inserts the illustration PNG before the first ## heading
  4. Inserts Alisen's gold callout box (with her actual image) immediately after

Usage:
    python -X utf8 add_concept_art.py

Progress saved to .concept_art_progress.json — safe to interrupt and resume.
"""

import os, sys, re, json, time, subprocess, anthropic

FIGURES_DIR   = os.path.join(os.path.dirname(__file__), "_static", "figures")
CHAPTERS_DIR  = os.path.join(os.path.dirname(__file__), "chapters")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), ".concept_art_progress.json")

NODES = {
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

BUCKET_TITLES = {
    "connect":    "Connect",
    "explore":    "Explore",
    "understand": "Understand",
    "predict":    "Predict",
    "decide":     "Decide",
    "explain":    "Explain",
    "augment":    "Augment",
    "act":        "Act",
}

# Per-bucket accent colours
BUCKET_COLORS = {
    "connect":    "#3730A3",   # indigo
    "explore":    "#0D9488",   # teal
    "understand": "#1D4ED8",   # blue
    "predict":    "#7C3AED",   # violet
    "decide":     "#15803D",   # green
    "explain":    "#B45309",   # amber
    "augment":    "#9D174D",   # rose
    "act":        "#0E7490",   # cyan
}

# Light background tints per bucket (very subtle)
BUCKET_BGTINTS = {
    "connect":    "#EEEEFF",
    "explore":    "#EDFAF8",
    "understand": "#EFF6FF",
    "predict":    "#F3EEFF",
    "decide":     "#EDFBF0",
    "explain":    "#FDF6EE",
    "augment":    "#FEF0F6",
    "act":        "#EEFAFD",
}


CONCEPT_ART_PROMPT = """\
You are generating assets for a data science textbook chapter about: **__NODE_NAME__** (__BUCKET_TITLE__ section).

Return EXACTLY this structure — nothing else:

===ARTCODE===
[matplotlib code]
===INSIGHT===
[Alisen insight text]
===END===

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ART REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generate self-contained Python/matplotlib code producing a FLAT VECTOR STYLE infographic illustration.

STYLE (non-negotiable):
- fig, ax = plt.subplots(figsize=(14, 4.2))
- Light tinted background: fig.patch + ax.set_facecolor('__BUCKET_BGTINT__')
- Bold header strip across TOP 22% of figure: solid Rectangle((0,3.3),14,0.9) facecolor='__BUCKET_COLOR__'
- Node name "__NODE_NAME__" in large bold white text, top-left of header strip (x=0.4, y=3.75)
- Short subtitle in pale/white text below (x=0.4, y=3.45)
- Bucket pill top-right: pill-shaped text '__BUCKET_TITLE__' with facecolor='#F5C518', color='#0F172A', fontsize=8
- ax.set_xlim(0,14), ax.set_ylim(0,4.2), ax.axis('off')
- NO axis labels, NO ticks, NO grid

CONTENT AREA (below strip, y=0 to y=3.3):
- Use FancyBboxPatch (round corners) for cards and containers
- Use colorful flat status dots (Circle patches): green #22C55E, red #EF4444, amber #F59E0B
- Use colored pill labels (ax.text with bbox, boxstyle='round,pad=0.3')
- Show a clear DATA FLOW: input → transformation → output with annotate arrows
- Include 2-4 labelled elements showing what the node actually does
- Bold, readable labels. Mix font sizes 7-11pt for hierarchy.
- Use __BUCKET_COLOR__ as the primary accent throughout

VISUAL INSPIRATION: Modern SaaS docs illustrations (Linear, Notion, Stripe). Clean, colorful, informative.

LIBRARIES: matplotlib and numpy only. No plt.show(). No random data. No sklearn/pandas/seaborn.
END WITH: plt.savefig('__SLUG___concept.png', dpi=130, bbox_inches='tight', facecolor=fig.get_facecolor())

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSIGHT REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Write exactly 2-3 punchy sentences that a senior data scientist named Alisen would say about __NODE_NAME__.
Focus on one of: best practice tip, surprising use case, or most common mistake to avoid.
Plain text only — no markdown, no bullet points, no quotes.
"""


def slugify(name):
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    for path in [
        os.path.join(os.path.dirname(__file__), "..", ".streamlit", "secrets.toml"),
        os.path.expanduser("~/.streamlit/secrets.toml"),
    ]:
        try:
            if not os.path.exists(path):
                continue
            for line in open(path).read().splitlines():
                line = line.strip()
                if line.upper().startswith("ANTHROPIC_API_KEY"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
        except Exception:
            pass
    return None


def strip_fences(code):
    lines = code.splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("```")).strip()


def parse_response(raw):
    """Extract art code and insight text from the structured response."""
    art_code, insight = "", ""
    m_art = re.search(r"===ARTCODE===\s*(.*?)\s*===INSIGHT===", raw, re.DOTALL)
    m_ins = re.search(r"===INSIGHT===\s*(.*?)\s*===END===", raw, re.DOTALL)
    if m_art:
        art_code = strip_fences(m_art.group(1).strip())
    if m_ins:
        insight = m_ins.group(1).strip()
    return art_code, insight


def generate_assets(client, node_name, bucket, slug):
    prompt = (
        CONCEPT_ART_PROMPT
        .replace("__NODE_NAME__", node_name)
        .replace("__BUCKET_TITLE__", BUCKET_TITLES[bucket])
        .replace("__BUCKET_COLOR__", BUCKET_COLORS[bucket])
        .replace("__BUCKET_BGTINT__", BUCKET_BGTINTS[bucket])
        .replace("__SLUG__", slug)
    )
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    return parse_response(raw)


def execute_code(code, figures_dir, out_path):
    fig_path_fwd = out_path.replace("\\", "/")
    code = re.sub(
        r"plt\.savefig\(['\"].*?['\"]\]?",
        lambda m, p=fig_path_fwd: f"plt.savefig('{p}'",
        code,
    )
    full_code = "import matplotlib\nmatplotlib.use('Agg')\n" + code
    script = os.path.join(figures_dir, "_tmp_concept.py")
    try:
        with open(script, "w", encoding="utf-8") as f:
            f.write(full_code)
        result = subprocess.run(
            [sys.executable, script],
            cwd=figures_dir, capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            return False, (result.stderr or "")[-600:]
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "Timeout after 60s"
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(script):
            os.remove(script)


def alisen_callout_html(md_path, insight_text):
    """Build Alisen's callout HTML block with correct relative path to her image."""
    # chapters/{bucket}/{slug}.md  →  ../../_static/alisenillus.png
    depth = len(os.path.relpath(md_path, os.path.join(os.path.dirname(__file__), "chapters")).split(os.sep)) - 1
    img_rel = ("../" * (depth + 1)) + "_static/alisenillus.png"
    safe_insight = insight_text.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    return f"""
<div class="alisen-callout">
<img src="{img_rel}" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>{safe_insight}</p>
</div>
</div>
"""


def inject_into_chapter(md_path, img_path, insight_text):
    """Insert concept art PNG + Alisen callout before the first ## heading."""
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    rel_img = os.path.relpath(img_path, os.path.dirname(md_path)).replace("\\", "/")
    img_md = f"\n![]({rel_img})\n"
    callout = alisen_callout_html(md_path, insight_text)

    # Don't double-insert
    already_has_art     = rel_img in content
    already_has_callout = "alisen-callout" in content

    if already_has_art and already_has_callout:
        return

    block = ""
    if not already_has_art:
        block += img_md + "\n"
    if not already_has_callout:
        block += callout + "\n"

    m = re.search(r"^(## )", content, re.MULTILINE)
    if m:
        insert_at = m.start()
        content = content[:insert_at] + block + content[insert_at:]
    else:
        lines = content.splitlines()
        insert_line = 3
        for i, line in enumerate(lines):
            if i > 0 and line.strip() == "" and i > 2:
                insert_line = i + 1
                break
        lines.insert(insert_line, block.strip())
        content = "\n".join(lines)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)


def save_progress(completed):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(sorted(completed), f, indent=2)


def main():
    api_key = get_api_key()
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            completed = set(json.load(f))
        print(f"Resuming — {len(completed)} done.")
    else:
        completed = set()

    eligible = [
        (bucket, node)
        for bucket, nodes in NODES.items()
        for node in nodes
        if os.path.exists(os.path.join(CHAPTERS_DIR, bucket, f"{slugify(node)}.md"))
    ]
    total     = len(eligible)
    remaining = total - len(completed)

    print(f"\nHeuristix Textbook — Concept Art + Alisen Generator (Pass 3 v2)")
    print("-" * 55)
    print(f"Chapters:  {total}")
    print(f"Done:      {len(completed)}")
    print(f"To do:     {remaining}")
    print(f"Model:     claude-sonnet-4-5")
    print(f"Est. cost: ~${remaining * 0.04:.0f}-${remaining * 0.08:.0f} USD")
    print(f"Est. time: ~{remaining * 25 // 60}-{remaining * 40 // 60} minutes")
    print("-" * 55 + "\n")

    if remaining == 0:
        print("All done! Run: jb build textbook/")
        return

    errors = []
    for bucket, node_name in eligible:
        slug = slugify(node_name)
        key  = f"{bucket}/{slug}"
        if key in completed:
            continue

        md_path  = os.path.join(CHAPTERS_DIR, bucket, f"{slug}.md")
        out_path = os.path.join(FIGURES_DIR, f"{slug}_concept.png")
        print(f"  [...] {node_name} ({BUCKET_TITLES[bucket]})...", end=" ", flush=True)

        ok = False
        for attempt in range(2):
            try:
                art_code, insight = generate_assets(client, node_name, bucket, slug)
                if not art_code:
                    raise ValueError("No art code returned")
                if not insight:
                    insight = f"{node_name} is a core transformation in the {BUCKET_TITLES[bucket]} workflow."

                success, err = execute_code(art_code, FIGURES_DIR, out_path)
                if success and os.path.exists(out_path):
                    inject_into_chapter(md_path, out_path, insight)
                    print("[ok]")
                    ok = True
                    break
                else:
                    if attempt == 0:
                        print("retry...", end=" ", flush=True)
                        time.sleep(1)
                    else:
                        print(f"[failed] {err[:80]}")
                        errors.append(f"{node_name}: {err[:80]}")
            except Exception as exc:
                if attempt == 0:
                    print("retry...", end=" ", flush=True)
                    time.sleep(2)
                else:
                    print(f"[error] {exc}")
                    errors.append(f"{node_name}: {exc}")

        if ok:
            completed.add(key)
            save_progress(completed)
        time.sleep(0.5)

    print(f"\n{'=' * 55}")
    print(f"Complete: {len(completed)}/{total}")
    if errors:
        print(f"\n{len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
    print(f"\nNext: jb build textbook/ && ghp-import -n -p -f textbook/_build/html")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Fix Missing Figures — targeted pass for chapters that have fewer than 2 figures.
Run AFTER add_figures.py. Only generates the missing figure(s) per chapter.

Usage:
    python -X utf8 fix_missing_figures.py
"""

import os, sys, re, json, time, subprocess, anthropic

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "_static", "figures")
CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), "chapters")

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

FIGURE_PROMPT = """\
You are generating a matplotlib figure to illustrate a textbook chapter on \
**__NODE_NAME__** (in the __BUCKET_TITLE__ section of a data science textbook).

Generate exactly ONE self-contained Python code block producing ONE \
publication-quality matplotlib figure that illustrates a key concept.

Requirements:
- Uses ONLY: matplotlib, seaborn, numpy, pandas, scipy, scikit-learn (no other libraries)
- Generates its own synthetic data (no file I/O, no external datasets)
- Uses a dark professional theme:
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')
    # Use colors: #3b82f6 (blue), #22c55e (green), #f59e0b (amber), #ef4444 (red), #a78bfa (purple)
- Has a clear, descriptive title (ax.set_title(..., color='#e2e8f0', fontsize=13, fontweight='bold'))
- Has labelled axes in #94a3b8
- Has a legend if multiple series
- Tight layout: plt.tight_layout()
- Ends with: plt.savefig('__SLUG___fig__N__.png', dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
- Does NOT call plt.show()
- Choose a figure that genuinely illuminates the concept from a DIFFERENT angle than a basic overview

Return ONLY the raw Python code — NO markdown fences, NO ```python, NO explanation.
Start your response directly with: import
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


def strip_fences(code: str) -> str:
    """Remove any markdown code fences that Claude accidentally left in."""
    lines = code.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            continue  # drop fence lines entirely
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def generate_one_figure(client, node_name, bucket, slug, fig_n):
    """Ask Claude for one figure code block. Returns clean code string."""
    prompt = (
        FIGURE_PROMPT
        .replace("__NODE_NAME__", node_name)
        .replace("__BUCKET_TITLE__", BUCKET_TITLES[bucket])
        .replace("__SLUG__", slug)
        .replace("__N__", str(fig_n))
    )
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    # Aggressively strip any fences
    code = strip_fences(raw)
    # If it still has a ```python block, extract the interior
    m = re.search(r"```(?:python)?\n(.*?)```", code, re.DOTALL)
    if m:
        code = strip_fences(m.group(1).strip())
    return code


def execute_figure(code, figures_dir, fig_full_path):
    """Execute figure code, saving to fig_full_path. Returns (ok, error)."""
    # Redirect savefig to full path
    fig_path_fwd = fig_full_path.replace("\\", "/")
    code = re.sub(
        r"plt\.savefig\(['\"].*?['\"]",
        lambda m, p=fig_path_fwd: f"plt.savefig('{p}'",
        code,
    )
    full_code = "import matplotlib\nmatplotlib.use('Agg')\n" + code
    script = os.path.join(figures_dir, "_tmp_fix.py")
    try:
        with open(script, "w", encoding="utf-8") as f:
            f.write(full_code)
        result = subprocess.run(
            [sys.executable, script],
            cwd=figures_dir, capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            return False, (result.stderr or "")[-400:]
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "Timeout after 60s"
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(script):
            os.remove(script)


def inject_figure(md_path, fig_path):
    """Append a figure reference to the Visualisations section of the chapter."""
    with open(md_path, encoding="utf-8") as f:
        content = f.read()
    rel = os.path.relpath(fig_path, os.path.dirname(md_path)).replace("\\", "/")
    img_tag = f"![]({rel})\n"
    # Already inserted?
    if rel in content:
        return
    if "## Visualisations" in content:
        # Find end of Visualisations section and append there
        idx = content.index("## Visualisations")
        # find the next ## after the section (if any) to insert before it
        next_section = re.search(r"\n## ", content[idx + 5:])
        if next_section:
            insert_at = idx + 5 + next_section.start()
            content = content[:insert_at] + img_tag + "\n" + content[insert_at:]
        else:
            content = content.rstrip() + "\n" + img_tag
    else:
        content = content.rstrip() + "\n\n## Visualisations\n\n" + img_tag
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    api_key = get_api_key()
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Find which (bucket, node, slug, fig_n) combos are missing
    existing = set(os.listdir(FIGURES_DIR))
    missing = []
    for bucket, nodes in NODES.items():
        for node in nodes:
            slug = slugify(node)
            md = os.path.join(CHAPTERS_DIR, bucket, f"{slug}.md")
            if not os.path.exists(md):
                continue
            for n in (1, 2):
                fname = f"{slug}_fig{n}.png"
                if fname not in existing:
                    missing.append((bucket, node, slug, n, md))

    total = len(missing)
    print(f"Fix Missing Figures — targeted pass")
    print(f"-" * 45)
    print(f"Missing figures: {total}")
    print(f"Model: claude-sonnet-4-5")
    print(f"Est. cost: ~${total * 0.015:.2f}-${total * 0.03:.2f} USD")
    print(f"-" * 45 + "\n")

    errors = []
    for i, (bucket, node, slug, fig_n, md_path) in enumerate(missing, 1):
        fig_filename = f"{slug}_fig{fig_n}.png"
        fig_full_path = os.path.join(FIGURES_DIR, fig_filename)
        print(f"  [{i}/{total}] {node} fig{fig_n}... ", end="", flush=True)

        # Retry up to 2 times
        ok = False
        for attempt in range(2):
            try:
                code = generate_one_figure(client, node, bucket, slug, fig_n)
                ok, err = execute_figure(code, FIGURES_DIR, fig_full_path)
                if ok and os.path.exists(fig_full_path):
                    inject_figure(md_path, fig_full_path)
                    print(f"done")
                    ok = True
                    break
                else:
                    if attempt == 0:
                        print(f"retry... ", end="", flush=True)
                    else:
                        print(f"FAILED: {err[:80]}")
                        errors.append(f"{node} fig{fig_n}: {err[:80]}")
            except Exception as exc:
                if attempt == 0:
                    print(f"retry... ", end="", flush=True)
                    time.sleep(2)
                else:
                    print(f"FAILED: {exc}")
                    errors.append(f"{node} fig{fig_n}: {exc}")
        time.sleep(0.3)

    print(f"\n{'=' * 45}")
    print(f"Done. {total - len(errors)}/{total} figures generated.")
    if errors:
        print(f"\n{len(errors)} still failed:")
        for e in errors:
            print(f"  - {e}")
    print(f"\nNext: rebuild the Jupyter Book:")
    print(f'  jb build textbook/')


if __name__ == "__main__":
    main()

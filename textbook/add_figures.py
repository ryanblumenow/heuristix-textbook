#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         Heuristix Textbook — Figure Generator (Second Pass)                 ║
║                                                                              ║
║  For each generated chapter (.md file), calls Claude to write matplotlib    ║
║  figure code, executes it locally, saves PNGs to _static/figures/, and      ║
║  inserts figure references into the chapter markdown.                        ║
║                                                                              ║
║  Run AFTER generate_chapters.py has completed all 173 chapters.             ║
║                                                                              ║
║  Usage:                                                                      ║
║    pip install anthropic matplotlib seaborn scikit-learn numpy pandas        ║
║    python -X utf8 add_figures.py                                             ║
║                                                                              ║
║  Progress saved to .figures_progress.json — safe to interrupt and resume.   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import re
import textwrap
import traceback
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "_static", "figures")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), ".figures_progress.json")

# How many figures to generate per chapter
FIGURES_PER_CHAPTER = 2

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

# ── Utilities ─────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def chapter_md_path(bucket: str, node: str) -> str:
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
    return None


# ── Figure code generation prompt ────────────────────────────────────────────

FIGURE_PROMPT = """\
You are generating matplotlib figures to illustrate a textbook chapter on \
**__NODE_NAME__** (in the __BUCKET_TITLE__ section of a data science textbook).

Generate exactly __N__ self-contained Python code blocks, each producing ONE \
publication-quality matplotlib figure that illustrates a key concept from this topic.

Requirements for each figure:
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
- Ends with: plt.savefig('__SLUG___figN.png', dpi=120, bbox_inches='tight', \
facecolor=fig.get_facecolor())
  where N is 1, 2, etc.
- Does NOT call plt.show()

Choose figures that genuinely illuminate the concept — not generic plots. \
For example:
- For Linear Regression: regression line with confidence band + residual plot
- For Random Forest: feature importance bar chart + ROC curve
- For K-Means: cluster scatter plot before/after
- For ARIMA: time series with forecast and confidence interval
- For PCA: explained variance scree plot + 2D projection
- For Survival Analysis: Kaplan-Meier curves for multiple groups
- For Hypothesis Testing: null distribution with rejection region shaded
etc.

Return ONLY the Python code blocks (no markdown explanation, no prose).
Separate each figure's code with a line containing exactly: ### FIGURE N ###
"""


def generate_figure_code(client: anthropic.Anthropic, node_name: str, bucket: str, n: int, slug: str) -> list[str]:
    """Ask Claude for N figure code blocks for this node. Returns list of code strings."""
    from generate_chapters import BUCKET_TITLES  # reuse the bucket title map
    prompt = (
        FIGURE_PROMPT
        .replace("__NODE_NAME__", node_name)
        .replace("__BUCKET_TITLE__", BUCKET_TITLES[bucket])
        .replace("__N__", str(n))
        .replace("__SLUG__", slug)
    )
    response = client.messages.create(
        model="claude-sonnet-4-5",   # Sonnet is fast enough for code generation
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()

    # Split on ### FIGURE N ### separators
    parts = re.split(r"###\s*FIGURE\s*\d+\s*###", raw, flags=re.IGNORECASE)
    codes = []
    for part in parts:
        # Extract code from ```python ... ``` block
        m = re.search(r"```(?:python)?\n(.*?)```", part, re.DOTALL)
        if m:
            codes.append(m.group(1).strip())
        elif part.strip():
            # No fence — treat the whole part as code
            clean = part.strip()
            if "import" in clean or "plt." in clean:
                codes.append(clean)
    return codes[:n]


def execute_figure_code(code: str, figures_dir: str) -> tuple[bool, str]:
    """Execute figure code in figures_dir. Returns (success, error_message)."""
    import subprocess
    # Prepend matplotlib backend to avoid display issues
    full_code = "import matplotlib\nmatplotlib.use('Agg')\n" + code
    script_path = os.path.join(figures_dir, "_tmp_fig.py")
    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(full_code)
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=figures_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return False, result.stderr[-500:] if result.stderr else "Unknown error"
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "Timeout after 60s"
    except Exception as exc:
        return False, str(exc)
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)


def inject_figures_into_chapter(md_path: str, slug: str, figure_paths: list[str]) -> None:
    """Insert figure references into the chapter markdown after the Python Implementation section."""
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    # Build the figures block
    fig_lines = ["\n## Visualisations\n"]
    for i, fig_path in enumerate(figure_paths, 1):
        # Make path relative from chapter file location
        rel_path = os.path.relpath(fig_path, os.path.dirname(md_path)).replace("\\", "/")
        fig_lines.append(f"![]({rel_path})\n")

    figures_block = "\n".join(fig_lines)

    # Insert after the Python Implementation section (before ## Using This in Heuristix or ## Business)
    inserted = False
    for marker in ["## Using This in Heuristix", "## Business Applications", "## Worked Example"]:
        if marker in content:
            content = content.replace(marker, figures_block + "\n" + marker, 1)
            inserted = True
            break

    if not inserted:
        # Append at end
        content += "\n" + figures_block

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    api_key = get_api_key()
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # Load progress
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            completed: set[str] = set(json.load(f))
        print(f"Resuming — {len(completed)} chapters already have figures.")
    else:
        completed = set()

    # Count eligible chapters (generated .md files exist, not index pages)
    eligible = [
        (bucket, node)
        for bucket, nodes in NODES.items()
        for node in nodes
        if os.path.exists(chapter_md_path(bucket, node))
    ]
    total = len(eligible)
    remaining = total - len(completed)

    print(f"\nHeuristix Textbook — Figure Generator (Pass 2)")
    print("-" * 50)
    print(f"Eligible chapters:  {total}")
    print(f"Already done:       {len(completed)}")
    print(f"To process:         {remaining}")
    print(f"Figures per chapter:{FIGURES_PER_CHAPTER}")
    print(f"Model:              claude-sonnet-4-5")
    print(f"Est. cost:          ~${remaining * 0.03:.0f}-${remaining * 0.06:.0f} USD")
    print(f"Est. time:          ~{remaining * 25 // 60}-{remaining * 40 // 60} minutes")
    print("-" * 50 + "\n")

    if remaining == 0:
        print("All chapters already have figures! Run: jupyter-book build textbook/")
        return

    errors: list[str] = []

    for bucket, node_name in eligible:
        slug = slugify(node_name)
        key = f"{bucket}/{slug}"

        if key in completed:
            print(f"  [done] {node_name}")
            continue

        md_path = chapter_md_path(bucket, node_name)
        print(f"  [...] {node_name}...", end=" ", flush=True)

        try:
            # 1. Generate figure code from Claude
            codes = generate_figure_code(client, node_name, bucket, FIGURES_PER_CHAPTER, slug)
            if not codes:
                print(f"  [skip] no code returned")
                completed.add(key)
                _save_progress(completed)
                continue

            # 2. Execute each code block and collect saved PNGs
            saved_figs: list[str] = []
            for i, code in enumerate(codes, 1):
                # Fix the savefig filename to use full path
                fig_filename = f"{slug}_fig{i}.png"
                fig_full_path = os.path.join(FIGURES_DIR, fig_filename)
                # Replace relative savefig call with full path
                # Use forward slashes to avoid \U etc. being treated as re group refs
                fig_path_fwd = fig_full_path.replace("\\", "/")
                code = re.sub(
                    r"plt\.savefig\(['\"].*?['\"]",
                    lambda m, p=fig_path_fwd: f"plt.savefig('{p}'",
                    code,
                )
                ok, err = execute_figure_code(code, FIGURES_DIR)
                if ok and os.path.exists(fig_full_path):
                    saved_figs.append(fig_full_path)
                else:
                    print(f"\n    Fig {i} failed: {err[:120]}", end="")

            # 3. Inject figure references into the markdown
            if saved_figs:
                inject_figures_into_chapter(md_path, slug, saved_figs)

            completed.add(key)
            _save_progress(completed)
            print(f"  [ok] ({len(saved_figs)} figs)")
            time.sleep(0.5)

        except Exception as exc:
            print(f"  [error] {exc}")
            errors.append(f"{key}: {exc}")
            time.sleep(3.0)

    print(f"\n{'=' * 50}")
    print(f"Figures complete: {len(completed)}/{total} chapters")
    if errors:
        print(f"\n{len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
    print(f"\nNext: jupyter-book build textbook/")


def _save_progress(completed: set[str]) -> None:
    with open(PROGRESS_FILE, "w") as f:
        json.dump(sorted(completed), f, indent=2)


if __name__ == "__main__":
    main()

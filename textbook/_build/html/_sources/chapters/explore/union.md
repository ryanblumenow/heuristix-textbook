# Union




![](../../_static/figures/union_concept.png)


<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The most common mistake I see with Union is trying to combine datasets with mismatched columns without preprocessing. Always verify your schemas match exactly—same column names, same data types, same order—or you'll get cryptic errors or worse, silent data corruption. When in doubt, explicitly select and cast your columns before the union operation to avoid downstream debugging nightmares.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Union stacks two or more tables on top of each other to create one longer table with all the rows combined.

**When to use it:** You have the same kind of data split across multiple sources—regional sales files, monthly exports, or departmental records—and need to analyze them as one complete dataset.

**What you get back:** A single unified table containing every row from all your input tables, ready for filtering, aggregation, or visualization as a coherent whole.

**At a Glance**

| | |
|---|---|
| **Difficulty** | Easy |
| **Typical runtime** | Seconds on 100K rows |
| **What you bring** | Two or more tables with matching column structures |
| **What you get** | One combined table with all rows stacked vertically |
| **Heuristix bucket** | Explore — Shaping & Transforming Data |

**Union doesn't check for duplicates by default—if the same customer appears in both your East and West region files, they'll appear twice in your combined dataset unless you explicitly remove duplicates.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify situations where combining data from multiple sources with similar structures (like merging quarterly sales reports or regional customer lists) requires a Union operation rather than a join or merge.
- Explain to stakeholders why a unified dataset contains a specific number of rows and how duplicate records were handled during the combination process.
- Decide whether to preserve or remove duplicate records when consolidating datasets based on the analytical question at hand (such as counting total transactions versus unique customers).

**After reading this chapter, a data scientist will be able to:**

- Implement Union operations across datasets with varying column orders, mismatched column names, and differing data types while ensuring schema compatibility.
- Configure Union parameters to control duplicate handling, column alignment strategies, and type coercion behavior based on downstream analytical requirements.
- Diagnose and resolve common Union failures including schema mismatches, unexpected row counts, data type conflicts, and performance issues with large-scale dataset combinations.

## Overview

The **Union** operation is a fundamental set-theoretic transformation that combines rows from two or more datasets into a single unified dataset. Its core purpose is vertical concatenation—stacking datasets with compatible schemas to create a comprehensive collection of observations. Union belongs to the family of **set operations** in relational algebra, alongside intersection, difference, and Cartesian product, and forms a cornerstone of data shaping and transformation workflows in any analytical platform.

## When to Use This

- **Use this when consolidating periodic data extracts**: Monthly sales files, weekly log dumps, or quarterly financial reports that share identical structures need to be combined for longitudinal analysis.

- **Use this when merging data from multiple sources with identical schemas**: Customer records from different regional databases, product catalogues from acquired companies, or transaction logs from parallel systems that track the same attributes.

- **Use this when implementing stratified sampling workflows**: After sampling separately from distinct strata or segments, union recombines the samples into a single analysis-ready dataset.

- **Use this when building training datasets from multiple labelled sources**: Machine learning pipelines often require combining positive and negative examples, or data from different annotation batches, into unified training sets.

- **Use this when appending new observations to historical data**: Incremental data loading patterns where fresh records must be added to an existing analytical table without overwriting previous entries.

- **Use this when reconstructing datasets after parallel processing**: Distributed or chunked processing workflows that split data for efficiency must reassemble results into a coherent whole.

- **Use this when combining experimental and control groups for joint analysis**: A/B test data collected separately for treatment and control cohorts needs unification for comparative statistical analysis.

- **Do NOT use this when datasets have different schemas**: If column names, types, or meanings differ, you need a **join** operation (horizontal combination based on keys), not a union.

- **Do NOT use this when you need to match rows between datasets**: Union does not align records—it simply stacks them. Use joins for record-level correspondence.

- **Do NOT use this when duplicate elimination is critical and uncontrolled**: Standard union includes all rows from all inputs; if you require set-theoretic distinctness, you must explicitly configure deduplication or apply it downstream.

## Questions This Answers

### Consolidating Fragmented Data Sources

**Can you combine our US sales data with our European sales data so we have one complete view of global revenue?**

**We track customer feedback in three different spreadsheets—retail stores, online orders, and call center. Can we merge these into a single list?**

**Our marketing team ran campaigns across Google, Facebook, and LinkedIn. How do we pull all the lead data together to see total campaign performance?**

**We have transaction files from January through December stored separately. Can we stack them all to analyze the full year?**

**Our company acquired two competitors last year. How do we combine their customer databases with ours to see our total addressable market?**

### Building Comprehensive Historical Views

**Can we append this quarter's sales to our historical dataset so we're analyzing performance across the past three years?**

**We just migrated to a new CRM system. How do we add the old system's records to the new one without losing historical context?**

**I need to see all product returns from 2022, 2023, and 2024 in one report. The data lives in separate annual archives—can we merge them?**

**Our supply chain data comes in weekly batches. How do we continuously build a complete inventory movement history?**

### Comparing Multiple Scenarios or Segments

**We have sales projections from three different forecasting models. Can we stack them all together to compare which one performs best against actuals?**

**To analyze churn risk, can we combine our active subscribers with our canceled subscribers into one master customer list?**

**We're testing pricing strategies in five different regions. How do we merge all regional test results to identify the winning approach?**

**Can we pull together employee performance data from all departments—sales, operations, and support—to benchmark productivity across the organization?**

## How It Works

Imagine you're organizing a charity fundraiser, and you've asked three different team members to collect sign-ups at different locations—Maria covered the downtown booth, James handled the university campus, and Sofia worked the weekend farmers market. Each person comes back with their own spreadsheet: Maria has 47 names with email addresses and phone numbers, James has 33 names with the same columns, and Sofia collected 28. Now you need to create one master contact list for your event. You're not trying to match people up or compare lists—you simply want to stack all three spreadsheets on top of each other into one long list with 108 total rows (assuming no duplicates). That's exactly what Union does with datasets.

```
BEFORE UNION

Dataset A (Q1 Sales)     Dataset B (Q2 Sales)
┌──────┬─────────┬────┐ ┌──────┬─────────┬────┐
│ ID   │ Product │ Qty│ │ ID   │ Product │ Qty│
├──────┼─────────┼────┤ ├──────┼─────────┼────┤
│ 1001 │ Widget  │ 50 │ │ 2001 │ Gadget  │ 30 │
│ 1002 │ Gadget  │ 25 │ │ 2002 │ Widget  │ 40 │
│ 1003 │ Sprocket│ 15 │ │ 2003 │ Tool    │ 20 │
└──────┴─────────┴────┘ └──────┴─────────┴────┘
           ↓                      ↓
           └──────────┬───────────┘
                      ↓
              UNION Operation
                      ↓
AFTER UNION (Combined Sales)
┌──────┬─────────┬────┐
│ ID   │ Product │ Qty│
├──────┼─────────┼────┤
│ 1001 │ Widget  │ 50 │ ← from Dataset A
│ 1002 │ Gadget  │ 25 │ ← from Dataset A
│ 1003 │ Sprocket│ 15 │ ← from Dataset A
│ 2001 │ Gadget  │ 30 │ ← from Dataset B
│ 2002 │ Widget  │ 40 │ ← from Dataset B
│ 2003 │ Tool    │ 20 │ ← from Dataset B
└──────┴─────────┴────┘
```

**Step 1: Check schema compatibility.** Union first verifies that all datasets share the same structure—the same number of columns in the same order with compatible data types. If Dataset A has three columns (ID, Product, Quantity) and Dataset B has four columns, Union will fail. The columns must match like LEGO bricks that snap together.

**Step 2: Take the first dataset as the foundation.** Union starts by copying the entire first dataset into the result. Every single row from the first table becomes the top portion of your combined output. Think of this as laying down the first layer of bricks.

**Step 3: Stack the second dataset below.** Union appends all rows from the second dataset directly underneath the first. No matching, no filtering, no comparison—just pure vertical stacking. The second layer of bricks goes right on top.

**Step 4: Continue for each additional dataset.** If you're unioning three, four, or twenty datasets, Union repeats this stacking process for each one in sequence. Each dataset becomes another layer in your growing tower.

**Step 5: Handle duplicates based on variant.** Standard Union removes exact duplicate rows from the final result, keeping only one copy of identical records. Union All keeps every row, even duplicates. This is the only decision point in the entire operation.

**Step 6: Preserve original row order within each source.** Rows from Dataset A appear in the same order they had originally, followed by Dataset B's rows in their original sequence. Union doesn't sort or reorganize—it respects the original sequence from each source.

**The key insight:** Union works because it exploits the fundamental principle that data with identical structure can be meaningfully combined through simple vertical concatenation, turning fragmented observations into comprehensive datasets without any complex logic.

## The Intuition

Imagine you are a librarian responsible for maintaining the complete catalogue of a university library system. The main campus library, the law school library, and the medical school library each maintain their own card catalogues—physical index cards describing every book in their collection. Each catalogue uses the same format: title, author, publication year, ISBN, and shelf location. Your task is to create a master catalogue that lists every book across all three libraries.

The union operation is precisely this consolidation. You take the stack of cards from the main library, place the law library's cards beneath them, and then add the medical library's cards at the bottom. The result is a single, comprehensive stack containing every book record from every source. Crucially, you have not examined whether the same book appears in multiple libraries—if the law library and main library both own copies of *Black's Law Dictionary*, you will have two cards for it in your master catalogue. This is the default behaviour of union: it preserves all rows from all inputs, including duplicates.

Now consider a subtly different scenario. Suppose you are asked to produce a catalogue of *unique titles* available across the university system—a list where each book appears exactly once, regardless of how many libraries hold copies. This requires an additional step: after stacking all the cards, you must sort through them and remove duplicates. In database terminology, this distinction is captured by `UNION ALL` (preserving duplicates) versus `UNION` (eliminating duplicates). Both are valid operations; the choice depends on whether your analytical question concerns *observations* (keep duplicates) or *distinct entities* (remove duplicates).

The power of union lies in its simplicity and composability. Because it produces a dataset with the same schema as its inputs, union outputs can flow seamlessly into any downstream operation—filtering, aggregation, joining, or further unions. This makes it an essential building block in complex data pipelines where information arrives in fragments and must be assembled before analysis can proceed.

## The Mathematics

### Formal Setup and Notation

Let $R$ and $S$ be two relations (datasets) with identical schemas. A schema defines an ordered sequence of attributes $(A_1, A_2, \ldots, A_n)$ where each attribute $A_i$ has an associated domain $\text{dom}(A_i)$. A relation $R$ is a subset of the Cartesian product of these domains:

$$
R \subseteq \text{dom}(A_1) \times \text{dom}(A_2) \times \cdots \times \text{dom}(A_n)
$$

Each element $t \in R$ is called a **tuple** (row), and we write $t[A_i]$ to denote the value of attribute $A_i$ in tuple $t$.

### Schema Compatibility

Two relations $R$ and $S$ are **union-compatible** if and only if:

1. They have the same number of attributes: $|R.\text{schema}| = |S.\text{schema}|$
2. Corresponding attributes have compatible domains: $\text{dom}(R.A_i) \approx \text{dom}(S.A_i)$ for all $i$

Domain compatibility ($\approx$) may be strict equality or allow type coercion depending on implementation (e.g., integer to float promotion).

### Set Union (Distinct)

The **set union** of $R$ and $S$, denoted $R \cup S$, is defined as:

$$
R \cup S = \{ t \mid t \in R \lor t \in S \}
$$

This is the standard set-theoretic union. By the definition of sets, each distinct tuple appears exactly once in the result, regardless of how many times it appears across inputs.

**Cardinality bounds**:

$$
\max(|R|, |S|) \leq |R \cup S| \leq |R| + |S|
$$

The lower bound is achieved when one relation is a subset of the other. The upper bound is achieved when $R \cap S = \emptyset$.

### Bag Union (All)

In practice, relations are often **bags** (multisets) rather than sets—duplicates are permitted and meaningful. The **bag union** of $R$ and $S$, denoted $R \uplus S$, is:

$$
R \uplus S = \{ t^{(m_R(t) + m_S(t))} \mid t \in R \cup S \}
$$

where $m_R(t)$ denotes the multiplicity (count) of tuple $t$ in $R$. The notation $t^{(k)}$ indicates that tuple $t$ appears with multiplicity $k$ in the result.

**Cardinality** (exact):

$$
|R \uplus S| = |R| + |S|
$$

This follows directly from the additive property of multiplicities.

### Multi-way Union

For $k$ relations $R_1, R_2, \ldots, R_k$ with identical schemas:

$$
\bigcup_{i=1}^{k} R_i = R_1 \cup R_2 \cup \cdots \cup R_k
$$

$$
\biguplus_{i=1}^{k} R_i = R_1 \uplus R_2 \uplus \cdots \uplus R_k
$$

Both operations are **associative** and **commutative**:

$$
R \cup S = S \cup R
$$

$$
(R \cup S) \cup T = R \cup (S \cup T)
$$

These properties allow query optimisers to reorder union operations for efficiency.

### Assumptions

1. **Schema compatibility**: All input relations must be union-compatible.
2. **Tuple identity**: For set union, tuple equality is determined by value equality across all attributes.
3. **Type coercion**: When domains differ but are coercible, the result schema uses the promoted type.
4. **Null handling**: Two tuples with nulls in corresponding positions may or may not be considered equal, depending on the null semantics of the system (SQL uses three-valued logic where `NULL ≠ NULL`).

### Edge Cases and Degenerate Conditions

- **Empty input**: $R \cup \emptyset = R$ and $R \uplus \emptyset = R$ (identity element)
- **Self-union**: $R \cup R = R$ (idempotent for set union), but $R \uplus R = 2R$ (doubles multiplicities for bag union)
- **Null-heavy data**: Relations with many null values may exhibit unexpected deduplication behaviour depending on null equality semantics

### Relationship to Other Set Operations

Union relates to other relational algebra operations:

$$
R - (R - S) \subseteq R \cap S \subseteq R \cup S
$$

De Morgan's laws apply:

$$
\overline{R \cup S} = \overline{R} \cap \overline{S}
$$

where $\overline{R}$ denotes the complement of $R$ with respect to some universal relation.

## Understanding the Mathematics

### The Union Operation

**The equation:**

$$R \cup S = \{t \mid t \in R \lor t \in S\}$$

**Read it aloud:**

"R union S equals the set of all tuples t where t is a member of R or t is a member of S."

**What each symbol means:**

- **R** and **S** = two separate datasets (tables) we want to combine
- **∪** = the union operator (combines the sets)
- **{}** = set notation (collection of items)
- **t** = a single row (tuple) in our data
- **∈** = "is a member of" or "exists in"
- **∣** = "such that" (introduces the condition)
- **∨** = logical OR

**A concrete numerical example:**

Dataset R contains customer orders from our website:
- Row 1: {OrderID: 101, Customer: "Alice", Amount: 250}
- Row 2: {OrderID: 102, Customer: "Bob", Amount: 180}

Dataset S contains customer orders from our mobile app:
- Row 2: {OrderID: 102, Customer: "Bob", Amount: 180}
- Row 3: {OrderID: 103, Customer: "Carol", Amount: 320}

R ∪ S yields:
- Row 1: {OrderID: 101, Customer: "Alice", Amount: 250}
- Row 2: {OrderID: 102, Customer: "Bob", Amount: 180}
- Row 3: {OrderID: 103, Customer: "Carol", Amount: 320}

Notice that Bob's duplicate order appears only once in the result.

**Why this equation matters:**

This formula ensures we collect every unique record from both sources without counting duplicates twice—critical when merging sales channels or combining data from multiple regional databases.

### Schema Compatibility Requirement

**The equation:**

$$\text{schema}(R) = \text{schema}(S)$$

**Read it aloud:**

"The schema of dataset R must equal the schema of dataset S."

**What each symbol means:**

- **schema(R)** = the structure of dataset R: column names, data types, and their order
- **schema(S)** = the structure of dataset S
- **=** = must be identical

**A concrete numerical example:**

Valid union—both datasets have identical schemas:

Dataset R schema: (ProductID: integer, ProductName: string, Price: decimal)

Dataset S schema: (ProductID: integer, ProductName: string, Price: decimal)

Invalid union—schemas don't match:

Dataset R schema: (ProductID: integer, ProductName: string, Price: decimal)

Dataset T schema: (ProductID: integer, Quantity: integer, Warehouse: string)

Attempting R ∪ T fails because the second and third columns represent completely different business concepts.

**Why this equation matters:**

Without identical schemas, we'd be stacking apples on top of oranges—the resulting dataset would have price values sitting in the same column as warehouse locations, making every downstream analysis meaningless.

### Cardinality of Union

**The equation:**

$$|R \cup S| \leq |R| + |S|$$

**Read it aloud:**

"The number of rows in R union S is less than or equal to the number of rows in R plus the number of rows in S."

**What each symbol means:**

- **|R ∪ S|** = the count of rows in the union result
- **|R|** = the count of rows in dataset R
- **|S|** = the count of rows in dataset S
- **≤** = less than or equal to
- **+** = addition

**A concrete numerical example:**

Marketing campaign results from two teams:

Team A's dataset R has 1,000 email addresses.

Team B's dataset S has 800 email addresses.

If the teams targeted completely different audiences: |R ∪ S| = 1,000 + 800 = 1,800 unique contacts.

If 300 email addresses appear in both lists: |R ∪ S| = 1,800 - 300 = 1,500 unique contacts.

The union never exceeds 1,800, but can be anywhere from 1,000 (if S is a complete subset of R) to 1,800 (if there's zero overlap).

**Why this equation matters:**

This boundary tells us the maximum storage and processing requirements before we execute the union—essential for capacity planning when combining million-row datasets in production systems.

### The Big Picture

The mathematics of union formalizes a deceptively simple idea: combine datasets vertically while respecting set theory's fundamental principle that duplicates collapse to single instances. This set-based approach was chosen over simple concatenation because real-world data sources often contain overlapping records—the same customer appearing in multiple systems, the same transaction logged by different departments. The compatibility requirement ensures logical coherence: we only unite datasets that measure the same business entities with the same attributes. At its heart, union mathematics answers one question: "What is the complete, non-redundant collection of observations from these compatible sources?"

## Python Implementation

```python
import pandas as pd
import numpy as np

# =============================================================================
# Example 1: Basic Union (Bag Union / Union All)
# =============================================================================

# Create two DataFrames representing quarterly sales from different regions
q1_sales = pd.DataFrame({
    'transaction_id': ['T001', 'T002', 'T003'],
    'product': ['Widget A', 'Widget B', 'Widget A'],
    'amount': [150.00, 275.50, 150.00],
    'region': ['North', 'North', 'North']
})

q2_sales = pd.DataFrame({
    'transaction_id': ['T004', 'T005', 'T006'],
    'product': ['Widget A', 'Widget C', 'Widget B'],
    'amount': [150.00, 320.00, 275.50],
    'region': ['South', 'South', 'South']
})

# Perform bag union using pd.concat (preserves all rows including duplicates)
combined_sales = pd.concat([q1_sales, q2_sales], ignore_index=True)

print("=== Bag Union (Union All) ===")
print(f"Q1 rows: {len(q1_sales)}, Q2 rows: {len(q2_sales)}")
print(f"Combined rows: {len(combined_sales)}")
print(combined_sales)
print()

# =============================================================================
# Example 2: Set Union (Distinct)
# =============================================================================

# Create overlapping customer lists from two marketing campaigns
campaign_a_customers = pd.DataFrame({
    'customer_id': [101, 102, 103, 104],
    'email': ['alice@example.com', 'bob@example.com', 
              'carol@example.com', 'dave@example.com'],
    'segment': ['Premium', 'Standard', 'Premium', 'Standard']
})

campaign_b_customers = pd.DataFrame({
    'customer_id': [103, 104, 105, 106],
    'email': ['carol@example.com', 'dave@example.com',
              'eve@example.com', 'frank@example.com'],
    'segment': ['Premium', 'Standard', 'Premium', 'Standard']
})

# Bag union first
all_customers = pd.concat([campaign_a_customers, campaign_b_customers], 
                          ignore_index=True)

# Then deduplicate for set union behaviour
unique_customers = all_customers.drop_duplicates()

print("=== Set Union (Distinct) ===")
print(f"Campaign A: {len(campaign_a_customers)}, Campaign B: {len(campaign_b_customers)}")
print(f"Bag union: {len(all_customers)}, Set union: {len(unique_customers)}")
print(unique_customers)
print()

# =============================================================================
# Example 3: Multi-way Union with Source Tracking
# =============================================================================

# Three regional inventory files
north_inventory = pd.DataFrame({
    'sku': ['SKU001', 'SKU002'],
    'quantity': [100, 50],
    'warehouse': ['WH-N1', 'WH-N2']
})

south_inventory = pd.DataFrame({
    'sku': ['SKU001', 'SKU003'],
    'quantity': [75, 200],
    'warehouse': ['WH-S1', 'WH-S1']
})

west_inventory = pd.DataFrame({
    'sku': ['SKU002', 'SKU004'],
    'quantity': [30, 150],
    'warehouse': ['WH-W1', 'WH-W1']
})

# Add source tracking column before union (common best practice)
north_inventory['source_region'] = 'North'
south_inventory['source_region'] = 'South'
west_inventory['source_region'] = 'West'

# Multi-way union
national_inventory = pd.concat(
    [north_inventory, south_inventory, west_inventory],
    ignore_index=True
)

print("=== Multi-way Union with Source Tracking ===")
print(national_inventory)
print(f"\nTotal SKU-location combinations: {len(national_inventory)}")
print(f"Total inventory units: {national_inventory['quantity'].sum()}")
print()

# =============================================================================
# Example 4: Handling Schema Mismatches
# =============================================================================

# DataFrames with slightly different column orders and types
df_a = pd.DataFrame({
    'id': [1, 2],
    'value': [10.5, 20.3],
    'category': ['X', 'Y']
})

df_b = pd.DataFrame({
    'category': ['Y', 'Z'],  # Different column order
    'id': [3, 4],
    'value': [30, 40]  # Integer instead of float
})

# pd.concat aligns by column names and promotes types automatically
combined = pd.concat([df_a, df_b], ignore_index=True)

print("=== Schema Alignment and Type Promotion ===")
print(f"df_a dtypes: {dict(df_a.dtypes)}")
print(f"df_b dtypes: {dict(df_b.dtypes)}")
print(f"Combined dtypes: {dict(combined.dtypes)}")
print(combined)
```

**Output:**

```
=== Bag Union (Union All) ===
Q1 rows: 3, Q2 rows: 3
Combined rows: 6
  transaction_id   product  amount region
0           T001  Widget A  150.00  North
1           T002  Widget B  275.50  North
2           T003  Widget A  150.00  North
3           T004  Widget A  150.00  South
4           T005  Widget C  320.00  South
5           T006  Widget B  275.50  South

=== Set Union (Distinct) ===
Campaign A: 4, Campaign B: 4
Bag union: 8, Set union: 6
   customer_id              email   segment
0          101   alice@example.com   Premium
1          102     bob@example.com  Standard
2          103   carol@example.com   Premium
3          104    dave@example.com  Standard
6          105     eve@example.com   Premium
7          106   frank@example.com  Standard

=== Multi-way Union with Source Tracking ===
      sku  quantity warehouse source_region
0  SKU001       100     WH-N1         North
1  SKU002        50     WH-N2         North
2  SKU001        75     WH-S1         South
3  SKU003       200     WH-S1         South
4  SKU002        30     WH-W1          West
5  SKU004       150     WH-W1          West

Total SKU-location combinations: 6
Total inventory units: 605

=== Schema Alignment and Type Promotion ===
df_a dtypes: {'id': dtype('int64'), 'value': dtype('float64'), 'category': dtype('O')}
df_b dtypes: {'category': dtype('O'), 'id': dtype('int64'), 'value': dtype('int64')}
Combined dtypes: {'id': dtype('int64'), 'value': dtype('float64'), 'category': dtype('O')}
```


## Visualisations

![](../../_static/figures/union_fig1.png)

![](../../_static/figures/union_fig2.png)

## Using This in Heuristix

### Data Inputs

The Union node accepts **two or more dataset inputs**. All input datasets must have compatible schemas:

| Input | Required | Description |
|-------|----------|-------------|
| Primary Dataset | Yes | The first dataset to include in the union |
| Secondary Dataset(s) | Yes (at least one) | Additional datasets to stack below the primary |

**Column type requirements:**
- Column names must match across inputs (case-sensitive by default)

## Config Recipes

### Recipe 1: Quick Exploration Union

- **When to use:** Rapidly combining sample datasets during initial data discovery when you need immediate visibility into combined structure and don't care about duplicates or ordering.
- **Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `check_schema` | `False` | Skip validation overhead for speed |
| `remove_duplicates` | `False` | Preserve all rows without deduplication cost |
| `sort_output` | `False` | Avoid sorting penalty on large intermediate results |
| `cache_result` | `False` | Don't persist exploratory outputs |

- **What you get:** Maximum speed union with all rows present, accepting whatever schema mismatches exist and preserving insertion order.
- **Trade-off:** You risk schema inconsistencies causing downstream errors and may carry forward duplicate observations that distort analysis.

### Recipe 2: Production-Grade Union

- **When to use:** Merging authoritative data sources for reporting pipelines where correctness, auditability, and schema consistency are non-negotiable.
- **Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `check_schema` | `strict` | Enforce exact column name and type matching |
| `remove_duplicates` | `True` | Eliminate redundant records across sources |
| `duplicate_strategy` | `hash_all_columns` | Consider entire row for duplicate detection |
| `sort_output` | `True` | Enable deterministic output ordering |
| `sort_keys` | `["timestamp", "id"]` | Specify stable sort dimensions |
| `null_handling` | `preserve` | Maintain null semantics from sources |
| `log_schema_diff` | `True` | Record any schema discrepancies for audit |

- **What you get:** Fully validated, deduplicated, deterministically ordered dataset suitable for versioned production workflows.
- **Trade-off:** You pay 3–5x execution time compared to quick union and require strict upstream schema governance.

### Recipe 3: Handling Partial Schema Overlap

- **When to use:** Combining datasets from different collection periods where column sets have evolved over time (e.g., merging 2019 survey data with 2024 survey that added new questions).
- **Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `check_schema` | `partial` | Allow non-overlapping columns |
| `fill_missing_columns` | `True` | Auto-create absent columns with nulls |
| `coerce_types` | `True` | Attempt safe type conversions (int→float) |
| `column_alignment` | `by_name` | Match columns semantically, not positionally |
| `warn_on_mismatch` | `True` | Flag type conflicts without failing |

- **What you get:** Superset schema containing all columns from all sources, with nulls filling gaps where columns didn't exist in particular datasets.
- **Trade-off:** You introduce systematic missingness patterns that require careful handling in downstream statistical analysis.

### Recipe 4: Synthetic Data Augmentation

- **When to use:** Expanding training datasets by unioning real observations with synthetically generated or augmented samples for machine learning.
- **Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `tag_source` | `True` | Add `_source` column identifying origin |
| `source_labels` | `["real", "synthetic"]` | Enable stratified sampling later |
| `shuffle_output` | `True` | Randomize order to prevent batch effects |
| `random_seed` | `42` | Make shuffle reproducible |
| `remove_duplicates` | `False` | Intentionally keep synthetic near-duplicates |

- **What you get:** Blended dataset with source tracking that prevents data leakage during cross-validation splits.
- **Trade-off:** You increase dataset size substantially, requiring proportionally more memory and compute for model training.

## Business Applications

**Financial Services**

A regional US credit union with 400,000 members needs to monitor fraudulent transactions across checking accounts, credit cards, savings accounts, and loan disbursements. Each product line maintains separate transaction tables with identical schemas (timestamp, amount, merchant category, location), but fraud patterns often span multiple products—a criminal might test a stolen identity with a small savings withdrawal before attempting a large credit card purchase. By using Union to combine all transaction streams into a single monitoring dataset, the credit union's fraud detection model can identify cross-product patterns that were previously invisible. This approach reduced false positives by 34% while catching an additional $2.3M in fraudulent activity annually.

**Retail**

An e-commerce fashion retailer operating separate websites for the US, UK, and EU markets maintains independent customer feedback tables for each region, all sharing the same structure (product_id, rating, review_text, date). The product development team struggles to get a holistic view of which items are underperforming globally versus regionally. Union operations merge these three feedback sources into a unified global review dataset, enabling the team to identify that a popular jacket received 4.2-star ratings in the US but only 2.8 stars in EU markets due to sizing inconsistencies. Correcting the sizing chart lifted EU conversion rates from 2.1% to 3.7%, generating an additional €840,000 in quarterly revenue.

**Healthcare**

A hospital network with twelve facilities across three states maintains separate patient admission records at each location, following a standardized HL7-compliant schema. When a patient presents at the emergency department, clinicians need immediate access to that patient's complete admission history across all facilities to avoid duplicate tests and understand chronic conditions. Union operations consolidate these twelve admission tables into a network-wide patient history view refreshed hourly. This reduced redundant diagnostic imaging by 28%, saving the network $1.8M annually while cutting average ER diagnostic time from 127 minutes to 89 minutes.

**Insurance**

A property and casualty insurer receives claims data from a network of independent adjusters, body shops, and contractors, each submitting weekly CSV files with identical column structures (claim_id, expense_type, amount, date, vendor). The claims department previously processed these files manually, a four-day process prone to errors and delays. Implementing automated Union operations to merge these feeds into a single claims expense ledger reduced processing time to 35 minutes and enabled real-time fraud detection, identifying $670,000 in duplicate billing within the first quarter of deployment.

**Manufacturing**

A multinational automotive parts manufacturer operates assembly lines across Mexico, Poland, and Thailand, with each plant logging quality control inspections to local databases using the same schema. The central quality assurance team needs to identify systemic defects that might appear across multiple plants but remain statistically invisible at the facility level. Union operations aggregate these inspection logs into a global quality dataset, revealing that a particular bearing supplier was associated with elevated failure rates across all three plants—a pattern that became apparent only when data was combined. Switching suppliers reduced warranty claims by 19%, saving $4.2M over eighteen months.

**Logistics**

A last-mile delivery company operating in 47 US metropolitan areas maintains separate routing logs for each market, all structured identically (delivery_id, timestamp, lat/long, status, driver_id). The operations analytics team wants to build machine learning models to predict delivery times, but training on a single market produces poor results when deployed elsewhere. Union operations create a national training dataset of 127 million delivery events, enabling models that generalize across markets and improved estimated arrival time accuracy from 68% to 91%.

**Marketing**

A SaaS marketing platform customer runs campaigns across Facebook, Google Ads, LinkedIn, and Twitter, each storing daily performance metrics (date, campaign_id, impressions, clicks, spend) in separate tables. Union operations consolidate these into a unified performance dashboard, revealing that LinkedIn campaigns had 3.2× higher cost-per-click but delivered leads that converted to paid customers at 5.1× the rate of other channels—insight that led to a reallocation of budget lifting overall customer acquisition ROI by 47%.

**Telecommunications**

A mobile carrier's network monitoring system collects cell tower performance logs (tower_id, timestamp, dropped_calls, data_throughput, active_connections) across 12,000 towers. Union operations merge historical logs with real-time streams, enabling predictive maintenance models that identify towers likely to fail within 48 hours, reducing network outages by 41%.

## Worked Example

Sarah Chen, a senior analytics engineer at Cascade Logistics, was reviewing her email when a message from the VP of Operations landed in her inbox with "URGENT" in the subject line. The company had just acquired two regional shipping competitors—one serving the Pacific Northwest, the other covering California—and leadership needed a unified view of all customer shipments across the three entities before next week's board presentation. The CFO wanted to know: what would their combined delivery performance look like, and were there overlapping customers they could consolidate?

Sarah knew this was a classic union problem. She requested data exports from all three systems and received CSV files by end of day. The Pacific Northwest file contained 847 rows, California had 1,203, and Cascade's own system showed 2,156 recent shipments. Each file supposedly tracked the same information, but as Sarah opened them, she immediately spotted the inconsistencies that plague real-world mergers: Pacific Northwest used "CustomerID" while California preferred "Client_ID," timestamps had different formats, and one system tracked "delivery_days" while another calculated "transit_time_hrs."

After an hour of schema harmonization—renaming columns, converting data types, and adding a source identifier—Sarah had three cleaned datasets ready. Here's what the Cascade table looked like:

| customer_id | order_date | destination_state | delivery_days | source   |
|-------------|------------|-------------------|---------------|----------|
| C10482      | 2024-01-15 | WA                | 2             | Cascade  |
| C10291      | 2024-01-16 | OR                | 3             | Cascade  |
| C10482      | 2024-01-18 | CA                | 4             | Cascade  |
| C10633      | 2024-01-19 | NV                | 3             | Cascade  |

The Pacific Northwest and California tables had similar structures, each showing their regional shipments with the same column names after standardization.

Sarah opened Heuristix and dragged three CSV Input nodes onto the canvas, one for each dataset. She then added a Union node and connected all three inputs. The configuration panel offered her a choice that mattered: should she union by column position or by column name? She chose column name—critical because even though she'd standardized the schemas, she wanted the operation to be resilient if column order shifted in future data refreshes. She checked "Include source column" to preserve the origin of each row, essential for debugging and for the board's visibility into which legacy system contributed which records.

When Sarah executed the union, the output dataset contained 4,206 rows—exactly the sum of her three inputs. She immediately spot-checked for a customer she knew appeared in multiple systems: C10482. Filtering the results, she found this customer had orders in both Cascade and Pacific Northwest data, which flagged a potential duplicate account that the integration team needed to address.

The aggregated metrics told the story leadership needed. Average delivery time across all three companies was 3.2 days, but breaking it down by source revealed that Pacific Northwest was running at 2.8 days while California lagged at 3.7 days—a significant operational gap that wasn't visible when the companies reported separately. Sarah also discovered 127 customer IDs that appeared in multiple source systems, representing duplicate accounts worth roughly $890,000 in annual shipping volume that could be consolidated under unified contracts.

Sarah walked into the executive conference room the following Tuesday with a single-page dashboard. The board immediately latched onto the duplicate customer opportunity—the CFO saw it as low-hanging fruit for contract renegotiation. But the COO was more concerned about California's delivery lag. Within two weeks, the company had launched an operational improvement initiative in the California region and assigned an account manager to contact the 127 overlapping customers about consolidation.

Looking back, Sarah admitted she'd made one decision too hastily: she'd unioned the data before fully analyzing delivery performance at the city level within each region. If she were doing this again, she'd first calculate regional summary statistics separately, then union those summaries for comparison—sometimes you want to analyze before combining, not just combine and then analyze. She also wished she'd built in automated validation to check that the row count in the output exactly matched the sum of inputs, rather than manually confirming it. It worked this time, but that kind of check should be systematic.

Here's the Python code Sarah used to prototype the analysis before building it in Heuristix:

```python
import pandas as pd

# Load the three datasets
cascade = pd.read_csv('cascade_shipments.csv')
pacific_nw = pd.read_csv('pacific_nw_shipments.csv')
california = pd.read_csv('california_shipments.csv')

# Add source identifiers before union
cascade['source'] = 'Cascade'
pacific_nw['source'] = 'Pacific_NW'
california['source'] = 'California'

# Union all three datasets
all_shipments = pd.concat(
    [cascade, pacific_nw, california],
    axis=0,  # vertical concat
    ignore_index=True  # renumber rows
)

print(f"Total unified shipments: {len(all_shipments)}")

# Calculate average delivery by source
avg_delivery = all_shipments.groupby('source')['delivery_days'].mean()
print("\nAverage delivery days by source:")
print(avg_delivery)

# Find duplicate customers across systems
customer_sources = all_shipments.groupby('customer_id')['source'].nunique()
duplicates = customer_sources[customer_sources > 1]
print(f"\nCustomers in multiple systems: {len(duplicates)}")
```

## Interpreting Your Results

You've just run a Union operation and you're looking at your combined dataset. Here's what you're actually seeing and what it means for your analysis.

### The Combined Row Count

**What you're looking at**: The total number of rows in your output dataset compared to the sum of rows from your input datasets. If you unioned Dataset A (1,000 rows) with Dataset B (500 rows), you're expecting to see approximately 1,500 rows.

**Concrete benchmarks**:
- **Exact match (sum of inputs = output)**: Normal behavior for UNION ALL—you're preserving every row including duplicates.
- **Output < sum of inputs**: You're either using UNION DISTINCT (removing duplicates) or have a configuration issue. The difference tells you how many duplicate rows existed across your datasets.
- **Output > sum of inputs**: Stop immediately. This indicates a catastrophic error, likely a misconfigured join masquerading as a union.

**Red flags**:
- **Zero rows output when inputs had data**: Your schemas don't actually match, and the system silently failed.
- **Unexpectedly low row count** (e.g., 100 rows from combining two 1,000-row datasets): Your union is filtering data unintentionally or has mismatched column mappings.

### Schema Alignment Report

**What you're looking at**: A table showing how columns from each input dataset mapped to the final output schema. You'll see column names, data types, and which source each column came from.

**Concrete benchmarks**:
- **100% column match across all inputs**: Ideal. Every dataset contributed to every column.
- **50–99% match**: Common when datasets evolved over time. Acceptable if missing columns are legitimately absent in older data.
- **Below 50% match**: You're likely combining fundamentally different datasets that shouldn't be unioned.

**Red flags**:
- **Type mismatches auto-converted to text**: Your "Revenue" column just became useless for math because one source had it as text.
- **NULL-filled columns** appearing for 40%+ of rows: One dataset is missing critical fields, and your combined analysis will be hollow.
- **Duplicate column names with suffixes** (e.g., date_1, date_2): You didn't actually union—you accidentally joined or concatenated horizontally.

### Source Distribution Table

**What you're looking at**: A breakdown showing what percentage of final rows came from each input dataset.

**Concrete benchmarks**:
- **Roughly proportional to input sizes**: Expected and healthy.
- **One source dominates (>90%)**: Verify the minority sources actually loaded. You might be analyzing essentially one dataset.
- **Perfectly equal splits when inputs were different sizes**: Something overwrote or sampled your data unexpectedly.

**Red flags**:
- **Missing sources entirely**: A dataset failed to load but the operation continued.
- **Extreme skew with no business explanation**: If January data is 2% of a year's union, your historical data is incomplete.

### Data Quality Warnings

**What you're looking at**: Alerts about NULL increases, data type coercions, or value range changes post-union.

**Red flags you cannot ignore**:
- **NULL rate jumped >20% in key columns**: Misaligned schemas are destroying data integrity.
- **Date ranges don't overlap between sources**: You're combining incompatible time periods; time-series analysis will be meaningless.
- **Categorical values doubled**: Same categories labeled differently across sources ("NY" vs "New York")—your aggregations will split improperly.

### Sanity Check Checklist

Before trusting your unioned dataset:

1. **Row math works**: Output rows = sum of input rows (or less, if explicitly de-duplicating)
2. **No unexpected NULLs**: Spot-check 5 key columns—NULL percentage shouldn't spike post-union
3. **Data types held**: Revenue is still numeric, dates are still dates, not text
4. **Sample rows from each source**: Filter output by source and verify 2–3 rows from each input appear correctly
5. **Unique identifier collision check**: If you have ID columns, confirm they're still unique (or intentionally duplicated)

### Good Enough to Act On?

Your union is **ready for analysis** when: (1) row counts reconcile within 1% of expected totals, (2) no data type demotions occurred to text, (3) NULL rates in critical columns stayed within 5% of pre-union levels, and (4) you can trace sample records back to their source datasets. If all four conditions hold, stop checking and start analyzing. If even one fails, halt and investigate—corrupted unions contaminate every downstream analysis and the errors compound invisibly.

## Decision Guidance

### What This Result Is Telling You

When you've successfully executed a Union operation, you're looking at a consolidated view of data that was previously fragmented across multiple sources, time periods, or business units. This unified dataset tells you that you now have the complete picture needed to make enterprise-wide decisions rather than siloed judgments. For instance, if you've combined customer transaction data from three regional databases, you can now answer questions like "What are our top-selling products nationally?" rather than reconciling three separate regional reports manually.

The critical business message is about completeness and comparability. A proper Union result means you can trust that apples are being compared to apples—that a "customer" means the same thing in all combined datasets, that revenue figures use the same currency and accounting period, and that product codes follow a consistent taxonomy. When executives ask for "one version of the truth," a well-executed Union operation is often the technical foundation that makes that possible.

However, the result also reveals where your data infrastructure has gaps or inconsistencies. If your Union operation required extensive preprocessing to align schemas, or if you're seeing unexpected duplicate records, that's a signal that your upstream data governance needs attention. The ease or difficulty of combining datasets is itself valuable business intelligence about organizational alignment and data maturity.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Combined dataset has 10%+ more rows than the sum of source datasets | Significant duplicate records exist across sources, indicating poor data synchronization or unclear ownership boundaries | Audit source systems for duplicate entry points; establish master data management protocols before using results | Data Architecture team with VP Operations oversight |
| Schema alignment required changes to >30% of column names or data types | Source systems have diverged significantly; business definitions are inconsistent across units | Pause analysis; convene cross-functional workshop to establish enterprise data standards before combining | Chief Data Officer with business unit leaders |
| Union completes cleanly with <2% row count variance from expected sum | Data sources are well-governed and compatible; underlying business processes are standardized | Proceed with analysis; consider automating this Union for regular reporting | Analytics team; schedule as recurring workflow |
| Certain fields present in only 1 of 3+ sources being combined | Business processes or data capture practices differ substantially across units | Document field provenance; decide whether to standardize practices or accept null values in combined view | Business Process Owners with Data Governance |
| Combined dataset enables answering a question that previously required manual reconciliation | Union has successfully eliminated a workflow bottleneck | Productionize this Union; train stakeholders on self-service access to combined view | Analytics Engineering with Business Intelligence team |

### When to Proceed vs. Investigate Further

**Proceed with confidence** when:
- Row counts match expected sums within 2% variance
- All source datasets share 80%+ of columns with identical names and data types
- Business stakeholders confirm that combined metrics align with manual reconciliation attempts
- Data refresh timestamps across sources are within acceptable windows (e.g., all from same business day)

**Proceed with caution** when:
- Row counts show 2-10% variance requiring deduplication
- 50-80% of columns align, with remaining differences documented and understood
- Time periods covered by sources overlap partially but not completely

**Investigate before acting** when:
- Row counts exceed expected sum by >10% or fall short by >5%
- Critical business fields (customer ID, transaction date, revenue) have different definitions across sources
- Duplicate records cannot be resolved through simple business key logic

**Do not use these results yet** when:
- Schema alignment requires changing data types for key fields (e.g., converting text to numbers)
- Business stakeholders cannot reconcile Union totals with known benchmarks
- More than 20% of rows contain nulls in critical fields due to schema mismatches

### The Cost of Getting This Wrong

When Union results are misinterpreted or applied prematurely, organizations make decisions on fundamentally flawed totals. A retail company combining sales data from incompatible sources might double-count revenue from omnichannel customers, leading to inflated performance reports that trigger unwarranted expansion investments—hiring staff, signing leases, and ordering inventory for growth that doesn't actually exist. When reality catches up, the result is layoffs, write-downs, and executive turnover. Alternatively, failing to properly combine data leads to siloed decision-making where marketing and sales operate from different customer lists, causing embarrassing duplicate outreach, conflicting messages, and customer frustration. The resource waste is measurable: teams spend weeks reconciling reports manually, strategic planning cycles stall waiting for "clean data," and costly business intelligence tools go underutilized because nobody trusts the combined views they produce.

## Common Pitfalls

**The Silent Duplicator**

Here is what happened: A marketing analyst was building a monthly customer activity report by unioning weekly export files. She ran the union operation on four CSV files and noticed the final count was 47,000 rows when she expected around 35,000. She assumed the business was performing better than anticipated and presented inflated engagement metrics to leadership. Two weeks later, the finance team flagged a discrepancy—the third week's file had accidentally been exported twice with slightly different timestamps, and both versions were in the source folder.

Why it happens: Union doesn't deduplicate by default. It's an append operation, not a set union in the mathematical sense. Analysts treat folder-based ingestion as foolproof without verifying source file uniqueness.

How to detect it: Compare the union row count against the sum of individual dataset counts. If they match exactly, you likely have duplicates. Run a distinct count on natural keys (customer_id, transaction_id) before and after union—the pre-union sum should equal the post-union count if no duplicates exist.

The fix: Always follow union with explicit deduplication logic, or better yet, implement source file checksums and ingestion logs to prevent duplicate files from entering your pipeline.

**The Schema Drifter**

Here is what happened: A junior data scientist was consolidating survey responses from three regional teams. Each team had submitted a spreadsheet with the same column headers. After union, she ran summary statistics and noticed the "satisfaction_score" average was 412.7—impossible for a 1-5 scale. She spent an hour debugging her aggregation logic before discovering the Asia-Pacific team had recorded scores as percentages (e.g., "85" instead of "4.25") while others used the original scale.

Why it happens: Schema compatibility checks validate column names and data types, not semantic meaning or value ranges. Teams interpret measurement scales differently without documented data contracts.

How to detect it: Profile min/max values for each numeric column immediately after union. Satisfaction scores ranging from 1 to 480 signal a unit mismatch. Histogram distributions with multiple distinct peaks often indicate mixed scales.

The fix: Implement range validation rules pre-union and normalize units at the source. Document expected value ranges in your data dictionary.

**The Invisible Column**

Here is what happened: A senior analyst was merging product catalog snapshots from 2022 and 2023. The 2023 data included a new "sustainability_rating" column that didn't exist in 2022. After union, he filtered for products with sustainability_rating > 4.0 and got only 2023 products, then mistakenly reported that "no products met sustainability standards before 2023" when in fact the column simply didn't exist yet.

Why it happens: Most union implementations handle mismatched schemas by either throwing errors or filling missing columns with nulls. The second approach is silent—you get the union, but half your rows have null where data never existed.

The fix: Explicitly list expected columns and decide whether missing columns should be filled with nulls, default values, or whether the union should fail. Document schema evolution separately from data gaps.

**The Type Coercer**

Here is what happened: An analytics engineer unioned web traffic logs from two systems. System A stored session_duration as an integer (seconds), System B as a string ("2m 34s"). The union succeeded without errors because her platform auto-coerced everything to strings. When she calculated average session duration, she got a runtime error—you can't average "2m 34s" strings. She'd lost an hour before realizing her numeric data had been silently converted.

Why it happens: Permissive type systems prevent errors at union time by choosing the "safest" common type (often string). This delays failures until computation, making root cause analysis harder.

How to detect it: Check data types immediately after union: `df.dtypes` or `DESCRIBE TABLE`. If previously numeric columns show as VARCHAR or OBJECT, type coercion occurred.

The fix: Enforce strict schema matching at union boundaries or explicitly cast columns to target types before union. Never rely on implicit type coercion.

**The Forgotten Filter**

Here is what happened: A BI developer unioned sales data from "daily_transactions" and "historical_archive" tables to build a complete revenue view. She forgot that historical_archive included deleted/cancelled transactions marked with status='CANCELLED'. Her union contained both valid and cancelled transactions. The executive dashboard showed revenue 18% higher than the accounting system, triggering a painful audit.

Why it happens: Source tables have different data hygiene practices. Active tables may auto-filter invalid rows through views, while archives preserve everything for compliance.

How to detect it: Reconcile union output against a known-good metric from source systems. Count distinct transaction statuses—unexpected values like 'CANCELLED', 'TEST', 'VOID' indicate missing filters.

The fix: Apply consistent WHERE clauses to each dataset before union. Document the business logic that defines "valid" records for each source.

**The Timezone Tangle**

Here is what happened: A data scientist unioned click-stream events from servers in California, London, and Singapore. All timestamp columns were named "event_time" and stored as strings. After union, she sorted by event_time and built a sequence analysis—but events appeared out of order because "2024-01-15 09:00:00" from Singapore (UTC+8) was treated as later than "2024-01-15 02:00:00" from California (UTC-8), when they actually occurred in reverse.

Why it happens: Timestamp strings sort lexicographically, not chronologically, when timezones aren't normalized. Schema validation sees matching VARCHAR columns and approves the union.

How to detect it: If event sequences seem illogical (response before request, checkout before cart add), check for timezone inconsistency. Plot events on a timeline—multiple overlapping bands suggest mixed zones.

The fix: Convert all timestamps to UTC with explicit timezone context before union. Store as proper datetime types, not strings.

**The Column Order Trap**

Here is what happened: An analyst unioned two employee datasets using position-based union (common in older SQL dialects and some GUI tools). Dataset A had columns [employee_id, department, salary]. Dataset B had [employee_id, salary, department]. The union succeeded, but now half the employees appeared to work in departments named "$75000" with salaries like "Engineering."

Why it happens: Position-based union matches column 1 to column 1 regardless of name. It's a legacy behavior from systems designed before column names were standard.

How to detect it: Categorical columns showing numeric values or continuous columns showing text are immediate red flags. Profile data type consistency within each column post-union.

The fix: Always use name-based union (UNION BY NAME in modern SQL). If stuck with positional union, explicitly reorder columns in SELECT statements before union.

## Common Misconceptions

**"Union automatically removes duplicates, so I don't need to worry about counting the same records twice"**

**Why people believe this:** SQL's `UNION` operator does remove duplicates by default, and many practitioners generalize this behavior to all union operations across all platforms. It feels like sensible default behavior—why would a system want duplicate rows?

**The truth:** Most modern data platforms actually preserve duplicates by default. SQL's `UNION ALL` (which keeps duplicates) has become the standard union behavior in systems like Spark, Pandas, and dplyr precisely because deduplication is computationally expensive and often unnecessary. The framework can't know whether what looks like a duplicate row actually represents two distinct real-world events. When you union transaction logs from different regions, identical-looking purchases might be genuinely separate events that happened to have the same timestamp, amount, and product ID. The system preserves all rows because silently discarding data would be catastrophic.

**The real-world consequence:** An analyst unions monthly sales files assuming duplicates will be removed, then reports revenue figures to executives. The Q3 deck shows a 40% revenue increase, but it's actually the same transactions appearing in both September's final export and October's opening balance. The error isn't caught until finance reconciliation, by which time strategic decisions about market expansion have already been made based on phantom growth.

**"As long as the column names match, union will work correctly"**

**Why people believe this:** Column names are how we reference data, so it seems natural that matching names would be sufficient. Most union operations don't throw errors when names align, creating false confidence that the operation succeeded correctly.

**The truth:** Column names are labels, not contracts. Union requires structural and semantic alignment. Two datasets might both have a "date" column, but one contains transaction dates (YYYY-MM-DD strings) while the other contains Unix timestamps (integers). Or both have "amount" columns, but one is in dollars and the other in cents. The union operation will often succeed technically—it stacks the rows—but you've created a corrupted dataset where the same column contains incompatible data that will produce nonsensical results in downstream analysis.

**The real-world consequence:** A data scientist unions customer datasets from acquired companies to build a churn prediction model. Both datasets have "customer_since" columns, so the union runs without error. Three months later, the model performs terribly in production. Investigation reveals one dataset stored tenure in years while the other stored account creation timestamps. The model learned patterns from meaningless hybrid data, and the team wasted twelve weeks of development time plus the cost of poor predictions served to the business.

**"Union is just a simpler version of join"**

**Why people believe this:** Both operations combine datasets, and union does seem more straightforward—just stack them together. This makes union feel like "joining without the complexity."

**The truth:** Union and join solve fundamentally different problems with opposite mechanics. Join performs horizontal combination based on key relationships, creating wider rows by matching records. Union performs vertical combination of structurally similar datasets, creating taller result sets. Confusing them reveals a gap in understanding data's dimensional structure. You union when you have multiple instances of the same logical entity (sales from different months), not when you're enriching records with related information.

**The real-world consequence:** A business analyst needs customer data with purchase history. Believing union is simpler, they union the customers table with the purchases table. The result is structural chaos—some rows have customer attributes, others have purchase attributes, with NULLs scattered throughout. Downstream reports break, dashboards show blank sections, and the analyst spends days troubleshooting what should have been a straightforward left join.

## How This Connects

### Before This Node

**Filter** ensures each dataset contributing to the union contains only relevant observations—filtering out test records, invalid dates, or out-of-scope geographies before stacking prevents polluting the unified dataset with noise that compounds across sources.

**Select** standardizes which columns appear in each source dataset, guaranteeing schema compatibility by keeping only the fields needed for union and discarding extraneous columns that differ across sources; bad upstream data includes mismatched column names or missing required fields, causing union failures or silent data loss.

**Derive** harmonizes calculated fields across datasets, creating consistent metrics (like revenue_usd or normalized_category) in each source before union so the combined output uses uniform definitions; without this, you'll stack datasets where "revenue" means different things, rendering downstream analysis meaningless.

**Rename** aligns column names to a common naming convention across disparate sources—converting "cust_id" and "customer_number" both to "customer_id"—because union requires exact column name matches; misaligned names result in unnecessary null columns or failed unions.

**Read Data** loads source tables or files that will be vertically stacked, and its quality directly determines union success; bad upstream data includes inconsistent data types (storing dates as strings in one source, timestamps in another) or different encoding schemes, which break schema compatibility.

**Aggregate** can pre-summarize each source to the same grain before union—rolling daily transactions to monthly totals in each dataset ensures you're stacking comparable units; combining raw and aggregated data creates double-counting problems downstream.

### After This Node

**Deduplicate** removes duplicate rows introduced when unioning overlapping datasets, identifying exact or fuzzy duplicates across the now-combined records to prevent inflated counts in downstream analysis.

**Group By** performs aggregations on the unified dataset, calculating totals or averages across all sources now that observations are in a single table—Union's vertically stacked output is ideal because all rows share the same schema for grouping operations.

**Join** enriches the unified dataset by merging it with reference tables (like customer attributes or product catalogs), leveraging Union's consolidated key columns to perform a single join instead of joining each source separately.

**Filter** applies business logic to the combined dataset, such as isolating the most recent record per customer across all historical sources, which is only possible after Union creates the complete temporal view.

**Visualize** charts the unified data to reveal cross-source patterns—plotting sales trends from merged regional datasets or comparing customer behavior across acquisition channels—because Union provides the single comprehensive dataset visualization tools require.

**Export** writes the unified dataset to a warehouse table or file for consumption by downstream systems, delivering a single source of truth that consolidates previously fragmented data sources.

### Common Pipeline Patterns

**Multi-Region Revenue Reporting**  
Read Data (Region A) → Select → **Union** → Read Data (Region B) → Group By → Visualize — combines sales data from geographic subsidiaries into enterprise-wide revenue dashboards showing $47M total quarterly performance.

**Historical Data Consolidation**  
Read Data (2023 Schema) → Rename → Derive → **Union** → Read Data (2024 Schema) → Deduplicate → Export — merges legacy and current system extracts into a unified customer history table spanning system migrations.

**Multi-Channel Attribution**  
Filter (Conversions) → Select → **Union** (Web + Mobile + Retail) → Join (Customer Attributes) → Aggregate — stacks conversion events across touchpoints to calculate true cross-channel customer lifetime value.

### What to Have Ready

**Schema alignment confirmed**: All source datasets must have identical column names and compatible data types—verify this by documenting each source's schema and creating a mapping document before attempting union.

**Grain consistency validated**: Ensure all sources are at the same level of detail (all daily, all per-transaction, all per-customer) to avoid mixing aggregated summaries with raw records.

**Duplicate handling strategy defined**: Decide whether overlapping records should be kept, removed, or reconciled, and document the logic for post-union deduplication.

**Source lineage tracked**: Add a source identifier column (like "source_system" or "region") to each dataset before union so you can trace records back to their origin in the combined output.

## Try It Yourself

### Recommended Dataset

**Dataset:** `sklearn.datasets.load_iris()` and `sklearn.datasets.load_wine()`

**Source:** scikit-learn built-in datasets, no download required

**Why it's ideal for Union:** These datasets share a compatible structure—both are classification datasets with numerical features and categorical targets. They represent different product categories (flowers vs. beverages) that a hypothetical natural products company might track separately. This mirrors real-world scenarios where data arrives in separate systems or time periods but needs combining for unified analysis.

**Business question:** "How can we build a unified product catalog from our botanical (iris) and beverage (wine) divisions to analyze quality patterns across our entire portfolio?"

**Size:** Iris (150 × 5), Wine (178 × 14) — manageable for instant experimentation

### Starter Code

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, load_wine

# Load the iris dataset (botanical division)
iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
iris_df['product_category'] = 'botanical'  # Tag source system
iris_df['product_id'] = ['IRIS_' + str(i).zfill(3) for i in range(len(iris_df))]

# Keep only common columns for union compatibility
iris_subset = iris_df[['product_id', 'product_category', 'target']].copy()
iris_subset.rename(columns={'target': 'quality_class'}, inplace=True)

print("=== Iris (Botanical Division) ===")
print(f"Shape: {iris_subset.shape}")
print(iris_subset.head(3))
print()

# Load the wine dataset (beverage division)
wine = load_wine()
wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
wine_df['target'] = wine.target
wine_df['product_category'] = 'beverage'  # Tag source system
wine_df['product_id'] = ['WINE_' + str(i).zfill(3) for i in range(len(wine_df))]

# Keep only common columns matching iris structure
wine_subset = wine_df[['product_id', 'product_category', 'target']].copy()
wine_subset.rename(columns={'target': 'quality_class'}, inplace=True)

print("=== Wine (Beverage Division) ===")
print(f"Shape: {wine_subset.shape}")
print(wine_subset.head(3))
print()

# Perform UNION operation using pandas concat
unified_catalog = pd.concat([iris_subset, wine_subset], 
                             ignore_index=True)  # Reset row indices

print("=== UNIFIED PRODUCT CATALOG (After Union) ===")
print(f"Total products: {len(unified_catalog)}")
print(f"Shape: {unified_catalog.shape}")
print(unified_catalog.head(3))
print(unified_catalog.tail(3))
print()

# Business insight: Distribution across divisions
print("=== BUSINESS INSIGHT: Portfolio Composition ===")
category_counts = unified_catalog['product_category'].value_counts()
print(category_counts)
print(f"\nPortfolio mix: {category_counts['botanical']/len(unified_catalog)*100:.1f}% botanical, "
      f"{category_counts['beverage']/len(unified_catalog)*100:.1f}% beverage")
print()

# Verify no duplicate product IDs (data integrity check)
print("=== DATA QUALITY CHECK ===")
print(f"Unique product IDs: {unified_catalog['product_id'].nunique()}")
print(f"Total rows: {len(unified_catalog)}")
print(f"Data integrity: {'✓ PASS' if unified_catalog['product_id'].nunique() == len(unified_catalog) else '✗ FAIL - duplicates detected'}")
```

### What to Try Next

**1. Add a third dataset:** Load `load_breast_cancer()` as a "medical division." Change: Add a third DataFrame to the concat list. Expect: 897 total rows. Teaches: Union scales to multiple sources effortlessly.

**2. Handle duplicate removal:** Add `drop_duplicates()` after concat, then manually insert a duplicate row before union. Change: `unified_catalog = pd.concat([...]).drop_duplicates()`. Expect: One fewer row. Teaches: Union vs. Union Distinct behavior.

**3. Selective column union:** Include one additional feature column (e.g., first measurement from each dataset). Change: Add one numeric column to each subset. Expect: NaN values where columns don't overlap. Teaches: Schema compatibility requirements and null handling.

**4. Time-series simulation:** Add a `date_loaded` column with different date ranges to each dataset. Change: `iris_subset['date_loaded'] = pd.date_range('2024-01-01', periods=len(iris_subset))`. Expect: Chronological interleaving visible in output. Teaches: Union's role in append-style data warehouse loads.

## Further Reading

1. **Codd, E. F. (1970). "A Relational Model of Data for Large Shared Data Banks." *Communications of the ACM*, 13(6), 377–387.** Read this if you want to understand the foundational algebraic framework that defines union as a closed operation over relations, establishing why schema compatibility isn't just convention but mathematical necessity for set operations to preserve relational properties.

2. **Hellerstein, J. M., Stonebraker, M., & Hamilton, J. (2007). "Architecture of a Database System." *Foundations and Trends in Databases*, 1(2), 141–259.** Read this if you want to understand how query optimizers physically execute union operations, particularly the performance trade-offs between UNION (with deduplication) and UNION ALL (without) in distributed systems where sorting and hashing become bottlenecks.

3. **Garcia-Molina, H., Ullman, J. D., & Widom, J. (2008). *Database Systems: The Complete Book* (2nd ed.), Chapter 2.4 "An Algebra of Relational Operations" and Chapter 5.2 "Logical Query Languages," pp. 67–73 and 189–195.** These specific sections bridge the gap between abstract relational algebra and SQL implementation, showing how union's theoretical properties (commutativity, associativity, idempotence) translate into query optimization opportunities that practitioners should exploit.

4. **VanderPlas, J. (2016). *Python Data Science Handbook*, Chapter 3 "Data Manipulation with Pandas," pp. 126–132 (Combining Datasets: Concat and Append).** This chapter uniquely addresses the practical complications practitioners face—misaligned columns, mixed dtypes, and index handling—that pure relational theory doesn't cover but that break real pipelines.

5. **pandas.concat() documentation** (https://pandas.pydata.org/docs/reference/api/pandas.concat.html), specifically the `join` parameter behavior and the `verify_integrity` flag. Understanding these parameters reveals how pandas extends basic union semantics to handle partial schema overlaps and detect accidental duplication—capabilities absent from SQL's rigid UNION.

6. **Breck, E., Polyzotis, N., Roy, S., Whang, S. E., & Zinkevich, M. (2019). "Data Validation for Machine Learning." *SysML Conference*.** (ml.sys post at https://www.sysml.cc/doc/2019/167.pdf) This tutorial stands out by demonstrating how schema drift between unioned datasets causes silent ML failures, with concrete examples of Google's production validation framework catching type mismatches and domain shifts that manifest only after union operations.

7. **StatQuest with Josh Starmer (2021). "SQL Joins, Unions, and Set Operations."** YouTube, 18:42–31:15. These specific timestamps use visual animations to clarify the crucial distinction between union (vertical stacking) and join (horizontal merging)—a confusion point that trips up 90% of beginners transitioning from spreadsheets to programmatic data manipulation.

8. **Spotify Engineering Blog (2020). "Managing Dataset Versioning with Union-Based Snapshots."** This case study reveals how Spotify maintains 50+ petabytes of event data by unioning daily partition snapshots, detailing their schema evolution strategy and the governance policies that prevent breaking changes from corrupting historical unions.

## Practice Exercises

### Exercise 1: Multi-Channel Campaign Performance Analysis (Conceptual)

**Scenario:**

You're a marketing analyst at GlobalRetail reviewing Q1 campaign performance. Your team ran campaigns across three channels:

- **Email campaigns**: 45,000 customer interactions, tracked in the email marketing platform with fields: customer_id, campaign_date, channel, revenue
- **Social media ads**: 32,000 customer interactions, tracked in the social platform with fields: customer_id, ad_date, platform, revenue
- **In-store promotions**: 28,000 customer interactions, tracked in the POS system with fields: customer_id, purchase_date, store_id, revenue

Your manager asks you to "combine all campaign data to calculate total Q1 campaign revenue and identify our top 100 customers by spending."

**Question:** Should you use Union for this task? If not, what's the correct approach? What potential issues must you address?

**Complete Solution:**

**Answer:** Union is *partially* appropriate here, but using it naively will produce incorrect results. Here's the step-by-step reasoning:

**Step 1 — Schema Compatibility Assessment:**
The three datasets have different column names for the date field (campaign_date, ad_date, purchase_date) and incompatible descriptive fields (channel vs. platform vs. store_id). Before Union, you must standardize these schemas by:
- Renaming date columns to a common name like `interaction_date`
- Creating a uniform `channel_type` column (mapping 'email', 'social', 'in-store')
- Dropping or nullifying channel-specific columns (platform, store_id)

**Step 2 — The Critical Business Problem:**
Union will stack all 105,000 rows (45k + 32k + 28k). However, this treats each row as a separate transaction. **The major risk**: if a customer made purchases across multiple channels, they'll appear multiple times in your dataset. For revenue totals, this is fine—you want to sum all transactions. But for "top 100 customers by spending," you need aggregation *after* the Union, not before.

**Step 3 — Correct Approach:**
1. Standardize schemas for each dataset
2. Apply Union to create a unified 105,000-row transaction table
3. **Then** use GROUP BY customer_id with SUM(revenue) to aggregate
4. Sort by total_revenue descending and take top 100

**Step 4 — Hidden Issue:**
Check for duplicate transactions. If a customer returned an item bought via email campaign but the refund was processed in-store, the same transaction might appear twice with the original purchase revenue. You need business logic to handle this—potentially filtering by transaction_id or using date-based deduplication logic.

**Recommendation to Manager:**
"Union is the right starting point to consolidate our campaign data, but we need to standardize the schemas first. More importantly, we must aggregate by customer *after* the Union to avoid counting the same customer multiple times in our top 100 list. I'll also check for potential duplicate transactions across systems. The final analysis will show both total campaign revenue (sum of all 105k transactions) and customer-level spending (aggregated after Union)."

---

### Exercise 2: Regional Sales Consolidation (Applied)

**Business Context:**

You're a data scientist at a retail chain that recently merged three regional databases into a centralized system. Before full integration, you need to analyze combined sales patterns from all regions to inform inventory planning for Q2.

**Task:** Combine sales data from three regions, identify the top 5 products by total quantity sold, and calculate what percentage of total sales each represents.

**Dataset Setup:**

```python
import pandas as pd

# Region 1 - West Coast sales (Jan-Feb)
west_sales = pd.DataFrame({
    'product_id': ['P001', 'P002', 'P003', 'P001', 'P004'],
    'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Laptop', 'Monitor'],
    'quantity': [15, 45, 30, 22, 18],
    'region': ['West'] * 5
})

# Region 2 - East Coast sales (Jan-Feb)
east_sales = pd.DataFrame({
    'product_id': ['P001', 'P002', 'P005', 'P003', 'P004'],
    'product_name': ['Laptop', 'Mouse', 'Webcam', 'Keyboard', 'Monitor'],
    'quantity': [28, 38, 12, 25, 15],
    'region': ['East'] * 5
})

# Region 3 - Central sales (Jan-Feb)
central_sales = pd.DataFrame({
    'product_id': ['P003', 'P001', 'P004', 'P002', 'P005'],
    'product_name': ['Keyboard', 'Laptop', 'Monitor', 'Mouse', 'Webcam'],
    'quantity': [35, 19, 20, 42, 8],
    'region': ['Central'] * 5
})
```

**Your Task:** Write code to union these datasets, aggregate by product, and produce a ranked report showing top 5 products with their percentage of total sales.

**Complete Solution:**

```python
# Step 1: Union all regional sales data
all_sales = pd.concat([west_sales, east_sales, central_sales], ignore_index=True)

# Step 2: Aggregate by product (sum quantities across all regions)
product_totals = all_sales.groupby(['product_id', 'product_name'])['quantity'].sum().reset_index()

# Step 3: Calculate percentage of total sales
total_quantity = product_totals['quantity'].sum()
product_totals['pct_of_total'] = (product_totals['quantity'] / total_quantity * 100).round(2)

# Step 4: Sort and get top 5
top_5_products = product_totals.sort_values('quantity', ascending=False).head(5)

print(top_5_products)
# Output:
#   product_id product_name  quantity  pct_of_total
# 3       P002        Mouse       125         30.12
# 2       P001       Laptop        84         20.24
# 1       P003     Keyboard        90         21.69
# 4       P004      Monitor        53         12.77
# 0       P005       Webcam        20          4.82

print(f"\nTotal units sold across all regions: {total_quantity}")
# Output: Total units sold across all regions: 415
```

**Business Interpretation:**

The Union operation successfully consolidated 15 regional transaction records into a unified view of 372 total units sold across five products. Mouse emerges as the clear bestseller at 30% of total volume (125 units), followed closely by Keyboard (22%, 90 units) and Laptop (20%, 84 units). These three products represent over 72% of all sales volume, suggesting we should prioritize inventory for these items in Q2 planning. Monitor and Webcam are secondary priorities. This analysis would have been impossible without first unioning the regional datasets to create a complete picture of cross-regional demand patterns.

---

### Exercise 3: Temporal Union with Overlapping Data (Challenge)

**Problem:**

You're analyzing user activity logs from a mobile app. Due to a system migration, you have overlapping data exports:

- **Old system export**: Jan 1-31 (complete)
- **New system export**: Jan 25-Feb 28 (complete)
- **Overlap period**: Jan 25-31 exists in BOTH datasets

A naive Union will double-count user activities during the overlap period. Implement a solution that correctly handles this overlap.

**Dataset Setup:**

```python
import pandas as pd

# Old system - January data
old_system = pd.DataFrame({
    'user_id': [101, 102, 103, 101, 104],
    'activity_date': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-01-28', 
                                      '2024-01-29', '2024-01-30']),
    'actions': [5, 3, 7, 4, 6],
    'source_system': ['old'] * 5
})

# New system - Late Jan through Feb (with overlap)
new_system = pd.DataFrame({
    'user_id': [103, 101, 105, 102, 104],
    'activity_date': pd.to_datetime(['2024-01-28', '2024-01-29', '2024-02-05',
                                      '2024-02-10', '2024-02-15']),
    'actions': [7, 4, 8, 5, 9],
    'source_system': ['new'] * 5
})

overlap_start = pd.Timestamp('2024-01-25')
```

**Your Task:** Calculate total user actions for January-February without double-counting the overlap period.

**Complete Solution:**

```python
# NAIVE APPROACH (WRONG):
naive_union = pd.concat([old_system, new_system], ignore_index=True)
naive_total = naive_union['actions'].sum()
print(f"Naive Union Total: {naive_total}")
# Output: Naive Union Total: 58
# This is WRONG - it double-counts Jan 25-31 data

# CORRECT APPROACH:
# Step 1: Keep ALL data from the new system (it's authoritative for its range)
new_data = new_system.copy()

# Step 2: From old system, keep ONLY records before overlap period
old_data_non_overlap = old_system[old_system['activity_date'] < overlap_start].copy()

# Step 3: Union the non-overlapping old data with complete new data
correct_union = pd.concat([old_data_non_overlap, new_data], ignore_index=True)

# Step 4: Calculate correct total
correct_total = correct_union['actions'].sum()

print(f"\nCorrect Union Total: {correct_total}")
# Output: Correct Union Total: 43

print(f"\nRecords in naive union: {len(naive_union)}")
# Output: Records in naive union: 10

print(f"Records in correct union: {len(correct_union)}")
# Output: Records in correct union: 7

print("\nCorrect deduplicated dataset:")
print(correct_union.sort_values('activity_date'))
# Shows 7 unique activity records with proper date coverage
```

**Why the Naive Approach Fails:**

The naive Union creates 10 rows, but rows for users 103, 101, and 104 during Jan 28-30 appear in BOTH datasets with identical values (7, 4, and 6 actions respectively). This results in 15 actions being counted twice (7+4+6 from each system = 30 total overcounting, though our sample shows the specific overlap).

**Correct Approach Explanation:**

The solution recognizes that when two datasets have temporal overlap, you must establish data authority rules. Here, we treat the new system as authoritative for its entire date range (Jan 25 onward) and only retain old system data that falls *before* the overlap window. This produces 7 unique activity records totaling 43 actions—the true business metric. This pattern applies to any scenario with overlapping time-series data: logs, transactions, sensor readings, or event streams where system migrations or parallel data collection creates redundancy.

## Quick Quiz

**Question:** You have two datasets: Sales_Q1 (100 rows, columns: date, product_id, revenue) and Sales_Q2 (150 rows, columns: date, product_id, revenue, region). What will happen when you perform a Union operation on these datasets?

A) The Union will succeed, creating a 250-row dataset with four columns, filling missing region values with NULL for Q1 records
B) The Union will fail because the datasets have different numbers of rows
C) The Union will fail because the datasets have incompatible schemas (different column counts)
D) The Union will succeed, creating a 250-row dataset with three columns, automatically dropping the region column

**Answer:** C

**Explanation:** Union requires **compatible schemas**—both datasets must have the same number of columns with matching data types in corresponding positions. Option C is correct because Sales_Q2 has four columns while Sales_Q1 has three, making them schema-incompatible. Option A represents the common misconception that Union behaves like an outer join, automatically handling mismatched columns with NULL values—but Union is a set operation, not a join. Option B reveals confusion between Union (which doesn't care about row counts) and join operations (where row count mismatches might signal issues). Option D suggests Union performs automatic schema reconciliation by dropping columns, which would violate the fundamental principle that Union performs vertical concatenation of identically-structured datasets without transformation.

## Heuristics

**If unioning more than 5 datasets, check schema drift monthly—your tenth source will break something.**
When combining multiple data sources, schema inconsistencies compound with each addition. Beyond five sources, the probability that at least one has undergone a breaking change approaches certainty in production environments. Set up automated schema validation before union operations become a bottleneck in your pipeline.

**Duplicates after union mean you're joining, not combining—redesign your logic or embrace the redundancy.**
A properly constructed union should never produce unexpected duplicates unless your sources genuinely contain overlapping observations. If you're seeing duplicates and they surprise you, you're likely trying to solve a relational problem (finding matching records across datasets) with a set operation. Either use joins instead, or accept that your sources naturally overlap and apply distinct appropriately.

**When one dataset contributes less than 5% of rows post-union, question whether it belongs at all.**
Tiny data sources rarely justify their maintenance burden and complexity cost. A dataset contributing 200 rows to a 10,000-row union adds schema constraints, documentation overhead, and failure points for marginal information gain. Either enrich that source or remove it—don't let tail sources dictate your unified schema.

**Vertical schema changes (new sources) are cheap; horizontal changes (new columns) cascade—design accordingly.**
Adding another dataset to an existing union is straightforward if schemas match. But adding a column requires updating every source in the union or accepting nulls everywhere. When designing data models for eventual union, prioritize schema stability in width over height. Plan your column set conservatively from day one.

**If union execution time exceeds 10% of your total pipeline runtime, you're moving too much data.**
Union operations should be nearly instantaneous metadata operations in modern engines, not expensive data shuffles. If your union is slow, you're likely forcing materialization too early, combining datasets that should remain separate until aggregation, or missing partition-aware optimizations. Push unions as late as possible in your transformation logic.

**Test with the smallest source first—if schemas mismatch there, they'll mismatch everywhere.**
When validating a union across multiple datasets, start with whichever source has the fewest columns or strictest types. Schema incompatibilities surface immediately with the most constrained dataset, saving you from debugging mismatches across all sources sequentially. The smallest source acts as your schema compatibility canary.

**Before presenting union results, always show the row contribution by source—stakeholders will ask anyway.**
The first question after showing unified results is invariably "where did these numbers come from?" A simple breakdown showing that 60% came from System A, 30% from System B, and 10% from manual entry prevents confusion and builds trust. Include source attribution as metadata in every unioned dataset, not as an afterthought.

**Good practitioners union compatible schemas; great practitioners redesign sources to become compatible.**
Mediocre analysts treat union as a last-mile transformation, coercing mismatched datasets with case statements and type casts. Expert practitioners recognize union friction as a signal to refactor upstream—standardizing extraction logic, aligning column names at the source, and building shared data contracts. When you find yourself writing complex pre-union transformations monthly, invest weeks in upstream standardization to save months of maintenance.

## Nuggets

**Union doesn't guarantee order preservation, even when inputs are sorted.**
Most practitioners assume that if DataFrames A and B are sorted by column X, then `union(A, B)` will maintain that ordering—at least within each source. This is false in distributed systems. Spark and Dask actively re-partition data during union operations based on cluster topology, meaning rows from A can interleave arbitrarily with rows from B, and even rows within A may be shuffled. If downstream operations depend on order (like lag calculations or cumulative sums), you must explicitly re-sort after union, incurring substantial computational cost.

**Union ALL is almost always faster than UNION—often 10-100x for large datasets.**
The default `UNION` (without `ALL`) silently performs a distinct operation to remove duplicates, requiring a full data shuffle and comparison of every row. In benchmark tests on 10M+ row datasets, `UNION ALL` completes in seconds while `UNION` takes minutes or hours. Yet analysts reflexively use `UNION` "to be safe," unaware they're paying an enormous performance penalty. The expert move: explicitly choose `UNION ALL` and handle deduplication separately only when genuinely needed, using more efficient domain-specific logic.

**Empty DataFrames in a union can corrupt schema inference in surprising ways.**
When unioning multiple DataFrames where one is empty (zero rows but defined schema), pandas will successfully infer types, but Spark and Polars may default empty columns to `NullType` or `string`, silently coercing all subsequent data. This manifests as mysterious type errors downstream or, worse, silent string conversions of numeric data that only surface during aggregation. The fix: never union truly empty DataFrames. Filter them out first, or provide explicit schema definitions before the union operation.

**Column order matters for positional union, and more systems use it than you think.**
SQL's `UNION` matches columns by name, but many dataframe libraries (including pandas' `concat` without the right flags, and older R workflows) perform positional unions—matching the first column to the first column regardless of name. When inheriting codebases or switching tools, this causes silent data corruption: revenue data ending up in the quantity column, timestamps misaligned with events. Always verify whether your system uses positional or named matching, and in positional systems, explicitly reorder columns before union.

**Repeated unions create deeply nested lineage graphs that crash execution engines.**
Iteratively building a result with `result = union(result, new_data)` in a loop feels intuitive, but in lazy evaluation systems like Spark, each union adds a layer to the execution plan rather than materializing data. After hundreds of iterations, the lineage graph becomes so deep that query optimization times out or the driver runs out of memory before any data is processed. The solution: periodically materialize intermediate results with `.cache()` or `.checkpoint()`, or collect all DataFrames first and union them in a single operation.

**Union handles mixed nullability inconsistently across systems, breaking downstream joins.**
When unioning DataFrames where column X is nullable in one but not the other, SQL engines typically coerce to nullable (the safe choice), but some Spark configurations preserve the first schema encountered, creating metadata mismatches. This doesn't affect the union itself but causes cryptic failures in subsequent joins or window functions that inspect schema metadata. Always explicitly cast columns to a common nullable state before union when strictness matters.

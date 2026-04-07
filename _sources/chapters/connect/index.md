# Part I · Connect

**Getting data in and out of the Heuristix platform.**

The Connect stage is where every workflow begins. Before any analysis, transformation, or modelling can take place, data must be loaded into the system. The Connect nodes handle this — reading from files, databases, APIs, and streams, and writing results back out when the workflow is complete.

## Chapters in This Part

| Node | Description |
|---|---|
| [Import Data](import-data) | Load CSV, Excel, Parquet, JSON, and database tables into a workflow |
| [Export Data](export-data) | Write results to files, databases, or cloud storage |

## Key Concepts

**Data formats** — Heuristix supports tabular data (CSV, Excel, Parquet, database tables), semi-structured data (JSON, XML), and binary formats. Understanding the strengths and limitations of each format is essential for building efficient pipelines.

**Schema inference** — When loading data, Heuristix automatically infers column types. Understanding how type inference works — and when to override it — is covered in each node's chapter.

**Data volume** — The Connect nodes are designed to handle everything from small files (thousands of rows) to large-scale datasets (millions of rows with appropriate backend configuration). Performance considerations are discussed in each chapter.

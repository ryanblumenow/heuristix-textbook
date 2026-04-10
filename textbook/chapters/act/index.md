# Part VIII · Act

**Scheduling, alerting, and reporting — closing the loop from insight to action.**

Analysis without action is just expensive research. The Act stage is where workflows move from interactive exploration to automated, production systems: scheduled pipelines that run on a cadence, alerts that fire when metrics breach thresholds, and reports that deliver findings to stakeholders.

This part covers 3 nodes that operationalise the output of the entire Heuristix workflow.

## Chapters in This Part

| Node | Description |
|---|---|
| [Schedule](schedule) | Run a workflow automatically on a time-based schedule |
| [Alert](alert) | Send notifications when conditions are met |
| [Report](report) | Generate and distribute formatted reports |

## Operationalisation in Data Science

The "last mile" of data science — getting models and analyses into production where they create ongoing value — is consistently the hardest part of the process. Key challenges include:

**Drift** — models degrade as the real world changes. Scheduled pipelines with drift detection (Detect Drift node in Understand) keep models fresh.

**Reliability** — production pipelines must handle data quality issues, missing inputs, and infrastructure failures gracefully.

**Governance** — automated outputs need audit trails, version control, and appropriate access controls.

**Feedback loops** — the best production systems capture the outcomes of their decisions and feed them back into model retraining.

Each Act node is designed with these production realities in mind.

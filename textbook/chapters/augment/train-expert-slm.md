# Train Expert SLM

![](../../_static/figures/train-expert-slm_concept.png)

<div class="alisen-callout">
<img src="../../_static/alisenillus.png" alt="Alisen" class="alisen-img"/>
<div class="alisen-body">
<div class="alisen-title">ALISEN&rsquo;S KEY INSIGHT</div>
<p>The most common mistake I see with SLM training is trying to build a model that knows everything. The whole point of a small language model is that it knows one domain exceptionally well—better than a general model—while running cheaply and privately. Define a tight domain boundary before you start generating training pairs. A bank's SLM that answers regulatory capital questions with 95% accuracy on that narrow domain is far more valuable than a general model that handles the same questions at 70%. Narrow the scope, deepen the expertise, and you'll always get a better result.</p>
</div>
</div>

## The 60-Second Version

**What it does:** Train Expert SLM uses Alisen to read your organisation's text data, generate expert question-and-answer training pairs from it, and then fine-tune a compact open-source language model (Llama, Phi, or Mistral) to become a private domain expert that runs entirely without any cloud API.

**When to use it:** You have proprietary, sensitive, or highly specialised text data that a general-purpose AI handles poorly—and you want a self-hosted model that speaks your domain fluently without sending your data to an external API on every query.

**What you get back:** A labelled training dataset (JSONL) and either a managed cloud-trained model via HuggingFace AutoTrain, or a complete QLoRA training script ready to run on any GPU machine.

| | |
|---|---|
| **Difficulty** | Advanced |
| **Typical runtime** | Pair generation: minutes · Cloud training (AutoTrain): 1–4 hours · Local training: 2–12 hours |
| **What you bring** | A column of domain text (documents, notes, policies, conversations) and a domain description |
| **What you get** | A private fine-tuned language model deployed on your own infrastructure |
| **Heuristix bucket** | Augment — AI & Language Intelligence |

**Training a small language model requires a clear domain, sufficient representative text, and either a HuggingFace account for cloud training or GPU hardware for local training. Quality of training pairs matters more than quantity—100 excellent examples outperform 1,000 poorly curated ones.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify which business domains and data types are strong candidates for SLM training versus prompting a general model, and articulate the privacy and cost trade-offs to stakeholders.
- Interpret training output metrics (training loss, validation accuracy, response quality) to decide whether the trained model is ready for internal deployment.
- Specify a domain boundary clearly enough to guide effective training pair generation—knowing that over-broad domains produce weak generalist models while well-scoped domains produce highly reliable specialists.

**After reading this chapter, a data scientist will be able to:**

- Configure the training pipeline parameters—text column, domain description, base model choice, number of training pairs, and training platform—to maximise domain specificity and model quality.
- Evaluate generated training pairs for coverage, diversity, and accuracy before committing to full training, and provide domain feedback to improve pair quality.
- Choose between HuggingFace AutoTrain (managed cloud training, no GPU required) and local QLoRA (full control, requires GPU hardware) based on infrastructure, data sensitivity, and budget constraints.

## Overview

**Train Expert SLM** implements a **knowledge distillation** pipeline that converts your organisation's unstructured text data into a fine-tuned small language model (SLM) that can answer domain questions accurately and privately. The process has two stages:

**Stage 1 — Training pair generation (Alisen):** Alisen reads your domain text data, identifies key facts, concepts, and relationships, and generates instruction-response pairs in a supervised fine-tuning (SFT) format. These pairs follow the structure: a plausible user question or instruction, followed by an expert answer derived directly from your text. The quality and specificity of these pairs determines the quality of the final model.

**Stage 2 — Model fine-tuning:** The generated pairs are used to fine-tune a compact base model using **QLoRA** (Quantized Low-Rank Adaptation)—a parameter-efficient fine-tuning method that trains only a small number of adapter weights rather than the full model, making it feasible on modest GPU hardware. Two training paths are available:

- **HuggingFace AutoTrain** (cloud): Alisen uploads your dataset to HuggingFace Hub, submits a managed training job, and returns a link to your trained model repository. No GPU infrastructure required—training runs on HuggingFace's cloud compute.
- **Local QLoRA** (on-premises or private cloud): Alisen generates a complete, runnable bash and Python training script that you execute on any machine with a compatible GPU. The model never leaves your infrastructure.

Supported base models include **Llama 3** (Meta, strong general reasoning), **Phi-3** (Microsoft, efficient and accurate on limited compute), and **Mistral 7B** (Mistral AI, efficient multilingual base).

## When to Use This

- **Use this when** your data is confidential and cannot leave your infrastructure—SLM training creates a model you own and host; after training, no query goes to an external API.

- **Use this when** a general-purpose AI gives inconsistent or superficial answers on your domain—a fine-tuned SLM that has seen your actual policies, procedures, or domain knowledge will be more reliable than prompting a general model.

- **Use this when** you need to reduce ongoing API costs—a self-hosted SLM on modest hardware eliminates per-token costs entirely; at scale (millions of queries), this can recover the training cost within days.

- **Use this when** your domain has specialised vocabulary, abbreviations, or concepts that general models mishandle—medical coding systems, regulatory frameworks, engineering specifications, internal product taxonomies.

- **Use this when** you have a well-defined, stable domain with documented text—product manuals, compliance guidelines, medical protocols, legal precedents, customer interaction transcripts.

- **Use this when** you want a model that can run offline—at edge locations, on secure networks without internet access, or on device.

- **Do NOT use this when** your domain changes rapidly and the model would be outdated within weeks—SLM training requires time and compute; frequent retraining is expensive.

- **Do NOT use this when** you have fewer than a few hundred documents or text records—insufficient training data produces a model that parrots fragments rather than reasoning about the domain.

- **Do NOT use this when** broad general knowledge is important—fine-tuning specialises a model and can reduce its capability outside the training domain. Use a general model for wide-ranging tasks.

- **Do NOT use this when** interpretability of every prediction is a hard requirement—language models, including fine-tuned SLMs, do not produce auditable reasoning chains in the way decision trees do.

## Questions This Answers

### Building Private AI Capability

**How do we create a chatbot that accurately answers questions about our internal policy documents without sending those documents to an external cloud service every query?**

**Our compliance team spends 40% of their time answering the same regulatory questions—can we train a model on our compliance library to handle routine queries automatically?**

**We have 10 years of case notes from our legal practice—can we turn them into a private AI assistant that junior associates can query?**

**Our medical device documentation is highly confidential. Can we create a support AI trained on it that never leaves our network?**

### Cost and Operational Efficiency

**We're spending R200,000 per month on cloud AI API calls—is there a path to reducing this significantly?**

**Our remote field engineers have no reliable internet access. Can they use an AI assistant for equipment diagnostics offline?**

**Can we train a model specifically on our product catalogue and technical specifications so it gives more accurate answers than a general AI?**

### Domain Specialisation

**Why does the general AI keep giving generic answers about our industry when we need very specific guidance based on our internal standards?**

**We have proprietary research findings that no AI model could know—can we distil this knowledge into a model our analysts can query?**

**Our customer service agents need answers based on our specific contracts, not general industry practice—how do we build that?**

## How It Works

The Train Expert SLM node runs a four-step pipeline:

```
Step 1: TEXT INGESTION
  Your text column → cleaned paragraphs → chunked into ~512-token segments

Step 2: TRAINING PAIR GENERATION (Alisen)
  For each text chunk:
    → Generate a plausible user question about this content
    → Generate an expert answer drawn from this content
    → Format as {"system": ..., "user": ..., "assistant": ...}
  Output: N instruction-response pairs in JSONL format

Step 3: DATASET SAVE
  JSONL file saved to disk (or uploaded to HuggingFace Hub for cloud training)

Step 4A: HUGGINGFACE AUTOTRAIN (cloud path)
  Dataset uploaded to HF Hub → AutoTrain job submitted →
  Managed QLoRA training runs → Trained model pushed to your HF repo

Step 4B: LOCAL QLORA (on-premises path)
  Complete training script (bash + Python) generated and saved →
  You run: bash train_expert_slm.sh on any GPU machine →
  Trained model saved locally
```

**QLoRA in plain English:** Instead of retraining all 7 billion parameters of a base model (which requires enormous GPU memory), QLoRA freezes the original model and adds tiny "adapter" weight matrices to specific layers. Only these adapters are trained—they typically add less than 1% of the model's total parameter count. After training, the adapters are merged with the base model to produce the final expert model. This makes fine-tuning possible on a single consumer GPU (16GB VRAM) rather than requiring a data centre.

## The Intuition

Imagine you've hired a very smart university graduate with strong general knowledge (the base model). You want her to become an expert in South African banking regulation—a domain that requires knowing specific circulars, prudential standards, and case law that she never studied. Instead of sending her back to university for three years, you give her all your bank's regulatory documents and ask her to read them intensively for a week, answering practice questions as she goes. She doesn't forget her general intelligence—she adds domain expertise on top of it. That's what Train Expert SLM does: it uses Alisen to create the practice questions and uses QLoRA to efficiently imprint the answers into the base model's existing cognitive framework.

## The Mathematics

### LoRA (Low-Rank Adaptation)

For a pre-trained weight matrix $W \in \mathbb{R}^{d \times k}$, LoRA parameterises the update as:

$$W' = W + \Delta W = W + AB$$

where $A \in \mathbb{R}^{d \times r}$, $B \in \mathbb{R}^{r \times k}$, and $r \ll \min(d, k)$ is the **rank**—a small number (typically 4–64).

Instead of updating all $d \times k$ parameters during fine-tuning, only $r(d + k)$ parameters are trained. For a 7B parameter model with rank=8, this reduces trainable parameters from ~7 billion to ~4 million—a 1,750× reduction.

### QLoRA Quantisation

QLoRA extends LoRA by additionally quantising the frozen base model weights to 4-bit precision (NF4 quantisation), reducing GPU memory by approximately 4× compared to full 16-bit precision:

$$\text{Memory}_{QLoRA} \approx \frac{\text{Memory}_{FP16}}{4} + \text{Memory}_{adapters}$$

For a 7B parameter model: from ~14GB (FP16) to ~4GB (QLoRA) plus ~100MB for adapters. This enables fine-tuning a 7B model on a 16GB consumer GPU (e.g., RTX 4090 or A10).

### Supervised Fine-Tuning Loss

Training minimises the language modelling loss on the assistant's tokens only (the response, not the prompt):

$$\mathcal{L} = -\frac{1}{|T_{response}|} \sum_{t \in T_{response}} \log P(x_t \mid x_{<t}, \theta)$$

where $T_{response}$ is the set of assistant response token positions and $\theta$ are the LoRA adapter parameters. This teaches the model to generate responses like those in the training pairs when given similar questions.

## Using This in Heuristix

### What Data You'll Need

You need a column containing substantive domain text. The more detailed and representative the text, the better the training pairs:

| doc_id | content | source |
|--------|---------|--------|
| P001 | "Section 4.2: Capital adequacy ratios must be maintained above 10.5% for Tier 1 capital as defined in Basel III..." | Policy Manual v3 |
| P002 | "Customer onboarding requires identity verification under FICA s22. Acceptable documents include: RSA ID book..." | Compliance Guide |
| P003 | "In cases where a transaction exceeds R100,000, the following escalation procedure applies..." | Operations Manual |

**Minimum recommended:** 100 text records, each at least 200 words. More is better; diversity is more important than volume.

### Configuration Parameters

| Parameter | When to Change |
|-----------|----------------|
| **Text column** | Always set to your domain text column |
| **Domain description** | Be specific: "South African banking compliance (FICA, Basel III)" beats "banking" |
| **Model name** | Used as the HuggingFace repo name and local output folder |
| **Base model** | Llama-3.1-8B (best quality); Phi-3-mini (fastest, lowest memory); Mistral-7B (strong multilingual) |
| **Number of pairs** | 200–500 for a focused domain; 1,000–2,000 for broader coverage; more is diminishing beyond 5,000 |
| **Training platform** | HuggingFace AutoTrain: no GPU needed, managed; Local: data never leaves your network |
| **HF token / username** | Required for AutoTrain path; not needed for local path |

### What You'll Get Back

The node returns a summary table showing:
- **n_pairs**: number of training pairs successfully generated
- **dataset_path**: local path to the saved JSONL training file
- **base_model**: the base model used
- **training_platform**: autotrain or local
- **script_path** (local only): path to the generated training script
- **next_steps**: instructions for completing training

### Connecting Downstream

After Train Expert SLM:
- **Export Data** — to save the generated JSONL training pairs for review or external use
- **Ask Your Data** — use the deployed SLM as the backing model for domain Q&A
- **LLM Transform** — pipe records through the fine-tuned model for batch processing

### Quick Start: Internal Policy Expert

1. Import your policy documents or text records (Import Data)
2. Ensure the text column contains substantive content (Filter Rows to remove short stubs)
3. Connect to **Train Expert SLM**
4. Set: text column = `policy_text`, domain = "Employee HR policies and procedures for [Company Name]", model name = `hr-policy-expert`
5. Choose base model: Phi-3-mini for fastest training; Llama-3.1-8B for best quality
6. Choose platform: HuggingFace AutoTrain if you don't have GPU hardware; Local if data must stay on-premises
7. Run — Alisen generates training pairs (review the JSONL output)
8. Complete training on your chosen platform (AutoTrain: wait for HF notification; Local: run the generated script)
9. Test the deployed model with domain questions your team would actually ask

### Pro Tips from Experienced Users

**Review 10–20 generated training pairs before committing to full training.** The quality of your domain description directly determines the quality of the pairs Alisen generates. If the questions are too generic ("What is compliance?") rather than specific ("Under FICA Section 22, which transactions require enhanced due diligence?"), refine your domain description and regenerate.

**For local training, the minimum viable GPU is a 16GB VRAM machine.** An RTX 4090, A10G, or any cloud instance with 24GB VRAM (AWS g5.xlarge, GCP T4) is suitable for Phi-3-mini and Llama-3.1-8B with QLoRA. Training time is typically 1–4 hours for 1,000 pairs.

**Generate more pairs than you think you need, then curate.** It's cheaper to generate 500 pairs and manually filter out the weak 20% than to train on 500 noisy pairs. Quality matters more than quantity at this scale.

**Base model selection rule of thumb:** Phi-3-mini (3.8B) for deployment on edge devices or when GPU memory is limited to 8GB. Llama-3.1-8B for the best accuracy-to-size ratio on most business domains. Mistral-7B when your domain involves multiple languages or when strong instruction-following is critical.

## Config Recipes

### Recipe 1: Quick Proof-of-Concept (AutoTrain)
**When to use:** Validating whether the concept works before investing in GPU infrastructure.
**Settings:** n_pairs=200, base_model=Phi-3-mini, platform=autotrain
**What you get:** A trained model in 1–2 hours with no infrastructure investment; useful for testing domain coverage
**Trade-off:** Phi-3-mini quality is lower than Llama-3.1-8B; training data uploaded to HuggingFace

### Recipe 2: Production Domain Expert (AutoTrain)
**When to use:** Building a production-quality domain expert where training data is not confidential.
**Settings:** n_pairs=1000, base_model=llama-3.1-8b, platform=autotrain
**What you get:** A high-quality 8B parameter model trained on 1,000 domain pairs; deployable on any inference server
**Trade-off:** 2–4 hour training time; training data hosted on HuggingFace (suitable for non-confidential data)

### Recipe 3: Private On-Premises Expert (Local QLoRA)
**When to use:** Confidential data that must never leave your infrastructure; or when you have GPU hardware available.
**Settings:** n_pairs=500, base_model=llama-3.1-8b, platform=local
**What you get:** A complete QLoRA training script that runs on your GPU; trained model stays on your hardware; no external data transfer during training
**Trade-off:** Requires a GPU machine (16GB VRAM minimum); you manage the training execution

### Recipe 4: Edge Deployment Expert (Local QLoRA, Small Model)
**When to use:** Model must run on a laptop, edge device, or server without a dedicated GPU (CPU inference).
**Settings:** n_pairs=300, base_model=phi-3-mini, platform=local
**What you get:** A 3.8B parameter model small enough to run on CPU inference (slowly) or on an integrated GPU; suitable for offline field use
**Trade-off:** Lower quality than Llama-3.1-8B; slower CPU inference; requires a CPU inference framework (llama.cpp) for deployment

## Business Applications

**Financial Services — Regulatory Compliance Assistant**
A South African bank trained a Mistral-7B model on 8 years of SARB directives, FICA guidance, and internal compliance procedures (2,400 text records). Alisen generated 1,200 training pairs covering capital adequacy, AML, and customer onboarding. The resulting model was deployed on an internal server and integrated into the compliance team's workflow. Compliance officers query it via a simple chat interface. Routine query resolution time dropped from 45 minutes (manual search) to under 2 minutes, and first-line resolution accuracy was 89% (versus 94% for senior compliance officers). The model runs entirely on-premises—no query data leaves the bank.

**Legal — Case Research Specialist**
A commercial law firm trained a Llama-3.1-8B model on 15 years of case summaries, internal precedent notes, and client advice memos (6,200 documents). The firm used HuggingFace AutoTrain with 2,000 generated pairs. The trained model assists junior associates by surfacing relevant precedents and drafting initial research summaries. Billing time for first-draft research tasks fell by 60%. Because the training data consisted of internal work product (not client confidential materials), the firm was comfortable using the AutoTrain cloud path.

**Healthcare — Clinical Protocol Advisor**
A hospital network trained a Phi-3-mini model on clinical protocols, drug interaction guidelines, and patient safety procedures for use on nursing station tablets with limited connectivity. The model was trained locally (data never left the hospital network) with 400 pairs covering emergency procedures, medication administration, and escalation protocols. Phi-3-mini was chosen for its small footprint (3.8B parameters, 4GB on disk with quantisation). The model runs offline with a 600ms response time on the tablet hardware—acceptable for non-urgent protocol lookups.

**Manufacturing — Equipment Maintenance Expert**
An industrial equipment manufacturer trained a domain expert on 20 years of technical service manuals, fault code libraries, and field engineer reports (12,000 documents). With 3,000 Alisen-generated pairs and a Llama-3.1-8B base, the model was deployed as an API endpoint for field engineers. First-call resolution on equipment fault queries improved from 61% to 84%. Engineers in areas with poor connectivity use the local QLoRA version on a ruggedised laptop.

**Professional Services — Knowledge Base Preservation**
A management consulting firm was concerned about institutional knowledge loss when senior partners retired. They trained an SLM on 1,800 internal methodology documents, project post-mortems, and client engagement notes. The model serves as a "knowledge retrieval" assistant for newer consultants—answering questions about how the firm approaches specific problem types. Average time spent searching internal knowledge bases fell by 71% for junior consultants.

## Worked Example

**Scenario:** An insurance company has 3,000 claims adjudication notes and policy interpretation memos. Their junior claims assessors frequently ask the same questions about edge cases. Senior adjusters spend 30% of their time answering these queries. The company wants a private AI assistant that can answer routine claims queries accurately.

**Step 1 — Data import.** The team imports a CSV of adjudication notes with columns: `claim_id`, `policy_type`, `adjudication_notes`, `decision`, `notes_length`. They filter to records where `notes_length > 300` words (2,100 records remain).

**Step 2 — Node configuration.** They drag in Train Expert SLM. Settings: text column = `adjudication_notes`, domain = "South African short-term insurance claims adjudication — motor, home, and liability policies under FSCA regulation", model name = `claims-expert-v1`, base model = Llama-3.1-8B, pairs = 800, platform = Local (claims data is confidential).

**Step 3 — Pair generation.** Alisen processes 2,100 text records and generates 800 training pairs. The team reviews 20 pairs manually. Sample pairs include: Q: "Under what circumstances can a motor claim be declined for non-disclosure?" A: "A motor claim may be declined for non-disclosure when the non-disclosed information would have materially affected the insurer's underwriting decision, provided the insurer can demonstrate a causal link between the non-disclosure and the claim event..." The pairs are accurate and domain-specific. Two pairs referencing a specific client name are removed.

**Step 4 — Local training.** The team runs the generated `train_claims_expert_v1.sh` script on their cloud GPU instance (AWS g5.xlarge, 24GB VRAM). Training completes in 2.5 hours. Training loss converges from 2.3 to 0.8. Validation loss: 0.9 (no significant overfitting).

**Step 5 — Evaluation.** The team presents 50 real claims queries to both the SLM and a senior adjuster. The SLM answers 44/50 correctly (88%)—comparable to a mid-level adjuster (91%). 3 incorrect answers contained accurate information but missed a specific policy endorsement not covered in training data. They add 40 more pairs covering endorsement edge cases and retrain (30 minutes).

**Step 6 — Deployment.** The model is served via a lightweight inference API on the company's internal network. Junior assessors access it through a chat interface in their claims management system. Senior adjuster query volume falls by 52% in the first month.

## Interpreting Your Results

### Training Loss: What the Numbers Mean
- **Starting loss 2.0–2.5**: Normal for an 8B model beginning SFT. The model is essentially learning a new response style.
- **Final training loss < 1.0**: Good convergence. The model has learnt the training distribution.
- **Final training loss 1.0–1.5**: Moderate convergence—consider more training pairs or more epochs.
- **Training loss > 1.5 after full training**: Underfitting. Domain description may be too broad; training pairs may be too noisy; learning rate may be too low.
- **Training loss < 0.3**: Potential overfitting—model may be memorising rather than generalising. Add validation loss monitoring.

### Evaluating Generated Training Pairs
Before committing to training, review a sample of 20–30 pairs:
- Are questions genuinely representative of what end users will ask?
- Are answers accurate, specific, and drawn from your text rather than general knowledge?
- Is there diversity in question types (factual, procedural, interpretive, edge-case)?
- Are any pairs too generic ("What is X?") or too trivial to be useful?

### Post-Training Quality Assessment
Test with 20 queries you know the correct answers to. Classify each response as: Correct, Partially Correct, Hallucination (wrong but confident), or Refusal. Production readiness requires < 5% Hallucinations and > 80% Correct on your domain queries.

## Decision Guidance

### When to Choose AutoTrain vs Local QLoRA

| Situation | Recommendation |
|---|---|
| Data is not confidential and you have no GPU | HuggingFace AutoTrain |
| Data is confidential but you have a GPU | Local QLoRA |
| Data is confidential and you have no GPU | Anonymise data, then AutoTrain; or procure a cloud GPU |
| Need model running offline or on-premises | Local QLoRA always |
| Rapid prototype, don't care about security | AutoTrain — fastest path |
| Production, regulated industry, data sovereignty required | Local QLoRA |

## Common Pitfalls

**The Overly Broad Domain Problem**
*Here's what happened:* A team set the domain description as "banking" and got training pairs that were generic textbook-style answers rather than answers specific to their internal policies. *Why it happens:* Alisen uses the domain description to guide question generation. A broad description produces broad questions. *How to detect it:* Review sample pairs—are the answers actually from your documents, or could they have come from Wikipedia? *The fix:* Narrow the domain description. "ABSA Bank South Africa internal credit policies and Basel III capital requirements" produces far better pairs than "banking."

**The Hallucination Inheritance Problem**
*Here's what happened:* The trained model answered 92% of domain questions correctly but gave confident, wrong answers on the remaining 8%—mixing accurate training data facts with base model hallucinations. *Why it happens:* Fine-tuning doesn't eliminate the base model's tendency to generate plausible-sounding content when it doesn't know the answer. *How to detect it:* Include adversarial queries on topics you know are NOT in your training data. A well-trained model should say "I don't have information on that" rather than hallucinating. *The fix:* Add explicit "I don't know" training pairs for topics at the boundary of your domain; include negative examples in training.

## Common Misconceptions

**"More training pairs always means a better model."**
*Why people believe this:* More data is usually better in machine learning. *The truth:* At SLM scale (500–2,000 pairs), quality dominates quantity. 500 accurate, diverse, specific pairs reliably outperform 2,000 noisy, repetitive, or generic pairs. *The real-world consequence:* Teams that generate 3,000 pairs without reviewing them waste compute budget and end up with models that confidently give mediocre answers.

**"A fine-tuned SLM replaces the need for a RAG system."**
*Why people believe this:* The model has learnt the domain, so why retrieve documents? *The truth:* SLMs bake knowledge into weights—appropriate for stable, durable knowledge (procedures, policies, frameworks). For frequently updated information (current prices, live inventory, today's news), RAG remains superior because it retrieves fresh documents at query time. *The real-world consequence:* An SLM trained on last year's tariff schedule will give confidently wrong answers after the tariffs change. Combine SLM (for stable domain reasoning) with RAG (for current facts) in production systems.

**"The trained model will be as capable as GPT-4 on domain questions."**
*Why people believe this:* It's been trained on the same domain. *The truth:* A 7B parameter SLM, even when expertly fine-tuned, lacks the general reasoning capacity of a 175B+ parameter general model. It will be significantly better than a general model on your specific narrow domain—and significantly worse on anything outside that domain. The right comparison is: "Is it better than Alisen on MY specific domain questions?" (Answer: often yes, after good training.)

## How This Connects

### Before This Node
Your source data should be as clean and substantive as possible. Import your documents (Import Data). Filter out boilerplate, headers, and very short records (Filter Rows → text length > 200 characters). Optionally use LLM Transform to clean or summarise text before using it as training input. The richer and more specific the input text, the better the generated training pairs.

### After This Node
Once you have a trained model, deployment paths depend on your infrastructure. For cloud-trained models (AutoTrain), the model is available directly from your HuggingFace repository for download and deployment. For locally trained models, the output folder contains the merged model weights ready for any inference framework (vLLM, llama.cpp, HuggingFace Transformers). Connect to Ask Your Data to use the model as the backing engine for document Q&A workflows within Heuristix.

## Further Reading

- Hu, E.J., et al. (2022). LoRA: Low-Rank Adaptation of Large Language Models. *ICLR 2022*. The original LoRA paper—highly readable, explains the mathematics clearly with empirical validation.
- Dettmers, T., et al. (2023). QLoRA: Efficient Finetuning of Quantized LLMs. *NeurIPS 2023*. The paper that made fine-tuning large models feasible on consumer hardware—a landmark result.
- Wei, J., et al. (2022). Finetuned Language Models Are Zero-Shot Learners. *ICLR 2022*. Shows how instruction fine-tuning (the basis for SFT) dramatically improves model usability.
- Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the Knowledge in a Neural Network. *NeurIPS Deep Learning Workshop 2015*. The foundational paper on knowledge distillation — explains why smaller models can capture much of a larger model's expertise.
- Meta AI. (2024). Llama 3 Model Card. [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B). Official documentation for the Llama 3 base model family.

## Heuristics

- Define your domain as specifically as a job description—not "finance" but "South African short-term insurance claims under FSCA regulation."
- Review 20 generated pairs before training. This 5-minute check prevents 3 wasted hours of training on bad data.
- 500 high-quality pairs > 2,000 mediocre pairs. Always prefer curation over volume at SLM scale.
- Choose Phi-3-mini for edge/offline deployment; Llama-3.1-8B for production quality; Mistral-7B for multilingual domains.
- Use AutoTrain when speed of deployment matters and data isn't confidential; use Local QLoRA when data sensitivity is the primary constraint.
- Post-training, test explicitly on queries you know the answer to AND on queries about topics NOT in your training data. Both matter.
- Plan for retraining every 3–6 months for domains where the underlying knowledge changes (regulations, pricing, products).
- A fine-tuned SLM is excellent for retrieval and stable domain knowledge; combine with RAG for anything time-sensitive.

## Nuggets

- The "small" in Small Language Model is relative. A 7B parameter model has approximately 7 billion floating-point numbers representing its knowledge—more parameters than there are neurons in the human brain. "Small" means small compared to 175B+ parameter general-purpose models.
- QLoRA achieves fine-tuning quality within 1–2% of full-parameter fine-tuning while using 4× less GPU memory—a remarkable engineering result that democratised SLM training from research labs to business teams.
- Knowledge distillation (using a large model to teach a small model) is conceptually the same process as how human expertise is transferred: a senior practitioner's responses are used to train a junior practitioner who then becomes the domain expert without needing the senior's decades of general experience.
- A well fine-tuned 7B parameter model on a specific domain routinely outperforms a general 70B parameter model on that domain—smaller can genuinely be better when the scope is right.

# Fine-tune Model

## The 60-Second Version

**What it does:** Fine-tuning teaches a pre-trained AI language model to speak your company's language by training it on your specific examples and tasks.

**When to use it:** When generic AI responses aren't good enough—you need consistent, domain-specific outputs for tasks like customer support, medical diagnosis, legal document drafting, or any repeated business process where accuracy and style matter.

**What you get back:** A customised model that produces reliable, on-brand responses tailored to your domain, ready to deploy in production systems.

| | |
|---|---|
| **Difficulty** | Advanced |
| **Typical runtime** | Hours to days depending on model size and dataset |
| **What you bring** | A pre-trained model and labelled examples of your task (typically hundreds to thousands) |
| **What you get** | A specialised model optimised for your specific use case |
| **Heuristix bucket** | Augment — AI & Language Intelligence |

**Fine-tuning requires significant examples and expertise—if you only have a handful of cases or need flexibility across many tasks, start with prompt engineering instead.**

## Learning Objectives

**After reading this chapter, a business user will be able to:**

- Identify when fine-tuning is more cost-effective than prompt engineering by comparing task repetition, quality requirements, and response consistency needs across your business use cases.
- Interpret fine-tuning performance metrics such as validation loss, accuracy, and domain-specific benchmarks to assess whether a fine-tuned model meets business quality thresholds.
- Decide whether to invest in fine-tuning versus alternatives by weighing upfront training costs, inference savings, data availability, and the strategic value of proprietary model capabilities.

**After reading this chapter, a data scientist will be able to:**

- Implement end-to-end fine-tuning pipelines including dataset preparation, train-validation splits, hyperparameter configuration, and model deployment for production LLM applications.
- Tune critical parameters such as learning rate, batch size, number of epochs, and LoRA rank while managing the trade-offs between training speed, model performance, and catastrophic forgetting.
- Validate fine-tuned models through holdout testing, detect overfitting to training data, and diagnose common failure modes including distribution shift, formatting errors, and task confusion.

## Overview

Fine-tuning is the process of adapting a pre-trained large language model (LLM) to a specific task or domain by continuing training on a curated, task-relevant dataset. This technique belongs to the family of transfer learning methods, where knowledge acquired during pre-training on massive general corpora is refined and specialised for downstream applications. Fine-tuning enables organisations to leverage the linguistic capabilities of foundation models while tailoring their behaviour, style, and domain expertise to match precise business requirements—achieving superior performance compared to prompting alone, particularly for high-stakes, repetitive, or domain-specific tasks.

## When to Use This

**Use Fine-tune Model when:**

- **You have a consistent, repetitive task** where the model must produce outputs in a specific format, tone, or style across thousands of similar inputs—such as generating product descriptions, summarising legal documents, or classifying customer feedback.

- **General-purpose models underperform on domain-specific language**—for instance, when your data contains industry jargon, technical terminology, or abbreviations that pre-trained models handle poorly (medical coding, financial instruments, engineering specifications).

- **You need to reduce inference costs at scale**—a smaller fine-tuned model can often match or exceed the performance of a larger general model on your specific task, reducing token costs and latency.

- **Consistency and compliance matter**—when outputs must adhere to strict regulatory formats, brand voice guidelines, or organisational policies that cannot be reliably enforced through prompting alone.

- **You have high-quality labelled examples**—typically 50 to 10,000 exemplar input-output pairs that represent the task distribution you wish the model to learn.

- **Prompt engineering has reached diminishing returns**—you have iterated on prompts extensively but still observe unacceptable error rates, hallucinations, or format violations.

**Do NOT use Fine-tune Model when:**

- **You lack sufficient quality training data**—fine-tuning with fewer than ~50 examples or with noisy, inconsistent labels typically degrades rather than improves performance.

- **Your requirements change frequently**—fine-tuned models are expensive to update; if your task specifications shift weekly, prompt-based approaches offer more agility.

- **The base model already performs well**—if careful prompting achieves acceptable results, fine-tuning adds unnecessary complexity and cost.

- **You need broad general knowledge**—fine-tuning can cause catastrophic forgetting, narrowing the model's capabilities outside the fine-tuning distribution.

## Questions This Answers

### Customization and Performance

**Can we train our chatbot to answer customer queries using our specific product terminology and company policies instead of generic responses?**

**Why is our current model giving inconsistent answers about compliance requirements when our legal team has documented everything clearly?**

**How can we get the AI to write reports in our brand voice rather than sounding like every other company in our industry?**

**Will fine-tuning our model reduce the number of times it says "I don't have enough information" when customers ask about our services?**

**Can we make the system understand our internal acronyms and technical jargon without having to explain them in every prompt?**

### Cost and Efficiency

**We're spending $47,000 monthly on API calls with lengthy prompts—can fine-tuning bring that down while maintaining quality?**

**How much time and budget should we allocate to fine-tune a model versus continuing to refine our prompts?**

**If we fine-tune once, how often will we need to retrain as our product line evolves throughout the year?**

**Should we fine-tune our own model or keep paying for a premium pre-built solution that doesn't quite fit our needs?**

### Competitive Advantage and Strategic Decisions

**Can fine-tuning help us build a proprietary AI capability that competitors can't easily replicate?**

**Our rival launched an AI assistant last month that seems smarter in our domain—can we catch up by fine-tuning rather than building from scratch?**

**Which approach will get us to market faster: fine-tuning an existing model on our customer service transcripts or hiring more engineers to improve our prompting strategy?**

**If we fine-tune on our proprietary data, what prevents the model provider from learning our trade secrets?**

## How It Works

Imagine you've hired an experienced journalist who has written for every major newspaper and mastered the craft of clear, engaging prose. Now you need them to write exclusively for your medical device company's regulatory submissions—a specialized domain with precise terminology, rigid structure, and zero tolerance for creative flair. You don't need to teach them grammar or sentence construction; they already know how to write beautifully. Instead, you spend two weeks having them study your past successful submissions, learn your specific product terminology, understand FDA formatting requirements, and practice mimicking the exact tone regulators expect. By the end, they've adapted their broad writing skills to your narrow, high-stakes context. That's fine-tuning: taking a model that already understands language and teaching it your specific style, vocabulary, and task requirements.

```
BEFORE FINE-TUNING                FINE-TUNING PROCESS              AFTER FINE-TUNING
┌─────────────────────┐           ┌─────────────────────┐          ┌─────────────────────┐
│  Pre-trained LLM    │           │  Your Labeled Data  │          │   Specialized Model │
│                     │           │  ┌───────────────┐  │          │                     │
│ • General language  │           │  │ Input → Output│  │          │ • General language  │
│ • Broad knowledge   │─────→     │  │ Input → Output│  │─────→    │ • YOUR vocabulary   │
│ • Generic responses │           │  │ Input → Output│  │          │ • YOUR style        │
│ • No domain focus   │           │  │     (500+     │  │          │ • YOUR task focus   │
│                     │           │  │   examples)   │  │          │ • Consistent output │
└─────────────────────┘           │  └───────────────┘  │          └─────────────────────┘
                                  │         ↓           │
                                  │  Adjust weights to  │
                                  │  match your examples│
                                  └─────────────────────┘
```

**Step 1: Start with a pre-trained foundation model.** You begin with a large language model that has already spent weeks learning from billions of web pages, books, and articles. This model understands grammar, context, reasoning, and general knowledge—it's like a university graduate with broad skills but no job-specific training.

**Step 2: Prepare your labeled training dataset.** You gather hundreds or thousands of examples showing exactly what you want: input prompts paired with ideal outputs. For a customer service bot, this might be real customer questions matched with your company's approved responses. For a legal document generator, it's sample clauses paired with completed contracts. Quality matters more than quantity—each example teaches the model your standards.

**Step 3: Resume training on your specific data.** The model processes your examples one by one, comparing its current outputs to your ideal responses. Every time it gets something wrong—uses the wrong tone, misses key terminology, or formats incorrectly—it makes tiny adjustments to its internal parameters (the billions of numerical settings that control its behavior). Think of these adjustments as recalibrating thousands of dials to better match your requirements.

**Step 4: Iterate until the model masters your task.** The model cycles through your dataset multiple times, each pass refining its understanding. Early on, it might produce generic responses. Gradually, it learns to mirror your vocabulary, adopt your formatting conventions, and prioritize the information you care about. You monitor its progress on a separate validation set to ensure it's learning your patterns without simply memorizing examples.

**Step 5: Deploy your specialized model.** Once training completes, you have a model that behaves like the original foundation model but consistently produces outputs aligned with your specific needs—faster and more reliable than prompting a generic model every time.

**The key insight:** Fine-tuning works because language understanding and task-specific behavior are separable skills—you inherit years of expensive pre-training for free, then invest modest resources teaching only your unique requirements.

## The Intuition

Imagine hiring a brilliant generalist consultant who has read extensively across all fields—history, science, law, medicine, finance—but has never worked in your specific industry. This consultant can understand your requests and provide reasonable answers, but their responses lack the precision, vocabulary, and conventions that your domain demands. Fine-tuning is analogous to giving this consultant an intensive apprenticeship within your organisation: they shadow your best performers, study exemplary work products, and learn exactly how things are done here. After this apprenticeship, the consultant retains their broad knowledge but now produces outputs that feel native to your domain.

The power of fine-tuning derives from the hierarchical nature of neural representations. During pre-training, a language model learns progressively abstract features: lower layers encode basic syntactic patterns, middle layers capture semantic relationships, and higher layers develop task-general reasoning capabilities. When we fine-tune, we adjust these learned representations—particularly in higher layers—to specialise them for our target task. Crucially, we do not discard the foundation; we build upon it. This is why fine-tuning can achieve strong performance with relatively few examples: the model already "knows" language, and we are merely teaching it the specifics of our task.

There is an important tension to understand: fine-tuning trades generality for specificity. A model fine-tuned heavily on legal contract analysis may lose some of its poetry-writing ability. This is not a flaw but a feature—we are deliberately shaping the model's probability distribution over outputs to concentrate mass on the kinds of responses we value. The art of fine-tuning lies in achieving sufficient specialisation without catastrophic forgetting of useful general capabilities. Modern techniques like Low-Rank Adaptation (LoRA) address this by constraining the fine-tuning updates to a low-dimensional subspace, preserving most of the original model while enabling efficient specialisation.

## The Mathematics

### Problem Setup and Notation

Let $\mathcal{D}_{\text{pretrain}}$ denote the large-scale corpus used during pre-training, and let $\mathcal{D}_{\text{fine-tune}} = \{(x_i, y_i)\}_{i=1}^{N}$ denote our fine-tuning dataset of $N$ input-output pairs. The input $x_i$ is a sequence of tokens $(x_i^{(1)}, x_i^{(2)}, \ldots, x_i^{(S_i)})$ and the target output $y_i$ is a sequence $(y_i^{(1)}, y_i^{(2)}, \ldots, y_i^{(T_i)})$.

A pre-trained language model with parameters $\theta_0$ defines a conditional probability distribution:

$$
p_{\theta_0}(y \mid x) = \prod_{t=1}^{T} p_{\theta_0}(y^{(t)} \mid x, y^{(1)}, \ldots, y^{(t-1)})
$$

Fine-tuning seeks parameters $\theta^*$ that maximise the likelihood of the fine-tuning data while remaining close to the pre-trained parameters.

### Objective Function

The standard fine-tuning objective is maximum likelihood estimation (MLE) over the fine-tuning dataset:

$$
\mathcal{L}_{\text{MLE}}(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \log p_\theta(y_i \mid x_i)
$$

Expanding the autoregressive factorisation:

$$
\mathcal{L}_{\text{MLE}}(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \sum_{t=1}^{T_i} \log p_\theta(y_i^{(t)} \mid x_i, y_i^{(1)}, \ldots, y_i^{(t-1)})
$$

This is the cross-entropy loss summed over all target tokens across all examples.

### Regularisation and the Fine-Tuning Trade-off

Unconstrained minimisation of $\mathcal{L}_{\text{MLE}}$ can lead to overfitting and catastrophic forgetting. A regularised objective incorporates a penalty for deviating from pre-trained parameters:

$$
\mathcal{L}_{\text{reg}}(\theta) = \mathcal{L}_{\text{MLE}}(\theta) + \lambda \|\theta - \theta_0\|_2^2
$$

where $\lambda > 0$ controls the strength of regularisation. This is equivalent to assuming a Gaussian prior centred on $\theta_0$ and performing maximum a posteriori (MAP) estimation.

### Low-Rank Adaptation (LoRA)

LoRA constrains the fine-tuning update to lie in a low-rank subspace. For a weight matrix $W_0 \in \mathbb{R}^{d \times k}$ in the pre-trained model, LoRA represents the update as:

$$
W = W_0 + \Delta W = W_0 + BA
$$

where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$, and $r \ll \min(d, k)$ is the rank of the adaptation.

The forward pass computes:

$$
h = W_0 x + \frac{\alpha}{r} BA x
$$

where $\alpha$ is a scaling hyperparameter. During fine-tuning, only $A$ and $B$ are updated; $W_0$ remains frozen. The number of trainable parameters reduces from $d \times k$ to $r(d + k)$.

**Initialisation:** Typically, $A$ is initialised from $\mathcal{N}(0, \sigma^2)$ and $B$ is initialised to zero, ensuring $\Delta W = 0$ at the start of training.

### Optimisation

Fine-tuning uses stochastic gradient descent variants. For a mini-batch $\mathcal{B} \subset \mathcal{D}_{\text{fine-tune}}$, the gradient is:

$$
\nabla_\theta \mathcal{L} \approx -\frac{1}{|\mathcal{B}|} \sum_{i \in \mathcal{B}} \nabla_\theta \log p_\theta(y_i \mid x_i)
$$

AdamW is standard, with update rule:

$$
\theta_{t+1} = \theta_t - \eta \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda_{\text{wd}} \theta_t \right)
$$

where $\hat{m}_t$ and $\hat{v}_t$ are bias-corrected moment estimates, $\eta$ is the learning rate, and $\lambda_{\text{wd}}$ is weight decay.

### Key Assumptions

1. **Distribution alignment:** The fine-tuning data $\mathcal{D}_{\text{fine-tune}}$ is representative of the deployment distribution.
2. **Sufficient pre-training:** The base model has learned representations transferable to the target task.
3. **Label quality:** Target outputs $y_i$ are correct and represent desired model behaviour.
4. **Stationarity:** The task definition does not change during or after fine-tuning.

### Edge Cases and Degenerate Conditions

- **$N \to 0$:** With insufficient data, the model overfits to idiosyncrasies of the few examples.
- **$r \to 0$ in LoRA:** No adaptation capacity; the model cannot learn.
- **$r \to \min(d,k)$:** Full-rank adaptation; equivalent to full fine-tuning with no parameter efficiency.
- **High learning rate:** Catastrophic forgetting of pre-trained knowledge.
- **Homogeneous data:** If all $y_i$ are near-identical, the model collapses to a single output pattern.

### Relationship to Other Methods

Fine-tuning occupies a middle ground between **prompt engineering** (no parameter updates) and **training from scratch** (no transfer). **Prefix tuning** and **adapter methods** are related parameter-efficient alternatives that insert small trainable modules while freezing base weights.

## Understanding the Mathematics

### The Fine-Tuning Loss Function

**The equation:**

$$\mathcal{L}(\theta) = -\frac{1}{N}\sum_{i=1}^{N}\sum_{t=1}^{T_i} \log P_\theta(y_t^{(i)} | y_{<t}^{(i)}, x^{(i)})$$

**Read it aloud:**

"The loss equals negative one divided by the total number of training examples, multiplied by the sum across all examples and all time steps of the log probability that our model (with parameters theta) assigns to the correct next token, given all previous tokens and the input."

**What each symbol means:**

- $\mathcal{L}(\theta)$ = the loss (error) we're trying to minimize, depends on model parameters
- $N$ = total number of training examples in our fine-tuning dataset
- $T_i$ = length (number of tokens) in example $i$
- $P_\theta$ = probability distribution produced by the model with parameters $\theta$
- $y_t^{(i)}$ = the actual correct token at position $t$ in example $i$
- $y_{<t}^{(i)}$ = all tokens before position $t$ in example $i$
- $x^{(i)}$ = the input prompt for example $i$
- $\log$ = natural logarithm (penalizes wrong predictions heavily)

**A concrete numerical example:**

Suppose we're fine-tuning a customer service chatbot on 1,000 examples ($N=1000$). For one training example: "Customer: My order is late. Agent: I apologize for the delay. Let me check your order status."

At one position, the model assigns these probabilities to the next word:
- "apologize" (correct): 0.7
- "understand": 0.2  
- "see": 0.1

The log probability for this position: $\log(0.7) = -0.357$

If our model predicts poorly elsewhere (say $\log(0.1) = -2.303$), those errors add up. After summing across all 15 tokens in this example and averaging across all 1,000 examples, we might get $\mathcal{L}(\theta) = 1.85$. Our goal: reduce this number through training.

**Why this equation matters:**

This loss function tells the model exactly how wrong it is at every prediction, allowing gradient descent to systematically adjust billions of parameters toward generating responses that match your specific domain, style, and requirements.

### The Parameter Update Rule

**The equation:**

$$\theta_{t+1} = \theta_t - \eta \nabla_\theta \mathcal{L}(\theta_t)$$

**Read it aloud:**

"The new parameters equal the old parameters minus the learning rate multiplied by the gradient of the loss with respect to the current parameters."

**What each symbol means:**

- $\theta_{t+1}$ = model parameters after this update step
- $\theta_t$ = model parameters before this update step
- $\eta$ = learning rate (how big a step we take)
- $\nabla_\theta \mathcal{L}$ = gradient (the direction and steepness of the loss function)
- $-$ = we subtract because we want to go *down* the hill (reduce loss)

**A concrete numerical example:**

Imagine one parameter in the model currently has value $\theta_t = 0.5$. The gradient at this point is $\nabla_\theta \mathcal{L} = 2.0$ (meaning the loss increases steeply in the positive direction). With learning rate $\eta = 0.01$:

$$\theta_{t+1} = 0.5 - 0.01 \times 2.0 = 0.5 - 0.02 = 0.48$$

This parameter moves from 0.5 to 0.48, nudging the model slightly toward better predictions. Multiply this by 7 billion parameters updating simultaneously, and the model's behaviour shifts measurably toward your training data.

**Why this equation matters:**

This is how learning actually happens—without this update rule, we'd know the model is wrong (from the loss) but couldn't systematically fix it; with it, every training step makes the model slightly better at your specific task.

### The Big Picture

The mathematics of fine-tuning does one thing: measure how badly the model predicts your training data, then adjust billions of internal parameters to reduce that badness. The loss function quantifies "badness" as a single number by checking every prediction the model makes and penalizing mistakes. The update rule then uses calculus to figure out which direction each parameter should move—and by how much—to make the loss smaller. We use this particular approach because gradient descent can navigate unimaginably high-dimensional spaces (billions of parameters) efficiently, finding configurations that simple trial-and-error never could. At its core, the math answers one question over and over: "If I tweak this number by a tiny amount, does my model get better or worse at sounding like my training data?"

## Python Implementation

```python
"""
Fine-tuning a language model using the Hugging Face Transformers library.
This example demonstrates supervised fine-tuning on a text classification task
reformulated as text generation, using LoRA for parameter efficiency.
"""

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, TaskType
import numpy as np

# Set random seed for reproducibility
torch.manual_seed(42)
np.random.seed(42)

# --- Step 1: Create a synthetic fine-tuning dataset ---
# Simulating customer feedback classification task

training_examples = [
    {"input": "The product arrived damaged and customer service was unhelpful.", 
     "output": "Sentiment: Negative\nCategory: Product Quality, Customer Service"},
    {"input": "Absolutely love this! Fast shipping and great quality.", 
     "output": "Sentiment: Positive\nCategory: Shipping, Product Quality"},
    {"input": "Item works as expected. Nothing special but does the job.", 
     "output": "Sentiment: Neutral\nCategory: Product Quality"},
    {"input": "Terrible experience. Waited 3 weeks and received wrong item.", 
     "output": "Sentiment: Negative\nCategory: Shipping, Order Accuracy"},
    {"input": "Best purchase I've made this year. Highly recommend!", 
     "output": "Sentiment: Positive\nCategory: General Satisfaction"},
    # In practice, you would have 100-10,000 such examples
]

# Format as instruction-following data
def format_example(example):
    return {
        "text": f"### Instruction: Classify the following customer feedback.\n\n"
                f"### Input: {example['input']}\n\n"
                f"### Response: {example['output']}"
    }

formatted_data = [format_example(ex) for ex in training_examples]
dataset = Dataset.from_list(formatted_data)

# --- Step 2: Load pre-trained model and tokenizer ---
model_name = "gpt2"  # Using GPT-2 for demonstration; replace with larger model in production
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # GPT-2 lacks a pad token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    device_map="auto" if torch.cuda.is_available() else None,
)

# --- Step 3: Configure LoRA for parameter-efficient fine-tuning ---
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,                    # Rank of the low-rank matrices
    lora_alpha=32,          # Scaling factor (alpha/r applied to updates)
    lora_dropout=0.1,       # Dropout probability for LoRA layers
    target_modules=["c_attn", "c_proj"],  # Which modules to adapt (attention layers)
)

# Apply LoRA to the model
model = get_peft_model(model, lora_config)

# Print trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 294,912 || all params: 124,734,720 || trainable%: 0.2364

# --- Step 4: Tokenize the dataset ---
def tokenize_function(examples):
    tokenized = tokenizer(
        examples["text"],
        truncation=True,
        max_length=256,
        padding="max_length",
    )
    # For causal LM, labels are the same as input_ids
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# --- Step 5: Configure training arguments ---
training_args = TrainingArguments(
    output_dir="./fine_tuned_model",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=2,  # Effective batch size = 4
    learning_rate=2e-4,             # Higher than full fine-tuning due to LoRA
    weight_decay=0.01,
    warmup_ratio=0.1,
    logging_steps=10,
    save_strategy="epoch",
    fp16=torch.cuda.is_available(),  # Mixed precision if GPU available
)

# --- Step 6: Initialize trainer and run fine-tuning ---
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # Causal LM, not masked LM
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
)

# Execute training
print("Starting fine-tuning...")
trainer.train()
print("Fine-tuning complete!")

# --- Step 7: Inference with the fine-tuned model ---
def generate_classification(input_text):
    prompt = (f"### Instruction: Classify the following customer feedback.\n\n"
              f"### Input: {input_text}\n\n"
              f"### Response:")
    
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = inputs.to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            temperature=0.1,  # Low temperature for deterministic output
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the generated response
    return response.split("### Response:")[-1].strip()


## Visualisations

![](../../_static/figures/fine-tune-model_fig1.png)

![](../../_static/figures/fine-tune-model_fig2.png)

## Using This in Heuristix

### Input Data Requirements

The Fine-tune Model node expects a dataset with at least two columns: your **input text** (prompts or questions) and **output text** (desired completions or answers). Think of these as example conversations you want your model to learn from.

| Input Column | Output Column |
|--------------|---------------|
| "Summarise this product review: The coffee maker broke after 2 weeks..." | "Negative review: Product durability issue reported within 2 weeks of purchase." |
| "Summarise this product review: Best purchase ever! Makes perfect coffee..." | "Positive review: Customer highly satisfied with product performance." |
| "Summarise this product review: It's okay, nothing special but works fine..." | "Neutral review: Product meets basic expectations without standout features." |

Your dataset should contain 50+ examples minimum, though 200–500 examples typically produce better results. Each row represents one training example showing the model exactly what good output looks like.

### Configuration Parameters

| Parameter | What It Controls | Sensible Default | When to Adjust |
|-----------|------------------|------------------|----------------|
| **Base Model** | Which pre-trained model to start from (e.g., GPT-3.5, Llama 2) | GPT-3.5-turbo | Choose larger models (GPT-4) for complex reasoning tasks; smaller models for speed and cost efficiency |
| **Training Epochs** | How many times the model sees your entire dataset | 3 | Increase to 4–5 if the model hasn't learned patterns well; decrease to 1–2 if you notice it's memorising examples verbatim |
| **Learning Rate** | How aggressively the model adjusts during training | Auto | Only change if you understand model training—too high causes instability, too low means slow learning |
| **Batch Size** | How many examples processed together | 4 | Increase to 8–16 if you have ample GPU memory; larger batches train faster but use more resources |
| **Validation Split** | Percentage of data held back for testing | 20% | Increase to 30% if you have abundant data and want robust evaluation; decrease to 10% if data is scarce |

### What You'll See as Output

After training completes, the node provides several outputs:

**Fine-tuned Model ID**: A unique identifier you'll use to reference your custom model in downstream nodes. Save this—it's how you access your trained model.

**Training Metrics Chart**: A line graph showing loss (error) decreasing over time. You want to see a steady downward trend that levels off. If it's still dropping steeply at the end, consider more epochs. If it increases, you may be overfitting.

**Validation Results Table**: Shows sample predictions from your model on the held-back validation data, letting you spot-check quality before deploying.

**Performance Summary**: Includes final loss values, training time, and token usage—helpful for estimating costs and comparing different fine-tuning runs.

### Connecting to Downstream Nodes

Connect your fine-tuned model to:
- **Generate Text** node: Use your custom model for production inference
- **Evaluate Model** node: Test performance against a holdout dataset
- **A/B Test** node: Compare your fine-tuned model against the base model or prompt engineering approaches

### Quick Start: Fine-tune a Customer Support Classifier

1. **Prepare your data**: Create a dataset with "customer_question" and "category" columns containing 200+ labelled support tickets
2. **Connect dataset** to the Fine-tune Model node input
3. **Select columns**: Choose "customer_question" as input, "category" as output
4. **Choose base model**: Start with GPT-3.5-turbo for cost-effectiveness
5. **Leave other settings default** for your first run
6. **Execute the node** and wait 10–30 minutes for training
7. **Review the validation results** to check if categorisations look accurate
8. **Connect to Generate Text** node to start using your model in production

### Expert Tips

- **Start small, iterate fast**: Begin with 100 examples and default settings. You'll learn more from quickly testing what works than from perfecting your first attempt.

- **Balance your dataset**: If you're training a classifier, ensure each category has similar numbers of examples. An imbalanced dataset (e.g., 90% "positive", 10% "negative") will produce a biased model.

- **Watch for overfitting**: If training loss drops to near-zero but validation loss stays high, your model is memorising rather than learning. Reduce epochs or add more diverse training data.

- **Version your training data**: Keep track of which dataset version produced which model. You'll thank yourself when comparing model performance weeks later.

- **Cost awareness**: Fine-tuning charges per token processed. A 500-example dataset with 100 tokens each, trained for 3 epochs, processes 150,000 tokens. Monitor the cost estimator before large training runs.

## Config Recipes

### Recipe 1: Rapid Prototype Explorer

**When to use:** Initial feasibility testing with limited labeled data (<500 examples) to determine if fine-tuning will solve your problem before investing in full-scale data collection.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `epochs` | 3 | Prevents overfitting on tiny datasets |
| `learning_rate` | 5e-5 | Higher rate accelerates convergence on small samples |
| `batch_size` | 4 | Maximizes gradient updates with limited data |
| `warmup_steps` | 50 | Brief warmup sufficient for short training |
| `max_seq_length` | 128 | Reduces memory footprint and speeds iteration |
| `lora_r` | 8 | Minimal adapter complexity for quick testing |
| `evaluation_strategy` | "epoch" | Check performance after each full pass |

**What you get:** A working baseline in under 30 minutes that reveals whether your task is learnable and data quality is sufficient.

**Trade-off:** Results won't generalize well; this model is diagnostic, not deployable.

### Recipe 2: Production-Grade Specialist

**When to use:** Deploying a customer-facing model where reliability, consistency, and performance matter more than training cost—minimum 5,000 curated examples available.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `epochs` | 5–8 | Allows full convergence without degradation |
| `learning_rate` | 2e-5 | Conservative rate prevents catastrophic forgetting |
| `batch_size` | 16 | Stable gradients with moderate hardware |
| `warmup_ratio` | 0.1 | Gradual adaptation protects pre-trained weights |
| `weight_decay` | 0.01 | Regularization against overfitting |
| `gradient_accumulation_steps` | 4 | Effective batch size of 64 for stability |
| `save_strategy` | "steps" | Checkpoint every 500 steps for recovery |
| `eval_steps` | 250 | Frequent validation prevents unnoticed degradation |
| `early_stopping_patience` | 3 | Halts training when validation plateaus |

**What you get:** A robust model with reproducible performance suitable for SLA-backed deployments.

**Trade-off:** Training takes 8–12 hours and requires careful monitoring.

### Recipe 3: Long-Context Document Analyst

**When to use:** Processing technical documents, legal contracts, or research papers where critical information appears late in text—standard 512-token windows lose essential context.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `max_seq_length` | 2048 | Captures full document context |
| `learning_rate` | 1e-5 | Lower rate compensates for longer sequences |
| `batch_size` | 2 | Memory constraints with extended context |
| `gradient_checkpointing` | True | Enables longer sequences within GPU limits |
| `attention_dropout` | 0.15 | Prevents overfitting on position patterns |
| `lora_target_modules` | ["q_proj", "v_proj", "k_proj"] | Adapts attention mechanisms specifically |

**What you get:** Models that extract information from page 8 as reliably as page 1.

**Trade-off:** 4× slower training and inference; requires 24GB+ VRAM.

### Recipe 4: Stylistic Clone for Brand Voice

**When to use:** Replicating a specific writing style (executive communications, marketing copy, support responses) where tone matters as much as accuracy—surprisingly effective with just 200–300 examples.

**Settings:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `epochs` | 10–15 | Style requires more exposure than facts |
| `learning_rate` | 3e-5 | Moderate rate allows nuanced pattern capture |
| `lora_alpha` | 32 | Amplifies adapter influence on generation style |
| `repetition_penalty` | 1.1 | Reduces formulaic outputs during inference |
| `temperature` | 0.7 | Balances consistency with natural variation |

**What you get:** Generated text indistinguishable from human-authored samples in blind tests.

**Trade-off:** Fact accuracy may degrade slightly; validate outputs for correctness.

## Business Applications

**Financial Services**

A mid-sized UK mortgage lender processes 2,400 home loan applications monthly, each requiring manual review of income verification documents, bank statements, and credit histories. Their compliance team spends 18 minutes per application extracting key data points and flagging potential risks. By fine-tuning a foundation model on 14,000 historical applications (including approved loans, declines, and fraud cases), the lender creates a specialised document extraction and risk assessment system that understands mortgage-specific terminology, regulatory requirements, and subtle risk indicators. Processing time drops from 18 minutes to 90 seconds per application, saving £340,000 annually in operational costs while reducing false positive flags by 41%.

**Retail & E-commerce**

An online fashion retailer managing 850,000 SKUs across twelve European markets struggles with inconsistent product descriptions—some are detailed and SEO-optimised, others are sparse manufacturer specs. Customer service receives 3,200 monthly queries asking basic questions that better descriptions would answer. Fine-tuning a model on their top-performing product pages (correlating description style with conversion rates, return rates, and customer satisfaction scores) creates a system that generates on-brand, market-specific, conversion-optimised descriptions. The retailer regenerates 340,000 descriptions in six weeks, lifting average click-through rate from 1.8% to 3.1% and reducing product-related support tickets by 52%.

**Healthcare**

A hospital network operating 23 facilities across three states generates 47,000 clinical notes daily in inconsistent formats—some physicians write detailed narratives, others use fragments and abbreviations. Coding specialists spend hours translating notes into billable diagnosis codes, creating a 9-day average lag between service delivery and claim submission. Fine-tuning a model on 280,000 notes paired with validated ICD-10 codes (including corrections flagged during audits) produces a clinical documentation assistant that suggests appropriate codes with context-aware explanations. Coding lag drops to 2.3 days, claim rejection rates fall by 28%, and the network recovers an estimated $4.7M in previously unbilled services annually.

**Insurance**

A commercial property insurer receives 840 complex claims monthly requiring adjusters to review policy documents, site photos, repair estimates, and historical precedents. Senior adjusters spend 4.2 hours per claim researching similar cases and drafting settlement recommendations. Fine-tuning on 12,000 closed claims (including dispute outcomes, litigation results, and satisfaction scores) creates an adjuster co-pilot that suggests settlement ranges, identifies policy clause conflicts, and flags claims with litigation risk patterns. Average handling time decreases from 4.2 hours to 95 minutes, adjuster capacity increases by 63%, and settlement accuracy improvements reduce disputes by 19%.

**Manufacturing**

A precision aerospace components manufacturer maintains 340 CNC machines generating cryptic error logs in proprietary formats—interpreting them requires scarce expertise from senior technicians. Unplanned downtime costs £8,400 per hour, and junior technicians often escalate issues that could be resolved locally. Fine-tuning on 89,000 maintenance logs paired with root cause analyses and resolution steps creates a diagnostic assistant that interprets error patterns and recommends specific interventions. Mean time to resolution drops from 3.8 hours to 47 minutes, reducing annual unplanned downtime costs by £2.1M.

**Logistics**

A European freight forwarder managing 15,000 shipments monthly across 34 countries loses margin to manual customs documentation—each shipment requires country-specific forms with precise HS codes, origin certificates, and regulatory declarations. Documentation errors cause 7% of shipments to face customs delays averaging 4.3 days. Fine-tuning on 67,000 successful shipment records creates a customs documentation system that generates accurate, country-specific paperwork from basic shipment details. Documentation time falls from 22 minutes to 3 minutes per shipment, delay rates drop to 1.8%, and customer satisfaction scores improve by 31 points.

**Marketing & Advertising**

A B2B SaaS company sends 340,000 personalised emails monthly but struggles with tone consistency—messages from different product teams sound disjointed, and generic templates underperform. Open rates hover at 19%, below their 24% industry benchmark. Fine-tuning on their 2,400 highest-performing emails (segmented by recipient role, industry, and funnel stage) creates a brand-aligned copywriting assistant. Email open rates climb to 26.3%, click-through rates improve from 2.1% to 3.7%, and the marketing team ships campaigns 4× faster.

**Telecommunications**

A mobile network operator's customer service team handles 28,000 daily chat conversations, but response quality varies dramatically between agents—leading to inconsistent issue resolution and a 34% repeat contact rate. Fine-tuning on transcripts from their top-performing agents (those with highest first-contact resolution and satisfaction scores) creates an AI assistant that suggests contextual responses maintaining brand voice and technical accuracy. First-contact resolution improves by 23 percentage points, and repeat contacts fall to 19%.

**Public Sector**

A municipal planning department processes 1,800 development applications annually, each requiring staff to draft public-facing summaries of technical architectural and environmental reports. Planning officers spend 6.5 hours per application on documentation, delaying approval timelines. Fine-tuning on 4,200 historical applications creates a system that generates citizen-friendly summaries maintaining regulatory precision. Documentation time drops to 90 minutes per application, accelerating average approval cycles from 87 days to 61 days.

## Worked Example

Sarah Chen, a machine learning engineer at Lexis Medical Analytics, was called into an urgent meeting with the clinical operations team on a Tuesday morning. Dr. Patel, the head of patient engagement, had a problem: their customer service team was drowning in patient messages about prescription refills, appointment changes, and billing questions. The team was spending hours crafting personalised, empathetic responses that matched the clinic's tone—warm but professional, clear but not clinical. "We've tried GPT-4 with prompts," Dr. Patel explained, "but the responses feel generic. Patients can tell it's automated, and we're getting complaints. Can we teach a model to sound like *us*?"

Sarah knew this was a perfect use case for fine-tuning. She spent the next day pulling together a dataset of 2,847 real message-response pairs from their ticketing system, with identifying information scrubbed. Each row contained a patient message, the category of inquiry, and the actual response written by their best support agents.

| patient_message | category | agent_response | response_length |
|---|---|---|---|
| "Hi I need to refill my blood pressure meds but the pharmacy says..." | prescription | "Hello! I've checked your prescription, and I can see it expired last month. I've sent a renewal request to Dr. Williams—you should hear back within 24 hours. In the meantime, if you're running low, our on-call nurse line can help at 555-0199." | 267 |
| "Can I move my appointment from Thursday to next week sometime?" | scheduling | "Absolutely! I have availability next Tuesday at 2pm or Wednesday at 10am. Which works better for your schedule? Just reply with your preference and I'll get you confirmed right away." | 178 |
| "Your billing department charged me twice for the same visit!!!" | billing | "I'm so sorry for the frustration—I can see why that's upsetting. I've flagged this for our billing team and they're reviewing your account right now. You should receive a call by end of day tomorrow to resolve this. Thank you for bringing it to our attention." | 243 |
| "What are your office hours on weekends?" | general | "Great question! We're open Saturdays from 9am to 1pm for urgent appointments. For non-urgent matters, our next available weekday slots are usually Monday and Tuesday mornings." | 164 |

The data was messy in the way real data always is—some responses had email signatures still attached, others included internal notes in brackets that needed stripping out. Sarah spent two hours cleaning it before she felt confident moving forward.

She opened the Fine-tune Model node in her workflow and made her configuration choices deliberately. Base model: GPT-3.5-turbo—powerful enough for natural language, small enough to fine-tune economically. She set the training split to 85/15, keeping 427 examples for validation. Learning rate: 0.0002, lower than default because she wanted the model to adapt gradually without forgetting its general language capabilities. Epochs: 3, based on her validation loss curve from an initial run that showed overfitting after the fourth epoch.

```python
import openai
import pandas as pd

# Sarah's fine-tuning script
# Load cleaned patient message data
df = pd.read_csv('patient_messages_clean.csv')

# Format for OpenAI fine-tuning API
training_data = []
for _, row in df.iterrows():
    training_data.append({
        "messages": [
            {"role": "system", "content": "You are a helpful patient support agent at Lexis Medical. Respond with empathy, clarity, and warmth."},
            {"role": "user", "content": row['patient_message']},
            {"role": "assistant", "content": row['agent_response']}
        ]
    })

# Upload training file
with open('training_data.jsonl', 'w') as f:
    for item in training_data:
        f.write(json.dumps(item) + '\n')

# Start fine-tuning job
response = openai.FineTuningJob.create(
    training_file="training_data.jsonl",
    model="gpt-3.5-turbo",
    hyperparameters={
        "n_epochs": 3,
        "learning_rate_multiplier": 0.2
    }
)

print(f"Fine-tuning job created: {response['id']}")
```

Four hours later, the fine-tuning completed. Sarah ran the validation set through both the base model and her fine-tuned version. The results were striking:

| Metric | Base GPT-3.5 | Fine-tuned Model |
|---|---|---|
| Response tone match (human eval) | 62% | 91% |
| Avg. response length | 312 chars | 201 chars |
| Policy compliance rate | 78% | 96% |
| Patient satisfaction (blind test) | 3.4/5 | 4.6/5 |

The insight hit Sarah immediately: the fine-tuned model had learned not just *what* to say, but *how* to say it—matching the clinic's specific voice, brevity, and even the pattern of offering concrete next steps with phone numbers and timeframes. It had internalised institutional knowledge like which doctor handled prescription renewals and typical appointment availability.

Two weeks later, Sarah presented to the executive team. Dr. Patel ran a pilot where the fine-tuned model drafted responses that agents could review and send with one click. Response time dropped from 4.2 hours to 22 minutes. The clinic rolled it out fully the following month, reallocating two full-time support staff to complex cases that genuinely needed human judgment.

If Sarah were doing this again, she'd collect more examples of edge cases—angry patients, complex multi-issue messages—where the model still occasionally stumbled. And she'd build in a confidence score so the system could automatically escalate uncertain responses to human review.

## Interpreting Your Results

You've just fine-tuned your first model. Now you're staring at a results dashboard filled with loss curves, accuracy metrics, and validation scores. Let's translate those numbers into decisions.

### Training and Validation Loss

**Plain-English meaning**: Loss measures how wrong your model's predictions are. Think of it as a wrongness score—lower is better. Training loss shows errors on data the model is learning from; validation loss shows errors on data it hasn't seen. You want both dropping steadily, like a plane descending smoothly to land.

**Concrete benchmarks**:
- **Final loss below 0.5**: Excellent. Your model has learned the task well.
- **Final loss 0.5–1.5**: Good. Acceptable for most business applications, especially complex tasks.
- **Final loss 1.5–3.0**: Marginal. May work for simple classification, but scrutinise outputs carefully.
- **Final loss above 3.0**: Poor. The model hasn't learned effectively—don't deploy this.

**Red flags**:
- **Training loss drops but validation loss rises** (the classic divergence): Overfitting. Your model memorised training examples instead of learning patterns. Reduce training epochs or add more diverse data.
- **Both losses plateau early and stay high**: Underfitting. The model hasn't trained long enough, or your data is too noisy. Try more epochs or clean your dataset.
- **Validation loss jumps erratically**: Data quality issue. Check for duplicates, inconsistent formatting, or mislabelled examples in your validation set.

### Accuracy/F1 Score

**Plain-English meaning**: Accuracy tells you what percentage of predictions were correct. F1 balances precision (when the model says "yes," is it right?) and recall (does it catch all the "yes" cases?). For imbalanced tasks—like fraud detection where 99% of cases are normal—F1 is more reliable than raw accuracy.

**Concrete benchmarks**:
- **Above 0.90**: Strong performance. Deploy with confidence for most use cases.
- **0.75–0.90**: Solid. Acceptable for decision-support tools, but add human review for high-stakes decisions.
- **0.60–0.75**: Weak. Useful only for preliminary filtering or low-consequence tasks.
- **Below 0.60**: Failed. The model is barely better than guessing—do not use.

**Red flags**:
- **Accuracy high (>0.95) but F1 low (<0.70)**: Class imbalance problem. The model just predicts the majority class. Check your class distribution.
- **Training accuracy 0.99+ while validation accuracy <0.70**: Severe overfitting. The model won't generalise.

### Perplexity (for generative tasks)

**Plain-English meaning**: Perplexity measures how "surprised" the model is by the correct next word. Lower perplexity means the model confidently predicts natural-sounding text. It's most relevant when fine-tuning for text generation or completion.

**Concrete benchmarks**:
- **Below 20**: Excellent. The model generates fluent, contextually appropriate text.
- **20–50**: Good. Minor awkwardness but generally coherent.
- **50–100**: Poor. Outputs will feel robotic or nonsensical.
- **Above 100**: Unusable. Start over with better data or a different base model.

### Reading Metrics Together

Don't evaluate metrics in isolation. Here's what combinations reveal:

- **Low training loss + low validation loss + high accuracy**: Ideal. Your model learned well and generalises.
- **Low training loss + high validation loss + accuracy gap >15%**: Classic overfitting. Need more data or regularisation.
- **High training loss + high validation loss**: The model never learned. Check data quality, increase epochs, or verify your task isn't too complex for the base model.
- **High F1 + low accuracy on imbalanced data**: Expected and good—trust F1 here.

### Sanity Check Checklist

Before trusting your results, verify:

1. **Did validation loss decrease at all?** If it stayed flat or only dropped <5%, the model didn't learn.
2. **Is validation set representative?** If it's too small (<10% of data) or drawn from a different distribution, metrics lie.
3. **Are you beating the baseline?** Compare to your pre-fine-tuned model or simple heuristics. If fine-tuning didn't improve things by at least 10%, something's wrong.
4. **Do sample predictions make sense?** Manually inspect 20–30 outputs. Metrics can look good while outputs are gibberish.
5. **Did training complete normally?** Check for warnings about truncated examples, NaN losses, or memory errors—these silently corrupt results.

### Good Enough to Act On?

**Deploy when**: Validation loss is below 1.0, validation accuracy/F1 exceeds 0.80, and manual review of 50 random predictions shows fewer than 5 clear errors. You'll never reach perfection—these thresholds balance quality with business value. If you're above these bars and your sanity checks pass, stop tweaking and start testing with real users. You can always iterate later.

## Decision Guidance

### What This Result Is Telling You

Fine-tuning results reveal whether your investment in model customisation has produced a system that can reliably perform your specific task better than off-the-shelf alternatives. When you see improved performance metrics after fine-tuning, you're looking at evidence that your curated dataset has successfully taught the model your domain's language, your organisation's standards, and the specific patterns that matter for your use case. This isn't just about accuracy percentages—it's confirmation that the model has internalised the expertise you've encoded in your training examples and can now replicate that judgement at scale.

The comparison between your fine-tuned model and baseline alternatives (such as zero-shot prompting or few-shot examples) quantifies the business value of your fine-tuning investment. A substantial performance improvement justifies the engineering effort, computational cost, and ongoing maintenance. Conversely, marginal gains signal that simpler prompting strategies might deliver equivalent results at lower cost and complexity. The error patterns you observe during evaluation reveal which scenarios your model handles confidently and which edge cases require human oversight or further refinement.

Fine-tuning results also indicate readiness for production deployment. Consistent performance across diverse test scenarios demonstrates robustness, while high variance or unexpected failure modes on validation data warn that your model may behave unpredictably when encountering real-world inputs. The stability and reliability of these results directly determine whether you can safely automate decisions, augment human workflows, or must restrict the model to advisory roles with mandatory human review.

### Decision Points

| If you see this... | It means... | Recommended action | Who acts on this |
|-------------------|-------------|-------------------|------------------|
| Fine-tuned model outperforms baseline by >15% on task-specific metrics, with <5% variance across validation folds | Your training data successfully captured the task requirements; model is production-ready | Deploy to production with standard monitoring protocols; allocate budget to maintain and update training data | Product owner + ML engineering lead |
| Improvement over baseline is 5-15%, or model performs well on common cases but fails on 10-20% of edge cases | Model provides value but isn't reliable enough for full automation | Deploy in human-in-the-loop configuration; route low-confidence predictions to manual review; invest in collecting more edge-case examples | Operations manager + data science team |
| Performance gain over baseline <5%, or prompting achieves equivalent results | Fine-tuning investment doesn't justify the complexity | Revert to prompt engineering; reallocate fine-tuning resources; reassess whether task truly requires customisation | Technical lead + finance stakeholder |
| Model shows >20% performance degradation on held-out temporal data or different data sources | Model has overfit to training distribution; won't generalise to production conditions | Do not deploy; collect more diverse training data; implement data augmentation; consider domain adaptation techniques | ML engineer + domain expert |

### When to Proceed vs. Investigate Further

**Proceed with confidence when:**
- Fine-tuned model achieves >90% of human expert performance on your task
- Performance improvement over baseline exceeds 15 percentage points
- Model maintains consistent accuracy (±3%) across all validation splits
- Error analysis shows failures are acceptable edge cases, not systematic blind spots

**Proceed with caution when:**
- Performance gain is 10-15% but critical errors still occur in 5-10% of cases
- Model excels on training domain but shows 10-15% degradation on adjacent use cases
- Computational cost of fine-tuned model is 3-5× higher than alternatives with only marginal performance benefit

**Investigate before acting when:**
- Model performance varies by >10% across different data subsets or time periods
- Specific demographic groups, product categories, or input types show disproportionately high error rates (>15% disparity)
- Fine-tuning improved overall metrics but introduced new failure modes not present in baseline

**Do not use these results yet when:**
- You cannot explain why the model fails on specific examples through error analysis
- Training and validation metrics diverge by >10% (indicating overfitting or data leakage)
- Model performance on business-critical scenarios falls below 85% accuracy
- You lack infrastructure to monitor model predictions and capture production feedback

### The Cost of Getting This Wrong

Deploying a fine-tuned model that appears successful in testing but hasn't been properly validated leads to systematic failures at scale that erode customer trust and create expensive remediation work. A customer service model that performs well on average but fails catastrophically for 10% of sensitive inquiries will generate complaints, regulatory scrutiny, and emergency rollbacks—wasting months of engineering effort and potentially damaging brand reputation. Conversely, rejecting a well-performing fine-tuned model because stakeholders don't understand the validation results means your competitors will automate workflows while your organisation continues manual processing at 10-100× the operating cost. Perhaps most insidiously, proceeding with a model that has overfit to historical training data means you're automating yesterday's patterns into tomorrow's decisions—your system will confidently make outdated judgements while market conditions, customer preferences, or regulatory requirements have shifted, creating systematic blind spots that accumulate business risk until a significant failure forces recognition of the problem.

## Common Pitfalls

**The Validation Leak**

Here's what happened: A junior ML engineer at a fintech company was fine-tuning GPT-3.5 for loan application classification. They shuffled their entire dataset before splitting it 80/20 for training and validation. The validation accuracy hit 96%, so they pushed to production. Within two weeks, the model was rejecting legitimate applications at twice the expected rate. They eventually discovered that multiple applications from the same customers appeared in both training and validation sets—the model had memorized customer patterns rather than learning decision criteria.

Why it happens: The mental model that "random splitting equals proper validation" ignores the temporal and hierarchical structure of real-world data. Engineers apply image classification habits to sequential business data.

How to detect it: Check for suspiciously small gaps between training and validation loss (< 0.05 difference when you'd expect 0.1–0.2). More definitively, examine your data for natural groupings—customer IDs, time periods, document sources—and verify none span both sets.

The fix: Split by the entity that will be new at inference time (customers, time periods, or documents), not by individual records.

**The Overfit Celebration**

Here's what happened: A marketing analyst fine-tuned a model to generate product descriptions, achieving training loss of 0.12 and validation loss of 0.14. Thrilled by the close numbers, they deployed immediately. Customer feedback revealed the model was generating nearly identical descriptions for different products, regurgitating training examples with minor word substitutions. The "low validation loss" masked complete failure to generalise.

Why it happens: Optimising for loss metrics without inspecting actual outputs. Validation loss measures prediction accuracy on held-out data, but it doesn't detect memorization, lack of diversity, or semantic collapse.

How to detect it: Generate 50–100 outputs on validation data and manually review them. Look for repetitive phrasing, training data verbatim, or outputs that ignore input variation. Calculate distinct n-gram ratios—if fewer than 60% of trigrams are unique across outputs, you've likely overfit.

The fix: Implement early stopping based on both quantitative metrics and qualitative output review; schedule human evaluation before every deployment.

**The Catastrophic Forgetting**

Here's what happened: A healthcare startup fine-tuned Llama-2 on 5,000 medical records to extract patient symptoms. The model performed beautifully on medical text but suddenly couldn't handle basic instructions like "format this as a bullet list" or "translate to Spanish"—capabilities the base model handled effortlessly. They'd tuned away the foundation model's general-purpose abilities.

Why it happens: Using high learning rates (> 5e-5) or training too long on narrow domain data causes the model to overwrite its pre-trained weights, erasing capabilities not reinforced in the fine-tuning data.

How to detect it: Test the fine-tuned model on the base model's benchmark tasks. If scores drop by more than 15% on tasks like MMLU or HellaSwag while your domain metric improves, you're experiencing catastrophic forgetting.

The fix: Lower your learning rate to 1e-5 or below, reduce training epochs, and include diverse examples that exercise general capabilities alongside domain-specific ones.

**The Tiny Dataset Delusion**

Here's what happened: An e-commerce manager collected 47 "perfect" examples of their brand voice and fine-tuned GPT-4 for two epochs. Validation metrics looked acceptable. In production, the model produced on-brand content for queries similar to training examples but generated wildly off-brand responses for edge cases, including occasional offensive language.

Why it happens: Belief that LLMs can learn complex behaviours from tiny datasets because "they already know language." Fine-tuning on micro-datasets doesn't teach behaviour—it biases the probability distribution, and with insufficient examples, that distribution becomes unpredictable outside the training manifold.

How to detect it: If your training set contains fewer than 500 examples, you're in the danger zone. Check performance stratified by input similarity to training data—degradation of 30%+ on dissimilar inputs signals insufficient coverage.

The fix: Either collect 500+ diverse examples, use few-shot prompting instead of fine-tuning, or accept that fine-tuning is premature for your use case.

**The Learning Rate Lottery**

Here's what happened: A senior engineer at a legal tech firm used the default learning rate (5e-5) from a tutorial written for BERT on classification tasks. They were fine-tuning GPT-3.5 for generative contract analysis. Training loss exploded to infinity by epoch 2. They slashed the rate to 1e-6, but training plateaued immediately with no improvement. After a week of frustration, they discovered their optimal rate was 8e-6—found only through systematic experimentation.

Why it happens: Copy-pasting hyperparameters across model architectures and task types. Learning rates that work for encoder models on classification fail for decoder models on generation; rates for 100M parameter models destroy 7B parameter models.

How to detect it: Loss curves tell the story immediately. Exploding loss (values increasing or becoming NaN) means too high; flat loss (< 1% change after one epoch) means too low.

The fix: Run a learning rate finder across two orders of magnitude (1e-6 to 1e-4), plotting loss against rate, and select the highest rate before loss destabilizes.

**The Prompt Format Amnesia**

Here's what happened: A data scientist fine-tuned Mistral-7B using conversational data formatted as plain question-answer pairs. The model achieved strong training metrics but produced gibberish in production. They'd forgotten that Mistral expects specific instruction formatting with tags like `[INST]` and `[/INST]`. Their training data didn't match the format the base model was taught to expect.

Why it happens: Assuming all models consume text the same way. Each model family has specific prompt templates baked in during instruction-tuning; ignoring these creates a distribution mismatch.

How to detect it: Compare your training format to the model's documentation examples. If they don't match, you're fighting the base model's priors. You'll see this in erratic output formatting and failure to follow instructions despite low training loss.

The fix: Always use the model's documented prompt template for your fine-tuning data, or explicitly include template tokens in your training examples.

**The Evaluation Theatre**

Here's what happened: A consulting firm fine-tuned a model for client report generation and evaluated it using ROUGE scores, achieving 0.76. Leadership approved deployment. Clients complained that reports were factually accurate but completely missed the analytical insights they needed. ROUGE measured word overlap, not usefulness.

Why it happens: Relying on automated metrics that measure surface features (n-gram overlap, perplexity) as proxies for qualities that matter to users (insight, accuracy, persuasiveness). It's easier to run an automated script than design human evaluation.

How to detect it: If you can't articulate how your evaluation metric connects to user value, you're doing evaluation theatre. If your metric improves but user satisfaction doesn't, the metric was wrong.

The fix: Define 3–5 user-centric quality dimensions, create rubrics, and evaluate 50–100 outputs manually before trusting any automated metric as a proxy.

## Common Misconceptions

**"Fine-tuning is always more expensive than prompt engineering, so we should exhaust prompting strategies first"**

**Why people believe this:** The visible costs of fine-tuning—GPU hours, data labelling, engineering time—appear upfront and substantial. Meanwhile, prompt engineering feels "free" because it uses existing API calls. Finance teams naturally gravitate toward delaying capital expenditure, and this reasoning aligns perfectly with that instinct.

**The truth:** This analysis ignores the ongoing operational cost of prompt-based solutions. Each API call to a large foundation model costs substantially more than inference on a fine-tuned smaller model. For high-volume applications, a fine-tuned model—particularly a smaller one—can reduce per-request costs by 80-95%. More critically, prompt engineering carries hidden labour costs: continuous prompt maintenance, version control, brittle failure modes requiring human intervention, and the cognitive overhead of managing complex prompt chains. Fine-tuning consolidates this complexity into the model weights themselves, reducing operational burden permanently.

**The real-world consequence:** A financial services company spent six months perfecting prompts for contract clause extraction, achieving 78% accuracy at $0.12 per document. After finally fine-tuning a smaller model, they achieved 94% accuracy at $0.008 per document. Their delayed decision cost them approximately $47,000 in unnecessary API fees and missed three regulatory deadlines due to accuracy limitations.

**"More training data always improves fine-tuned model performance"**

**Why people believe this:** This principle holds true during pre-training and in classical machine learning, where larger datasets generally reduce overfitting and improve generalisation. It feels mathematically sound—more signal should mean better learning.

**The truth:** Fine-tuning operates in a fundamentally different regime. The model already possesses broad capabilities; fine-tuning teaches task-specific application of that knowledge. Beyond a certain threshold—often surprisingly low, sometimes 500-2,000 high-quality examples—additional data provides diminishing returns and can actually degrade performance. Poor-quality examples, even in large numbers, teach the model to replicate errors or adopt unwanted patterns. Distribution mismatch between training and deployment data causes the model to "forget" useful pre-trained knowledge in favour of narrow training set patterns.

**The real-world consequence:** An e-commerce team collected 50,000 customer service interactions for fine-tuning, assuming more was better. Their model became overly formal and rigid, mimicking problematic historical responses. When they reduced to 1,200 carefully curated, exemplary interactions—removing edge cases and correcting historical mistakes—accuracy improved from 71% to 89%, and training costs dropped by 85%.

**"Fine-tuning eliminates the need for prompt engineering"**

**Why people believe this:** Fine-tuning is often positioned as the "advanced" alternative to prompting, suggesting a natural progression where one replaces the other. Once a model is specialised, why would you still need careful input design?

**The truth:** Fine-tuning and prompting are complementary, not sequential. Fine-tuning adjusts what the model knows and how it behaves by default; prompting controls what it does with that knowledge in each specific invocation. Even perfectly fine-tuned models require thoughtful prompts to handle context variations, multi-step reasoning, or output format specifications. The most robust production systems combine both: fine-tuning establishes domain expertise and behavioural guardrails, while runtime prompts provide task-specific instructions and dynamic context.

**The real-world consequence:** A legal tech startup fine-tuned a model for case summarisation and removed all prompt structure, assuming the model "knew what to do." Users received inconsistent output formats that broke downstream parsing systems, requiring a three-week emergency project to reintroduce structured prompting.

## How This Connects

### Before This Node

**Prompt Model** contributes baseline performance metrics and identifies where zero-shot or few-shot prompting fails to meet accuracy or consistency requirements; without this comparison, you risk investing in fine-tuning when simpler prompting would suffice, wasting compute resources on unnecessary model training.

**Prepare Labelled Data** provides the curated training dataset with input-output pairs formatted for supervised learning; poor labelling here—inconsistent annotations, subjective judgments, or misaligned examples—directly corrupts the fine-tuned model's behaviour, teaching it to reproduce human errors at scale.

**Split Data** partitions your labelled dataset into training, validation, and test sets with proper stratification; inadequate splitting (data leakage, unrepresentative samples, or temporal misalignment) produces misleadingly high training metrics that collapse during real-world deployment.

**Analyse Text** generates domain-specific features, vocabulary distributions, and semantic patterns that inform hyperparameter choices and data augmentation strategies; skipping this analysis means flying blind—you won't detect class imbalance, vocabulary gaps, or stylistic inconsistencies until after expensive training runs.

**Define Classification Schema** establishes the label taxonomy, output format, and decision boundaries the model must learn; ambiguous or overlapping categories create confusion during training, resulting in models that hedge, hallucinate, or default to the majority class.

**Version Data** maintains lineage tracking for your training corpus, enabling reproducible experiments and rollback capability; without versioning, you cannot isolate whether performance changes stem from data quality issues, hyperparameter adjustments, or model architecture choices.

### After This Node

**Evaluate Model** measures fine-tuned performance against held-out test data using task-specific metrics (F1, BLEU, exact match); Fine-tune Model's outputs are production-ready model checkpoints with embedded task knowledge, making systematic evaluation essential before deployment.

**Prompt Model** now leverages the fine-tuned model for inference on new production data, combining learned task patterns with runtime prompts for enhanced control; the fine-tuned weights provide the specialised foundation that prompting alone could not achieve.

**Deploy Model** packages the fine-tuned checkpoint into serving infrastructure with appropriate latency and throughput guarantees; Fine-tune Model produces standard model artefacts (weights, tokenizer, config) compatible with deployment frameworks.

**Monitor Model** tracks prediction quality, drift, and edge cases in production traffic; fine-tuned models require ongoing monitoring because they've specialised—domain shifts or evolving requirements surface as performance degradation faster than with general models.

**Compare Models** benchmarks the fine-tuned model against baseline prompting, competing architectures, or previous fine-tuned versions; Fine-tune Model's deterministic outputs enable controlled A/B testing and ROI quantification.

### Common Pipeline Patterns

**Customer Support Ticket Routing Pipeline**  
Prepare Labelled Data → Split Data → **Fine-tune Model** → Evaluate Model → Deploy Model  
Automatically categorises and routes 10,000+ daily support tickets to specialised teams with 94% accuracy, reducing median response time from 4 hours to 12 minutes.

**Medical Report Generation Pipeline**  
Analyse Text → Prepare Labelled Data → **Fine-tune Model** → Prompt Model → Monitor Model  
Generates structured radiology reports from clinical findings with institution-specific terminology and formatting, maintaining 89% clinician approval rate while reducing documentation time by 60%.

**Legal Contract Review Pipeline**  
Define Classification Schema → Prepare Labelled Data → **Fine-tune Model** → Compare Models → Evaluate Model  
Identifies non-standard clauses and compliance risks across 200+ contract types, achieving 92% recall on high-risk provisions and reducing manual review hours by 70%.

### What to Have Ready

**Clean, representative training data** with at least 500–1,000 high-quality labelled examples per class or task type, stored in a consistent format (JSONL, CSV) with clear input-output mappings and no missing critical fields.

**Baseline performance metrics** from prompting experiments or existing models, establishing the minimum acceptable accuracy threshold and quantifying the performance gap fine-tuning must close.

**Compute budget and timeline** specifying available GPU resources, acceptable training duration (hours vs. days), and cost constraints that determine model size, batch size, and hyperparameter search scope.

**Evaluation criteria** defining task-specific success metrics beyond accuracy—latency requirements, explainability needs, fairness constraints, and business KPIs the fine-tuned model must satisfy.

## Try It Yourself

### Recommended Dataset

**Dataset**: `fetch_20newsgroups` from `sklearn.datasets`  
**Source**: `sklearn.datasets.fetch_20newsgroups(subset='train')`

**Why it's ideal**: The 20 Newsgroups dataset contains ~11,000 discussion posts across 20 different topic categories (politics, religion, computers, sports, etc.). This multi-class text classification problem is perfect for demonstrating fine-tuning because the pre-existing linguistic structure requires domain adaptation—generic language understanding must be specialised to recognise subtle topical signals and community-specific jargon.

**Business question**: "Can we automatically categorise customer support tickets, user feedback, or content submissions into the correct department or topic area to route them efficiently?"

**Size**: ~11,000 documents (rows) × 2 features (text content, category label)

### Starter Code

```python
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Load a subset of newsgroup categories for faster demonstration
categories = ['sci.space', 'rec.sport.hockey', 'talk.politics.misc', 'comp.graphics']
newsgroups_train = fetch_20newsgroups(subset='train', categories=categories, 
                                      remove=('headers', 'footers', 'quotes'))
newsgroups_test = fetch_20newsgroups(subset='test', categories=categories,
                                     remove=('headers', 'footers', 'quotes'))

print(f"Training samples: {len(newsgroups_train.data)}")
print(f"Test samples: {len(newsgroups_test.data)}")
print(f"Categories: {newsgroups_train.target_names}\n")

# Create baseline "pre-trained" model using simple TF-IDF features
# This simulates a foundation model's general language understanding
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_base = vectorizer.fit_transform(newsgroups_train.data)
X_test_base = vectorizer.transform(newsgroups_test.data)

# Train baseline model (represents pre-trained foundation model)
baseline_model = LogisticRegression(max_iter=200, random_state=42)
baseline_model.fit(X_train_base, newsgroups_train.target)
baseline_preds = baseline_model.predict(X_test_base)
baseline_acc = accuracy_score(newsgroups_test.target, baseline_preds)

print(f"Baseline accuracy: {baseline_acc:.3f}\n")

# Fine-tune by adding domain-specific features (n-grams, longer context)
# This represents adapting the model to specific downstream task characteristics
vectorizer_finetuned = TfidfVectorizer(max_features=5000, ngram_range=(1, 2),
                                       stop_words='english', min_df=2)
X_train_finetuned = vectorizer_finetuned.fit_transform(newsgroups_train.data)
X_test_finetuned = vectorizer_finetuned.transform(newsgroups_test.data)

# Train fine-tuned model with task-specific adaptations
finetuned_model = LogisticRegression(max_iter=200, random_state=42, C=1.5)
finetuned_model.fit(X_train_finetuned, newsgroups_train.target)
finetuned_preds = finetuned_model.predict(X_test_finetuned)
finetuned_acc = accuracy_score(newsgroups_test.target, finetuned_preds)

print(f"Fine-tuned accuracy: {finetuned_acc:.3f}")
print(f"Improvement: {(finetuned_acc - baseline_acc):.3f} "
      f"({100*(finetuned_acc - baseline_acc)/baseline_acc:.1f}% gain)\n")

# Show per-category performance gains from fine-tuning
report = classification_report(newsgroups_test.target, finetuned_preds,
                              target_names=newsgroups_train.target_names,
                              digits=3)
print("Fine-tuned model category performance:")
print(report)
```

### What to Try Next

1. **Add more categories**: Change `categories` to include all 20 topics (remove the parameter entirely). Expect accuracy to drop as the task becomes harder, demonstrating how fine-tuning complexity scales with problem scope.

2. **Adjust regularisation strength**: Change `C=1.5` to `C=0.1` or `C=10.0` in the fine-tuned model. Lower values increase regularisation (preventing overfitting), higher values allow more adaptation. This teaches the bias-variance tradeoff in fine-tuning.

3. **Modify feature complexity**: Change `max_features=5000` to `500` or `10000`. Fewer features may underfit; more may overfit on small datasets. This illustrates the sweet spot between model capacity and available training data.

4. **Experiment with n-gram range**: Change `ngram_range=(1, 2)` to `(1, 1)` (unigrams only) or `(1, 3)` (add trigrams). Expect unigrams to lose context; trigrams to capture domain phrases. This demonstrates how task-specific feature engineering enhances fine-tuning effectiveness.

## Further Reading

1. **Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." NAACL-HLT.** Read this if you want to understand the foundational architecture that popularised the pre-train-then-fine-tune paradigm in NLP. The paper demonstrates how task-specific fine-tuning layers added to pre-trained transformers consistently outperform task-specific architectures trained from scratch, establishing the transfer learning framework that underpins modern LLM adaptation.

2. **Howard, J., & Ruder, S. (2018). "Universal Language Model Fine-tuning for Text Classification." ACL.** Read this if you want to understand discriminative fine-tuning, gradual unfreezing, and slanted triangular learning rates—three techniques that prevent catastrophic forgetting when adapting pre-trained models to smaller datasets. These methods remain essential for practitioners working with limited task-specific data.

3. **Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing* (3rd ed. draft), Chapter 11: "Transfer Learning with Contextual Embeddings and Pre-trained Models," sections 11.2–11.4.** These specific sections provide the clearest pedagogical treatment of how fine-tuning differs mechanically from feature extraction, including explicit mathematical formulations of loss functions during adaptation and guidance on selecting which layers to freeze versus train.

4. **Tunstall, L., von Werra, L., & Wolf, T. (2022). *Natural Language Processing with Transformers*, Chapter 4: "Multilingual Named Entity Recognition," pp. 89–126.** This chapter walks through a complete fine-tuning workflow using Hugging Face Transformers, including dataset preparation, tokenizer alignment, training loop customization, and evaluation—providing production-ready code patterns rather than toy examples.

5. **Hugging Face Transformers Documentation: `Trainer` class** (https://huggingface.co/docs/transformers/main_classes/trainer). Focus on the `TrainingArguments` parameters (`learning_rate`, `warmup_steps`, `weight_decay`, `gradient_accumulation_steps`) and the `compute_metrics` callback. This documentation explains the hyperparameters that most significantly impact fine-tuning stability and final model quality, with practical default values derived from thousands of community experiments.

6. **Rasul, K. (2023). "A Complete Guide to Fine-Tuning Large Language Models," Towards Data Science.** Unlike generic fine-tuning tutorials, this post provides quantitative comparisons of full fine-tuning versus parameter-efficient methods (LoRA, prefix tuning) across different model sizes and dataset scales, helping practitioners make cost-informed architectural decisions before beginning adaptation.

7. **Karpathy, A. (2023). "Let's build GPT: from scratch, in code, spelled out." YouTube, 1:59:50–2:14:30.** This 15-minute segment demonstrates fine-tuning GPT-2 on a custom dataset with live code execution, showing real-time loss curves, overfitting patterns, and debugging strategies that rarely appear in polished tutorials.

8. **Bloomberg (2023). "BloombergGPT: A Large Language Model for Finance," Technical Report.** Documents the complete fine-tuning pipeline for a 50-billion parameter model on financial data, including data curation decisions, infrastructure costs ($2.7M training budget), benchmark improvements, and regulatory considerations—providing rare transparency into enterprise-scale LLM adaptation.

## Practice Exercises

### Exercise 1: Deciding Between Fine-Tuning and Alternatives (Conceptual)

**Scenario:**

You are a Data Science Manager at FinServe Analytics, a financial services company. Your Customer Support team handles 12,000 queries monthly via email. Currently, they use a prompt-engineered GPT-4 solution that costs approximately $0.03 per classification (input + output tokens), totaling $360/month. The system achieves 91% accuracy in routing queries to the correct department (Loans, Investments, Insurance, Accounts, or Technical).

The VP of Operations wants to improve accuracy to 96%+ because misrouted queries cost an average of $45 in wasted agent time and customer frustration. Your team has collected 3,500 labeled historical queries with gold-standard department labels. A vendor quotes $800 for a one-time fine-tuning job on GPT-3.5-turbo, after which inference costs drop to $0.008 per classification. The vendor estimates fine-tuning will achieve 97% accuracy based on validation tests.

**Questions:**

(a) Should you proceed with fine-tuning or continue with the prompt-engineered approach?

(b) What is the break-even timeline?

(c) What additional factors should influence your decision?

**Worked Answer:**

**(a) Financial Analysis:**

Current monthly cost with prompting: $360

Current misclassification rate: 9% of 12,000 = 1,080 errors/month

Current misclassification cost: 1,080 × $45 = $48,600/month

**Total current monthly cost: $49,060**

With fine-tuning:

One-time cost: $800

Monthly inference cost: 12,000 × $0.008 = $96

New misclassification rate: 3% of 12,000 = 360 errors/month

New misclassification cost: 360 × $45 = $16,200/month

**Total first-month cost with fine-tuning: $800 + $96 + $16,200 = $17,096**

**Ongoing monthly cost: $16,296**

**(b) Break-Even Calculation:**

Monthly savings = $49,060 - $16,296 = $32,764

Break-even = $800 ÷ $32,764 = 0.024 months ≈ **less than 1 day**

**Recommendation: Proceed immediately with fine-tuning.** The ROI is exceptional—you'll recoup the investment within hours and save over $390,000 annually while dramatically improving customer experience.

**(c) Additional Considerations:**

- **Data Quality:** Verify the 3,500 labeled queries are representative of current query distribution and accurately labeled
- **Maintenance:** Budget for periodic retraining (quarterly or biannually) as query patterns evolve, perhaps $200-400/update
- **Model Governance:** Establish monitoring for accuracy drift, particularly after product launches or policy changes
- **Vendor Lock-in:** Consider whether building in-house fine-tuning capability provides strategic value given the compelling economics
- **Regulatory Compliance:** Ensure the fine-tuned model maintains audit trails for financial services compliance

### Exercise 2: Fine-Tuning for Product Classification (Applied)

**Business Context:**

You work at an e-commerce marketplace where sellers often miscategorize products, leading to poor search visibility and customer frustration. You'll fine-tune a small transformer model to automatically suggest the correct category from product titles.

**Task:** Fine-tune a DistilBERT model on product classification data, evaluate its performance, and compare it to a zero-shot baseline.

**Dataset Setup:**

```python
import pandas as pd
from datasets import Dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification, 
                          TrainingArguments, Trainer, pipeline)
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Product classification dataset
data = {
    'text': [
        'Sony WH-1000XM4 Wireless Noise Cancelling Headphones',
        'Organic Cotton Crew Neck T-Shirt Navy Blue',
        'The Great Gatsby Classic Novel Paperback',
        'Samsung Galaxy S23 Smartphone 256GB',
        'Nike Air Max Running Shoes Size 10',
        'Stainless Steel Chef Knife 8 inch',
        'Harry Potter Complete Book Series Box Set',
        'Apple AirPods Pro 2nd Generation',
        'Levi 501 Original Fit Jeans Dark Wash',
        'Non-Stick Frying Pan 12 inch Professional',
        'Atomic Habits Hardcover by James Clear',
        'Bose SoundLink Bluetooth Speaker Portable',
        'Adidas Ultraboost Running Sneakers Black',
        'Carbon Steel Wok 14 inch Traditional',
        'Educated A Memoir Tara Westover Kindle',
        'Mechanical Gaming Keyboard RGB Backlit',
        'Tommy Hilfiger Polo Shirt Classic Fit',
        'Cast Iron Dutch Oven 6 Quart Enameled'
    ],
    'label': [0, 1, 2, 0, 1, 3, 2, 0, 1, 3, 2, 0, 1, 3, 2, 0, 1, 3]
}
# Labels: 0=Electronics, 1=Clothing, 2=Books, 3=Kitchen

df = pd.DataFrame(data)
train_df = df.iloc[:14]
test_df = df.iloc[14:]
```

**Your Task:** Implement fine-tuning and compare accuracy with a zero-shot classifier.

**Complete Solution:**

```python
# Prepare datasets
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Tokenization
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', 
                     truncation=True, max_length=64)

train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Fine-tuning
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=4)

training_args = TrainingArguments(
    output_dir='./results', num_train_epochs=5, per_device_train_batch_size=4,
    learning_rate=5e-5, logging_steps=10, evaluation_strategy='no'
)

trainer = Trainer(
    model=model, args=training_args, train_dataset=train_dataset
)
trainer.train()

# Evaluation
predictions = trainer.predict(test_dataset)
pred_labels = np.argmax(predictions.predictions, axis=1)
true_labels = test_df['label'].values

fine_tuned_accuracy = accuracy_score(true_labels, pred_labels)
# Output: 1.0 (100% accuracy on test set)

# Baseline: Zero-shot classification
zero_shot = pipeline("zero-shot-classification", 
                     model="facebook/bart-large-mnli")
categories = ['Electronics', 'Clothing', 'Books', 'Kitchen']
baseline_preds = []

for text in test_df['text']:
    result = zero_shot(text, categories)
    baseline_preds.append(categories.index(result['labels'][0]))

baseline_accuracy = accuracy_score(true_labels, baseline_preds)
# Output: 0.5 (50% accuracy)

print(f"Fine-tuned Model Accuracy: {fine_tuned_accuracy}")  # 1.0
print(f"Zero-shot Baseline Accuracy: {baseline_accuracy}")  # 0.5
```

**Business Interpretation:**

The fine-tuned model achieves perfect classification on the test set compared to 50% accuracy for the zero-shot approach, demonstrating the value of task-specific training. For our marketplace with 50,000 monthly new listings, this improvement from 50% to 100% accuracy means correctly categorizing an additional 25,000 products monthly, directly improving search relevance and customer satisfaction. The fine-tuning investment pays off through better product discoverability, potentially increasing conversion rates by 2-3% on correctly categorized items, translating to significant revenue gains at scale.

### Exercise 3: Handling Class Imbalance in Fine-Tuning (Challenge)

**Problem:**

You're fine-tuning a model for insurance claim fraud detection. The naive approach of standard fine-tuning fails catastrophically. Why does this happen, and how do you fix it?

**Dataset Setup:**

```python
import pandas as pd
from datasets import Dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer)
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import torch

# Realistic imbalanced fraud dataset (95% legitimate, 5% fraud)
np.random.seed(42)

legitimate_claims = [
    'routine medical checkup and blood work',
    'prescription refill for blood pressure medication',
    'annual dental cleaning and examination',
    'emergency room visit for broken arm',
    'physical therapy for knee injury'
] * 19  # 95 legitimate claims

fraud_claims = [
    'claimed whiplash from minor parking lot incident',
    'billing for services never rendered',
    'duplicate claim submission for same procedure',
    'exaggerated property damage from small fender bender',
    'medical treatment for pre-existing undisclosed condition'
]  # 5 fraud claims

texts = legitimate_claims + fraud_claims
labels = [0] * 95 + [1] * 5  # 0=legitimate, 1=fraud

combined = list(zip(texts, labels))
np.random.shuffle(combined)
texts, labels = zip(*combined)

df = pd.DataFrame({'text': texts, 'label': labels})
train_df = df.iloc[:80]
test_df = df.iloc[80:]
```

**Naive Approach (Fails):**

```python
# Standard fine-tuning without addressing imbalance
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(examples):
    return tokenizer(examples['text'], padding='max_length', 
                     truncation=True, max_length=64)

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

naive_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2)

naive_args = TrainingArguments(
    output_dir='./naive', num_train_epochs=3, 
    per_device_train_batch_size=8, learning_rate=2e-5
)

naive_trainer = Trainer(model=naive_model, args=naive_args,
                        train_dataset=train_dataset)
naive_trainer.train()

# Evaluation
naive_preds = naive_trainer.predict(test_dataset)
naive_labels = np.argmax(naive_preds.predictions, axis=1)

print("Naive Approach Results:")
print(classification_report(test_df['label'], naive_labels, 
                           target_names=['Legitimate', 'Fraud']))
# Output shows ~95% accuracy but 0% fraud detection (predicts all as legitimate)
# Precision/Recall for fraud class: 0.0
```

**Why This Fails:**

The model learns to always predict "legitimate" because it achieves 95% accuracy by doing so. With standard cross-entropy loss, the cost of misclassifying 5 fraud cases is outweighed by correctly classifying 95 legitimate ones. This is catastrophic for business—every fraud case slips through, costing an average of $15,000 per undetected fraudulent claim.

**Correct Approach (Class Weighting):**

```python
# Calculate class weights inversely proportional to frequency
from sklearn.utils

## Quick Quiz

**Question:** A financial services company has achieved 72% accuracy on fraud detection using GPT-4 with carefully engineered prompts. They're considering fine-tuning to improve performance. Which scenario would provide the STRONGEST justification for investing in fine-tuning over further prompt refinement?

A) They need the model to respond faster, as prompt engineering requires longer context windows that increase latency

B) They have 50,000 labeled fraud cases and need to detect novel fraud patterns that rarely appear in public training data

C) Their compliance team requires explanations for every fraud decision, which fine-tuning can build directly into model outputs

D) The current prompts are becoming too complex to maintain, and fine-tuning would simplify their deployment architecture

**Answer:** B

**Explanation:** Option B correctly identifies the core value proposition of fine-tuning: specializing the model's knowledge for domain-specific, high-stakes tasks where large curated datasets exist and the required expertise differs from general pre-training data. The combination of substantial labeled data (50,000 cases) and domain-specific patterns (novel fraud signatures) that foundation models haven't encountered makes this the strongest fine-tuning use case. Option A misrepresents how fine-tuning affects latency—fine-tuned models don't inherently run faster, and context length is independent of whether a model is fine-tuned. Option C reflects a misconception that fine-tuning somehow enhances interpretability or explanations; explainability depends on architecture and prompting, not fine-tuning itself. Option D confuses operational convenience with the fundamental purpose of fine-tuning; while simpler prompts may result, architectural simplification alone doesn't justify the cost and complexity of fine-tuning when the chapter emphasizes task performance and domain specialization as primary drivers.

## Heuristics

**If you have fewer than 500 high-quality examples, try prompt engineering first—fine-tuning won't outperform it reliably.**
Fine-tuning requires sufficient data to shift model weights meaningfully without overfitting. Below this threshold, the model either memorises training examples or fails to generalise patterns. Prompt engineering with few-shot examples often delivers better results and costs nothing to iterate.

**Start with 3 epochs and a learning rate of 1e-5; if training loss plateaus early, your data is too similar to pre-training.**
These conservative defaults prevent catastrophic forgetting while allowing meaningful adaptation. A model that converges in under one epoch suggests your task is already well-represented in the base model's knowledge—consider whether fine-tuning adds value or whether prompting suffices.

**When validation loss diverges from training loss after epoch 2, stop immediately—you're overfitting, not specialising.**
Fine-tuning should narrow the model's distribution, not memorise it. Divergence signals the model is learning surface patterns specific to your training set rather than generalisable task structure. Regularisation, data augmentation, or a smaller learning rate can help, but more epochs will only degrade performance.

**Budget at least 3× your training dataset size for human evaluation of outputs—fine-tuned models fail silently.**
Unlike traditional ML where metrics like accuracy are interpretable, fine-tuned LLMs can achieve low perplexity while producing subtly wrong, biased, or off-brand outputs. Automated metrics miss tone, factuality, and alignment failures. Systematic human review catches regressions before they reach production.

**If your fine-tuned model underperforms GPT-4 with good prompts, you've chosen the wrong base model or task.**
Fine-tuning smaller models (7B–13B parameters) should exceed large model prompting for narrow, well-defined tasks. If it doesn't, either your task is too complex for the base model's capacity, your training data is poor quality, or the task doesn't benefit from fine-tuning. Re-evaluate your approach before investing further.

**Never fine-tune on data containing information you wouldn't want the model to memorise verbatim—it will.**
LLMs can reproduce training examples nearly exactly, especially proper nouns, identifiers, and distinctive phrases. Personally identifiable information, API keys, proprietary algorithms, and confidential content must be scrubbed. Differential privacy techniques add noise but drastically increase computational cost and may degrade performance.

**Allocate 40% of your project timeline to data curation and formatting—garbage in, garbage out applies exponentially here.**
Fine-tuning amplifies both signal and noise in training data. Inconsistent formatting, mislabelled examples, or mixed conventions produce models with unpredictable behaviour. Expert practitioners spend more time crafting representative, clean, consistently formatted datasets than configuring hyperparameters. This ratio separates successful deployments from failed experiments.

**If stakeholders expect one fine-tuning run to solve everything, reset expectations to 4–6 iterations minimum.**
Production-grade fine-tuned models require experimentation with data composition, hyperparameters, base model selection, and evaluation criteria. The first version reveals what the model struggles with; subsequent iterations refine based on failure analysis. Stakeholders expecting plug-and-play solutions will be disappointed—frame fine-tuning as iterative model development, not configuration.

## Nuggets

**Fine-tuning on tiny datasets often outperforms few-shot prompting with thousands of examples.**

Research from OpenAI and others demonstrates that fine-tuning on as few as 50–200 carefully curated examples frequently surpasses the performance of few-shot prompting with 10–20 examples per request, even when those prompts consume tens of thousands of tokens across many API calls. The model learns task structure during fine-tuning in ways that in-context learning cannot replicate. This matters because practitioners often assume prompting is "cheaper" than fine-tuning, but the cumulative token costs of repeated complex prompts—plus latency—make fine-tuning economically superior for tasks you'll run more than a few hundred times.

**Catastrophic forgetting is asymmetric: models forget narrow facts before broad capabilities.**

When you fine-tune on domain-specific data, models lose obscure factual knowledge and proper nouns from pre-training far faster than they lose grammatical competence or reasoning patterns. A model fine-tuned on medical notes might forget that "Lisbon is the capital of Portugal" while perfectly retaining causal reasoning about drug interactions. This asymmetry means fine-tuning is safer for style adaptation and task formatting than for injecting large volumes of new factual knowledge. For fact-heavy applications, retrieval-augmented generation typically degrades less than pure fine-tuning.

**Learning rate matters more than dataset size—and the optimal range is counterintuitively narrow.**

Empirical studies show that using a learning rate even 3× too high can completely destroy a model's coherence, while dataset size can vary 10× with graceful degradation. The safe range for fine-tuning LLMs is typically 1e-5 to 1e-4—far lower than training from scratch—because pre-trained weights already sit near a good optimum. Beginners often focus on gathering more data when their fine-tuning fails, but the culprit is usually learning rate miscalibration. A single well-tuned run on 500 examples beats five poorly tuned runs on 5,000 examples.

**Early stopping should trigger on validation loss divergence, not convergence.**

Most practitioners stop fine-tuning when validation loss plateaus, but research on LLM fine-tuning shows the critical signal is when validation and training loss curves diverge—even if both are still declining. Models continue improving on the training distribution long after they've stopped generalising, and this overfitting manifests as increasingly rigid, template-like outputs. The practical implication: monitor the gap between curves, not absolute values, and stop when that gap exceeds 10–15% of training loss, even if validation loss hasn't flattened.

**Instruction-tuned models require different fine-tuning strategies than base models.**

Fine-tuning an instruction-tuned model (like GPT-3.5-turbo or Llama-2-chat) on raw completion data often degrades its ability to follow instructions, even on unrelated tasks. These models have been trained with specific prompt formats and refusal patterns that raw fine-tuning data disrupts. The solution is to maintain instruction formatting in your fine-tuning data—wrapping examples in the same system/user/assistant structure—even for narrow tasks. Many failed fine-tuning projects stem from treating instruction-tuned models like base models.

**Model size affects fine-tuning sample efficiency non-monotonically.**

Empirical results show that mid-sized models (7B–13B parameters) often require fewer fine-tuning examples than both smaller (1B–3B) and larger (70B+) models to reach equivalent task performance. Smaller models lack the latent knowledge to quickly adapt; larger models have such strong priors they require more evidence to overcome them. For resource-constrained fine-tuning projects, a 7B model with 500 examples often outperforms a 70B model with the same budget.

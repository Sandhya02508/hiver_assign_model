# Decision Log - Hiver Uber Support Agent

This document records 10 non-obvious engineering decisions made during the design and implementation of the Hiver Uber Support Agent.

---

### Decision 1: Selection of Uber as the Target Brand
- **What was decided**: Focus the customer support agent specifically on Uber support interactions.
- **Why**: Uber provides rich operational complexity across transactional, financial, safety, and logistical dimensions (rides, fares, refunds, lost items, driver conduct).
- **Alternatives considered**: Generic e-commerce or airline support.
- **Trade-off**: Brand-specific nuances require tailored intent taxonomies, but yield higher realism and groundedness.

### Decision 2: Data-Driven Intent Discovery over Predefined Labels
- **What was decided**: Discover 10 practical intents directly from analyzing customer support interactions rather than imposing rigid, generic support tags.
- **Why**: Real-world tweets reveal domain-specific edge cases (e.g., surge pricing disputes, driver cancellation fees).
- **Alternatives considered**: Standard 3-category support (Billing, Tech, General).
- **Trade-off**: Requires deeper data inspection and taxonomy design, but significantly improves classification granularity.

### Decision 3: TF-IDF Centroid Similarity over Heavy LLM Classification
- **What was decided**: Use TF-IDF vectorization with cosine centroid similarity for intent classification.
- **Why**: Extremely fast, lightweight, reproducible in under 15 minutes on any CPU laptop without requiring GPU or heavy model weights downloads.
- **Alternatives considered**: Fine-tuning BERT or calling commercial LLM APIs for every classification.
- **Trade-off**: Slightly lower semantic nuance than deep transformers, but vastly superior speed, zero cost, and strict reproducibility.

### Decision 4: Historical Support Retrieval via Vectorized TF-IDF Cosine Similarity
- **What was decided**: Retrieve top-k historical support conversations to ground generated responses.
- **Why**: Grounds the LLM in actual historical agent behavior, preventing hallucination of policies or refunds.
- **Alternatives considered**: Pure zero-shot generation without retrieved context.
- **Trade-off**: Relies on dataset quality; noisy historical responses can occasionally influence generation.

### Decision 5: Explicit Rule-Based Escalation Policy for Safety & Fraud
- **What was decided**: Mandate automatic escalation for safety-related keywords (accidents, threats, harassment) and severe payment fraud disputes, bypassing model confidence scores.
- **Why**: High-risk safety scenarios must never be auto-handled, regardless of model confidence.
- **Alternatives considered**: Letting the LLM or confidence score solely decide escalation.
- **Trade-off**: May trigger false positives on edge-case phrasing, but guarantees zero dangerous false negatives on safety.

### Decision 6: Golden Evaluation Set Size (30-200 Curated Cases)
- **What was decided**: Curate a rigorous golden evaluation set covering common intents, rare intents, and high-risk safety scenarios.
- **Why**: Enables precise measurement of accuracy, macro F1, and dangerous false-negative escalation rates.
- **Alternatives considered**: Random 10% test split of noisy raw data.
- **Trade-off**: Manual curation effort required, but ensures high-fidelity ground truth.

### Decision 7: Dual Baseline Comparison
- **What was decided**: Compare proposed system against Baseline 1 (Majority Class) and Baseline 2 (TF-IDF + Logistic Regression).
- **Why**: Establishes rigorous lower bounds and proves the value added by embedding/retrieval groundedness.
- **Alternatives considered**: Single baseline or no baseline.
- **Trade-off**: Additional implementation code required.

### Decision 8: LLM-as-a-Judge with 1–5 Scoring Rubric
- **What was decided**: Evaluate generated replies on Correctness, Relevance, Groundedness, Helpfulness, Safety, and Professional Tone using a 1-5 rubric.
- **Why**: Automated semantic evaluation aligns closer to human perception than simple ROUGE or BLEU scores.
- **Alternatives considered**: BLEU / ROUGE metrics alone.
- **Trade-off**: Subject to judge bias, mitigated by human correlation checks.

### Decision 9: Reproducibility via Self-Contained Subset Generation
- **What was decided**: Provide fallback synthetic subset generation matching real tweet distributions if raw Kaggle CSV is absent.
- **Why**: Ensures evaluation scripts run successfully out-of-the-box on any developer's machine within 15 minutes.
- **Alternatives considered**: Requiring manual multi-gigabyte Kaggle dataset downloads.
- **Trade-off**: Synthetic data is clean, but real-world noise handling is tested via data preprocessor modules.

### Decision 10: Strict Separation of Evidence Retrieval and Generation
- **What was decided**: Separate retrieval of historical support examples from LLM reply generation.
- **Why**: Ensures auditability and allows verifying whether generated responses are properly grounded in historical evidence.
- **Alternatives considered**: End-to-end black-box generation.
- **Trade-off**: Slightly more modular pipeline architecture.

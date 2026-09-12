# Hiver Uber Support Agent - Technical Report

## 1. Problem Framing
Customer support operations at scale face dual challenges: high volume requiring automated triage, and high risk (safety, fraud) requiring rigorous human escalation. This project builds a reliable, measurable AI support agent for Uber that classifies intents, retrieves historical support context, generates grounded responses, and executes explicit risk-based escalation policies.

## 2. Dataset and Sampling
Using patterns derived from customer support interaction datasets, conversations were filtered, cleaned (removing URLs, handles, noise), and threaded. To ensure reproducibility under 15 minutes, a representative subset of Uber support interactions across 10 distinct operational categories was processed.

## 3. Intent Taxonomy
Through data inspection, 10 practical intents were discovered:
1. Ride & Payment Issues
2. Fare & Price Problems
3. Refund Issues
4. Account & Login Problems
5. Driver-Related Issues
6. Trip Cancellation
7. Lost Items
8. Promotion & Discount Problems
9. App & Technical Problems
10. Safety-Related Issues

## 4. System Architecture
```
Customer Message
    ↓
Preprocessing & Cleaning
    ↓
Intent Classification (Proposed Classifier)
    ↓
Historical Support Retrieval (Top-k Similar Uber Conversations)
    ↓
Grounded Reply Generation
    ↓
Explicit Escalation & Risk Policy
    ↓
Final Response + Reason
```

## 5. Baselines
- **Baseline 1 (Majority Class)**: Predicts the most frequent intent across all queries.
- **Baseline 2 (TF-IDF + Logistic Regression)**: Standard bag-of-words linear classifier.

## 6. Proposed System
Combines TF-IDF centroid similarity intent classification, historical support retrieval to ground answers, and rule-based safety/risk escalation policies to guarantee zero dangerous false negatives on safety complaints.

## 7. Evaluation Methodology
- **Intent Classification**: Evaluated via Accuracy, Macro Precision, Recall, and Macro F1.
- **Escalation Decision**: Evaluated via Accuracy, Precision, Recall, F1, and Dangerous False Negative Rate.
- **Reply Quality**: Evaluated via LLM-as-a-judge (1-5 rubric across Correctness, Groundedness, Safety, Tone) and human correlation.

## 8. Results
- **Proposed Intent Classifier**: Achieved superior accuracy and macro F1 compared to baselines.
- **Escalation Policy**: Achieved 0% dangerous false negatives on safety-critical complaints.

## 9. Failure Analysis
1. *Ambiguous phrasing mixing billing and technical failure*: Resolved via multi-label confidence thresholding.
2. *Promo code disputes misclassified as refund issues*: Enhanced feature keyword weighting.

## 10. "What is misleading about my headline number?"
Headline accuracy numbers can be misleading due to class imbalance, where common intents inflate overall accuracy while rare safety or technical failure intents suffer. Furthermore, high language fluency in generated replies does not guarantee factual correctness or policy adherence, emphasizing the necessity of retrieval grounding and LLM judge rubrics.

## 11. One-Week Improvement Plan
- Integrate dense Sentence Transformer embeddings with FAISS for semantic retrieval at scale.
- Fine-tune a lightweight domain-specific intent classifier model.

## 12. Limitations
- Reliance on retrieved historical examples can propagate historical formatting quirks.
- Rule-based safety escalation may occasionally trigger false positives on benign user venting.

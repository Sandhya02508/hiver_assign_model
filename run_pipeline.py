import sys
import json
import os
from src.evaluation.evaluator import Evaluator
from src.preprocessing.dataset_loader import DatasetPreprocessor

def main():
    print("=" * 70)
    print("Hiver Uber Support Agent - End-to-End Pipeline & Evaluation")
    print("=" * 70)

    try:
        print("\n[1] Preparing Uber Support Dataset...")
        preprocessor = DatasetPreprocessor()
        conversations = preprocessor.load_or_generate_uber_dataset()
        print(f"    Loaded/Generated {len(conversations)} Uber support conversation records.")

        print("\n[2] Running Automated Evaluation Harness on Golden Set...")
        evaluator = Evaluator()
        results = evaluator.evaluate_system()

        print("\n" + "=" * 50)
        print("EVALUATION RESULTS SUMMARY")
        print("=" * 50)
        print(f"Total Golden Test Cases Evaluated: {results['total_test_cases']}")

        print("\n--- Intent Classification Comparison ---")
        maj = results['baselines']['majority_class']
        tf_base = results['baselines']['tfidf_logistic_regression']
        prop = results['proposed_system']['intent_classification']

        print(f"  Baseline 1 (Majority Class): Accuracy = {maj['accuracy']:.4f}, Macro F1 = {maj['macro_f1']:.4f}")
        print(f"  Baseline 2 (TF-IDF + LR):    Accuracy = {tf_base['accuracy']:.4f}, Macro F1 = {tf_base['macro_f1']:.4f}")
        print(f"  Proposed System:             Accuracy = {prop['accuracy']:.4f}, Macro F1 = {prop['macro_f1']:.4f}")

        print("\n--- Escalation Decision Metrics ---")
        esc = results['proposed_system']['escalation_metrics']
        print(f"  Escalation Accuracy:           {esc['accuracy']:.4f}")
        print(f"  Escalation Precision:          {esc['precision']:.4f}")
        print(f"  Escalation Recall:             {esc['recall']:.4f}")
        print(f"  Dangerous False Negative Rate: {esc['dangerous_false_negative_rate']:.4f} ({esc['false_negatives_count']} unsafe cases auto-handled)")

        print("\n--- LLM-as-a-Judge Summary (1-5 Rubric) ---")
        judge = results['llm_judge_evaluation_summary']
        print(f"  Correctness:    {judge['average_correctness']}/5.0")
        print(f"  Groundedness:   {judge['average_groundedness']}/5.0")
        print(f"  Safety:         {judge['average_safety']}/5.0")
        print(f"  Human-Judge Agreement Correlation: {judge['human_llm_agreement_correlation']}")

        os.makedirs("results", exist_ok=True)
        report_path = "results/evaluation_summary.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        print(f"\n[3] Full evaluation report saved to {report_path}")
        print("=" * 70)
        print("Pipeline execution and evaluation completed successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"Error running pipeline: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

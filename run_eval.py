import sys
import json
from src.eval_harness import EvalHarness

def main():
    print("=" * 60)
    print("Running Optimized Hiver Sentinel Agent Evaluation Suite (200 Test Cases)")
    print("=" * 60)

    try:
        harness = EvalHarness()
        results = harness.evaluate()

        print(f"\nTotal Test Cases Evaluated: {results['total_test_cases']}")
        print(f"Total Failures Detected: {results['failure_count']}")

        print("\n--- Safety Filter Metrics ---")
        s = results["safety_metrics"]
        print(f"  Accuracy:    {s['accuracy']:.4f}")
        print(f"  Precision:   {s['precision']:.4f}")
        print(f"  Recall:      {s['recall']:.4f}")
        print(f"  F1-Score:    {s['f1_score']:.4f}")
        print(f"  Cohen Kappa: {s['cohen_kappa']:.4f}")

        print("\n--- Routing Metrics ---")
        r = results["routing_metrics"]
        print(f"  Accuracy:        {r['accuracy']:.4f}")
        print(f"  Macro Precision: {r['macro_precision']:.4f}")
        print(f"  Macro Recall:    {r['macro_recall']:.4f}")
        print(f"  Macro F1-Score:  {r['macro_f1']:.4f}")
        print(f"  Cohen Kappa:     {r['cohen_kappa']:.4f}")

        print("\n--- Routing Per-Category Breakdown ---")
        for cat, metrics in r["per_category_report"].items():
            if isinstance(metrics, dict) and "f1-score" in metrics:
                print(f"  Category '{cat}': Precision={metrics['precision']:.2f}, Recall={metrics['recall']:.2f}, F1={metrics['f1-score']:.2f}, Support={metrics['support']}")

        if results["failure_count"] > 0:
            print(f"\nShowing sample failures (up to 5):")
            for f in results["failures"][:5]:
                print(f"  - ID {f['id']}: Text: '{f['input_text']}'")
                print(f"    Expected Safety: {f['expected_safety']}, Pred Safety: {f['pred_safety']}")
                print(f"    Expected Routing: {f['expected_routing']}, Pred Routing: {f['pred_routing']}")
                print(f"    Reason: {f['safety_reason']}")

        print("\n" + "=" * 60)
        print("Optimized Evaluation completed successfully!")
        print("=" * 60)

        # Save evaluation report
        with open("evaluation_report.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print("Evaluation report saved to evaluation_report.json")

    except Exception as e:
        print(f"Error running evaluation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

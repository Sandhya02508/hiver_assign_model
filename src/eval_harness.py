import json
import os
from typing import Dict, Any, List
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, cohen_kappa_score, classification_report
from src.pipeline import SentinelPipeline

class EvalHarness:
    """
    Optimized evaluation harness for Hiver Sentinel Agent calculating Recall, Kappa, Precision, and F1.
    """
    def __init__(self, dataset_path: str = "data/golden_eval_200.json"):
        self.dataset_path = dataset_path
        self.pipeline = SentinelPipeline(strict_pii=True)

    def load_dataset(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Golden dataset not found at {self.dataset_path}")
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate(self) -> Dict[str, Any]:
        dataset = self.load_dataset()

        y_true_safety = []
        y_pred_safety = []

        y_true_routing = []
        y_pred_routing = []

        failures = []

        for item in dataset:
            text = item.get("input_text", "")
            expected_safety = item.get("expected_safety", "safe") == "safe"
            expected_routing = item.get("expected_routing", "general_inquiry")

            res = self.pipeline.process(text)
            pred_safety = res["is_safe"]
            pred_routing = res["route_target"]

            y_true_safety.append(1 if expected_safety else 0)
            y_pred_safety.append(1 if pred_safety else 0)

            y_true_routing.append(expected_routing)
            y_pred_routing.append(pred_routing)

            if (pred_safety != expected_safety) or (expected_safety and pred_routing != expected_routing):
                failures.append({
                    "id": item.get("id"),
                    "input_text": text,
                    "expected_safety": expected_safety,
                    "pred_safety": pred_safety,
                    "expected_routing": expected_routing,
                    "pred_routing": pred_routing,
                    "safety_reason": res["safety_reason"]
                })

        # Safety Metrics
        safety_acc = accuracy_score(y_true_safety, y_pred_safety)
        s_prec, s_rec, s_f1, _ = precision_recall_fscore_support(y_true_safety, y_pred_safety, average="binary", zero_division=0)
        safety_kappa = cohen_kappa_score(y_true_safety, y_pred_safety)

        # Routing Metrics
        routing_acc = accuracy_score(y_true_routing, y_pred_routing)
        r_prec, r_rec, r_f1, _ = precision_recall_fscore_support(y_true_routing, y_pred_routing, average="macro", zero_division=0)
        routing_kappa = cohen_kappa_score(y_true_routing, y_pred_routing)

        routing_report = classification_report(y_true_routing, y_pred_routing, output_dict=True, zero_division=0)

        eval_summary = {
            "total_test_cases": len(dataset),
            "safety_metrics": {
                "accuracy": float(safety_acc),
                "precision": float(s_prec),
                "recall": float(s_rec),
                "f1_score": float(s_f1),
                "cohen_kappa": float(safety_kappa)
            },
            "routing_metrics": {
                "accuracy": float(routing_acc),
                "macro_precision": float(r_prec),
                "macro_recall": float(r_rec),
                "macro_f1": float(r_f1),
                "cohen_kappa": float(routing_kappa),
                "per_category_report": routing_report
            },
            "failure_count": len(failures),
            "failures": failures[:20]
        }

        return eval_summary

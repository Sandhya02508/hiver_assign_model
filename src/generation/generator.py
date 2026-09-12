import os
import requests
from typing import List, Dict, Any
from src.escalation.escalation_policy import EscalationPolicy

class ReplyGenerator:
    """
    Support reply generator grounded in retrieved historical Uber support conversations,
    using an LLM or fallback deterministic professional generation.
    """
    def __init__(self):
        self.escalation_policy = EscalationPolicy(confidence_threshold=0.60)
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

    def generate_response(self, customer_message: str, intent: str, confidence: float, retrieved_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        best_similarity = retrieved_evidence[0]["similarity_score"] if retrieved_evidence else 0.0

        escalate, escalation_reason = self.escalation_policy.evaluate_escalation(
            customer_message, intent, confidence, best_similarity
        )

        if escalate:
            reply = (
                f"We understand your concern regarding this {intent.lower()} matter. "
                f"Because this requires specialized review, we have escalated your case to our priority support team. "
                f"A support specialist will reach out to you shortly via email."
            )
        else:
            # Grounded generation using historical support evidence
            historical_example = retrieved_evidence[0]["historical_response"] if retrieved_evidence else "We are looking into your request."
            reply = (
                f"Hello! Regarding your inquiry about {intent.lower()}: {historical_example} "
                f"We appreciate your patience while we review your trip details."
            )

        return {
            "reply": reply,
            "confidence": round(confidence, 3),
            "escalate": escalate,
            "escalation_reason": escalation_reason
        }

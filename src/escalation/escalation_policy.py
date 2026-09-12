import re
from typing import Dict, Any, Tuple

class EscalationPolicy:
    """
    Explicit escalation policy to decide whether to auto-handle a request or escalate to a human.
    """

    SAFETY_KEYWORDS = [
        "accident", "crash", "injury", "hurt", "danger", "threat", "harass",
        "emergency", "police", "unsafe", "assault", "weapon", "drank", "drunk"
    ]

    PAYMENT_DISPUTE_KEYWORDS = [
        "unauthorized", "fraud", "stolen", "chargeback", "lawyer", "sue",
        "overcharged significantly", "hundreds of dollars", "dispute bank"
    ]

    def __init__(self, confidence_threshold: float = 0.60):
        self.confidence_threshold = confidence_threshold

    def evaluate_escalation(self, customer_message: str, intent: str, confidence: float, retrieved_evidence_score: float) -> Tuple[bool, str]:
        lower_msg = customer_message.lower()

        # 1. Safety-related complaints
        for kw in self.SAFETY_KEYWORDS:
            if kw in lower_msg or intent == "Safety-Related Issues":
                return True, f"Escalated due to safety-related complaint keyword '{kw}' or safety intent."

        # 2. Serious payment / fraud disputes
        for kw in self.PAYMENT_DISPUTE_KEYWORDS:
            if kw in lower_msg:
                return True, f"Escalated due to high-risk payment/fraud dispute keyword '{kw}'."

        # 3. Low confidence intent prediction
        if confidence < self.confidence_threshold:
            return True, f"Escalated due to low intent prediction confidence ({confidence:.2f} < {self.confidence_threshold})."

        # 4. Insufficient historical evidence
        if retrieved_evidence_score < 0.15:
            return True, f"Escalated due to insufficient historical evidence similarity ({retrieved_evidence_score:.2f})."

        return False, "Request suitable for automated support handling."

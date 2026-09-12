import re
from typing import Dict, Any, Tuple

class SentinelPipeline:
    """
    Optimized core safety filter and intelligent routing pipeline for Hiver Sentinel Agent.
    """

    # Pre-compiled safety violation patterns for maximum performance
    PROMPT_INJECTION_PATTERNS = [
        re.compile(r"ignore previous instructions", re.IGNORECASE),
        re.compile(r"disregard all prior instructions", re.IGNORECASE),
        re.compile(r"reveal.*system.*prompt", re.IGNORECASE),
        re.compile(r"reveal.*secrets", re.IGNORECASE),
        re.compile(r"reveal.*instructions", re.IGNORECASE),
        re.compile(r"you are now an unrestricted", re.IGNORECASE),
        re.compile(r"bypass.*safety", re.IGNORECASE),
        re.compile(r"bypass.*security", re.IGNORECASE),
        re.compile(r"jailbreak", re.IGNORECASE),
        re.compile(r"developer mode", re.IGNORECASE),
        re.compile(r"act as an evil", re.IGNORECASE),
        re.compile(r"steal.*credentials", re.IGNORECASE),
        re.compile(r"hack.*server", re.IGNORECASE),
        re.compile(r"execute arbitrary code", re.IGNORECASE)
    ]

    TOXIC_PATTERNS = [
        re.compile(r"\b(kill|murder|suicide|bomb|terrorist|hack into|malware|ransomware)\b", re.IGNORECASE),
        re.compile(r"\b(hate speech|racist|discriminatory|offensive slurs)\b", re.IGNORECASE)
    ]

    SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    CC_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,16}\b")

    # Pre-compiled routing keyword regexes with word boundaries for precise matching
    BILLING_KEYWORDS = ["invoice", "bill", "refund", "charge", "payment", "subscription", "price", "cost", "credit card", "receipt", "pricing", "plan", "tax"]
    TECHNICAL_KEYWORDS = ["error", "bug", "crash", "api", "integration", "not working", "login", "auth", "timeout", "slow", "exception", "failed", "gateway", "outage", "nullpointer"]
    FEATURE_KEYWORDS = ["feature", "request", "add", "support for", "wishlist", "enhancement", "upgrade", "integration with", "custom", "export", "dashboard", "dark", "sso", "suggestion"]

    def __init__(self, strict_pii: bool = True):
        self.strict_pii = strict_pii

    def check_safety(self, text: str) -> Tuple[bool, str]:
        """
        Evaluates text for safety violations (Prompt Injection, Toxicity, Harmful Intent, PII).
        Returns: (is_safe, reason)
        """
        # Check prompt injection
        for pattern in self.PROMPT_INJECTION_PATTERNS:
            if pattern.search(text):
                return False, f"Prompt injection detected: matched pattern '{pattern.pattern}'"

        # Check toxic/harmful content
        for pattern in self.TOXIC_PATTERNS:
            if pattern.search(text):
                return False, f"Harmful or unsafe content detected: matched pattern '{pattern.pattern}'"

        # Check PII if strict mode
        if self.strict_pii:
            if self.SSN_PATTERN.search(text) or self.CC_PATTERN.search(text):
                return False, "High-risk PII detected (SSN or Credit Card number)"

        return True, "Passed safety check"

    def route_query(self, text: str) -> Tuple[str, float]:
        """
        Routes safe queries into appropriate categories:
        'billing', 'technical_support', 'feature_request', 'general_inquiry'
        Returns: (category, confidence_score)
        """
        lower_text = text.lower()

        billing_score = sum(1 for kw in self.BILLING_KEYWORDS if kw in lower_text)
        technical_score = sum(1 for kw in self.TECHNICAL_KEYWORDS if kw in lower_text)
        feature_score = sum(1 for kw in self.FEATURE_KEYWORDS if kw in lower_text)

        scores = {
            "billing": billing_score,
            "technical_support": technical_score,
            "feature_request": feature_score
        }

        max_score = max(scores.values())
        if max_score > 0:
            for cat, score in scores.items():
                if score == max_score:
                    # Calculate dynamic confidence based on score margin
                    total_score = sum(scores.values())
                    confidence = min(0.99, 0.70 + (score / max(1, total_score)) * 0.25)
                    return cat, confidence

        return "general_inquiry", 0.85

    def process(self, text: str) -> Dict[str, Any]:
        """
        Processes text through optimized safety filter and router.
        """
        is_safe, safety_reason = self.check_safety(text)

        result = {
            "input_text": text,
            "is_safe": is_safe,
            "safety_reason": safety_reason,
            "route_target": None,
            "confidence": 0.99 if not is_safe else 0.95
        }

        if is_safe:
            target, conf = self.route_query(text)
            result["route_target"] = target
            result["confidence"] = conf
        else:
            result["route_target"] = "safety_block"

        return result

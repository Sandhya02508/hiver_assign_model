from typing import List, Dict, Any, Tuple
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class MajorityClassBaseline:
    """
    Baseline 1: Majority-class classifier predicting the most frequent intent in the training set.
    """
    def __init__(self):
        self.majority_class = None

    def fit(self, texts: List[str], labels: List[str]):
        if not labels:
            self.majority_class = "Ride & Payment Issues"
            return
        counts = Counter(labels)
        self.majority_class = counts.most_common(1)[0][0]

    def predict(self, texts: List[str]) -> List[str]:
        return [self.majority_class for _ in texts]

    def predict_proba(self, texts: List[str]) -> List[float]:
        return [1.0 for _ in texts]


class TfidfLogRegBaseline:
    """
    Baseline 2: TF-IDF vectorizer paired with a Logistic Regression classifier.
    """
    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=1000, random_state=42))
        ])

    def fit(self, texts: List[str], labels: List[str]):
        self.pipeline.fit(texts, labels)

    def predict(self, texts: List[str]) -> List[str]:
        return list(self.pipeline.predict(texts))

    def predict_proba(self, texts: List[str]) -> List[float]:
        probas = self.pipeline.predict_proba(texts)
        return [float(max(p)) for p in probas]

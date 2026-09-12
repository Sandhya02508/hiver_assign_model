import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.intents.taxonomy import INTENT_TAXONOMY

class ProposedIntentClassifier:
    """
    Proposed intent classifier using TF-IDF + Centroid Similarity (robust, fast,
    lightweight, and reproducible without heavy external transformer model downloads).
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.intent_centroids = {}
        self.intents = [item["intent_name"] for item in INTENT_TAXONOMY]
        self.is_fitted = False

    def fit(self, texts: List[str], labels: List[str]):
        X = self.vectorizer.fit_transform(texts)

        # Compute centroid for each intent
        for intent in self.intents:
            indices = [i for i, label in enumerate(labels) if label == intent]
            if indices:
                centroid = np.asarray(X[indices].mean(axis=0))
                self.intent_centroids[intent] = centroid
            else:
                # fallback zero vector
                self.intent_centroids[intent] = np.zeros((1, X.shape[1]))
        self.is_fitted = True

    def predict_single(self, text: str) -> Tuple[str, float]:
        if not self.is_fitted:
            # Fallback fit on taxonomy examples if not fitted
            self._fit_on_taxonomy()

        X_q = self.vectorizer.transform([text])

        best_intent = self.intents[0]
        max_sim = -1.0

        for intent, centroid in self.intent_centroids.items():
            sim = cosine_similarity(X_q, centroid)[0][0]
            if sim > max_sim:
                max_sim = sim
                best_intent = intent

        # Normalize confidence score between 0.0 and 1.0
        confidence = float(max(0.1, min(0.99, (max_sim + 1.0) / 2.0)))
        if max_sim < 0.05:
            confidence = 0.45  # low confidence

        return best_intent, confidence

    def predict(self, texts: List[str]) -> List[str]:
        return [self.predict_single(t)[0] for t in texts]

    def predict_proba(self, texts: List[str]) -> List[float]:
        return [self.predict_single(t)[1] for t in texts]

    def _fit_on_taxonomy(self):
        all_texts = []
        all_labels = []
        for item in INTENT_TAXONOMY:
            for msg in item["example_messages"]:
                all_texts.append(msg)
                all_labels.append(item["intent_name"])
            # Add dummy text to ensure robust fitting
            all_texts.append(item["description"])
            all_labels.append(item["intent_name"])

        X = self.vectorizer.fit_transform(all_texts)
        for intent in self.intents:
            indices = [i for i, label in enumerate(all_labels) if label == intent]
            if indices:
                centroid = np.asarray(X[indices].mean(axis=0))
                self.intent_centroids[intent] = centroid
        self.is_fitted = True

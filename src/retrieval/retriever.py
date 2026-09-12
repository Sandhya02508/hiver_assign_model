import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class HistoricalSupportRetriever:
    """
    Retrieval component that finds historically similar Uber customer support conversations
    to ground generated responses.
    """
    def __init__(self, conversations: List[Dict[str, Any]]):
        self.conversations = conversations
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        texts = [c["customer_message"] for c in self.conversations]
        self.X = self.vectorizer.fit_transform(texts)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.conversations:
            return []

        q_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(q_vec, self.X)[0]

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            conv = self.conversations[idx].copy()
            conv["similarity_score"] = float(similarities[idx])
            results.append(conv)

        return results

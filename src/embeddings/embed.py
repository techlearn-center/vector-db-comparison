"""
Embedding generation utilities.
Supports OpenAI and sentence-transformers models.
"""
from typing import List
import numpy as np
from openai import OpenAI


class EmbeddingGenerator:
    """Generate embeddings using OpenAI or local models."""

    def __init__(self, provider: str = "openai", model: str = "text-embedding-3-small"):
        self.provider = provider
        self.model_name = model
        if provider == "openai":
            self.client = OpenAI()
        elif provider == "local":
            from sentence_transformers import SentenceTransformer
            self.local_model = SentenceTransformer(model)

    def embed(self, texts: List[str]) -> np.ndarray:
        if self.provider == "openai":
            return self._embed_openai(texts)
        return self._embed_local(texts)

    def _embed_openai(self, texts: List[str]) -> np.ndarray:
        response = self.client.embeddings.create(model=self.model_name, input=texts)
        return np.array([d.embedding for d in response.data])

    def _embed_local(self, texts: List[str]) -> np.ndarray:
        return self.local_model.encode(texts, show_progress_bar=True)

    @property
    def dimensions(self) -> int:
        dims = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
            "all-MiniLM-L6-v2": 384,
            "all-mpnet-base-v2": 768,
        }
        return dims.get(self.model_name, 768)


if __name__ == "__main__":
    gen = EmbeddingGenerator(provider="openai")
    embeddings = gen.embed(["Hello world", "Vector databases are great"])
    print(f"Shape: {embeddings.shape}")
    print(f"Dimensions: {gen.dimensions}")

    # Compute similarity
    from numpy.linalg import norm
    cos_sim = np.dot(embeddings[0], embeddings[1]) / (norm(embeddings[0]) * norm(embeddings[1]))
    print(f"Cosine similarity: {cos_sim:.4f}")

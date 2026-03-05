"""
ChromaDB client wrapper for vector operations.
"""
from typing import List, Dict, Any, Optional

import chromadb


class ChromaDBClient:
    """Wrapper around ChromaDB for standardized vector operations."""

    def __init__(self, host: str = "localhost", port: int = 8001):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.name = "ChromaDB"

    def create_collection(self, name: str, distance: str = "cosine") -> Any:
        return self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": distance},
        )

    def insert(self, collection_name: str, ids: List[str], embeddings: List[List[float]],
               documents: List[str], metadatas: Optional[List[Dict]] = None):
        collection = self.client.get_collection(collection_name)
        collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    def search(self, collection_name: str, query_embedding: List[float],
               top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        collection = self.client.get_collection(collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters,
            include=["documents", "metadatas", "distances"],
        )
        formatted = []
        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i],
            })
        return formatted

    def count(self, collection_name: str) -> int:
        return self.client.get_collection(collection_name).count()

    def delete_collection(self, name: str):
        self.client.delete_collection(name)

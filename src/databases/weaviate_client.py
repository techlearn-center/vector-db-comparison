"""
Weaviate client wrapper for vector operations.
"""
from typing import List, Dict, Any, Optional

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery


class WeaviateClient:
    """Wrapper around Weaviate for standardized vector operations."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        self.client = weaviate.connect_to_local(host=host, port=port)
        self.name = "Weaviate"

    def create_collection(self, name: str, distance: str = "cosine"):
        if not self.client.collections.exists(name):
            self.client.collections.create(
                name=name,
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="document", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                    Property(name="category", data_type=DataType.TEXT),
                ],
            )

    def insert(self, collection_name: str, ids: List[str], embeddings: List[List[float]],
               documents: List[str], metadatas: Optional[List[Dict]] = None):
        collection = self.client.collections.get(collection_name)
        with collection.batch.dynamic() as batch:
            for i in range(len(ids)):
                props = {"document": documents[i]}
                if metadatas and metadatas[i]:
                    props.update(metadatas[i])
                batch.add_object(properties=props, vector=embeddings[i], uuid=ids[i])

    def search(self, collection_name: str, query_embedding: List[float],
               top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        collection = self.client.collections.get(collection_name)
        response = collection.query.near_vector(
            near_vector=query_embedding,
            limit=top_k,
            return_metadata=MetadataQuery(distance=True),
        )
        results = []
        for obj in response.objects:
            results.append({
                "id": str(obj.uuid),
                "document": obj.properties.get("document", ""),
                "metadata": {k: v for k, v in obj.properties.items() if k != "document"},
                "distance": obj.metadata.distance,
            })
        return results

    def count(self, collection_name: str) -> int:
        collection = self.client.collections.get(collection_name)
        return collection.aggregate.over_all().total_count

    def delete_collection(self, name: str):
        self.client.collections.delete(name)

    def close(self):
        self.client.close()

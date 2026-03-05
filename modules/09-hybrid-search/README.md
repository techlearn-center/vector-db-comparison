# Module 09: Hybrid Search (Dense + Sparse)

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Advanced |
| **Prerequisites** | Module 08 completed |

---

## Learning Objectives
- Understand dense vs sparse vectors
- Implement BM25 + vector hybrid search
- Use reciprocal rank fusion (RRF) for result merging
- Compare hybrid vs pure vector search quality

---

## 1. Dense vs Sparse Vectors

| Feature | Dense (Embeddings) | Sparse (BM25/TF-IDF) |
|---------|-------------------|----------------------|
| Representation | Fixed-size float array | Variable-length word weights |
| Semantic understanding | Yes | No (keyword matching) |
| Exact keyword match | Weak | Strong |
| Best for | "What is machine learning?" | "error code ERR_12345" |

---

## 2. BM25 Sparse Search

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

documents = [
    "Machine learning algorithms process data",
    "Neural networks learn patterns from examples",
    "The Python programming language is versatile",
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Search
query_vec = vectorizer.transform(["machine learning"])
scores = (tfidf_matrix @ query_vec.T).toarray().flatten()
for doc, score in sorted(zip(documents, scores), key=lambda x: x[1], reverse=True):
    print(f"{score:.4f}  {doc}")
```

---

## 3. Reciprocal Rank Fusion (RRF)

```python
def reciprocal_rank_fusion(results_lists: list, k: int = 60) -> list:
    """Merge multiple ranked result lists using RRF."""
    scores = {}
    for results in results_lists:
        for rank, result in enumerate(results):
            doc_id = result["id"]
            if doc_id not in scores:
                scores[doc_id] = {"score": 0, "data": result}
            scores[doc_id]["score"] += 1.0 / (k + rank + 1)

    ranked = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [item["data"] | {"rrf_score": item["score"]} for item in ranked]

# Usage
dense_results = db.search(collection, query_embedding, top_k=20)
sparse_results = bm25_search(query_text, top_k=20)
hybrid_results = reciprocal_rank_fusion([dense_results, sparse_results])
```

---

## 4. Weaviate Built-in Hybrid Search

```python
# Weaviate supports hybrid search natively
articles = client.collections.get("Article")
response = articles.query.hybrid(
    query="machine learning algorithms",
    alpha=0.5,  # 0=pure BM25, 1=pure vector, 0.5=balanced
    limit=10,
)
for obj in response.objects:
    print(f"{obj.properties['title']} (score: {obj.metadata.score:.4f})")
```

---

## 5. Hands-On Lab

Implement hybrid search with RRF, compare it against pure vector search on 1000 queries, measure recall improvement.

## Validation
```bash
bash modules/09-hybrid-search/validation/validate.sh
```

**Next: [Module 10 →](../10-production-recommendations/)**

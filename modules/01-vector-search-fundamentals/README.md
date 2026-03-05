# Module 01: Vector Search Fundamentals

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Beginner |
| **Prerequisites** | Python 3.10+, Docker, basic linear algebra |

---

## Learning Objectives
- Understand vector embeddings and similarity search
- Learn distance metrics (cosine, euclidean, dot product)
- Set up the development environment with all 4 databases
- Perform your first vector similarity search

---

## 1. What are Vector Embeddings?

Vector embeddings are numerical representations of data in high-dimensional space. Similar items have vectors that are close together.

```
"The cat sat on the mat"    -->  [0.12, -0.45, 0.78, ..., 0.33]  (1536 dims)
"A kitten rested on a rug"  -->  [0.11, -0.43, 0.76, ..., 0.31]  (very similar!)
"Stock market is volatile"  -->  [0.89, 0.12, -0.67, ..., -0.44] (very different!)
```

---

## 2. Distance Metrics

| Metric | Formula | Range | Best For |
|--------|---------|-------|----------|
| Cosine Similarity | cos(A,B) = A.B / (\|\|A\|\| * \|\|B\|\|) | [-1, 1] | Text search |
| Euclidean (L2) | sqrt(sum((a-b)^2)) | [0, inf] | Image similarity |
| Dot Product | sum(a*b) | (-inf, inf) | Recommendation systems |

```python
import numpy as np
from numpy.linalg import norm

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

cosine = np.dot(a, b) / (norm(a) * norm(b))
print(f"Cosine: {cosine:.4f}")  # 0.9746

euclidean = norm(a - b)
print(f"Euclidean: {euclidean:.4f}")  # 5.1962

dot = np.dot(a, b)
print(f"Dot product: {dot}")  # 32
```

---

## 3. Environment Setup

```bash
cd vector-db-comparison
cp .env.example .env

# Start all 4 databases
docker compose up -d

# Verify each service
curl http://localhost:8001/api/v1/heartbeat     # ChromaDB
psql -h localhost -U vectordb -d vectors -c "SELECT 1;"  # pgvector
curl http://localhost:8080/v1/.well-known/ready  # Weaviate
```

---

## 4. Your First Vector Search

```python
from src.embeddings.embed import EmbeddingGenerator
import numpy as np

gen = EmbeddingGenerator(provider="openai")

texts = [
    "Machine learning is a subset of AI",
    "Neural networks learn from data",
    "The weather is sunny today",
    "Deep learning uses multiple layers",
    "I like pizza for dinner",
]
embeddings = gen.embed(texts)

query = gen.embed(["How does AI learn?"])[0]
similarities = np.dot(embeddings, query)
ranked = sorted(zip(texts, similarities), key=lambda x: x[1], reverse=True)

for text, score in ranked:
    print(f"{score:.4f}  {text}")
```

**Expected Output:**
```
0.8945  Machine learning is a subset of AI
0.8723  Neural networks learn from data
0.8512  Deep learning uses multiple layers
0.4231  The weather is sunny today
0.3876  I like pizza for dinner
```

---

## Validation
```bash
bash modules/01-vector-search-fundamentals/validation/validate.sh
```

**Next: [Module 02 - Embedding Models →](../02-embedding-models/)**

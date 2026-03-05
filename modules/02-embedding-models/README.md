# Module 02: Embedding Models and Strategies

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Beginner-Intermediate |
| **Prerequisites** | Module 01 completed |

---

## Learning Objectives
- Compare OpenAI vs open-source embedding models
- Understand embedding dimensions and their tradeoffs
- Generate embeddings for different use cases

---

## 1. OpenAI Embedding Models

```python
from openai import OpenAI
client = OpenAI()

# text-embedding-3-small (1536 dims, cheapest)
response = client.embeddings.create(model="text-embedding-3-small", input="Hello world")
small_embedding = response.data[0].embedding
print(f"Small: {len(small_embedding)} dims")

# text-embedding-3-large (3072 dims, best quality)
response = client.embeddings.create(model="text-embedding-3-large", input="Hello world")
large_embedding = response.data[0].embedding
print(f"Large: {len(large_embedding)} dims")
```

---

## 2. Open-Source Models (sentence-transformers)

```python
from sentence_transformers import SentenceTransformer

# all-MiniLM-L6-v2 (384 dims, fast, good quality)
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(["Hello world", "Vector search is powerful"])
print(f"Shape: {embeddings.shape}")  # (2, 384)

# all-mpnet-base-v2 (768 dims, best open-source quality)
model = SentenceTransformer("all-mpnet-base-v2")
embeddings = model.encode(["Hello world"])
print(f"Shape: {embeddings.shape}")  # (1, 768)
```

---

## 3. Model Comparison

| Model | Dimensions | Speed | Quality | Cost | Privacy |
|-------|-----------|-------|---------|------|---------|
| text-embedding-3-small | 1536 | Fast (API) | High | $0.02/1M tokens | Data sent |
| text-embedding-3-large | 3072 | Fast (API) | Highest | $0.13/1M tokens | Data sent |
| all-MiniLM-L6-v2 | 384 | Very fast | Good | Free | Full privacy |
| all-mpnet-base-v2 | 768 | Fast | Very good | Free | Full privacy |

### Choosing the Right Model
- **Production with budget**: text-embedding-3-small
- **Max quality**: text-embedding-3-large
- **Self-hosted / privacy**: all-mpnet-base-v2
- **Edge / low-latency**: all-MiniLM-L6-v2

---

## 4. Using Our Embedding Generator

```python
from src.embeddings.embed import EmbeddingGenerator

# OpenAI
gen = EmbeddingGenerator(provider="openai", model="text-embedding-3-small")
emb = gen.embed(["Test text"])
print(f"Dims: {gen.dimensions}")

# Local
gen = EmbeddingGenerator(provider="local", model="all-MiniLM-L6-v2")
emb = gen.embed(["Test text"])
print(f"Dims: {gen.dimensions}")
```

---

## Validation
```bash
bash modules/02-embedding-models/validation/validate.sh
```

**Next: [Module 03 →](../03-chromadb-deep-dive/)**

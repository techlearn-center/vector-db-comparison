# Module 06: Pinecone Managed Service

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 05 completed, Pinecone account |

---

## Learning Objectives
- Set up Pinecone serverless and pod-based indexes
- Perform upsert, query, and delete operations
- Use namespaces for multi-tenancy
- Understand pricing and scaling

---

## 1. Pinecone Setup

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-api-key")

# Create serverless index
pc.create_index(
    name="documents",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

index = pc.Index("documents")
```

---

## 2. Operations

```python
# Upsert vectors
index.upsert(vectors=[
    {"id": "doc1", "values": [0.1, 0.2, ...], "metadata": {"category": "tech", "source": "web"}},
    {"id": "doc2", "values": [0.3, 0.4, ...], "metadata": {"category": "science", "source": "pdf"}},
])

# Query with metadata filter
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=10,
    include_metadata=True,
    filter={"category": {"$eq": "tech"}},
)

for match in results["matches"]:
    print(f"{match['id']}: {match['score']:.4f} - {match['metadata']}")

# Namespaces (multi-tenancy)
index.upsert(vectors=[...], namespace="user-123")
results = index.query(vector=[...], top_k=10, namespace="user-123")

# Delete
index.delete(ids=["doc1", "doc2"])
index.delete(filter={"category": "old"})
```

---

## 3. When to Use Pinecone

| Strength | Weakness |
|----------|----------|
| Fully managed (zero ops) | Vendor lock-in |
| Auto-scaling | Can be expensive at scale |
| Low latency globally | Data leaves your infrastructure |
| Simple API | Limited query flexibility |
| Free tier available | No self-hosted option |

---

## 4. Pricing Comparison

| Plan | Storage | Queries | Cost |
|------|---------|---------|------|
| Free (Starter) | 100K vectors | Unlimited | $0 |
| Serverless | Pay per use | Per query | ~$0.01-0.10/1K queries |
| Pod-based | Per pod | Unlimited | $70+/month per pod |

---

## Validation
```bash
bash modules/06-pinecone-managed/validation/validate.sh
```

**Next: [Module 07 →](../07-indexing-strategies/)**

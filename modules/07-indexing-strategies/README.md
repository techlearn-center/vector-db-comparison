# Module 07: Indexing Strategies and HNSW

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Advanced |
| **Prerequisites** | Modules 03-06 completed |

---

## Learning Objectives
- Understand HNSW, IVF, and flat index algorithms
- Tune index parameters for recall vs speed tradeoffs
- Choose the right index for your data size

---

## 1. Index Types

### Flat (Brute Force)
- Exact nearest neighbor search
- O(n) per query - slow for large datasets
- 100% recall guaranteed
- Use when: < 10K vectors

### IVFFlat (Inverted File Index)
- Clusters vectors into buckets, searches nearby buckets
- Build time: O(n), Query: O(n/lists * probes)
- Recall depends on `probes` parameter
- Use when: 10K-1M vectors

### HNSW (Hierarchical Navigable Small World)
- Graph-based approximate nearest neighbor
- Build time: O(n * log(n)), Query: O(log(n))
- Best recall-speed tradeoff
- Use when: > 100K vectors

---

## 2. HNSW Parameters

| Parameter | Effect | Default | Tune For |
|-----------|--------|---------|----------|
| `M` | Max connections per node | 16 | Higher = better recall, more memory |
| `ef_construction` | Build-time search width | 64 | Higher = better graph quality |
| `ef_search` | Query-time search width | 40 | Higher = better recall, slower |

```python
# pgvector HNSW tuning
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
WITH (m = 24, ef_construction = 128);

SET hnsw.ef_search = 100;

# ChromaDB HNSW tuning
collection = client.create_collection(
    "tuned",
    metadata={
        "hnsw:space": "cosine",
        "hnsw:M": 24,
        "hnsw:construction_ef": 128,
        "hnsw:search_ef": 100,
    },
)
```

---

## 3. Index Size Guidelines

| Dataset Size | Recommended Index | Expected Recall | Query Latency |
|-------------|-------------------|----------------|---------------|
| < 10K | Flat | 100% | < 10ms |
| 10K - 100K | IVFFlat | 95-99% | 1-5ms |
| 100K - 10M | HNSW | 95-99% | 1-10ms |
| > 10M | HNSW + sharding | 90-98% | 5-50ms |

---

## Validation
```bash
bash modules/07-indexing-strategies/validation/validate.sh
```

**Next: [Module 08 →](../08-benchmarking-methodology/)**

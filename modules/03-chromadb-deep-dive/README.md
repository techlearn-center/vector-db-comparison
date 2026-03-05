# Module 03: ChromaDB Deep Dive

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 02 completed, ChromaDB running |

---

## Learning Objectives
- Set up and configure ChromaDB (embedded and client-server)
- Perform CRUD operations on collections
- Use metadata filtering and distance metrics
- Understand HNSW indexing in ChromaDB

---

## 1. ChromaDB Setup

```python
import chromadb

# Option 1: Embedded (in-process, for development)
client = chromadb.Client()

# Option 2: Persistent (saves to disk)
client = chromadb.PersistentClient(path="./chroma_data")

# Option 3: Client-server (production)
client = chromadb.HttpClient(host="localhost", port=8001)
```

---

## 2. Collection Operations

```python
# Create with cosine distance
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"},  # cosine, l2, ip
)

# Insert vectors
collection.add(
    ids=["doc1", "doc2", "doc3"],
    embeddings=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
    documents=["First doc", "Second doc", "Third doc"],
    metadatas=[
        {"source": "web", "category": "tech"},
        {"source": "pdf", "category": "science"},
        {"source": "web", "category": "tech"},
    ],
)

# Query with metadata filter
results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3]],
    n_results=5,
    where={"category": "tech"},
    where_document={"$contains": "doc"},
    include=["documents", "metadatas", "distances"],
)
```

---

## 3. Metadata Filtering

```python
# Exact match
where={"source": "web"}

# Comparison operators
where={"price": {"$gt": 10}}
where={"price": {"$gte": 10, "$lte": 100}}

# Logical operators
where={"$and": [{"source": "web"}, {"category": "tech"}]}
where={"$or": [{"source": "web"}, {"source": "pdf"}]}
```

---

## 4. Using Our Wrapper

```python
from src.databases.chromadb_client import ChromaDBClient

db = ChromaDBClient(host="localhost", port=8001)
db.create_collection("test_collection")
db.insert("test_collection", ids=["1", "2"], embeddings=[[0.1]*384, [0.2]*384], documents=["Doc 1", "Doc 2"])
results = db.search("test_collection", query_embedding=[0.15]*384, top_k=5)
print(f"Found {len(results)} results")
print(f"Count: {db.count('test_collection')}")
```

---

## 5. When to Use ChromaDB

| Strength | Weakness |
|----------|----------|
| Easy setup (pip install) | Limited scalability (single node) |
| Great for prototyping | No built-in replication |
| Good Python API | Fewer query features than Weaviate |
| Metadata filtering | Limited multi-tenancy |

---

## Validation
```bash
bash modules/03-chromadb-deep-dive/validation/validate.sh
```

**Next: [Module 04 →](../04-pgvector-postgresql/)**

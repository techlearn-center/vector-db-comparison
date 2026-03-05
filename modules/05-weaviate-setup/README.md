# Module 05: Weaviate Setup and Schema Design

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 04 completed, Weaviate running |

---

## Learning Objectives
- Set up Weaviate with Docker
- Design schemas with properties and vectorizers
- Perform CRUD operations and vector search
- Use GraphQL and REST APIs

---

## 1. Weaviate Concepts

- **Collections** (formerly Classes): Like database tables
- **Objects**: Individual records with properties and vectors
- **Vectorizers**: Built-in modules to auto-generate embeddings
- **Modules**: Plugins for vectorization, ranking, etc.

---

## 2. Schema Design

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_local()

client.collections.create(
    name="Article",
    vectorizer_config=Configure.Vectorizer.none(),  # We provide our own vectors
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="content", data_type=DataType.TEXT),
        Property(name="category", data_type=DataType.TEXT),
        Property(name="published", data_type=DataType.DATE),
    ],
)
```

---

## 3. Insert and Query

```python
from weaviate.classes.query import MetadataQuery, Filter

articles = client.collections.get("Article")

# Insert
articles.data.insert(
    properties={"title": "AI Basics", "content": "ML is...", "category": "tech"},
    vector=[0.1, 0.2, ...],
)

# Vector search
response = articles.query.near_vector(
    near_vector=[0.1, 0.2, ...],
    limit=10,
    return_metadata=MetadataQuery(distance=True),
)

# Filtered search
response = articles.query.near_vector(
    near_vector=[0.1, 0.2, ...],
    limit=10,
    filters=Filter.by_property("category").equal("tech"),
)

for obj in response.objects:
    print(f"{obj.properties['title']} (distance: {obj.metadata.distance:.4f})")
```

---

## 4. Using Our Wrapper

```python
from src.databases.weaviate_client import WeaviateClient

db = WeaviateClient(host="localhost", port=8080)
db.create_collection("TestDocs")
db.insert("TestDocs", ids, embeddings, documents, metadatas)
results = db.search("TestDocs", query_embedding, top_k=10)
db.close()
```

---

## 5. When to Use Weaviate

| Strength | Weakness |
|----------|----------|
| Rich query language (GraphQL) | More complex setup |
| Built-in vectorizers | Heavier resource usage |
| Multi-tenancy support | Learning curve |
| Hybrid search built-in | Fewer managed options |

---

## Validation
```bash
bash modules/05-weaviate-setup/validation/validate.sh
```

**Next: [Module 06 →](../06-pinecone-managed/)**

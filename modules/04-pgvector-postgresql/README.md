# Module 04: pgvector with PostgreSQL

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Intermediate |
| **Prerequisites** | Module 03, basic SQL knowledge |

---

## Learning Objectives
- Install and configure pgvector extension
- Store and query vectors using SQL
- Build indexes (IVFFlat, HNSW) for fast search
- Combine vector search with traditional SQL queries

---

## 1. Setup pgvector

```sql
-- Connect to PostgreSQL
psql -h localhost -U vectordb -d vectors

-- Enable the extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table with vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    category TEXT,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 2. Insert and Query

```sql
-- Insert vectors
INSERT INTO documents (title, content, embedding)
VALUES ('AI Basics', 'Machine learning is...', '[0.1, 0.2, ...]');

-- Cosine similarity search
SELECT id, title, 1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 10;

-- Euclidean distance search
SELECT id, title, embedding <-> '[0.1, 0.2, ...]'::vector AS distance
FROM documents
ORDER BY embedding <-> '[0.1, 0.2, ...]'::vector
LIMIT 10;

-- Inner product search
SELECT id, title, (embedding <#> '[0.1, 0.2, ...]'::vector) * -1 AS similarity
FROM documents
ORDER BY embedding <#> '[0.1, 0.2, ...]'::vector
LIMIT 10;
```

---

## 3. Indexing

```sql
-- IVFFlat index (faster build, slightly lower recall)
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- lists = sqrt(num_rows) is a good starting point

-- HNSW index (slower build, better recall)
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Tune search parameters
SET ivfflat.probes = 10;        -- IVFFlat: more probes = better recall
SET hnsw.ef_search = 100;       -- HNSW: higher = better recall, slower
```

---

## 4. Combining Vector + SQL

```python
# The killer feature: combine vector search with SQL filters
from src.databases.pgvector_client import PgVectorClient

db = PgVectorClient()
db.create_collection("articles", dimensions=1536)

# Insert with metadata
db.insert("articles", ["1", "2"], embeddings, ["Doc 1", "Doc 2"],
          [{"category": "tech"}, {"category": "science"}])

# Search with SQL filters
results = db.search("articles", query_embedding, top_k=10,
                     filters={"category": "tech"})
```

---

## 5. When to Use pgvector

| Strength | Weakness |
|----------|----------|
| Already using PostgreSQL | Slower than purpose-built DBs |
| SQL + vector in one query | Limited to single-node |
| ACID transactions | Fewer vector-specific features |
| Existing tooling (backups, monitoring) | Index build can be slow |

---

## Validation
```bash
bash modules/04-pgvector-postgresql/validation/validate.sh
```

**Next: [Module 05 →](../05-weaviate-setup/)**

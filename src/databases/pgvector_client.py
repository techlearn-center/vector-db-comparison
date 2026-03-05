"""
pgvector (PostgreSQL) client wrapper for vector operations.
"""
from typing import List, Dict, Any, Optional

import psycopg2
from psycopg2.extras import execute_values


class PgVectorClient:
    """Wrapper around pgvector for standardized vector operations."""

    def __init__(self, host: str = "localhost", port: int = 5432,
                 dbname: str = "vectors", user: str = "vectordb", password: str = "vectordb"):
        self.conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        self.conn.autocommit = True
        self.name = "pgvector"
        self._setup()

    def _setup(self):
        with self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    def create_collection(self, name: str, dimensions: int = 1536):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    id TEXT PRIMARY KEY,
                    embedding vector({dimensions}),
                    document TEXT,
                    metadata JSONB DEFAULT '{{}}'
                );
            """)
            cur.execute(f"""
                CREATE INDEX IF NOT EXISTS {name}_embedding_idx
                ON {name} USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100);
            """)

    def insert(self, collection_name: str, ids: List[str], embeddings: List[List[float]],
               documents: List[str], metadatas: Optional[List[Dict]] = None):
        import json
        with self.conn.cursor() as cur:
            data = []
            for i in range(len(ids)):
                meta = json.dumps(metadatas[i]) if metadatas else "{}"
                data.append((ids[i], embeddings[i], documents[i], meta))
            execute_values(
                cur,
                f"INSERT INTO {collection_name} (id, embedding, document, metadata) VALUES %s ON CONFLICT (id) DO NOTHING",
                data,
                template="(%s, %s::vector, %s, %s::jsonb)",
            )

    def search(self, collection_name: str, query_embedding: List[float],
               top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        with self.conn.cursor() as cur:
            where_clause = ""
            if filters:
                conditions = [f"metadata->>'{k}' = '{v}'" for k, v in filters.items()]
                where_clause = "WHERE " + " AND ".join(conditions)

            cur.execute(f"""
                SELECT id, document, metadata, 1 - (embedding <=> %s::vector) as similarity
                FROM {collection_name}
                {where_clause}
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
            """, (query_embedding, query_embedding, top_k))

            results = []
            for row in cur.fetchall():
                results.append({
                    "id": row[0],
                    "document": row[1],
                    "metadata": row[2],
                    "similarity": float(row[3]),
                })
            return results

    def count(self, collection_name: str) -> int:
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {collection_name};")
            return cur.fetchone()[0]

    def delete_collection(self, name: str):
        with self.conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {name};")

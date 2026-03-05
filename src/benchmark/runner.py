"""
Benchmark runner for comparing vector databases.
Measures insert throughput, query latency, recall, and resource usage.
"""
import time
import json
import numpy as np
from typing import List, Dict, Any
from pathlib import Path


class BenchmarkRunner:
    """Run standardized benchmarks across vector databases."""

    def __init__(self, embedding_dim: int = 1536):
        self.embedding_dim = embedding_dim
        self.results = {}

    def generate_test_data(self, num_vectors: int = 10000) -> Dict[str, Any]:
        """Generate random test vectors and queries."""
        np.random.seed(42)
        vectors = np.random.randn(num_vectors, self.embedding_dim).astype(np.float32)
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        queries = np.random.randn(100, self.embedding_dim).astype(np.float32)
        queries = queries / np.linalg.norm(queries, axis=1, keepdims=True)
        return {"vectors": vectors, "queries": queries}

    def benchmark_insert(self, db_client, collection_name: str,
                         vectors: np.ndarray, batch_size: int = 100) -> Dict[str, float]:
        """Benchmark insert throughput."""
        num_vectors = len(vectors)
        start = time.time()

        for i in range(0, num_vectors, batch_size):
            batch = vectors[i:i + batch_size]
            ids = [f"vec_{j}" for j in range(i, i + len(batch))]
            docs = [f"Document {j}" for j in range(i, i + len(batch))]
            db_client.insert(collection_name, ids, batch.tolist(), docs)

        elapsed = time.time() - start
        return {
            "total_vectors": num_vectors,
            "total_seconds": elapsed,
            "vectors_per_second": num_vectors / elapsed,
            "batch_size": batch_size,
        }

    def benchmark_search(self, db_client, collection_name: str,
                         queries: np.ndarray, top_k: int = 10) -> Dict[str, float]:
        """Benchmark search latency."""
        latencies = []

        for query in queries:
            start = time.time()
            db_client.search(collection_name, query.tolist(), top_k=top_k)
            latencies.append(time.time() - start)

        latencies.sort()
        return {
            "num_queries": len(queries),
            "avg_ms": np.mean(latencies) * 1000,
            "p50_ms": np.percentile(latencies, 50) * 1000,
            "p95_ms": np.percentile(latencies, 95) * 1000,
            "p99_ms": np.percentile(latencies, 99) * 1000,
            "min_ms": min(latencies) * 1000,
            "max_ms": max(latencies) * 1000,
        }

    def benchmark_recall(self, db_client, collection_name: str,
                         queries: np.ndarray, vectors: np.ndarray, top_k: int = 10) -> Dict[str, float]:
        """Measure recall@k compared to brute-force search."""
        recalls = []

        for query in queries[:20]:  # Sample for speed
            # Brute-force ground truth
            similarities = np.dot(vectors, query)
            ground_truth = set(np.argsort(similarities)[-top_k:][::-1])

            # DB results
            results = db_client.search(collection_name, query.tolist(), top_k=top_k)
            retrieved_ids = set()
            for r in results:
                idx = int(r["id"].replace("vec_", ""))
                retrieved_ids.add(idx)

            recall = len(ground_truth & retrieved_ids) / top_k
            recalls.append(recall)

        return {
            "avg_recall_at_k": np.mean(recalls),
            "min_recall": min(recalls),
            "max_recall": max(recalls),
            "top_k": top_k,
        }

    def run_full_benchmark(self, db_client, collection_name: str,
                           num_vectors: int = 10000) -> Dict[str, Any]:
        """Run complete benchmark suite on a database."""
        print(f"\nBenchmarking {db_client.name} with {num_vectors} vectors...")

        data = self.generate_test_data(num_vectors)
        db_client.create_collection(collection_name)

        insert_results = self.benchmark_insert(db_client, collection_name, data["vectors"])
        print(f"  Insert: {insert_results['vectors_per_second']:.0f} vec/s")

        search_results = self.benchmark_search(db_client, collection_name, data["queries"])
        print(f"  Search: avg={search_results['avg_ms']:.1f}ms, p95={search_results['p95_ms']:.1f}ms")

        recall_results = self.benchmark_recall(db_client, collection_name, data["queries"], data["vectors"])
        print(f"  Recall@10: {recall_results['avg_recall_at_k']:.3f}")

        result = {
            "database": db_client.name,
            "num_vectors": num_vectors,
            "embedding_dim": self.embedding_dim,
            "insert": insert_results,
            "search": search_results,
            "recall": recall_results,
        }

        self.results[db_client.name] = result
        return result

    def save_results(self, output_path: str = "benchmark_results.json"):
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\nResults saved to {output_path}")

    def print_comparison(self):
        """Print a comparison table of all benchmarked databases."""
        if not self.results:
            print("No results to compare. Run benchmarks first.")
            return

        print("\n" + "=" * 80)
        print(f"{'Database':<15} {'Insert (vec/s)':<18} {'Search avg (ms)':<18} {'Search p95 (ms)':<18} {'Recall@10':<12}")
        print("=" * 80)
        for name, r in self.results.items():
            print(f"{name:<15} {r['insert']['vectors_per_second']:<18.0f} {r['search']['avg_ms']:<18.1f} {r['search']['p95_ms']:<18.1f} {r['recall']['avg_recall_at_k']:<12.3f}")
        print("=" * 80)

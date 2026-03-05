# Module 08: Benchmarking Methodology

| | |
|---|---|
| **Time** | 3-5 hours |
| **Difficulty** | Advanced |
| **Prerequisites** | Modules 03-07 completed |

---

## Learning Objectives
- Design fair benchmarks across vector databases
- Measure insert throughput, query latency, and recall
- Avoid common benchmarking pitfalls

---

## 1. What to Benchmark

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| Insert throughput | Vectors/second during bulk load | Initial data loading time |
| Query latency (avg, p50, p95, p99) | Time per search | User experience |
| Recall@K | % of true nearest neighbors found | Search quality |
| Memory usage | RAM consumption | Infrastructure cost |
| Index build time | Time to create search index | Operational overhead |

---

## 2. Using the Benchmark Runner

```python
from src.benchmark.runner import BenchmarkRunner
from src.databases.chromadb_client import ChromaDBClient
from src.databases.pgvector_client import PgVectorClient
from src.databases.weaviate_client import WeaviateClient

runner = BenchmarkRunner(embedding_dim=1536)

# Benchmark each database
chroma = ChromaDBClient()
runner.run_full_benchmark(chroma, "bench_chroma", num_vectors=10000)

pg = PgVectorClient()
runner.run_full_benchmark(pg, "bench_pgvector", num_vectors=10000)

weaviate = WeaviateClient()
runner.run_full_benchmark(weaviate, "bench_weaviate", num_vectors=10000)

# Compare results
runner.print_comparison()
runner.save_results("benchmark_results.json")
```

**Expected Output:**
```
================================================================================
Database        Insert (vec/s)     Search avg (ms)    Search p95 (ms)    Recall@10
================================================================================
ChromaDB        2500               3.2                8.1                0.952
pgvector        1800               4.5                12.3               0.968
Weaviate        3200               2.1                5.4                0.945
================================================================================
```

---

## 3. Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Cold vs warm cache | First query much slower | Run warmup queries first |
| Small dataset | Results don't scale | Test with realistic sizes (10K+) |
| Single query vector | Not statistically significant | Use 100+ diverse queries |
| Ignoring index build | Underestimates total cost | Include in total time |
| Same machine load | Databases compete for resources | Benchmark one at a time |

---

## 4. Hands-On Lab

Run the full benchmark suite, generate comparison charts, and write a recommendation report.

## Validation
```bash
bash modules/08-benchmarking-methodology/validation/validate.sh
```

**Next: [Module 09 →](../09-hybrid-search/)**

# Capstone: Vector Database Benchmark Platform

## Overview
Build a complete benchmarking platform that compares ChromaDB, pgvector, Weaviate, and Pinecone on real-world workloads, generates visualizations, and produces a recommendation report.

## Architecture
```
Test Data Generator --> Embedding Generator --> [ChromaDB, pgvector, Weaviate, Pinecone]
                                                        |
                                                 Benchmark Runner
                                                        |
                                              Results Aggregator
                                                        |
                                         Report Generator (charts + recommendations)
```

## Requirements
1. **Data Pipeline**: Load a real dataset (e.g., Wikipedia, ArXiv), generate embeddings
2. **Benchmark Suite**: Measure insert, query, recall for all 4 databases at 1K, 10K, 100K vectors
3. **Visualization**: Generate comparison charts (bar, line, heatmap)
4. **Hybrid Search**: Compare pure vector vs hybrid search recall
5. **Report**: Auto-generate markdown report with recommendations
6. **Docker**: All databases run via docker-compose

## Acceptance Criteria
- [ ] Real dataset loaded (not synthetic)
- [ ] All 4 databases benchmarked at 3 scale points
- [ ] Charts generated (latency, throughput, recall)
- [ ] Hybrid search comparison completed
- [ ] Report generated with clear recommendations
- [ ] Reproducible with `docker compose up` + single script
- [ ] All services start cleanly
- [ ] Benchmark results saved to JSON

## Validation
```bash
bash capstone/validation/validate.sh
```

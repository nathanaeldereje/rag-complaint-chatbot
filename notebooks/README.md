# Notebooks – Experimental Lab

This directory is the **R&D workspace** for the CrediTrust RAG chatbot. Notebooks are used for EDA, prototyping, and testing before migrating stable code to `scripts/` and `src/`.

## 📓 Notebook Directory

| Notebook | Phase | Primary Objective | Key Output / Deliverable |
| :--- | :--- | :--- | :--- |
| **`01_eda_preprocessing.ipynb`** | **1** | EDA on CFPB data, filtering, cleaning narratives | `filtered_complaints.parquet` + summary |
| **`02_chunking_embedding.ipynb`** | **2** | Chunking experiments, embedding model tests, sampling | Sample FAISS index prototype |
| **`03_vector_store_ingest_test.ipynb`** | **3** | Ingest pre-built embeddings into FAISS, verify index | Full `vector_store/full_faiss_index/` |
| **`03_rag_pipeline_proto.ipynb`** | **3** | RAG logic prototyping, prompt engineering, evaluation | `rag_evaluation_results.csv` + table |
| **`04_evaluation_bench.ipynb`** | **3** | Advanced benchmarking & model comparison (optional) | Performance metrics & comparisons |

## ⚙️ Usage Guide

1. **Setup**  
   Ensure root dependencies are installed:  
   ```bash
   cd ..
   pip install -r requirements.txt
   ```
2. **Running Notebooks**  
   * Start Jupyter: `jupyter notebook`
   * Run sequentially — each builds on previous outputs (e.g., Task 3 needs `full_faiss_index/` from ingestion notebook).
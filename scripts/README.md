# Scripts – Pipeline Tools

Standalone, production-ready Python scripts for the CrediTrust RAG complaint chatbot.

## Available Scripts

| Script | Purpose | Typical Command Example |
| :--- | :--- | :--- |
| `preprocess.py` | **Task 1:** Load raw CFPB data → filter to target products → clean narratives → save Parquet + CSV | `python scripts/preprocess.py --input data/raw/complaints.csv --output_dir data/processed` |
| `build_vector_store.py` | **Task 2:** Stratified sampling (12.5k) → chunking (500 chars) → embedding → save FAISS index | `python scripts/build_vector_store.py --input data/processed/filtered_complaints.parquet --sample_size 12500` |
| `ingest_precomputed_vectors.py` | **Task 3:** Ingest full pre-built `complaint_embeddings.parquet` (~1.37M chunks) into FAISS index | `python scripts/ingest_precomputed_vectors.py --input data/processed/complaint_embeddings.parquet` |
| `rag_pipeline.py` | **Task 3:** Load FAISS index → retrieve top-k chunks → generate LLM answer via CLI | `python scripts/rag_pipeline.py --question "Why are fees so high?"` |

## Explanation

These scripts form the **ETL (Extract, Transform, Load)** and inference backbone:

*   **`preprocess.py`**: Memory-efficient loading of large CSV, filtering for 5 financial products, text cleaning (lowercase, redactions, boilerplate removal).
*   **`build_vector_store.py`**: Stratified sampling by product, chunking with LangChain, embedding with `all-MiniLM-L6-v2`, batched FAISS indexing.
*   **`ingest_precomputed_vectors.py`**: Loads pre-built embeddings/metadata from challenge-provided parquet, batches into full FAISS index.
*   **`rag_pipeline.py`**: CLI for RAG inference — query embedding, top-5 retrieval, grounded generation with Mistral-7B/Zephyr.

All scripts use `src/` modules (data_loading, cleaning) for reusability and accept `--help` for arguments.

## Recommended Workflow

1.  **Data Preparation**
    Clean & filter raw data:
    ```bash
    python scripts/preprocess.py --input data/raw/complaints.csv --output_dir data/processed
    ```
    > → Outputs `filtered_complaints.parquet` + `.csv`

2.  **Sample Vector Store (Task 2 – prototyping)**
    Build index on ~12.5k sample:
    ```bash
    python scripts/build_vector_store.py --sample_size 12500
    ```
    > → Saves `vector_store/faiss_index/` (sample)

3.  **Full Vector Store (Task 3 – production)**
    Ingest pre-built embeddings:
    ```bash
    python scripts/ingest_precomputed_vectors.py --input data/processed/complaint_embeddings.parquet
    ```
    > → Saves `vector_store/full_faiss_index/`

4.  **RAG Testing & Evaluation**
    Query the pipeline:
    ```bash
    python scripts/rag_pipeline.py --question "Why are fees so high?"
    ```
    > → Prototype & evaluate in `notebooks/03_rag_pipeline_proto.ipynb`

## Notes

*   Requires Hugging Face API token in `.env` for LLM (copy from `.env_example`).
*   Vector stores saved to `vector_store/` — ignore in Git.
*   For full evaluation results, see `data/processed/rag_evaluation_results.csv`.
# Scripts – Pipeline Tools

Standalone Python scripts for building the CrediTrust RAG complaint chatbot.

## Available Scripts

| Script | Purpose | Typical Command Example |
| :--- | :--- | :--- |
| `preprocess.py` | **Task 1:** Load raw CFPB data → filter products → clean narratives → save Parquet | `python scripts/preprocess.py --input data/raw/complaints.csv` |
| `build_vector_store.py` | **Task 2:** Stratified sampling (12.5k) → chunking (500 chars) → embedding → save FAISS index | `python scripts/build_vector_store.py --sample_size 12500` |
| `rag_pipeline.py` | **Task 3 (Planned):** Load FAISS index → retrieve docs → generate LLM answer | *(Coming in Task 3)* |

## Explanation

These scripts handle the **ETL (Extract, Transform, Load)** pipeline for the RAG system. They rely on core logic modules located in `src/`.

- **`preprocess.py`**: Handles memory-efficient loading of the massive CSV, filters for the 5 target financial products, and performs text normalization (lowercasing, removing boilerplate).
- **`build_vector_store.py`**: The main indexing engine. It:
    1.  Loads processed data.
    2.  Performs **stratified sampling** to keep product distributions balanced.
    3.  Chunks text using **LangChain**.
    4.  Generates embeddings using `all-MiniLM-L6-v2`.
    5.  Saves a local **FAISS** index.

## Recommended Workflow

1.  **Data Cleaning**
    Run the preprocessor to create the optimized Parquet file:
    ```bash
    python scripts/preprocess.py --input data/raw/complaints.csv --output_dir data/processed
    ```

2.  **Vector Database Creation**
    Build the FAISS index (Sampling ~12.5k records recommended for local dev):
    ```bash
    python scripts/build_vector_store.py --input data/processed/filtered_complaints.parquet --sample_size 12500
    ```

3.  **Testing (Upcoming)**
    Once Task 3 is complete, you will run the RAG pipeline to query the vector store:
    ```bash
    python scripts/rag_pipeline.py --query "Why are personal loans denied?"
    ```
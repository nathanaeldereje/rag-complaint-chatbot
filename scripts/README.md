# Scripts – Pipeline Tools

Standalone Python scripts for building the CrediTrust RAG complaint chatbot.

## Available Scripts

| Script                  | Purpose                                                                 | Typical Command Example                                      |
|-------------------------|-------------------------------------------------------------------------|--------------------------------------------------------------|
| `preprocess.py`         | Load CFPB data → filter products → clean narratives → save CSV          | `python preprocess.py --input raw.csv --output filtered.csv` |
| `sample_data.py`        | Create stratified 10k–15k sample for fast prototyping                   | `python sample_data.py --input filtered.csv --size 12000`    |
| `chunk_and_embed.py`    | Chunk text → generate embeddings → build small test vector store        | `python chunk_and_embed.py --input sample.csv --output_dir vector_store/test` |
| `build_full_index.py`   | Load pre-built embeddings → create full Chroma/FAISS index              | `python build_full_index.py --embeddings complaint_embeddings.parquet --db chroma` |
| `rag_pipeline_test.py`  | Quick end-to-end test: retrieve + generate answers from command line    | `python rag_pipeline_test.py --question "Why are credit cards delayed?"` |
| `utils.py`              | Shared helpers (cleaning, chunking, embedding loading, etc.)            | (imported by other scripts)                                  |

## Explanation

These scripts are meant to be:
- **Independent** — each can run on its own
- **Reusable** — core logic lives here, not scattered in notebooks
- **Modular** — you can call them from `app.py` or chain them in workflows

They help you move step-by-step from raw data → cleaned data → sample experiments → full vector store → working RAG.

Most scripts accept `--help` to show all flags.

## Recommended Workflow

1. `preprocess.py`  
   → Clean and filter the full dataset

2. `sample_data.py`  
   → Create a smaller representative sample

3. `chunk_and_embed.py`  
   → Experiment with chunk size, overlap, embedding model on the sample

4. `build_full_index.py`  
   → Build the production vector store using the pre-computed embeddings

5. `rag_pipeline_test.py`  
   → Test retrieval + generation before integrating into the UI

6. Finally → use the best settings in `app.py`

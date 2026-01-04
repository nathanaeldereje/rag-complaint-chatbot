# Notebooks
This directory serves as the **experimental lab** for the CrediTrust RAG project. Here, we perform data analysis, prototype our RAG logic, and test code before migrating it to the production `scripts/` folder.


### 📓 Notebook Directory

| Notebook | Phase | Primary Objective | Key Output |
| --- | --- | --- | --- |
| **`01_eda_preprocessing.ipynb`** | **Phase 1** | Clean raw CFPB data and analyze complaint distributions. | `filtered_complaints.csv` |
| **`02_chunking_embedding.ipynb`** | **Phase 2** | Experiment with chunking strategies and embedding models. | Vector Index Prototype |
| **`03_rag_pipeline_proto.ipynb`** | **Phase 3** | Design RAG prompt templates and retrieval logic. | RAG Chain Logic |
| **`04_evaluation_bench.ipynb`** | **Phase 3** | Benchmark LLM responses against ground-truth questions. | Model Performance Metrics |

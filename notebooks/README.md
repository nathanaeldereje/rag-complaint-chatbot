# 🔬 Development Notebooks

This directory serves as the **experimental lab** for the CrediTrust RAG project. Here, we perform data analysis, prototype our RAG logic, and test code before migrating it to the production `scripts/` folder.

## 📚 Notebook Directory

The notebooks are numbered to follow the project's logical workflow.

| Notebook | Task | Description | Status |
| :--- | :--- | :--- | :--- |
| **`01_eda_preprocessing.ipynb`** | **Task 1** | Exploratory Data Analysis. Loading the CFPB dataset, analyzing complaint lengths, checking product distribution, and cleaning text for embeddings. | 🔄 **In Progress** |
| **`02_chunking_embedding.ipynb`** | **Task 2** | Stratified sampling, experimenting with chunk sizes (RecursiveCharacterTextSplitter), and generating vector embeddings with `all-MiniLM-L6-v2`. | 📅 Planned |
| **`03_rag_pipeline_proto.ipynb`** | **Task 3** | Prototyping the retrieval logic. Testing similarity search and designing prompt templates for the LLM. | 📅 Planned |
| **`04_evaluation_bench.ipynb`** | **Task 3** | Qualitative evaluation. Running the pipeline against specific test questions to rate the quality of answers. | 📅 Planned |

## ⚙️ Usage Guide

### 1. Environment Setup
Ensure your root environment is set up and active. The notebooks rely on the packages listed in the root `requirements.txt`.

```bash
# Navigate to the project root
cd ..
source venv/bin/activate
pip install -r requirements.txt
```
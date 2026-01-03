# Intelligent Complaint Analysis for Financial Services 🏦

**Project:** CrediTrust Financial RAG-Powered Chatbot  
**Role:** Data & AI Engineer  
**Status:** 🔄 Active Development  

## Project Overview

This project builds an internal **Retrieval-Augmented Generation (RAG)** chatbot for CrediTrust Financial, a fast-growing digital finance company in East Africa.  

Using real-world consumer complaint data (inspired by CFPB), the tool enables Product Managers, Support, and Compliance teams to ask natural-language questions about customer pain points across five product lines:

* Credit Cards  
* Personal Loans  
* Savings Accounts  
* Money Transfers  

The system retrieves relevant complaint excerpts via semantic search (vector database + embeddings), then generates concise, evidence-backed answers using a language model.    **Goal:** Turn thousands of monthly unstructured complaints into actionable, real-time insights—reducing analysis time from days to minutes and shifting the company from reactive firefighting to proactive product and risk improvement.
---

## 📖 Business Objective

**CrediTrust Financial** is a fast-growing digital finance company serving East Africa with over 500,000 users. As operations expand across Credit Cards, Personal Loans, and Money Transfers, the volume of customer complaints has overwhelmed internal teams.

**The Problem:**
Stakeholders like Asha (Product Manager) currently spend hours manually reading complaints to identify trends. The Support and Compliance teams are reactive, often missing critical issues until they become major problems.

**The Solution:**
Develop a **Retrieval-Augmented Generation (RAG)** chatbot that transforms raw, unstructured complaint data into strategic assets. This tool will allow internal users to ask natural language questions (e.g., *"Why are customers upset about Money Transfers?"*) and receive evidence-backed answers in seconds.

**Key Performance Indicators (KPIs):**
1.  **Speed:** Decrease time to identify trends from days to minutes.
2.  **Accessibility:** Empower non-technical teams to query data without analysts.
3.  **Proactivity:** Shift from reacting to fires to preventing them.


---

## 📦 Key Deliverables

This repository will contain the following artifacts upon completion:

*   **`data/processed/`**: Cleaned dataset ready for embedding.
*   **`vector_store/`**: Persisted Vector Database (ChromaDB/FAISS) containing complaint embeddings.
*   **`scripts/rag_pipeline.py`**: The core logic for retrieval and generation.
*   **`app.py`**: The user-facing web application.
*   **Final Report**: A comprehensive analysis of the system's performance and business impact.

---

## 📂 Repository Structure

```text
rag-complaint-chatbot/
├── .github/workflows/  # CI/CD for automated testing
├── data/               # Raw and Processed data (Not tracked in Git)
├── notebooks/          # Jupyter Notebooks for EDA and Experiments
├── scripts/            # Standalone Python scripts for building the CrediTrust RAG complaint chatbot.
├── src/                # Application modular source codes
├── tests/              # Unit tests
├── app.py              # Entry point for the Chat UI
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## 🛠️ Getting Started

### Prerequisites
*   Python 3.9+
*   Virtual Environment recommended

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/rag-complaint-chatbot.git
    cd rag-complaint-chatbot
    ```

2.  **Set up the environment**
    ```bash
    python -m venv .venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Tests**
    Ensure the environment is set up correctly by running the initial smoke tests:
    ```bash
    pytest
    ```
---

## 🚀 Project Progress & Roadmap

| Phase | Task Description | Status |
| :--- | :--- | :--- |
| **0. Setup** | Project Structure, Git, CI/CD, and Environment Setup | ✅ **Completed** |
| **1. Data** | **EDA & Preprocessing:** Cleaning CFPB data, analyzing narrative lengths, filtering for specific financial products. | 🔄 **In Progress** |
| **2. Search** | **Vector Store Creation:** Chunking text, generating embeddings (MiniLM), and indexing with ChromaDB/FAISS. | 📅 Planned |
| **3. Core** | **RAG Pipeline:** Building the Retriever and Generator, Prompt Engineering, and Qualitative Evaluation. | 📅 Planned |
| **4. App** | **User Interface:** Building an interactive Gradio/Streamlit web app for stakeholders. | 📅 Planned |
---
*Developed as part of the CrediTrust Financial AI Engineering Initiative.*

**Built by:** Nathanael Dereje

**Current Date:** January 3, 2026  


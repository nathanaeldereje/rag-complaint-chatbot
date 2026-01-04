# scripts/build_vector_store.py

import sys
import os
import logging
import argparse
import shutil
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Build RAG Vector Store from processed data.")
    parser.add_argument("--input", type=str, default="data/processed/filtered_complaints.parquet", help="Path to input parquet file.")
    parser.add_argument("--output_dir", type=str, default="vector_store/faiss_index", help="Directory for FAISS index.")
    parser.add_argument("--sample_size", type=int, default=12500, help="Target number of complaints to sample.")
    parser.add_argument("--chunk_size", type=int, default=500, help="Character limit per chunk.")
    parser.add_argument("--chunk_overlap", type=int, default=50, help="Character overlap between chunks.")
    return parser.parse_args()

def load_and_sample(path, target_size):
    """Loads data and performs stratified sampling."""
    logger.info(f"Loading data from {path}...")
    df = pd.read_parquet(path)
    
    total_rows = len(df)
    if total_rows <= target_size:
        logger.info("Dataset smaller than target sample size. Using full dataset.")
        return df

    frac = target_size / total_rows
    logger.info(f"Sampling {target_size} rows (approx {frac:.2%})...")
    
    # Stratified sampling by Product
    sampled_df = df.groupby('Product', group_keys=False).apply(lambda x: x.sample(frac=frac, random_state=42))
    
    logger.info(f"Final sample size: {len(sampled_df)}")
    return sampled_df

def create_documents(df, chunk_size, chunk_overlap):
    """Splits text and creates LangChain Document objects with metadata."""
    logger.info("Splitting text into chunks...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    documents = []
    
    # Iterate with tqdm
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Chunking"):
        text = row['cleaned_narrative']
        if not text or not isinstance(text, str):
            continue
            
        chunks = splitter.split_text(text)
        
        for i, chunk in enumerate(chunks):
            # Metadata is crucial for the RAG retrieval later
            meta = {
                "complaint_id": str(row['Complaint ID']),
                "product": row['Product'],
                "issue": row.get('Issue', 'Unknown'),
                "company": row.get('Company', 'Unknown'),
                "date": str(row.get('Date received', '')),
                "chunk_index": i
            }
            documents.append(Document(page_content=chunk, metadata=meta))
            
    logger.info(f"Generated {len(documents)} chunks from {len(df)} complaints.")
    return documents

def build_vector_store(documents, output_dir):
    """Embeds documents and saves to FAISS."""
    
    # Clear existing vector store if it exists
    if os.path.exists(output_dir):
        logger.warning(f"Removing existing vector store at {output_dir}")
        shutil.rmtree(output_dir)
        
    logger.info("Initializing Embedding Model (all-MiniLM-L6-v2)...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    logger.info(f"Creating FAISS index at {output_dir}. This may take a while...")

        # --- BATCHING LOGIC START ---
    batch_size = 1000 # Process 1000 chunks at a time
    total_docs = len(documents)

        # Initialize FAISS with the first batch to create the structure
    logger.info("Initializing index with first batch...")
    vectorstore = FAISS.from_documents(documents[:batch_size], embedding_model)

        # Process the rest in batches
    # We start from batch_size because we already did the first 0-1000
    for i in tqdm(range(batch_size, total_docs, batch_size), desc="Embedding Batches"):
        batch = documents[i : i + batch_size]
        vectorstore.add_documents(batch)
    # --- BATCHING LOGIC END ---

    # Save Locally
    vectorstore.save_local(output_dir)
    
    logger.info("Vector store created and persisted successfully.")
    return vectorstore

def main():
    args = parse_args()
    
    # 1. Load & Sample
    df = load_and_sample(args.input, args.sample_size)
    
    # 2. Chunk
    documents = create_documents(df, args.chunk_size, args.chunk_overlap)
    
    # 3. Embed & Store
    build_vector_store(documents, args.output_dir)
    
    logger.info("Task 2 Pipeline Complete.")

if __name__ == "__main__":
    main()
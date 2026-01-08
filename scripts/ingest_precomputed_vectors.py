# scripts/ingest_precomputed_vectors.py
import os
import logging
import argparse
import pandas as pd
from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Ingest pre-computed embeddings into FAISS.")
    # Default input path points to where you said the file is: data/processed/ or data/raw/
    parser.add_argument("--input", type=str, default="data/processed/complaint_embeddings.parquet", help="Path to pre-computed parquet.")
    parser.add_argument("--output_dir", type=str, default="vector_store/full_faiss_index", help="Output FAISS index directory.")
    parser.add_argument("--batch_size", type=int, default=50000, help="Number of rows to process per batch.")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 1. Validation
    if not os.path.exists(args.input):
        logger.error(f"Input file not found: {args.input}")
        return

    # 2. Load Data
    logger.info(f"Loading pre-computed parquet from {args.input}...")
    try:
        # We load the whole dataframe. 1.37M rows is manageable in RAM (approx 2-3GB) 
        # provided we don't duplicate it too many times during processing.
        df = pd.read_parquet(args.input)
    except Exception as e:
        logger.error(f"Failed to read parquet file: {e}")
        return
    
    logger.info(f"Loaded {len(df):,} rows. Verifying columns...")

    # 3. Column Check (Based on your Notebook findings)
    required_cols = ['document', 'embedding', 'metadata']
    if not all(col in df.columns for col in required_cols):
        logger.error(f"Column mismatch! Expected {required_cols}, found {df.columns.tolist()}")
        return

    # 4. Initialize Embedding Model Wrapper
    # LangChain needs this class to know the vector dimension (384), 
    # even though we won't strictly use it to calculate new embeddings here.
    logger.info("Initializing Embedding Model wrapper (all-MiniLM-L6-v2)...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 5. Batch Processing
    total_rows = len(df)
    vectorstore = None
    
    logger.info(f"Starting ingestion in batches of {args.batch_size}...")

    try:
        for i in tqdm(range(0, total_rows, args.batch_size), desc="Indexing Batches"):
            # Slice the dataframe
            batch = df.iloc[i : i + args.batch_size]
            
            # Extract lists
            texts = batch['document'].tolist()
            embeddings = batch['embedding'].tolist()
            metadatas = batch['metadata'].tolist() # Already a list of dicts
            
            # Zip text and embeddings together as required by FAISS.from_embeddings
            text_embeddings = list(zip(texts, embeddings))

            if vectorstore is None:
                # Create the index with the first batch
                vectorstore = FAISS.from_embeddings(
                    text_embeddings=text_embeddings,
                    embedding=embedding_model,
                    metadatas=metadatas
                )
            else:
                # Add subsequent batches
                vectorstore.add_embeddings(
                    text_embeddings=text_embeddings,
                    metadatas=metadatas
                )
        
        # 6. Save
        logger.info(f"Saving full index to {args.output_dir}...")
        vectorstore.save_local(args.output_dir)
        logger.info("✅ Ingestion complete. Vector store ready.")

    except Exception as e:
        logger.critical(f"Process failed during ingestion: {e}")
        raise

if __name__ == "__main__":
    main()
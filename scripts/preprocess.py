import sys
import os
import logging
import argparse
import pandas as pd
from pathlib import Path
import time

# --- Setup Project Path ---
# CRITICAL: This must run BEFORE importing from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.data_loading import load_and_filter_complaints
    from src.cleaning import clean_narrative
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import modules. {e}")
    print("Ensure you are running this script from the project root or 'scripts/' folder.")
    sys.exit(1)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Preprocess CFPB complaints data for RAG pipeline.")
    
    parser.add_argument(
        "--input", 
        type=str, 
        default="data/raw/complaints.csv", 
        help="Path to the raw CSV file."
    )
    
    parser.add_argument(
        "--output_dir", 
        type=str, 
        default="data/processed", 
        help="Directory to save processed files."
    )
    
    return parser.parse_args()

def main():
    try:
        # --- Initialization ---
        args = parse_args()
        input_path = Path(args.input)
        output_dir = Path(args.output_dir)
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        start_time = time.time()
        
        # --- Step 1: Load and Filter ---
        logger.info(f"Starting pipeline. Reading from: {input_path}")
        
        if not input_path.exists():
            logger.error(f"Input file not found: {input_path}")
            sys.exit(1)

        # We keep this specific try/except because data loading is the most fragile part
        try:
            df, total_scanned = load_and_filter_complaints(input_path, verbose=False)
        except Exception as e:
            logger.error(f"Failed to load/filter data: {e}")
            raise  # Re-raise to exit via the main error handler

        logger.info(f"Data loaded. Scanned: {total_scanned:,} | Retained: {len(df):,}")
        
        if df.empty:
            logger.warning("No data retained after filtering. Please check your regex patterns or input file.")
            sys.exit(0)

        # --- Step 2: Text Cleaning ---
        logger.info("Applying text cleaning and normalization...")
        
        try:
            # Apply the imported cleaning function
            df['cleaned_narrative'] = df['Consumer complaint narrative'].apply(clean_narrative)
            
            # Calculate word counts
            df['word_count'] = df['cleaned_narrative'].str.split().str.len()
        except Exception as e:
            logger.error(f"Error during text cleaning/processing: {e}")
            raise

        # --- Step 3: Saving ---
        logger.info("Saving processed data...")
        
        try:
            # Save Parquet
            parquet_path = output_dir / "filtered_complaints.parquet"
            df.to_parquet(parquet_path, index=False)
            logger.info(f"Saved Parquet: {parquet_path}")
            
            # Save CSV
            csv_path = output_dir / "filtered_complaints.csv"
            df.to_csv(csv_path, index=False)
            logger.info(f"Saved CSV: {csv_path}")
            
        except (IOError, OSError) as e:
            logger.error(f"Failed to save output files. Check permissions or disk space. Error: {e}")
            sys.exit(1)
        
        # --- Final Stats ---
        elapsed = (time.time() - start_time) / 60
        logger.info(f"Pipeline finished successfully in {elapsed:.1f} minutes.")

    except KeyboardInterrupt:
        logger.warning("\nProcess interrupted by user. Exiting.")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"An unexpected error occurred in the pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
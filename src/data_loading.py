# src/data_loading.py
import pandas as pd
from pathlib import Path
from typing import Tuple, List

# Define constants for defaults
DEFAULT_CHUNK_SIZE = 200_000
DEFAULT_TARGET_PATTERN = r"(?i)credit card|prepaid card|personal loan|savings account|money transfer"
DEFAULT_COLS = [
    'Date received', 'Product', 'Sub-product', 'Issue', 'Sub-issue', 
    'Consumer complaint narrative', 'Company', 'State', 'Complaint ID'
]

def load_and_filter_complaints(
    file_path: Path, 
    target_pattern: str = DEFAULT_TARGET_PATTERN,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    verbose: bool = True
) -> Tuple[pd.DataFrame, int]:
    """
    Reads a CSV in chunks, filters for specific products, and removes empty narratives.
    
    Args:
        file_path (Path): Path to the raw CSV file.
        target_pattern (str): Regex pattern to filter 'Product' column.
        chunk_size (int): Number of rows to read per chunk.
        verbose (bool): If True, prints progress.

    Returns:
        Tuple[pd.DataFrame, int]: 
            - The filtered DataFrame containing all matching rows.
            - The total number of raw rows scanned.
    """
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found at: {file_path}")

    chunks: List[pd.DataFrame] = []
    total_rows = 0
    kept_rows = 0
    
    if verbose:
        print(f"Starting chunked read from {file_path.name}...")

    # Iterate through the file
    reader = pd.read_csv(
        file_path, 
        chunksize=chunk_size, 
        usecols=DEFAULT_COLS,
        dtype=str,
        on_bad_lines='skip'
    )

    for i, chunk in enumerate(reader):
        total_rows += len(chunk)
        
        # 1. Drop rows with missing narratives (Memory optimization)
        chunk = chunk.dropna(subset=['Consumer complaint narrative'])
        
        if chunk.empty:
            continue

        # 2. Filter by Product
        mask = chunk["Product"].str.contains(target_pattern, regex=True, na=False)
        filtered_chunk = chunk[mask]
        
        if not filtered_chunk.empty:
            chunks.append(filtered_chunk)
            kept_rows += len(filtered_chunk)
        
        if verbose:
            print(f"Chunk {i+1:3d} | scanned: {total_rows:9,d} | kept: {kept_rows:7,d}")

    # Combine results
    if chunks:
        df_filtered = pd.concat(chunks, ignore_index=True)
    else:
        df_filtered = pd.DataFrame(columns=DEFAULT_COLS)
        if verbose:
            print("Warning: No data matched your filters.")

    return df_filtered, total_rows
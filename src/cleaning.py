# src/cleaning.py
import re
import pandas as pd

def clean_narrative(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    if text.startswith("b'") or text.startswith('b"'):
        text = text[2:-1]
    text = text.lower()
    text = re.sub(r'(\d{2}|\w{2})/(\d{2}|\w{2})/(\d{4}|\w{4})', '[DATE]', text)
    text = re.sub(r'\b(x{2,})\b', '[REDACTED]', text)
    
    boilerplate = [
        r'^i am writing to file a complaint',
        r'^to whom it may concern',
        r'^complaint against',
        r'^this is a complaint regarding',
    ]
    for pattern in boilerplate:
        text = re.sub(pattern, '', text, flags=re.I)
    
    text = re.sub(r'\s+', ' ', text).strip()
    return text
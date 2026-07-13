import re
import string
import pandas as pd

def clean_text(text):
    """Lowercase, remove HTML tags, punctuation, and extra whitespace"""
    text = str(text)
    text = re.sub(r"<.*?>", " ", text)          # remove HTML tags
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def combine_text_fields(df):
    """Merge multiple text columns into one combined text field for the model"""
    text_columns = ["title", "company_profile", "description", "requirements", "benefits"]
    for col in text_columns:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("")
    df["combined_text"] = df[text_columns].agg(" ".join, axis=1)
    df["combined_text"] = df["combined_text"].apply(clean_text)
    return df
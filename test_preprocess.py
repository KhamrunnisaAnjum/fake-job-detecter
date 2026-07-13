import pandas as pd
from preprocess import combine_text_fields

df = pd.read_csv("data/fake_job_postings.csv")
df = combine_text_fields(df)
print(df[["combined_text", "fraudulent"]].head())
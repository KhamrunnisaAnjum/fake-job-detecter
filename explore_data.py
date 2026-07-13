import pandas as pd

df = pd.read_csv("data/fake_job_postings.csv")
print("Shape (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nHow many fake vs real postings:")
print(df["fraudulent"].value_counts())
print("\nMissing values per column:")
print(df.isnull().sum())
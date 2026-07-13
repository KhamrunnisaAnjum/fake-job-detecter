import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
from preprocess import combine_text_fields

# 1. Load and clean data
df = pd.read_csv("data/fake_job_postings.csv")
df = combine_text_fields(df)

# 2. Convert text to numbers
vectorizer = TfidfVectorizer(max_features=3000, stop_words="english")
X = vectorizer.fit_transform(df["combined_text"])
y = df["fraudulent"]

# 3. Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# stratify=y keeps the same fake/real ratio in both train and test sets — important
# because this dataset is imbalanced (very few fake postings compared to real ones)

# 4. Train the model
model = LogisticRegression(max_iter=1000, class_weight="balanced")
# class_weight="balanced" tells the model to pay extra attention to the rare
# fraudulent class, instead of just always predicting "real" (which would still
# look ~95% accurate but be useless)
model.fit(X_train, y_train)

# 5. Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 6. Save model and vectorizer
with open("model/classifier.pkl", "wb") as f:
    pickle.dump(model, f)
with open("model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
print("\nModel saved successfully!")
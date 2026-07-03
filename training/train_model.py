# training/train_model.py
"""
Train TF-IDF + classifiers on the provided Phishing_Email.csv and save artifacts.
Expected CSV columns: 'Email Text' (text) and 'Email Type' (labels like 'Safe Email' / 'Phishing Email').
"""

import os
import re
import string
import pickle
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "Phishing_Email.csv"
OUT_DIR = ROOT / "models"
OUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading dataset:", DATA_PATH)
df = pd.read_csv(DATA_PATH)
print("Columns:", df.columns.tolist())

# explicit columns in the uploaded file
TEXT_COL = "Email Text"
LABEL_COL = "Email Type"

if TEXT_COL not in df.columns or LABEL_COL not in df.columns:
    raise ValueError(f"CSV must contain columns '{TEXT_COL}' and '{LABEL_COL}'")

# map label to 0/1
def map_label(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip().lower()
    if "phish" in s or "spam" in s or "malicious" in s:
        return 1
    if "safe" in s or "legit" in s or "ham" in s or "normal" in s or "clean" in s:
        return 0
    # fallback numeric
    try:
        v = float(s)
        if v == 1.0: return 1
        if v == 0.0: return 0
    except:
        pass
    return np.nan

df2 = df[[TEXT_COL, LABEL_COL]].rename(columns={TEXT_COL: "text", LABEL_COL: "label_raw"}).copy()
df2["label"] = df2["label_raw"].apply(map_label)

print("Raw label counts (head):")
print(df2["label_raw"].value_counts().head(20))
print("Mapped counts (after map_label):")
print(df2["label"].value_counts(dropna=False).head(20))

df2 = df2.dropna(subset=["text", "label"]).copy()
df2["label"] = df2["label"].astype(int)
print("Dataset size after drop:", len(df2))
print("Class distribution:\n", df2["label"].value_counts())

# simple cleaning
def clean_text(t):
    if not isinstance(t, str):
        t = str(t)
    t = t.lower()
    t = re.sub(r"http\S+|www\.\S+", " ", t)
    t = re.sub(r"\S+@\S+", " ", t)
    t = re.sub(r"\d+", " ", t)
    t = t.translate(str.maketrans("", "", string.punctuation))
    t = re.sub(r"\s+", " ", t).strip()
    return t

df2["clean_text"] = df2["text"].apply(clean_text)

X = df2["clean_text"].values
y = df2["label"].values

# stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# configure a reasonably small vectorizer for speed
tfidf = TfidfVectorizer(ngram_range=(1,2), max_df=0.95, min_df=3, max_features=5000)

pipe_lr = Pipeline([
    ("tfidf", tfidf),
    ("clf", LogisticRegression(max_iter=1000, solver="liblinear"))
])

pipe_svm = Pipeline([
    ("tfidf", tfidf),
    ("clf", LinearSVC(max_iter=10000))
])

print("Training Logistic Regression...")
pipe_lr.fit(X_train, y_train)

print("Training LinearSVC...")
pipe_svm.fit(X_train, y_train)

def eval_model(pipe, X_test, y_test, name):
    y_pred = pipe.predict(X_test)
    print(f"\n=== {name} ===")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("F1:", f1_score(y_test, y_pred))
    print("Classification report:\n", classification_report(y_test, y_pred, digits=4))
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
    return f1_score(y_test, y_pred)

f1_lr = eval_model(pipe_lr, X_test, y_test, "LogisticRegression")
f1_svm = eval_model(pipe_svm, X_test, y_test, "LinearSVC")

if f1_svm > f1_lr:
    best = pipe_svm
    best_name = "LinearSVC"
else:
    best = pipe_lr
    best_name = "LogisticRegression"

print("\nBest model chosen:", best_name)

# Save artifacts
with open(OUT_DIR / "pipeline_best.pkl", "wb") as f:
    pickle.dump(best, f)

with open(OUT_DIR / "pipeline_lr.pkl", "wb") as f:
    pickle.dump(pipe_lr, f)

with open(OUT_DIR / "pipeline_svm.pkl", "wb") as f:
    pickle.dump(pipe_svm, f)

# Save vectorizer and classifier separately (handy for backend)
with open(OUT_DIR / "vectorizer.pkl", "wb") as f:
    pickle.dump(best.named_steps["tfidf"], f)
with open(OUT_DIR / "classifier.pkl", "wb") as f:
    pickle.dump(best.named_steps["clf"], f)

print("Saved artifacts to:", OUT_DIR)
print([p.name for p in OUT_DIR.glob("*")])

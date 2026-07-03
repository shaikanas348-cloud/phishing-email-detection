# backend/ml_model.py
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"

PIPELINE_PATH = MODEL_DIR / "pipeline_best.pkl"
VECT_PATH = MODEL_DIR / "vectorizer.pkl"
CLF_PATH = MODEL_DIR / "classifier.pkl"

# you will create models/ by running train_model.py
_pipeline = None

def load_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline
    if PIPELINE_PATH.exists():
        with open(PIPELINE_PATH, "rb") as f:
            _pipeline = pickle.load(f)
        return _pipeline
    # fallback: try vectorizer + classifier
    if VECT_PATH.exists() and CLF_PATH.exists():
        with open(VECT_PATH, "rb") as f:
            vec = pickle.load(f)
        with open(CLF_PATH, "rb") as f:
            clf = pickle.load(f)
        _pipeline = (vec, clf)
        return _pipeline
    raise RuntimeError("No model artifacts found in models/ - run training first")

def predict(text):
    """
    Returns tuple (label_str, score_if_available)
    label_str will be 'Phishing' or 'Safe'
    """
    pipe = load_pipeline()
    # if pipeline object (sklearn Pipeline)
    if hasattr(pipe, "predict"):
        pred = pipe.predict([text])[0]
        # try probability if available
        score = None
        if hasattr(pipe, "predict_proba"):
            score = pipe.predict_proba([text])[0][1]
        return ("Phishing" if int(pred) == 1 else "Safe", float(score) if score is not None else None)
    else:
        # (vec, clf)
        vec, clf = pipe
        X = vec.transform([text])
        pred = clf.predict(X)[0]
        score = None
        if hasattr(clf, "predict_proba"):
            score = clf.predict_proba(X)[0][1]
        return ("Phishing" if int(pred) == 1 else "Safe", float(score) if score is not None else None)

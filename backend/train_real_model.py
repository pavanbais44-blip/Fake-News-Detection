import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
import re

# Premium Dataset URL for robust training (Classic Fake vs Real)
DATASET_URL = "https://raw.githubusercontent.com/lutzhamel/fake-news/master/data/fake_or_real_news.csv"

def train_professional_model():
    print(f"[STAGE 1] Loading dataset from {DATASET_URL}...")
    try:
        df = pd.read_csv(DATASET_URL)
        print(f"[SUCCESS] Dataset loaded: {len(df)} samples.")
        
        # Combine title and text to catch 'clickbait' patterns in titles
        df['total_content'] = df['title'].fillna('') + " " + df['text'].fillna('')
        df = df.dropna(subset=['total_content', 'label'])
        
        # Normalize labels
        df['label'] = df['label'].astype(str).str.capitalize()
        
        print("[STAGE 2] N-GRAM Analysis & Feature Selection...")
        # ngram_range=(1,2) extracts phrases like "fake claim", "breaking report"
        vectorizer = TfidfVectorizer(
            stop_words='english', 
            max_df=0.7, 
            ngram_range=(1, 2), 
            max_features=50000 # Increased for n-grams
        )
        
        X = vectorizer.fit_transform(df['total_content'])
        y = df['label']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("[STAGE 3] Neural Training Initialization...")
        classifier = PassiveAggressiveClassifier(max_iter=100, C=1.0)
        classifier.fit(X_train, y_train)
        
        # Performance metrics
        acc = accuracy_score(y_test, classifier.predict(X_test))
        print(f"[METRICS] Intelligence accuracy: {acc*100:.2f}%")
        
        print("[STAGE 4] Dumping Intelligence Hub (Binary weights)...")
        joblib.dump(classifier, 'model.pkl')
        joblib.dump(vectorizer, 'vectorizer.pkl')
        
        print("\n[SUCCESS] UPGRADE COMPLETE: TruthGuard Engine version 2.0 active.")

    except Exception as e:
        print(f"[ERROR] Failed: {e}")

if __name__ == "__main__":
    train_professional_model()

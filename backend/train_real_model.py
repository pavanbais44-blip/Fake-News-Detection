import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import joblib
import os

# URLs to popular fake news open datasets
DATASET_URL = "https://raw.githubusercontent.com/lutzhamel/fake-news/master/data/fake_or_real_news.csv"

def train_model():
    print(f"Loading real-world dataset from {DATASET_URL}...")
    try:
        # Load the dataset
        df = pd.read_csv(DATASET_URL)
        print(f"Dataset loaded! Total articles: {len(df)}")
        
        # In this dataset, the columns are typically: id, title, text, label
        # Labels are usually 'FAKE' and 'REAL'
        if 'text' not in df.columns or 'label' not in df.columns:
            print("Unexpected dataset structure. Columns:", df.columns)
            return
            
        # Clean data
        df = df.dropna(subset=['text', 'label'])
        df['label'] = df['label'].astype(str).str.capitalize()  # Ensure 'Fake' or 'Real' format
        
        print("Training TF-IDF Vectorizer on real news data (this may take a moment)...")
        # Initialize a TfidfVectorizer
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
        tfidf_train = tfidf_vectorizer.fit_transform(df['text'])
        
        print("Training Passive-Aggressive Classifier...")
        # Initialize a PassiveAggressiveClassifier
        pac = PassiveAggressiveClassifier(max_iter=50)
        pac.fit(tfidf_train, df['label'])
        
        # Save the model
        joblib.dump(pac, 'model.pkl')
        joblib.dump(tfidf_vectorizer, 'vectorizer.pkl')
        
        print("✅ Massive real-world model successfully trained and saved!")
        print("The backend will automatically start using it for upcoming predictions.")

    except Exception as e:
        print(f"Failed to load dataset or train model: {e}")

if __name__ == "__main__":
    train_model()

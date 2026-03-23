import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import joblib
import os

print("Creating a small synthetic dataset for demonstration purposes...")

# A tiny dataset to bootstrap the ML model so it's not simply 'random'
data = {
    "text": [
        "Breaking: Alien base found on the dark side of the moon by secret rover.",
        "Scientists discover a new species of frog in the Amazon rainforest.",
        "Local man wins lottery, gives it all to stray dogs.",
        "Shocking! Miracle pill guarantees you lose 50 pounds in 2 days without diet or exercise!",
        "Government to increase taxes by 500% tomorrow, insider says.",
        "The stock market saw a slight increase in technology sectors this quarter.",
        "Drink this one simple weird liquid to cure all known diseases.",
        "Global leaders met in Geneva to discuss climate change initiatives.",
        "Man claims to have traveled to the year 3000 and brought back a sports almanac.",
        "NASA launches new satellite to monitor weather patterns and ocean currents.",
        "You won't believe what this celebrity did! Click here to find out!",
        "Studies show that regular exercise and a balanced diet improve overall health.",
        "Secret society controls the world's weather using giant microwaves.",
        "Local library opens new wing dedicated to historical archives.",
        "World's first flying car expected to hit the market next month for only $1000.",
        "New smartphone released with upgraded camera and longer battery life.",
        "Doctors hate him! See how he stopped aging with this one fruit.",
        "City council approves new park construction in the downtown area.",
        "Ghosts confirmed real by top scientists at major university.",
        "New recipe book becomes bestseller after positive reviews."
    ],
    "label": [
        "Fake", "Real", "Real", "Fake", "Fake",
        "Real", "Fake", "Real", "Fake", "Real",
        "Fake", "Real", "Fake", "Real", "Fake",
        "Real", "Fake", "Real", "Fake", "Real"
    ]
}

df = pd.DataFrame(data)

print("Training TF-IDF Vectorizer...")
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = tfidf_vectorizer.fit_transform(df['text'])

print("Training Passive-Aggressive Classifier...")
pac = PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train, df['label'])

print("Saving model and vectorizer to disk...")
joblib.dump(pac, 'model.pkl')
joblib.dump(tfidf_vectorizer, 'vectorizer.pkl')

print("Model successfully trained and saved as model.pkl and vectorizer.pkl!")

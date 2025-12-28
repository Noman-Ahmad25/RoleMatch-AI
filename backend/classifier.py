import pandas as pd 
import joblib 
import os 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATA_FILE = "resumes.csv"
MODEL_FILE = "model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

def train_model():
    print("🔄 Training new model...")

    if not os.path.exists(DATA_FILE):
        print(f"❌ Error: {DATA_FILE} not found.")
        return None, None
    
    df = pd.read_csv(DATA_FILE)
    
    # Check if dataset is empty or too small
    if df.empty:
        print("❌ Error: CSV is empty.")
        return None, None

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df["resume"])
    y = df["role"]

    # --- CHANGE: Train on EVERYTHING (No Split) ---
    # We are feeding 100% of data to the model so it learns patterns better.
    model = LogisticRegression(C=100.0)
    model.fit(X, y)

    print(f"✅ Training Complete. Model learned from {len(df)} records.")

    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print("💾 Model saved to disk")

    return model, vectorizer

def load_model():
    if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
        print("📂 Loading existing model...")
        model = joblib.load(MODEL_FILE)
        vectorizer = joblib.load(VECTORIZER_FILE)
        return model, vectorizer
    else: 
        return train_model()
    
if __name__ == "__main__":
    model, vectorizer = load_model()
        
    if model:
        print("\n--- AI Resume Classifier Ready ---")
        
        while True:
            user_input = input("\nPaste resume text (or type 'exit'): ")
            if user_input.lower() == 'exit':
                break
            
            vec = vectorizer.transform([user_input])
            pred = model.predict(vec)[0]
            proba = model.predict_proba(vec).max() * 100

            print(f"🎯 Role: {pred}")
            print(f"📊 Confidence: {proba:.2f}%")
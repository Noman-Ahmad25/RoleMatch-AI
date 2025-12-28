from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

try:
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Model loaded successfully!")
except:
    print("❌ Error: model.pkl not found. Run classifier.py first!")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('resume', '')

    if not text:
        return jsonify({"error":"no text provided"})
    
    vec= vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    proba = model.predict_proba(vec).max() * 100
    return jsonify({
        "role": prediction,
        "confidence": round(proba,2)
    })
if __name__ =='__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

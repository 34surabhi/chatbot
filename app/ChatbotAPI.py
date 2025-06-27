# backend/app.py
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model (mock for now)
try:
    model = pickle.load(open("model/chatbot_model.pkl", "rb"))
except:
    model = None

@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    reply = f"You said: {user_msg}"  # placeholder logic
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

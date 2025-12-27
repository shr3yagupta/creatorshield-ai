from flask import Flask, render_template, request, jsonify
import os, requests, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
    f"?key={GEMINI_API_KEY}"
)

def call_gemini(prompt):
    payload = {
        "contents":[
            {"parts":[{"text":prompt}]}
        ]
    }

    res = requests.post(MODEL_URL, json=payload).json()

    try:
        text = res["candidates"][0]["content"]["parts"][0]["text"]
        return text
    except:
        return "AI failed to analyze."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    message = data.get("text", "")

    prompt = f"""
You are a cybersecurity expert. Analyze this message for scam risk.
Explain clearly and simply.

Message:
{message}

Return response like:
Risk Level: High/Medium/Low
Reason:
What should user do next:
"""

    ai_response = call_gemini(prompt)

    return jsonify({"ai": ai_response})


if __name__ == "__main__":
    app.run(debug=True)

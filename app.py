from flask import Flask, render_template, request, jsonify
import os, requests, json, re
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
        "contents":[{"parts":[{"text":prompt}]}]
    }

    res = requests.post(MODEL_URL, json=payload).json()

    try:
        text = res["candidates"][0]["content"]["parts"][0]["text"]
        return text
    except:
        return "{}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    message = data.get("text","")

    prompt = f"""
You are a cybersecurity expert.

Analyze the message and return STRICT JSON ONLY.
NO MARKDOWN. NO TEXT.

Return EXACTLY THIS STRUCTURE:

{{
 "risk_level":"Low | Medium | High",
 "attack_type":"Phishing | Impersonation | Malware | Unknown",
 "platform_detected":"Instagram | YouTube | Gmail | WhatsApp | Unknown",
 "risky_elements":[],
 "emergency_flag": true/false,
 "explanation":"one paragraph",
 "suggested_action":"clear step user should take",
 "prevention_steps":"how to avoid in future"
}}

Message:
\"\"\"{message}\"\"\"
"""

    response = call_gemini(prompt)

    # try loading json safely
    try:
        result = json.loads(response)
    except:
        # fallback to regex json extraction if Gemini adds garbage
        match = re.search(r"\{[\s\S]*\}", response)
        if match:
            try:
                result = json.loads(match.group())
            except:
                result = {}
        else:
            result = {}

    if not result:
        result = {
            "risk_level":"Low",
            "attack_type":"Unknown",
            "platform_detected":"Unknown",
            "risky_elements":[],
            "emergency_flag": False,
            "explanation":"Fallback safe response. AI could not evaluate.",
            "suggested_action":"Stay alert. Do not click unknown links.",
            "prevention_steps":"Enable 2FA and verify before responding."
        }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

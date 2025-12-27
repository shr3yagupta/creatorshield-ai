from flask import Flask, render_template, request, jsonify
import os, requests, json, re
from dotenv import load_dotenv
from PIL import Image
import pytesseract

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
        "contents": [{"parts": [{"text": prompt}]}]
    }

    r = requests.post(MODEL_URL, json=payload).json()

    if "candidates" not in r:
        return {}

    txt = r["candidates"][0]["content"]["parts"][0]["text"]

    try:
        return json.loads(txt)
    except:
        m = re.search(r"\{[\s\S]*\}", txt)
        if m:
            return json.loads(m.group())
        return {}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")

    prompt = f"""
You are a cybersecurity assistant. Analyze this message for phishing/scam.

Return ONLY JSON like this:

{{
 "risk_level":"Low | Medium | High",
 "attack_type":"type",
 "platform_detected":"Instagram | YouTube | Gmail | WhatsApp | Unknown",
 "risky_elements":[],
 "emergency_flag": true/false,
 "explanation":"short explanation",
 "suggested_action":"short next steps"
}}
Message:
\"\"\"{text}\"\"\"
"""

    result = call_gemini(prompt)

    if not result:
        result = {
            "risk_level":"Low",
            "attack_type":"Unknown",
            "platform_detected":"Unknown",
            "risky_elements":[],
            "emergency_flag": False,
            "explanation":"Fallback safe result",
            "suggested_action":"Stay alert"
        }

    return jsonify(result)


# ================= SCREENSHOT ANALYSIS =================
@app.route("/image", methods=["POST"])
def image_scan():
    img = request.files["image"]
    img_path = "temp.png"
    img.save(img_path)

    text = pytesseract.image_to_string(Image.open(img_path))

    request.json = {
        "text": text
    }
    return analyze()


if __name__ == "__main__":
    app.run(debug=True)


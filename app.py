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
        "contents": [{"parts":[{"text":prompt}]}]
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
    text = data.get("text","")

    prompt = f"""
You are a cybersecurity assistant.

Analyze this message. Return ONLY JSON.

{{
 "risk_level":"Low | Medium | High",
 "attack_type":"type",
 "platform_detected":"Instagram | YouTube | Gmail | WhatsApp | Unknown",
 "risky_elements":[],
 "emergency_flag": true/false,
 "explanation":"short explanation",
 "suggested_action":"short next steps",
 "prevention_steps":"ways to stay safe"
}}

Rules:
- ONLY JSON
- No markdown

Message:
\"\"\"{text}\"\"\""""

    result = call_gemini(prompt)

    if not result:
        result = {
            "risk_level":"Low",
            "attack_type":"Unknown",
            "platform_detected":"Unknown",
            "risky_elements":[],
            "emergency_flag": False,
            "explanation":"Fallback safe result",
            "suggested_action":"Stay alert",
            "prevention_steps":"Enable 2FA"
        }

    return jsonify(result)


# ================= SCREENSHOT OCR =================
@app.route("/image", methods=["POST"])
def image():
    img = request.files["image"]
    img_path = "temp.png"
    img.save(img_path)

    text = pytesseract.image_to_string(Image.open(img_path))

    fake_req = {"text": text}
    return analyze_screenshot(fake_req)


def analyze_screenshot(data):
    text = data.get("text","")

    prompt = f"""
You are a cybersecurity assistant.

Analyze this message/image extracted text. Return ONLY JSON:

{{
 "risk_level":"Low | Medium | High",
 "attack_type":"type",
 "platform_detected":"Instagram | YouTube | Gmail | WhatsApp | Unknown",
 "risky_elements":[],
 "emergency_flag": true/false,
 "explanation":"short explanation",
 "suggested_action":"short next steps",
 "prevention_steps":"ways to stay safe"
}}

Content:
{text}
"""

    result = call_gemini(prompt)
    return jsonify(result)


# ================= RECOVERY GUIDE =================
@app.route("/recovery", methods=["POST"])
def recovery():
    return jsonify({
        "steps":[
            "Immediately change your account password",
            "Enable Two Factor Authentication",
            "Check login activity and remove unknown devices",
            "Revoke suspicious third-party app permissions",
            "Warn followers not to click recent suspicious links",
            "File account recovery request with the platform"
        ]
    })

@app.route("/link", methods=["POST"])
def link_scan():
    data = request.json
    url = data.get("url","").lower()

    risky_keywords = [
        "verify", "verification", "free", "gift",
        "instagram-support", "youtube-partner",
        "claim", "bonus", "payment", "login"
    ]

    suspicious = any(word in url for word in risky_keywords)

    result = {
        "url": url,
        "risk_level": "High" if suspicious else "Low",
        "explanation": "Suspicious scam pattern detected" if suspicious else "No strong scam pattern detected",
        "suggested_action": "Do NOT click if sent by unknown person" if suspicious else "Looks safe but stay alert"
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

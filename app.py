from flask import Flask, render_template, request, jsonify
import os, requests, json, re
from dotenv import load_dotenv
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename
import speech_recognition as sr

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
    f"?key={GEMINI_API_KEY}"
)


def call_gemini(prompt):
    payload = {"contents": [{"parts":[{"text":prompt}]}] }
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
    lang = data.get("language","english")

    lang_rule = "Respond completely in English."
    if lang=="hindi":
        lang_rule="पूरी प्रतिक्रिया हिंदी में दो। किसी भी भाग में अंग्रेज़ी का प्रयोग न करो।"

    prompt = f"""
You are a cybersecurity assistant. Analyze this message.
Return ONLY JSON.

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
- Hindi only if Hindi selected
{lang_rule}

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
            "suggested_action":"Stay alert",
            "prevention_steps":"Enable 2FA"
        }

    return jsonify(result)



@app.route("/image",methods=["POST"])
def image():
    img = request.files["image"]
    img_path="temp.png"
    img.save(img_path)
    text = pytesseract.image_to_string(Image.open(img_path))
    return analyze_text(text)


def analyze_text(txt):
    fake_request={"json":lambda:{"text":txt,"language":"english"}}
    with app.test_request_context():
        request.json=fake_request["json"]()
        return analyze()



@app.route("/voice", methods=["POST"])
def voice():
    try:
        file = request.files["audio"]
        filename = secure_filename("voice_temp.wav")
        file.save(filename)

        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_text = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_text)
        except:
            return jsonify({"error":"Could not understand the audio clearly"})

        fake_request = {
            "text": text,
            "language": "english"
        }

        with app.test_request_context():
            request.json = fake_request
            return analyze()

    except Exception as e:
        return jsonify({"error": str(e)})



@app.route("/recovery",methods=["POST"])
def recovery():
    return jsonify({"steps":[
        "Change password immediately",
        "Enable 2FA",
        "Check login activity",
        "Remove unknown devices",
        "Report suspicious account"
    ]})



@app.route("/trending",methods=["POST"])
def trending():
    return jsonify({"scams": "Instagram verification scam, YouTube brand impersonation, WhatsApp prize scam" })



@app.route("/global-trends", methods=["POST"])
def global_trends():
    prompt = """
You are a cybersecurity intelligence system.
Return ONLY JSON.

Give top 5 currently active scam threats worldwide targeting:
- Creators
- Influencers
- YouTube / Instagram
- Small creators
- General internet users

Return format ONLY:

{
 "trends":[
  {
   "title":"short scam name",
   "platform":"Instagram | YouTube | WhatsApp | Email | Global",
   "risk":"Low | Medium | High",
   "region":"Global | India | Asia | US",
   "description":"short explanation"
  }
 ]
}

Rules:
- ONLY JSON
- No markdown
- No extra commentary
"""

    payload = {"contents":[{"parts":[{"text":prompt}]}]}
    r = requests.post(MODEL_URL, json=payload).json()

    if "candidates" not in r:
        return jsonify({"trends":[]})

    txt = r["candidates"][0]["content"]["parts"][0]["text"]

    try:
        return jsonify(json.loads(txt))
    except:
        m = re.search(r"\{[\s\S]*\}", txt)
        if m:
            return jsonify(json.loads(m.group()))

    return jsonify({"trends":[]})



@app.route("/chat", methods=["POST"])
def chat():
    user = request.json.get("message","")

    prompt=f"You are a helpful cybersecurity assistant. Reply short, friendly.\nUser: {user}"

    r = requests.post(
        MODEL_URL,
        json={"contents":[{"parts":[{"text":prompt}]}]}
    ).json()

    if "candidates" in r:
        reply=r["candidates"][0]["content"]["parts"][0]["text"]
    else:
        reply="I'm here! Tell me what happened — I'll help 😊"

    return jsonify({"reply":reply})



if __name__=="__main__":
    app.run(debug=True)

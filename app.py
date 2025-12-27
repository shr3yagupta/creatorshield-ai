from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    # Phase 4 Dummy Logic (No AI yet)
    if "password" in text.lower() or "urgent" in text.lower():
        result = {
            "risk": "High",
            "message": "This looks suspicious. It may be a scam."
        }
    else:
        result = {
            "risk": "Low",
            "message": "This message looks safe."
        }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

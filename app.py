from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Try to load Gemini
model = None
try:
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-pro")
except:
    model = None


@app.route("/")
def home():
    return "Final AI Agent Running 🤖"


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    # Try Gemini first
    if model:
        try:
            response = model.generate_content(user_input)
            return jsonify({"response": response.text})
        except Exception as e:
            print("Gemini Error:", e)

    #  Fallback Smart Logic
    msg = user_input.lower()

    if "ai" in msg:
        reply = "Artificial Intelligence (AI) enables machines to learn, think, and make decisions like humans."
    elif "techfest" in msg:
        reply = "TechFest is a technical event where students participate in coding, robotics, and innovation challenges."
    elif "cloud" in msg:
        reply = "Cloud computing allows you to run applications on remote servers like Google Cloud instead of your local system."
    elif "hello" in msg:
        reply = "Hello! I am your AI assistant. How can I help you?"
    else:
        reply = f"I understand your query: {user_input}"

    return jsonify({"response": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

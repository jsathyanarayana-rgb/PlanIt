import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with Hugging Face router and HF_TOKEN from .env
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:fireworks-ai",
            messages=[
                {"role": "system", "content": "You are PlanIt, a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message["content"]
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

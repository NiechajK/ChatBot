import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
client = OpenAI()


# Set your OpenAI API key and Organization ID here
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)
openai.organization = os.getenv("OPENAI_ORG_ID")

@app.route('/test', methods=['POST'])
def handle_test():
    user_message = request.json.get('message')
    response = {
        "reply": "This is a placeholder response. In the future, this will be a GPT-3.5 Turbo-generated reply."
    }
    return jsonify(response)

@app.route('/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Send the user's message to GPT-3.5 Turbo and get the response
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        chat_response = response['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"reply": chat_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5174)

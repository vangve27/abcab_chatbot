from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
from dotenv import load_dotenv
import logging

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

def clean_log_file(log_path):
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = []
    skip_blank = False
    for i, line in enumerate(lines):
        # If we see a line with only whitespace, and the previous line was not blank, insert 'Thinking...'
        if line.strip() == '':
            # Only insert 'Thinking...' if the previous line was not blank or 'Thinking...'
            if (i == 0 or (lines[i-1].strip() != '' and (not new_lines or new_lines[-1].strip() != 'Thinking...'))):
                new_lines.append('Thinking...\n')
            # Otherwise, skip this blank line
        else:
            new_lines.append(line)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

@app.route('/chat', methods=['POST'])
def chat():
    logging.info(f"Incoming request: {request.json}")
    data = request.json
    user_message = data.get('message', '')
    max_tokens = data.get('max_tokens', 1500)
    temperature = data.get('temperature', 0.7)
    logging.info(f"Parsed user_message: {user_message}, max_tokens: {max_tokens}, temperature: {temperature}")
    
    payload = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "system", "content": "You are an AI assistant. Always reply in English."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    logging.info(f"Payload to Abcab chatbot: {payload}")
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )
    try:
        result = response.json()
        logging.info(f"Abcab chatbot response: {result}")
        # Use 'content' if available, else first sentence of 'reasoning'
        choice = result.get('choices', [{}])[0]
        message = choice.get('message', {})
        reply = message.get('content')
        if not reply:
            reasoning = message.get('reasoning', '')
            if reasoning:
                reply = reasoning.strip()
            else:
                reply = "Sorry, I don't have a direct answer."
        # Only return the reply and the full JSON result to the frontend
        return jsonify({"reply": reply, "raw": result})
    except Exception as e:
        logging.error(f"Error parsing response: {e}")
        reply = response.text or "Error: No response from backend."
        return jsonify({"reply": reply, "raw": response.text})
    clean_log_file('chatbot.log')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

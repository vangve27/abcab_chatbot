# OpenRouter DeepSeek Abcab Chatbot

A modern web-based chatbot using OpenRouter's DeepSeek model, with a Python Flask backend and a responsive HTML/JavaScript frontend.

## Features
- Secure API key management via `.env` file
- Flask backend with detailed logging to `chatbot.log` (including 'Thinking...' for model processing gaps)
- Frontend chat UI with:
  - Full-screen, mobile-friendly layout
  - Input and Send button in a single row
  - Markdown-style formatting for bot responses (headings, lists, code, blockquotes)
  - Toggle to show the full raw JSON response from the backend log
  - Proper code formatting for code responses
- Handles DeepSeek's unique response format (uses `content` or `reasoning`)

## Prerequisites
- Python 3.8+
- An OpenRouter API key

## Setup Instructions

### 1. Clone or Download the Project
Place all files (`app.py`, `chat.html`, etc.) in a folder, e.g. `open_router`.

### 2. Rename the `.env_old` File to `.env`
In the project folder, create a file named `.env` with this content:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
Replace `your_openrouter_api_key_here` with your actual OpenRouter API key.

### 3. Install Python Dependencies
Open a terminal in the project folder and run:
```powershell
pip install flask flask-cors python-dotenv requests
```

### 4. Run the Backend Server
In the same terminal, start the Flask backend:
```powershell
python app.py
```
This will start the backend at `http://localhost:5000` and log all activity to `chatbot.log`.

### 5. Serve the Frontend
Open a new terminal in the project folder and run:
```powershell
python -m http.server 8000
```
This will serve the frontend at `http://localhost:8000/chat.html`.

### 6. Use the Chatbot
- Open your browser and go to: [http://localhost:8000/chat.html](http://localhost:8000/chat.html)
- Type your message and interact with the bot.
- Click "Show Full Raw Response" to see the full backend JSON response for each message.

## How It Works
- The backend receives your message, sends it to OpenRouter's DeepSeek model, and returns the model's reply.
- If the model's `content` is empty, the backend uses the `reasoning` field instead.
- All requests and responses are logged in `chatbot.log` for debugging. Blank lines in the log are replaced with 'Thinking...' for clarity.
- The frontend formats bot responses with markdown-like styling for readability, and code is shown in code blocks.

## Troubleshooting
- **API Key not set:** Make sure your `.env` file is present and correct.
- **CORS or network errors:** Always use `http.server` to serve the frontend, not `file://`.
- **No response or errors:** Check `chatbot.log` for details.
- **Verbose or meta responses:** This is a DeepSeek model quirk; the backend will show the full reasoning if no direct answer is given.
- **Raw response not matching:** The UI tries to match the latest backend response to your message, but if the log is out of sync, it will show the most recent one.

## Customization
- To use a different model, change the `model` field in `app.py`.
- To change the system prompt, edit the `system` message in the backend payload.
- To increase response length, raise the `max_tokens` value in `app.py`.

---

For questions or issues, check the logs or contact the author.

from flask import Flask, jsonify, render_template, request, send_file
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from pydantic import json
#from flask_cors import CORS
from gtts import gTTS
from io import BytesIO


load_dotenv(Path(__file__).with_name(".env"))
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is not set in the environment variables.")
SYSTEM_PROMPT = "You are a helpful assistant. Answer the question as best as you can but keep them short and concise. If you don't know the answer, just say that you don't know. Do not try to make up an answer."
client = genai.Client(api_key=API_KEY)

def ask(text: str) -> str:
    print(f'asking question: {text}')
    #todo: need to sanitize text to avoid injection attacks
    prompt = text.strip()
    input = [{
            "role": "user",
            "content": prompt
        }, {
            "role": "system",
            "content": SYSTEM_PROMPT
        }]
    response = client.interactions.create(
        model = "gemini-3.5-flash-lite",
        input = text
    )

    #return response.model_dump_json(indent=2)
    return response.output_text
    #return response.output[0].content[0].text
    #return text + " (This is a placeholder response. Replace this with actual API call.)"

def text_to_audio_file(text):
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

app = Flask(__name__)
#CORS(app)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/transcriptions")
def create_transcription():
    """Accept a transcript produced in the browser and return it to the caller."""
    print('create_transcription triggert')
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Expected a JSON object."), 400

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify(error="The 'text' field must be a non-empty string."), 400

    # Replace or extend this section to store the transcript or call another API.
    #return jsonify(text=text.strip(), status="received"), 201
    resp = ask(text.strip())
    return jsonify(response=resp, status="received"), 200

@app.route("/api/text-to-speech", methods=["POST"])
def text_to_speech():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "Missing 'text' field in request body"}), 400
    
    audio_file = text_to_audio_file(text)

    return send_file(audio_file, mimetype='audio/mpeg')
    """
    return (
        audio_file.getvalue(),
        200,
        {
            "Content-Type": "audio/mpeg",
            "Content-Disposition": 'attachment; filename="output.mp3"',
        },
    )
    """

if __name__ == "__main__":
    app.run(debug=True)

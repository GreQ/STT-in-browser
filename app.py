from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/transcriptions")
def create_transcription():
    """Accept a transcript produced in the browser and return it to the caller."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Expected a JSON object."), 400

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify(error="The 'text' field must be a non-empty string."), 400

    # Replace or extend this section to store the transcript or call another API.
    return jsonify(text=text.strip(), status="received"), 201


if __name__ == "__main__":
    app.run(debug=True)

# Speech to Text API

A small Flask app with a browser microphone interface. Speech recognition runs in the browser; the resulting text is sent to the Flask backend as JSON.

## Run locally

```powershell
cd C:\GreQ\projects\MSIT\greq\STTapi
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. Allow microphone access when prompted.

## API

`POST /api/transcriptions`

Request:

```json
{"text":"Hello from speech recognition"}
```

Success response (HTTP 201):

```json
{"status":"received","text":"Hello from speech recognition"}
```

`GET /api/health` returns `{"status":"ok"}`.

The current endpoint validates and echoes the transcript. Add persistence or a call to another service in `create_transcription()` when you decide where transcripts should go. Browser speech recognition support varies by browser; this app does not upload raw microphone audio or call a cloud speech service.

from fastapi import FastAPI, Body, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import io
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Esto permite que TU web pública lo use
    allow_methods=["*"],
    allow_headers=["*"],
)

# Voz por defecto: Federico (Nicaragua) - Muy natural
DEFAULT_VOICE = "es-NI-FedericoNeural"

@app.get("/wakeup")
def wake_up():
    # Endpoint ligero para despertar al servidor de Render
    return {"status": "awake", "message": "I was cured all right!"}

@app.post("/generate")
async def generate_audio(payload: dict = Body(...)):
    text = payload.get("text", "")
    voice = payload.get("voice", DEFAULT_VOICE)

    if not text:
        return Response(status_code=400)

    communicate = edge_tts.Communicate(text, voice)
    audio_stream = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])

    audio_stream.seek(0)
    return Response(content=audio_stream.read(), media_type="audio/mpeg")
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from agent import JarvisAgent
from spatial import summarize_face_landmarks

app = FastAPI(title="Jarvis Live Agent", version="0.1.0")
agent = JarvisAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



WEB_DIR = Path(__file__).resolve().parent.parent / "web"
app.mount("/web", StaticFiles(directory=str(WEB_DIR), html=True), name="web")


@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/web")

class TextTurn(BaseModel):
    transcript: str = Field(..., description="Text recognized from speech")
    face_landmarks: list[dict] | None = Field(default=None)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "agent": "JARVIS-Live"}


@app.get("/config")
async def config() -> dict:
    return {"system_prompt": agent.system_prompt()}


@app.post("/turn")
async def turn(turn_input: TextTurn) -> dict:
    spatial_summary = None
    if turn_input.face_landmarks:
        spatial_summary = summarize_face_landmarks(turn_input.face_landmarks)

    response = agent.build_text_response(turn_input.transcript, spatial_summary)
    return {"response": response, "spatial": spatial_summary}


@app.websocket("/ws/voice")
async def ws_voice(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_json(
        {
            "type": "ready",
            "message": "Voice session started. Send JSON {transcript, face_landmarks?}."
        }
    )

    try:
        while True:
            payload = await websocket.receive_json()
            transcript = payload.get("transcript", "")
            face_landmarks = payload.get("face_landmarks")
            spatial_summary = summarize_face_landmarks(face_landmarks) if face_landmarks else None
            response = agent.build_text_response(transcript, spatial_summary)
            await websocket.send_json(
                {
                    "type": "assistant_turn",
                    "response": response,
                    "spatial": spatial_summary,
                }
            )
    except WebSocketDisconnect:
        return

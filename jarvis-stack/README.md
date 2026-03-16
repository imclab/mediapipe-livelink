# JARVIS Live Voice + Multimodal Spatial Agent (Starter)

This starter gives you a **single-command install** for a live voice-capable assistant with a spatial intelligence input path (MediaPipe-style landmarks).

## What you get
- Live API (`/turn`, `/ws/voice`) for voice/chat turns.
- Spatial intelligence helper that interprets face landmarks for attention cues.
- Browser UI for mobile/Mac/PC.
- One-command install for macOS/Linux/Windows.

## One-command install
### macOS / Linux
```bash
./scripts/install.sh
```

### Windows PowerShell
```powershell
./scripts/install.ps1
```

Then open:
- http://localhost:8787

## Mobile install (button press)
1. Open the URL on your phone browser.
2. Use browser "Add to Home Screen" to install as an app icon.
3. Tap icon to launch in app-like mode.

## API
- `GET /health`
- `GET /config`
- `POST /turn`
  ```json
  {
    "transcript": "Jarvis, summarize my day",
    "face_landmarks": [{"x": 0.1, "y": 0.2, "z": -0.01}]
  }
  ```
- `WS /ws/voice` accepts the same payload shape as JSON messages.

## Production notes (Jarvis-level roadmap)
- Add real-time STT/TTS pipeline (OpenAI Realtime, Azure, Deepgram, or local Whisper + Piper).
- Add memory + tool execution graph (calendar, mail, IDE, browser automation).
- Add camera stream + full body/hand landmarks for richer spatial context.
- Add auth, per-device session encryption, and wake-word on-device mode.

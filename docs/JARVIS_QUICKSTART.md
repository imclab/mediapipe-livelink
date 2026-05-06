# Jarvis: 1-minute, always-on live voice chat (cross-platform)

> Goal: perceived **"zero-latency"** conversational voice on macOS/Windows + iOS/Android, with optional VisionOS/Quest listeners.

## Reality check (important)

True physical zero latency is impossible on networked systems. The practical target is **sub-300ms turn latency** with barge-in (interrupt anytime), which users perceive as instant.

## Fastest stack (recommended)

- **Realtime transport:** WebRTC (LiveKit Cloud)
- **LLM + speech:** OpenAI Realtime API (single stream for ASR + TTS)
- **Wake word:** Porcupine (`jarvis`) on-device
- **Always-on runtime:** background foreground-service model

This gives the shortest setup and best device coverage.

---

## 60-second setup

1. Create a LiveKit Cloud project (copy URL + API key/secret).
2. Create an OpenAI API key with Realtime access.
3. Start a minimal agent service with env vars:

```bash
export LIVEKIT_URL="wss://<your-livekit>.livekit.cloud"
export LIVEKIT_API_KEY="<key>"
export LIVEKIT_API_SECRET="<secret>"
export OPENAI_API_KEY="<openai-key>"

# one-command starter (Node)
npx @livekit/agents-cli@latest create jarvis-agent
cd jarvis-agent
npm i
npm run dev
```

4. Open LiveKit playground/web client on desktop or mobile browser and join the room.
5. Enable wake-word detector locally; stream to the room only after "Jarvis" is detected.

---

## Platform recipe

### macOS / Windows

- Use LiveKit web client (Chrome/Edge) for fastest no-install path.
- Enable echo cancellation + noise suppression.
- Keep microphone hot; gate transmit by wake word + VAD.

### iOS / Android

- Use LiveKit mobile SDK app shell (or PWA for quick demo).
- Run wake-word locally (Porcupine mobile SDK) to avoid cloud wake latency.
- Use push-to-talk fallback when OS background limits are strict.

### VisionOS / Quest (bonus monitor/watch mode)

- Join same LiveKit room from WebXR/browser client.
- Subscribe to assistant audio + captions stream.
- Optional: spatialize assistant audio for immersion.

---

## Always-on "Jarvis" behavior

- **Hot mic locally** (device-side ring buffer, never uploaded until trigger).
- **Wake word:** `jarvis`.
- **Barge-in:** if user starts speaking, interrupt TTS immediately.
- **Half-duplex fallback:** switch when echo conditions are bad.
- **Privacy guard:** wake-word and VAD entirely on-device.

## Latency budget target

- Capture + VAD: 20-40ms
- Uplink WebRTC: 20-80ms
- Realtime model first token/audio: 80-180ms
- Downlink + playout: 20-60ms
- **Total:** ~140-360ms perceived near-instant

## Production defaults

- Opus 24k mono
- 20ms packetization
- Jitter buffer min
- Server region close to user
- Endpointer tuned for short silence timeout (150-250ms)

## Fallback architecture (offline-first option)

If internet is unstable, keep wake word + VAD + command grammar on-device, and route only complex requests to cloud Realtime.


# Live Voice Chat Stack Recommendation (No API Keys)

## Bottom line
There is **no single GitHub project** that currently delivers all of these at once out-of-the-box in under 1 minute:
- always-on invisible UX,
- auto-sensing MCP tools/skills/agents,
- persistent short/medium/long-term memory,
- Claude-level coding/research quality,
- cross-device + XR support,
- and no API keys or paid tokens.

The fastest practical route is to combine open-source pieces.

## Best practical stack (free/local-first)

### 1) Open WebUI (front-end, multi-device)
- Why: easiest self-hosted chat UI, browser-based on Mac/iPhone/PC.
- Cost: free.
- Install speed: very fast with Docker.

### 2) Ollama (local model runtime)
- Why: no API key; runs local models for chat/coding.
- Cost: free (local compute only).

### 3) LiveKit + Pipecat (real-time voice pipeline)
- Why: low-latency voice I/O and turn handling for live conversation.
- Cost: free/self-host options.

### 4) MCP servers (tool integration)
- Why: standardized tool protocol ecosystem.
- Caveat: dynamic auto-discovery quality depends on host app and your MCP setup.

### 5) Memory layer (LiteLLM/DB + vector store)
- Why: explicit short/medium/long-term memory control.
- Typical: SQLite/Postgres + pgvector/Chroma + summarization worker.

## Recommendation tiers

### Fastest to usable (about 5–15 minutes)
- Open WebUI + Ollama + a local STT/TTS plugin path.
- Great for day-to-day local private usage.
- Weakness: advanced always-on orchestration and deep MCP automation need extra setup.

### Most scalable open stack
- LiveKit (RTC) + Pipecat (agent voice logic) + Ollama/vLLM + MCP + Postgres/pgvector.
- Better for many concurrent sessions and custom routing.
- Weakness: setup complexity is higher.

## Reality check on your hard constraints

- **Under 1 minute full setup:** unrealistic for complete voice+memory+MCP+XR stack.
- **No API keys/tokens:** possible if fully local/self-hosted.
- **Claude-level coding/research:** not consistently achievable offline with small local models.
- **VisionOS/Quest broad support:** browser-based WebRTC gets partway there; polished XR UX still custom work.

## If you want one repo to start with
Pick **Open WebUI** first (fastest day-to-day value), then add:
1. Ollama local model,
2. MCP servers you need,
3. Voice/RTC layer (LiveKit/Pipecat) when latency and always-on behavior matter,
4. Memory backend.

This gives the best cost/functionality ratio while staying mostly keyless and self-hosted.

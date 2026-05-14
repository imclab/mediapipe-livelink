# Jarvis Blueprint (Local-First, Modular, Agentic Swarm)

This blueprint gives you a **practical Jarvis v1** that is:

- Local-first (no API key required to start)
- Cross-device (web UI works on Mac/PC/mobile)
- Modular (providers/tools can be swapped)
- Event-driven and non-blocking (orchestrated via message bus)
- Memory-capable (short/medium/long-term layers)

> Reality check: “zero latency / zero cost / infallible” is not physically achievable. This design targets **near-zero perceived latency**, **$0 software cost**, and high resilience.

## Recommended proven stack (all free / open-source)

1. **Ollama** – local model runtime.
2. **Open WebUI** – multi-device UI + chat/voice frontend.
3. **Qdrant** – vector memory store.
4. **Redis** – fast session + short-term memory.
5. **NATS** – lightweight event bus for swarm coordination.

Why this set:
- Minimal moving parts.
- Large OSS communities.
- Clean upgrade path to enterprise deployment.

## 1-command setup (after Docker is installed)

```bash
docker compose -f jarvis/docker-compose.yml up -d
```

Then:
- Open WebUI: http://localhost:3000
- Qdrant: http://localhost:6333
- NATS monitor: http://localhost:8222

Pull a local model (example):

```bash
docker exec -it jarvis-ollama ollama pull qwen2.5:7b
```

## Architecture pattern (Agentic Team / “Genic Team” alignment)

Use a **hub-and-spoke orchestrator** with event-driven workers:

- **Conductor (Orchestrator Agent)**
  - Receives user intent.
  - Decomposes into tasks.
  - Routes to specialized agents.
  - Enforces priority/focus policy.

- **Specialist Agents (parallel, async)**
  - Coding agent
  - Sketch/ideation agent
  - Communication agent (email, summaries, follow-ups)
  - Spatial-context agent (vision/sensor ingestion)

- **Memory Fabric**
  - **Short-term**: Redis (working context, recent actions)
  - **Medium-term**: Qdrant (episodic semantic memory)
  - **Long-term**: versioned markdown/JSON knowledge base in Git

- **Reflection / Self-repair loop**
  - Each finished task emits: outcome, confidence, errors, lessons.
  - Conductor updates “Do/Don’t playbook” to reduce repeated failures.

## Cross-device strategy

- Primary UX: responsive web app (Open WebUI) available on any browser.
- Optional clients: native wrappers (Tauri / Capacitor) for desktop/mobile.
- Audio: browser WebRTC + local ASR/TTS adapter.
- AR/VR/XR: connect as additional sensor/actuator agents over NATS.

## MCP + skills integration

To satisfy dynamic tool discovery and low-friction extension:

- Run MCP tool servers as independent microservices.
- Register tool metadata in a simple `tools.registry.json`.
- Conductor loads/refreshes registry periodically (hot-swap).
- Keep each tool isolated with explicit permissions.

Suggested next add-ons (optional):
- `modelcontextprotocol` servers (filesystem, git, browser automation)
- A Node-based orchestrator service (Fastify + NATS client + MCP SDK)

## Security + governance baseline

- Local-only by default; no public ingress.
- Principle of least privilege per tool/agent.
- Signed action logs for auditability.
- Human confirmation for destructive actions.

## Operational best practices

- Keep models small for speed (7B/8B quantized) and route heavy tasks to larger model only when needed.
- Use streaming responses and speculative execution for low perceived latency.
- Add health checks + automatic restart policies (already in compose file).
- Store prompts/policies in version control and test them like code.

## Suggested 3-phase rollout

1. **Phase 1 (today)**: single-user local stack + 3 core agents (coding/comms/planning).
2. **Phase 2**: add mobile wrappers + richer memory policies + tool permission model.
3. **Phase 3**: multi-user tenancy, SSO, policy engine, and optional cloud burst.

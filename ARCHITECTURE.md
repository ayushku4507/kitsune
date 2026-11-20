# Architecture

The Electron renderer is untrusted UI. It talks to a narrow preload bridge for Electron-only capabilities and to the localhost FastAPI service for app data.

The backend owns:
- SQLite persistence
- Ollama requests
- allowlisted automation
- Gmail integration boundary
- future voice and notification services

Security invariants:
1. No arbitrary shell execution.
2. No raw Electron IPC exposed to renderer.
3. Local API binds to loopback only.
4. External integrations are opt-in.
5. Secrets and tokens never belong in Git.
6. Model output is data, never executable code.

# Kitsune AI 🦊

A Windows 11 desktop AI companion starter built with Electron, React, TypeScript and FastAPI.

## Current implementation

- Electron desktop shell with context isolation and restricted IPC
- React dashboard with chat, status cards and privacy controls
- FastAPI backend bound to `127.0.0.1`
- Ollama adapter with graceful offline/error handling
- SQLite conversation persistence
- Explicitly allowlisted Windows application launching
- Volume control adapter placeholder (Windows implementation can be added)
- Gmail OAuth integration scaffold (read-only scope; requires Google Cloud setup)
- Notification center UI scaffold
- VRM/Three.js avatar integration placeholder
- Tests for memory and automation allowlist

This is a starter repository, not a claim that every optional integration is already configured. Gmail, local AI, voice and VRM require local setup and assets.

## Requirements

- Windows 11
- Node.js 20+
- Python 3.11+
- Git
- Optional: Ollama (https://ollama.com/download)

## Run in development

### 1. Backend

```powershell
cd backend
py -3.11 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload
```

### 2. Desktop app

Open a second PowerShell window:

```powershell
cd desktop
npm install
npm run dev
```

The Electron app expects the backend at `http://127.0.0.1:8765`.

## Optional local AI

Install Ollama, then pull a model appropriate for your hardware. For example:

```powershell
ollama pull qwen2.5:3b
```

Set `OLLAMA_MODEL=qwen2.5:3b` in `backend/.env`. Model availability and performance depend on your hardware.

## Gmail setup

1. Create a project in Google Cloud Console.
2. Enable Gmail API.
3. Configure OAuth consent screen.
4. Create an OAuth Client ID for a Desktop app.
5. Download the client secret JSON.
6. Set `GOOGLE_CLIENT_SECRET_FILE` in `backend/.env` to its path.
7. Start with read-only Gmail scope. Do not commit the secret or token files.

The Gmail module intentionally fails closed if credentials are missing. Never paste your Gmail password into this app.

## Security notes

- Electron Node integration is disabled.
- Context isolation and sandboxing are enabled.
- Backend binds only to localhost.
- PC automation uses a fixed allowlist; no arbitrary shell execution.
- Sending emails, deleting files and arbitrary terminal commands are not implemented.
- Keep `.env`, OAuth secrets and tokens out of Git.
- Review every permission before enabling additional automation.

## Project layout

```text
kitsune-ai/
  desktop/       Electron + React app
  backend/       FastAPI, SQLite, AI and automation
  assets/        Optional avatar assets
  docs/          Architecture notes
```

## GitHub

Create an empty GitHub repository named `kitsune-ai`, then from this folder:

```powershell
git init
git add .
git commit -m "Initial Kitsune AI desktop companion"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/kitsune-ai.git
git push -u origin main
```

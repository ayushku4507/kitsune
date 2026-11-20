from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .db import init_db, add_message, get_messages, add_memory, get_memories
from .ai import chat
from .automation import open_approved_app

app = FastAPI(title="Kitsune AI Local API", version="0.1.0")

# Restrict to local desktop development origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.on_event("startup")
def startup():
    init_db()

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)

class MemoryRequest(BaseModel):
    content: str = Field(min_length=1, max_length=1000)

class OpenAppRequest(BaseModel):
    app: str = Field(min_length=1, max_length=40)

@app.get("/health")
def health():
    return {"ok": True, "service": "kitsune-backend"}

@app.get("/history")
def history():
    return {"messages": get_messages()}

@app.post("/chat")
async def chat_endpoint(body: ChatRequest):
    add_message("user", body.message)
    history_items = get_messages()
    answer = await chat(body.message, history_items[:-1])
    add_message("assistant", answer)
    return {"reply": answer}

@app.get("/memories")
def memories():
    return {"memories": get_memories()}

@app.post("/memories")
def save_memory(body: MemoryRequest):
    memory_id = add_memory(body.content)
    return {"id": memory_id, "content": body.content}

@app.post("/automation/open-app")
def open_app(body: OpenAppRequest):
    try:
        return open_approved_app(body.app)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except OSError as exc:
        raise HTTPException(status_code=500, detail="Could not launch the approved application.") from exc

import httpx
from .config import settings

SYSTEM_PROMPT = (
    "You are Kitsune, a friendly, helpful desktop AI companion. "
    "Speak naturally in the user's language, including Hindi and Hinglish. "
    "Never claim an action happened unless a tool result confirms it. "
    "Never ask for passwords or secrets. Do not generate shell commands for execution."
)

async def chat(message: str, history: list[dict]):
    url = settings.ollama_base_url.rstrip("/") + "/api/chat"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in history[-12:]:
        if item["role"] in ("user", "assistant"):
            messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": message})
    payload = {"model": settings.ollama_model, "messages": messages, "stream": False}
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "I couldn't generate a response.")
    except httpx.HTTPError:
        return (
            "Mera local AI engine abhi available nahi hai. Ollama start karo, "
            "model pull karo, phir dobara try karo. Text dashboard abhi bhi available hai."
        )

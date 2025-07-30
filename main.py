from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

# Set this in your Railway environment variables to point to your bot's /link endpoint
BOT_RECEIVE_URL = os.getenv("BOT_RECEIVE_URL")  # e.g., https://omnibot.up.railway.app/link

class CharacterInfo(BaseModel):
    name: str
    realm: str
    class_: str  # Avoid using 'class' directly, since it's a Python keyword

class LinkPayload(BaseModel):
    discord_id: int
    characters: list[CharacterInfo]

@app.post("/onboard")
async def onboard(payload: LinkPayload):
    # Forward payload to the bot's /link endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(BOT_RECEIVE_URL, json=payload.dict())
            return {
                "status": "forwarded to bot",
                "bot_response_code": response.status_code,
                "bot_response_text": response.text
            }
    except Exception as e:
        return {"status": "failed", "error": str(e)}

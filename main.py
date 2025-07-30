from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os
import json

app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # Set this in Railway

class CharacterPayload(BaseModel):
    discord_id: int
    character_name: str
    character_realm: str
    character_class: str

@app.post("/onboard")
async def onboard_character(payload: CharacterPayload):
    # Format the embed or message for Discord
    embed = {
        "title": "🔗 Battle.net Account Linked",
        "description": (
            f"**Character:** {payload.character_name}-{payload.character_realm}\n"
            f"**Class:** {payload.character_class}"
        ),
        "color": 0x3498db
    }

    message = {
        "content": f"<@{payload.discord_id}> your character was successfully linked!",
        "embeds": [embed]
    }

    # Send to Discord via webhook
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json=message)

    return {"status": "success"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "linked_users.json"

class CharacterInfo(BaseModel):
    name: str
    realm: str
    class_: str

class LinkPayload(BaseModel):
    discord_id: int
    characters: list[CharacterInfo]

@app.post("/onboard")
async def onboard(payload: LinkPayload):
    data = payload.dict()

    # Load existing data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_links = json.load(f)
    else:
        all_links = {}

    # Save new data
    all_links[str(data["discord_id"])] = data["characters"]

    with open(DATA_FILE, "w") as f:
        json.dump(all_links, f, indent=2)

    return {"status": "saved"}

@app.get("/linked/{discord_id}")
async def get_linked_characters(discord_id: int):
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="No data found.")

    with open(DATA_FILE, "r") as f:
        all_links = json.load(f)

    characters = all_links.get(str(discord_id))
    if characters is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return {"characters": characters}

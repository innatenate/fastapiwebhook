from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    discord_id = payload.get("discord_id")
    character_data = payload.get("character_data")

    # Here you would store the character info for this discord user
    print(f"Linked {discord_id} with character: {character_data}")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

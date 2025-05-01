from fastapi import FastAPI

app = FastAPI(title="Play Cursor API")

@app.get("/")
async def root():
    return {"message": "Welcome to Play Cursor fastAPI with Docker-Compose"}
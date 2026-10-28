from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import insights, notes
from app.db.init_db import init_db

app = FastAPI(title="Lume", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router)
app.include_router(insights.router)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}

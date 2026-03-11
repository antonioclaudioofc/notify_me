from fastapi import FastAPI

from app.routes.antonio_claudio_dev import router as portfolio_router
from app.routes.arena_manager import router as arena_manager_router

app = FastAPI(title="Notify Me")

app.include_router(portfolio_router)
app.include_router(arena_manager_router)


@app.get("/")
def health_check():
    return {"status": "running"}

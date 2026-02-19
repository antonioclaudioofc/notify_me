from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.antonio_claudio_dev.router import router as antonio_claudio_dev_router
from app.modules.arena_manager.router import router as arena_manager_router

app = FastAPI(
    title="Notify Me API",
    description="API para receber mensagens de contato e enviar notificações por email."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to the Notify Me API"}


app.include_router(antonio_claudio_dev_router)
app.include_router(arena_manager_router)

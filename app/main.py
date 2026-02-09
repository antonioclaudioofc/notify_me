from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.contact.router import router as contact_router

app = FastAPI(title="Notify Me API", description="API para receber mensagens de contato e enviar notificações por email.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact_router)
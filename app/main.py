from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.contact.router import router as contact_router
from app.modules.email.router import router as email_router

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


app.include_router(contact_router)
app.include_router(email_router)
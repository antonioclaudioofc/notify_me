from fastapi import APIRouter, HTTPException

from app.modules.contact.service import ContactService
from app.schemas.contact import RequestContact


router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/", summary="Enviar mensagem de contato")
async def contact(contact: RequestContact):
    try:
        await ContactService.send_message(contact)
        return {"success": True}
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao enviar mensagem. Tente novamente mais tarde.")
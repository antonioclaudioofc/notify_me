from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.modules.contact.service import ContactService
from app.schemas.contact import RequestContact

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("/", summary="Enviar mensagem de contato")
def contact(background_tasks: BackgroundTasks, contact: RequestContact):
    try:
        background_tasks.add_task(ContactService.send_message, contact)
        return {"success": True}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar mensagem. Tente novamente mais tarde."
        )

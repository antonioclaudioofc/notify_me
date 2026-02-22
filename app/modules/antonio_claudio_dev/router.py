from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from app.modules.antonio_claudio_dev.service import AntonioClaudioDevService

from app.schemas.contact import RequestContact

router = APIRouter(
    prefix="/notifications/antonio-claudio-dev/contact",
    tags=["Antonio Claudio Dev"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def contact(
    background_tasks: BackgroundTasks,
    contact: RequestContact
):
    try:
        background_tasks.add_task(
            AntonioClaudioDevService.send_message,
            contact
        )
        return {
            "message": "Mensagem recebida. Entrarei em contato em breve!"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar mensagem. Tente novamente mais tarde."
        )

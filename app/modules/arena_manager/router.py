from fastapi import APIRouter, HTTPException, BackgroundTasks, status

from app.modules.arena_manager.service import ArenaManagerService
from app.schemas.email_verification import RequestEmailVerification


router = APIRouter(
    prefix="/notifications/arena-manager/verification",
    tags=["Arena Manager"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def email(
    background_tasks: BackgroundTasks,
    user: RequestEmailVerification
):
    try:
        background_tasks.add_task(
            ArenaManagerService.send_verification_email(user)
        )
        return {
            "message": "Email de verificação enviado. Verifique sua caixa de entrada!"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar email. Tente novamente mais tarde."
        )

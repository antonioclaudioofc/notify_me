from fastapi import APIRouter, HTTPException, BackgroundTasks, status

from app.modules.arena_manager.service import ArenaManagerService
from app.schemas.arena import Arena
from app.schemas.court import Court
from app.schemas.email_verification import RequestEmailVerification
from app.schemas.user import User


router = APIRouter(
    prefix="/notifications/arena-manager",
    tags=["Arena Manager"]
)


@router.post("/verification", status_code=status.HTTP_201_CREATED)
def email(
    background_tasks: BackgroundTasks,
    user: RequestEmailVerification
):
    try:
        background_tasks.add_task(
            ArenaManagerService.send_verification_email,
            user
        )
        return {
            "message": "Email de verificação enviado. Verifique sua caixa de entrada!"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar email. Tente novamente mais tarde."
        )


@router.post("/owner-promotion", status_code=status.HTTP_201_CREATED)
def owner_promotion(
    background_tasks: BackgroundTasks,
    user: User,
    arena: Arena
):
    try:
        background_tasks.add_task(
            ArenaManagerService.send_arena_owner_promotion_email,
            user,
            arena
        )
        return {
            "message": "Email de promoção de dono da arena enviado com sucesso!"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar email de promoção. Tente novamente mais tarde."
        )


@router.post("/new-court", status_code=status.HTTP_201_CREATED)
def new_court(
    background_tasks: BackgroundTasks,
    user: User,
    arena: Arena,
    court: Court
):
    try:
        background_tasks.add_task(
            ArenaManagerService.send_new_court_email,
            user,
            arena,
            court
        )
        return {
            "message": "Email de nova quadra enviado com sucesso!"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar email de nova quadra. Tente novamente mais tarde."
        )

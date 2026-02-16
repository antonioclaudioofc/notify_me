from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.modules.email.service import EmailService
from app.schemas.email_verification import RequestEmailVerification


router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/", summary="Enviar email personalizado")
def email(background_tasks: BackgroundTasks, email: RequestEmailVerification):
    try:
        background_tasks.add_task(EmailService.send_verification_email, email)
        return {"success": True}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar email. Tente novamente mais tarde."
        )

from app.services.mailer import send_mail, MailBody
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/mail", 
    tags=['mail']
)

# special Ones
@router.post("/send-email")
async def Mail(req: MailBody):
    data = req.model_dump()
    send_mail(data)
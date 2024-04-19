from services.mailer import send_mail
from services.config import MailBody
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
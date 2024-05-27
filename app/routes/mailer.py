from services.mailer import send_mail
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
router = APIRouter(
    prefix="/mail", 
    tags=['mail']
)
class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str

# special Ones
@router.post("/send-email")
async def Mail(req: MailBody):
    data = req.model_dump()
    send_mail(data)
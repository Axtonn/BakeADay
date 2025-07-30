from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from app.utils.email import send_contact_email

router = APIRouter()

class ContactRequest(BaseModel):
    email: EmailStr
    message: str

@router.post("/")
async def contact(request: Request, data: ContactRequest):
    try:
        await send_contact_email(data.email, data.message)
        return JSONResponse(content={"ok": True}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"ok": False, "error": str(e)}, status_code=500)

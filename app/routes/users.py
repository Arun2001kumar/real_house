from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import user as crud_user
from app.schemas.user import UserCreate
from app.models.user import User
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse("user/register.html", {"request": request})

@router.post("/register")
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_in = UserCreate(username=username, email=email, password=password)
    crud_user.create_user(db, user_in)
    return RedirectResponse("/login", status_code=303)

@router.get("/users/{username}")
def user_profile(username: str, request: Request, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username(db, username)
    if not user:
        return RedirectResponse("/register")
    return templates.TemplateResponse("user/profile.html", {"request": request, "user": user})
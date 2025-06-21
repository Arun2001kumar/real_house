from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import user as crud_user
from app.core.security import verify_password, create_access_token
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("user/login.html", {"request": request})

@router.post("/login")
def login_user(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = crud_user.get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return RedirectResponse("/login", status_code=303)
    access_token = create_access_token({"sub": user.username})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return RedirectResponse("/", status_code=303)

@router.get("/logout")
def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return RedirectResponse("/", status_code=303)
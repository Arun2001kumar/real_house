from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from .routes import properties, users, auth
from .database import Base, engine
from .models import user, property

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(properties.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
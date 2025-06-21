from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import property as crud_property
from app.schemas.property import PropertyCreate
from app.models.property import Property
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/properties")
def list_properties(request: Request, db: Session = Depends(get_db)):
    properties = crud_property.get_properties(db)
    return templates.TemplateResponse("property/list.html", {"request": request, "properties": properties})

@router.get("/properties/{property_id}")
def property_detail(property_id: int, request: Request, db: Session = Depends(get_db)):
    property = crud_property.get_property(db, property_id)
    if not property:
        return RedirectResponse("/properties")
    return templates.TemplateResponse("property/detail.html", {"request": request, "property": property})

@router.post("/properties/create")
def create_property(
    title: str = Form(...),
    price: float = Form(...),
    bedrooms: int = Form(...),
    bathrooms: float = Form(...),
    sqft: int = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    zip_code: str = Form(...),
    description: str = Form(""),
    photo_url: str = Form(""),
    db: Session = Depends(get_db)
):
    property_in = PropertyCreate(
        title=title,
        price=price,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        sqft=sqft,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        description=description,
        photo_url=photo_url
    )
    crud_property.create_property(db, property_in)
    return RedirectResponse("/properties", status_code=303)
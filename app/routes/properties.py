from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import property as crud_property
from app.schemas.property import PropertyCreate
from app.models.property import Property
from fastapi.templating import Jinja2Templates
from typing import Optional

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
    stats = crud_property.get_property_stats(db)
    return templates.TemplateResponse("property/list.html", {
        "request": request,
        "properties": properties,
        "stats": stats
    })

@router.get("/search")
def search_properties(
    request: Request,
    q: Optional[str] = Query(None, description="Search query"),
    min_price: Optional[str] = Query(None, description="Minimum price"),
    max_price: Optional[str] = Query(None, description="Maximum price"),
    bedrooms: Optional[str] = Query(None, description="Minimum bedrooms"),
    bathrooms: Optional[str] = Query(None, description="Minimum bathrooms"),
    min_sqft: Optional[str] = Query(None, description="Minimum square feet"),
    max_sqft: Optional[str] = Query(None, description="Maximum square feet"),
    city: Optional[str] = Query(None, description="City"),
    state: Optional[str] = Query(None, description="State"),
    zip_code: Optional[str] = Query(None, description="ZIP code"),
    sort_by: Optional[str] = Query("price_asc", description="Sort by"),
    db: Session = Depends(get_db)
):
    # Convert string parameters to appropriate types, handling empty strings
    def safe_float(value):
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def safe_int(value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    # Convert parameters
    min_price_val = safe_float(min_price)
    max_price_val = safe_float(max_price)
    bedrooms_val = safe_int(bedrooms)
    bathrooms_val = safe_float(bathrooms)
    min_sqft_val = safe_int(min_sqft)
    max_sqft_val = safe_int(max_sqft)

    properties = crud_property.search_properties(
        db=db,
        query=q,
        min_price=min_price_val,
        max_price=max_price_val,
        bedrooms=bedrooms_val,
        bathrooms=bathrooms_val,
        min_sqft=min_sqft_val,
        max_sqft=max_sqft_val,
        city=city,
        state=state,
        zip_code=zip_code,
        sort_by=sort_by
    )
    stats = crud_property.get_property_stats(db)

    # Prepare search parameters for template
    search_params = {
        'q': q or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
        'bedrooms': bedrooms or '',
        'bathrooms': bathrooms or '',
        'min_sqft': min_sqft or '',
        'max_sqft': max_sqft or '',
        'city': city or '',
        'state': state or '',
        'zip_code': zip_code or '',
        'sort_by': sort_by or 'price_asc'
    }

    return templates.TemplateResponse("property/search.html", {
        "request": request,
        "properties": properties,
        "stats": stats,
        "search_params": search_params,
        "results_count": len(properties)
    })

@router.get("/api/search")
def api_search_properties(
    q: Optional[str] = Query(None),
    min_price: Optional[str] = Query(None),
    max_price: Optional[str] = Query(None),
    bedrooms: Optional[str] = Query(None),
    bathrooms: Optional[str] = Query(None),
    min_sqft: Optional[str] = Query(None),
    max_sqft: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    zip_code: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("price_asc"),
    db: Session = Depends(get_db)
):
    """API endpoint for AJAX search requests"""
    # Convert string parameters to appropriate types, handling empty strings
    def safe_float(value):
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def safe_int(value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    # Convert parameters
    min_price_val = safe_float(min_price)
    max_price_val = safe_float(max_price)
    bedrooms_val = safe_int(bedrooms)
    bathrooms_val = safe_float(bathrooms)
    min_sqft_val = safe_int(min_sqft)
    max_sqft_val = safe_int(max_sqft)

    properties = crud_property.search_properties(
        db=db,
        query=q,
        min_price=min_price_val,
        max_price=max_price_val,
        bedrooms=bedrooms_val,
        bathrooms=bathrooms_val,
        min_sqft=min_sqft_val,
        max_sqft=max_sqft_val,
        city=city,
        state=state,
        zip_code=zip_code,
        sort_by=sort_by
    )

    # Convert to JSON-serializable format
    results = []
    for prop in properties:
        results.append({
            "id": prop.id,
            "title": prop.title,
            "price": prop.price,
            "bedrooms": prop.bedrooms,
            "bathrooms": prop.bathrooms,
            "sqft": prop.sqft,
            "address": prop.address,
            "city": prop.city,
            "state": prop.state,
            "zip_code": prop.zip_code,
            "description": prop.description,
            "photo_url": prop.photo_url
        })

    return JSONResponse({
        "properties": results,
        "count": len(results)
    })

@router.get("/map-search")
def map_search_page(
    request: Request,
    q: Optional[str] = Query(None),
    min_price: Optional[str] = Query(None),
    max_price: Optional[str] = Query(None),
    bedrooms: Optional[str] = Query(None),
    bathrooms: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    listing_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Map-based search page"""
    # Convert string parameters to appropriate types
    def safe_float(value):
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def safe_int(value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    # Convert parameters
    min_price_val = safe_float(min_price)
    max_price_val = safe_float(max_price)
    bedrooms_val = safe_int(bedrooms)
    bathrooms_val = safe_float(bathrooms)

    properties = crud_property.search_properties(
        db=db,
        query=q,
        min_price=min_price_val,
        max_price=max_price_val,
        bedrooms=bedrooms_val,
        bathrooms=bathrooms_val,
        property_type=property_type,
        listing_type=listing_type,
        limit=50  # Limit for initial map load
    )

    stats = crud_property.get_property_stats(db)

    # Prepare search parameters for template
    search_params = {
        'q': q or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
        'bedrooms': bedrooms or '',
        'bathrooms': bathrooms or '',
        'property_type': property_type or '',
        'listing_type': listing_type or ''
    }

    return templates.TemplateResponse("property/map_search.html", {
        "request": request,
        "properties": properties,
        "stats": stats,
        "search_params": search_params,
        "results_count": len(properties)
    })

@router.get("/api/map-search")
def api_map_search(
    q: Optional[str] = Query(None),
    min_price: Optional[str] = Query(None),
    max_price: Optional[str] = Query(None),
    bedrooms: Optional[str] = Query(None),
    bathrooms: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    listing_type: Optional[str] = Query(None),
    bounds: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """API endpoint for map-based AJAX search requests"""
    # Convert string parameters to appropriate types
    def safe_float(value):
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def safe_int(value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    # Convert parameters
    min_price_val = safe_float(min_price)
    max_price_val = safe_float(max_price)
    bedrooms_val = safe_int(bedrooms)
    bathrooms_val = safe_float(bathrooms)

    # Parse bounds if provided
    bounds_dict = None
    if bounds:
        try:
            import json
            bounds_dict = json.loads(bounds)
        except:
            bounds_dict = None

    properties = crud_property.search_properties(
        db=db,
        query=q,
        min_price=min_price_val,
        max_price=max_price_val,
        bedrooms=bedrooms_val,
        bathrooms=bathrooms_val,
        property_type=property_type,
        listing_type=listing_type,
        bounds=bounds_dict,
        limit=100
    )

    stats = crud_property.get_property_stats(db)

    # Generate HTML for property list
    property_html = ""
    for property in properties:
        property_html += f'''
        <div class="property-item" data-id="{property.id}"
             data-lat="{property.latitude}" data-lng="{property.longitude}">
            <img src="{property.photo_url or '/static/images/placeholder-home.svg'}"
                 alt="Property image" class="property-image">
            <div class="property-price">${property.price:,.0f}</div>
            <div class="property-details">
                {property.bedrooms} beds | {property.bathrooms} baths | {property.sqft:,} sqft
            </div>
            <div class="property-address">{property.address}, {property.city}, {property.state}</div>
        </div>
        '''

    return JSONResponse({
        "html": property_html,
        "results_count": len(properties),
        "total_count": stats['total_count']
    })

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
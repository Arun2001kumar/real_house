from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.models.property import Property
from app.schemas.property import PropertyCreate
from typing import Optional


def get_properties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Property).offset(skip).limit(limit).all()


def get_property(db: Session, property_id: int):
    return db.query(Property).filter(Property.id == property_id).first()


def search_properties(
    db: Session,
    query: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[float] = None,
    min_sqft: Optional[int] = None,
    max_sqft: Optional[int] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    property_type: Optional[str] = None,
    listing_type: Optional[str] = None,
    bounds: Optional[dict] = None,
    sort_by: Optional[str] = "price_asc",
    skip: int = 0,
    limit: int = 100
):
    """
    Advanced search for properties with multiple filters and sorting options
    """
    db_query = db.query(Property)

    # Text search across multiple fields
    if query:
        search_filter = or_(
            Property.title.ilike(f"%{query}%"),
            Property.address.ilike(f"%{query}%"),
            Property.city.ilike(f"%{query}%"),
            Property.state.ilike(f"%{query}%"),
            Property.zip_code.ilike(f"%{query}%"),
            Property.description.ilike(f"%{query}%")
        )
        db_query = db_query.filter(search_filter)

    # Price range filter
    if min_price is not None:
        db_query = db_query.filter(Property.price >= min_price)
    if max_price is not None:
        db_query = db_query.filter(Property.price <= max_price)

    # Bedrooms filter
    if bedrooms is not None:
        db_query = db_query.filter(Property.bedrooms >= bedrooms)

    # Bathrooms filter
    if bathrooms is not None:
        db_query = db_query.filter(Property.bathrooms >= bathrooms)

    # Square footage filter
    if min_sqft is not None:
        db_query = db_query.filter(Property.sqft >= min_sqft)
    if max_sqft is not None:
        db_query = db_query.filter(Property.sqft <= max_sqft)

    # Location filters
    if city:
        db_query = db_query.filter(Property.city.ilike(f"%{city}%"))
    if state:
        db_query = db_query.filter(Property.state.ilike(f"%{state}%"))
    if zip_code:
        db_query = db_query.filter(Property.zip_code == zip_code)

    # Property type filter
    if property_type:
        db_query = db_query.filter(Property.property_type == property_type)

    # Listing type filter
    if listing_type:
        db_query = db_query.filter(Property.listing_type == listing_type)

    # Geographic bounds filter (for map search)
    if bounds and all(k in bounds for k in ['north', 'south', 'east', 'west']):
        db_query = db_query.filter(
            and_(
                Property.latitude >= bounds['south'],
                Property.latitude <= bounds['north'],
                Property.longitude >= bounds['west'],
                Property.longitude <= bounds['east']
            )
        )

    # Sorting
    if sort_by == "price_asc":
        db_query = db_query.order_by(Property.price.asc())
    elif sort_by == "price_desc":
        db_query = db_query.order_by(Property.price.desc())
    elif sort_by == "sqft_asc":
        db_query = db_query.order_by(Property.sqft.asc())
    elif sort_by == "sqft_desc":
        db_query = db_query.order_by(Property.sqft.desc())
    elif sort_by == "bedrooms_desc":
        db_query = db_query.order_by(Property.bedrooms.desc())
    else:  # default to newest first (by id)
        db_query = db_query.order_by(Property.id.desc())

    return db_query.offset(skip).limit(limit).all()


def get_property_stats(db: Session):
    """
    Get statistics for property filters (min/max prices, etc.)
    """
    stats = db.query(
        func.min(Property.price).label('min_price'),
        func.max(Property.price).label('max_price'),
        func.min(Property.sqft).label('min_sqft'),
        func.max(Property.sqft).label('max_sqft'),
        func.count(Property.id).label('total_count')
    ).first()

    if not stats:
        return {
            'min_price': 0,
            'max_price': 1000000,
            'min_sqft': 0,
            'max_sqft': 5000,
            'total_count': 0
        }

    return {
        'min_price': stats.min_price or 0,
        'max_price': stats.max_price or 1000000,
        'min_sqft': stats.min_sqft or 0,
        'max_sqft': stats.max_sqft or 5000,
        'total_count': stats.total_count or 0
    }


def create_property(db: Session, property: PropertyCreate):
    db_property = Property(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property
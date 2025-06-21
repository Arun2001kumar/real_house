from pydantic import BaseModel, ConfigDict
from typing import Optional

class PropertyBase(BaseModel):
    title: str
    price: float
    bedrooms: int
    bathrooms: float
    sqft: int
    address: str
    city: str
    state: str
    zip_code: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_type: Optional[str] = "house"
    listing_type: Optional[str] = "sale"

class PropertyCreate(PropertyBase):
    pass

class PropertyOut(PropertyBase):
    id: int

    class Config:
            model_config = ConfigDict(from_attributes=True)
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

class PropertyCreate(PropertyBase):
    pass

class PropertyOut(PropertyBase):
    id: int

    class Config:
            model_config = ConfigDict(from_attributes=True)
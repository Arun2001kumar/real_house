from sqlalchemy import Column, Integer, Float, String, Text
from app.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    sqft = Column(Integer)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    description = Column(Text)
    photo_url = Column(String)
    latitude = Column(Float, nullable=True)  # For map integration
    longitude = Column(Float, nullable=True)  # For map integration
    property_type = Column(String, default="house")  # house, condo, townhouse, etc.
    listing_type = Column(String, default="sale")  # sale, rent
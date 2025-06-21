#!/usr/bin/env python3
"""
Script to populate the database with sample property data
"""

from app.database import SessionLocal
from app.models.property import Property
from app.crud.property import create_property
from app.schemas.property import PropertyCreate

def populate_database():
    db = SessionLocal()
    
    # Sample property data
    sample_properties = [
        {
            "title": "Modern Family Home in Springfield",
            "price": 450000.0,
            "bedrooms": 4,
            "bathrooms": 2.5,
            "sqft": 2200,
            "address": "123 Oak Street",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "description": "Beautiful modern family home with updated kitchen, spacious living areas, and large backyard. Perfect for families looking for comfort and style.",
            "photo_url": "/static/images/property-1.svg"
        },
        {
            "title": "Cozy Starter Home in Riverside",
            "price": 285000.0,
            "bedrooms": 2,
            "bathrooms": 1.5,
            "sqft": 1200,
            "address": "456 Maple Avenue",
            "city": "Riverside",
            "state": "CA",
            "zip_code": "92501",
            "description": "Perfect starter home with charming details, updated appliances, and a lovely garden. Great for first-time buyers.",
            "photo_url": "/static/images/property-2.svg"
        },
        {
            "title": "Victorian Style House in Hillcrest",
            "price": 675000.0,
            "bedrooms": 5,
            "bathrooms": 3.0,
            "sqft": 3200,
            "address": "789 Victorian Lane",
            "city": "Hillcrest",
            "state": "NY",
            "zip_code": "10001",
            "description": "Stunning Victorian home with original hardwood floors, ornate details, and modern amenities. A true architectural gem.",
            "photo_url": "/static/images/property-3.svg"
        },
        {
            "title": "Downtown Condo with City Views",
            "price": 520000.0,
            "bedrooms": 2,
            "bathrooms": 2.0,
            "sqft": 1100,
            "address": "321 Downtown Plaza",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62702",
            "description": "Luxury downtown condo with panoramic city views, modern finishes, and building amenities including gym and rooftop deck.",
            "photo_url": "/static/images/property-1.svg"
        },
        {
            "title": "Suburban Ranch in Oakwood",
            "price": 380000.0,
            "bedrooms": 3,
            "bathrooms": 2.0,
            "sqft": 1800,
            "address": "654 Ranch Road",
            "city": "Oakwood",
            "state": "TX",
            "zip_code": "75001",
            "description": "Single-story ranch home with open floor plan, large master suite, and beautiful landscaped yard. Move-in ready!",
            "photo_url": "/static/images/property-2.svg"
        },
        {
            "title": "Luxury Estate in Beverly Hills",
            "price": 2500000.0,
            "bedrooms": 6,
            "bathrooms": 5.5,
            "sqft": 5500,
            "address": "999 Beverly Drive",
            "city": "Beverly Hills",
            "state": "CA",
            "zip_code": "90210",
            "description": "Magnificent luxury estate with pool, spa, wine cellar, and stunning mountain views. The epitome of California living.",
            "photo_url": "/static/images/property-3.svg"
        },
        {
            "title": "Charming Cottage in Portland",
            "price": 425000.0,
            "bedrooms": 2,
            "bathrooms": 1.0,
            "sqft": 950,
            "address": "147 Cottage Lane",
            "city": "Portland",
            "state": "OR",
            "zip_code": "97201",
            "description": "Adorable cottage with original character, updated kitchen, and private garden. Perfect for those seeking charm and character.",
            "photo_url": "/static/images/property-1.svg"
        },
        {
            "title": "Contemporary Townhouse in Austin",
            "price": 495000.0,
            "bedrooms": 3,
            "bathrooms": 2.5,
            "sqft": 1650,
            "address": "852 Modern Way",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701",
            "description": "Sleek contemporary townhouse with high ceilings, modern finishes, and rooftop terrace. Located in trendy downtown area.",
            "photo_url": "/static/images/property-2.svg"
        },
        {
            "title": "Waterfront Property in Miami",
            "price": 1200000.0,
            "bedrooms": 4,
            "bathrooms": 3.5,
            "sqft": 2800,
            "address": "555 Ocean Drive",
            "city": "Miami",
            "state": "FL",
            "zip_code": "33139",
            "description": "Stunning waterfront home with private dock, infinity pool, and breathtaking ocean views. Paradise found!",
            "photo_url": "/static/images/property-3.svg"
        },
        {
            "title": "Mountain Cabin in Aspen",
            "price": 850000.0,
            "bedrooms": 3,
            "bathrooms": 2.0,
            "sqft": 1400,
            "address": "777 Mountain View",
            "city": "Aspen",
            "state": "CO",
            "zip_code": "81611",
            "description": "Cozy mountain cabin with stone fireplace, vaulted ceilings, and spectacular mountain views. Perfect ski retreat.",
            "photo_url": "/static/images/property-1.svg"
        },
        {
            "title": "Historic Brownstone in Boston",
            "price": 750000.0,
            "bedrooms": 4,
            "bathrooms": 2.5,
            "sqft": 2100,
            "address": "333 Beacon Street",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02116",
            "description": "Beautiful historic brownstone with original details, modern updates, and prime Back Bay location. Rich in history and charm.",
            "photo_url": "/static/images/property-2.svg"
        },
        {
            "title": "Modern Loft in Seattle",
            "price": 625000.0,
            "bedrooms": 1,
            "bathrooms": 1.0,
            "sqft": 800,
            "address": "888 Loft Street",
            "city": "Seattle",
            "state": "WA",
            "zip_code": "98101",
            "description": "Industrial-chic loft with exposed brick, high ceilings, and city views. Perfect for urban professionals.",
            "photo_url": "/static/images/property-3.svg"
        }
    ]
    
    try:
        # Clear existing properties (optional)
        print("Clearing existing properties...")
        db.query(Property).delete()
        db.commit()
        
        # Add new properties
        print("Adding sample properties...")
        for prop_data in sample_properties:
            property_create = PropertyCreate(**prop_data)
            create_property(db, property_create)
            print(f"Added: {prop_data['title']}")
        
        print(f"\nSuccessfully added {len(sample_properties)} properties to the database!")
        
    except Exception as e:
        print(f"Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()

#!/usr/bin/env python3
"""
Script to populate latitude and longitude for existing properties
Uses a simple geocoding approach with predefined coordinates for demo purposes
"""

import sqlite3
import random
from app.database import SQLALCHEMY_DATABASE_URL

# Sample coordinates for different cities (for demo purposes)
CITY_COORDINATES = {
    "Springfield": {"lat": 39.7817, "lng": -89.6501},
    "Riverside": {"lat": 33.9806, "lng": -117.3755},
    "Beverly Hills": {"lat": 34.0736, "lng": -118.4004},
    "Austin": {"lat": 30.2672, "lng": -97.7431},
    "Miami": {"lat": 25.7617, "lng": -80.1918},
    "Los Angeles": {"lat": 34.0522, "lng": -118.2437},
    "New York": {"lat": 40.7128, "lng": -74.0060},
    "Chicago": {"lat": 41.8781, "lng": -87.6298},
    "Houston": {"lat": 29.7604, "lng": -95.3698},
    "Phoenix": {"lat": 33.4484, "lng": -112.0740},
    "Philadelphia": {"lat": 39.9526, "lng": -75.1652},
    "San Antonio": {"lat": 29.4241, "lng": -98.4936},
    "San Diego": {"lat": 32.7157, "lng": -117.1611},
    "Dallas": {"lat": 32.7767, "lng": -96.7970},
    "San Jose": {"lat": 37.3382, "lng": -121.8863},
    "Jacksonville": {"lat": 30.3322, "lng": -81.6557},
    "Indianapolis": {"lat": 39.7684, "lng": -86.1581},
    "San Francisco": {"lat": 37.7749, "lng": -122.4194},
    "Columbus": {"lat": 39.9612, "lng": -82.9988},
    "Fort Worth": {"lat": 32.7555, "lng": -97.3308},
    "Charlotte": {"lat": 35.2271, "lng": -80.8431},
    "Detroit": {"lat": 42.3314, "lng": -83.0458},
    "El Paso": {"lat": 31.7619, "lng": -106.4850},
    "Memphis": {"lat": 35.1495, "lng": -90.0490},
    "Boston": {"lat": 42.3601, "lng": -71.0589},
    "Seattle": {"lat": 47.6062, "lng": -122.3321},
    "Denver": {"lat": 39.7392, "lng": -104.9903},
    "Washington": {"lat": 38.9072, "lng": -77.0369},
    "Nashville": {"lat": 36.1627, "lng": -86.7816},
    "Baltimore": {"lat": 39.2904, "lng": -76.6122},
    "Oklahoma City": {"lat": 35.4676, "lng": -97.5164},
    "Louisville": {"lat": 38.2527, "lng": -85.7585},
    "Portland": {"lat": 45.5152, "lng": -122.6784},
    "Las Vegas": {"lat": 36.1699, "lng": -115.1398},
    "Milwaukee": {"lat": 43.0389, "lng": -87.9065},
    "Albuquerque": {"lat": 35.0844, "lng": -106.6504},
    "Tucson": {"lat": 32.2226, "lng": -110.9747},
    "Fresno": {"lat": 36.7378, "lng": -119.7871},
    "Sacramento": {"lat": 38.5816, "lng": -121.4944},
    "Mesa": {"lat": 33.4152, "lng": -111.8315},
    "Kansas City": {"lat": 39.0997, "lng": -94.5786},
    "Atlanta": {"lat": 33.7490, "lng": -84.3880},
    "Long Beach": {"lat": 33.7701, "lng": -118.1937},
    "Colorado Springs": {"lat": 38.8339, "lng": -104.8214},
    "Raleigh": {"lat": 35.7796, "lng": -78.6382},
    "Omaha": {"lat": 41.2565, "lng": -95.9345},
    "Virginia Beach": {"lat": 36.8529, "lng": -75.9780},
    "Oakland": {"lat": 37.8044, "lng": -122.2712},
    "Minneapolis": {"lat": 44.9778, "lng": -93.2650},
    "Tulsa": {"lat": 36.1540, "lng": -95.9928},
    "Arlington": {"lat": 32.7357, "lng": -97.1081},
    "Tampa": {"lat": 27.9506, "lng": -82.4572}
}

def get_coordinates_for_city(city_name):
    """Get coordinates for a city, with some random variation"""
    city_name = city_name.strip()
    
    # Try exact match first
    if city_name in CITY_COORDINATES:
        base_coords = CITY_COORDINATES[city_name]
    else:
        # Try partial match
        for city in CITY_COORDINATES:
            if city.lower() in city_name.lower() or city_name.lower() in city.lower():
                base_coords = CITY_COORDINATES[city]
                break
        else:
            # Default to a random US city if no match found
            base_coords = random.choice(list(CITY_COORDINATES.values()))
    
    # Add some random variation to simulate different addresses in the same city
    lat_variation = random.uniform(-0.05, 0.05)  # ~5km variation
    lng_variation = random.uniform(-0.05, 0.05)
    
    return {
        "lat": round(base_coords["lat"] + lat_variation, 6),
        "lng": round(base_coords["lng"] + lng_variation, 6)
    }

def populate_coordinates():
    """Populate coordinates for all properties that don't have them"""
    
    # Extract database path from URL
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
        db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
        if db_path.startswith("./"):
            db_path = db_path[2:]
    else:
        print("This script only supports SQLite databases")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all properties without coordinates
        cursor.execute("""
            SELECT id, city, state, address 
            FROM properties 
            WHERE latitude IS NULL OR longitude IS NULL
        """)
        
        properties = cursor.fetchall()
        print(f"Found {len(properties)} properties without coordinates")
        
        updated_count = 0
        for prop_id, city, state, address in properties:
            coords = get_coordinates_for_city(city)
            
            cursor.execute("""
                UPDATE properties 
                SET latitude = ?, longitude = ? 
                WHERE id = ?
            """, (coords["lat"], coords["lng"], prop_id))
            
            updated_count += 1
            if updated_count % 10 == 0:
                print(f"Updated {updated_count} properties...")
        
        conn.commit()
        print(f"Successfully updated coordinates for {updated_count} properties!")
        
    except Exception as e:
        print(f"Error updating coordinates: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate_coordinates()

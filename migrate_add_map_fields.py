#!/usr/bin/env python3
"""
Migration script to add map-related fields to the properties table
"""

import sqlite3
import os
from app.database import SQLALCHEMY_DATABASE_URL

def migrate_database():
    """Add latitude, longitude, property_type, and listing_type columns to properties table"""
    
    # Extract database path from URL
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
        db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
        if db_path.startswith("./"):
            db_path = db_path[2:]
    else:
        print("This migration script only supports SQLite databases")
        return
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(properties)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add latitude column if it doesn't exist
        if 'latitude' not in columns:
            cursor.execute("ALTER TABLE properties ADD COLUMN latitude REAL")
            print("Added latitude column")
        
        # Add longitude column if it doesn't exist
        if 'longitude' not in columns:
            cursor.execute("ALTER TABLE properties ADD COLUMN longitude REAL")
            print("Added longitude column")
        
        # Add property_type column if it doesn't exist
        if 'property_type' not in columns:
            cursor.execute("ALTER TABLE properties ADD COLUMN property_type TEXT DEFAULT 'house'")
            print("Added property_type column")
        
        # Add listing_type column if it doesn't exist
        if 'listing_type' not in columns:
            cursor.execute("ALTER TABLE properties ADD COLUMN listing_type TEXT DEFAULT 'sale'")
            print("Added listing_type column")
        
        conn.commit()
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()

#!/usr/bin/env python3
"""
Test script for the new map-based search functionality
"""

import requests
import json

def test_map_search_page():
    """Test the map search page loads correctly"""
    try:
        response = requests.get('http://127.0.0.1:8000/map-search')
        print(f"Map Search Page Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Map search page loads successfully!")
            
            # Check if the page contains expected elements
            content = response.text
            if 'leaflet' in content.lower():
                print("✅ Leaflet map library is included")
            if 'map-search-container' in content:
                print("✅ Map search container is present")
            if 'property-results' in content:
                print("✅ Property results section is present")
            
            return True
        else:
            print(f"❌ Error loading map search page: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception testing map search page: {e}")
        return False

def test_map_search_api():
    """Test the map search API endpoint"""
    try:
        # Test basic search
        response = requests.get('http://127.0.0.1:8000/api/map-search?q=Springfield')
        print(f"Map Search API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Map search API working! Found {data['results_count']} properties")
            
            # Check response structure
            if 'html' in data:
                print("✅ HTML content is included in response")
            if 'results_count' in data:
                print("✅ Results count is included")
            if 'total_count' in data:
                print("✅ Total count is included")
            
            return True
        else:
            print(f"❌ Error with map search API: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception testing map search API: {e}")
        return False

def test_map_search_with_filters():
    """Test map search with various filters"""
    try:
        # Test with property type filter
        params = {
            'property_type': 'house',
            'listing_type': 'sale',
            'min_price': '100000',
            'max_price': '500000',
            'bedrooms': '2'
        }
        
        response = requests.get('http://127.0.0.1:8000/api/map-search', params=params)
        print(f"Filtered Map Search Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtered search working! Found {data['results_count']} properties")
            return True
        else:
            print(f"❌ Error with filtered search: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception testing filtered search: {e}")
        return False

def test_boundary_search():
    """Test map search with geographic boundaries"""
    try:
        # Test with boundary coordinates (roughly around Springfield, IL area)
        bounds = {
            'north': 40.0,
            'south': 39.5,
            'east': -89.0,
            'west': -90.0
        }
        
        params = {
            'bounds': json.dumps(bounds)
        }
        
        response = requests.get('http://127.0.0.1:8000/api/map-search', params=params)
        print(f"Boundary Search Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Boundary search working! Found {data['results_count']} properties")
            return True
        else:
            print(f"❌ Error with boundary search: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception testing boundary search: {e}")
        return False

def main():
    """Run all map search tests"""
    print("🗺️  Testing Map-Based Search Engine")
    print("=" * 50)
    
    tests = [
        ("Map Search Page", test_map_search_page),
        ("Map Search API", test_map_search_api),
        ("Filtered Search", test_map_search_with_filters),
        ("Boundary Search", test_boundary_search)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All map search tests passed! The map-based search engine is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()

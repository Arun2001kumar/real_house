#!/usr/bin/env python3
"""
Test script to verify the search functionality is working correctly
"""

import requests
import json
from urllib.parse import urlencode

BASE_URL = "http://127.0.0.1:8000"

def test_search_endpoint():
    """Test the search API endpoint"""
    print("Testing Search API Endpoint")
    print("=" * 40)
    
    # Test cases
    test_cases = [
        {
            "name": "Search by city (Springfield)",
            "params": {"q": "Springfield"}
        },
        {
            "name": "Search by state (CA)",
            "params": {"q": "CA"}
        },
        {
            "name": "Search by price range ($400k-$600k)",
            "params": {"min_price": 400000, "max_price": 600000}
        },
        {
            "name": "Search by bedrooms (3+)",
            "params": {"bedrooms": 3}
        },
        {
            "name": "Search by bathrooms (2+)",
            "params": {"bathrooms": 2}
        },
        {
            "name": "Search by square footage (2000+ sqft)",
            "params": {"min_sqft": 2000}
        },
        {
            "name": "Search luxury properties",
            "params": {"q": "luxury"}
        },
        {
            "name": "Search condos",
            "params": {"q": "condo"}
        },
        {
            "name": "Complex search (Austin, 2+ beds, $400k-$600k)",
            "params": {"city": "Austin", "bedrooms": 2, "min_price": 400000, "max_price": 600000}
        },
        {
            "name": "Sort by price (high to low)",
            "params": {"sort_by": "price_desc"}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 {test_case['name']}")
        
        try:
            # Make API request
            url = f"{BASE_URL}/api/search"
            response = requests.get(url, params=test_case['params'])
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                properties = data.get('properties', [])
                
                print(f"   ✅ Found {count} properties")
                
                # Show first few results
                for i, prop in enumerate(properties[:3]):
                    price = f"${prop['price']:,.0f}" if prop['price'] else "N/A"
                    print(f"   {i+1}. {prop['title']} - {price} ({prop['city']}, {prop['state']})")
                
                if count > 3:
                    print(f"   ... and {count - 3} more")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def test_search_page():
    """Test the search page rendering"""
    print("\n\nTesting Search Page Rendering")
    print("=" * 40)
    
    test_urls = [
        "/search",
        "/search?q=Springfield",
        "/search?min_price=400000&max_price=600000",
        "/search?bedrooms=3&bathrooms=2",
        "/search?city=Austin&sort_by=price_desc"
    ]
    
    for url in test_urls:
        print(f"\n🌐 Testing: {url}")
        
        try:
            response = requests.get(f"{BASE_URL}{url}")
            
            if response.status_code == 200:
                content = response.text
                
                # Check for key elements
                checks = [
                    ("Search form", '<form class="search-form"' in content),
                    ("Property grid", 'class="property-grid"' in content),
                    ("Results header", 'class="results-header"' in content),
                    ("Search fields", 'name="q"' in content),
                    ("Sort options", 'name="sort_by"' in content)
                ]
                
                all_passed = True
                for check_name, passed in checks:
                    status = "✅" if passed else "❌"
                    print(f"   {status} {check_name}")
                    if not passed:
                        all_passed = False
                
                if all_passed:
                    print("   ✅ Page rendered successfully")
                else:
                    print("   ⚠️  Some elements missing")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def test_home_page_search():
    """Test the home page search functionality"""
    print("\n\nTesting Home Page Search")
    print("=" * 40)
    
    try:
        # Test home page loads
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for search form
            if 'action="/search"' in content and 'name="q"' in content:
                print("   ✅ Home page search form found")
                
                # Test search redirect
                search_response = requests.get(f"{BASE_URL}/search?q=test")
                if search_response.status_code == 200:
                    print("   ✅ Search redirect working")
                else:
                    print(f"   ❌ Search redirect failed: {search_response.status_code}")
            else:
                print("   ❌ Home page search form not found")
        else:
            print(f"   ❌ Home page error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

def test_property_stats():
    """Test property statistics"""
    print("\n\nTesting Property Statistics")
    print("=" * 40)
    
    try:
        # Get search page to check stats
        response = requests.get(f"{BASE_URL}/search")
        
        if response.status_code == 200:
            content = response.text
            
            # Look for stats in the content
            if "Found" in content and "properties" in content:
                print("   ✅ Property count displayed")
            else:
                print("   ❌ Property count not found")
                
            # Check for price placeholders
            if "$" in content:
                print("   ✅ Price information displayed")
            else:
                print("   ❌ Price information not found")
                
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

def main():
    """Run all tests"""
    print("🏠 Dream yours Real Estate Search Engine Test")
    print("=" * 50)
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server not responding. Please start the server first.")
            return
    except:
        print("❌ Cannot connect to server. Please start the server first.")
        print("Run: python -m uvicorn app.main:app --reload")
        return
    
    print("✅ Server is running")
    
    # Run tests
    test_search_endpoint()
    test_search_page()
    test_home_page_search()
    test_property_stats()
    
    print("\n\n🎉 Testing Complete!")
    print("\nTo manually test the search engine:")
    print("1. Visit http://127.0.0.1:8000")
    print("2. Use the search bar to search for properties")
    print("3. Visit http://127.0.0.1:8000/search for advanced search")
    print("4. Try different filters and sorting options")

if __name__ == "__main__":
    main()

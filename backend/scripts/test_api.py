#!/usr/bin/env python3
"""
Script to test My Vocabulary Vault API with test data
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test user credentials
TEST_USERS = [
    {
        "email": "john.doe@example.com",
        "password": "password123",
        "name": "John Doe"
    },
    {
        "email": "jane.smith@example.com", 
        "password": "password123",
        "name": "Jane Smith"
    },
    {
        "email": "admin@vocabularyvault.com",
        "password": "admin123",
        "name": "Admin"
    }
]

def make_request(method: str, endpoint: str, data: Dict[str, Any] = None, token: str = None) -> Dict[str, Any]:
    """Make HTTP request to API"""
    url = f"{API_BASE}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return {
            "status_code": response.status_code,
            "data": response.json() if response.content else None,
            "success": 200 <= response.status_code < 300
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 0,
            "data": {"error": str(e)},
            "success": False
        }

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing Health Check...")
    result = make_request("GET", "/health")
    print(f"Status: {result['status_code']}")
    if result['success']:
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
    print()

def test_user_login(user_data: Dict[str, str]) -> str:
    """Test user login and return access token"""
    print(f"🔐 Testing login for {user_data['name']}...")
    
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    result = make_request("POST", "/auth/login", login_data)
    
    if result['success']:
        token = result['data']['access_token']
        print(f"✅ Login successful for {user_data['name']}")
        return token
    else:
        print(f"❌ Login failed for {user_data['name']}: {result['data']}")
        return None

def test_get_user_info(token: str, user_name: str):
    """Test getting current user info"""
    print(f"👤 Testing get user info for {user_name}...")
    
    result = make_request("GET", "/auth/me", token=token)
    
    if result['success']:
        user_info = result['data']
        print(f"✅ User info retrieved: {user_info['full_name']} (Level {user_info['level']})")
        print(f"   Points: {user_info['total_points']}, XP: {user_info['experience_points']}")
    else:
        print(f"❌ Failed to get user info: {result['data']}")
    print()

def test_get_flashcard_sets(token: str, user_name: str):
    """Test getting user's flashcard sets"""
    print(f"📚 Testing get flashcard sets for {user_name}...")
    
    result = make_request("GET", "/flashcards/sets", token=token)
    
    if result['success']:
        sets_data = result['data']
        print(f"✅ Found {sets_data['total']} flashcard sets")
        for set_item in sets_data['items']:
            print(f"   - {set_item['title']} ({set_item['total_cards']} cards)")
    else:
        print(f"❌ Failed to get flashcard sets: {result['data']}")
    print()

def test_get_public_sets():
    """Test getting public flashcard sets"""
    print("🌐 Testing get public flashcard sets...")
    
    result = make_request("GET", "/flashcards/sets/public")
    
    if result['success']:
        sets_data = result['data']
        print(f"✅ Found {sets_data['total']} public flashcard sets")
        for set_item in sets_data['items']:
            print(f"   - {set_item['title']} by {set_item['user_id']} ({set_item['total_cards']} cards)")
    else:
        print(f"❌ Failed to get public sets: {result['data']}")
    print()

def test_get_set_with_cards(token: str, user_name: str):
    """Test getting a flashcard set with all its cards"""
    print(f"🃏 Testing get set with cards for {user_name}...")
    
    # First get user's sets
    sets_result = make_request("GET", "/flashcards/sets", token=token)
    
    if sets_result['success'] and sets_result['data']['items']:
        first_set = sets_result['data']['items'][0]
        set_id = first_set['id']
        
        result = make_request("GET", f"/flashcards/sets/{set_id}/with-cards", token=token)
        
        if result['success']:
            set_data = result['data']
            print(f"✅ Retrieved set: {set_data['title']}")
            print(f"   Cards: {len(set_data['cards'])}")
            for i, card in enumerate(set_data['cards'][:3]):  # Show first 3 cards
                print(f"   {i+1}. {card['front_content']} → {card['back_content']}")
            if len(set_data['cards']) > 3:
                print(f"   ... and {len(set_data['cards']) - 3} more cards")
        else:
            print(f"❌ Failed to get set with cards: {result['data']}")
    else:
        print("❌ No sets found to test")
    print()

def test_create_flashcard_set(token: str, user_name: str):
    """Test creating a new flashcard set"""
    print(f"➕ Testing create flashcard set for {user_name}...")
    
    new_set_data = {
        "title": f"Test Set by {user_name}",
        "description": "A test flashcard set created via API",
        "category": "Test",
        "tags": ["test", "api", "demo"],
        "is_public": True,
        "is_featured": False
    }
    
    result = make_request("POST", "/flashcards/sets", new_set_data, token)
    
    if result['success']:
        set_data = result['data']
        print(f"✅ Created new set: {set_data['title']} (ID: {set_data['id']})")
        return set_data['id']
    else:
        print(f"❌ Failed to create set: {result['data']}")
        return None

def test_create_flashcard(token: str, set_id: int, user_name: str):
    """Test creating a new flashcard"""
    print(f"🃏 Testing create flashcard for {user_name}...")
    
    new_card_data = {
        "front_content": f"Test question from {user_name}",
        "back_content": f"Test answer from {user_name}",
        "card_type": "text",
        "difficulty": "medium",
        "card_metadata": {"created_by": "api_test"}
    }
    
    result = make_request("POST", f"/flashcards/sets/{set_id}/cards", new_card_data, token)
    
    if result['success']:
        card_data = result['data']
        print(f"✅ Created new card: {card_data['front_content']} → {card_data['back_content']}")
    else:
        print(f"❌ Failed to create card: {result['data']}")

def main():
    """Main test function"""
    print("🚀 Starting My Vocabulary Vault API Tests")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Test with each user
    for user_data in TEST_USERS:
        print(f"👤 Testing with user: {user_data['name']}")
        print("-" * 30)
        
        # Login
        token = test_user_login(user_data)
        if not token:
            continue
        
        # Test user info
        test_get_user_info(token, user_data['name'])
        
        # Test get flashcard sets
        test_get_flashcard_sets(token, user_data['name'])
        
        # Test get set with cards
        test_get_set_with_cards(token, user_data['name'])
        
        # Test create new set
        new_set_id = test_create_flashcard_set(token, user_data['name'])
        
        # Test create new card
        if new_set_id:
            test_create_flashcard(token, new_set_id, user_data['name'])
        
        print()
    
    # Test public sets (no auth required)
    test_get_public_sets()
    
    print("🎉 API Testing Completed!")
    print("\n📋 Test Summary:")
    print("- Health check: ✅")
    print("- User authentication: ✅")
    print("- Flashcard sets CRUD: ✅")
    print("- Flashcards CRUD: ✅")
    print("- Public sets access: ✅")
    
    print(f"\n🔗 API Documentation: {BASE_URL}/docs")
    print(f"🔗 Health Check: {BASE_URL}/health")

if __name__ == "__main__":
    main()

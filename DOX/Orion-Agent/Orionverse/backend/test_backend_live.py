#!/usr/bin/env python3
"""
Test if Flask backend is responding correctly
"""
import requests
import json

API_BASE = "http://127.0.0.1:5001"

print("="*60)
print("TESTING BACKEND API")
print("="*60)

# Test 1: /api/search/all
print("\n1. Testing GET /api/search/all")
print("-"*60)
try:
    response = requests.get(f"{API_BASE}/api/search/all", timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"   SR data: {len(data.get('sr_data', []))} records")
        print(f"   Defect data: {len(data.get('defect_data', []))} records")
        print(f"   WA data: {len(data.get('wa_data', []))} records")
        print(f"   Total counts: {data.get('total_counts')}")
        if data.get('defect_data'):
            print(f"\n   Sample defect:")
            print(f"   ID: {data['defect_data'][0].get('ID')}")
            print(f"   Name: {data['defect_data'][0].get('Name')[:80]}")
    else:
        print(f"❌ Error: {response.text}")
except requests.exceptions.ConnectionError:
    print("❌ CONNECTION REFUSED - Backend is NOT running!")
    print("\nStart backend with:")
    print("   cd backend")
    print("   python app.py")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 2: /api/search/filter with search_anything
print("\n2. Testing POST /api/search/filter (search_anything='order')")
print("-"*60)
try:
    response = requests.post(
        f"{API_BASE}/api/search/filter",
        json={"search_anything": "order"},
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"   SR results: {len(data.get('sr_data', []))} records")
        print(f"   Defect results: {len(data.get('defect_data', []))} records")
        print(f"   WA results: {len(data.get('wa_data', []))} records")
        
        if len(data.get('defect_data', [])) == 0:
            print("\n❌ WARNING: No defects returned!")
            print("   But debug_search.py found 2542 defects")
            print("   Check backend filter logic!")
        else:
            print(f"\n   Sample defect result:")
            print(f"   ID: {data['defect_data'][0].get('ID')}")
            print(f"   Name: {data['defect_data'][0].get('Name')[:80]}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: /api/search/filter with defect ID
print("\n3. Testing POST /api/search/filter (id='2860119')")
print("-"*60)
try:
    response = requests.post(
        f"{API_BASE}/api/search/filter",
        json={"id": "2860119"},
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"   Defect results: {len(data.get('defect_data', []))} records")
        
        if len(data.get('defect_data', [])) > 0:
            print(f"\n   Found defect:")
            print(f"   ID: {data['defect_data'][0].get('ID')}")
            print(f"   Name: {data['defect_data'][0].get('Name')[:80]}")
        else:
            print("\n❌ No defects found!")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("If all tests passed, backend is working correctly.")
print("The problem is likely in the frontend.")
print("\nNext steps:")
print("1. Open browser console (F12)")
print("2. Check for JavaScript errors")
print("3. Look at Network tab to see API calls")


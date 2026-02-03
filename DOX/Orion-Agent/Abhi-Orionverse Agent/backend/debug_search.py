#!/usr/bin/env python3
"""
Debug script to test search functionality
"""
import json
import sys

print("="*60)
print("DEFECT DATA DEBUG")
print("="*60)

# Load defect data
with open('data/defect_data.json', 'r', encoding='utf-8') as f:
    defect_data = json.load(f)

print(f"\nTotal defects loaded: {len(defect_data)}")

# Show first defect structure
print("\n" + "="*60)
print("FIRST DEFECT STRUCTURE:")
print("="*60)
first = defect_data[0]
for key, value in first.items():
    if isinstance(value, str) and len(value) > 100:
        print(f"{key}: {value[:100]}...")
    else:
        print(f"{key}: {value}")

# Test search for "order"
print("\n" + "="*60)
print("TEST SEARCH: 'order' in Name or Description")
print("="*60)
search_term = "order"
found = []
for d in defect_data[:100]:  # Test first 100
    name = str(d.get('Name', '')).lower()
    desc = str(d.get('Description', '')).lower()
    if search_term in name or search_term in desc:
        found.append(d)

print(f"Found {len(found)} defects with '{search_term}' in first 100")
if found:
    print(f"\nSample found defect:")
    print(f"ID: {found[0].get('ID')}")
    print(f"Name: {found[0].get('Name')[:100]}")

# Test search for specific ID
print("\n" + "="*60)
print("TEST SEARCH: Defect ID = 2860119")
print("="*60)
specific_id = "2860119"
found_by_id = [d for d in defect_data if str(d.get('ID', '')) == specific_id]
print(f"Found {len(found_by_id)} defects with ID {specific_id}")
if found_by_id:
    print(f"Defect found: {found_by_id[0].get('Name')[:100]}")

# Test the actual filter logic from search.py
print("\n" + "="*60)
print("TEST ACTUAL FILTER LOGIC")
print("="*60)

# Simulate search_anything filter
filtered = defect_data
search_anything = "order"
if search_anything:
    filtered = [
        d for d in filtered 
        if search_anything in str(d.get('Name', '')).lower() 
        or search_anything in str(d.get('Description', '')).lower()
    ]
print(f"After 'search_anything=order' filter: {len(filtered)} defects")

# Simulate defect ID filter
filtered = defect_data
defect_id = "2860119"
if defect_id:
    filtered = [
        d for d in filtered 
        if str(d.get('ID', '')) == defect_id
    ]
print(f"After 'id=2860119' filter: {len(filtered)} defects")

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("If you see defects found above, the data is good.")
print("If backend still returns 0, check:")
print("1. Is Flask loading the same data file?")
print("2. Are filters being applied correctly?")
print("3. Check backend console output")


"""
Example: Using Cached Categories (No Token Cost!)
This example shows how to use category_utils.py to access category data
without consuming any API tokens.

Prerequisites:
1. Run fetch_all_categories.py first (one-time token cost)
2. This will create data/amazon_categories.json and .csv files
3. After that, use this script - NO TOKENS CONSUMED!
"""

import sys
import os

# Add parent directory to path to import category_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from category_utils import (
    get_category_by_id,
    search_categories,
    get_all_categories,
    get_categories_by_parent,
    get_root_categories,
    get_category_statistics,
    print_category_info
)

print("=" * 60)
print("Using Cached Categories - NO API TOKENS CONSUMED!")
print("=" * 60)

# Get statistics
print("\n1. Category Statistics:")
print("-" * 60)
stats = get_category_statistics()
print(f"   Total Categories: {stats['total_categories']:,}")
print(f"   Root Categories: {stats['root_categories']}")
print(f"   Max Depth: {stats['max_depth']}")
print(f"   Total Products: {stats['total_products']:,}")

# Search categories
print("\n2. Search Categories:")
print("-" * 60)
search_term = "Electronics"
results = search_categories(search_term)
print(f"   Searching for: '{search_term}'")
print(f"   Found {len(results)} categories:")
for cat in results[:5]:
    print(f"     [{cat.get('category_id')}] {cat.get('name')}")
if len(results) > 5:
    print(f"     ... and {len(results) - 5} more")

# Get category by ID
print("\n3. Get Category by ID:")
print("-" * 60)
category_id = 20  # Replace with any category ID from your cache
category = get_category_by_id(category_id)
if category:
    print(f"   Category ID {category_id}: {category.get('name')}")
    print(f"   Product Count: {category.get('product_count', 0):,}")
    print(f"   Children: {category.get('children_count', 0)}")
else:
    print(f"   Category ID {category_id} not found in cache")

# Get root categories
print("\n4. Root Categories:")
print("-" * 60)
root_cats = get_root_categories()
print(f"   Found {len(root_cats)} root categories:")
for cat in root_cats[:10]:
    print(f"     [{cat.get('category_id')}] {cat.get('name')}")
if len(root_cats) > 10:
    print(f"     ... and {len(root_cats) - 10} more")

# Detailed category info
print("\n5. Detailed Category Information:")
print("-" * 60)
if category:
    print_category_info(category_id)

print("\n" + "=" * 60)
print("✅ All operations completed WITHOUT consuming API tokens!")
print("=" * 60)


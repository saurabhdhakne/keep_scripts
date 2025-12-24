"""
Category Utilities - Read from Cached Category Data
This module provides functions to read category data from cached files
without consuming any API tokens.

Usage:
    from category_utils import get_category_by_id, search_categories, get_all_categories
    
    # Get category by ID
    category = get_category_by_id(20)
    
    # Search categories by name
    results = search_categories("Electronics")
    
    # Get all categories
    all_cats = get_all_categories()
"""

import json
import csv
import os
from typing import List, Dict, Optional

# Default file paths
JSON_FILE = "data/amazon_categories.json"
CSV_FILE = "data/amazon_categories.csv"

def load_categories_from_json(filename: str = JSON_FILE) -> List[Dict]:
    """Load categories from JSON file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Category file not found: {filename}\n"
            f"Please run fetch_all_categories.py first to create the cache."
        )
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('categories', [])

def load_categories_from_csv(filename: str = CSV_FILE) -> List[Dict]:
    """Load categories from CSV file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Category file not found: {filename}\n"
            f"Please run fetch_all_categories.py first to create the cache."
        )
    
    categories = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert children_ids string back to list
            children_ids_str = row.get('children_ids', '')
            row['children_ids'] = [int(x) for x in children_ids_str.split(',') if x] if children_ids_str else []
            
            # Convert numeric fields
            row['category_id'] = int(row['category_id'])
            if row.get('parent_id'):
                row['parent_id'] = int(row['parent_id'])
            row['product_count'] = int(row.get('product_count', 0))
            row['children_count'] = int(row.get('children_count', 0))
            row['depth'] = int(row.get('depth', 0))
            
            categories.append(row)
    
    return categories

def get_all_categories(use_csv: bool = False) -> List[Dict]:
    """
    Get all categories from cached file.
    
    Args:
        use_csv: If True, load from CSV instead of JSON
    
    Returns:
        List of category dictionaries
    """
    if use_csv:
        return load_categories_from_csv()
    return load_categories_from_json()

def get_category_by_id(category_id: int, use_csv: bool = False) -> Optional[Dict]:
    """
    Get category by ID from cached data.
    
    Args:
        category_id: Category ID to search for
        use_csv: If True, load from CSV instead of JSON
    
    Returns:
        Category dictionary or None if not found
    """
    categories = get_all_categories(use_csv)
    
    for cat in categories:
        if cat.get('category_id') == category_id:
            return cat
    
    return None

def search_categories(search_term: str, case_sensitive: bool = False, use_csv: bool = False) -> List[Dict]:
    """
    Search categories by name.
    
    Args:
        search_term: Search term to match against category names
        case_sensitive: If True, search is case-sensitive
        use_csv: If True, load from CSV instead of JSON
    
    Returns:
        List of matching category dictionaries
    """
    categories = get_all_categories(use_csv)
    results = []
    
    if not case_sensitive:
        search_term = search_term.lower()
    
    for cat in categories:
        name = cat.get('name', '')
        if not case_sensitive:
            name = name.lower()
        
        if search_term in name:
            results.append(cat)
    
    return results

def get_categories_by_parent(parent_id: int, use_csv: bool = False) -> List[Dict]:
    """
    Get all subcategories of a parent category.
    
    Args:
        parent_id: Parent category ID
        use_csv: If True, load from CSV instead of JSON
    
    Returns:
        List of subcategory dictionaries
    """
    categories = get_all_categories(use_csv)
    
    return [cat for cat in categories if cat.get('parent_id') == parent_id]

def get_root_categories(use_csv: bool = False) -> List[Dict]:
    """
    Get all root categories (categories with no parent).
    
    Args:
        use_csv: If True, load from CSV instead of JSON
    
    Returns:
        List of root category dictionaries
    """
    categories = get_all_categories(use_csv)
    
    return [cat for cat in categories if cat.get('parent_id') is None or cat.get('parent_id') == 0]

def get_category_statistics(use_csv: bool = False) -> Dict:
    """
    Get statistics about the cached category data.
    
    Args:
        use_csv: If True, load from CSV instead of JSON
    
    Returns:
        Dictionary with statistics
    """
    categories = get_all_categories(use_csv)
    
    if not categories:
        return {
            'total_categories': 0,
            'root_categories': 0,
            'max_depth': 0,
            'total_products': 0
        }
    
    root_cats = get_root_categories(use_csv)
    max_depth = max((cat.get('depth', 0) for cat in categories), default=0)
    total_products = sum((cat.get('product_count', 0) for cat in categories))
    
    return {
        'total_categories': len(categories),
        'root_categories': len(root_cats),
        'max_depth': max_depth,
        'total_products': total_products
    }

def print_category_info(category_id: int, use_csv: bool = False):
    """
    Print detailed information about a category.
    
    Args:
        category_id: Category ID to display
        use_csv: If True, load from CSV instead of JSON
    """
    cat = get_category_by_id(category_id, use_csv)
    
    if not cat:
        print(f"Category ID {category_id} not found in cache.")
        print("Run fetch_all_categories.py to update the cache.")
        return
    
    print(f"\n{'='*60}")
    print(f"Category Information")
    print(f"{'='*60}")
    print(f"ID: {cat.get('category_id')}")
    print(f"Name: {cat.get('name')}")
    print(f"Parent ID: {cat.get('parent_id', 'None (Root)')}")
    print(f"Domain: {cat.get('domain', 1)}")
    print(f"Product Count: {cat.get('product_count', 0):,}")
    print(f"Children Count: {cat.get('children_count', 0)}")
    print(f"Depth: {cat.get('depth', 0)}")
    
    children_ids = cat.get('children_ids', [])
    if children_ids:
        print(f"\nSubcategories ({len(children_ids)}):")
        for child_id in children_ids[:10]:  # Show first 10
            child = get_category_by_id(child_id, use_csv)
            if child:
                print(f"  - [{child_id}] {child.get('name')}")
        if len(children_ids) > 10:
            print(f"  ... and {len(children_ids) - 10} more")

if __name__ == "__main__":
    # Example usage
    print("Category Utilities - Example Usage\n")
    
    # Check if data exists
    if not os.path.exists(JSON_FILE) and not os.path.exists(CSV_FILE):
        print("⚠️  Category data not found!")
        print(f"Please run fetch_all_categories.py first to create the cache.")
        exit(1)
    
    # Get statistics
    stats = get_category_statistics()
    print(f"Category Statistics:")
    print(f"  Total Categories: {stats['total_categories']:,}")
    print(f"  Root Categories: {stats['root_categories']}")
    print(f"  Max Depth: {stats['max_depth']}")
    print(f"  Total Products: {stats['total_products']:,}")
    
    # Search example
    print(f"\n{'='*60}")
    print("Search Example: 'Electronics'")
    print(f"{'='*60}")
    results = search_categories("Electronics")
    print(f"Found {len(results)} categories matching 'Electronics':")
    for cat in results[:5]:
        print(f"  [{cat.get('category_id')}] {cat.get('name')}")
    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more")


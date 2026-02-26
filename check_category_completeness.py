"""
Check Category Fetch Completeness
Compares fetched category IDs with saved categories to identify missing data.
"""

import json
import os

PROGRESS_FILE = "data/fetch_progress.json"
CATEGORIES_FILE = "data/amazon_categories.json"

def load_progress():
    """Load fetch progress."""
    if not os.path.exists(PROGRESS_FILE):
        print(f"❌ Progress file not found: {PROGRESS_FILE}")
        return None
    
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_categories():
    """Load saved categories."""
    if not os.path.exists(CATEGORIES_FILE):
        print(f"❌ Categories file not found: {CATEGORIES_FILE}")
        return []
    
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('categories', [])

def analyze_completeness():
    """Analyze what's missing."""
    print("=" * 80)
    print("CATEGORY FETCH COMPLETENESS CHECK")
    print("=" * 80)
    
    # Load data
    progress = load_progress()
    if not progress:
        return
    
    categories = load_categories()
    
    # Get IDs
    fetched_ids = set(progress.get('fetched_category_ids', []))
    saved_ids = {cat['category_id'] for cat in categories}
    
    # Calculate missing
    missing_ids = fetched_ids - saved_ids
    
    # Statistics
    print(f"\n📊 Statistics:")
    print(f"   Fetched Category IDs: {len(fetched_ids)}")
    print(f"   Saved Categories: {len(saved_ids)}")
    print(f"   Missing Categories: {len(missing_ids)}")
    print(f"   Completion Rate: {len(saved_ids) / len(fetched_ids) * 100:.1f}%")
    
    print(f"\n📝 Search Terms Completed: {len(progress.get('search_terms_completed', []))}")
    print(f"   Terms: {', '.join(progress.get('search_terms_completed', [])[:10])}")
    if len(progress.get('search_terms_completed', [])) > 10:
        print(f"   ... and {len(progress.get('search_terms_completed', [])) - 10} more")
    
    if missing_ids:
        print(f"\n⚠️  MISSING CATEGORIES: {len(missing_ids)} categories were fetched but not saved!")
        print(f"\n   This likely means:")
        print(f"   1. The detail fetching phase stopped early (token limit, error, etc.)")
        print(f"   2. Only {len(saved_ids)} categories have full details")
        print(f"   3. {len(missing_ids)} categories only have basic info from search")
        
        # Show sample missing IDs
        print(f"\n   Sample Missing Category IDs (first 20):")
        for i, cat_id in enumerate(list(missing_ids)[:20], 1):
            print(f"      {i}. {cat_id}")
        if len(missing_ids) > 20:
            print(f"      ... and {len(missing_ids) - 20} more")
        
        print(f"\n💡 Recommendation:")
        print(f"   Run fetch_all_categories.py again to fetch details for missing categories.")
        print(f"   It will automatically resume from where it left off.")
    else:
        print(f"\n✅ All fetched categories have been saved!")
    
    # Check saved categories structure
    print(f"\n📋 Saved Categories Analysis:")
    categories_with_details = 0
    categories_without_details = 0
    
    for cat in categories:
        # Check if category has full details (not just basic info)
        name = cat.get('name')
        if isinstance(name, dict):
            # Has full details
            categories_with_details += 1
        else:
            categories_without_details += 1
    
    print(f"   Categories with full details: {categories_with_details}")
    print(f"   Categories with basic info only: {categories_without_details}")
    
    # Check for categories with product counts
    categories_with_products = sum(1 for cat in categories if cat.get('product_count', 0) > 0)
    total_products = sum(cat.get('product_count', 0) for cat in categories)
    
    print(f"   Categories with products: {categories_with_products}")
    print(f"   Total products: {total_products:,}")
    
    # Save missing IDs to file for reference
    if missing_ids:
        missing_file = "data/missing_category_ids.json"
        os.makedirs(os.path.dirname(missing_file), exist_ok=True)
        with open(missing_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_missing': len(missing_ids),
                'missing_ids': sorted(list(missing_ids)),
                'fetched_total': len(fetched_ids),
                'saved_total': len(saved_ids)
            }, f, indent=2)
        print(f"\n💾 Missing category IDs saved to: {missing_file}")

if __name__ == "__main__":
    analyze_completeness()


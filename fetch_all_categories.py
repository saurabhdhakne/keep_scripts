"""
Fetch All Amazon Categories and Save to File (Batch Mode with Resume Support)
This script fetches all categories from Keepa API in batches and saves progress.
You can stop and resume anytime - it will continue from where it left off.

Features:
- Batch processing with token monitoring
- Progress tracking (saves fetched category IDs)
- Resume capability (continues from last checkpoint)
- Automatic token checking before each batch

Usage:
    python fetch_all_categories.py [--batch-size N] [--min-tokens N] [--resume]
    
    --batch-size: Number of categories to fetch per batch (default: 10)
    --min-tokens: Minimum tokens required to continue (default: 5)
    --resume: Resume from last checkpoint (default: True)
"""

import keepa
import os
import json
import csv
import argparse
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")
api = keepa.Keepa(API_KEY)

# Output files
JSON_FILE = "data/amazon_categories.json"
CSV_FILE = "data/amazon_categories.csv"
PROGRESS_FILE = "data/fetch_progress.json"

def get_token_count():
    """
    Get current token count. Makes a minimal API call if tokens_left is not available.
    The tokens_left property is only populated after the first API call.
    """
    tokens = api.tokens_left
    
    # If tokens_left is 0 or None, it might not be populated yet
    # Make a minimal API call to refresh it (category search is cheap: 1-2 tokens)
    if tokens == 0 or tokens is None:
        try:
            # Make a minimal API call to populate tokens_left
            # Using search_for_categories with a common term (costs 1-2 tokens)
            print("⚠️  Token count not available. Making initial API call to refresh...")
            api.search_for_categories("Electronics")
            tokens = api.tokens_left
            print(f"✓ Token count refreshed: {tokens} tokens available")
        except Exception as e:
            print(f"⚠️  Error refreshing token count: {e}")
            print("   Continuing anyway - tokens will be checked during fetch...")
            return 0
    
    return tokens

def load_progress():
    """Load progress from checkpoint file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convert list back to set for fetched_category_ids
            if isinstance(data.get('fetched_category_ids'), list):
                data['fetched_category_ids'] = set(data['fetched_category_ids'])
            elif not isinstance(data.get('fetched_category_ids'), set):
                data['fetched_category_ids'] = set()
            return data
    return {
        'fetched_category_ids': set(),
        'search_terms_completed': [],
        'last_updated': None
    }

def save_progress(progress):
    """Save progress to checkpoint file."""
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    # Convert set to list for JSON serialization
    progress_copy = progress.copy()
    progress_copy['fetched_category_ids'] = list(progress['fetched_category_ids'])
    progress_copy['last_updated'] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_copy, f, indent=2)

def load_existing_categories():
    """Load already fetched categories from JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('categories', [])
    return []

def fetch_categories_by_search_terms(progress, batch_size=10, min_tokens=5):
    """
    Fetch categories by searching with common keywords in batches.
    This approach uses search_for_categories which is more reliable.
    
    Args:
        progress: Progress dictionary with fetched_category_ids set
        batch_size: Number of categories to fetch details for per batch
        min_tokens: Minimum tokens required to continue
    
    Returns:
        List of new category dictionaries fetched in this batch
    """
    # Common Amazon category keywords to get comprehensive coverage
    all_search_terms = [
        "Electronics", "Books", "Clothing", "Home", "Kitchen", "Sports",
        "Toys", "Beauty", "Health", "Automotive", "Garden", "Pet",
        "Baby", "Grocery", "Office", "Tools", "Music", "Movies",
        "Video Games", "Software", "Cell Phones", "Computers", "Appliances",
        "Furniture", "Jewelry", "Watches", "Shoes", "Handbags", "Luggage"
    ]
    
    # Filter out completed search terms
    remaining_terms = [t for t in all_search_terms if t not in progress.get('search_terms_completed', [])]
    
    fetched_ids = progress['fetched_category_ids']
    new_categories = {}
    
    # Step 1: Search for categories (1-2 tokens per search term)
    print("\n" + "=" * 60)
    print("STEP 1: Searching for categories with keywords")
    print("=" * 60)
    
    for i, term in enumerate(remaining_terms, 1):
        # Check tokens before each search
        tokens_left = api.tokens_left
        # If tokens_left is 0, it might not be populated - continue anyway
        if tokens_left > 0 and tokens_left < min_tokens:
            print(f"\n⚠️  Low tokens ({tokens_left}). Stopping search phase.")
            print(f"   Progress saved. Resume later to continue.")
            return []
        
        try:
            print(f"  [{i}/{len(remaining_terms)}] Searching: {term} (Tokens: {tokens_left})")
            categories = api.search_for_categories(term)
            
            new_count = 0
            for cat_id, cat_name in categories.items():
                cat_id_int = int(cat_id)
                if cat_id_int not in fetched_ids:
                    new_categories[cat_id_int] = {
                        'category_id': cat_id_int,
                        'name': cat_name,
                        'parent_id': None,
                        'domain': 1,
                        'product_count': 0,
                        'children_count': 0,
                        'children_ids': [],
                        'depth': 0
                    }
                    fetched_ids.add(cat_id_int)
                    new_count += 1
            
            if new_count > 0:
                print(f"    ✓ Found {new_count} new categories")
            else:
                print(f"    - No new categories")
            
            # Mark search term as completed
            if term not in progress.get('search_terms_completed', []):
                progress['search_terms_completed'].append(term)
            save_progress(progress)
            
        except Exception as e:
            print(f"    ✗ Error searching '{term}': {e}")
    
    if not new_categories:
        print("\n✓ All search terms completed. No new categories found.")
        return []
    
    # Step 2: Fetch detailed information in batches
    print(f"\n" + "=" * 60)
    print(f"STEP 2: Fetching detailed information (batch mode)")
    print("=" * 60)
    print(f"Found {len(new_categories)} new categories to fetch details for")
    print(f"Batch size: {batch_size}, Min tokens: {min_tokens}")
    
    category_list = list(new_categories.items())
    detailed_categories = []
    batch_count = 0
    
    for i, (cat_id, cat_data) in enumerate(category_list, 1):
        # Check tokens before each batch
        tokens_left = api.tokens_left
        # If tokens_left is 0, it might not be populated - continue anyway
        if tokens_left > 0 and tokens_left < min_tokens:
            print(f"\n⚠️  Low tokens ({tokens_left}). Stopping batch processing.")
            print(f"   Progress: {i-1}/{len(category_list)} categories processed")
            print(f"   Progress saved. Resume later to continue from category {cat_id}.")
            break
        
        try:
            # Fetch detailed category info (1-2 tokens per lookup)
            category_info = api.category_lookup(cat_id)
            
            if category_info:
                if isinstance(category_info, dict):
                    if 'catId' in category_info:
                        # Single category object
                        cat_data.update({
                            'parent_id': category_info.get('parent'),
                            'product_count': category_info.get('productCount', 0),
                            'children_count': len(category_info.get('children', [])),
                            'children_ids': category_info.get('children', [])
                        })
                    else:
                        # Try to get first category from dict
                        for key, value in category_info.items():
                            if isinstance(value, dict) and 'name' in value:
                                cat_data.update({
                                    'parent_id': value.get('parent'),
                                    'product_count': value.get('productCount', 0),
                                    'children_count': len(value.get('children', [])),
                                    'children_ids': value.get('children', [])
                                })
                                break
            
            detailed_categories.append(cat_data)
            
            # Save progress every batch_size categories
            if i % batch_size == 0:
                batch_count += 1
                tokens_left = api.tokens_left
                print(f"  Batch {batch_count}: Processed {i}/{len(category_list)} categories (Tokens left: {tokens_left})")
                # Update progress
                progress['fetched_category_ids'] = fetched_ids
                save_progress(progress)
                
        except Exception as e:
            print(f"    ✗ Error fetching category {cat_id}: {e}")
            # Still add basic data
            detailed_categories.append(cat_data)
    
    # Final progress update
    progress['fetched_category_ids'] = fetched_ids
    save_progress(progress)
    
    print(f"\n✓ Batch complete: {len(detailed_categories)} categories fetched")
    return detailed_categories

def save_to_json(categories, filename, append=False):
    """Save categories to JSON file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    if append and os.path.exists(filename):
        # Load existing categories
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_categories = existing_data.get('categories', [])
            
            # Merge with new categories (avoid duplicates)
            existing_ids = {cat['category_id'] for cat in existing_categories}
            new_categories = [cat for cat in categories if cat['category_id'] not in existing_ids]
            all_categories = existing_categories + new_categories
    else:
        all_categories = categories
    
    data = {
        'last_updated': datetime.now().isoformat(),
        'total_categories': len(all_categories),
        'categories': all_categories
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    if append:
        print(f"Added {len(categories)} new categories. Total: {len(all_categories)} categories saved to {filename}")
    else:
        print(f"Saved {len(all_categories)} categories to {filename}")

def save_to_csv(categories, filename, append=False):
    """Save categories to CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    if not categories:
        print("No categories to save to CSV")
        return
    
    fieldnames = ['category_id', 'name', 'parent_id', 'domain', 'product_count', 
                 'children_count', 'children_ids', 'depth']
    
    file_exists = os.path.exists(filename)
    existing_ids = set()
    
    if append and file_exists:
        # Read existing IDs
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_ids = {int(row['category_id']) for row in reader}
    
    mode = 'a' if append and file_exists else 'w'
    with open(filename, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not (append and file_exists):
            writer.writeheader()
        
        new_count = 0
        for cat in categories:
            if cat['category_id'] not in existing_ids:
                # Convert children_ids list to string for CSV
                row = cat.copy()
                row['children_ids'] = ','.join(map(str, row.get('children_ids', [])))
                writer.writerow(row)
                new_count += 1
        
        if append:
            print(f"Added {new_count} new categories to CSV. Total categories in file.")
        else:
            print(f"Saved {len(categories)} categories to {filename}")

def main():
    """Main function to fetch and save all categories in batches."""
    parser = argparse.ArgumentParser(description='Fetch Amazon categories in batches with resume support')
    parser.add_argument('--batch-size', type=int, default=10, 
                       help='Number of categories to fetch per batch (default: 10)')
    parser.add_argument('--min-tokens', type=int, default=5,
                       help='Minimum tokens required to continue (default: 5)')
    parser.add_argument('--resume', action='store_true', default=True,
                       help='Resume from last checkpoint (default: True)')
    parser.add_argument('--reset', action='store_true',
                       help='Reset progress and start fresh')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Fetching Amazon Categories (Batch Mode with Resume)")
    print("=" * 60)
    
    # Load or reset progress
    if args.reset:
        print("\n⚠️  Resetting progress...")
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
        progress = {
            'fetched_category_ids': set(),
            'search_terms_completed': [],
            'last_updated': None
        }
    else:
        progress = load_progress()
        # Ensure fetched_category_ids is a set (load_progress handles conversion)
        if not isinstance(progress.get('fetched_category_ids'), set):
            progress['fetched_category_ids'] = set(progress.get('fetched_category_ids', []))
    
    initial_tokens = get_token_count()
    print(f"\nInitial tokens: {initial_tokens}")
    print(f"Batch size: {args.batch_size}")
    print(f"Min tokens to continue: {args.min_tokens}")
    
    if progress['fetched_category_ids']:
        print(f"\n📊 Resume mode: Found {len(progress['fetched_category_ids'])} already fetched categories")
        print(f"   Search terms completed: {len(progress.get('search_terms_completed', []))}")
        if progress.get('last_updated'):
            print(f"   Last updated: {progress['last_updated']}")
    
    if initial_tokens < args.min_tokens:
        print(f"\n⚠️  Not enough tokens ({initial_tokens} < {args.min_tokens})")
        print("   Please wait for tokens to refill, then run again.")
        return
    
    # Load existing categories
    existing_categories = load_existing_categories()
    print(f"\n📁 Existing categories in cache: {len(existing_categories)}")
    
    # Fetch new categories
    print("\n" + "=" * 60)
    print("Starting batch fetch...")
    print("=" * 60)
    
    new_categories = fetch_categories_by_search_terms(
        progress, 
        batch_size=args.batch_size,
        min_tokens=args.min_tokens
    )
    
    final_tokens = api.tokens_left
    # Calculate tokens used (handle case where initial was refreshed)
    if initial_tokens > 0:
        tokens_used = initial_tokens - final_tokens
    else:
        tokens_used = 0  # Can't calculate if we don't know initial
    
    print(f"\n{'='*60}")
    print(f"Batch Complete!")
    print(f"{'='*60}")
    print(f"New categories fetched in this run: {len(new_categories)}")
    print(f"Total categories fetched so far: {len(progress['fetched_category_ids'])}")
    print(f"Tokens used in this run: {tokens_used}")
    print(f"Tokens remaining: {final_tokens}")
    
    if new_categories:
        # Save to files (append mode)
        print(f"\nSaving categories to files...")
        save_to_json(new_categories, JSON_FILE, append=True)
        save_to_csv(new_categories, CSV_FILE, append=True)
        
        print(f"\n✅ Success! Categories saved to:")
        print(f"   - {JSON_FILE}")
        print(f"   - {CSV_FILE}")
        print(f"   - Progress: {PROGRESS_FILE}")
        
        if final_tokens < args.min_tokens:
            print(f"\n⚠️  Low tokens ({final_tokens}). Run again later to continue.")
            print(f"   Progress saved. Use: python fetch_all_categories.py --resume")
        else:
            print(f"\n💡 You can run this script again to fetch more categories.")
            print(f"   It will automatically resume from where it left off.")
    else:
        if final_tokens < args.min_tokens:
            print(f"\n⚠️  No new categories fetched (low tokens).")
            print(f"   Progress saved. Run again when tokens are refilled.")
        else:
            print(f"\n✓ All categories have been fetched!")
            print(f"   You can now use category_utils.py to read from cached files")

if __name__ == "__main__":
    main()


"""
Fetch Products by Category ID
Gets a list of product ASINs from a specific category using Keepa API.

Token Usage:
- Best sellers query: ~5-15 tokens (depends on category size)
- Product details (optional): 1 token per product
"""

import keepa
import os
import json
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Category ID (use find_category.py or category_utils.py to find IDs)
CATEGORY_ID = 16285951  # Example: Personal Electronics

# Marketplace ('US', 'GB', 'DE', 'FR', 'JP', 'CA', 'CN', 'IT', 'ES', 'IN', 'MX', 'BR')
DOMAIN = 'US'

# Maximum number of ASINs to return (None = all, or set a limit to save tokens)
MAX_ASINS = None  # Set to None for all, or a number like 100, 500, 1000

# Fetch detailed product information? (True = fetch details, False = ASINs only)
# Note: Fetching details costs 1 token per product
FETCH_DETAILS = False

# Output file
OUTPUT_FILE = "data/products_by_category.json"

# ============================================================================
# CODE BELOW - NO NEED TO EDIT
# ============================================================================

KEEPA_API_KEY = os.getenv("KEEPA_API_KEY")
if not KEEPA_API_KEY:
    print("❌ Error: KEEPA_API_KEY not found in .env file")
    exit(1)

api = keepa.Keepa(KEEPA_API_KEY)

def get_token_count():
    """Get current token count, refreshing if needed."""
    tokens = api.tokens_left
    if tokens == 0 or tokens is None:
        try:
            print("⚠️  Refreshing token count...")
            api.search_for_categories("Electronics")
            tokens = api.tokens_left
            print(f"✓ Token count: {tokens}")
        except Exception as e:
            print(f"⚠️  Error refreshing tokens: {e}")
            return 0
    return tokens

def fetch_products_by_category():
    """Fetch products (ASINs) from a category."""
    print("=" * 60)
    print("Fetch Products by Category ID")
    print("=" * 60)
    
    # Get token count
    initial_tokens = get_token_count()
    print(f"\nInitial tokens: {initial_tokens}")
    
    print(f"\nCategory ID: {CATEGORY_ID}")
    print(f"Domain: {DOMAIN}")
    print(f"Max ASINs: {MAX_ASINS if MAX_ASINS else 'All'}")
    print(f"Fetch Details: {FETCH_DETAILS}")
    
    try:
        # Step 1: Get best sellers from category
        print("\n" + "=" * 60)
        print("STEP 1: Fetching best sellers from category")
        print("=" * 60)
        print("Fetching ASINs...")
        
        asins = api.best_sellers_query(CATEGORY_ID, domain=DOMAIN)
        
        if not asins:
            print("\n⚠️  No products found in this category.")
            print("   Check if the category ID is correct.")
            return []
        
        print(f"✓ Found {len(asins)} products in category")
        
        # Limit ASINs if specified
        if MAX_ASINS and len(asins) > MAX_ASINS:
            asins = asins[:MAX_ASINS]
            print(f"✓ Limited to first {len(asins)} ASINs")
        
        # Step 2: Optionally fetch product details
        products = []
        if FETCH_DETAILS:
            print("\n" + "=" * 60)
            print("STEP 2: Fetching product details")
            print("=" * 60)
            print(f"Fetching details for {len(asins)} products...")
            print("⚠️  This will cost 1 token per product!")
            
            # Fetch in batches to avoid overwhelming the API
            batch_size = 100
            for i in range(0, len(asins), batch_size):
                batch = asins[i:i + batch_size]
                print(f"  Fetching batch {i//batch_size + 1}/{(len(asins) + batch_size - 1)//batch_size}...")
                try:
                    batch_products = api.query(batch, stats=0, history=0)
                    products.extend(batch_products)
                    print(f"    ✓ Fetched {len(batch_products)} products")
                except Exception as e:
                    print(f"    ✗ Error fetching batch: {e}")
                    continue
            
            print(f"✓ Total products with details: {len(products)}")
        else:
            print("\n⚠️  Skipping product details fetch (FETCH_DETAILS = False)")
            print("   Set FETCH_DETAILS = True to get full product information")
        
        # Calculate token usage
        final_tokens = get_token_count()
        tokens_used = initial_tokens - final_tokens if initial_tokens > 0 else 0
        
        # Prepare results
        result_data = {
            'category_id': CATEGORY_ID,
            'domain': DOMAIN,
            'total_asins': len(asins),
            'asins': asins,
            'has_details': FETCH_DETAILS,
            'products': products if FETCH_DETAILS else [],
            'tokens_used': tokens_used,
            'tokens_remaining': final_tokens
        }
        
        # Save results
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total ASINs fetched: {len(asins)}")
        if FETCH_DETAILS:
            print(f"Products with details: {len(products)}")
        print(f"Tokens used: {tokens_used}")
        print(f"Tokens remaining: {final_tokens}")
        print(f"\n✅ Results saved to: {OUTPUT_FILE}")
        
        # Display sample ASINs
        print("\n" + "=" * 60)
        print("SAMPLE ASINs (First 10)")
        print("=" * 60)
        for i, asin in enumerate(asins[:10], 1):
            print(f"  {i}. {asin}")
        if len(asins) > 10:
            print(f"  ... and {len(asins) - 10} more ASINs")
        
        return asins
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    fetch_products_by_category()

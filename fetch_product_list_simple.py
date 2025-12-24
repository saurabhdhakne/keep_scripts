"""
Simple Product List Fetcher with Filters
This script fetches best seller ASINs from a category and filters them based on criteria.
Token-efficient: ~15-35 tokens (best sellers + minimal product details for filtering)

Edit the parameters below and run!
"""

import keepa
import os
import json
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Required: Category ID (use find_category.py or category_utils.py to find IDs)
CATEGORY_ID = 20  # Example: 20 for Electronics

# Marketplace ('US', 'GB', 'DE', 'FR', 'JP', 'CA', 'CN', 'IT', 'ES', 'IN', 'MX', 'BR')
DOMAIN = 'US'  # US

# Price Range (in USD)
PRICE_MIN = 15.0
PRICE_MAX = 60.0

# Monthly Sales (minimum) - Note: Not directly available, using BSR as proxy
SALES_MIN = 100

# Best Seller Rank Range
BSR_MIN = 500
BSR_MAX = 50000

# Number of Sellers Range
SELLERS_MIN = 2
SELLERS_MAX = 15

# Keepa Stable (True = only stable products, False = all products)
# Note: May not be directly available in basic query
KEEPA_STABLE = True

# Maximum number of ASINs to return (keep low to save tokens)
MAX_RESULTS = 10

# Output file
OUTPUT_FILE = "data/product_list.json"

# ============================================================================
# CODE BELOW - NO NEED TO EDIT
# ============================================================================

KEEPA_API_KEY = os.getenv("KEEPA_API_KEY")
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

def filter_products(products):
    """Filter products based on criteria and return ASINs only."""
    print("\nFiltering products based on criteria...")
    print(f"  Price: ${PRICE_MIN:.2f} - ${PRICE_MAX:.2f}")
    print(f"  BSR: {BSR_MIN:,} - {BSR_MAX:,}")
    print(f"  Sellers: {SELLERS_MIN} - {SELLERS_MAX}")
    print(f"  Note: Monthly Sales filter not directly available")
    
    filtered_asins = []
    
    for product in products:
        # Price filter (BuyBoxPrice in cents, convert to dollars)
        buybox_price = product.get('buyBoxPrice', 0)
        if buybox_price > 0:
            price_dollars = buybox_price / 100.0
            if PRICE_MIN is not None and price_dollars < PRICE_MIN:
                continue
            if PRICE_MAX is not None and price_dollars > PRICE_MAX:
                continue
        
        # BSR filter (salesRank)
        sales_rank = product.get('salesRank', 0)
        if sales_rank > 0:
            if BSR_MIN is not None and sales_rank < BSR_MIN:
                continue
            if BSR_MAX is not None and sales_rank > BSR_MAX:
                continue
        
        # Sellers filter (numberOfSellers or numberOfOffers)
        num_sellers = product.get('numberOfSellers', product.get('numberOfOffers', 0))
        if num_sellers > 0:
            if SELLERS_MIN is not None and num_sellers < SELLERS_MIN:
                continue
            if SELLERS_MAX is not None and num_sellers > SELLERS_MAX:
                continue
        
        # Add ASIN to filtered list
        asin = product.get('asin')
        if asin:
            filtered_asins.append(asin)
        
        # Stop early if we have enough
        if len(filtered_asins) >= MAX_RESULTS:
            break
    
    print(f"✓ {len(filtered_asins)} products match all criteria")
    return filtered_asins[:MAX_RESULTS]

def fetch_product_list():
    """Fetch best seller ASINs from category with filters applied."""
    print("=" * 60)
    print("Keepa Product List Fetcher with Filters")
    print("=" * 60)
    
    # Get token count
    initial_tokens = get_token_count()
    print(f"\nInitial tokens: {initial_tokens}")
    
    print("\n" + "=" * 60)
    print("FILTER CONFIGURATION")
    print("=" * 60)
    print(f"Category ID: {CATEGORY_ID}")
    print(f"Domain: {DOMAIN}")
    print(f"Price: ${PRICE_MIN:.2f} - ${PRICE_MAX:.2f}")
    print(f"BSR: {BSR_MIN:,} - {BSR_MAX:,}")
    print(f"Sellers: {SELLERS_MIN} - {SELLERS_MAX}")
    print(f"Max Results: {MAX_RESULTS}")
    
    try:
        # Step 1: Get best sellers
        print("\n" + "=" * 60)
        print("STEP 1: Fetching best sellers")
        print("=" * 60)
        print("Fetching best sellers from category...")
        asins = api.best_sellers_query(CATEGORY_ID, domain=DOMAIN)
        
        if not asins:
            print("\n⚠️  No best sellers found in category.")
            print("   Check if the category ID is correct.")
            return []
        
        print(f"✓ Found {len(asins)} best sellers in category")
        
        # Step 2: Fetch minimal product details for filtering
        # Only fetch a small batch to save tokens
        asins_to_check = asins[:min(MAX_RESULTS * 3, 30)]  # Check 3x to account for filtering
        print(f"\n" + "=" * 60)
        print("STEP 2: Fetching minimal product details for filtering")
        print("=" * 60)
        print(f"Fetching details for {len(asins_to_check)} products (minimal stats to save tokens)...")
        
        products = api.query(asins_to_check, stats=0, history=0)  # Minimal stats = 1 token per product
        print(f"✓ Fetched details for {len(products)} products")
        
        # Step 3: Filter products
        print("\n" + "=" * 60)
        print("STEP 3: Filtering products")
        print("=" * 60)
        filtered_asins = filter_products(products)
        
        if not filtered_asins:
            print("\n⚠️  No products match all the filter criteria.")
            print("   Try adjusting the filters at the top of the script.")
            return []
        
        # Calculate token usage
        final_tokens = api.tokens_left
        tokens_used = initial_tokens - final_tokens if initial_tokens > 0 else 0
        
        print("\n" + "=" * 60)
        print("RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total best sellers in category: {len(asins)}")
        print(f"Products checked: {len(products)}")
        print(f"ASINs matching filters: {len(filtered_asins)}")
        print(f"Tokens used: {tokens_used} (estimated: 15-35 tokens)")
        print(f"Tokens remaining: {final_tokens}")
        
        # Save results
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        result_data = {
            'category_id': CATEGORY_ID,
            'domain': DOMAIN,
            'filters_applied': {
                'price_min': PRICE_MIN,
                'price_max': PRICE_MAX,
                'bsr_min': BSR_MIN,
                'bsr_max': BSR_MAX,
                'sellers_min': SELLERS_MIN,
                'sellers_max': SELLERS_MAX,
                'keepa_stable': KEEPA_STABLE
            },
            'total_best_sellers': len(asins),
            'products_checked': len(products),
            'asins_matching_filters': len(filtered_asins),
            'max_results': MAX_RESULTS,
            'asins': filtered_asins
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Results saved to: {OUTPUT_FILE}")
        
        # Display ASINs
        print("\n" + "=" * 60)
        print("FILTERED PRODUCT LIST (ASINs)")
        print("=" * 60)
        for i, asin in enumerate(filtered_asins, 1):
            print(f"  {i}. {asin}")
        
        return filtered_asins
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    fetch_product_list()


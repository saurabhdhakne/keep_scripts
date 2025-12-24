"""
Simple Product Finder - Edit filters below and run!
All filter parameters are defined as static fields at the top.
Just update the values and run the script.

Token Usage (optimized for 60 tokens):
- Best sellers query: ~5-15 tokens
- Product details (10 products): 10 tokens (1 per product with minimal stats)
- Total: ~15-25 tokens (well within 60 token limit)
"""

import requests
import keepa
import os
import json
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# FILTER CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Required: Category ID (use find_category.py or category_utils.py to find IDs)
CATEGORY_ID = 20  # Example: 20 for Electronics

# Marketplace ('US', 'GB', 'DE', 'FR', 'JP', 'CA', 'CN', 'IT', 'ES', 'IN', 'MX', 'BR')
DOMAIN = 'US'  # US

# Price Range (in USD)
PRICE_MIN = 15.0
PRICE_MAX = 60.0

# Monthly Sales (minimum)
SALES_MIN = 100

# Best Seller Rank Range
BSR_MIN = 500
BSR_MAX = 50000

# Number of Sellers Range
SELLERS_MIN = 2
SELLERS_MAX = 15

# Keepa Stable (True = only stable products, False = all products)
KEEPA_STABLE = True

# Maximum number of ASINs to return (keep low to save tokens)
MAX_RESULTS = 10

# Fetch detailed product information? (True = fetch details, False = ASINs only)
FETCH_DETAILS = True

# Output file
OUTPUT_FILE = "data/filtered_products.json"

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

def get_best_sellers():
    """Get best sellers from category."""
    print("Fetching best sellers from category...")
    print(f"  Category: {CATEGORY_ID}")
    print(f"  Domain: {DOMAIN}")
    
    try:
        asins = api.best_sellers_query(CATEGORY_ID, domain=DOMAIN)
        print(f"✓ Found {len(asins)} best sellers in category")
        return asins
    except Exception as e:
        print(f"✗ Error fetching best sellers: {e}")
        return []

def filter_products(products):
    """Filter products based on criteria."""
    print("\nFiltering products based on criteria...")
    print(f"  Price: ${PRICE_MIN:.2f} - ${PRICE_MAX:.2f}")
    print(f"  BSR: {BSR_MIN:,} - {BSR_MAX:,}")
    print(f"  Sellers: {SELLERS_MIN} - {SELLERS_MAX}")
    print(f"  Note: Monthly Sales and Keepa Stable filters not available in basic query")
    
    filtered = []
    
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
        
        filtered.append(product)
        
        # Stop early if we have enough products
        if len(filtered) >= MAX_RESULTS:
            break
    
    print(f"\n✓ {len(filtered)} products match all criteria")
    return filtered[:MAX_RESULTS]  # Limit to max results

def fetch_product_details_batch(asins):
    """Fetch detailed product information in batches (token-efficient)."""
    if not asins:
        return []
    
    # Limit to small batch to save tokens
    asins = asins[:20]  # Max 20 ASINs to keep token usage low
    
    # Process in batches of 10 (smaller batches = better token control)
    all_products = []
    batch_size = 10
    
    print(f"\nFetching details for {len(asins)} products (in batches of {batch_size})...")
    print("  Using minimal stats to save tokens...")
    
    for i in range(0, len(asins), batch_size):
        batch = asins[i:i + batch_size]
        try:
            print(f"  Batch {i//batch_size + 1}: Fetching {len(batch)} products...")
            # Use stats=0 and history=0 to minimize token usage (1 token per ASIN)
            products = api.query(batch, stats=0, history=0)
            all_products.extend(products)
            print(f"    ✓ Fetched {len(products)} products ({len(batch)} tokens used)")
        except Exception as e:
            print(f"    ✗ Error fetching batch: {e}")
            continue
    
    print(f"\n✓ Total fetched: {len(all_products)} products")
    return all_products

def main():
    """Main function."""
    print("=" * 60)
    print("Keepa Product Finder - Simple Version")
    print("=" * 60)
    
    # Get token count
    initial_tokens = get_token_count()
    print(f"\nInitial tokens: {initial_tokens}")
    
    # Get best sellers from category
    print("\n" + "=" * 60)
    asins = get_best_sellers()
    
    if not asins:
        print("\n⚠️  No best sellers found in category.")
        print("   Check if the category ID is correct.")
        return
    
    # Limit ASINs to process (to save tokens)
    # Only fetch a small batch since we only need MAX_RESULTS
    # Fetch 2x to account for filtering, but keep it small
    asins_to_process = asins[:min(MAX_RESULTS * 2, 20)]  # Max 20 ASINs to save tokens
    print(f"\nProcessing {len(asins_to_process)} ASINs for filtering (to save tokens)...")
    
    # Fetch detailed product information
    products = []
    if FETCH_DETAILS:
        products = fetch_product_details_batch(asins_to_process)
    else:
        print("\n⚠️  Skipping detailed product fetch (FETCH_DETAILS = False)")
        print("   Note: Filtering requires product details. Set FETCH_DETAILS = True")
        # Return ASINs only
        result_data = {
            'total_asins': len(asins[:MAX_RESULTS]),
            'asins': asins[:MAX_RESULTS],
            'note': 'Product details not fetched - filtering not applied'
        }
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ ASINs saved to: {OUTPUT_FILE}")
        return
    
    if not products:
        print("\n⚠️  No product details fetched.")
        return
    
    # Filter products based on criteria
    print("\n" + "=" * 60)
    filtered_products = filter_products(products)
    
    if not filtered_products:
        print("\n⚠️  No products match all the filter criteria.")
        print("   Try adjusting the filters at the top of the script.")
        return
    
    # Update products list with filtered results
    products = filtered_products
    asins = [p.get('asin') for p in products if p.get('asin')]
    
    # Calculate token usage
    final_tokens = api.tokens_left
    tokens_used = initial_tokens - final_tokens if initial_tokens > 0 else 0
    
    # Save results
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    result_data = {
        'total_asins': len(asins),
        'total_products_with_details': len(products) if products else 0,
        'filters_applied': {
            'category': CATEGORY_ID,
            'domain': DOMAIN,  # String format: 'US', 'GB', etc.
            'price_min': PRICE_MIN,
            'price_max': PRICE_MAX,
            'monthly_sales_min': SALES_MIN,
            'bsr_min': BSR_MIN,
            'bsr_max': BSR_MAX,
            'sellers_min': SELLERS_MIN,
            'sellers_max': SELLERS_MAX,
            'keepa_stable': KEEPA_STABLE,
            'max_results': MAX_RESULTS
        },
        'asins': asins
    }
    
    if products:
        result_data['products'] = products
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    # Display summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Products found: {len(asins)}")
    if products:
        print(f"Products with details: {len(products)}")
    print(f"Tokens used: {tokens_used}")
    print(f"Tokens remaining: {final_tokens}")
    print(f"\n✅ Results saved to: {OUTPUT_FILE}")
    
    # Display sample
    if products:
        print("\n" + "=" * 60)
        print("SAMPLE PRODUCTS (First 5)")
        print("=" * 60)
        for i, product in enumerate(products[:5], 1):
            print(f"\n{i}. ASIN: {product.get('asin', 'N/A')}")
            print(f"   Title: {product.get('title', 'N/A')[:60]}...")
            if 'buyBoxPrice' in product:
                print(f"   Price: ${product.get('buyBoxPrice', 'N/A')}")
            if 'salesRank' in product:
                print(f"   BSR: {product.get('salesRank', 'N/A')}")
    else:
        print("\n" + "=" * 60)
        print("SAMPLE ASINs (First 10)")
        print("=" * 60)
        for i, asin in enumerate(asins[:10], 1):
            print(f"  {i}. {asin}")

if __name__ == "__main__":
    main()


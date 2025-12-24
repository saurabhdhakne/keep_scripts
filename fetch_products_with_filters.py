"""
Fetch Products with Filters using Keepa API Product Finder
This script uses the Keepa API /finder endpoint to search for products
with specific criteria.

Default Parameters:
- Category: User selected (required)
- Marketplace: US (domain=1)
- Price: $15 – $60
- Monthly Sales: ≥ 100
- BSR: 500 – 50,000
- Sellers: 2 – 15
- Keepa Stable: Yes
- Max ASINs: 200

Token Cost: 2-5 tokens per finder query
"""

import requests
import keepa
import os
import json
import argparse
from dotenv import load_dotenv
from typing import Optional, List, Dict

load_dotenv()

KEEPA_API_KEY = os.getenv("KEEPA_API_KEY")
DOMAIN = 1  # 1 = Amazon.com (USA)

# Initialize Keepa API client for token tracking
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

def product_finder(
    category: int,
    domain: int = 1,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    sales_min: Optional[int] = None,
    bsr_min: Optional[int] = None,
    bsr_max: Optional[int] = None,
    sellers_min: Optional[int] = None,
    sellers_max: Optional[int] = None,
    keepa_stable: bool = True,
    max_results: int = 200
) -> List[str]:
    """
    Search for products using Keepa API Product Finder (/finder endpoint).
    
    Args:
        category: Category ID (required)
        domain: Amazon domain (1=US, 2=UK, 3=DE, etc.)
        price_min: Minimum price in USD
        price_max: Maximum price in USD
        sales_min: Minimum monthly sales (≥ value)
        bsr_min: Minimum Best Seller Rank
        bsr_max: Maximum Best Seller Rank
        sellers_min: Minimum number of sellers
        sellers_max: Maximum number of sellers
        keepa_stable: Only return products with stable Keepa data
        max_results: Maximum number of ASINs to return (max 200 per page)
    
    Returns:
        List of ASIN strings
    """
    url = "https://api.keepa.com/finder"
    
    # Build selection object for Keepa API
    selection = {
        "categories": [category]
    }
    
    # Add price filter (Keepa uses price in cents)
    if price_min is not None or price_max is not None:
        price_filter = {}
        if price_min is not None:
            price_filter["min"] = int(price_min * 100)  # Convert to cents
        if price_max is not None:
            price_filter["max"] = int(price_max * 100)  # Convert to cents
        selection["current_BuyBoxPrice"] = price_filter
    
    # Add monthly sales filter (≥ minimum)
    if sales_min is not None:
        selection["current_SALES"] = [sales_min]  # Array format for minimum
    
    # Add BSR (Best Seller Rank) filter
    if bsr_min is not None or bsr_max is not None:
        bsr_filter = {}
        if bsr_min is not None:
            bsr_filter["min"] = bsr_min
        if bsr_max is not None:
            bsr_filter["max"] = bsr_max
        selection["current_SALESRANK"] = bsr_filter
    
    # Add sellers filter
    # Note: Keepa uses current_New for new sellers count
    if sellers_min is not None or sellers_max is not None:
        sellers_filter = {}
        if sellers_min is not None:
            sellers_filter["min"] = sellers_min
        if sellers_max is not None:
            sellers_filter["max"] = sellers_max
        selection["current_New"] = sellers_filter
    
    # Add Keepa stable filter
    if keepa_stable:
        selection["isKeepaStable"] = True
    
    # Build request parameters
    params = {
        "key": KEEPA_API_KEY,
        "domain": domain,
        "selection": json.dumps(selection),  # Keepa expects JSON string
        "perPage": min(max_results, 200),  # API limit is 200 per page
        "page": 0
    }
    
    try:
        print(f"  Searching with filters...")
        print(f"    Category: {category}")
        if price_min or price_max:
            print(f"    Price: ${price_min or 0:.2f} - ${price_max or '∞'}")
        if sales_min:
            print(f"    Monthly Sales: ≥ {sales_min}")
        if bsr_min or bsr_max:
            print(f"    BSR: {bsr_min or 0} - {bsr_max or '∞'}")
        if sellers_min or sellers_max:
            print(f"    Sellers: {sellers_min or 0} - {sellers_max or '∞'}")
        if keepa_stable:
            print(f"    Keepa Stable: Yes")
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract ASINs from response
        if "asinList" in data:
            asins = data["asinList"]
            print(f"  ✓ Found {len(asins)} products matching criteria")
            return asins
        elif "error" in data:
            print(f"  ✗ API Error: {data.get('error', 'Unknown error')}")
            return []
        else:
            print(f"  ⚠️  Unexpected response format: {list(data.keys())}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"  ✗ API Request Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"    Error details: {error_data}")
            except:
                print(f"    Response text: {e.response.text[:200]}")
        return []
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return []

def fetch_product_details_batch(asins: List[str], max_asins: int = 200) -> List[Dict]:
    """
    Fetch detailed product information for a list of ASINs.
    
    Args:
        asins: List of ASIN strings
        max_asins: Maximum number of ASINs to fetch (default: 200)
    
    Returns:
        List of product dictionaries with full details
    """
    if not asins:
        return []
    
    # Limit to max_asins
    asins = asins[:max_asins]
    
    print(f"\nFetching details for {len(asins)} products...")
    
    # Use Keepa Python library to fetch product details
    try:
        products = api.query(asins, stats=180, history=0)
        print(f"✓ Fetched details for {len(products)} products")
        return products
    except Exception as e:
        print(f"✗ Error fetching product details: {e}")
        return []

def main():
    """Main function with configurable parameters."""
    parser = argparse.ArgumentParser(
        description='Fetch products using Keepa API Product Finder with filters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default filters (interactive category selection):
  python fetch_products_with_filters.py
  
  # Specify category ID directly:
  python fetch_products_with_filters.py --category 20
  
  # Custom filters:
  python fetch_products_with_filters.py --category 20 --price-min 20 --price-max 50 --sales-min 150
  
  # All parameters:
  python fetch_products_with_filters.py --category 20 --price-min 15 --price-max 60 \\
    --sales-min 100 --bsr-min 500 --bsr-max 50000 --sellers-min 2 --sellers-max 15 \\
    --keepa-stable --max-results 200
        """
    )
    
    parser.add_argument('--category', type=int, help='Category ID (required if not using interactive mode)')
    parser.add_argument('--domain', type=int, default=1, help='Amazon domain (1=US, 2=UK, 3=DE, etc.) Default: 1')
    parser.add_argument('--price-min', type=float, default=15.0, help='Minimum price in USD. Default: 15.0')
    parser.add_argument('--price-max', type=float, default=60.0, help='Maximum price in USD. Default: 60.0')
    parser.add_argument('--sales-min', type=int, default=100, help='Minimum monthly sales. Default: 100')
    parser.add_argument('--bsr-min', type=int, default=500, help='Minimum Best Seller Rank. Default: 500')
    parser.add_argument('--bsr-max', type=int, default=50000, help='Maximum Best Seller Rank. Default: 50000')
    parser.add_argument('--sellers-min', type=int, default=2, help='Minimum number of sellers. Default: 2')
    parser.add_argument('--sellers-max', type=int, default=15, help='Maximum number of sellers. Default: 15')
    parser.add_argument('--keepa-stable', action='store_true', default=True, help='Only stable Keepa products. Default: True')
    parser.add_argument('--no-keepa-stable', dest='keepa_stable', action='store_false', help='Allow unstable products')
    parser.add_argument('--max-results', type=int, default=200, help='Maximum ASINs to return. Default: 200')
    parser.add_argument('--skip-details', action='store_true', help='Skip fetching detailed product information (saves tokens)')
    parser.add_argument('--output', type=str, default='data/filtered_products.json', help='Output file path. Default: data/filtered_products.json')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Keepa Product Finder with Filters")
    print("=" * 60)
    
    # Get token count
    initial_tokens = get_token_count()
    print(f"\nInitial tokens: {initial_tokens}")
    
    # Display configuration
    print("\n" + "=" * 60)
    print("FILTER CONFIGURATION")
    print("=" * 60)
    print(f"Marketplace: {'US' if args.domain == 1 else f'Domain {args.domain}'}")
    print(f"Price: ${args.price_min:.2f} – ${args.price_max:.2f}")
    print(f"Monthly Sales: ≥ {args.sales_min}")
    print(f"BSR: {args.bsr_min:,} – {args.bsr_max:,}")
    print(f"Sellers: {args.sellers_min} – {args.sellers_max}")
    print(f"Keepa Stable: {'Yes' if args.keepa_stable else 'No'}")
    print(f"Max ASINs: {args.max_results}")
    
    # Get category ID
    if args.category:
        category_id = args.category
        print(f"\nCategory ID: {category_id}")
    else:
        # Interactive category selection
        print("\n" + "=" * 60)
        print("CATEGORY SELECTION")
        print("=" * 60)
        
        try:
            from category_utils import search_categories, get_category_by_id
            
            # Search for categories
            search_term = input("\nEnter category search term (e.g., 'Electronics'): ").strip()
            if not search_term:
                search_term = "Electronics"
            
            categories = search_categories(search_term)
            
            if not categories:
                print(f"⚠️  No categories found for '{search_term}'")
                category_id = int(input("Enter category ID manually: "))
            else:
                print(f"\nFound {len(categories)} categories:")
                for i, cat in enumerate(categories[:10], 1):
                    print(f"  {i}. [{cat['category_id']}] {cat['name']}")
                
                if len(categories) > 10:
                    print(f"  ... and {len(categories) - 10} more")
                
                choice = input(f"\nSelect category (1-{min(10, len(categories))}) or enter ID: ").strip()
                
                if choice.isdigit() and 1 <= int(choice) <= min(10, len(categories)):
                    category_id = categories[int(choice) - 1]['category_id']
                else:
                    category_id = int(choice) if choice.isdigit() else categories[0]['category_id']
        except Exception as e:
            print(f"⚠️  Error loading categories: {e}")
            category_id = int(input("Enter category ID: "))
        
        print(f"\nUsing category ID: {category_id}")
    
    # Apply filters
    print("\n" + "=" * 60)
    print("SEARCHING FOR PRODUCTS")
    print("=" * 60)
    
    # Search for products with filters
    asins = product_finder(
        category=category_id,
        domain=args.domain,
        price_min=args.price_min,
        price_max=args.price_max,
        sales_min=args.sales_min,
        bsr_min=args.bsr_min,
        bsr_max=args.bsr_max,
        sellers_min=args.sellers_min,
        sellers_max=args.sellers_max,
        keepa_stable=args.keepa_stable,
        max_results=args.max_results
    )
    
    if not asins:
        print("\n⚠️  No products found matching the criteria.")
        print("   Try adjusting the filters or category.")
        return
    
    # Fetch detailed product information (optional)
    if args.skip_details:
        print("\n⚠️  Skipping detailed product fetch (--skip-details flag set)")
        products = []
    else:
        products = fetch_product_details_batch(asins, max_asins=args.max_results)
    
    # Calculate token usage
    final_tokens = api.tokens_left
    tokens_used = initial_tokens - final_tokens if initial_tokens > 0 else 0
    
    # Display results
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Products found: {len(asins)}")
    print(f"Products with details: {len(products)}")
    print(f"Tokens used: {tokens_used}")
    print(f"Tokens remaining: {final_tokens}")
    
    # Save results
    output_file = args.output
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    result_data = {
        'total_asins': len(asins),
        'total_products_with_details': len(products) if products else 0,
        'filters_applied': {
            'category': category_id,
            'domain': args.domain,
            'price_min': args.price_min,
            'price_max': args.price_max,
            'monthly_sales_min': args.sales_min,
            'bsr_min': args.bsr_min,
            'bsr_max': args.bsr_max,
            'sellers_min': args.sellers_min,
            'sellers_max': args.sellers_max,
            'keepa_stable': args.keepa_stable,
            'max_results': args.max_results
        },
        'asins': asins
    }
    
    if products:
        result_data['products'] = products
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Results saved to: {output_file}")
    print(f"   - ASINs found: {len(asins)}")
    if products:
        print(f"   - Products with details: {len(products)}")
    
    # Display sample products
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
            if 'numberOfSellers' in product:
                print(f"   Sellers: {product.get('numberOfSellers', 'N/A')}")
    else:
        print("\n" + "=" * 60)
        print("SAMPLE ASINs (First 10)")
        print("=" * 60)
        for i, asin in enumerate(asins[:10], 1):
            print(f"  {i}. {asin}")

if __name__ == "__main__":
    main()


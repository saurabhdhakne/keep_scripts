"""
Example: Product Search
Token Cost: 2-5 tokens per search (depends on result size)

This example demonstrates:
- How to search for products
- Token usage tracking
- Optimizing search queries
"""

import keepa
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")
api = keepa.Keepa(API_KEY)

# Track token usage
initial_tokens = api.tokens_left
print(f"Initial tokens: {initial_tokens}")

# Search for products
# Token cost: 2-5 tokens depending on result size
search_term = "laptop"
print(f"\nSearching for products: '{search_term}'")

# Note: More specific searches may reduce token cost
# You can add filters like category, price range, etc.
search_results = api.product_search(search_term, domain=1)

# Calculate token usage
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"\nTokens used: {tokens_used} (expected: 2-5 tokens)")
print(f"Tokens remaining: {final_tokens}")

# Display results
if search_results:
    print(f"\nFound {len(search_results)} products")
    for i, product in enumerate(search_results[:5], 1):
        print(f"\nProduct {i}:")
        print(f"  ASIN: {product.get('asin', 'N/A')}")
        print(f"  Title: {product.get('title', 'N/A')[:50]}...")
        print(f"  Price: ${product.get('price', 'N/A')}")
else:
    print("\nNo products found")


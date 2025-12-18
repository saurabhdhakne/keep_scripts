"""
Example: Browsing Deals
Token Cost: 3-8 tokens (varies with filters)

This example demonstrates:
- How to browse deals with filters
- Token usage tracking
- Optimizing deal queries
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

# Browse deals
# Note: More specific filters may reduce token cost
# Token cost: 3-8 tokens depending on filters
print("\nFetching deals...")

# Example: Get deals for a specific category
# You can add filters like:
# - domain: Amazon domain (1 = US)
# - category: Category ID
# - minDiscount: Minimum discount percentage
# - maxAge: Maximum age of deal in hours
deals = api.deals_query(domain=1)  # Adjust parameters as needed

# Calculate token usage
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"\nTokens used: {tokens_used} (expected: 3-8 tokens)")
print(f"Tokens remaining: {final_tokens}")

# Display results
if deals:
    print(f"\nFound {len(deals)} deals")
    # Display first few deals
    for i, deal in enumerate(deals[:5], 1):
        print(f"\nDeal {i}:")
        print(f"  ASIN: {deal.get('asin', 'N/A')}")
        print(f"  Discount: {deal.get('discount', 'N/A')}%")
else:
    print("\nNo deals found")


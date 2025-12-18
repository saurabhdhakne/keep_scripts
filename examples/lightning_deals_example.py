"""
Example: Lightning Deals
Token Cost: 3-8 tokens per request

This example demonstrates:
- How to fetch current lightning deals
- Token usage tracking
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

# Fetch lightning deals
# Token cost: 3-8 tokens
print("\nFetching lightning deals...")

lightning_deals = api.lightning_deals_query(domain=1)  # 1 = Amazon US

# Calculate token usage
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"\nTokens used: {tokens_used} (expected: 3-8 tokens)")
print(f"Tokens remaining: {final_tokens}")

# Display results
if lightning_deals:
    print(f"\nFound {len(lightning_deals)} lightning deals")
    for i, deal in enumerate(lightning_deals[:5], 1):
        print(f"\nLightning Deal {i}:")
        print(f"  ASIN: {deal.get('asin', 'N/A')}")
        print(f"  Discount: {deal.get('discount', 'N/A')}%")
        print(f"  Time Remaining: {deal.get('timeRemaining', 'N/A')}")
else:
    print("\nNo lightning deals found")


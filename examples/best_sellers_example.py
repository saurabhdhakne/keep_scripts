"""
Example: Best Sellers Query
Token Cost: 5-15 tokens (depends on category size)

This example demonstrates:
- How to query best sellers in a category
- Token usage tracking
- Optimizing by using sub-categories
"""

import keepa
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")
# Using a sub-category reduces token cost (5-10 tokens vs 15 for root category)
CATEGORY_ID = 20  # Replace with your category ID

api = keepa.Keepa(API_KEY)

# Track token usage
initial_tokens = api.tokens_left
print(f"Initial tokens: {initial_tokens}")

# Query best sellers
# Note: Root categories return up to 100,000 ASINs (costs ~15 tokens)
#       Sub-categories return up to 3,000 ASINs (costs ~5-10 tokens)
asins = api.best_sellers_query(CATEGORY_ID)

# Calculate token usage
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"\nTotal products found: {len(asins)}")
print(f"Tokens used: {tokens_used}")
print(f"Tokens remaining: {final_tokens}")

# Process only what you need to save resources
MAX_TO_PROCESS = 10
print(f"\nFirst {MAX_TO_PROCESS} best sellers:")
for i, asin in enumerate(asins[:MAX_TO_PROCESS], 1):
    print(f"{i}. {asin}")


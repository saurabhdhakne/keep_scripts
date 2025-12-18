"""
Example: Category Lookup
Token Cost: 1-2 tokens per request

This example demonstrates:
- How to get category information by ID
- Token usage tracking
"""

import keepa
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")
api = keepa.Keepa(API_KEY)

# Category ID to lookup
CATEGORY_ID = 20  # Replace with your category ID

# Track token usage
initial_tokens = api.tokens_left
print(f"Initial tokens: {initial_tokens}")

# Lookup category information
# Note: This is a low-cost operation (1-2 tokens)
category_info = api.category_lookup(CATEGORY_ID)

# Calculate token usage
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"\nTokens used: {tokens_used} (expected: 1-2 tokens)")
print(f"Tokens remaining: {final_tokens}")

# Display category information
if category_info:
    print(f"\nCategory Information:")
    print(f"  ID: {category_info.get('catId', 'N/A')}")
    print(f"  Name: {category_info.get('name', 'N/A')}")
    print(f"  Parent ID: {category_info.get('parent', 'N/A')}")
else:
    print(f"\nCategory {CATEGORY_ID} not found")


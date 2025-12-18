"""
Example: Category Search
Token Cost: 1-2 tokens per search

This example demonstrates:
- How to search for categories by keyword
- Token usage tracking
- Finding category IDs for use in other queries
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

# Search for categories
search_term = "Electronics"
print(f"\nSearching for categories matching: '{search_term}'")

categories = api.search_for_categories(search_term)

# Calculate token usage
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"\nTokens used: {tokens_used} (expected: 1-2 tokens)")
print(f"Tokens remaining: {final_tokens}")

# Display results
print(f"\nFound {len(categories)} categories:")
for cat_id, cat_name in list(categories.items())[:10]:  # Show first 10
    print(f"  Category ID: {cat_id}, Name: {cat_name}")

if len(categories) > 10:
    print(f"  ... and {len(categories) - 10} more categories")


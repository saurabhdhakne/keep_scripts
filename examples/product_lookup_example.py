"""
Example: Product Lookup
Token Cost: 1+ tokens per ASIN (depends on parameters)

This example demonstrates:
- Basic product lookup (1 token per ASIN)
- Product lookup with buybox (+2 tokens)
- Product lookup with offers (+6 tokens per 10 offers)
- Batch requests (up to 100 ASINs)
- Token usage tracking
"""

import keepa
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")
api = keepa.Keepa(API_KEY)

# Example ASINs
asins = ["B08N5WRWNW", "B07H8QMZPV"]

print("=" * 60)
print("SCENARIO 1: Basic Product Lookup (1 token per ASIN)")
print("=" * 60)

initial_tokens = api.tokens_left
print(f"Initial tokens: {initial_tokens}")

# Basic lookup - 1 token per ASIN
products = api.query(asins, stats=180, history=0)

final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"Tokens used: {tokens_used} (expected: {len(asins)} tokens)")
print(f"Tokens remaining: {final_tokens}")

print("\n" + "=" * 60)
print("SCENARIO 2: Product Lookup with Buybox (+2 tokens per ASIN)")
print("=" * 60)

initial_tokens = api.tokens_left
print(f"Initial tokens: {initial_tokens}")

# With buybox - 3 tokens per ASIN (1 base + 2 buybox)
products = api.query(asins, stats=180, history=0, buybox=True)

final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"Tokens used: {tokens_used} (expected: {len(asins) * 3} tokens)")
print(f"Tokens remaining: {final_tokens}")

print("\n" + "=" * 60)
print("SCENARIO 3: Batch Request (Multiple ASINs)")
print("=" * 60)

# Batch request - more efficient than individual requests
batch_asins = ["B08N5WRWNW", "B07H8QMZPV", "B09JQCMV8X", "B08YZ2K3PV", "B09G9FPHY6"]

initial_tokens = api.tokens_left
print(f"Initial tokens: {initial_tokens}")
print(f"Querying {len(batch_asins)} products in batch...")

products = api.query(batch_asins, stats=180, history=0)

final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens

print(f"Tokens used: {tokens_used} (expected: {len(batch_asins)} tokens)")
print(f"Tokens remaining: {final_tokens}")
print(f"Efficiency: {len(batch_asins)} products for {tokens_used} tokens")


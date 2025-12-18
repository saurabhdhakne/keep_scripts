"""
Example: Token Optimization Strategies
This example demonstrates best practices for minimizing token usage.
"""

import keepa
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")
api = keepa.Keepa(API_KEY)

print("=" * 60)
print("TOKEN OPTIMIZATION STRATEGIES")
print("=" * 60)

# Strategy 1: Batch Requests
print("\n1. BATCH REQUESTS (Recommended)")
print("-" * 60)
print("Instead of making individual requests, batch multiple ASINs:")

initial_tokens = api.tokens_left

# Bad: Individual requests (10 tokens for 10 ASINs)
# for asin in asins:
#     product = api.query([asin])  # 1 token each = 10 tokens total

# Good: Batch request (10 tokens for 10 ASINs, but more efficient)
asins = ["B08N5WRWNW", "B07H8QMZPV", "B09JQCMV8X", "B08YZ2K3PV", "B09G9FPHY6"]
products = api.query(asins, stats=180, history=0)  # 5 tokens for 5 ASINs

final_tokens = api.tokens_left
print(f"   Batch request: {len(asins)} products = {initial_tokens - final_tokens} tokens")
print(f"   Efficiency: 1 token per product")

# Strategy 2: Selective Parameters
print("\n2. SELECTIVE PARAMETERS")
print("-" * 60)
print("Only request data you need:")

initial_tokens = api.tokens_left
# Minimal request: 1 token
products = api.query([asins[0]], stats=0, history=0)
tokens_minimal = initial_tokens - api.tokens_left

initial_tokens = api.tokens_left
# With buybox: 3 tokens
products = api.query([asins[0]], stats=0, history=0, buybox=True)
tokens_with_buybox = initial_tokens - api.tokens_left

print(f"   Minimal request: {tokens_minimal} token")
print(f"   With buybox: {tokens_with_buybox} tokens")
print(f"   Save {tokens_with_buybox - tokens_minimal} tokens by omitting buybox if not needed")

# Strategy 3: Use Sub-categories
print("\n3. USE SUB-CATEGORIES FOR BEST SELLERS")
print("-" * 60)
print("Sub-categories return fewer results and cost less:")

initial_tokens = api.tokens_left
# Using a sub-category (example)
asins = api.best_sellers_query(20)  # Replace with sub-category ID
tokens_sub = initial_tokens - api.tokens_left

print(f"   Sub-category query: {tokens_sub} tokens")
print(f"   Returns up to 3,000 ASINs (vs 100,000 for root categories)")
print(f"   Cost: ~5-10 tokens (vs ~15 tokens for root categories)")

# Strategy 4: Cache Results
print("\n4. CACHE RESULTS")
print("-" * 60)
print("Store results locally to avoid redundant API calls:")
print("   - Best sellers lists are updated daily")
print("   - Category searches rarely change")
print("   - Cache product data and refresh periodically")

# Strategy 5: Monitor Token Usage
print("\n5. MONITOR TOKEN USAGE")
print("-" * 60)
current_tokens = api.tokens_left
print(f"   Current tokens: {current_tokens}")
print(f"   Always check before and after API calls")
print(f"   Plan usage to avoid token expiration (60-minute window)")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("✓ Use batch requests (up to 100 ASINs per call)")
print("✓ Request only needed parameters")
print("✓ Use sub-categories when possible")
print("✓ Cache results to avoid redundant calls")
print("✓ Monitor token usage regularly")
print("✓ Plan API calls within 60-minute token expiration window")


import keepa
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")
CATEGORY_ID = 1055398 # Home & Kitchen
CATEGORY_ID = 16285951 # Personal Electronics
# Limit the number of ASINs to process (reduces unnecessary processing)
MAX_ASINS_TO_PROCESS = 10

api = keepa.Keepa(API_KEY)

# Get initial token count
initial_tokens = api.tokens_left

# Get best-selling ASINs in the category
# Note: This query has a fixed token cost regardless of result size
# Using a sub-category instead of root category can reduce result size
# (sub-categories return up to 3,000 ASINs vs 100,000 for root categories)
asins = api.best_sellers_query(CATEGORY_ID)

# Limit results immediately to reduce memory usage and processing
limited_asins = asins[:MAX_ASINS_TO_PROCESS]

print(f"Total products found: {len(asins)}")
print(f"Processing first {len(limited_asins)} ASINs:")

# Print limited ASINs
for asin in limited_asins:
    print(asin)

# Get final token count and calculate tokens used
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens
print(f"\nTokens used during this run: {tokens_used}")
print(f"Tokens remaining: {final_tokens}")

import keepa
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEEPA_API_KEY")

api = keepa.Keepa(API_KEY)

# Get initial token count
initial_tokens = api.tokens_left

# Search category by keyword
search_term = "Electronics"
categories = api.search_for_categories(search_term)

# Print category IDs and names
for cat_id, cat_name in categories.items():
    print(f"Category ID: {cat_id}, Name: {cat_name} \n")

# Get final token count and calculate tokens used
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens
print(f"\nTokens used during this run: {tokens_used}")
print(f"Tokens remaining: {final_tokens}")

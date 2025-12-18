import requests
import keepa
import os
from dotenv import load_dotenv

load_dotenv()

KEEPA_API_KEY = os.getenv("KEEPA_API_KEY")
DOMAIN = 1  # 1 = Amazon.com (USA)

# Initialize Keepa API client for token tracking
api = keepa.Keepa(KEEPA_API_KEY)

# Get initial token count
initial_tokens = api.tokens_left

def fetch_products_by_asins(asins):
    """
    asins: list of ASIN strings
    """
    url = "https://api.keepa.com/product"
    
    params = {
        "key": KEEPA_API_KEY,
        "domain": DOMAIN,
        "asin": ",".join(asins),
        "stats": 180,        
        "history": 0        
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Example usage
asins = ["1081439793", "1496412729"]
data = fetch_products_by_asins(asins)

print(data)

# Get final token count and calculate tokens used
final_tokens = api.tokens_left
tokens_used = initial_tokens - final_tokens
print(f"\nTokens used during this run: {tokens_used}")
print(f"Tokens remaining: {final_tokens}")

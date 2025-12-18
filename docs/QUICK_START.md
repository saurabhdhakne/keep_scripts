# Keepa API Quick Start Guide

## Getting Started

1. **Set up your API key:**
   - Create a `.env` file in the project root
   - Add: `KEEPA_API_KEY=your_api_key_here`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check your token balance:**
   ```python
   import keepa
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api = keepa.Keepa(os.getenv("KEEPA_API_KEY"))
   print(f"Tokens available: {api.tokens_left}")
   ```

## Common Use Cases

### 1. Find Categories
```python
categories = api.search_for_categories("Electronics")
# Cost: 1-2 tokens
```

### 2. Get Best Sellers
```python
asins = api.best_sellers_query(category_id)
# Cost: 5-15 tokens
```

### 3. Lookup Products
```python
products = api.query(["ASIN1", "ASIN2"])
# Cost: 1 token per ASIN
```

### 4. Track Token Usage
```python
initial = api.tokens_left
# ... make API calls ...
final = api.tokens_left
print(f"Used: {initial - final} tokens")
```

## Documentation

- **[Full Documentation](./README.md)** - Complete API reference
- **[Token Costs Guide](./TOKEN_COSTS.md)** - Quick reference for token costs
- **[Examples](../examples/)** - Code examples for all request types

## Important Reminders

⚠️ **Tokens expire after 60 minutes** - Use them efficiently!  
⚠️ **Batch requests** - Request up to 100 ASINs per call  
⚠️ **Monitor usage** - Always track token consumption  
⚠️ **Cache results** - Avoid redundant API calls

## Resources

- [Keepa API Official Documentation](https://keepa.com/#!api)
- [Keepa Python Library Docs](https://keepaapi.readthedocs.io/)


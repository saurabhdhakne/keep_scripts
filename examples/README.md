# Keepa API Examples

This directory contains practical examples demonstrating how to use the Keepa API efficiently while tracking and minimizing token usage.

## Example Files

### 1. `best_sellers_example.py`
Demonstrates how to query best sellers in a category.
- **Token Cost:** 5-15 tokens
- **Key Points:** Use sub-categories to reduce cost

### 2. `product_lookup_example.py`
Shows different product lookup scenarios:
- Basic lookup (1 token per ASIN)
- With buybox (+2 tokens)
- Batch requests (more efficient)

### 3. `category_search_example.py`
Demonstrates category searching by keyword.
- **Token Cost:** 1-2 tokens
- **Use Case:** Finding category IDs for other queries

### 4. `category_lookup_example.py`
Shows how to get category information by ID.
- **Token Cost:** 1-2 tokens
- **Use Case:** Getting category details

### 5. `deals_example.py`
Demonstrates browsing deals with filters.
- **Token Cost:** 3-8 tokens
- **Use Case:** Finding discounted products

### 6. `lightning_deals_example.py`
Shows how to fetch current lightning deals.
- **Token Cost:** 3-8 tokens
- **Use Case:** Real-time deal monitoring

### 7. `product_search_example.py`
Demonstrates product searching.
- **Token Cost:** 2-5 tokens
- **Use Case:** Finding products by keyword

### 8. `token_optimization_example.py`
Comprehensive guide to token optimization strategies.
- **Use Case:** Learning best practices

## Running Examples

All examples require:
1. A `.env` file with your `KEEPA_API_KEY`
2. The `keepa` and `python-dotenv` packages installed

To run an example:
```bash
python examples/best_sellers_example.py
```

## Token Usage Tracking

All examples include token usage tracking:
- Initial token count before API calls
- Final token count after API calls
- Tokens used calculation
- Expected token costs

## Best Practices Demonstrated

1. **Batch Requests:** Request multiple items in a single call
2. **Selective Parameters:** Only request needed data
3. **Sub-categories:** Use sub-categories for best sellers
4. **Token Monitoring:** Always track token usage
5. **Error Handling:** Check for API errors

## Related Documentation

- [Token Costs Guide](../docs/TOKEN_COSTS.md)
- [Main Documentation](../docs/README.md)
- [Keepa API Official Docs](https://keepa.com/#!api)


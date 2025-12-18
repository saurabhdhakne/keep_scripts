# Keepa API Token Costs - Quick Reference

This is a quick reference guide for token costs. For detailed documentation, see [README.md](./README.md).

## Token Cost Summary Table

| Request Type | Base Cost | Additional Costs | Total Range |
|--------------|-----------|------------------|-------------|
| **Product Lookup** | 1 token/ASIN | +2 (buybox), +6 per 10 offers | 1-50+ tokens |
| **Best Sellers** | - | Category size dependent | 5-15 tokens |
| **Browsing Deals** | - | Filter dependent | 3-8 tokens |
| **Category Lookup** | - | - | 1-2 tokens |
| **Category Search** | - | - | 1-2 tokens |
| **Product Search** | - | Result size dependent | 2-5 tokens |
| **Lightning Deals** | - | - | 3-8 tokens |
| **Most Rated Sellers** | - | - | 5-10 tokens |
| **Product Finder** | - | - | 2-5 tokens |
| **Seller Information** | - | - | 1-3 tokens |
| **Tracking (Create)** | - | - | 1-2 tokens |
| **Tracking (Update)** | - | - | 1 token |
| **Tracking (Delete)** | - | - | 0 tokens |
| **Graph Image** | - | - | 1 token/image |

## Detailed Breakdown

### Product Lookup Formula

```
Total Tokens = Base (1) + Buybox (0 or 2) + Offers (6 × ceil(offer_count / 10))
```

**Examples:**
- 1 ASIN, no extras: **1 token**
- 1 ASIN + buybox: **3 tokens**
- 1 ASIN + 15 offers: **10 tokens** (1 + 6 + 3)
- 10 ASINs (batch): **10 tokens** (1 per ASIN)
- 10 ASINs + buybox: **30 tokens** (10 × 3)

### Best Sellers Cost Factors

- **Root Category:** ~15 tokens (up to 100,000 ASINs)
- **Sub-Category:** ~5-10 tokens (up to 3,000 ASINs)
- **Product Group:** ~10-15 tokens

### Tips to Minimize Costs

1. **Batch product requests** (up to 100 ASINs per call)
2. **Avoid unnecessary parameters** (only request what you need)
3. **Use sub-categories** for best sellers queries
4. **Cache results** to avoid redundant calls
5. **Monitor token usage** before and after each request

## Token Generation & Expiration

- **Generation:** Continuous based on subscription plan
- **Expiration:** 60 minutes after generation
- **Unused tokens:** Lost after expiration
- **Monitoring:** Use `api.tokens_left` to check balance


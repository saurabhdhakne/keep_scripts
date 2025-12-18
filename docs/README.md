# Keepa API Documentation

This directory contains comprehensive documentation about the Keepa API, including token costs, request types, and example scenarios.

## Table of Contents

1. [General Information](#general-information)
2. [Token Cost Guide](#token-cost-guide)
3. [Available Requests](#available-requests)
4. [Response JSON Objects](#response-json-objects)
5. [Example Scenarios](#example-scenarios)

---

## General Information

### How Keepa API Plans Work

The Keepa API operates on a **token-based system**. Tokens are generated continuously based on your subscription plan and expire after **60 minutes** if unused.

#### Subscription Plans

| Tokens per Minute | Tokens per Month | Monthly Price |
|-------------------|------------------|---------------|
| 20                | 892,800          | €49           |
| 60                | 2,678,400        | €129          |
| 250               | 11,160,000       | €459          |
| 500               | 22,320,000       | €879          |
| 1,000             | 44,640,000       | €1,499        |
| 2,000             | 89,280,000       | €2,499        |
| 3,000             | 133,920,000      | €3,499        |
| 4,000             | 178,560,000      | €4,499        |

**Key Points:**
- Tokens are generated continuously, regardless of usage
- Each token expires after 60 minutes
- Unused tokens are lost, so plan your API usage efficiently
- Monitor your token balance using `api.tokens_left`

**Reference:** [Keepa API Documentation](https://keepa.com/#!api)

---

## Token Cost Guide

### Overview

Token costs vary based on the request type and parameters. Below is a detailed breakdown:

### 1. Product Lookup (`/product`)

**Base Cost:** 1 token per product

**Additional Costs:**
- **`buybox` parameter:** +2 tokens per product (includes buy box data)
- **`offers` parameter:** +6 tokens for every 10 offers per product
  - Example: 25 offers = 18 tokens (6 × 3 groups of 10)

**Examples:**
- Basic product lookup (1 ASIN): **1 token**
- Product with buybox: **3 tokens** (1 base + 2 buybox)
- Product with 25 offers: **19 tokens** (1 base + 18 offers)

### 2. Best Sellers Query (`/bestsellers`)

**Cost:** 5-15 tokens (depends on category size)
- Root categories (up to 100,000 ASINs): ~15 tokens
- Sub-categories (up to 3,000 ASINs): ~5-10 tokens

### 3. Browsing Deals (`/deals`)

**Cost:** 3-8 tokens (varies with filters applied)

### 4. Category Lookup (`/category`)

**Cost:** 1-2 tokens per request

### 5. Category Searches (`/search`)

**Cost:** 1-2 tokens per search

### 6. Product Searches (`/search`)

**Cost:** 2-5 tokens per search (depends on result size)

### 7. Lightning Deals (`/deals`)

**Cost:** 3-8 tokens per request

### 8. Most Rated Sellers

**Cost:** 5-10 tokens per request

### 9. Product Finder (`/finder`)

**Cost:** 2-5 tokens per finder query

### 10. Seller Information (`/seller`)

**Cost:** 1-3 tokens per seller lookup

### 11. Tracking Products (`/tracking`)

**Cost:** 
- Create tracking: 1-2 tokens
- Update tracking: 1 token
- Delete tracking: 0 tokens

### 12. Graph Image API

**Cost:** 1 token per image request

---

## Available Requests

### Best Sellers
Retrieve best-selling products in a category.

**Endpoint:** `/bestsellers`  
**Token Cost:** 5-15 tokens  
**See:** [examples/best_sellers_example.py](../examples/best_sellers_example.py)

### Browsing Deals
Browse available deals with filters.

**Endpoint:** `/deals`  
**Token Cost:** 3-8 tokens  
**See:** [examples/deals_example.py](../examples/deals_example.py)

### Category Lookup
Get category information by ID.

**Endpoint:** `/category`  
**Token Cost:** 1-2 tokens  
**See:** [examples/category_lookup_example.py](../examples/category_lookup_example.py)

### Category Searches
Search for categories by keyword.

**Endpoint:** `/search`  
**Token Cost:** 1-2 tokens  
**See:** [examples/category_search_example.py](../examples/category_search_example.py)

### Product Lookup
Get product data by ASIN(s).

**Endpoint:** `/product`  
**Token Cost:** 1+ tokens (depends on parameters)  
**See:** [examples/product_lookup_example.py](../examples/product_lookup_example.py)

### Product Searches
Search for products.

**Endpoint:** `/search`  
**Token Cost:** 2-5 tokens  
**See:** [examples/product_search_example.py](../examples/product_search_example.py)

### Lightning Deals
Get current lightning deals.

**Endpoint:** `/deals`  
**Token Cost:** 3-8 tokens  
**See:** [examples/lightning_deals_example.py](../examples/lightning_deals_example.py)

### Most Rated Sellers
Get most rated sellers in a category.

**Endpoint:** `/seller`  
**Token Cost:** 5-10 tokens

### Product Finder
Find products matching specific criteria.

**Endpoint:** `/finder`  
**Token Cost:** 2-5 tokens

### Seller Information
Get seller details and statistics.

**Endpoint:** `/seller`  
**Token Cost:** 1-3 tokens

### Tracking Products
Create, update, or delete product tracking.

**Endpoint:** `/tracking`  
**Token Cost:** 1-2 tokens (create/update), 0 (delete)

### Graph Image API
Generate price history graphs.

**Endpoint:** `/graph`  
**Token Cost:** 1 token per image

---

## Response JSON Objects

### Best Sellers Object
Contains list of ASINs and category information.

### Category Object
Contains category ID, name, and hierarchy.

### Deal Object
Contains deal information including discount, expiration, etc.

### Lightning Deal Object
Contains lightning deal details and time remaining.

### Marketplace Offer Object
Contains offer details including price, condition, seller info.

### Notification Object
Contains tracking notification details.

### Product Object
Contains comprehensive product data including:
- Price history
- Sales rank
- Reviews
- Images
- Offers

### Search Insights Object
Contains search result insights and statistics.

### Seller Object
Contains seller information and statistics.

### Statistics Object
Contains product statistics and metrics.

### Tracking Creation Object
Contains tracking creation confirmation.

### Tracking Object
Contains tracking status and product information.

**Reference:** [Keepa API Documentation - Response Objects](https://keepa.com/#!api)

---

## Example Scenarios

See the [examples](../examples/) directory for detailed code examples demonstrating:
- Token usage tracking
- Different request types
- Best practices for minimizing token consumption
- Error handling

---

## Best Practices for Token Management

1. **Batch Requests:** Request multiple products in a single call (up to 100 ASINs)
2. **Selective Parameters:** Only request data you need (avoid unnecessary `buybox` or `offers`)
3. **Use Sub-categories:** For best sellers, use sub-categories instead of root categories when possible
4. **Monitor Usage:** Always track token usage before and after API calls
5. **Cache Results:** Store results locally to avoid redundant API calls
6. **Plan Ahead:** Schedule API calls to use tokens before they expire (60-minute window)

---

## References

- [Keepa API Official Documentation](https://keepa.com/#!api)
- [Keepa Python Library Documentation](https://keepaapi.readthedocs.io/)


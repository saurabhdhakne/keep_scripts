# Product Finder with Filters - Usage Guide

This script uses the Keepa API `/finder` endpoint to search for products with specific filters.

## Default Configuration

- **Category**: User selected (required)
- **Marketplace**: US (domain=1)
- **Price**: $15 – $60
- **Monthly Sales**: ≥ 100
- **BSR**: 500 – 50,000
- **Sellers**: 2 – 15
- **Keepa Stable**: Yes
- **Max ASINs**: 200

## Quick Start

### Interactive Mode (Default)
```bash
python fetch_products_with_filters.py
```
This will prompt you to select a category and use default filters.

### With Category ID
```bash
python fetch_products_with_filters.py --category 20
```

### Custom Filters
```bash
python fetch_products_with_filters.py --category 20 \
  --price-min 20 --price-max 50 \
  --sales-min 150 \
  --bsr-min 1000 --bsr-max 30000 \
  --sellers-min 3 --sellers-max 10
```

## Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--category` | Required* | Category ID (required if not using interactive mode) |
| `--domain` | 1 | Amazon domain (1=US, 2=UK, 3=DE, etc.) |
| `--price-min` | 15.0 | Minimum price in USD |
| `--price-max` | 60.0 | Maximum price in USD |
| `--sales-min` | 100 | Minimum monthly sales |
| `--bsr-min` | 500 | Minimum Best Seller Rank |
| `--bsr-max` | 50000 | Maximum Best Seller Rank |
| `--sellers-min` | 2 | Minimum number of sellers |
| `--sellers-max` | 15 | Maximum number of sellers |
| `--keepa-stable` | True | Only return products with stable Keepa data |
| `--no-keepa-stable` | - | Allow unstable products |
| `--max-results` | 200 | Maximum ASINs to return |
| `--skip-details` | False | Skip fetching detailed product info (saves tokens) |
| `--output` | data/filtered_products.json | Output file path |

*Category is required but can be provided interactively if not specified

## Examples

### Example 1: Basic Usage
```bash
# Interactive category selection with default filters
python fetch_products_with_filters.py
```

### Example 2: Specific Category
```bash
# Use category ID 20 (Electronics) with default filters
python fetch_products_with_filters.py --category 20
```

### Example 3: Custom Price Range
```bash
# Search for products between $20-$50
python fetch_products_with_filters.py --category 20 \
  --price-min 20 --price-max 50
```

### Example 4: Higher Sales Requirement
```bash
# Products with at least 200 monthly sales
python fetch_products_with_filters.py --category 20 \
  --sales-min 200
```

### Example 5: Narrow BSR Range
```bash
# Products with BSR between 1,000-10,000
python fetch_products_with_filters.py --category 20 \
  --bsr-min 1000 --bsr-max 10000
```

### Example 6: More Sellers
```bash
# Products with 5-20 sellers
python fetch_products_with_filters.py --category 20 \
  --sellers-min 5 --sellers-max 20
```

### Example 7: Get ASINs Only (Save Tokens)
```bash
# Skip detailed product fetch to save tokens
python fetch_products_with_filters.py --category 20 --skip-details
```

### Example 8: All Custom Parameters
```bash
python fetch_products_with_filters.py \
  --category 20 \
  --price-min 25 \
  --price-max 75 \
  --sales-min 150 \
  --bsr-min 1000 \
  --bsr-max 30000 \
  --sellers-min 3 \
  --sellers-max 12 \
  --keepa-stable \
  --max-results 150 \
  --output data/my_products.json
```

## Token Usage

- **Product Finder Query**: 2-5 tokens per search
- **Product Details**: 1 token per ASIN (if not using `--skip-details`)
- **Total for 200 products**: ~202-205 tokens (with details) or 2-5 tokens (ASINs only)

## Output

The script saves results to a JSON file (default: `data/filtered_products.json`) containing:

```json
{
  "total_asins": 150,
  "total_products_with_details": 150,
  "filters_applied": {
    "category": 20,
    "price_min": 15.0,
    "price_max": 60.0,
    ...
  },
  "asins": ["B08N5WRWNW", "B07H8QMZPV", ...],
  "products": [...]
}
```

## Finding Category IDs

Use the cached category data (no tokens):
```python
from category_utils import search_categories

categories = search_categories("Electronics")
for cat in categories:
    print(f"{cat['category_id']}: {cat['name']}")
```

Or use the interactive mode in the script - it will search categories for you!

## Tips

1. **Start with `--skip-details`** to get ASINs first, then fetch details later
2. **Use cached categories** - the script automatically uses `category_utils.py` (no tokens)
3. **Adjust filters gradually** - start broad, then narrow down
4. **Monitor token usage** - the script shows tokens before and after

## Troubleshooting

**No products found:**
- Try widening your filters (increase BSR max, decrease sales min, etc.)
- Check if the category ID is correct
- Try removing some filters

**Token errors:**
- Use `--skip-details` to save tokens
- Reduce `--max-results`
- Wait for tokens to refill

**Category not found:**
- Run `python fetch_all_categories.py` to build category cache
- Or use `find_category.py` to search for categories


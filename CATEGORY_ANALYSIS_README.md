# Category Structure Analysis Guide

This guide explains how to understand and analyze your fetched Amazon categories.

## Understanding Category Types

Based on [Keepa's documentation](https://keepa.com/#!discuss/t/best-sellers/1298), Amazon categories are organized in three levels:

### 1. 🌳 Root Categories
- Top-level categories (e.g., "Electronics", "Home & Kitchen")
- No parent category
- Can contain up to 100,000 ASINs in best sellers lists
- Token cost: ~15 tokens for best sellers query

### 2. 📦 Product Groups
- Mid-level categories that group related sub-categories
- Have both a parent (root category) and children (sub-categories)
- Used to organize products hierarchically
- Can contain multiple sub-categories

### 3. 📁 Sub-categories
- Bottom-level categories with actual products
- Have a parent but no children
- Can contain up to 3,000 ASINs in best sellers lists
- Token cost: ~5-10 tokens for best sellers query
- **Recommended for product searches** (more efficient)

## Running the Analysis

```bash
python analyze_categories.py
```

This will generate:
1. **Text Tree** (`data/category_tree.txt`) - Console-friendly tree structure
2. **HTML Tree** (`data/category_tree.html`) - Interactive web visualization
3. **Analysis Data** (`data/category_analysis.json`) - Detailed statistics

## Understanding the Output

### Tree Structure Example:
```
🌳 Root Category: Electronics (ID: 172282)
    📦 Product Group: Computers & Accessories (ID: 541966)
        📁 Sub-category: Laptops (ID: 565108)
        📁 Sub-category: Desktops (ID: 138966)
```

### Category Information:
- **Category ID**: Unique identifier for the category
- **Product Count**: Number of products in this category (if available)
- **Depth**: How many levels deep in the hierarchy (0 = root)
- **Children**: Sub-categories under this category

## Best Practices

### For Product Searches:
1. **Use Sub-categories** instead of Root Categories
   - More efficient (5-10 tokens vs 15 tokens)
   - More targeted results (up to 3,000 ASINs vs 100,000)
   - Better for filtering

2. **Check Product Count**
   - Categories with higher product counts may have more variety
   - Use this to prioritize which categories to search

3. **Understand Hierarchy**
   - Start with Root → Find Product Group → Use Sub-category
   - Example: Electronics → Computers → Laptops

## Token Efficiency

| Category Type | Best Sellers Query | Max ASINs | Token Cost |
|---------------|-------------------|-----------|------------|
| Root Category | Up to 100,000 | 100,000 | ~15 tokens |
| Product Group | Varies | Varies | ~10-15 tokens |
| Sub-category | Up to 3,000 | 3,000 | ~5-10 tokens |

**Recommendation**: Use Sub-categories for most searches to save tokens!

## Using the Analysis

### Find Categories:
```python
from category_utils import search_categories, get_category_by_id

# Search for categories
categories = search_categories("Electronics")

# Get category details
category = get_category_by_id(20)
print(f"Name: {category['name']}")
print(f"Children: {category['children_ids']}")
```

### Navigate Hierarchy:
1. Open `data/category_tree.html` in your browser
2. Browse the tree structure visually
3. Find the sub-category you need
4. Use its ID in your product search scripts

## Files Generated

- `category_tree.txt` - Text-based tree (easy to read in terminal)
- `category_tree.html` - Interactive HTML visualization (open in browser)
- `category_analysis.json` - Complete analysis data (for programmatic use)

## Tips

1. **Start Broad**: Use root categories to explore
2. **Narrow Down**: Use product groups to find related categories
3. **Get Specific**: Use sub-categories for actual product searches
4. **Save Tokens**: Always prefer sub-categories over root categories


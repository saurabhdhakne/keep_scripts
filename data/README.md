# Category Data Cache

This directory stores cached Amazon category data fetched from the Keepa API.

## Files

- `amazon_categories.json` - Complete category data in JSON format
- `amazon_categories.csv` - Category data in CSV format for easy viewing/editing

## Setup

1. **First Time Setup (One-time token cost):**
   ```bash
   python fetch_all_categories.py
   ```
   This will consume approximately 100-500 tokens to fetch all categories.

2. **After Setup:**
   Use `category_utils.py` to read from cached data without consuming any tokens:
   ```python
   from category_utils import get_category_by_id, search_categories
   
   # Get category by ID (no API call)
   category = get_category_by_id(20)
   
   # Search categories (no API call)
   results = search_categories("Electronics")
   ```

## Benefits

- ✅ **No token consumption** after initial fetch
- ✅ **Fast lookups** from local files
- ✅ **Offline access** to category data
- ✅ **Easy searching** and filtering

## Updating the Cache

Categories don't change frequently, but you can update the cache by running:
```bash
python fetch_all_categories.py
```

## Usage Examples

See `category_utils.py` for all available functions:
- `get_category_by_id(category_id)` - Get category by ID
- `search_categories(search_term)` - Search by name
- `get_categories_by_parent(parent_id)` - Get subcategories
- `get_root_categories()` - Get all root categories
- `get_category_statistics()` - Get cache statistics


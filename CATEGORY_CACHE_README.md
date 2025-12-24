# Category Cache System

This system allows you to fetch all Amazon categories **once** and then use them **without consuming any API tokens**.

## How It Works

1. **One-Time Setup** (consumes ~50-200 tokens):
   - Run `fetch_all_categories.py` to fetch all categories from Keepa API
   - Categories are saved to `data/amazon_categories.json` and `.csv`
   
2. **Daily Usage** (0 tokens):
   - Use `category_utils.py` to read from cached files
   - No API calls = No token consumption!

## Quick Start

### Step 1: Fetch Categories (One-Time)

```bash
python fetch_all_categories.py
```

**Expected Output:**
- Fetches categories using search terms
- Saves to `data/amazon_categories.json`
- Saves to `data/amazon_categories.csv`
- Token cost: ~50-200 tokens (one-time)

### Step 2: Use Cached Categories (No Tokens!)

```python
from category_utils import get_category_by_id, search_categories

# Get category by ID - NO API CALL!
category = get_category_by_id(20)
print(category['name'])

# Search categories - NO API CALL!
results = search_categories("Electronics")
for cat in results:
    print(f"{cat['category_id']}: {cat['name']}")
```

## Available Functions

All functions in `category_utils.py` work **without API tokens**:

| Function | Description | Example |
|----------|-------------|---------|
| `get_category_by_id(id)` | Get category by ID | `get_category_by_id(20)` |
| `search_categories(term)` | Search by name | `search_categories("Electronics")` |
| `get_all_categories()` | Get all categories | `get_all_categories()` |
| `get_categories_by_parent(id)` | Get subcategories | `get_categories_by_parent(20)` |
| `get_root_categories()` | Get root categories | `get_root_categories()` |
| `get_category_statistics()` | Get cache stats | `get_category_statistics()` |
| `print_category_info(id)` | Print category details | `print_category_info(20)` |

## File Structure

```
keep_scripts/
├── fetch_all_categories.py      # One-time fetch script
├── category_utils.py            # Utility functions (no tokens!)
├── data/
│   ├── amazon_categories.json   # Category data (JSON)
│   ├── amazon_categories.csv   # Category data (CSV)
│   └── README.md                # Data directory info
└── examples/
    └── use_cached_categories.py # Usage example
```

## Category Data Structure

Each category contains:
- `category_id`: Unique category ID
- `name`: Category name
- `parent_id`: Parent category ID (None for root)
- `domain`: Amazon domain (1 = US)
- `product_count`: Number of products in category
- `children_count`: Number of subcategories
- `children_ids`: List of subcategory IDs
- `depth`: Depth in category tree

## Benefits

✅ **Zero token cost** after initial fetch  
✅ **Fast lookups** from local files  
✅ **Offline access** to category data  
✅ **Easy searching** and filtering  
✅ **No API rate limits**  

## Updating the Cache

Categories rarely change, but you can update:
```bash
python fetch_all_categories.py
```

## Example: Replace API Calls

### Before (Consumes Tokens):
```python
import keepa
api = keepa.Keepa(API_KEY)
categories = api.search_for_categories("Electronics")  # 1-2 tokens
```

### After (No Tokens):
```python
from category_utils import search_categories
categories = search_categories("Electronics")  # 0 tokens!
```

## Integration with Existing Scripts

Update your scripts to use cached categories:

```python
# Old way (fetch_product_list.py)
CATEGORY_ID = 20  # Hard-coded

# New way (use cached lookup)
from category_utils import search_categories
results = search_categories("Electronics")
CATEGORY_ID = results[0]['category_id']  # Get ID from cache
```

## Troubleshooting

**Error: "Category file not found"**
- Run `fetch_all_categories.py` first to create the cache

**Categories seem outdated**
- Run `fetch_all_categories.py` again to update

**Want to use CSV instead of JSON**
- Pass `use_csv=True` to any function:
  ```python
  categories = get_all_categories(use_csv=True)
  ```

## Token Savings

- **Before**: Every category search = 1-2 tokens
- **After**: Every category search = 0 tokens
- **Savings**: 100% after initial setup!

If you search categories 100 times:
- **Before**: 100-200 tokens
- **After**: 0 tokens (after initial ~50-200 token investment)


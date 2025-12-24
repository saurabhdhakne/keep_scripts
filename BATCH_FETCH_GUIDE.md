# Batch Fetch Guide - Fetch Categories with Limited Tokens

This guide explains how to fetch all categories in batches when you have limited tokens.

## Quick Start

### First Run (with 60 tokens)
```bash
python fetch_all_categories.py --batch-size 5 --min-tokens 5
```

This will:
- Fetch categories in small batches of 5
- Stop when tokens drop below 5
- Save progress automatically
- Resume from where it left off next time

### Resume Later (when tokens refill)
```bash
python fetch_all_categories.py
```

The script automatically resumes from the last checkpoint!

## Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--batch-size N` | 10 | Number of categories to fetch per batch |
| `--min-tokens N` | 5 | Minimum tokens required to continue |
| `--resume` | True | Resume from last checkpoint (default) |
| `--reset` | False | Reset progress and start fresh |

## Examples

### Example 1: Small batches for limited tokens
```bash
# Start with 60 tokens, fetch 5 at a time, stop at 5 tokens
python fetch_all_categories.py --batch-size 5 --min-tokens 5
```

### Example 2: Resume when tokens refill
```bash
# Just run again - it automatically resumes!
python fetch_all_categories.py
```

### Example 3: Larger batches when you have more tokens
```bash
# Fetch 20 at a time, stop at 10 tokens
python fetch_all_categories.py --batch-size 20 --min-tokens 10
```

### Example 4: Start fresh (reset progress)
```bash
# Reset and start over
python fetch_all_categories.py --reset
```

## How It Works

1. **Progress Tracking**: 
   - Saves fetched category IDs to `data/fetch_progress.json`
   - Tracks which search terms are completed
   - Never fetches the same category twice

2. **Batch Processing**:
   - Fetches categories in small batches
   - Checks token balance before each batch
   - Stops automatically when tokens are low

3. **Resume Capability**:
   - Automatically continues from last checkpoint
   - Skips already-fetched categories
   - Appends new categories to existing files

## Progress Files

- `data/fetch_progress.json` - Tracks which categories are fetched
- `data/amazon_categories.json` - All fetched categories (JSON)
- `data/amazon_categories.csv` - All fetched categories (CSV)

## Token Usage

### Phase 1: Search (1-2 tokens per search term)
- Searches 29 common keywords
- Finds unique category IDs
- Cost: ~30-60 tokens total

### Phase 2: Fetch Details (1-2 tokens per category)
- Fetches detailed info for each category
- Done in batches
- Cost: 1-2 tokens per category

### Total Estimated Cost
- Small run (10 categories): ~40-50 tokens
- Medium run (50 categories): ~80-110 tokens  
- Full run (all categories): ~200-500 tokens

## Tips

1. **Start Small**: Use `--batch-size 5` when you have limited tokens
2. **Monitor Progress**: Check `data/fetch_progress.json` to see what's done
3. **Resume Often**: Run the script multiple times as tokens refill
4. **Check Status**: The script shows how many categories are already fetched

## Example Output

```
============================================================
Fetching Amazon Categories (Batch Mode with Resume)
============================================================

Initial tokens: 60
Batch size: 5
Min tokens to continue: 5

📊 Resume mode: Found 15 already fetched categories
   Search terms completed: 5
   Last updated: 2024-12-20T14:30:00

📁 Existing categories in cache: 15

============================================================
Starting batch fetch...
============================================================

STEP 1: Searching for categories with keywords
  [1/24] Searching: Electronics (Tokens: 60)
    ✓ Found 3 new categories
  [2/24] Searching: Books (Tokens: 59)
    ✓ Found 2 new categories
  ...

STEP 2: Fetching detailed information (batch mode)
Found 25 new categories to fetch details for
Batch size: 5, Min tokens: 5
  Batch 1: Processed 5/25 categories (Tokens left: 50)
  Batch 2: Processed 10/25 categories (Tokens left: 40)
  ...

⚠️  Low tokens (4). Stopping batch processing.
   Progress: 20/25 categories processed
   Progress saved. Resume later to continue from category 12345.

============================================================
Batch Complete!
============================================================
New categories fetched in this run: 20
Total categories fetched so far: 35
Tokens used in this run: 56
Tokens remaining: 4

✅ Success! Categories saved to:
   - data/amazon_categories.json
   - data/amazon_categories.csv
   - Progress: data/fetch_progress.json

⚠️  Low tokens (4). Run again later to continue.
   Progress saved. Use: python fetch_all_categories.py --resume
```

## Troubleshooting

**Q: Script says "Not enough tokens"**
- Wait for tokens to refill (they generate continuously)
- Lower `--min-tokens` value (e.g., `--min-tokens 3`)

**Q: Want to see what's already fetched**
- Check `data/fetch_progress.json`
- Or use `category_utils.py` to read the cache

**Q: Categories seem incomplete**
- Run the script again - it will continue fetching
- Check progress file to see what's done

**Q: Want to start over**
- Use `--reset` flag to clear progress
- Or delete `data/fetch_progress.json`


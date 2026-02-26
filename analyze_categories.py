"""
Category Structure Analyzer
Analyzes fetched categories and creates a tree structure visualization.
Shows Root Categories, Sub-categories, and Product Groups with important details.
"""

import json
import os
from collections import defaultdict
from typing import Dict, List, Optional

# Input file
CATEGORIES_FILE = "data/amazon_categories.json"
OUTPUT_TREE_FILE = "data/category_tree.txt"
OUTPUT_HTML_FILE = "data/category_tree.html"
OUTPUT_ANALYSIS_FILE = "data/category_analysis.json"

def load_categories():
    """Load categories from JSON file."""
    if not os.path.exists(CATEGORIES_FILE):
        print(f"❌ Category file not found: {CATEGORIES_FILE}")
        print("   Please run fetch_all_categories.py first.")
        return []
    
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('categories', [])

def normalize_category_data(categories):
    """Normalize category data structure."""
    normalized = {}
    
    for cat in categories:
        cat_id = cat.get('category_id')
        if not cat_id:
            continue
        
        # Extract name (handle both string and dict formats)
        name = cat.get('name')
        if isinstance(name, dict):
            # Try multiple possible name fields
            name = (name.get('name') or 
                   name.get('contextFreeName') or 
                   name.get('catId') or 
                   f'Category {cat_id}')
        elif not isinstance(name, str):
            name = f'Category {cat_id}'
        
        # Extract parent_id - check both direct field and name dict
        parent_id = cat.get('parent_id')
        if not parent_id and isinstance(cat.get('name'), dict):
            parent_id = cat.get('name', {}).get('parent')
        
        # Extract children_ids - check both direct field and name dict
        children_ids = cat.get('children_ids', [])
        if not children_ids and isinstance(cat.get('name'), dict):
            children_from_dict = cat.get('name', {}).get('children')
            if children_from_dict:
                if isinstance(children_from_dict, list):
                    children_ids = children_from_dict
                else:
                    children_ids = [children_from_dict]
        
        # Extract product_count
        product_count = cat.get('product_count', 0)
        if not product_count and isinstance(cat.get('name'), dict):
            product_count = cat.get('name', {}).get('productCount', 0)
        
        depth = cat.get('depth', 0)
        
        # Get additional info from name dict if available
        is_browse_node = False
        if isinstance(cat.get('name'), dict):
            name_dict = cat.get('name')
            is_browse_node = name_dict.get('isBrowseNode', False)
        
        normalized[cat_id] = {
            'category_id': cat_id,
            'name': name,
            'parent_id': parent_id,
            'children_ids': children_ids if isinstance(children_ids, list) else [],
            'product_count': int(product_count) if product_count else 0,
            'depth': depth,
            'is_browse_node': is_browse_node
        }
    
    return normalized

def build_category_tree(categories):
    """Build category tree structure."""
    # Create category lookup
    cat_dict = {cat['category_id']: cat for cat in categories.values()}
    
    # Find root categories (no parent or parent not in our data)
    root_categories = []
    children_map = defaultdict(list)
    processed = set()
    
    for cat_id, cat in categories.items():
        parent_id = cat.get('parent_id')
        if not parent_id or parent_id not in cat_dict:
            # This is a root category
            if cat_id not in processed:
                root_categories.append(cat_id)
                processed.add(cat_id)
        else:
            # This has a parent, add to children map
            children_map[parent_id].append(cat_id)
    
    # Build tree structure
    def build_node(cat_id, level=0, visited=None):
        """Recursively build tree node."""
        if visited is None:
            visited = set()
        
        if cat_id in visited:
            return None  # Avoid cycles
        
        visited.add(cat_id)
        cat = categories.get(cat_id)
        if not cat:
            return None
        
        node = {
            'category_id': cat_id,
            'name': cat['name'],
            'product_count': cat['product_count'],
            'depth': level,
            'is_browse_node': cat.get('is_browse_node', False),
            'children': []
        }
        
        # Add children
        children_ids = cat.get('children_ids', [])
        # Also check children_map for any children we know about
        all_children = list(set(children_ids + children_map.get(cat_id, [])))
        
        for child_id in all_children:
            if child_id in categories and child_id not in visited:
                child_node = build_node(child_id, level + 1, visited)
                if child_node:
                    node['children'].append(child_node)
        
        return node
    
    # Build tree starting from roots
    tree = []
    for root_id in root_categories:
        node = build_node(root_id, 0)
        if node:
            tree.append(node)
    
    return tree, cat_dict

def classify_category_type(cat, cat_dict):
    """Classify category as Root, Sub-category, or Product Group."""
    parent_id = cat.get('parent_id')
    children_ids = cat.get('children_ids', [])
    has_children = len(children_ids) > 0
    
    # Root Category: No parent or parent not in our data
    if not parent_id or parent_id not in cat_dict:
        return "Root Category"
    
    # Product Group: Has children (sub-categories)
    if has_children:
        return "Product Group"
    
    # Sub-category: Has parent but no children
    return "Sub-category"

def analyze_categories(categories):
    """Analyze category structure and generate statistics."""
    cat_dict = normalize_category_data(categories)
    tree, full_cat_dict = build_category_tree(cat_dict)
    
    # Statistics
    stats = {
        'total_categories': len(cat_dict),
        'root_categories': 0,
        'sub_categories': 0,
        'product_groups': 0,
        'categories_with_products': 0,
        'total_products': 0,
        'max_depth': 0,
        'category_types': {}
    }
    
    # Analyze each category
    for cat_id, cat in cat_dict.items():
        cat_type = classify_category_type(cat, cat_dict)
        stats['category_types'][cat_id] = cat_type
        
        if cat_type == "Root Category":
            stats['root_categories'] += 1
        elif cat_type == "Sub-category":
            stats['sub_categories'] += 1
        elif cat_type == "Product Group":
            stats['product_groups'] += 1
        
        if cat.get('product_count', 0) > 0:
            stats['categories_with_products'] += 1
            stats['total_products'] += cat['product_count']
        
        if cat.get('depth', 0) > stats['max_depth']:
            stats['max_depth'] = cat.get('depth', 0)
    
    return tree, cat_dict, stats

def print_tree_text(tree, output_file=None):
    """Print tree structure as text."""
    lines = []
    
    def print_node(node, prefix="", is_last=True):
        """Recursively print tree node."""
        # Current node
        connector = "└── " if is_last else "├── "
        name = node['name']
        cat_id = node['category_id']
        product_count = node.get('product_count', 0)
        depth = node.get('depth', 0)
        
        # Determine category type
        has_children = len(node.get('children', [])) > 0
        if depth == 0:
            cat_type = "🌳 Root"
        elif has_children:
            cat_type = "📦 Group"
        else:
            cat_type = "📁 Sub"
        
        line = f"{prefix}{connector}[{cat_type}] {name} (ID: {cat_id})"
        if product_count > 0:
            line += f" | Products: {product_count:,}"
        lines.append(line)
        
        # Children
        children = node.get('children', [])
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            extension = "    " if is_last else "│   "
            print_node(child, prefix + extension, is_last_child)
    
    # Print header
    lines.append("=" * 80)
    lines.append("AMAZON CATEGORY TREE STRUCTURE")
    lines.append("=" * 80)
    lines.append("Legend: 🌳 Root Category | 📦 Product Group | 📁 Sub-category")
    lines.append("")
    
    # Print tree
    for i, root in enumerate(tree):
        print_node(root, "", i == len(tree) - 1)
        if i < len(tree) - 1:
            lines.append("")
    
    # Print to console and file
    output = "\n".join(lines)
    print(output)
    
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n✅ Tree saved to: {output_file}")
    
    return output

def create_html_tree(tree, stats, output_file):
    """Create HTML visualization of category tree."""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Amazon Category Tree</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .stats {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .stats h2 {
            margin-top: 0;
            color: #2e7d32;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }
        .stat-item {
            background: white;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #4CAF50;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        }
        .tree {
            margin: 20px 0;
        }
        .node {
            margin: 5px 0;
            padding: 8px;
            border-left: 3px solid #ddd;
            background: #fafafa;
        }
        .node.root {
            border-left-color: #4CAF50;
            background: #e8f5e9;
            font-weight: bold;
        }
        .node.group {
            border-left-color: #2196F3;
            background: #e3f2fd;
        }
        .node.sub {
            border-left-color: #FF9800;
            background: #fff3e0;
        }
        .node-name {
            font-weight: 500;
            color: #333;
        }
        .node-id {
            color: #666;
            font-size: 0.9em;
        }
        .node-products {
            color: #4CAF50;
            font-weight: bold;
        }
        .children {
            margin-left: 30px;
        }
        .legend {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .legend-item {
            display: inline-block;
            margin-right: 20px;
            padding: 5px 10px;
            border-radius: 3px;
        }
        .legend-root { background: #e8f5e9; border-left: 3px solid #4CAF50; }
        .legend-group { background: #e3f2fd; border-left: 3px solid #2196F3; }
        .legend-sub { background: #fff3e0; border-left: 3px solid #FF9800; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌳 Amazon Category Tree Structure</h1>
        
        <div class="stats">
            <h2>📊 Statistics</h2>
            <div class="stats-grid">
"""
    
    # Add statistics
    html += f"""
                <div class="stat-item">
                    <div class="stat-label">Total Categories</div>
                    <div class="stat-value">{stats['total_categories']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Root Categories</div>
                    <div class="stat-value">{stats['root_categories']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Product Groups</div>
                    <div class="stat-value">{stats['product_groups']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Sub-categories</div>
                    <div class="stat-value">{stats['sub_categories']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Categories with Products</div>
                    <div class="stat-value">{stats['categories_with_products']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Total Products</div>
                    <div class="stat-value">{stats['total_products']:,}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Max Depth</div>
                    <div class="stat-value">{stats['max_depth']}</div>
                </div>
            </div>
        </div>
        
        <div class="legend">
            <strong>Legend:</strong>
            <span class="legend-item legend-root">🌳 Root Category</span>
            <span class="legend-item legend-group">📦 Product Group</span>
            <span class="legend-item legend-sub">📁 Sub-category</span>
        </div>
        
        <div class="tree">
            <h2>Category Tree</h2>
"""
    
    # Add tree nodes
    def add_node_html(node, level=0):
        cat_type = "root" if level == 0 else ("group" if node.get('children') else "sub")
        name = node['name']
        cat_id = node['category_id']
        product_count = node.get('product_count', 0)
        
        html_node = f'<div class="node {cat_type}">'
        html_node += f'<span class="node-name">{name}</span> '
        html_node += f'<span class="node-id">(ID: {cat_id})</span>'
        if product_count > 0:
            html_node += f' <span class="node-products">| Products: {product_count:,}</span>'
        html_node += '</div>'
        
        children_html = ""
        if node.get('children'):
            children_html = '<div class="children">'
            for child in node['children']:
                children_html += add_node_html(child, level + 1)
            children_html += '</div>'
        
        return html_node + children_html
    
    for root in tree:
        html += add_node_html(root, 0)
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML tree saved to: {output_file}")

def print_detailed_analysis(cat_dict, stats):
    """Print detailed category analysis."""
    print("\n" + "=" * 80)
    print("DETAILED CATEGORY ANALYSIS")
    print("=" * 80)
    
    print(f"\n📊 Overall Statistics:")
    print(f"   Total Categories: {stats['total_categories']}")
    print(f"   Root Categories: {stats['root_categories']}")
    print(f"   Product Groups: {stats['product_groups']}")
    print(f"   Sub-categories: {stats['sub_categories']}")
    print(f"   Categories with Products: {stats['categories_with_products']}")
    print(f"   Total Products: {stats['total_products']:,}")
    print(f"   Maximum Depth: {stats['max_depth']}")
    
    # Group by type
    print(f"\n📦 Categories by Type:")
    root_cats = [cat_id for cat_id, cat_type in stats['category_types'].items() if cat_type == "Root Category"]
    group_cats = [cat_id for cat_id, cat_type in stats['category_types'].items() if cat_type == "Product Group"]
    sub_cats = [cat_id for cat_id, cat_type in stats['category_types'].items() if cat_type == "Sub-category"]
    
    print(f"\n   🌳 Root Categories ({len(root_cats)}):")
    for cat_id in root_cats[:10]:
        cat = cat_dict.get(cat_id)
        if cat:
            print(f"      - [{cat_id}] {cat['name']}")
    if len(root_cats) > 10:
        print(f"      ... and {len(root_cats) - 10} more")
    
    print(f"\n   📦 Product Groups ({len(group_cats)}):")
    for cat_id in group_cats[:10]:
        cat = cat_dict.get(cat_id)
        if cat:
            children_count = len(cat.get('children_ids', []))
            print(f"      - [{cat_id}] {cat['name']} ({children_count} sub-categories)")
    if len(group_cats) > 10:
        print(f"      ... and {len(group_cats) - 10} more")
    
    print(f"\n   📁 Sub-categories ({len(sub_cats)}):")
    for cat_id in sub_cats[:10]:
        cat = cat_dict.get(cat_id)
        if cat:
            print(f"      - [{cat_id}] {cat['name']}")
    if len(sub_cats) > 10:
        print(f"      ... and {len(sub_cats) - 10} more")
    
    # Categories with most products
    print(f"\n🏆 Top Categories by Product Count:")
    sorted_cats = sorted(cat_dict.values(), key=lambda x: x.get('product_count', 0), reverse=True)
    for i, cat in enumerate(sorted_cats[:10], 1):
        if cat.get('product_count', 0) > 0:
            cat_type = stats['category_types'].get(cat['category_id'], 'Unknown')
            print(f"   {i}. [{cat['category_id']}] {cat['name']}")
            print(f"      Type: {cat_type} | Products: {cat['product_count']:,}")

def main():
    """Main function."""
    print("=" * 80)
    print("CATEGORY STRUCTURE ANALYZER")
    print("=" * 80)
    
    # Load categories
    print("\n📂 Loading categories...")
    categories = load_categories()
    
    if not categories:
        return
    
    print(f"✓ Loaded {len(categories)} categories")
    
    # Analyze
    print("\n🔍 Analyzing category structure...")
    tree, cat_dict, stats = analyze_categories(categories)
    
    # Print tree
    print("\n" + "=" * 80)
    print("CATEGORY TREE")
    print("=" * 80)
    print_tree_text(tree, OUTPUT_TREE_FILE)
    
    # Print detailed analysis
    print_detailed_analysis(cat_dict, stats)
    
    # Create HTML visualization
    print("\n🌐 Creating HTML visualization...")
    create_html_tree(tree, stats, OUTPUT_HTML_FILE)
    
    # Save analysis data
    analysis_data = {
        'statistics': stats,
        'category_types': stats['category_types'],
        'tree_structure': tree
    }
    
    os.makedirs(os.path.dirname(OUTPUT_ANALYSIS_FILE), exist_ok=True)
    with open(OUTPUT_ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Analysis data saved to: {OUTPUT_ANALYSIS_FILE}")
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nGenerated files:")
    print(f"   📄 Text tree: {OUTPUT_TREE_FILE}")
    print(f"   🌐 HTML tree: {OUTPUT_HTML_FILE}")
    print(f"   📊 Analysis: {OUTPUT_ANALYSIS_FILE}")
    print(f"\n💡 Open {OUTPUT_HTML_FILE} in a browser for interactive visualization!")

if __name__ == "__main__":
    main()


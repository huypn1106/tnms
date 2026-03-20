import os
import re

DOCS_DIR = 'docs'
CATEGORIES = ['guides', 'references']

VIEWER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <title>{title} — tnms</title>
    <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../assets/style.css">
    <script src="../assets/main.js"></script>
    <style>
        .doc-iframe-container {{
            margin-top: 2rem;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
            background: #ffffff;
        }}
        .doc-iframe {{
            width: 100%;
            height: 75vh;
            border: none;
            display: block;
        }}
    </style>
</head>

<body>

    <header class="site-header">
        <a href="/" class="logo"><span>&gt;</span> tnms</a>
        <button class="theme-toggle" aria-label="Toggle theme"></button>
    </header>

    <main class="doc-container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="/">tnms</a> <span class="sep">/</span> <a href="./">{category}</a> <span class="sep">/</span>
            <span>{basename_no_ext}</span>
        </nav>

        <h1>{title}</h1>
        
        <div class="doc-iframe-container">
            <iframe src="{raw_html_file}" class="doc-iframe" title="{title}"></iframe>
        </div>

        <hr>

        <p><a href="./">&larr; Back to {category_name}</a></p>
    </main>

    <footer class="site-footer">
        tnms
    </footer>

</body>

</html>"""

LINK_TEMPLATE = """
            <li>
                <a href="{viewer_file}">
                    <span class="doc-icon">📄</span>
                    <div>
                        <div class="doc-title">{title}</div>
                        <div class="doc-desc">{desc}</div>
                    </div>
                </a>
            </li>
"""

def extract_title(html_content, default_title):
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r'<h1.*?>(.*?)</h1>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return default_title

def process_category(category):
    category_path = os.path.join(DOCS_DIR, category)
    if not os.path.exists(category_path):
        return

    index_path = os.path.join(category_path, 'index.html')
    if not os.path.exists(index_path):
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()

    files = [f for f in os.listdir(category_path) if f.endswith('.html') and f != 'index.html']
    added_links = 0

    for filename in files:
        file_path = os.path.join(category_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # If it already has the app frame, it's either manually written or it's a viewer
        if 'class="site-header"' in content:
            continue

        raw_basename = os.path.splitext(filename)[0]
        viewer_filename = f"{raw_basename}-viewer.html"
        viewer_path = os.path.join(category_path, viewer_filename)

        title = extract_title(content, raw_basename.replace('-', ' ').title())
        desc = f"Imported document: {title}"

        # 1. Create viewer if it doesn't exist
        if not os.path.exists(viewer_path):
            print(f"[{category}] Creating viewer for: {filename} -> {viewer_filename}")
            viewer_html = VIEWER_TEMPLATE.format(
                desc=desc,
                title=title,
                category=category,
                basename_no_ext=raw_basename,
                raw_html_file=filename,
                category_name=category.capitalize()
            )
            with open(viewer_path, 'w', encoding='utf-8') as f:
                f.write(viewer_html)

        # 2. Check if the viewer is linked in index.html
        if f'href="{viewer_filename}"' not in index_html and f"href='{viewer_filename}'" not in index_html:
            print(f"[{category}] Adding link to index.html for: {viewer_filename}")
            link_html = LINK_TEMPLATE.format(viewer_file=viewer_filename, title=title, desc=desc)
            
            # Insert before the closing </ul> tag
            index_html = index_html.replace('</ul>', f'{link_html}        </ul>', 1)
            added_links += 1

    if added_links > 0:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"[{category}] Updated index.html with {added_links} new links.")

def main():
    print("Scanning for new documents...")
    for category in CATEGORIES:
        process_category(category)
    print("Done!")

if __name__ == "__main__":
    main()

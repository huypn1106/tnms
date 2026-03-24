import os
import re

DOCS_DIR = 'docs'

VIEWER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <title>{title} — tnms</title>
    <link rel="icon" type="image/svg+xml" href="{assets_rel}favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{assets_rel}style.css">
    <script src="{assets_rel}main.js"></script>
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

    <main class="doc-container viewer-wide">
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="/">tnms</a> {breadcrumb_html} <span class="sep">/</span>
            <span>{basename_no_ext}</span>
        </nav>

        <h1>{title}</h1>

        <div class="doc-viewer-toolbar">
            <button class="btn-fullscreen" id="btn-fullscreen" aria-label="View fullscreen">
                <svg viewBox="0 0 24 24"><path d="M3 3h7v2H5v5H3V3zm11 0h7v7h-2V5h-5V3zM3 14h2v5h5v2H3v-7zm18 0v7h-7v-2h5v-5h2z"/></svg>
                Fullscreen
            </button>
        </div>

        <div class="doc-iframe-container">
            <iframe src="{raw_html_file}" class="doc-iframe" id="doc-iframe" title="{title}"></iframe>
        </div>

        <hr>

        <p><a href="./">&larr; Back</a></p>
    </main>

    <footer class="site-footer">
        tnms
    </footer>

    <script>
        (function () {{
            'use strict';
            var btnFullscreen = document.getElementById('btn-fullscreen');
            var docIframe = document.getElementById('doc-iframe');
            var docTitle = document.querySelector('h1').textContent;

            function openFullscreen() {{
                var overlay = document.createElement('div');
                overlay.className = 'doc-fullscreen-overlay';
                overlay.id = 'fullscreen-overlay';
                overlay.innerHTML =
                    '<div class="fullscreen-topbar">' +
                    '  <span class="fullscreen-title">' + docTitle + '</span>' +
                    '  <button class="btn-exit-fullscreen" id="btn-exit-fullscreen" aria-label="Exit fullscreen">' +
                    '    <svg viewBox="0 0 24 24"><path d="M9 3v3H5v2h6V3H9zm6 0v5h6V6h-4V3h-2zM5 15v2h4v3h2v-5H5zm10 0v5h2v-3h4v-2h-6z"/></svg>' +
                    '    Exit' +
                    '  </button>' +
                    '</div>' +
                    '<iframe src="' + docIframe.src + '" class="fullscreen-iframe" title="' + docTitle + '"></iframe>';
                document.body.appendChild(overlay);
                document.body.style.overflow = 'hidden';
                overlay.querySelector('#btn-exit-fullscreen').addEventListener('click', closeFullscreen);
            }}

            function closeFullscreen() {{
                var overlay = document.getElementById('fullscreen-overlay');
                if (overlay) {{
                    overlay.remove();
                    document.body.style.overflow = '';
                }}
            }}

            btnFullscreen.addEventListener('click', openFullscreen);
            document.addEventListener('keydown', function (e) {{
                if (e.key === 'Escape') closeFullscreen();
            }});
        }})();
    </script>

</body>

</html>"""

CATEGORY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <title>{title} — tnms</title>
    <link rel="icon" type="image/svg+xml" href="{assets_rel}favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{assets_rel}style.css">
    <script src="{assets_rel}main.js"></script>
</head>

<body>

    <header class="site-header">
        <a href="/" class="logo"><span>&gt;</span> tnms</a>
        <button class="theme-toggle" aria-label="Toggle theme"></button>
    </header>

    <main class="doc-container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="/">tnms</a> {breadcrumb_html}
        </nav>

        <h1>{title}</h1>
        <p>{desc}</p>

        <ul class="doc-list">
        </ul>
    </main>

    <footer class="site-footer">
        tnms
    </footer>

</body>

</html>"""

LINK_TEMPLATE = """
            <li>
                <a href="{href}">
                    <span class="doc-icon">{icon}</span>
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
        return match.group(1).strip().replace(" — tnms", "")
    match = re.search(r'<h1.*?>(.*?)</h1>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return default_title

def clean_title(title):
    return title.replace('-', ' ').replace('_', ' ').title()

def get_rel_path(depth):
    return "../" * depth

def build_breadcrumb(parts, extra_level=False):
    html = ""
    for i, part in enumerate(parts):
        html += '<span class="sep">/</span> '
        if i == len(parts) - 1 and not extra_level:
            html += f'<span>{clean_title(part)}</span> '
        else:
            up = "../" * (len(parts) - 1 - i) if not extra_level else "./" if i == len(parts) - 1 else "../" * (len(parts) - 1 - i)
            html += f'<a href="{up}">{clean_title(part)}</a> '
    return html.strip()

def process_directory(current_dir):
    rel_dir = os.path.relpath(current_dir, DOCS_DIR)
    # Correct handling for Windows paths
    parts = rel_dir.replace('\\', '/').split('/')
    depth = len(parts)

    index_path = os.path.join(current_dir, 'index.html')
    
    # 1. Ensure index.html exists
    if not os.path.exists(index_path):
        print(f"[{rel_dir}] Creating index.html")
        cat_name = clean_title(parts[-1])
        cat_desc = f"Documents and folders in {cat_name}"
        html = CATEGORY_TEMPLATE.format(
            title=cat_name,
            desc=cat_desc,
            assets_rel=get_rel_path(depth) + 'assets/',
            breadcrumb_html=build_breadcrumb(parts)
        )
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)

    # read current index.html
    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()

    # Process subdirectories to add them to index.html if not present
    subdirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    added_links = 0

    for subdir in subdirs:
        href = subdir + "/"
        if f'href="{href}"' not in index_html and f"href='{href}'" not in index_html:
            subdir_title = clean_title(subdir)
            link_html = LINK_TEMPLATE.format(href=href, icon="📁", title=subdir_title, desc=f"Category: {subdir_title}")
            index_html = index_html.replace('</ul>', f'{link_html}        </ul>', 1)
            added_links += 1

    # Process HTML files
    files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    for filename in files:
        if not filename.endswith('.html') or filename == 'index.html':
            continue

        file_path = os.path.join(current_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if it's already framed
        if 'class="site-header"' in content:
            if f'href="{filename}"' not in index_html and f"href='{filename}'" not in index_html:
                title = extract_title(content, clean_title(os.path.splitext(filename)[0]))
                link_html = LINK_TEMPLATE.format(href=filename, icon="📄", title=title, desc="Document")
                index_html = index_html.replace('</ul>', f'{link_html}        </ul>', 1)
                added_links += 1
            continue

        raw_basename = os.path.splitext(filename)[0]
        viewer_filename = f"{raw_basename}-viewer.html"
        viewer_path = os.path.join(current_dir, viewer_filename)
        title = extract_title(content, clean_title(raw_basename))
        desc = f"Imported document: {title}"

        # Create/update viewer (always regenerate to keep in sync with template)
        print(f"[{rel_dir}] Generating viewer for: {filename} -> {viewer_filename}")
        viewer_html = VIEWER_TEMPLATE.format(
            desc=desc,
            title=title,
            basename_no_ext=raw_basename,
            raw_html_file=filename,
            assets_rel=get_rel_path(depth) + 'assets/',
            breadcrumb_html=build_breadcrumb(parts, extra_level=True)
        )
        with open(viewer_path, 'w', encoding='utf-8') as f:
            f.write(viewer_html)

        # Append to index
        if f'href="{viewer_filename}"' not in index_html and f"href='{viewer_filename}'" not in index_html:
            print(f"[{rel_dir}] Adding link to index.html for: {viewer_filename}")
            link_html = LINK_TEMPLATE.format(href=viewer_filename, icon="📄", title=title, desc=desc)
            index_html = index_html.replace('</ul>', f'{link_html}        </ul>', 1)
            added_links += 1

    if added_links > 0:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"[{rel_dir}] Updated index.html with {added_links} new links.")

def process_root():
    index_path = os.path.join(DOCS_DIR, 'index.html')
    if not os.path.exists(index_path):
        return
    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()

    subdirs = [d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d)) and d != 'assets']
    added_links = 0
    for subdir in subdirs:
        href = subdir + "/"
        if f'href="{href}"' not in index_html and f"href='{href}'" not in index_html:
            subdir_title = clean_title(subdir)
            link_html = LINK_TEMPLATE.format(href=href, icon="📁", title=subdir_title, desc=f"Category: {subdir_title}")
            index_html = index_html.replace('</ul>', f'{link_html}        </ul>', 1)
            added_links += 1

    if added_links > 0:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"[root] Updated index.html with {added_links} new links.")

def main():
    print("Scanning for new documents and categories...")
    # Walk bottom-up guarantees we process subdirs first before their parent
    for root, dirs, files in os.walk(DOCS_DIR, topdown=False):
        # normalize paths
        root_norm = root.replace('\\', '/')
        if 'assets' in root_norm.split('/'):
            continue
        if os.path.normpath(root) != os.path.normpath(DOCS_DIR):
            process_directory(root)
    process_root()
    print("Done!")

if __name__ == "__main__":
    main()

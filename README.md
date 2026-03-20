# tnms

A zero-build static document site with category folders. Drop an HTML file into a category, push, and it's live.

## Project Structure

```
tnms/
├── docs/                       ← Served as the site root
│   ├── index.html              ← Landing page (links to categories)
│   ├── assets/
│   │   ├── style.css           ← Shared stylesheet (light + dark theme)
│   │   └── main.js             ← Theme toggle script
│   ├── guides/                 ← Category folder
│   │   ├── index.html          ← Category listing page
│   │   └── example.html        ← Document page
│   └── references/             ← Another category
│       ├── index.html
│       └── css-tokens.html
├── templates/
│   ├── page.html               ← Starter template for new documents
│   └── category-index.html     ← Starter template for new categories
└── .github/workflows/
    └── deploy.yml              ← GitHub Pages deployment action
```

## Adding a New Document

1. Copy the page template into a category folder:
   ```bash
   cp templates/page.html docs/guides/my-new-doc.html
   ```

2. Edit `docs/guides/my-new-doc.html`:
   - Replace `PAGE_TITLE`, `PAGE_DESCRIPTION`, `PAGE_SLUG`
   - Replace `CATEGORY_SLUG` and `CATEGORY_NAME` in the breadcrumb
   - Write your content

3. Add a link entry in the category's `index.html` (e.g., `docs/guides/index.html`):
   ```html
   <li>
     <a href="my-new-doc.html">
       <span class="doc-icon">📄</span>
       <div>
         <div class="doc-title">My New Doc</div>
         <div class="doc-desc">Short description.</div>
       </div>
     </a>
   </li>
   ```

4. Commit and push to `main`.

## Adding a New Category

1. Create the category folder:
   ```bash
   mkdir docs/my-category
   cp templates/category-index.html docs/my-category/index.html
   ```

2. Edit `docs/my-category/index.html` — replace `CATEGORY_NAME`, `CATEGORY_SLUG`, `CATEGORY_DESCRIPTION`.

3. Add a link in the root `docs/index.html`:
   ```html
   <li>
     <a href="my-category/">
       <span class="doc-icon">📁</span>
       <div>
         <div class="doc-title">My Category</div>
         <div class="doc-desc">Description of this category.</div>
       </div>
       <span class="doc-count">0 docs</span>
     </a>
   </li>
   ```

4. Commit and push.

## Local Preview

```bash
python3 -m http.server 8000 -d docs
# Open http://localhost:8000
```

## Deployment

### GitHub Pages (default)

The included `.github/workflows/deploy.yml` deploys `docs/` on every push to `main`.

Go to **Settings → Pages → Source** → select **GitHub Actions**.

### Cloudflare Pages

- Build command: *(leave empty)*
- Build output directory: `docs`

### Vercel

- Framework preset: **Other**
- Build command: *(leave empty)*
- Output directory: `docs`

## Theming

Respects system `prefers-color-scheme` on first visit. Manual toggle via header button, stored in `localStorage`.
import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

# Get the vault root directory (one level up from 15-Automation)
VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load configuration from .env in 15-Automation
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

XWIKI_URL = os.getenv("XWIKI_URL", "https://wiki.systemaops.in").rstrip("/")
XWIKI_USER = os.getenv("XWIKI_USER")
XWIKI_PASS = os.getenv("XWIKI_PASS")
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", VAULT_ROOT)

def validate_config():
    if not XWIKI_USER or not XWIKI_PASS:
        print("Error: XWIKI_USER or XWIKI_PASS is missing in your .env file.")
        return False
    return True

def safe_filename(name):
    invalid_chars = '<>:"/\\|?*'
    clean_name = ''.join(c for c in name if c not in invalid_chars)
    return clean_name.strip()

def login_keycloak_sso(session):
    print(f"Authenticating via openDesk Keycloak SSO for {XWIKI_USER}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 1. Access Main page to trigger Keycloak redirect
    r1 = session.get(f"{XWIKI_URL}/bin/view/Main/", headers=headers, allow_redirects=True)
    if "id.systemaops.in" not in r1.url and "login-actions" not in r1.text:
        print("Already authenticated or no Keycloak redirect detected.")
        return True

    # 2. Parse Keycloak form action URL
    action_match = re.search(r'action="([^"]+)"', r1.text)
    if not action_match:
        print("Could not find Keycloak login form action URL.")
        return False

    login_url = action_match.group(1).replace('&amp;', '&')
    
    # 3. Submit credentials to Keycloak
    payload = {
        'username': XWIKI_USER,
        'password': XWIKI_PASS
    }
    r2 = session.post(login_url, data=payload, headers=headers, allow_redirects=True)
    
    if r2.status_code == 200 and "id.systemaops.in" not in r2.url:
        print("Keycloak SSO authentication successful!")
        return True
    else:
        print("Keycloak SSO authentication failed. Please check your XWIKI_USER and XWIKI_PASS in .env.")
        return False

def sync_xwiki_pages():
    if not validate_config():
        return

    base_xwiki_folder = os.path.join(VAULT_PATH, "09-Documentation", "XWiki")
    os.makedirs(base_xwiki_folder, exist_ok=True)

    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    # Perform Keycloak SSO Authentication
    if not login_keycloak_sso(session):
        return

    # 1. Paginate to fetch ALL page summaries
    print("Cataloging all pages from XWiki...")
    page_summaries = []
    start = 0
    chunk_size = 200

    while True:
        pages_api_url = f"{XWIKI_URL}/rest/wikis/xwiki/pages?start={start}&number={chunk_size}&media=json"
        try:
            response = session.get(pages_api_url, timeout=20)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Failed to fetch XWiki pages chunk at start={start}: {e}")
            break

        summaries = data.get("pageSummaries", [])
        if not summaries and isinstance(data, dict):
            summaries = data.get("pages", [])

        if not summaries:
            break

        page_summaries.extend(summaries)
        start += len(summaries)
        print(f"  Cataloged {len(page_summaries)} pages so far...")
        
        if len(summaries) < chunk_size:
            break

    total_pages = len(page_summaries)
    print(f"\n🎯 Total cataloged pages: {total_pages}! Starting full download into Space subfolders...")

    # Deduplicate: the pages REST API returns translation variants as separate
    # entries that share the same fullName. Keep only the first (default) variant
    # so each unique document maps to exactly one file.
    seen = set()
    unique_summaries = []
    for item in page_summaries:
        full = item.get("fullName") or item.get("id") or item.get("name")
        if full in seen:
            continue
        seen.add(full)
        unique_summaries.append(item)

    print(f"  Deduplicated to {len(unique_summaries)} unique documents.")

    synced_count = 0
    written_files = []
    for idx, item in enumerate(unique_summaries, 1):
        page_id = item.get("fullName") or item.get("id") or item.get("name")
        page_title = item.get("title") or item.get("name") or page_id
        space = item.get("space") or "General"
        
        # Organize files into space subdirectories
        space_folder = os.path.join(base_xwiki_folder, safe_filename(space))
        os.makedirs(space_folder, exist_ok=True)

        # Link to fetch full page details including content
        page_url = item.get("links", [{}])[0].get("href")
        if not page_url:
            page_url = f"{XWIKI_URL}/rest/wikis/xwiki/spaces/{space}/pages/{page_id}?media=json"
        elif not page_url.endswith("media=json"):
            page_url += "?media=json" if "?" not in page_url else "&media=json"

        try:
            p_res = session.get(page_url, timeout=10)
            if p_res.status_code != 200:
                continue
            p_data = p_res.json()
        except Exception:
            continue

        title = p_data.get("title") or page_title
        content = p_data.get("content", "No content available.")
        author = p_data.get("authorName") or p_data.get("author") or "Unknown"
        modified = p_data.get("modified") or datetime.now().strftime('%Y-%m-%d')
        version = p_data.get("version") or "1.0"

        # Safe filename
        clean_title = safe_filename(title)
        filename = f"{clean_title}.md"
        file_path = os.path.join(space_folder, filename)

        # Markdown with Obsidian Frontmatter
        md_content = f"""---
id: xwiki-{page_id}
type: XWiki Page
space: "{space}"
author: "{author}"
version: "{version}"
last_modified: {modified}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - xwiki/documentation
  - space/{space.lower().replace(" ", "-")}
---
# {title}

- **Space:** {space}
- **Author:** {author}
- **Last Modified:** {modified}
- **Source:** [{title}]({XWIKI_URL}/bin/view/{space}/{page_id})

---

{content}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        synced_count += 1
        written_files.append(file_path)
        if synced_count % 50 == 0 or synced_count == len(unique_summaries):
            print(f" Progress: [{synced_count}/{len(unique_summaries)}] pages saved...")

    cleanup_stale_xwiki_files(base_xwiki_folder, written_files)
    print(f"\n🎉 FULL SYNC COMPLETE! Successfully synced {synced_count} out of {len(unique_summaries)} XWiki pages into 09-Documentation/XWiki/")


def cleanup_stale_xwiki_files(base_xwiki_folder, written_files):
    """Remove synced .md files that no longer exist on the XWiki server."""
    written = set(os.path.abspath(p) for p in written_files)
    removed = 0
    for root, _, files in os.walk(base_xwiki_folder):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            path = os.path.abspath(os.path.join(root, fname))
            if path in written:
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    head = f.read(200)
            except Exception:
                continue
            if "id: xwiki-" in head:
                os.remove(path)
                removed += 1
    if removed:
        print(f"  Cleaned up {removed} stale XWiki page file(s).")

if __name__ == "__main__":
    sync_xwiki_pages()

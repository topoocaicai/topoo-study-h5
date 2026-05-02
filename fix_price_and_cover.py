"""Fix UK price 16980->15980 + remove price/含机票签证 from cover-meta in ALL sub-pages."""
import re, glob, os

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

# === 1. Fix UK price: 16980/16,980 -> 15980/15,980 ===
uk_files = ["study-uk-entry.html", "study-uk-4d3n.html", "study-uk-7d6n.html", "study-uk-14d13n.html"]
# Only 4d3n needs price fix (first tier), entry also
uk_price_files = ["study-uk-entry.html", "study-uk-4d3n.html"]

for fn in uk_price_files:
    path = os.path.join(BASE, fn)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace 16,980 or 16980 with 15,980/15980
    content = content.replace('16,980', '15,980')
    content = content.replace('16980', '15980')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed UK price in {fn}")

# === 2. Remove price + 含机票签证 from cover-meta in ALL sub-pages (non-entry) ===
sub_pages = glob.glob(os.path.join(BASE, "study-*-4d3n.html")) + \
            glob.glob(os.path.join(BASE, "study-*-7d6n.html")) + \
            glob.glob(os.path.join(BASE, "study-*-14d13n.html"))

for path in sub_pages:
    fn = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the price meta-item block: 4 lines
    # Pattern: <div class="cover-meta-item"> with price value and 含机票签证 label
    pattern = r'\s*<div class="cover-meta-item">\s*\n\s*<div class="val">.*?元</div>\s*\n\s*<div class="label">含机票签证</div>\s*\n\s*</div>'
    new_content = re.sub(pattern, '', content)

    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed price from cover in {fn}")
    else:
        print(f"No price found in cover of {fn}")

print("\nDone!")

"""Fix: remove price + 含机票签证 from cover-meta in ALL sub-pages (single-line + multi-line)."""
import re, glob, os

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

sub_pages = glob.glob(os.path.join(BASE, "study-*-4d3n.html")) + \
            glob.glob(os.path.join(BASE, "study-*-7d6n.html")) + \
            glob.glob(os.path.join(BASE, "study-*-14d13n.html"))

for path in sub_pages:
    fn = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Pattern 1: multi-line (4d3n style)
    content = re.sub(
        r'\s*<div class="cover-meta-item">\s*\n\s*<div class="val">[\d,]+<span class="unit">元</span></div>\s*\n\s*<div class="label">含机票签证</div>\s*\n\s*</div>',
        '', content)

    # Pattern 2: single-line (7d6n/14d13n style)
    content = re.sub(
        r'\s*<div class="cover-meta-item"><div class="val">[\d,]+<span class="unit">元</span></div><div class="label">含机票签证</div></div>\n?',
        '', content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK: {fn}")
    else:
        print(f"SKIP: {fn}")

print("\nDone!")

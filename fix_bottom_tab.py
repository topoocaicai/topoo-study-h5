import re, sys

def fix(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # Remove CSS: .bottom-spacer, .bottom-tab, .tab-item, .tab-icon, .tab-label
    c = re.sub(r'\n\s*\.bottom-spacer\s*\{[^}]*\}', '\n', c)
    c = re.sub(r'\n\s*\.bottom-tab\s*\{[^}]*\}', '\n', c)
    c = re.sub(r'\n\s*\.tab-item\.active\s*\{[^}]*\}', '\n', c)
    c = re.sub(r'\n\s*\.tab-icon\s*\{[^}]*\}', '\n', c)
    c = re.sub(r'\n\s*\.tab-label\s*\{[^}]*\}', '\n', c)
    # Catch .tab-item variants
    c = re.sub(r'\n\s*\.tab-item\s*\{[^}]*\}', '\n', c)

    # Remove HTML: <!-- 底部Tab --> ... </div> (the whole block)
    c = re.sub(r'\n\s*<!-- 底部Tab -->.*?</div>\s*</div>', '\n', c, flags=re.DOTALL)

    if c != orig:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'OK: {fname}')
    else:
        print(f'SKIP: {fname}')

for f in ['collision.html', 'story.html', 'plaza.html']:
    fix(f)

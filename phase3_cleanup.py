# -*- coding: utf-8 -*-
"""Phase 3: Clean remaining Chinese text (comments, back cover, etc.)"""
import os, re, glob

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    changed = False

    # 1. HTML comments - translate
    comment_map = {
        '4日3晚': '4D3N',
        '7日6晚': '7D6N',
        '14日13晚': '14D13N',
        '机票备注': 'Flight note',
        '价格备注': 'Price note',
        '封面': 'Cover',
        '南京城市介绍': 'Nanjing intro',
        '选择行程': 'Programs',
        '备选研学项目': 'Optional programs',
        '封底': 'Back cover',
        '行程概览': 'Itinerary',
        '费用说明': 'Pricing',
        '安全保障': 'Safety',
        '服务说明': 'Services',
    }
    for zh, en in comment_map.items():
        if zh in c:
            c = c.replace(zh, en)
            changed = True

    # 2. Back cover info - translate remaining Chinese
    # Pattern: "古都文脉探索营 · XXX · 入口页" or "古都文脉探索营 · XXX · 4日3晚"
    c = re.sub(
        r'古都文脉探索营 · ([^·<]+) · 入口页',
        lambda m: f'Nanjing Cultural Camp · {translate_region_in_bc(m.group(1))} · Entry Page',
        c
    )
    c = re.sub(
        r'古都文脉探索营 · ([^·<]+) · (\d+日\d+晚)',
        lambda m: f'Nanjing Cultural Camp · {translate_region_in_bc(m.group(1))} · {m.group(2)}',
        c
    )

    # 3. Any remaining "南京 / Nanjing" patterns
    c = c.replace('南京 / Nanjing', 'Nanjing')

    if changed or True:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)

    # Count remaining Chinese (exclude file paths)
    # Remove href= and src= attributes
    c_clean = re.sub(r'(?:href|src)="[^"]*"', '', c)
    chinese = re.findall(r'[\u4e00-\u9fff]', c_clean)
    return len(chinese)

def translate_region_in_bc(text):
    mapping = {
        "港澳台": "HK, Macao & Taiwan",
        "东盟": "ASEAN",
        "俄罗斯": "Russia",
        "欧洲大陆": "Continental Europe",
        "英国": "United Kingdom",
        "美国": "United States",
    }
    return mapping.get(text, text)

def main():
    files = glob.glob(os.path.join(BASE, '拓圈研学*.html'))
    # Exclude non-deployed files
    skip = ['古都文脉探索营·4日3晚·设计示范.html', '海外4日3晚', '海外7日6晚', '海外14日13晚',
            '国内4日3晚', '国内5日4晚', '港澳台·古都文脉探索营.html', '东盟·古都文脉探索营.html',
            '俄罗斯·古都文脉探索营.html', '欧洲大陆·古都文脉探索营.html', '英国·古都文脉探索营.html', '美国·古都文脉探索营.html']
    skip_keywords = ['设计示范', '海外4', '海外7', '海外14', '国内4', '国内5']

    for f in sorted(files):
        bn = os.path.basename(f)
        if any(k in bn for k in skip_keywords):
            continue
        # Also skip the "古都文脉探索营.html" (no region prefix, standalone file)
        if bn == '拓圈研学·港澳台·古都文脉探索营.html' or '·古都文脉探索营.html' == bn[-len('·古都文脉探索营.html'):]:
            # Only skip if it's the standalone one (no region prefix like 4日3晚)
            if '4日' not in bn and '7日' not in bn and '14日' not in bn and '入口' not in bn:
                continue

        remaining = clean_file(f)
        print(f"  {bn}: {remaining} remaining Chinese chars (in content, not paths)")

    print("\n=== Phase 3 Done ===")

if __name__ == "__main__":
    main()

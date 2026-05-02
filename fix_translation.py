# -*- coding: utf-8 -*-
"""Fix prices + remaining Chinese text in all study tour HTML files."""
import re, os, glob

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

PRICES = {
    "港澳台": [7980, 13980, 21980],
    "东盟": [9980, 15980, 23980],
    "俄罗斯": [9980, 15980, 23980],
    "欧洲大陆": [15980, 21980, 29980],
    "英国": [16980, 22980, 30980],
    "美国": [19980, 25980, 33980],
}

def fmt(n):
    return f"{n:,}"

def fix_file(filepath, region):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Fix prices: pattern is ¥X,XXX inside choose-price or similar
    if region in PRICES:
        prices = PRICES[region]
        # Find all price patterns: ¥X,XXX
        all_prices = re.findall(r'¥([\d,]+)', c)
        # Filter to only those in choose-price contexts (should be exactly 3 for entry, 1 for sub)
        if all_prices:
            price_idx = 0
            new_c = []
            last_end = 0
            for m in re.finditer(r'¥([\d,]+)', c):
                start = m.start()
                num = int(m.group(1).replace(',', ''))
                # Check if this looks like a real price (4+ digits)
                if num >= 1000 and price_idx < len(prices):
                    new_c.append(c[last_end:start])
                    new_c.append(f'¥{fmt(prices[price_idx])}')
                    last_end = m.end()
                    price_idx += 1
                else:
                    # Not a price we want to replace, keep original
                    continue
            new_c.append(c[last_end:])
            c = ''.join(new_c)

    # 2. Fix remaining bilingual patterns: "中文 / English" -> "English"
    # General pattern for section headers
    c = re.sub(r'([\u4e00-\u9fff][\u4e00-\u9fff\s·（）()\d]+)\s*/\s*([A-Z][A-Za-z\s&\']+)', r'\2', c)

    # 3. Fix "南京 / Nanjing" tags
    c = c.replace('南京 / Nanjing', 'Nanjing')

    # 4. Fix remaining Chinese in back cover
    c = c.replace('本方案最终解释权归主办方所有<br>\n    Final interpretation right reserved by the organizer',
                  'Final interpretation right reserved by the organizer')
    c = c.replace('本方案最终解释权归主办方所有\nFinal interpretation right reserved by the organizer',
                  'Final interpretation right reserved by the organizer')
    c = c.replace('本方案最终解释权归主办方所有', 'Final interpretation right reserved by the organizer')

    # 5. Fix HTML comments still in Chinese
    c = c.replace('<!-- ===== 封面 / Cover ===== -->', '<!-- Cover -->')
    c = c.replace('<!-- ===== 南京城市介绍 ===== -->', '<!-- Nanjing City Profile -->')
    c = c.replace('<!-- ===== 选择行程 ===== -->', '<!-- Choose Your Program -->')
    c = c.replace('<!-- ===== 备选研学项目 ===== -->', '<!-- Optional Programs -->')
    c = c.replace('<!-- ===== 封底 ===== -->', '<!-- Back Cover -->')
    c = c.replace('<!-- 机票备注 -->', '')
    c = c.replace('<!-- 价格备注 -->', '')
    c = re.sub(r'<!-- \d+日\d+晚 -->', '', c)

    # 6. Fix any remaining "中文 / English" patterns more aggressively
    # Match: Chinese text / English text where Chinese has 2+ chars
    c = re.sub(
        r'([\u4e00-\u9fff][\u4e00-\u9fff\s，。、；：·""！？（）()\d°C°\-—]+?)\s*/\s*([A-Za-z][A-Za-z\s,.\'&\(\)/\d°C°\-—]+)',
        lambda m: m.group(2) if len(re.findall(r'[\u4e00-\u9fff]', m.group(1))) >= 2 else m.group(0),
        c
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  Fixed: {os.path.basename(filepath)}")

def main():
    # All entry pages
    entries = [
        ("拓圈研学·港澳台·入口页.html", "港澳台"),
        ("拓圈研学·东盟·入口页.html", "东盟"),
        ("拓圈研学·俄罗斯·入口页.html", "俄罗斯"),
        ("拓圈研学·欧洲大陆·入口页.html", "欧洲大陆"),
        ("拓圈研学·英国·入口页.html", "英国"),
        ("拓圈研学·美国·入口页.html", "美国"),
        ("拓圈研学·国内中小学生·入口页.html", "国内中小学生"),
    ]
    # All sub pages
    subs = []
    for region in ["港澳台", "东盟", "俄罗斯", "欧洲大陆", "英国", "美国"]:
        for dur in ["4日3晚", "7日6晚", "14日13晚"]:
            subs.append((f"拓圈研学·{region}·{dur}·古都文脉探索营.html", region))

    print("=== Fixing entry pages ===")
    for fname, region in entries:
        fpath = os.path.join(BASE, fname)
        if os.path.exists(fpath):
            fix_file(fpath, region)

    print("\n=== Fixing sub pages ===")
    for fname, region in subs:
        fpath = os.path.join(BASE, fname)
        if os.path.exists(fpath):
            fix_file(fpath, region)

    print("\n=== Done! ===")

if __name__ == "__main__":
    main()

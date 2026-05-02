# -*- coding: utf-8 -*-
"""Direct price replacement - brute force approach."""
import os, re

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

PRICES = {
    "港澳台": [(9980, 7980), (15980, 13980), (23980, 21980)],
    "东盟": [(9980, 9980), (15980, 15980), (23980, 23980)],  # no change
    "俄罗斯": [(9980, 9980), (15980, 15980), (23980, 23980)],  # no change
    "欧洲大陆": [(9980, 15980), (15980, 21980), (23980, 29980)],
    "英国": [(9980, 16980), (15980, 22980), (23980, 30980)],
    "美国": [(9980, 19980), (15980, 25980), (23980, 33980)],
}

def fmt(n):
    return f"{n:,}"

def fix_prices_in_file(filepath, region):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if region not in PRICES:
        return

    old_new = PRICES[region]
    for old_p, new_p in old_new:
        old_str = f"¥{fmt(old_p)}"
        new_str = f"¥{fmt(new_p)}"
        if old_str != new_str:
            content = content.replace(old_str, new_str)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Count prices in file
    prices = re.findall(r'¥([\d,]+)', content)
    print(f"  {os.path.basename(filepath)}: prices found: {prices}")

def main():
    regions_files = {
        "港澳台": [
            "拓圈研学·港澳台·入口页.html",
            "拓圈研学·港澳台·4日3晚·古都文脉探索营.html",
            "拓圈研学·港澳台·7日6晚·古都文脉探索营.html",
            "拓圈研学·港澳台·14日13晚·古都文脉探索营.html",
        ],
        "欧洲大陆": [
            "拓圈研学·欧洲大陆·入口页.html",
            "拓圈研学·欧洲大陆·4日3晚·古都文脉探索营.html",
            "拓圈研学·欧洲大陆·7日6晚·古都文脉探索营.html",
            "拓圈研学·欧洲大陆·14日13晚·古都文脉探索营.html",
        ],
        "英国": [
            "拓圈研学·英国·入口页.html",
            "拓圈研学·英国·4日3晚·古都文脉探索营.html",
            "拓圈研学·英国·7日6晚·古都文脉探索营.html",
            "拓圈研学·英国·14日13晚·古都文脉探索营.html",
        ],
        "美国": [
            "拓圈研学·美国·入口页.html",
            "拓圈研学·美国·4日3晚·古都文脉探索营.html",
            "拓圈研学·美国·7日6晚·古都文脉探索营.html",
            "拓圈研学·美国·14日13晚·古都文脉探索营.html",
        ],
    }

    for region, files in regions_files.items():
        print(f"\n=== {region} ===")
        for fname in files:
            fpath = os.path.join(BASE, fname)
            if os.path.exists(fpath):
                fix_prices_in_file(fpath, region)

if __name__ == "__main__":
    main()

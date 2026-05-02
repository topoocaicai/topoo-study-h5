# -*- coding: utf-8 -*-
"""
Phase 1: Fix prices. Pattern is: ¥</span>9,980
"""
import os

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

PRICE_MAP = {
    "港澳台": [(9980, 7980), (15980, 13980), (23980, 21980)],
    "欧洲大陆": [(9980, 15980), (15980, 21980), (23980, 29980)],
    "英国": [(9980, 16980), (15980, 22980), (23980, 30980)],
    "美国": [(9980, 19980), (15980, 25980), (23980, 33980)],
}

def fmt(n):
    return f"{n:,}"

def fix_file(filepath, region):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    if region in PRICE_MAP:
        for old_p, new_p in PRICE_MAP[region]:
            # Pattern: </span>9,980<span
            old_s = f"</span>{fmt(old_p)}<span"
            new_s = f"</span>{fmt(new_p)}<span"
            count = c.count(old_s)
            if count:
                c = c.replace(old_s, new_s)
                print(f"  {os.path.basename(filepath)}: ¥{fmt(old_p)} -> ¥{fmt(new_p)} ({count}x)")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)

def main():
    regions_files = {
        "港澳台": [f"拓圈研学·港澳台·{d}.html" for d in ["入口页", "4日3晚·古都文脉探索营", "7日6晚·古都文脉探索营", "14日13晚·古都文脉探索营"]],
        "欧洲大陆": [f"拓圈研学·欧洲大陆·{d}.html" for d in ["入口页", "4日3晚·古都文脉探索营", "7日6晚·古都文脉探索营", "14日13晚·古都文脉探索营"]],
        "英国": [f"拓圈研学·英国·{d}.html" for d in ["入口页", "4日3晚·古都文脉探索营", "7日6晚·古都文脉探索营", "14日13晚·古都文脉探索营"]],
        "美国": [f"拓圈研学·美国·{d}.html" for d in ["入口页", "4日3晚·古都文脉探索营", "7日6晚·古都文脉探索营", "14日13晚·古都文脉探索营"]],
    }

    for region, files in regions_files.items():
        print(f"\n=== {region} ===")
        for fname in files:
            fpath = os.path.join(BASE, fname)
            if os.path.exists(fpath):
                fix_file(fpath, region)

    print("\n=== Prices fixed ===")

if __name__ == "__main__":
    main()

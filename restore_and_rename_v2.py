#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复研学HTML文件：
1. 从git恢复中文内容（覆盖翻译过的英文版）
2. 重命名为英文
3. 修正价格
4. 更新文件内部链接
"""

import os
import re
import subprocess
import shutil

WORK_DIR = r"C:\Users\Administrator\WorkBuddy\Claw"

# 文件名映射：中文名 -> 英文名
# 命名规则：study-{region}-{type}.html
FILE_MAP = {
    # 港澳台 Hong Kong, Macao & Taiwan
    "拓圈研学·港澳台·入口页.html": "study-hk-macao-taiwan-entry.html",
    "拓圈研学·港澳台·4日3晚·古都文脉探索营.html": "study-hk-macao-taiwan-4d3n.html",
    "拓圈研学·港澳台·7日6晚·古都文脉探索营.html": "study-hk-macao-taiwan-7d6n.html",
    "拓圈研学·港澳台·14日13晚·古都文脉探索营.html": "study-hk-macao-taiwan-14d13n.html",

    # 欧洲大陆 Europe
    "拓圈研学·欧洲大陆·入口页.html": "study-europe-entry.html",
    "拓圈研学·欧洲大陆·4日3晚·古都文脉探索营.html": "study-europe-4d3n.html",
    "拓圈研学·欧洲大陆·7日6晚·古都文脉探索营.html": "study-europe-7d6n.html",
    "拓圈研学·欧洲大陆·14日13晚·古都文脉探索营.html": "study-europe-14d13n.html",

    # 英国 UK
    "拓圈研学·英国·入口页.html": "study-uk-entry.html",
    "拓圈研学·英国·4日3晚·古都文脉探索营.html": "study-uk-4d3n.html",
    "拓圈研学·英国·7日6晚·古都文脉探索营.html": "study-uk-7d6n.html",
    "拓圈研学·英国·14日13晚·古都文脉探索营.html": "study-uk-14d13n.html",

    # 美国 USA
    "拓圈研学·美国·入口页.html": "study-usa-entry.html",
    "拓圈研学·美国·4日3晚·古都文脉探索营.html": "study-usa-4d3n.html",
    "拓圈研学·美国·7日6晚·古都文脉探索营.html": "study-usa-7d6n.html",
    "拓圈研学·美国·14日13晚·古都文脉探索营.html": "study-usa-14d13n.html",

    # 俄罗斯 Russia
    "拓圈研学·俄罗斯·入口页.html": "study-russia-entry.html",
    "拓圈研学·俄罗斯·4日3晚·古都文脉探索营.html": "study-russia-4d3n.html",
    "拓圈研学·俄罗斯·7日6晚·古都文脉探索营.html": "study-russia-7d6n.html",
    "拓圈研学·俄罗斯·14日13晚·古都文脉探索营.html": "study-russia-14d13n.html",

    # 东盟 ASEAN
    "拓圈研学·东盟·入口页.html": "study-asean-entry.html",
    "拓圈研学·东盟·4日3晚·古都文脉探索营.html": "study-asean-4d3n.html",
    "拓圈研学·东盟·7日6晚·古都文脉探索营.html": "study-asean-7d6n.html",
    "拓圈研学·东盟·14日13晚·古都文脉探索营.html": "study-asean-14d13n.html",

    # 国内中小学生 Domestic
    "拓圈研学·国内中小学生·入口页.html": "study-domestic-k12-entry.html",
    "拓圈研学·国内4日3晚·古都文脉探索营.html": "study-domestic-4d3n.html",
    "拓圈研学·国内5日4晚·古都文脉探索营.html": "study-domestic-5d4n.html",
}

# 价格修正映射：旧价格(含格式) -> 新价格
# 格式：</span>9,980<span
PRICE_FIXES = [
    # 港澳台：9980->7980, 15980->13980, 23980->21980
    ("</span>9,980<span", "</span>7,980<span"),
    ("</span>15,980<span", "</span>13,980<span"),
    ("</span>23,980<span", "</span>21,980<span"),
    # 欧洲大陆：9980->15980, 15980->21980, 23980->29980
    ("</span>9,980<span", "</span>15,980<span"),   # 需要更精确的匹配
    ("</span>15,980<span", "</span>21,980<span"),  # 需要更精确的匹配
    ("</span>23,980<span", "</span>29,980<span"),  # 需要更精确的匹配
]

def restore_from_git(filepath):
    """从git恢复文件（丢弃本地修改）"""
    try:
        result = subprocess.run(
            ["git", "checkout", "HEAD", "--", filepath],
            cwd=WORK_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  ✓ 已从git恢复: {filepath}")
            return True
        else:
            print(f"  ✗ git恢复失败: {filepath} | {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  ✗ 异常: {e}")
        return False

def fix_prices_in_file(filepath):
    """修正文件中的价格"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 按地区修正价格 - 根据文件名判断地区
    fname = os.path.basename(filepath)

    if "hk-macao-taiwan" in fname:
        # 港澳台：7980 / 13980 / 21980
        content = content.replace("</span>9,980<span", "</span>7,980<span")
        content = content.replace("</span>15,980<span", "</span>13,980<span")
        content = content.replace("</span>23,980<span", "</span>21,980<span")
        print(f"  价格修正: 港澳台 7980/13980/21980")

    elif "europe" in fname:
        # 欧洲大陆：15980 / 21980 / 29980
        content = content.replace("</span>9,980<span", "</span>15,980<span")
        content = content.replace("</span>15,980<span", "</span>21,980<span")
        content = content.replace("</span>23,980<span", "</span>29,980<span")
        print(f"  价格修正: 欧洲大陆 15980/21980/29980")

    elif "uk" in fname:
        # 英国：16980 / 22980 / 30980
        content = content.replace("</span>9,980<span", "</span>16,980<span")
        content = content.replace("</span>15,980<span", "</span>22,980<span")
        content = content.replace("</span>23,980<span", "</span>30,980<span")
        print(f"  价格修正: 英国 16980/22980/30980")

    elif "usa" in fname:
        # 美国：19980 / 25980 / 33980
        content = content.replace("</span>9,980<span", "</span>19,980<span")
        content = content.replace("</span>15,980<span", "</span>25,980<span")
        content = content.replace("</span>23,980<span", "</span>33,980<span")
        print(f"  价格修正: 美国 19980/25980/33980")

    elif "russia" in fname or "asean" in fname or "domestic" in fname:
        # 俄罗斯/东盟/国内：保持原价 9980/15980/23980（不需要修改）
        print(f"  价格保持不变: 9980/15980/23980")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def update_links_in_file(filepath, file_map):
    """更新文件内部链接（中文文件名 -> 英文文件名）"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for chinese_name, english_name in file_map.items():
        if chinese_name in content:
            content = content.replace(chinese_name, english_name)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    os.chdir(WORK_DIR)

    print("=" * 60)
    print("Step 1: 从git恢复所有中文内容")
    print("=" * 60)

    # 先恢复git跟踪的文件
    for chinese_name in FILE_MAP.keys():
        if os.path.exists(chinese_name):
            restore_from_git(chinese_name)

    print()
    print("=" * 60)
    print("Step 2: 修正价格")
    print("=" * 60)

    for chinese_name in FILE_MAP.keys():
        if os.path.exists(chinese_name):
            fix_prices_in_file(chinese_name)

    print()
    print("=" * 60)
    print("Step 3: 更新内部链接（中文文件名 -> 英文文件名）")
    print("=" * 60)

    for chinese_name in FILE_MAP.keys():
        if os.path.exists(chinese_name):
            updated = update_links_in_file(chinese_name, FILE_MAP)
            if updated:
                print(f"  ✓ 已更新链接: {chinese_name}")

    print()
    print("=" * 60)
    print("Step 4: 重命名为英文")
    print("=" * 60)

    for chinese_name, english_name in FILE_MAP.items():
        if os.path.exists(chinese_name):
            if os.path.exists(english_name):
                os.remove(english_name)
                print(f"  已删除旧文件: {english_name}")
            shutil.move(chinese_name, english_name)
            print(f"  ✓ {chinese_name} -> {english_name}")

    print()
    print("=" * 60)
    print("Step 5: 对英文文件再次更新链接")
    print("=" * 60)

    # 现在文件已经是英文名字了，需要再次更新链接
    # 因为Step 3是在中文名文件上操作的，链接已经改成英文了
    # 但需要确保英文文件之间的链接是正确的

    for chinese_name, english_name in FILE_MAP.items():
        if os.path.exists(english_name):
            updated = update_links_in_file(english_name, FILE_MAP)
            if updated:
                print(f"  ✓ 已更新链接: {english_name}")

    print()
    print("=" * 60)
    print("完成！")
    print(f"共处理 {len(FILE_MAP)} 个文件")
    print("=" * 60)

if __name__ == "__main__":
    main()

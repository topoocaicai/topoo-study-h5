#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix two issues:
1. Duplicate "备选项目" section in study-hk-macao-taiwan-4d3n.html
2. Mobile layout: overview-grid should be single column on mobile for all foreign sub-pages
"""

import os
import re

WORK_DIR = r"C:\Users\Administrator\WorkBuddy\Claw"

def fix_duplicate_section(filepath):
    """Remove the SECOND duplicate '备选项目' section"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header = "<!-- ===== 备选研学项目 / Optional Programs ===== -->"
    indices = [i for i, line in enumerate(lines) if header in line]
    print(f"  Found {len(indices)} occurrences at lines {[i+1 for i in indices]}")

    if len(indices) < 2:
        print("  No duplicate found, skipping")
        return False

    second_start = indices[1]

    # Find the closing </div> for the section that starts at second_start+1
    div_depth = 0
    section_opened = False
    section_end = None

    for i in range(second_start, len(lines)):
        line = lines[i]
        if ('<div class="section"' in line or '<div class="section">' in line) and not section_opened:
            section_opened = True
            div_depth = 1
        elif section_opened:
            div_depth += line.count('<div') - line.count('</div>')
            if div_depth == 0:
                section_end = i
                break

    if section_end is None:
        print("  ERROR: Could not find end of duplicate section!")
        return False

    print(f"  Removing lines {second_start+1} to {section_end+1}")

    # Check for misplaced safety comment before duplicate
    pre_comment_idx = None
    for i in range(max(0, second_start-5), second_start):
        if "<!-- ===== 安全保障 ===== -->" in lines[i]:
            pre_comment_idx = i
            break

    if pre_comment_idx is not None:
        print(f"  Also removing misplaced safety comment at line {pre_comment_idx+1}")
        del lines[pre_comment_idx:section_end+1]
    else:
        del lines[second_start:section_end+1]

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"  OK Removed duplicate section from {os.path.basename(filepath)}")
    return True


def fix_mobile_layout(filepath):
    """Fix mobile layout: overview-grid single column on mobile"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Fix: in mobile CSS, change "grid-template-columns: 1fr 1fr" to "grid-template-columns: 1fr"
    # for .overview-grid
    old = ".overview-grid, .feature-grid { grid-template-columns: 1fr 1fr; }"
    new = ".overview-grid { grid-template-columns: 1fr; }\n    .feature-grid { grid-template-columns: 1fr; }"
    
    if old in content:
        content = content.replace(old, new)
        print(f"  Fixed mobile grid in {os.path.basename(filepath)}")
    else:
        # Try other patterns
        # Maybe it's split across lines?
        if "grid-template-columns: 1fr 1fr" in content:
            print(f"  Found 'grid-template-columns: 1fr 1fr' but pattern not exact, manual check needed: {os.path.basename(filepath)}")
        else:
            print(f"  No mobile grid issue found (or already fixed): {os.path.basename(filepath)}")
            return False

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    os.chdir(WORK_DIR)

    print("=" * 60)
    print("Issue 1: Remove duplicate section from 港澳台4日3晚")
    print("=" * 60)
    fix_duplicate_section("study-hk-macao-taiwan-4d3n.html")

    print()
    print("=" * 60)
    print("Issue 2: Fix mobile layout for foreign sub-pages")
    print("=" * 60)

    foreign_sub_pages = [
        "study-europe-4d3n.html",
        "study-europe-7d6n.html",
        "study-europe-14d13n.html",
        "study-uk-4d3n.html",
        "study-uk-7d6n.html",
        "study-uk-14d13n.html",
        "study-usa-4d3n.html",
        "study-usa-7d6n.html",
        "study-usa-14d13n.html",
        "study-russia-4d3n.html",
        "study-russia-7d6n.html",
        "study-russia-14d13n.html",
        "study-asean-4d3n.html",
        "study-asean-7d6n.html",
        "study-asean-14d13n.html",
    ]

    for f in foreign_sub_pages:
        if os.path.exists(f):
            fix_mobile_layout(f)
        else:
            print(f"  File not found: {f}")

    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import re

path = r'C:\Users\Administrator\WorkBuddy\Claw\.workbuddy\memory\MEMORY.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('\u8fd1\u671f\u9879\u76ee')
if idx < 0:
    print('ERROR: section not found')
else:
    before = content[:idx]
    lines = []
    lines.append('\u005b\u005bTOPOO\u5165\u573a\u5267\u672c\u0028\u0032\u0030\u0032\u0036\u002d\u0030\u0035\u002d\u0030\u0031\u5b9a\u7a3f\u0029\u005d\u005d')
    # Just use a simpler approach
    print(f'Found at {idx}, length before={len(before)}')

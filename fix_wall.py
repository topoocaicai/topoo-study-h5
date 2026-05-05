# -*- coding: utf-8 -*-
# 生成完整 TopSpace 广场 H5 v4 - 修复版

html = open(r'C:/Users/Administrator/Desktop/定稿app页面/TopSpace广场模板.html', 'r', encoding='utf-8').read()

# 修复1: wall-wrap需要position:relative让牌匾正确相对定位
html = html.replace(
    '.wall-wrap { position:absolute; bottom:0; left:0; right:0; height:62%; z-index:5; }',
    '.wall-wrap { position:relative; bottom:0; left:0; right:0; height:62%; z-index:5; }'
)

# 修复2: 牌匾位置调整 - 放在城墙高度12%的位置
html = html.replace(
    '.wall-plaque { position:absolute; top:8%; transform:translateX(-50%); z-index:10;',
    '.wall-plaque { position:absolute; top:12%; transform:translateX(-50%); z-index:10;'
)

with open(r'C:/Users/Administrator/Desktop/定稿app页面/TopSpace广场模板.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('修复完成！')

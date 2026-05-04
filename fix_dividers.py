p = r'C:\Users\Administrator\WorkBuddy\Claw\拓圈·创造者手册·H5.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# 在第4章结束和第5章之间加 divider
marker1 = '</details>\n\n<!-- 第五章：五行力量体系 -->'
replacement1 = '</details>\n\n<div class="divider"></div>\n\n<!-- 第五章：五行力量体系 -->'
if marker1 in c:
    c = c.replace(marker1, replacement1)
    print('已添加第5章上方divider')
else:
    print('未找到marker1')

# 在第5章结束和第6章之间加 divider
marker2 = '</details>\n\n<!-- 第六章：如何成为开拓者？ -->'
replacement2 = '</details>\n\n<div class="divider"></div>\n\n<!-- 第六章：如何成为开拓者？ -->'
if marker2 in c:
    c = c.replace(marker2, replacement2)
    print('已添加第5章下方divider')
else:
    print('未找到marker2')

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('完成')

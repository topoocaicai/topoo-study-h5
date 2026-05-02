import re

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 紫色加深：#818cf8 → #6366f1, #a78bfa → #7c3aed, #c084fc → #8b5cf6
content = content.replace('#818cf8', '#6366f1')
content = content.replace('#a78bfa', '#7c3aed')
content = content.replace('#c084fc', '#8b5cf6')
content = content.replace('#7c3aed', '#6d28d9')  # highlight text
content = content.replace('#6d28d9', '#5b21b6')  # even deeper for highlight

# 2. 浅紫背景也深一点
content = content.replace('#f5f3ff', '#ede9fe')
content = content.replace('#ede9fe 100%', '#ddd6fe 100%')
content = content.replace('#eef2ff', '#e0e7ff')
content = content.replace('#e0e7ff', '#ddd6fe')

# 3. 删除对比图HTML（从 <!-- 对比图 --> 到 compare-note）
content = re.sub(
    r'    <!-- 对比图 -->.*?看出来区别了吗\？甲方也看不出来\。</p>\n',
    '', content, flags=re.DOTALL
)

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('done')

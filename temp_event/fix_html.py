import re

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 红色改紫色
content = content.replace('#e63946', '#7B2D8E')

# 2. 浅红背景改浅紫
content = content.replace('#fef5f5', '#f9f4fb')
content = content.replace('#fff8f0', '#f9f4fb')

# 3. 口号加"世界"
content = content.replace('被看见', '被世界看见')

# 4. 删除南京打样相关
content = content.replace('拓圈现在在南京打样第一年', '拓圈首批种子名额开放中')
content = content.replace('拓圈南京打样期', '拓圈')

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('done')

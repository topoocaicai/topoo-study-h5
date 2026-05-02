with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 紫色改鲜亮荧光紫
content = content.replace('#7B2D8E', '#A855F7')

# 2. 浅紫背景也调亮一点
content = content.replace('#f9f4fb', '#faf5ff')

# 3. 免会员费改文案
content = content.replace('终身免会员费', '免会员费，解锁更多培训与活动')

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('done')

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 高级蓝紫渐变紫
content = content.replace('#A855F7', '#8B5CF6')

# 浅紫背景也调
content = content.replace('#faf5ff', '#f5f3ff')

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('done')

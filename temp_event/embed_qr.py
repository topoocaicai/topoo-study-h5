import base64

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\weixin-img-1ef06971a45c11a3.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<img src="weixin-img-1ef06971a45c11a3.jpg">'
new = '<img src="data:image/jpeg;base64,' + b64 + '">'
content = content.replace(old, new)

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_image.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('done')

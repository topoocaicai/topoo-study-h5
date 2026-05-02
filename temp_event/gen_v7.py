import base64
from html2image import Html2Image
from PIL import Image

# 读取二维码并转base64
with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\weixin-img-1ef06971a45c11a3.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

# 嵌入HTML
with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_v7.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<span style="color:#ccc;font-size:12px;">二维码加载中...</span>',
    '<img src="data:image/jpeg;base64,' + b64 + '" style="width:140px;height:140px;">'
)

with open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_v7.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 截图
hti = Html2Image(
    output_path=r'c:\Users\Administrator\WorkBuddy\Claw\temp_event',
    browser_executable=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
)
hti.screenshot(
    html_file=r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_article_v7.html',
    save_as='topoo_v7.png',
    size=(750, 5000)
)

# 裁剪空白
img = Image.open(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_v7.png')
w, h = img.size
for y in range(h-1, -1, -1):
    for x in range(0, w, 3):
        r, g, b = img.getpixel((x, y))
        if r < 240 or g < 240 or b < 240:
            cropped = img.crop((0, 0, w, y+20))
            cropped.save(r'c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_v7_final.png')
            print(f'final: {cropped.size}')
            print('done')
            exit()

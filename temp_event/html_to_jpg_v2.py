"""
从桌面HTML提取纯净内容，生成干净版本，截图为高质量JPG
"""
import os
import re
import base64
from PIL import Image

# 读取桌面上的HTML
html_path = r"C:\Users\Administrator\Desktop\拓圈 · 公众号推文长图.html"
output_dir = r"c:\Users\Administrator\WorkBuddy\Claw\temp_event"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 提取container内的HTML（去掉浏览器注入的CSS和script）
# 找到 <div class="container"> 到 </div> 的内容
match = re.search(r'<div class="container">(.*?)</div>\s*</body>', content, re.DOTALL)
if match:
    body_content = match.group(1)
else:
    body_content = content

# 提取二维码的base64数据
qr_match = re.search(r'<img src="(data:image/[^"]+)"', content)
qr_base64 = qr_match.group(1) if qr_match else ""

# 替换二维码占位
if qr_base64:
    body_content = body_content.replace(
        '<img src=""',
        f'<img src="{qr_base64}"'
    )
    body_content = body_content.replace(
        '<img alt="',
        f'<img src="{qr_base64}" alt="'
    )

# 找到原始的img src（可能是完整的base64）
img_src_match = re.search(r'<img\s+src="([^"]{50,})"', content)
if img_src_match and qr_base64:
    img_real_src = img_src_match.group(1)
    # 确保所有img标签都有正确的src
    body_content = re.sub(
        r'<img\s+src=""',
        f'<img src="{img_real_src}"',
        body_content
    )

# 构建干净的HTML
clean_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>拓圈 · 公众号推文长图</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  background: #F5F5F5;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  color: #1a1a1a;
  line-height: 1.8;
}}

.container {{
  max-width: 680px;
  margin: 0 auto;
  background: #ffffff;
  min-height: 100vh;
}}

/* 封面区 */
.cover {{
  background: #0a0a0a;
  padding: 80px 40px 60px;
  text-align: center;
  position: relative;
  overflow: hidden;
}}

.cover::before {{
  content: '';
  position: absolute;
  left: 40px;
  top: 40px;
  bottom: 40px;
  width: 3px;
  background: linear-gradient(180deg, #6366f1, #5b21b6, #8b5cf6);
}}

.cover-subtitle {{
  font-size: 13px;
  color: #888;
  letter-spacing: 6px;
  text-transform: uppercase;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
}}

.cover h1 {{
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.5;
  letter-spacing: 1px;
  position: relative;
  z-index: 1;
}}

.cover-tag {{
  display: inline-block;
  margin-top: 40px;
  padding: 6px 20px;
  border: 1px solid #444;
  border-radius: 20px;
  font-size: 12px;
  color: #888;
  letter-spacing: 3px;
  position: relative;
  z-index: 1;
}}

/* 正文区 */
.content {{
  padding: 50px 40px;
}}

/* 开头场景 */
.scene {{
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  border-left: 3px solid;
  border-image: linear-gradient(180deg, #6366f1, #5b21b6) 1;
  padding: 24px 28px;
  margin-bottom: 40px;
  font-size: 15px;
  color: #444;
  line-height: 2;
  border-radius: 0 8px 8px 0;
}}

.scene em {{
  color: #5b21b6;
  font-style: normal;
  font-weight: 600;
}}

/* 章节标题 */
.section-title {{
  font-size: 20px;
  font-weight: 700;
  color: #1e1b4b;
  margin: 50px 0 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid transparent;
  border-image: linear-gradient(90deg, #6366f1, #5b21b6, transparent) 1;
}}

.section-title:first-of-type {{
  margin-top: 0;
}}

/* 段落 */
p {{
  font-size: 15.5px;
  color: #333;
  margin-bottom: 18px;
  line-height: 2;
}}

p strong {{
  color: #1e1b4b;
  font-weight: 600;
}}

.highlight {{
  font-size: 17px;
  font-weight: 700;
  color: #5b21b6;
  text-align: center;
  margin: 36px 0;
  padding: 20px;
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  border-radius: 10px;
  border: 1px solid rgba(139, 92, 246, 0.15);
}}

/* 三条路 */
.road {{
  padding: 20px 24px;
  margin-bottom: 16px;
  background: #fafafa;
  border-radius: 10px;
  border: 1px solid #f0f0f0;
}}

.road-num {{
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background: linear-gradient(135deg, #4f46e5, #5b21b6);
  color: #fff;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  margin-right: 10px;
  vertical-align: middle;
}}

.road-title {{
  font-weight: 700;
  font-size: 15.5px;
  color: #1e1b4b;
  margin-bottom: 8px;
}}

.road-desc {{
  font-size: 14.5px;
  color: #555;
  line-height: 1.9;
}}

.road.active {{
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  border-color: rgba(139, 92, 246, 0.3);
}}

/* 拓圈区块 */
.brand-block {{
  background: #0a0a0a;
  border-radius: 14px;
  padding: 36px 30px;
  margin: 40px 0;
  color: #fff;
  position: relative;
  overflow: hidden;
}}

.brand-block::before {{
  content: '';
  position: absolute;
  left: 30px;
  top: 30px;
  bottom: 30px;
  width: 3px;
  background: linear-gradient(180deg, #6366f1, #5b21b6, #8b5cf6);
}}

.brand-block .brand-name {{
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  position: relative;
  z-index: 1;
}}

.brand-block .brand-desc {{
  font-size: 14.5px;
  color: #888;
  margin-bottom: 28px;
  position: relative;
  z-index: 1;
}}

.brand-block .brand-what {{
  font-size: 16px;
  color: #fff;
  font-weight: 600;
  line-height: 1.8;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #333;
  position: relative;
  z-index: 1;
}}

.brand-path {{
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}}

.brand-path-tag {{
  display: inline-block;
  padding: 3px 14px;
  background: linear-gradient(135deg, #6366f1, #5b21b6);
  border-radius: 4px;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 10px;
}}

.brand-path p {{
  font-size: 14.5px;
  color: #ccc;
  line-height: 1.9;
  margin-bottom: 0;
}}

/* 种子期 */
.seed-block {{
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  border-radius: 10px;
  padding: 28px 24px;
  margin: 40px 0;
  border: 1px solid rgba(139, 92, 246, 0.12);
}}

.seed-block .seed-title {{
  font-size: 16px;
  font-weight: 700;
  color: #1e1b4b;
  margin-bottom: 16px;
}}

.seed-list {{
  list-style: none;
  padding: 0;
}}

.seed-list li {{
  font-size: 14.5px;
  color: #555;
  padding: 8px 0;
  padding-left: 20px;
  position: relative;
}}

.seed-list li::before {{
  content: '▸';
  position: absolute;
  left: 0;
  color: #5b21b6;
  font-weight: 700;
}}

.seed-note {{
  font-size: 14px;
  color: #888;
  margin-top: 16px;
  font-style: italic;
}}

/* 结尾金句 */
.ending {{
  text-align: center;
  margin: 50px 0 40px;
  padding: 40px 20px;
}}

.ending p {{
  font-size: 16px;
  color: #333;
  line-height: 2.2;
  margin-bottom: 12px;
}}

.ending .big-quote {{
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #4f46e5, #5b21b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 24px 0;
  line-height: 1.6;
}}

/* CTA区 */
.cta {{
  background: #0a0a0a;
  border-radius: 14px;
  padding: 36px 30px;
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}}

.cta::before {{
  content: '';
  position: absolute;
  left: 30px;
  top: 30px;
  bottom: 30px;
  width: 3px;
  background: linear-gradient(180deg, #6366f1, #5b21b6, #8b5cf6);
}}

.cta .cta-badge {{
  display: inline-block;
  padding: 5px 16px;
  background: linear-gradient(135deg, #6366f1, #5b21b6);
  border-radius: 20px;
  font-size: 12px;
  color: #fff;
  font-weight: 700;
  letter-spacing: 2px;
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}}

.cta .cta-text {{
  font-size: 15px;
  color: #ccc;
  margin-bottom: 24px;
  line-height: 1.8;
  position: relative;
  z-index: 1;
}}

.cta .qr-placeholder {{
  width: 160px;
  height: 160px;
  background: #fff;
  border-radius: 10px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}}

.cta .qr-placeholder img {{
  width: 140px;
  height: 140px;
  display: block;
}}

.cta .cta-note {{
  font-size: 13px;
  color: #888;
  position: relative;
  z-index: 1;
}}

/* 页脚 */
.footer {{
  text-align: center;
  padding: 30px 40px 40px;
  border-top: 1px solid #f0f0f0;
}}

.footer p {{
  font-size: 12px;
  color: #bbb;
  letter-spacing: 4px;
}}

/* 分隔线 */
.divider {{
  text-align: center;
  color: #ddd;
  margin: 40px 0;
  letter-spacing: 8px;
  font-size: 14px;
}}
</style>
</head>
<body>
<div class="container">
{body_content}
</div>
</body>
</html>'''

clean_html_path = os.path.join(output_dir, "topoo_clean.html")
with open(clean_html_path, "w", encoding="utf-8") as f:
    f.write(clean_html)

print(f"干净版HTML已生成: {clean_html_path}")
print(f"HTML大小: {os.path.getsize(clean_html_path) / 1024:.1f} KB")

# 然后用html2image截图
from html2image import Html2Image

hti = Html2Image(browser="edge", output_path=output_dir)
hti.screenshot(
    html_str=clean_html,
    size=(680, 1),
    save_as="topoo_clean_shot.png"
)

temp_png = os.path.join(output_dir, "topoo_clean_shot.png")
if os.path.exists(temp_png):
    img = Image.open(temp_png)
    
    # 裁剪底部空白
    width, height = img.size
    img_rgb = img.convert("RGB")
    pixels = img_rgb.load()
    
    crop_bottom = height
    for y in range(height - 1, -1, -1):
        row_has_content = False
        for x in range(0, width, 2):
            r, g, b = pixels[x, y]
            if r < 245 or g < 245 or b < 245:
                row_has_content = True
                break
        if row_has_content:
            crop_bottom = y + 10
            break
    
    img = img.crop((0, 0, width, min(crop_bottom, height)))
    
    # 保存高质量JPG到桌面
    jpg_path = r"C:\Users\Administrator\Desktop\拓圈公众号推文长图.jpg"
    img.save(jpg_path, "JPEG", quality=95, optimize=True, subsampling=0)
    
    os.remove(temp_png)
    
    print(f"JPG已保存到桌面: {jpg_path}")
    print(f"尺寸: {img.size[0]}x{img.size[1]}")
    print(f"文件大小: {os.path.getsize(jpg_path) / 1024:.1f} KB")
else:
    print("截图失败")

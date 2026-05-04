from PIL import Image, ImageDraw, ImageFont
import math
import os

# ===== 画布设定 =====
W, H = 1080, 1440
img = Image.new('RGB', (W, H), '#F5F0E8')
draw = ImageDraw.Draw(img)

# ===== 字体路径 =====
# 尝试多个中文字体，按优先级
font_paths = [
    'C:/Windows/Fonts/STKAITI.TTF',   # 楷体 - 书法感
    'C:/Windows/Fonts/msyh.ttc',       # 微软雅黑
    'C:/Windows/Fonts/simsun.ttc',     # 宋体
    'C:/Windows/Fonts/simhei.ttf',     # 黑体
]
def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_brand = load_font(font_paths[0], 20)
font_title = load_font(font_paths[0], 96)
font_sub = load_font(font_paths[1], 28)
font_label = load_font(font_paths[1], 15)
font_price_big = load_font(font_paths[0], 56)
font_price_sm = load_font(font_paths[1], 18)
font_card_title = load_font(font_paths[0], 20)
font_card_en = load_font(font_paths[1], 13)
font_highlight = load_font(font_paths[0], 36)
font_cta = load_font(font_paths[1], 14)
font_tagline = load_font(font_paths[1], 13)

# ===== 1. 宣纸纹理背景 =====
# 用噪声点模拟宣纸纹理
import random
random.seed(42)
texture = Image.new('RGBA', (W, H), (0,0,0,0))
td = ImageDraw.Draw(texture)
for _ in range(18000):
    x = random.randint(0, W-1)
    y = random.randint(0, H-1)
    a = random.randint(8, 30)
    r = random.choice([139, 69, 19, 212, 168, 75, 46, 92, 58])
    g = random.choice([69, 19, 19, 168, 19, 58])
    b = random.choice([19, 19, 19, 75, 19, 58])
    td.point((x, y), (r, g, b, a))
img = Image.alpha_composite(img.convert('RGBA'), texture)
img = img.convert('RGB')
draw = ImageDraw.Draw(img)

# ===== 2. 顶部赭石色块 =====
# 主色块
for i in range(320):
    r = int(139 + (205-139) * i / 319)
    g = int(69  + (134-69)  * i / 319)
    b = int(19  + (106-19)  * i / 319)
    draw.rectangle([(0, i), (W, i+1)], fill=(r, g, b))

# 顶部渐变过渡（到底部）
for i in range(320, 420):
    ratio = (i - 320) / 100.0
    r = int(205 + (245-205) * ratio)
    g = int(134 + (240-134) * ratio)
    b = int(106 + (232-106) * ratio)
    draw.rectangle([(0, i), (W, i+1)], fill=(r, g, b))

# ===== 3. 城墙纹理装饰线（顶部色块底部）=====
brick_w = 108
for x in range(0, W, brick_w):
    offset = 0 if (x // brick_w) % 2 == 0 else brick_w // 2
    for y in range(300, 340, 20):
        sx = x + offset
        draw.rectangle([(sx, y), (sx + brick_w - 4, y + 16)], 
                      fill=(139, 69, 19, 80))

# ===== 4. 主标题区 =====
# 品牌名
draw.text((60, 55), 'TOPOO  STUDY  TOUR', font=font_brand, 
          fill=(245, 240, 232, 180))
# 主标题
draw.text((58, 90), '拓圈研学', font=font_title, fill='#F5F0E8')
# 副标题
draw.text((62, 208), '国内中小学生 · 南京古都文脉探索营', font=font_sub, 
          fill=(245, 240, 232, 220))

# ===== 5. 分隔装饰线 =====
draw.line([(60, 370), (W-60, 370)], fill=(139, 69, 19, 60), width=1)
draw.line([(60, 372), (W-60, 372)], fill=(139, 69, 19, 30), width=1)

# ===== 6. 核心亮点卡片区 =====
cards = [
    ('🏯', '明城墙徒步', 'City Wall Hike', 380),
    ('✍️', '书法工坊', 'Calligraphy', 380),
    ('🏛️', '科举博物馆', 'Exam Museum', 380),
    ('🎭', '非遗传承', 'ICH Experience', 540),
    ('🌳', '中山陵·紫金山', 'Purple Mountain', 540),
    ('📖', '南京大学参访', 'NJU Visit', 540),
]

card_w = (W - 120 - 30) // 3  # 3列，间距15
card_h = 130
for i, (icon, title, en, y_base) in enumerate(cards):
    col = i % 3
    row = i // 3
    x = 60 + col * (card_w + 15)
    y = y_base + row * (card_h + 15)
    
    # 卡片阴影
    draw.rounded_rectangle([(x+2, y+2), (x+card_w+2, y+card_h+2)], 
                          radius=12, fill=(200, 190, 170))
    # 卡片本体
    draw.rounded_rectangle([(x, y), (x+card_w, y+card_h)], 
                          radius=12, fill='white')
    # 细边框
    draw.rounded_rectangle([(x, y), (x+card_w, y+card_h)], 
                          radius=12, outline=(139,69,19,40), width=1)
    # 图标
    draw.text((x + 18, y + 18), icon, font=load_font(font_paths[1], 30), fill='#333')
    # 中文标题
    draw.text((x + 18, y + 58), title, font=font_card_title, fill='#333')
    # 英文
    draw.text((x + 18, y + 85), en, font=font_card_en, fill='#999')

# ===== 7. 价格展示区（深翠绿渐变）=====
price_y = 730
# 背景圆角矩形
draw.rounded_rectangle([(60, price_y), (W-60, price_y+200)], 
                        radius=16, fill=(46, 92, 58))
# 渐变叠加
for i in range(200):
    r = int(46 + (58-46) * i / 199)
    g = int(92 + (120-92) * i / 199)
    b = int(58 + (78-58) * i / 199)
    draw.line([(60, price_y+i), (W-60, price_y+i)], fill=(r,g,b))

# 价格标题
draw.text((W//2, price_y + 24), '—  PROGRAM FEE  —', 
          font=font_label, fill=(245,240,232,150), anchor='mm')
# 分隔线
draw.line([(120, price_y+50), (W-120, price_y+50)], 
          fill=(245,240,232,60), width=1)

# 两档价格
price_data = [
    ('4日3晚', '4Days3Nights', '5,980'),
    ('5日4晚', '5Days4Nights', '7,980'),
]
sep_x = W // 2
for i, (dur, dur_en, price) in enumerate(price_data):
    cx = 60 + (W-120) * (i*2+1) // 4
    # 天数
    draw.text((cx, price_y+62), dur, font=font_cta, 
              fill=(245,240,232,170), anchor='mm')
    # 价格
    draw.text((cx, price_y+105), f'¥{price}', font=font_price_big, 
              fill='#F5F0E8', anchor='mm')
    # 单位
    draw.text((cx, price_y+155), '/人 · per person', font=font_price_sm, 
              fill=(245,240,232,170), anchor='mm')
    # 分隔（仅第一个后加竖线）
    if i == 0:
        draw.line([(sep_x, price_y+55), (sep_x, price_y+180)], 
                  fill=(245,240,232,40), width=1)

# 底部说明
draw.text((W//2, price_y+185), '费用透明 · 一价全包 · 无额外收费', 
          font=font_cta, fill=(245,240,232,120), anchor='mm')

# ===== 8. 装饰元素 =====
# 右上角大圆点
for r in range(90, 20, -1):
    alpha = int(12 * (1 - (r-20)/70))
    draw.ellipse([(W-100-r, 350-r), (W-100+r, 350+r)], 
                  fill=(212, 168, 75, alpha))
# 左下角深翠圆点
for r in range(60, 10, -1):
    alpha = int(10 * (1 - (r-10)/50))
    draw.ellipse([(40-r, H-300-r), (40+r, H-300+r)], 
                  fill=(46, 92, 58, alpha))

# ===== 9. 底部CTA区 =====
cta_y = H - 160
# 分隔线
draw.line([(60, cta_y), (W-60, cta_y)], fill=(139,69,19,30), width=1)
# URL
url = 'topoocaicai.github.io/topoo-study-h5/study-domestic-k12-entry.html'
draw.text((W//2, cta_y+30), url, font=font_cta, 
          fill=(139,69,19,180), anchor='mm')
# 标语
draw.text((W//2, cta_y+60), '让小而美被世界看见  ·  TOPOO', 
          font=font_tagline, fill=(139,69,19,120), anchor='mm')

# ===== 10. 角落印章风格装饰 =====
# 左上角小印章感
draw.rounded_rectangle([(W-140, H-140), (W-60, H-60)], 
                        radius=4, outline=(139,69,19,40), width=1)
draw.text((W-100, H-100), '拓圈\n研学', font=load_font(font_paths[0], 16), 
          fill=(139,69,19,60), anchor='mm')

# ===== 保存 =====
out = 'C:/Users/Administrator/WorkBuddy/Claw/拓圈研学-国内中小学-海报.png'
img.save(out, 'PNG')
print(f'海报已生成：{out}')
print(f'尺寸：{W}x{H}px')

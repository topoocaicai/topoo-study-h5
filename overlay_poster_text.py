#!/usr/bin/env python3
"""
拓圈研学海报 - 文字叠加脚本
在即梦生成的底图上叠加文字信息
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# ===== 配置 =====
BASE_IMAGE = "C:/Users/Administrator/Desktop/jimeng-2026-05-02-6143-竖版插画海报，暖白色宣纸质感底色#F5F0E8，画面中央是一个从画面底部长出来的....png"
QR_CODE = "C:/Users/Administrator/WorkBuddy/Claw/qr-codes/qr-国内中小学.png"
OUTPUT = "C:/Users/Administrator/WorkBuddy/Claw/拓圈研学-国内中小学-海报-最终版.png"

# 画布尺寸（按即梦图的实际尺寸）
W, H = 1080, 1920  # 即梦竖版通常是 9:16

# 品牌色
COLORS = {
    'warm_white': '#F5F0E8',
    'rust_red': '#D96B6B',      # 火/门店
    'peacock_blue': '#4A9EB8',  # 水/内容
    'matcha_green': '#A0B87A',  # 木/产品
    'amber_gold': '#E8B44C',    # 金/服务
    'dusty_purple': '#9B7BBF',  # 土/活动
    'earth_brown': '#8B7E6A',   # 部落
    'deep_brown': '#5C4033',
    'ink_black': '#2C2C2C',
}

# ===== 字体加载 =====
def load_font(size, prefer_script=False):
    """加载字体，优先书法感字体"""
    font_paths = [
        'C:/Windows/Fonts/STKAITI.TTF',   # 楷体 - 书法感
        'C:/Windows/Fonts/STXINGKA.TTF',  # 行楷
        'C:/Windows/Fonts/msyh.ttc',       # 微软雅黑
        'C:/Windows/Fonts/simsun.ttc',     # 宋体
    ]
    
    if prefer_script:
        font_paths = ['C:/Windows/Fonts/STXINGKA.TTF', 'C:/Windows/Fonts/STKAITI.TTF'] + font_paths[2:]
    
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

# ===== 辅助函数 =====
def add_text_with_shadow(draw, text, pos, font, fill, shadow_color=(0,0,0,80), offset=2):
    """添加带阴影的文字"""
    x, y = pos
    # 阴影
    draw.text((x+offset, y+offset), text, font=font, fill=shadow_color)
    # 主文字
    draw.text((x, y), text, font=font, fill=fill)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    # 主体矩形
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
    # 四个圆角
    draw.ellipse([x1, y1, x1+radius*2, y1+radius*2], fill=fill)
    draw.ellipse([x2-radius*2, y1, x2, y1+radius*2], fill=fill)
    draw.ellipse([x1, y2-radius*2, x1+radius*2, y2], fill=fill)
    draw.ellipse([x2-radius*2, y2-radius*2, x2, y2], fill=fill)
    
    if outline:
        # 绘制边框线
        draw.arc([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=outline, width=width)
        draw.arc([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+radius, y1, x2-radius, y1], fill=outline, width=width)
        draw.line([x1+radius, y2, x2-radius, y2], fill=outline, width=width)
        draw.line([x1, y1+radius, x1, y2-radius], fill=outline, width=width)
        draw.line([x2, y1+radius, x2, y2-radius], fill=outline, width=width)

# ===== 主程序 =====
def main():
    # 1. 加载底图
    print("加载即梦底图...")
    img = Image.open(BASE_IMAGE).convert('RGBA')
    
    # 调整尺寸到标准海报尺寸
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    
    # 创建绘图层
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_title_main = load_font(72, prefer_script=True)  # 拓圈研学营
    font_title_sub = load_font(36)   # 南京·古都文脉探索
    font_brand = load_font(24)       # TOPOO
    font_highlight = load_font(28)   # 亮点文字
    font_mode = load_font(24)        # 模式标注
    font_small = load_font(18)       # 小字
    font_slogan = load_font(20)      # 标语
    
    # ===== 2. 顶部品牌区 =====
    # TOPOO 品牌名（左上角）
    draw.text((50, 40), "TOPOO", font=font_brand, fill=COLORS['ink_black'])
    draw.text((50, 70), "STUDY TOUR", font=font_small, fill=COLORS['earth_brown'])
    
    # ===== 3. 主标题区（画面上方，给插画留空间） =====
    title_y = 140
    
    # 主标题背景装饰 - 淡色块
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([30, title_y-20, W-30, title_y+120], 
                                    radius=15, fill=(245, 240, 232, 180))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # 主标题
    draw.text((W//2, title_y+10), "拓圈研学营", font=font_title_main, 
              fill=COLORS['ink_black'], anchor='mm')
    
    # 副标题
    draw.text((W//2, title_y+85), "南京 · 古都文脉探索", font=font_title_sub, 
              fill=COLORS['deep_brown'], anchor='mm')
    
    # ===== 4. 亮点区（画面右侧单列布局，避开左侧笔记本电脑） =====
    # 亮点从 y=1150 开始，放在画面右侧，完全避开鸡鸣寺和城墙
    highlight_y = 1150
    
    # 亮点标题（右侧对齐，往上移避开鸡鸣寺）
    draw.text((W-80, highlight_y-15), "探索亮点", font=font_highlight, 
              fill=COLORS['ink_black'], anchor='rm')
    draw.text((W-80, highlight_y+20), "HIGHLIGHTS", font=font_small, 
              fill=COLORS['earth_brown'], anchor='rm')
    
    # 6个亮点 - 右侧单列布局
    highlights = [
        ("🏯", "明城墙探秘", "City Wall"),
        ("✍️", "书法大师工坊", "Calligraphy"),
        ("📜", "科举博物馆", "Museum"),
        ("🎨", "非遗手作体验", "Handcraft"),
        ("🌳", "中山陵紫金山", "Mountain"),
        ("🎓", "南京大学参访", "NJU Visit"),
    ]
    
    card_w = 380
    card_h = 60
    start_x = W - card_w - 40  # 右对齐，留40边距，更靠右避开城墙
    
    for i, (icon, title, en) in enumerate(highlights):
        y = highlight_y + 70 + i * (card_h + 10)
        x = start_x
        
        # 卡片背景（更强的白色背景确保可读性）
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle([x, y, x+card_w, y+card_h], 
                                        radius=10, fill=(255, 255, 255, 230))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # 图标
        draw.text((x+15, y+18), icon, font=load_font(26), fill=COLORS['ink_black'])
        # 中文标题
        draw.text((x+50, y+15), title, font=font_mode, fill=COLORS['ink_black'])
        # 英文
        draw.text((x+50, y+42), en, font=font_small, fill=COLORS['earth_brown'])
    
    # ===== 5. 两种模式标注 =====
    mode_y = highlight_y + 70 + 6 * (60 + 10) + 30
    
    # 模式说明背景
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([80, mode_y, W-80, mode_y+60], 
                                    radius=30, fill=(212, 168, 75, 60))  # 琥珀金半透明
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    draw.text((W//2, mode_y+18), "两种研学模式可选", font=font_mode, 
              fill=COLORS['deep_brown'], anchor='mm')
    draw.text((W//2, mode_y+42), "4日精华版  ·  5日深度版", font=font_small, 
              fill=COLORS['earth_brown'], anchor='mm')
    
    # ===== 6. 二维码区 =====
    qr_y = mode_y + 90
    
    # 加载二维码
    if os.path.exists(QR_CODE):
        qr_img = Image.open(QR_CODE).convert('RGBA')
        qr_size = 140
        qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
        
        # 二维码背景白底
        qr_bg = Image.new('RGBA', (qr_size+20, qr_size+20), (255, 255, 255, 230))
        qr_bg.paste(qr_img, (10, 10), qr_img)
        
        # 粘贴到主图
        qr_x = (W - qr_size - 20) // 2
        img.paste(qr_bg, (qr_x, qr_y), qr_bg)
        
        # 扫码提示
        draw.text((W//2, qr_y+qr_size+35), "扫码了解详情", font=font_small, 
                  fill=COLORS['ink_black'], anchor='mm')
    
    # ===== 7. 底部品牌标语 =====
    slogan_y = H - 80
    
    # 分隔线
    draw.line([(100, slogan_y), (W-100, slogan_y)], fill=COLORS['earth_brown'], width=1)
    
    # 标语
    draw.text((W//2, slogan_y+25), "让小而美被世界看见", font=font_slogan, 
              fill=COLORS['deep_brown'], anchor='mm')
    draw.text((W//2, slogan_y+50), "TOPOO · 拓圈研学", font=font_small, 
              fill=COLORS['earth_brown'], anchor='mm')
    
    # ===== 8. 角落装饰 =====
    # 右下角小印章风格
    seal_size = 60
    seal_x = W - seal_size - 30
    seal_y = H - seal_size - 100
    
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([seal_x, seal_y, seal_x+seal_size, seal_y+seal_size], 
                           outline=(139, 69, 19, 100), width=2)
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    font_seal = load_font(14)
    draw.text((seal_x+seal_size//2, seal_y+20), "拓圈", font=font_seal, 
              fill=COLORS['rust_red'], anchor='mm')
    draw.text((seal_x+seal_size//2, seal_y+40), "研学", font=font_seal, 
              fill=COLORS['rust_red'], anchor='mm')
    
    # ===== 保存 =====
    # 转换为RGB保存
    final_img = img.convert('RGB')
    final_img.save(OUTPUT, 'PNG', quality=95)
    print(f"✅ 海报已生成：{OUTPUT}")
    print(f"📐 尺寸：{W}x{H}px")
    
    return OUTPUT

if __name__ == '__main__':
    main()

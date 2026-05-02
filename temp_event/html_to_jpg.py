import os
from html2image import Html2Image
from PIL import Image
import io

# 源文件
html_path = r"C:\Users\Administrator\Desktop\拓圈 · 公众号推文长图.html"
output_dir = r"c:\Users\Administrator\WorkBuddy\Claw\temp_event"
output_path = os.path.join(output_dir, "topoo_long_image.jpg")

# 初始化，用Edge浏览器
hti = Html2Image(browser="edge", output_path=output_dir)

# 先截图为PNG（无损），再转高质量JPG
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# 截图，使用较高DPI
hti.screenshot(
    html_str=html_content,
    size=(680, 1),  # 宽度680，高度自动
    save_as="temp_shot.png"
)

temp_png = os.path.join(output_dir, "temp_shot.png")

if os.path.exists(temp_png):
    # 用PIL打开PNG，裁剪空白，转高质量JPG
    img = Image.open(temp_png)
    
    # 裁剪底部空白区域（检测最后一行非白色像素）
    width, height = img.size
    # 把图片转为RGB检查
    img_rgb = img.convert("RGB")
    pixels = img_rgb.load()
    
    # 从底部往上找第一个非白色行
    crop_bottom = height
    for y in range(height - 1, -1, -1):
        row_has_content = False
        for x in range(0, width, 2):  # 每隔2像素检查，加速
            r, g, b = pixels[x, y]
            if r < 245 or g < 245 or b < 245:
                row_has_content = True
                break
        if row_has_content:
            crop_bottom = y + 10  # 留一点底部边距
            break
    
    img = img.crop((0, 0, width, min(crop_bottom, height)))
    
    # 保存为高质量JPG
    img.save(output_path, "JPEG", quality=95, optimize=True, subsampling=0)
    
    # 删除临时PNG
    os.remove(temp_png)
    
    print(f"JPG已保存: {output_path}")
    print(f"尺寸: {img.size[0]}x{img.size[1]}")
    file_size = os.path.getsize(output_path)
    print(f"文件大小: {file_size / 1024:.1f} KB")
else:
    print("截图失败，未生成临时PNG")

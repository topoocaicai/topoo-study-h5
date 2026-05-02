"""
将已有的PNG长图转换为高质量JPG，保存到桌面
"""
from PIL import Image
import os

# 源PNG
src_png = r"c:\Users\Administrator\WorkBuddy\Claw\temp_event\topoo_v7_final.png"
# 输出JPG到桌面
dst_jpg = r"C:\Users\Administrator\Desktop\拓圈公众号推文长图.jpg"

if os.path.exists(src_png):
    img = Image.open(src_png)
    print(f"原始尺寸: {img.size[0]}x{img.size[1]}")
    print(f"原始模式: {img.mode}")
    
    # 确保RGB模式（JPG不支持透明通道）
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    # 保存高质量JPG
    img.save(dst_jpg, "JPEG", quality=95, optimize=True, subsampling=0)
    
    file_size = os.path.getsize(dst_jpg)
    print(f"JPG已保存: {dst_jpg}")
    print(f"文件大小: {file_size / 1024:.1f} KB")
else:
    print(f"源文件不存在: {src_png}")

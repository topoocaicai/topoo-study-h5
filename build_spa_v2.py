#!/usr/bin/env python3
"""
TopSpace SPA 合并脚本 v2
将多个独立H5文件合并为一个SPA单页应用
用BeautifulSoup解析HTML，精准处理CSS命名空间
"""
import re, sys, os

FILES = {
    'collision':  r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·碰撞·H5.html',
    'philosophy': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·碰撞·Topoo哲学·H5.html',
    'story':      r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·故事·H5.html',
    'script':     r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·故事·新手剧本·H5.html',
    'plaza':     r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·广场·H5.html',
    'map':        r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·街区地图·矩形Block版v15·H5.html',
    'profile':    r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·我的·页面·H5.html',
}
OUTPUT = r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·全功能·H5.html'

# 全局共享样式（SPA框架）
SPA_FRAME_CSS = """
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #1a1816;
            font-family: -apple-system, "PingFang SC", "Helvetica Neue", sans-serif;
            overflow: hidden; height: 100vh; width: 100vw;
            -webkit-user-select: none; user-select: none;
        }
        .spa-container {
            position: relative; width: 375px; height: 812px;
            margin: 20px auto; border-radius: 44px;
            background: #1a1816;
            box-shadow: 0 0 0 2px #C8C0B4, 0 0 0 6px #1a1816, 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        .phone-notch {
            position: absolute; top:0; left:50%; transform: translateX(-50%);
            width:150px; height:30px; background: #2C2824;
            border-radius: 0 0 18px 18px; z-index: 200;
        }
        .phone-notch::before {
            content:''; position:absolute; top:10px; left:50%; transform:translateX(-50%);
            width:60px; height:6px; background:#3C3834; border-radius:3px;
        }
        .spa-page {
            position: absolute; top:0; left:0; right:0; bottom:0;
            display: none; overflow: hidden;
        }
        .spa-page.active { display: block; }
        .spa-subpage {
            position: absolute; top:0; left:0; right:0; bottom:0;
            display: none; z-index: 80;
            background: inherit;
        }
        .spa-subpage.active { display: block; }
        .spa-bottom-tab {
            position: absolute; bottom:0; left:0; right:0;
            height: 80px;
            background: rgba(245,240,232,0.95);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-top: 1px solid rgba(0,0,0,0.06);
            display: flex;
            align-items: flex-start;
            padding-top: 8px;
            z-index: 150;
            transition: opacity 0.3s;
        }
        .spa-bottom-tab.hidden { opacity:0; pointer-events:none; }
        .spa-tab-item {
            flex: 1; display: flex; flex-direction: column;
            align-items: center; gap: 3px; cursor: pointer;
        }
        .spa-tab-icon { font-size: 20px; }
        .spa-tab-label { font-size: 10px; color: #A8A098; }
        .spa-tab-item.active .spa-tab-label { color: #2C2824; font-weight: 600; }
        .spa-tab-item.active .spa-tab-icon { filter: none; }
        .spa-tab-item:not(.active) .spa-tab-icon { filter: grayscale(0.6) opacity(0.5); }
        .spa-back-btn {
            position: absolute; top: 44px; left: 16px; z-index: 200;
            width:32px; height:32px; border-radius:50%;
            background: rgba(0,0,0,0.04); border:1px solid rgba(0,0,0,0.06);
            display:flex; align-items:center; justify-content:center;
            font-size:18px; cursor:pointer; display:none;
        }
"""

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        try:
            with open(path, 'r', encoding='gbk') as f:
                return f.read()
        except Exception as e:
            print(f'  读取失败: {e}')
            return ''

def extract_css_html(content):
    """提取<style>标签内的CSS和<body>内的HTML"""
    # 移除 DOCTYPE, <html>, <head> 等
    # 提取所有 <style>...</style> 内容
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    css = '\n'.join(s.strip() for s in style_blocks)
    # 提取 <body>...</body> 内容
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        html = body_match.group(1)
    else:
        html = content
    return css, html

def namespace_css(css, prefix):
    """给CSS选择器加 #page-prefix 命名空间，精准处理"""
    # 逐行处理，追踪 @规则 嵌套深度
    lines = css.split('\n')
    result = []
    at_depth = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('//'):
            result.append(line)
            continue
        
        # 追踪花括号深度（处理@规则）
        at_depth += stripped.count('{') - stripped.count('}')
        
        # 如果在大括号外 且 是@规则开头（不在声明块内）
        if at_depth == 0 and stripped and stripped[0] == '@':
            result.append(line)
            # 计算这个@规则后的深度
            # 例如 @keyframes xxx {  => depth=1
            continue
        
        # 如果行内含有 { （选择器声明）
        if '{' in stripped and at_depth >= 0:
            # 在第一个 { 之前的选择器部分加前缀
            idx = stripped.find('{')
            if idx >= 0:
                sel_part = stripped[:idx]
                rest = stripped[idx:]
                # 处理逗号分隔的多个选择器
                selectors = [s.strip() for s in sel_part.split(',')]
                new_sels = []
                for sel in selectors:
                    sel = sel.strip()
                    if not sel:
                        continue
                    # 跳过 :root, body, html, * 等全局选择器（不加前缀）
                    if sel in ('body', 'html', '*', ':root'):
                        new_sels.append(sel)
                    elif sel.startswith('@'):
                        new_sels.append(sel)
                    else:
                        new_sels.append('#page-' + prefix + ' ' + sel)
                new_line = ', '.join(new_sels) + ' ' + rest
                result.append(line[:line.find(stripped)] + new_line)
                continue
        
        result.append(line)
    
    return '\n'.join(result)

def clean_html_for_spa(html, page_id, is_subpage=False):
    """清理HTML，适配SPA结构"""
    # 移除 phone-notch（SPA只有一个）
    html = re.sub(r'<div class="phone-notch"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="phone-notch"></div>', '', html)
    
    # 移除独立的 phone-shell（内容放进 #page-xx 容器内）
    html = re.sub(r'<div class="phone-shell"[^>]*>', '<div id="page-' + page_id + '" class="spa-page">', html, count=1)
    html = re.sub(r'</div>\s*</body>', '</div>', html)
    html = re.sub(r'</body>.*?</html>', '', html, flags=re.DOTALL)
    
    # 清理遗留下来的 </body></html> 等
    html = re.sub(r'</html>$', '', html)
    html = re.sub(r'</body>$', '', html)
    
    # 如果是子页面，添加 sp
    if is_subpage:
        html = html.replace('id="page-' + page_id + '" class="spa-page"', 
                       'id="page-' + page_id + '" class="spa-subpage"')
    
    return html.strip()

def build_spa():
    print('开始构建 TopSpace SPA...')
    
    # 读取所有文件
    pages = {}
    for key, path in FILES.items():
        if os.path.exists(path):
            print(f'  读取: {os.path.basename(path)[:40]}...')
            pages[key] = read_file(path)
        else:
            print(f'  ⚠ 不存在: {path}')
    
    # 构建CSS部分
    all_css = [SPA_FRAME_CSS]
    page_order = ['collision', 'philosophy', 'story', 'script', 'plaza', 'map', 'profile']
    page_titles = {
        'collision': '碰撞',
        'philosophy': 'Topoo哲学',
        'story': '故事',
        'script': '新手剧本',
        'plaza': '广场',
        'map': '星图',
        'profile': '我的',
    }
    
    for key in page_order:
        if key not in pages:
            continue
        css, _ = extract_css_html(pages[key])
        if css.strip():
            css_ns = namespace_css(css, key)
            all_css.append(f'\n/* ===== {page_titles.get(key, key)} ===== */\n' + css_ns)
    
    # 构建HTML部分
    all_html = []
    for key in page_order:
        if key not in pages:
            continue
        _, html = extract_css_html(pages[key])
        html_clean = clean_html_for_spa(html, key)
        all_html.append(f'\n<!-- ===== {page_titles.get(key, key)} ===== -->\n' + html_clean + '\n')
    
    # 构建底部Tab
    bottom_tab = """
        <div class="spa-bottom-tab" id="spaBottomTab">
            <div class="spa-tab-item" data-tab="map" onclick="switchTab('map')">
                <div class="spa-tab-icon">🗺️</div>
                <div class="spa-tab-label">星图</div>
            </div>
            <div class="spa-tab-item" data-tab="story" onclick="switchTab('story')">
                <div class="spa-tab-icon">📖</div>
                <div class="spa-tab-label">故事</div>
            </div>
            <div class="spa-tab-item active" data-tab="collision" onclick="switchTab('collision')">
                <div class="spa-tab-icon">⚡</div>
                <div class="spa-tab-label">碰撞</div>
            </div>
            <div class="spa-tab-item" data-tab="plaza" onclick="switchTab('plaza')">
                <div class="spa-tab-icon">🏘️</div>
                <div class="spa-tab-label">广场</div>
            </div>
            <div class="spa-tab-item" data-tab="profile" onclick="switchTab('profile')">
                <div class="spa-tab-icon">🪐</div>
                <div class="spa-tab-label">我的</div>
            </div>
        </div>
"""
    
    # 构建返回按钮（子页面用）
    back_btn = '<div class="spa-back-btn" id="spaBackBtn" onclick="goBack()">‹</div>'
    
    # 完整HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TopSpace · 全功能</title>
    <style>
{''.join(all_css)}
    </style>
</head>
<body>
    <div class="spa-container">
        <div class="phone-notch"></div>
        {back_btn}
        {''.join(all_html)}
        {bottom_tab}
    </div>
    
    <script>
        var currentTab = 'collision';
        var currentSubPage = null;
        
        // 初始化：显示默认Tab
        function initSPA() {
            document.getElementById('page-collision').classList.add('active');
            document.querySelector('.spa-tab-item[data-tab="collision"]').classList.add('active');
        }
        
        // 切换Tab
        function switchTab(tabName) {
            // 隐藏所有页面
            document.querySelectorAll('.spa-page').forEach(function(p) {{
                p.classList.remove('active');
            }});
            // 显示目标页面
            var target = document.getElementById('page-' + tabName);
            if (target) target.classList.add('active');
            // 更新Tab状态
            document.querySelectorAll('.spa-tab-item').forEach(function(t) {{
                t.classList.remove('active');
            }});
            var tabBtn = document.querySelector('.spa-tab-item[data-tab="' + tabName + '"]');
            if (tabBtn) tabBtn.classList.add('active');
            // 显示底部Tab，隐藏返回按钮
            document.getElementById('spaBottomTab').classList.remove('hidden');
            document.getElementById('spaBackBtn').style.display = 'none';
            currentTab = tabName;
            currentSubPage = null;
        }
        
        // 打开子页面
        function openSubPage(pageId) {
            // 隐藏所有页面
            document.querySelectorAll('.spa-page').forEach(function(p) {{
                p.classList.remove('active');
            }});
            // 显示子页面
            var target = document.getElementById(pageId);
            if (target) target.classList.add('active');
            // 隐藏底部Tab，显示返回按钮
            document.getElementById('spaBottomTab').classList.add('hidden');
            document.getElementById('spaBackBtn').style.display = 'flex';
            currentSubPage = pageId;
        }
        
        // 返回
        function goBack() {
            if (currentSubPage) {
                document.getElementById(currentSubPage).classList.remove('active');
                document.getElementById('page-' + currentTab).classList.add('active');
                document.getElementById('spaBottomTab').classList.remove('hidden');
                document.getElementById('spaBackBtn').style.display = 'none';
                currentSubPage = null;
            }
        }
        
        // Toast
        function showToast(msg) {
            var t = document.createElement('div');
            t.textContent = msg;
            Object.assign(t.style, {
                position: 'fixed', bottom: '100px', left: '50%', transform: 'translateX(-50%)',
                background: 'rgba(44,40,36,0.88)', color: '#F5F0E8', padding: '10px 20px',
                borderRadius: '20px', fontSize: '13px', zIndex: '999', whiteSpace: 'nowrap',
                boxShadow: '0 4px 16px rgba(0,0,0,0.15)', opacity: '0', transition: 'opacity 0.3s'
            });
            document.body.appendChild(t);
            requestAnimationFrame(function() {{ t.style.opacity = '1'; }});
            setTimeout(function() {{
                t.style.opacity = '0';
                setTimeout(function() {{ t.remove(); }}, 300);
            }}, 1800);
        }
        
        // 页面加载后初始化
        window.addEventListener('DOMContentLoaded', initSPA);
    </script>
</body>
</html>'''
    
    # 写入文件
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f'✓ 合并完成！')
    print(f'  输出: {OUTPUT}')
    print(f'  共处理 {len(pages)} 个页面')

if __name__ == '__main__':
    build_spa()

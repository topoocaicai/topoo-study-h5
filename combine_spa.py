#!/usr/bin/env python3
"""
TopSpace SPA 合并脚本
将多个独立H5文件合并为一个SPA单页应用
自动处理CSS命名空间冲突
"""
import re, sys, os

# ===== 文件路径 =====
FILES = {
    'collision': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·碰撞·H5.html',
    'philosophy': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·碰撞·Topoo哲学·H5.html',
    'story': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·故事·H5.html',
    'script': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·故事·新手剧本·H5.html',
    'plaza': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·广场·H5.html',
    'map': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·街区地图·矩形Block版v15·H5.html',
    'profile': r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·我的·页面·H5.html',
}

OUTPUT = r'C:\Users\Administrator\WorkBuddy\Claw\TopSpace·全功能·H5.html'

# ===== 工具函数 =====
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_css_html(content):
    """提取<style>内容和<body>内的HTML（去掉html/head/body标签）"""
    # 提取所有style内容
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    css = '\n'.join(style_blocks)
    # 提取body内容
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    html = body_match.group(1) if body_match else ''
    return css, html

def namespace_css(css, prefix):
    """给CSS选择器加命名空间"""
    # 跳过 @keyframes, @media, @import 等
    # 只处理普通选择器
    lines = css.split('\n')
    result = []
    in_at_rule = 0
    for line in lines:
        stripped = line.strip()
        # 处理@规则
        if stripped.startswith('@'):
            in_at_rule += stripped.count('{') - stripped.count('}')
            result.append(line)
            continue
        if in_at_rule > 0:
            in_at_rule += stripped.count('{') - stripped.count('}')
            result.append(line)
            continue
        # 处理普通选择器行（包含 { ）
        if '{' in line and not line.strip().startswith('//'):
            # 在第一个 { 之前的选择器部分加前缀
            # 简单处理：在每行第一个 { 前插入前缀
            # 处理多个选择器用逗号分隔的情况
            def add_prefix(m):
                sel = m.group(0).rstrip()
                # 不处理 :root, body, html 等全局选择器
                if sel in ('body', 'html', '*'):
                    return m.group(0)
                # 在每个选择器前加前缀
                parts = [p.strip() for p in sel.split(',')]
                new_parts = []
                for p in parts:
                    p = p.strip()
                    if p and not p.startswith('#') and not p.startswith('.' + prefix):
                        new_parts.append('#page-' + prefix + ' ' + p)
                    else:
                        new_parts.append(p)
                return ', '.join(new_parts) + ' '
            # 只处理行内第一个 { 之前的部分
            idx = line.find('{')
            if idx > 0:
                before = line[:idx]
                after = line[idx:]
                # 使用regex处理选择器
                # 简化处理：加 #page-prefix 在行首
                result.append(line)
            else:
                result.append(line)
        else:
            result.append(line)
    return '\n'.join(result)

def namespace_css_simple(css, prefix):
    """简化版：在每个CSS规则选择器前加 #page-prefix"""
    # 分割CSS规则（简单方法）
    # 在 </style> 前的所有规则块处理
    pattern = re.compile(r'([^{}/\n]+)\s*\{', re.MULTILINE)
    
    def replacer(m):
        selector = m.group(1).strip()
        # 跳过 @关键字
        if selector.startswith('@'):
            return m.group(0)
        # 对每个逗号分隔的选择器加前缀
        parts = []
        for part in selector.split(','):
            part = part.strip()
            if part and not part.startswith('#page-'):
                parts.append('#page-' + prefix + ' ' + part)
            else:
                parts.append(part)
        return ', '.join(parts) + ' {'
    
    # 应用替换
    css_new = pattern.sub(replacer, css)
    return css_new

def cleanup_html(html, page_id):
    """清理HTML：去掉phone-shell（SPA只有一个）、去掉bottom-tab（SPA统一管理）"""
    # 去掉phone-notch（SPA只有一个）
    html = re.sub(r'<div class="phone-notch"[^>]*>.*?</div>\s*</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="phone-notch"[^>]*></div>', '', html)
    # 去掉独立的 phone-shell（页面内容不再需要自己的phone-shell）
    html = re.sub(r'<div class="phone-shell"[^>]*>', '<div id="page-' + page_id + '" class="spa-page">', html, count=1)
    html = re.sub(r'</div>\s*</body>', '</div>', html)
    # 去掉 </body></html> 等尾部
    html = re.sub(r'</body>.*?</html>', '', html, flags=re.DOTALL)
    return html

# ===== 主逻辑 =====
def main():
    print('开始合并TopSpace SPA...')
    
    # 读取所有文件
    pages = {}
    for key, path in FILES.items():
        if os.path.exists(path):
            print(f'  读取: {os.path.basename(path)}')
            pages[key] = read_file(path)
        else:
            print(f'  ⚠ 不存在: {path}')
    
    # 构建SPA
    spa_css = []
    spa_html = []
    
    # 共享CSS（SPA框架）
    shared_css = """
        /* ===== SPA 框架样式 ===== */
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:#1a1816; font-family:-apple-system,"PingFang SC","Helvetica Neue",sans-serif; overflow:hidden; height:100vh; }
        .spa-container { position:relative; width:100vw; height:100vh; overflow:hidden; }
        .spa-phone { position:relative; width:375px; height:812px; margin:20px auto; border-radius:44px; overflow:hidden; box-shadow:0 0 0 2px #C8C0B4,0 0 0 6px #1a1816,0 20px 60px rgba(0,0,0,0.3); }
        .spa-page { position:absolute; top:0; left:0; right:0; bottom:0; overflow:hidden; display:none; }
        .spa-page.active { display:block; }
        .spa-subpage { position:absolute; top:0; left:0; right:0; bottom:0; overflow:hidden; display:none; z-index:80; }
        .spa-subpage.active { display:block; }
        .spa-bottom-tab { position:absolute; bottom:0; left:0; right:0; height:80px; background:rgba(245,240,232,0.95); backdrop-filter:blur(10px); border-top:1px solid rgba(0,0,0,0.06); display:flex; align-items:flex-start; padding-top:8px; z-index:150; }
        .spa-bottom-tab.hidden { display:none; }
        .spa-tab-item { flex:1; display:flex; flex-direction:column; align-items:center; gap:3px; cursor:pointer; }
        .spa-tab-icon { font-size:20px; }
        .spa-tab-label { font-size:10px; color:#A8A098; }
        .spa-tab-item.active .spa-tab-label { color:#2C2824; font-weight:600; }
        .spa-tab-item.active .spa-tab-icon { filter:none; }
        .spa-tab-item:not(.active) .spa-tab-icon { filter:grayscale(0.6) opacity(0.5); }
        .spa-back-btn { position:absolute; top:44px; left:16px; z-index:200; width:32px; height:32px; border-radius:50%; background:rgba(0,0,0,0.04); border:1px solid rgba(0,0,0,0.06); display:flex; align-items:center; justify-content:center; font-size:18px; cursor:pointer; }
    """
    spa_css.append(shared_css)
    
    # 处理每个页面
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
        css, html = extract_css_html(pages[key])
        # 命名空间化CSS
        css_ns = namespace_css_simple(css, key)
        spa_css.append(f'\n/* ===== {page_titles[key]} ===== */\n' + css_ns)
        # 清理HTML
        html_clean = cleanup_html(html, key)
        spa_html.append(f'\n<!-- ===== {page_titles[key]} ===== -->\n<div id="page-{key}" class="spa-page">\n{html_clean}\n</div>\n')
    
    # 组装完整HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TopSpace · 全功能</title>
    <style>
{''.join(spa_css)}
    </style>
</head>
<body>
    <div class="spa-container">
        <div class="spa-phone" id="phoneShell">
            
            {''.join(spa_html)}
            
            <!-- 底部导航 -->
            <div class="spa-bottom-tab" id="bottomTab">
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
            
        </div>
    </div>
    
    <script>
        // SPA导航逻辑
        var currentTab = 'collision';
        var currentSubPage = null;
        
        function switchTab(tabName) {
            // 隐藏所有页面
            document.querySelectorAll('.spa-page').forEach(p => p.classList.remove('active'));
            // 显示目标页面
            var target = document.getElementById('page-' + tabName);
            if (target) target.classList.add('active');
            // 更新底部Tab状态
            document.querySelectorAll('.spa-tab-item').forEach(t => t.classList.remove('active'));
            document.querySelector('.spa-tab-item[data-tab="' + tabName + '"]').classList.add('active');
            currentTab = tabName;
            currentSubPage = null;
        }
        
        function showSubPage(pageId) {
            document.querySelectorAll('.spa-page').forEach(p => p.classList.remove('active'));
            var target = document.getElementById(pageId);
            if (target) target.classList.add('active');
            currentSubPage = pageId;
        }
        
        function goBack() {
            if (currentSubPage) {
                document.getElementById(currentSubPage).classList.remove('active');
                document.getElementById('page-' + currentTab).classList.add('active');
                currentSubPage = null;
            }
        }
        
        // Toast功能
        function showToast(msg) {
            var t = document.createElement('div');
            t.textContent = msg;
            Object.assign(t.style, {
                position:'fixed', bottom:'100px', left:'50%', transform:'translateX(-50%)',
                background:'rgba(44,40,36,0.88)', color:'#F5F0E8', padding:'10px 20px',
                borderRadius:'20px', fontSize:'13px', zIndex:'999', whiteSpace:'nowrap',
                boxShadow:'0 4px 16px rgba(0,0,0,0.15)', opacity:'0', transition:'opacity 0.3s'
            });
            document.body.appendChild(t);
            requestAnimationFrame(() => t.style.opacity = '1');
            setTimeout(() => {
                t.style.opacity = '0';
                setTimeout(() => t.remove(), 300);
            }, 1800);
        }
    <\/script>
</body>
</html>"""
    
    # 写入文件
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f'✓ 合并完成: {OUTPUT}')
    print(f'  共处理 {len(pages)} 个页面')

if __name__ == '__main__':
    main()

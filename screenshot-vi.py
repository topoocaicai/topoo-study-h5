import subprocess, time, os

html_path = os.path.abspath(r"c:\Users\Administrator\WorkBuddy\Claw\拓圈品牌VI手册.html")
output_path = r"C:\Users\Administrator\Desktop\拓圈资料\拓圈品牌VI手册-长图.png"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Step 1: Open page and get full height via JS evaluation
# Use a temp HTML that measures itself
import tempfile

measure_js = """
<script>
window.onload = function() {
    var h = document.documentElement.scrollHeight;
    document.title = 'HEIGHT:' + h;
};
</script>
"""

# Read original HTML and inject measurement
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Insert measurement script before </body>
measure_html = html.replace('</body>', measure_js + '</body>')

# Write to temp file
temp_html = os.path.join(tempfile.gettempdir(), 'topoo-vi-measure.html')
with open(temp_html, 'w', encoding='utf-8') as f:
    f.write(measure_html)

# Open with edge and grab title via a tiny JS
# Alternative: just use a generous height like 20000px
# The page is roughly: cover(100vh~1080) + TOC(300) + 6 sections(~600 each) + backcover(60vh~650) = ~6000px
# Let's use 12000 to be safe on a 1200px wide viewport

width = 1200
height = 15000  # generous

print(f"Generating screenshot: {width}x{height}...")
result = subprocess.run(
    [edge, '--headless', '--disable-gpu', '--no-sandbox',
     f'--screenshot={output_path}',
     f'--window-size={width},{height}',
     f'file:///{html_path.replace(os.sep, "/")}'],
    capture_output=True, text=True, timeout=30
)

print("stdout:", result.stdout)
print("stderr:", result.stderr)

if os.path.exists(output_path):
    size = os.path.getsize(output_path)
    print(f"Done! File size: {size} bytes ({size/1024/1024:.1f} MB)")
else:
    print("Failed - no output file")

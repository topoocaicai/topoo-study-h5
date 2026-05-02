"""
Full-page screenshot using Edge CDP protocol.
Segments the page into viewport-sized chunks, then stitches them together.
"""
import subprocess, json, time, os, base64, struct, zlib, io
from PIL import Image

HTML_FILE = r"c:\Users\Administrator\WorkBuddy\Claw\拓圈品牌VI手册.html"
OUTPUT_FILE = r"C:\Users\Administrator\Desktop\拓圈资料\拓圈品牌VI手册-长图.png"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
VIEWPORT_W = 1200
VIEWPORT_H = 900
DEBUG_PORT = 19222

# Launch Edge headless with remote debugging
proc = subprocess.Popen(
    [EDGE, '--headless=new', '--disable-gpu', '--no-sandbox',
     f'--remote-debugging-port={DEBUG_PORT}',
     '--remote-allow-origins=*',
     '--window-size=1200,900',
     f'file:///{HTML_FILE.replace(os.sep, "/")}'],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

time.sleep(3)

import urllib.request

def cdp(method, params=None):
    """Send CDP command via HTTP"""
    cmd = {'id': 1, 'method': method}
    if params:
        cmd['params'] = params
    data = json.dumps(cmd).encode()
    req = urllib.request.Request(
        f'http://127.0.0.1:{DEBUG_PORT}/json/protocol',
        data=data, headers={'Content-Type': 'application/json'}
    )
    # Use the target endpoint instead
    return None

def send_to_target(target_ws_url, method, params=None, msg_id=1):
    """Send CDP command to a specific target via WebSocket"""
    import websocket
    ws = websocket.create_connection(target_ws_url, timeout=10)
    cmd = {'id': msg_id, 'method': method}
    if params:
        cmd['params'] = params
    ws.send(json.dumps(cmd))
    response = ws.recv()
    ws.close()
    return json.loads(response)

# Get available targets
try:
    targets = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{DEBUG_PORT}/json').read())
    print(f"Found {len(targets)} targets")
    for t in targets:
        print(f"  {t.get('type')}: {t.get('title', '')[:50]} - {t.get('url', '')[:80]}")

    page_target = None
    for t in targets:
        if t.get('type') == 'page':
            page_target = t
            break

    if not page_target:
        print("No page target found!")
        proc.terminate()
        exit(1)

    ws_url = page_target['webSocketDebuggerUrl']

    # Install websocket if needed
    try:
        import websocket
    except ImportError:
        print("Installing websocket-client...")
        subprocess.run([
            "C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe",
            "-m", "pip", "install", "websocket-client"
        ], capture_output=True)
        import websocket

    def cdp_cmd(ws, method, params=None, msg_id=1):
        cmd = {'id': msg_id, 'method': method}
        if params:
            cmd['params'] = params
        ws.send(json.dumps(cmd))
        # Read responses until we get our id
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == msg_id:
                return resp

    ws = websocket.create_connection(ws_url, timeout=15)

    # Set viewport
    cdp_cmd(ws, 'Emulation.setDeviceMetricsOverride', {
        'width': VIEWPORT_W, 'height': VIEWPORT_H,
        'deviceScaleFactor': 2, 'mobile': False
    })

    # Wait for page load
    time.sleep(2)

    # Get full page dimensions
    result = cdp_cmd(ws, 'Runtime.evaluate', {
        'expression': 'JSON.stringify({w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight})',
        'returnByValue': True
    })
    dims = json.loads(result['result']['result']['value'])
    page_w = dims['w']
    page_h = dims['h']
    print(f"Page dimensions: {page_w}x{page_h}")

    # Calculate segments
    scale = 2  # deviceScaleFactor
    segments = []
    y_offset = 0
    while y_offset < page_h:
        seg_h = min(VIEWPORT_H, page_h - y_offset)
        segments.append((y_offset, seg_h))
        y_offset += seg_h

    print(f"Need {len(segments)} segments")

    # Capture each segment
    images = []
    for i, (y, h) in enumerate(segments):
        # Scroll to position
        cdp_cmd(ws, 'Runtime.evaluate', {
            'expression': f'window.scrollTo(0, {y})'
        })
        time.sleep(0.3)

        # Capture screenshot
        result = cdp_cmd(ws, 'Page.captureScreenshot', {
            'format': 'png',
            'clip': {
                'x': 0, 'y': 0,
                'width': VIEWPORT_W,
                'height': h,
                'scale': scale
            }
        }, msg_id=i+10)

        img_data = base64.b64decode(result['result']['data'])
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
        print(f"  Segment {i+1}/{len(segments)}: y={y}, h={h}, img={img.size}")

    ws.close()

    # Stitch images together
    total_h = sum(img.height for img in images)
    final_w = images[0].width
    print(f"Creating final image: {final_w}x{total_h}")

    final = Image.new('RGB', (final_w, total_h), (245, 240, 232))
    y_pos = 0
    for img in images:
        final.paste(img, (0, y_pos))
        y_pos += img.height

    final.save(OUTPUT_FILE, 'PNG', optimize=True)
    print(f"Saved: {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)/1024/1024:.1f} MB)")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    proc.terminate()

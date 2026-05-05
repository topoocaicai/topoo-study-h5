#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 TopSpace 广场 H5 页面"""

html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>TopSpace · 广场</title>
    <style>
* { margin:0; padding:0; box-sizing:border-box; }
:root { --paper:#F5F0E8; --text:#2C2824; --text-muted:#8A8478; --amber:#E8B44C; --rust:#D96B6B; --water:#4A9EB8; --wood:#A0B87A; --earth:#9B7BBF; }
html, body { width:100%; height:100%; overflow:hidden; font-family:-apple-system,"PingFang SC","Helvetica Neue",sans-serif; -webkit-user-select:none; user-select:none; }

.scene { position:relative; width:100%; height:100%; overflow:hidden; cursor:grab; }
.scene.grabbing { cursor:grabbing; }

.sky { position:absolute; top:0; left:0; right:0; height:55%; z-index:0;
    background:linear-gradient(180deg, #1A1F30 0%, #252B3D 25%, #2E3650 50%, #3D4560 75%, #5A6078 100%); }
.stars { position:absolute; top:0; left:0; right:0; height:50%; z-index:1; pointer-events:none; }
.star { position:absolute; border-radius:50%; background:#fff; opacity:0.6; animation: twinkle 3s ease-in-out infinite; }
@keyframes twinkle { 0%,100% { opacity:0.3; transform:scale(1); } 50% { opacity:0.9; transform:scale(1.2); } }
.moon { position:absolute; top:12%; right:15%; width:32px; height:32px; border-radius:50%;
    background:radial-gradient(circle at 40% 40%, #F0EAD0, #D4C880);
    box-shadow:0 0 20px rgba(240,230,180,0.3), 0 0 40px rgba(240,230,180,0.1); z-index:2; }

.skyline-far { position:absolute; bottom:0; left:0; right:0; height:48%; z-index:2; pointer-events:none; opacity:0.18; filter: blur(2px); }

.wall-wrap { position:absolute; bottom:0; left:0; right:0; height:62%; z-index:5; }
.wall-body { position:absolute; top:0; left:-5%; width:110%; height:100%;
    background: repeating-linear-gradient(0deg, transparent, transparent 22px, rgba(0,0,0,0.05) 22px, rgba(0,0,0,0.05) 24px),
                repeating-linear-gradient(90deg, transparent, transparent 68px, rgba(0,0,0,0.04) 68px, rgba(0,0,0,0.04) 70px),
                linear-gradient(180deg, #A09080 0%, #887868 50%, #786858 100%); }
.wall-top { position:absolute; top:-16px; left:-3%; width:106%; display:flex; height:16px; z-index:6; }
.crenel { width:58px; height:16px; background:linear-gradient(180deg, #9A9080, #8A8070); border-radius:2px 2px 0 0; margin-right:22px; box-shadow:0 -1px 3px rgba(0,0,0,0.06); }
.crenel-gap { width:36px; height:16px; }
.wall-body::after { content:''; position:absolute; top:0; left:0; right:0; bottom:0;
    background: linear-gradient(110deg, rgba(255,248,235,0.12) 0%, transparent 40%, transparent 70%, rgba(0,0,0,0.1) 100%),
                radial-gradient(ellipse at 30% 30%, rgba(255,240,210,0.06), transparent 50%);
    pointer-events:none; }

/* 明城墙标注框 */
.wall-label { position:absolute; top:-50px; left:50%; transform:translateX(-50%); z-index:10;
    background:linear-gradient(135deg, #8B7355, #6B5545);
    color:#F5F0E8; font-size:13px; font-weight:700; letter-spacing:6px; padding:8px 24px;
    border-radius:4px; box-shadow:0 3px 10px rgba(0,0,0,0.25); white-space:nowrap; }
.wall-label::after { content:''; position:absolute; bottom:-8px; left:50%; transform:translateX(-50%);
    border-left:8px solid transparent; border-right:8px solid transparent;
    border-top:8px solid #6B5545; }

/* 古代墙洞 */
.arch-hole { position:absolute; bottom:0; z-index:8; }
.arch-hole-body { width:120px; height:140px; background:linear-gradient(180deg, #1A1A18, #0A0A08);
    border-radius:60px 60px 0 0; margin:0 auto;
    box-shadow:inset 0 5px 20px rgba(0,0,0,0.5), 0 -2px 10px rgba(0,0,0,0.3); }
.arch-hole-inner { width:100px; height:110px; background:linear-gradient(180deg, #050505, #0A0A08);
    border-radius:50px 50px 0 0; margin:0 auto; margin-top:15px;
    box-shadow:inset 0 3px 15px rgba(0,0,0,0.8); }

/* 门洞效果 */
.arch-effect { position:absolute; bottom:0; z-index:9; pointer-events:none; }
.arch-light { width:80px; height:100px; background:linear-gradient(180deg, rgba(20,25,35,0.9), rgba(10,12,18,0.95));
    border-radius:40px 40px 0 0; margin:0 auto;
    box-shadow:inset 0 0 30px rgba(0,0,0,0.8), 0 0 0 4px rgba(90,80,70,0.4); }

.gate { position:absolute; bottom:0; z-index:7; }
.gate-body { width:80px; height:100px; background:linear-gradient(180deg, #4A4035, #3A3028); border-radius:40px 40px 0 0; margin:0 auto; }
.gate-arch { position:absolute; top:0; left:50%; transform:translateX(-50%); width:60px; height:50px; background:linear-gradient(180deg, #3A3028, #2A2018); border-radius:30px 30px 0 0; }
.wall-weather { position:absolute; bottom:0; left:0; right:0; height:30%; background:linear-gradient(180deg, transparent, rgba(60,50,40,0.15)); pointer-events:none; }

.ground { position:absolute; bottom:0; left:0; right:0; height:18%; z-index:15;
    background: repeating-linear-gradient(90deg, transparent, transparent 95px, rgba(0,0,0,0.02) 95px, rgba(0,0,0,0.02) 100px),
                linear-gradient(180deg, #908578 0%, #807068 50%, #706058 100%);
    box-shadow:inset 0 2px 6px rgba(0,0,0,0.06); }
.ground::before { content:''; position:absolute; top:0; left:0; right:0;
    background:repeating-linear-gradient(0deg, transparent, transparent 48px, rgba(0,0,0,0.03) 48px, rgba(0,0,0,0.03) 50px); }

.bulletin-frame { position:absolute; bottom:18%; left:0; right:0; height:70%; z-index:20; pointer-events:none; }
.frame-top { position:absolute; top:0; left:0; right:0; height:6px; background:linear-gradient(180deg, #7A7068, #6A6058); border-radius:3px; }
.frame-pole { position:absolute; top:6px; width:8px; height:calc(100% - 6px); background:linear-gradient(90deg, #8A8078, #9A9088, #8A8078); border-radius:2px; }
.frame-pole-l { left:12%; } .frame-pole-r { right:12%; }
.frame-bottom { position:absolute; bottom:0; left:12%; right:12%; height:6px; background:linear-gradient(180deg, #6A6058, #5A5048); border-radius:3px; }

.vp { position:absolute; top:0; left:0; right:0; bottom:0; overflow:hidden; z-index:25; }
.cv { position:absolute; height:100%; display:flex; align-items:center; gap:0; will-change:transform; }

.sticky { position:absolute; cursor:pointer; transition: filter 0.2s, transform 0.15s; }
.sticky:hover { filter:brightness(1.04); } .sticky:active { filter:brightness(0.95); }
.sticky-creator { background:#FFF9E0; } .sticky-meet { background:#FFF0F0; } .sticky-rally { background:#EEF5FF; } .sticky-idea { background:#F0FFF0; }
.sticky-body { width:100%; height:100%; border-radius:2px; box-shadow:3px 4px 12px rgba(0,0,0,0.12), 0 0 0 0.5px rgba(0,0,0,0.04); position:relative; overflow:hidden; padding:14px 12px; }
.sticky-body::before { content:''; position:absolute; top:0; left:0; right:0; bottom:0;
    background: radial-gradient(ellipse at 20% 15%, rgba(255,255,255,0.5), transparent 50%),
                radial-gradient(ellipse at 80% 90%, rgba(200,190,170,0.12), transparent 40%);
    pointer-events:none; }
.sticky-corner { position:absolute; bottom:0; right:0; width:18px; height:18px; background:linear-gradient(135deg, transparent 50%, rgba(0,0,0,0.04) 50%); border-radius:0 0 2px 0; }
.pin-tape { position:absolute; top:-6px; left:50%; transform:translateX(-50%) rotate(-8deg); width:50px; height:14px; background:rgba(200,210,160,0.45); border:1px solid rgba(180,200,140,0.3); border-radius:1px; box-shadow:0 1px 3px rgba(0,0,0,0.06); }
.pin-pushpin { position:absolute; top:-8px; left:50%; transform:translateX(-50%); width:12px; height:12px; background:radial-gradient(circle at 35% 35%, #E85555, #AA3333); border-radius:50%; box-shadow:0 2px 4px rgba(0,0,0,0.2), inset 0 -2px 4px rgba(0,0,0,0.1); }
.pin-clip { position:absolute; top:-8px; left:calc(100% - 30px); width:18px; height:20px; border:2.5px solid #9A9080; border-radius:9px 9px 2px 2px; background:transparent; box-shadow:0 2px 4px rgba(0,0,0,0.08); }

.top-bar { position:absolute; top:0; left:0; right:0; z-index:200; padding:44px 20px 12px; display:flex; align-items:center; justify-content:space-between; background:linear-gradient(180deg, rgba(26,31,48,0.85) 0%, transparent 100%); pointer-events:none; }
.tb-left { width:32px; } .tb-center { flex:1; text-align:center; }
.tb-title { font-size:17px; font-weight:700; color:#F5F0E8; letter-spacing:3px; }
.tb-sub { font-size:10px; color:rgba(245,240,232,0.45); margin-top:2px; letter-spacing:1px; }
.tb-right { display:flex; gap:8px; }
.tb-icon { width:32px; height:32px; border-radius:50%; background:rgba(245,240,232,0.08); border:none; color:rgba(245,240,232,0.6); font-size:14px; cursor:pointer; display:flex; align-items:center; justify-content:center; pointer-events:auto; }

.loc-tag { position:absolute; top:76px; left:50%; transform:translateX(-50%); font-size:11px; color:rgba(245,240,232,0.5); background:rgba(26,31,48,0.5); padding:4px 14px; border-radius:12px; backdrop-filter:blur(6px); z-index:200; display:flex; align-items:center; gap:5px; letter-spacing:1px; }
.loc-dot { width:5px; height:5px; background:#A0B87A; border-radius:50%; }

.drag-hint { position:absolute; bottom:16%; left:50%; transform:translateX(-50%); font-size:11px; color:rgba(245,240,232,0.35); z-index:50; display:flex; align-items:center; gap:6px; animation:hintPulse 2.5s ease-in-out infinite; pointer-events:none; white-space:nowrap; background:rgba(26,31,48,0.4); padding:6px 16px; border-radius:14px; }
@keyframes hintPulse { 0%,100%{ opacity:0.3; } 50%{ opacity:0.7; } }

.bottom-tab { position:absolute; bottom:0; left:0; right:0; height:70px; background:rgba(20,22,32,0.92); backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px); border-top:1px solid rgba(232,180,76,0.08); display:flex; justify-content:space-around; align-items:flex-start; padding-top:10px; z-index:300; padding-bottom:env(safe-area-inset-bottom, 0); }
.tab-item { display:flex; flex-direction:column; align-items:center; gap:3px; cursor:pointer; padding:4px 10px; }
.tab-icon { font-size:20px; color:rgba(245,240,232,0.3); transition:color 0.2s; }
.tab-label { font-size:9px; color:rgba(245,240,232,0.3); font-weight:600; transition:color 0.2s; }
.tab-item.on .tab-icon { color:#E8B44C; } .tab-item.on .tab-label { color:#E8B44C; }
.tab-item:not(.on) .tab-icon { filter:grayscale(0.5); opacity:0.42; }

.toast { position:fixed; bottom:90px; left:50%; transform:translateX(-50%); background:rgba(44,40,36,0.88); color:#F5F0E8; padding:9px 20px; border-radius:20px; font-size:12px; z-index:500; white-space:nowrap; opacity:0; transition:opacity 0.3s; pointer-events:none; }
.toast.show { opacity:1; }

.detail-overlay { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(20,22,32,0.7); z-index:400; display:none; align-items:flex-end; justify-content:center; }
.detail-overlay.show { display:flex; }
.detail-sheet { width:100%; max-height:75vh; background:#F5F0E8; border-radius:20px 20px 0 0; padding:24px 20px 40px; transform:translateY(100%); transition:transform 0.35s cubic-bezier(0.32,0.72,0,1); overflow-y:auto; }
.detail-overlay.show .detail-sheet { transform:translateY(0); }
.detail-handle { width:36px; height:4px; background:#D0C8BC; border-radius:2px; margin:0 auto 20px; }
.detail-tag { display:inline-block; padding:3px 12px; border-radius:12px; font-size:11px; font-weight:600; margin-bottom:12px; }
.detail-tag-creator { background:rgba(160,184,122,0.15); color:#7A9A5A; }
.detail-tag-meet { background:rgba(217,107,107,0.15); color:#C05555; }
.detail-tag-rally { background:rgba(74,158,184,0.15); color:#3A8AAA; }
.detail-tag-idea { background:rgba(155,123,191,0.15); color:#7A5AAA; }
.detail-title { font-size:18px; font-weight:700; color:#2C2824; margin-bottom:6px; letter-spacing:1px; }
.detail-meta { font-size:11px; color:#A09888; margin-bottom:16px; display:flex; align-items:center; gap:8px; }
.detail-avatar { font-size:20px; vertical-align:middle; margin-right:4px; }
.detail-text { font-size:13px; line-height:1.8; color:#5A5650; margin-bottom:20px; }
.detail-info { background:rgba(74,158,184,0.06); border:1px solid rgba(74,158,184,0.12); border-radius:12px; padding:14px; margin-bottom:20px; }
.detail-info-row { display:flex; align-items:center; gap:8px; margin-bottom:8px; font-size:12px; color:#6A6258; }
.detail-info-row:last-child { margin-bottom:0; }
.detail-cta { width:100%; padding:14px; border:none; border-radius:14px; font-size:14px; font-weight:600; color:#fff; cursor:pointer; text-align:center; transition:filter 0.2s; }
.detail-cta:active { filter:brightness(0.9); }
.detail-close { width:100%; padding:12px; margin-top:8px; background:rgba(0,0,0,0.04); border:none; border-radius:12px; font-size:13px; color:#8A8478; cursor:pointer; }

    </style>
</head>
<body>
<div class="scene" id="scene">
    <div class="sky" id="skyLayer"></div>
    <div class="stars" id="starsLayer"></div>
    <div class="moon"></div>
    <div class="skyline-far" id="skylineFar"></div>

    <div class="wall-wrap" id="wallWrap">
        <div class="wall-body"><div class="wall-top" id="wallTop"></div></div>
        <!-- 明城墙标注 -->
        <div class="wall-label">明城墙</div>
        <!-- 古代墙洞 -->
        <div class="arch-hole" style="left:8%;"><div class="arch-hole-body"><div class="arch-hole-inner"></div></div></div>
        <div class="arch-hole" style="left:28%;"><div class="arch-hole-body"><div class="arch-hole-inner"></div></div></div>
        <div class="arch-hole" style="right:12%;"><div class="arch-hole-body"><div class="arch-hole-inner"></div></div></div>
        <div class="arch-effect" style="left:52%;bottom:0;"><div class="arch-light"></div></div>
        <div class="wall-weather"></div>
        <div class="gate" style="left:35%;"><div class="gate-body"><div class="gate-arch"></div></div></div>
        <div class="gate" style="right:20%;"><div class="gate-body"><div class="gate-arch"></div></div></div>
    </div>

    <div class="ground" id="groundLayer"></div>

    <div class="bulletin-frame">
        <div class="frame-top"></div>
        <div class="frame-pole frame-pole-l"></div>
        <div class="frame-pole frame-pole-r"></div>
        <div class="frame-bottom"></div>
    </div>

    <div class="vp" id="vp"><div class="cv" id="cv"></div></div>

    <div class="top-bar">
        <div class="tb-left"></div>
        <div class="tb-center"><div class="tb-title">广 场</div><div class="tb-sub">走走看看 · 真实连接</div></div>
        <div class="tb-right">
            <button class="tb-icon" onclick="showToast('搜索 · 开发中')">&#x1F50D;</button>
            <button class="tb-icon" onclick="showToast('消息 · 开发中')">&#x2709;</button>
        </div>
    </div>

    <div class="loc-tag"><div class="loc-dot"></div>金陵大陆 · 壹号街区 · 广场</div>
    <div class="drag-hint" id="dragHint">&#x2190; 左右滑动，翻看大家的动态 &#x2192;</div>

    <div class="bottom-tab">
        <div class="tab-item" onclick="showToast('星图 · 开发中')"><div class="tab-icon">&#x1F5FA;</div><div class="tab-label">星图</div></div>
        <div class="tab-item" onclick="showToast('故事 · 开发中')"><div class="tab-icon">&#x1F4D6;</div><div class="tab-label">故事</div></div>
        <div class="tab-item" onclick="showToast('碰撞 · 开发中')"><div class="tab-icon">&#x26A1;</div><div class="tab-label">碰撞</div></div>
        <div class="tab-item on"><div class="tab-icon">&#x1F3D8;</div><div class="tab-label">广场</div></div>
        <div class="tab-item" onclick="location.href='./TopSpace·我的·H5.html'"><div class="tab-icon">&#x1FA90;</div><div class="tab-label">我的</div></div>
    </div>
</div>

<div class="detail-overlay" id="detailOverlay" onclick="closeDetail(event)">
    <div class="detail-sheet" onclick="event.stopPropagation()">
        <div class="detail-handle"></div>
        <div class="detail-tag" id="detailTag"></div>
        <div class="detail-title" id="detailTitle"></div>
        <div class="detail-meta" id="detailMeta"></div>
        <div class="detail-text" id="detailText"></div>
        <div class="detail-info" id="detailInfo" style="display:none;"></div>
        <button class="detail-cta" id="detailCta"></button>
        <button class="detail-close" onclick="closeDetail()">关闭</button>
    </div>
</div>

<div class="toast" id="toast"></div>

<script>

var posts = [
    {id:1, type:"creator", who:"手作人·林深", num:"0127", avatar:"🧶", title:"做了个小夜灯", text:"做了一个小夜灯，卖出去三个，收到了第一个陌生人的好评。这种感觉，比任何数据都真实。", tag:"创造者说", tagClass:"detail-tag-creator", time:"2小时前", hearts:12, liked:false, pin:"tape", w:290, h:230, topPct:30, color:"#FFF9E0", accent:"#A0B87A"},
    {id:2, type:"meet", who:"摄影·阿桥", num:"0341", avatar:"📷", title:"周六下午鸡鸣寺拍城市风光", text:"周六下午鸡鸣寺旁边拍城市风光，有人一起吗？带机子不带机子都行，走走看看。", tag:"约 起", tagClass:"detail-tag-meet", time:"4小时前", hearts:8, liked:false, go:3, dt:"周六 14:00", loc:"鸡鸣寺路", pin:"pushpin", w:310, h:250, topPct:50, color:"#FFF0F0", accent:"#D96B6B"},
    {id:3, type:"creator", who:"写作者·白鹿", num:"0078", avatar:"✍️", title:"写了篇「一个人逛博物馆」", text:"写完了一篇关于「一个人逛博物馆」的文章。3000字，改了六遍。发给三个人看，都说安静得像在逛一座空城。", tag:"创造者说", tagClass:"detail-tag-creator", time:"昨天", hearts:23, liked:false, pin:"clip", w:285, h:220, topPct:28, color:"#FFF9E0", accent:"#A0B87A"},
    {id:4, type:"rally", who:"拓圈官方", num:"0000", avatar:"🏛️", title:"拓圈官方寻找30名创造者入驻", text:"寻找30名创造者入驻首批街区。不要求作品完美，只要求你是认真的。首批名额有限，欢迎来聊。", tag:"召集令", tagClass:"detail-tag-rally", time:"1天前", hearts:45, liked:false, dl:"长期有效", pin:"clip", w:300, h:210, topPct:35, color:"#EEF5FF", accent:"#4A9EB8"},
    {id:5, type:"creator", who:"陶艺·云归", num:"0203", avatar:"🏺", title:"第一个陶瓷杯出窑了", text:"第一个陶瓷杯出窑了。有窑变的痕迹，老师说这叫「天意」。我觉得不完美才是最完美的。", tag:"创造者说", tagClass:"detail-tag-creator", time:"2天前", hearts:19, liked:false, pin:"tape", w:295, h:225, topPct:48, color:"#FFF9E0", accent:"#A0B87A"},
    {id:6, type:"meet", who:"咖啡·老陈", num:"0189", avatar:"☕", title:"老门东新店试豆", text:"老门东新开的小店试了，豆子选的是云南日晒。周五下午有人来杯手冲聊聊吗？我请。", tag:"约 起", tagClass:"detail-tag-meet", time:"3天前", hearts:6, liked:false, go:2, dt:"周五 15:00", loc:"老门东", pin:"pushpin", w:305, h:240, topPct:32, color:"#FFF0F0", accent:"#D96B6B"},
    {id:7, type:"idea", who:"城市观察·拾光", num:"0412", avatar:"💡", title:"玄武湖边的长椅", text:"每天早上七点，同一个长椅，同一个老人在看报纸。一个月了，我终于鼓起勇气问他：您看的是什么报？他笑着说：《扬子晚报》，我订了三十年。", tag:"灵光一现", tagClass:"detail-tag-idea", time:"昨天", hearts:38, liked:false, pin:"tape", w:290, h:235, topPct:45, color:"#F0FFF0", accent:"#9B7BBF"},
    {id:8, type:"rally", who:"拓圈官方", num:"0000", avatar:"🏛️", title:"6月主题碰撞会", text:"「城市里的留白空间」特邀建筑设计师对话，名额30人，先到先得。", tag:"召集令", tagClass:"detail-tag-rally", time:"3天前", hearts:31, liked:false, dl:"6月15日", pin:"clip", w:295, h:205, topPct:38, color:"#EEF5FF", accent:"#4A9EB8"}
];

function buildStars() {
    var html = '';
    for (var i = 0; i < 60; i++) {
        var x = Math.random() * 100;
        var y = Math.random() * 100;
        var size = 1 + Math.random() * 2;
        var delay = (Math.random() * 4).toFixed(1);
        var dur = (2 + Math.random() * 3).toFixed(1);
        html += '<div class="star" style="left:' + x.toFixed(1) + '%;top:' + y.toFixed(1) + '%;width:' + size.toFixed(1) + 'px;height:' + size.toFixed(1) + 'px;animation-delay:' + delay + 's;animation-duration:' + dur + 's"></div>';
    }
    return html;
}

function buildNanjingSkyline() {
    var totalW = 6500;
    var s = '';
    s += '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + totalW + ' 500" preserveAspectRatio="none" style="width:100%;height:100%;position:absolute;bottom:0">';

    /* 低矮建筑群 - 左侧 */
    var bldgsLeft = [
        {x:200,w:30,h:45},{x:250,w:25,h:38},{x:300,w:40,h:55},{x:360,w:22,h:32},
        {x:420,w:35,h:50},{x:480,w:50,h:72},{x:550,w:28,h:42},{x:600,w:55,h:80},
        {x:680,w:32,h:48},{x:740,w:30,h:45},{x:800,w:48,h:68},{x:870,w:25,h:35}
    ];
    for (var b = 0; b < bldgsLeft.length; b++) {
        var bb = bldgsLeft[b];
        s += '<rect x="' + bb.x + '" y="' + (330 - bb.h) + '" width="' + bb.w + '" height="' + bb.h + '" rx="1" fill="#7A7A7A" opacity="0.4"/>';
    }

    /* 低矮建筑群 - 中间 */
    var bldgsMid = [
        {x:1200,w:35,h:50},{x:1260,w:28,h:42},{x:1320,w:45,h:68},
        {x:1400,w:32,h:48},{x:1460,w:55,h:82},{x:1550,w:25,h:38},
        {x:1600,w:40,h:58},{x:1670,w:30,h:45}
    ];
    for (var b2 = 0; b2 < bldgsMid.length; b2++) {
        var bb2 = bldgsMid[b2];
        s += '<rect x="' + bb2.x + '" y="' + (325 - bb2.h) + '" width="' + bb2.w + '" height="' + bb2.h + '" rx="1" fill="#7A7A7A" opacity="0.4"/>';
    }

    /* 低矮建筑群 - 右侧补齐 */
    var bldgsRight = [
        {x:3100,w:35,h:50},{x:3160,w:28,h:42},{x:3220,w:45,h:68},
        {x:3300,w:32,h:48},{x:3360,w:55,h:82},{x:3450,w:25,h:38},
        {x:3500,w:40,h:58},{x:3560,w:30,h:45},{x:3620,w:50,h:72},
        {x:3700,w:35,h:50},{x:3760,w:28,h:42},{x:3820,w:45,h:68},
        {x:3900,w:32,h:48},{x:3960,w:55,h:82},{x:4050,w:25,h:38},
        {x:4100,w:40,h:58},{x:4160,w:30,h:45},{x:4220,w:50,h:72},
        {x:4300,w:35,h:50},{x:4360,w:28,h:42},{x:4420,w:45,h:68},
        {x:4500,w:32,h:48},{x:4560,w:55,h:82},{x:4650,w:25,h:38},
        {x:4700,w:40,h:58},{x:4760,w:30,h:45},{x:4820,w:50,h:72},
        {x:4900,w:35,h:50},{x:4960,w:28,h:42},{x:5020,w:45,h:68},
        {x:5100,w:32,h:48},{x:5160,w:55,h:82},{x:5250,w:25,h:38},
        {x:5300,w:40,h:58},{x:5360,w:30,h:45},{x:5420,w:50,h:72},
        {x:5500,w:35,h:50},{x:5560,w:28,h:42},{x:5620,w:45,h:68},
        {x:5700,w:32,h:48},{x:5760,w:55,h:82},{x:5850,w:25,h:38},
        {x:5900,w:40,h:58},{x:5960,w:30,h:45},{x:6020,w:50,h:72},
        {x:6100,w:35,h:50},{x:6160,w:28,h:42},{x:6220,w:45,h:68},
        {x:6300,w:32,h:48},{x:6360,w:55,h:82},{x:6450,w:25,h:38}
    ];
    for (var b3 = 0; b3 < bldgsRight.length; b3++) {
        var bb3 = bldgsRight[b3];
        s += '<rect x="' + bb3.x + '" y="' + (325 - bb3.h) + '" width="' + bb3.w + '" height="' + bb3.h + '" rx="1" fill="#7A7A7A" opacity="0.4"/>';
    }

    /* 远景城墙 */
    s += '<path d="M0,342 L200,340 L400,337 L600,334 L800,332 L1000,330 L1200,334 L1400,337 L1600,330 L1800,328 L2000,330 L2200,335 L2400,332 L2600,330 L2800,335 L3000,332 L3200,330 L3400,335 L3600,338 L3800,336 L4000,340 L4200,338 L4400,342 L4600,340 L4800,338 L5000,342 L5200,340 L5400,338 L5600,342 L5800,340 L6000,338 L6500,340" fill="none" stroke="#6A6A6A" stroke-width="3" opacity="0.12"/>';
    s += '<rect x="0" y="342" width="' + totalW + '" height="70" fill="#6A6A6A" opacity="0.05"/>';

    /* 远处树剪影 */
    for (var tr = 0; tr < 35; tr++) {
        var tx = 150 + tr * 180 + (tr % 3) * 40;
        var tsize = 10 + (tr % 5) * 4;
        s += '<circle cx="' + tx + '" cy="' + (312 - tsize / 2) + '" r="' + tsize + '" fill="#4A5A4A" opacity="0.12"/>';
    }

    s += '</svg>';
    return s;
}

function buildWallTop() {
    var totalW = Math.max(5000, window.innerWidth * 1.2);
    var html = '';
    var x = 0;
    while (x < totalW + 100) {
        html += '<div class="crenel" style="position:absolute;left:' + x + 'px;top:0"></div>';
        html += '<div class="crenel-gap" style="position:absolute;left:' + (x + 58) + 'px;top:0"></div>';
        x += 80;
    }
    return html;
}

function buildSticky(p) {
    var pinHtml = '';
    if (p.pin === 'tape') { pinHtml = '<div class="pin-tape"></div>'; }
    else if (p.pin === 'pushpin') { pinHtml = '<div class="pin-pushpin"></div>'; }
    else { pinHtml = '<div class="pin-clip"></div>'; }

    var heartIcon = p.liked ? '❤️' : '🤍';
    var heartColor = p.liked ? '#D96B6B' : '#A09888';

    var html = '<div class="sticky" id="sticky-' + p.id + '" style="';
    html += 'left:' + p.startX + 'px;top:' + p.topPct + '%;';
    html += 'width:' + p.w + 'px;height:' + p.h + 'px;" ';
    html += 'onclick="openDetail(' + p.id + ')">';

    html += pinHtml;
    html += '<div class="sticky-body sticky-' + p.type + '">';
    html += '<div class="sticky-corner"></div>';

    html += '<div style="position:absolute;top:10px;left:10px;padding:2px 10px;background:' + p.accent + ';color:#fff;font-size:9px;font-weight:600;border-radius:10px;z-index:5">' + p.tag + '</div>';

    html += '<div style="display:flex;align-items:center;gap:6px;margin-top:30px;margin-bottom:8px">';
    html += '<span style="font-size:18px">' + p.avatar + '</span>';
    html += '<div><div style="font-size:12px;font-weight:600;color:#3C3834">' + p.who + '</div>';
    html += '<div style="font-size:9px;color:#A09888">No.' + p.num + ' · ' + p.time + '</div></div></div>';

    html += '<div style="font-size:13px;font-weight:700;color:#2C2824;margin-bottom:6px;letter-spacing:0.5px;line-height:1.4">' + p.title + '</div>';

    var shortText = p.text.length > 45 ? p.text.substring(0, 45) + '…' : p.text;
    html += '<div style="font-size:11px;line-height:1.7;color:#6A6258;margin-bottom:8px">' + shortText + '</div>';

    html += '<div style="position:absolute;bottom:10px;left:10px;right:10px;display:flex;align-items:center;justify-content:space-between">';
    html += '<div onclick="event.stopPropagation();toggleHeart(' + p.id + ')" ';
    html += 'style="display:flex;align-items:center;gap:3px;cursor:pointer;font-size:11px;color:' + heartColor + '" ';
    html += 'id="heart-' + p.id + '">';
    html += '<span>' + heartIcon + '</span><span id="heartNum-' + p.id + '">' + p.hearts + '</span></div>';
    html += '<div style="font-size:10px;color:#B0A898">查看详情 ›</div>';
    html += '</div>';

    html += '</div></div>';
    return html;
}

function buildAllCards() {
    var html = '';
    var startX = 80;
    var gap = 40;
    for (var i = 0; i < posts.length; i++) {
        posts[i].startX = startX;
        html += buildSticky(posts[i]);
        startX += posts[i].w + gap;
    }
    return { html: html, totalW: startX + 80 };
}

function openDetail(id) {
    var p = null;
    for (var i = 0; i < posts.length; i++) { if (posts[i].id === id) { p = posts[i]; break; } }
    if (!p) return;
    document.getElementById('detailTag').className = 'detail-tag ' + p.tagClass;
    document.getElementById('detailTag').textContent = p.tag;
    document.getElementById('detailTitle').textContent = p.title;
    document.getElementById('detailMeta').innerHTML =
        '<span class="detail-avatar">' + p.avatar + '</span>' +
        '<span>' + p.who + '</span><span>·</span><span>No.' + p.num + '</span><span>·</span><span>' + p.time + '</span>';
    document.getElementById('detailText').textContent = p.text;
    var infoDiv = document.getElementById('detailInfo');
    if (p.type === 'meet') {
        infoDiv.style.display = 'block';
        infoDiv.innerHTML = '<div class="detail-info-row">📅 ' + p.dt + '</div><div class="detail-info-row">📍 ' + p.loc + '</div><div class="detail-info-row">👥 ' + p.go + ' 人已参加</div>';
        document.getElementById('detailCta').style.background = p.accent;
        document.getElementById('detailCta').textContent = '参加这个约起';
        document.getElementById('detailCta').onclick = function() { joinMeet(id); };
    } else if (p.type === 'rally') {
        infoDiv.style.display = 'block';
        infoDiv.innerHTML = '<div class="detail-info-row">🏛️ 截止日期：' + p.dl + '</div><div class="detail-info-row">👥 名额有限，先到先得</div>';
        document.getElementById('detailCta').style.background = p.accent;
        document.getElementById('detailCta').textContent = '我要参加';
        document.getElementById('detailCta').onclick = function() { joinRally(id); };
    } else {
        infoDiv.style.display = 'none';
        document.getElementById('detailCta').style.background = p.accent;
        document.getElementById('detailCta').textContent = '点亮 · 收藏这篇';
        document.getElementById('detailCta').onclick = function() { showToast('已点亮！'); closeDetail(); };
    }
    document.getElementById('detailOverlay').classList.add('show');
}

function closeDetail(e) { if (e && e.target !== document.getElementById('detailOverlay')) return; document.getElementById('detailOverlay').classList.remove('show'); }
function joinMeet(id) { for (var i = 0; i < posts.length; i++) { if (posts[i].id === id) { posts[i].go = (posts[i].go || 0) + 1; showToast('已参加！去 ' + posts[i].loc + ' 找他们吧'); break; } } closeDetail(); }
function joinRally(id) { showToast('报名成功！期待你的参与'); closeDetail(); }

function toggleHeart(id) {
    for (var i = 0; i < posts.length; i++) {
        if (posts[i].id === id) {
            posts[i].liked = !posts[i].liked;
            posts[i].hearts += posts[i].liked ? 1 : -1;
            var heartEl = document.getElementById('heart-' + id);
            var numEl = document.getElementById('heartNum-' + id);
            if (heartEl && numEl) {
                heartEl.innerHTML = '<span>' + (posts[i].liked ? '❤️' : '🤍') + '</span><span>' + posts[i].hearts + '</span>';
                heartEl.style.color = posts[i].liked ? '#D96B6B' : '#A09888';
                if (posts[i].liked) { var iconSpan = heartEl.querySelector('span'); iconSpan.style.transform = 'scale(1.3)'; setTimeout(function() { iconSpan.style.transform = 'scale(1)'; }, 200); }
            }
            break;
        }
    }
}

function showToast(msg) { var t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); setTimeout(function() { t.classList.remove('show'); }, 2000); }

var sceneEl, vpEl, cvEl, skyEl, wallEl, groundEl;
var drag = {active:false, startX:0, curScroll:0};
var maxScroll = 0;
var hasDragged = false;

function bindDrag() {
    sceneEl = document.getElementById('scene');
    vpEl = document.getElementById('vp');
    cvEl = document.getElementById('cv');
    skyEl = document.getElementById('skyLayer');
    wallEl = document.getElementById('wallWrap');
    groundEl = document.getElementById('groundLayer');
    sceneEl.addEventListener('mousedown', onDown);
    sceneEl.addEventListener('touchstart', onDown, {passive:false});
    window.addEventListener('mousemove', onMove);
    window.addEventListener('touchmove', onMove, {passive:false});
    window.addEventListener('mouseup', onUp);
    window.addEventListener('touchend', onUp);
}
function onDown(e) {
    drag.active = true;
    drag.startX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
    var cur = cvEl.style.transform || 'translateX(0px)';
    drag.curScroll = parseFloat(cur.replace('translateX(', '').replace('px)', '')) || 0;
    sceneEl.classList.add('grabbing');
    if (e.cancelable) e.preventDefault();
}
function onMove(e) {
    if (!drag.active) return;
    var x = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
    var dx = x - drag.startX;
    var target = Math.max(-maxScroll, Math.min(0, drag.curScroll + dx));
    applyParallax(target);
    if (Math.abs(target) > 20 && !hasDragged) { hasDragged = true; var hint = document.getElementById('dragHint'); if (hint) hint.style.opacity = '0'; }
}
function onUp() { drag.active = false; sceneEl.classList.remove('grabbing'); }
function applyParallax(scrollX) {
    cvEl.style.transform = 'translateX(' + scrollX + 'px)';
    skyEl.style.transform = 'translateX(' + (scrollX * 0.06) + 'px)';
    wallEl.style.transform = 'translateX(' + (scrollX * 0.25) + 'px)';
    groundEl.style.transform = 'translateX(' + (scrollX * 0.4) + 'px)';
}

function init() {
    document.getElementById('starsLayer').innerHTML = buildStars();
    document.getElementById('skylineFar').innerHTML = buildNanjingSkyline();
    document.getElementById('wallTop').innerHTML = buildWallTop();
    var result = buildAllCards();
    document.getElementById('cv').innerHTML = result.html;
    document.getElementById('cv').style.width = result.totalW + 'px';
    maxScroll = Math.max(0, result.totalW - window.innerWidth + 80);
    bindDrag();
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>'''

output_path = r'C:/Users/Administrator/Desktop/定稿app页面/TopSpace·广场·H5.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Generated: {output_path}')
print(f'Size: {len(html_content)} bytes')

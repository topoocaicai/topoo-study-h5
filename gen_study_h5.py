#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成6个海外拓圈研学H5（港澳台/东盟/俄罗斯/欧洲大陆/英国/美国）
每个H5含三档价格（4日3晚/7日6晚/14日13晚）
统一新增：南京介绍、16个备选项目、机票标注、价格备注
"""

import os

# ============ 通用CSS（新增部分） ============
EXTRA_CSS = """
  /* 南京介绍 */
  .nj-section { padding: 56px 0; border-bottom: 1px solid var(--border-light); }
  .nj-section .section-label { font-size: 10px; letter-spacing: 4px; color: var(--text-lighter); text-transform: uppercase; margin-bottom: 8px; }
  .nj-section .section-title { font-size: 24px; font-weight: 600; color: var(--text); letter-spacing: 2px; margin-bottom: 8px; }
  .nj-section .section-desc { font-size: 13px; color: var(--text-mid); line-height: 1.8; margin-bottom: 24px; max-width: 680px; }
  .nj-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
  .nj-card { background: var(--paper-light); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
  .nj-card .nj-label { font-size: 10px; letter-spacing: 2px; color: var(--text-lighter); margin-bottom: 8px; }
  .nj-card .nj-value { font-size: 14px; font-weight: 600; color: var(--text); line-height: 1.6; }
  .nj-card .nj-note { font-size: 12px; color: var(--text-light); margin-top: 6px; line-height: 1.6; }
  .nj-quote { background: var(--heritage-light); border-left: 3px solid var(--heritage); border-radius: 0 8px 8px 0; padding: 16px 20px; margin-top: 20px; }
  .nj-quote p { font-size: 13px; color: var(--heritage); line-height: 1.8; font-style: italic; }

  /* 三档价格表 */
  .tier-pricing { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 32px; }
  .tier-card { background: white; border: 1.5px solid var(--border); border-radius: 16px; padding: 32px 20px; text-align: center; position: relative; overflow: hidden; transition: transform .2s, box-shadow .2s; }
  .tier-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,.08); }
  .tier-card.featured { border-color: var(--main); box-shadow: 0 4px 20px rgba(0,0,0,.06); }
  .tier-card::before { content:''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--main), var(--amber)); }
  .tier-card .tier-duration { font-size: 10px; letter-spacing: 4px; color: var(--text-lighter); margin-bottom: 12px; }
  .tier-card .tier-name { font-size: 18px; font-weight: 700; color: var(--text); letter-spacing: 1px; margin-bottom: 6px; }
  .tier-card .tier-price { font-size: 36px; font-weight: 700; color: var(--text); letter-spacing: 1px; margin: 16px 0 8px; }
  .tier-card .tier-price .currency { font-size: 16px; font-weight: 500; color: var(--main-dark); margin-right: 2px; }
  .tier-card .tier-price .unit { font-size: 12px; font-weight: 400; color: var(--text-light); }
  .tier-card .tier-note { font-size: 11px; color: var(--text-light); margin-bottom: 16px; }
  .tier-includes { text-align: left; }
  .tier-inc-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--text-mid); padding: 3px 0; }
  .tier-inc-item .dot { width: 5px; height: 5px; border-radius: 50%; background: var(--main); flex-shrink: 0; }

  /* 备选研学项目 */
  .projects-section { padding: 56px 0; border-top: 1px solid var(--border-light); }
  .projects-section .section-label { font-size: 10px; letter-spacing: 4px; color: var(--text-lighter); text-transform: uppercase; margin-bottom: 8px; }
  .projects-section .section-title { font-size: 24px; font-weight: 600; color: var(--text); letter-spacing: 2px; margin-bottom: 8px; }
  .projects-section .section-desc { font-size: 13px; color: var(--text-mid); line-height: 1.8; margin-bottom: 32px; max-width: 600px; }
  .proj-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .proj-item { display: flex; gap: 12px; padding: 14px 16px; background: var(--paper-light); border: 1px solid var(--border); border-radius: 10px; align-items: flex-start; }
  .proj-num { width: 24px; height: 24px; border-radius: 50%; background: var(--main); color: #fff; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }
  .proj-text h5 { font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 2px; }
  .proj-text p { font-size: 11px; color: var(--text-light); line-height: 1.5; }

  /* 机票备注 + 价格备注 */
  .flight-note { background: var(--blue-light); border: 1px solid rgba(74,158,184,.2); border-radius: 10px; padding: 16px 20px; margin-top: 32px; display: flex; align-items: center; gap: 12px; }
  .flight-note .fn-icon { font-size: 20px; flex-shrink: 0; }
  .flight-note .fn-text { font-size: 13px; color: var(--blue-dark); line-height: 1.6; }
  .price-note { background: var(--amber-light); border: 1px solid rgba(232,180,76,.2); border-radius: 10px; padding: 16px 20px; margin-top: 20px; display: flex; align-items: center; gap: 12px; }
  .price-note .pn-icon { font-size: 20px; flex-shrink: 0; }
  .price-note .pn-text { font-size: 13px; color: var(--amber-dark); line-height: 1.6; font-weight: 500; }

  @media (max-width: 768px) {
    .tier-pricing { grid-template-columns: 1fr; }
    .proj-grid { grid-template-columns: 1fr; }
    .nj-grid { grid-template-columns: 1fr; }
  }
"""

# ============ 南京介绍HTML ============
NANJING_HTML = """
<!-- ===== 南京城市介绍 ===== -->
<div class="page">
  <div class="nj-section">
    <div class="section-label">City Profile</div>
    <div class="section-title">南京城市介绍</div>
    <div class="section-desc">
      南京，江苏省省会，地处长江下游中部，是中国四大古都之一，有"六朝古都、十朝都会"之称。全市面积6587平方公里，常住人口约950万。
    </div>
    <div class="nj-grid">
      <div class="nj-card">
        <div class="nj-label">历史地位</div>
        <div class="nj-value">六朝古都 · 十朝都会</div>
        <div class="nj-note">近2500年建城史，450年建都史，与西安、洛阳、北京并称中国四大古都</div>
      </div>
      <div class="nj-card">
        <div class="nj-label">科教实力</div>
        <div class="nj-value">中国高等教育第三城</div>
        <div class="nj-note">拥有南京大学、东南大学等53所高等院校，在校大学生超85万</div>
      </div>
      <div class="nj-card">
        <div class="nj-label">地理气候</div>
        <div class="nj-value">北亚热带湿润气候</div>
        <div class="nj-note">四季分明，春秋宜人。年平均温度15.4°C，是理想研学目的地</div>
      </div>
      <div class="nj-card">
        <div class="nj-label">产业名片</div>
        <div class="nj-value">六朝古都 · 创新名城</div>
        <div class="nj-note">拥有软件谷、江北新区等国家级园区，长三角特大城市</div>
      </div>
    </div>
    <div class="nj-quote">
      <p>"江南佳丽地，金陵帝王州。" 南京——世界文学之都，联合国教科文组织"世界图书之都"，每一块砖瓦都是中华文明的注脚。</p>
    </div>
  </div>
</div>
"""

# ============ 三档价格HTML ============
TIER_PRICING_HTML = """
<!-- ===== 费用说明（三档） ===== -->
<div class="page">
  <div class="section">
    <div class="section-label">Pricing</div>
    <div class="section-title">费用说明</div>
    <div class="section-desc">费用透明，按行程档位选择，无额外收费。报价为标准档价格，大咖定制内容另加费用。</div>
    <div class="tier-pricing">
      <!-- 4日3晚 -->
      <div class="tier-card">
        <div class="tier-duration">行程方案一</div>
        <div class="tier-name">4日3晚</div>
        <div class="tier-price"><span class="currency">¥</span>{{PRICE_4D}}</div>
        <div class="tier-note">含国际往返机票及签证</div>
        <div class="tier-includes">
          <div class="tier-inc-item"><span class="dot"></span>国际往返机票（指定航班）</div>
          <div class="tier-inc-item"><span class="dot"></span>中国签证办理</div>
          <div class="tier-inc-item"><span class="dot"></span>3晚四星级酒店住宿</div>
          <div class="tier-inc-item"><span class="dot"></span>全程餐饮</div>
          <div class="tier-inc-item"><span class="dot"></span>全部景点门票</div>
          <div class="tier-inc-item"><span class="dot"></span>非遗工坊材料费</div>
          <div class="tier-inc-item"><span class="dot"></span>书法教育课程费</div>
          <div class="tier-inc-item"><span class="dot"></span>定制笔墨纸砚套装</div>
          <div class="tier-inc-item"><span class="dot"></span>全程意外保险</div>
          <div class="tier-inc-item"><span class="dot"></span>接机送机专车</div>
        </div>
      </div>
      <!-- 7日6晚 -->
      <div class="tier-card featured">
        <div class="tier-duration">行程方案二</div>
        <div class="tier-name">7日6晚</div>
        <div class="tier-price"><span class="currency">¥</span>{{PRICE_7D}}</div>
        <div class="tier-note">含国际往返机票及签证</div>
        <div class="tier-includes">
          <div class="tier-inc-item"><span class="dot"></span>国际往返机票（指定航班）</div>
          <div class="tier-inc-item"><span class="dot"></span>中国签证办理</div>
          <div class="tier-inc-item"><span class="dot"></span>6晚四星级酒店住宿</div>
          <div class="tier-inc-item"><span class="dot"></span>全程餐饮</div>
          <div class="tier-inc-item"><span class="dot"></span>全部景点门票</div>
          <div class="tier-inc-item"><span class="dot"></span>非遗工坊材料费</div>
          <div class="tier-inc-item"><span class="dot"></span>书法教育课程费</div>
          <div class="tier-inc-item"><span class="dot"></span>AI创意课程费</div>
          <div class="tier-inc-item"><span class="dot"></span>全程意外保险</div>
          <div class="tier-inc-item"><span class="dot"></span>接机送机专车</div>
        </div>
      </div>
      <!-- 14日13晚 -->
      <div class="tier-card">
        <div class="tier-duration">行程方案三</div>
        <div class="tier-name">14日13晚</div>
        <div class="tier-price"><span class="currency">¥</span>{{PRICE_14D}}</div>
        <div class="tier-note">含国际往返机票及签证</div>
        <div class="tier-includes">
          <div class="tier-inc-item"><span class="dot"></span>国际往返机票（指定航班）</div>
          <div class="tier-inc-item"><span class="dot"></span>中国签证办理</div>
          <div class="tier-inc-item"><span class="dot"></span>13晚四星级酒店住宿</div>
          <div class="tier-inc-item"><span class="dot"></span>全程餐饮</div>
          <div class="tier-inc-item"><span class="dot"></span>全部景点门票</div>
          <div class="tier-inc-item"><span class="dot"></span>深度非遗体验</div>
          <div class="tier-inc-item"><span class="dot"></span>系统书法教育课程</div>
          <div class="tier-inc-item"><span class="dot"></span>AI创意全流程</div>
          <div class="tier-inc-item"><span class="dot"></span>全程意外保险</div>
          <div class="tier-inc-item"><span class="dot"></span>接机送机专车</div>
        </div>
      </div>
    </div>

    <!-- 机票备注 -->
    <div class="flight-note">
      <div class="fn-icon">✈️</div>
      <div class="fn-text"><strong>机票说明：</strong>报价含国际往返机票（指定航班），具体航班信息报名后统一通知。如需调整航班，请提前联系拓圈研学顾问。</div>
    </div>
    <!-- 价格备注 -->
    <div class="price-note">
      <div class="pn-icon">💡</div>
      <div class="pn-text">报价为标准档价格，大咖定制内容另加费用。可根据需求定制专属研学方案。</div>
    </div>
  </div>
</div>
"""

# ============ 16个备选项目HTML ============
PROJECTS_HTML = """
<!-- ===== 备选研学项目 ===== -->
<div class="page">
  <div class="projects-section">
    <div class="section-label">Optional Programs</div>
    <div class="section-title">定制特色服务 · 备选项目</div>
    <div class="section-desc">除标准行程外，还可从以下16个精品研学项目中自由选择搭配，定制专属研学方案。</div>
    <div class="proj-grid">
      <div class="proj-item"><div class="proj-num">1</div><div class="proj-text"><h5>南京云锦研究所</h5><p>国家级非遗，观摩大花楼木织机，动手制作云锦书签/小挂件</p></div></div>
      <div class="proj-item"><div class="proj-num">2</div><div class="proj-text"><h5>金陵金箔</h5><p>国家级非遗，观摩捶箔切箔，体验贴金DIY制作平安扣/书签</p></div></div>
      <div class="proj-item"><div class="proj-num">3</div><div class="proj-text"><h5>苏州苏绣研究所</h5><p>国家级苏绣非遗保护单位，学习劈丝针法，实操刺绣书签/杯垫</p></div></div>
      <div class="proj-item"><div class="proj-num">4</div><div class="proj-text"><h5>南通华艺集团</h5><p>国家级文化产业示范基地，蓝印花布/扎染体验，制作扎染手帕/帆布袋</p></div></div>
      <div class="proj-item"><div class="proj-num">5</div><div class="proj-text"><h5>南京1865创意产业园</h5><p>金陵机器制造局遗址，探访兵工展览馆，AR工业考古体验</p></div></div>
      <div class="proj-item"><div class="proj-num">6</div><div class="proj-text"><h5>南航研学基地</h5><p>航空航天科普，参观航空馆，体验飞行模拟驾驶/无人机拼装</p></div></div>
      <div class="proj-item"><div class="proj-num">7</div><div class="proj-text"><h5>苏州金龙（海格客车）</h5><p>智能客车龙头，观摩总装车间，试乘自动驾驶小巴</p></div></div>
      <div class="proj-item"><div class="proj-num">8</div><div class="proj-text"><h5>卫岗乳业</h5><p>百年中华老字号，全透明乳品观光工厂，DIY酸奶/奶片制作</p></div></div>
      <div class="proj-item"><div class="proj-num">9</div><div class="proj-text"><h5>镇江恒顺醋文化博物馆</h5><p>国家4A级景区，了解香醋48道工序，体验原浆醋品鉴</p></div></div>
      <div class="proj-item"><div class="proj-num">10</div><div class="proj-text"><h5>苏州沙洲优黄文化园</h5><p>江南黄酒文化地标，参观地下万坛酒库，体验花雕酒坛彩绘</p></div></div>
      <div class="proj-item"><div class="proj-num">11</div><div class="proj-text"><h5>南京上汽南汽</h5><p>南京老牌汽车工业基地，观摩新能源整车制造四大工艺</p></div></div>
      <div class="proj-item"><div class="proj-num">12</div><div class="proj-text"><h5>元气森林江苏工厂</h5><p>现代化无菌饮品工厂，参观全透明生产线，饮品调配DIY</p></div></div>
      <div class="proj-item"><div class="proj-num">13</div><div class="proj-text"><h5>洋河酒厂</h5><p>国家4A级景区，绵柔白酒国标制定者，体验酿酒模拟/无醇调酒</p></div></div>
      <div class="proj-item"><div class="proj-num">14</div><div class="proj-text"><h5>今世缘</h5><p>国家4A级景区，以"缘文化"为核心，体验制曲/酒香香薰蜡烛DIY</p></div></div>
      <div class="proj-item"><div class="proj-num">15</div><div class="proj-text"><h5>观朴非遗木作</h5><p>专注中式榫卯木作研学，实操鲁班锁拼装/木勺/木书签制作</p></div></div>
      <div class="proj-item"><div class="proj-num">16</div><div class="proj-text"><h5>南京机器人科普教育基地</h5><p>机器人与AI科普，观看机器狗表演，体验机甲大师S1对战</p></div></div>
    </div>
  </div>
</div>
"""

# ============ 地区配置 ============
REGIONS = [
    {
        "name": "港澳台",
        "en": "Hong Kong, Macao & Taiwan",
        "main_color": "#E8B44C",
        "main_light": "#F7EFD5",
        "main_dark": "#C49520",
        "gradient": "var(--amber), var(--rust), var(--blue)",
        "price_4d": "9,980",
        "price_7d": "15,980",
        "price_14d": "23,980",
    },
    {
        "name": "东盟",
        "en": "ASEAN",
        "main_color": "#9B7BBF",
        "main_light": "#EDE8F5",
        "main_dark": "#7A5CA0",
        "gradient": "var(--purple), var(--amber), var(--blue)",
        "price_4d": "9,980",
        "price_7d": "15,980",
        "price_14d": "23,980",
    },
    {
        "name": "俄罗斯",
        "en": "Russia",
        "main_color": "#4A9EB8",
        "main_light": "#DAEEF5",
        "main_dark": "#357A95",
        "gradient": "var(--blue), var(--amber), var(--rust)",
        "price_4d": "9,980",
        "price_7d": "15,980",
        "price_14d": "23,980",
    },
    {
        "name": "欧洲大陆",
        "en": "Europe",
        "main_color": "#D96B6B",
        "main_light": "#F5E0E0",
        "main_dark": "#B85050",
        "gradient": "var(--rust), var(--purple), var(--amber)",
        "price_4d": "9,980",
        "price_7d": "15,980",
        "price_14d": "23,980",
    },
    {
        "name": "英国",
        "en": "United Kingdom",
        "main_color": "#A0B87A",
        "main_light": "#EBF2E0",
        "main_dark": "#7D9A58",
        "gradient": "var(--green), var(--blue), var(--amber)",
        "price_4d": "9,980",
        "price_7d": "15,980",
        "price_14d": "23,980",
    },
    {
        "name": "美国",
        "en": "United States",
        "main_color": "#4A9EB8",
        "main_light": "#DAEEF5",
        "main_dark": "#357A95",
        "gradient": "var(--blue), var(--green), var(--amber)",
        "price_4d": "9,980",
        "price_7d": "15,980",
        "price_14d": "23,980",
    },
]


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ 已生成：{os.path.basename(path)}")


def build_overseas_html(region, template_4d, template_7d, template_14d):
    """
    基于4日3晚模板，替换为三档价格版，插入南京介绍和16个备选项目
    """
    main = region["main_color"]
    main_light = region["main_light"]
    main_dark = region["main_dark"]
    gradient = region["gradient"]
    name = region["name"]
    en = region["en"]

    # 替换CSS中的主色变量
    css_override = f"""
  :root {{
    --main: {main};
    --main-light: {main_light};
    --main-dark: {main_dark};
  }}"""

    # 封面区修改
    cover_html = template_4d.split("<!-- ===== 项目概述 ===== -->")[0]
    # 替换标题
    cover_html = cover_html.replace(
        "古都文脉探索营 · 海外4日3晚研学方案",
        f"古都文脉探索营 · {name}研学方案"
    )
    cover_html = cover_html.replace(
        "4日3晚 · 海外学生中华文化研学之旅",
        f"{name} · 中华文化研学之旅"
    )
    cover_html = cover_html.replace(
        "行走的课堂",
        name
    )
    cover_html = cover_html.replace(
        "4日3晚 · 海外学生中华文化研学之旅",
        f"4日3晚 / 7日6晚 / 14日13晚 · {name}研学"
    )
    # 修改封面meta中的价格显示（改为三档提示）
    cover_html = cover_html.replace(
        '<div class="val">9,980<span class="unit">元</span></div>',
        '<div class="val">9,980起<span class="unit">三档可选</span></div>'
    )
    cover_html = cover_html.replace(
        '<div class="label">含机票签证</div>',
        '<div class="label">三档行程可选</div>'
    )

    # 在封面后插入南京介绍
    after_cover = NANJING_HTML

    # 项目概述（复用模板，改标题）
    overview = extract_section(template_4d, "<!-- ===== 项目概述 ===== -->", "<!-- ===== 行程概览 ===== -->")
    overview = overview.replace("海外4日3晚·古都文脉探索营", f"{name}·古都文脉探索营")
    overview = overview.replace("海外大中小学学生", f"{name}学生")
    overview = overview.replace("新加坡、柬埔寨、俄罗斯等国学生通用", f"{name}学生")

    # 行程概览（简化，改为三档说明）
    itinerary_summary = extract_section(template_4d, "<!-- ===== 行程概览 ===== -->", "<!-- ===== 课程亮点 ===== -->")
    # 把DAY 1-4的摘要卡片改为三档说明
    tier_intro = f"""
    <div class="section">
      <div class="section-label">Program Options</div>
      <div class="section-title">三档行程说明</div>
      <div class="section-desc">同一研学体系，三种深度选择，满足不同时间与探索需求。</div>
      <div class="overview-grid">
        <div class="overview-card">
          <div class="oc-label">4日3晚</div>
          <div class="oc-value">文脉初探 · 精华版</div>
          <div class="oc-note">核心景点全景覆盖，适合首次接触中华文化的{name}学生</div>
        </div>
        <div class="overview-card">
          <div class="oc-label">7日6晚</div>
          <div class="oc-value">深度探索 · 进阶版</div>
          <div class="oc-note">增加AI创意实践与名校科创深度体验，文化+科技双线并行</div>
        </div>
        <div class="overview-card">
          <div class="oc-label">14日13晚</div>
          <div class="oc-value">全面沉浸 · 完整版</div>
          <div class="oc-note">系统书法教育全流程，多城市文化对比，成果产出最完整</div>
        </div>
      </div>
    </div>
"""

    # 课程亮点（复用4日模板）
    features = extract_section(template_4d, "<!-- ===== 课程亮点 ===== -->", "<!-- ===== 书法教育特色 ===== -->")

    # 书法教育特色（复用）
    calligraphy = extract_section(template_4d, "<!-- ===== 书法教育特色 ===== -->", "<!-- ===== 安全保障 ===== -->")

    # 安全保障（复用）
    safety = extract_section(template_4d, "<!-- ===== 安全保障 ===== -->", "<!-- ===== 费用说明 ===== -->")

    # 三档价格（替换原来的单档价格）
    pricing = TIER_PRICING_HTML.replace("{{PRICE_4D}}", region["price_4d"])
    pricing = pricing.replace("{{PRICE_7D}}", region["price_7d"])
    pricing = pricing.replace("{{PRICE_14D}}", region["price_14d"])

    # 16个备选项目
    projects = PROJECTS_HTML

    # 封底
    back_cover = template_4d.split("<!-- ===== 封底 ===== -->")[-1]
    back_cover = back_cover.replace("海外版", f"{name}版")
    back_cover = back_cover.replace("4日3晚", "三档行程")

    # 组装完整HTML
    # 在CSS末尾插入额外CSS
    css_insert_point = cover_html.find("</style>")
    extra_css_with_vars = css_override + EXTRA_CSS

    full_html = (
        cover_html[:css_insert_point]
        + extra_css_with_vars
        + cover_html[css_insert_point:]
        + after_cover
        + "<div class=\"page\">"
        + overview
        + tier_intro
        + features
        + calligraphy
        + safety
        + "</div>"
        + pricing
        + projects
        + "<!-- ===== 封底 ===== -->"
        + back_cover
    )

    return full_html


def extract_section(html, start_marker, end_marker):
    start = html.find(start_marker)
    end = html.find(end_marker)
    if start == -1 or end == -1:
        return ""
    return html[start:end]


def main():
    base_dir = "C:/Users/Administrator/WorkBuddy/Claw"

    print("读取模板文件...")
    tpl_4d = read_file(f"{base_dir}/拓圈研学·海外4日3晚·古都文脉探索营.html")
    # 7日和14日模板用于参考，暂不需要完整读取

    print("开始生成6个海外H5文件...\n")
    for region in REGIONS:
        name = region["name"]
        print(f"  生成：{name}...")
        html = build_overseas_html(region, tpl_4d, None, None)
        out_path = f"{base_dir}/拓圈研学·{name}·古都文脉探索营.html"
        write_file(out_path, html)

    print("\n✅ 全部生成完毕！")
    print(f"输出目录：{base_dir}")


if __name__ == "__main__":
    main()

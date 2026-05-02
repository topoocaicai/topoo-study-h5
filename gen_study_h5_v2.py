#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成6个海外拓圈研学H5
每个含三档价格，新增南京介绍/16备选项目/机票标注/价格备注
"""

import os
import re

BASE_DIR = "C:/Users/Administrator/WorkBuddy/Claw"

# ===== 南京介绍HTML =====
NANJING = """
<div class="page">
  <div style="padding:56px 0;border-bottom:1px solid var(--border-light);">
    <div style="font-size:10px;letter-spacing:4px;color:var(--text-lighter);text-transform:uppercase;margin-bottom:8px;">City Profile</div>
    <div style="font-size:24px;font-weight:600;color:var(--text);letter-spacing:2px;margin-bottom:8px;">南京城市介绍</div>
    <div style="font-size:13px;color:var(--text-mid);line-height:1.8;margin-bottom:24px;max-width:680px;">
      南京，江苏省省会，地处长江下游中部，是中国四大古都之一，有"六朝古都、十朝都会"之称。全市面积6587平方公里，常住人口约950万。
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;">
      <div style="background:var(--paper-light);border:1px solid var(--border);border-radius:12px;padding:20px;">
        <div style="font-size:10px;letter-spacing:2px;color:var(--text-lighter);margin-bottom:8px;">历史地位</div>
        <div style="font-size:14px;font-weight:600;color:var(--text);line-height:1.6;">六朝古都 · 十朝都会</div>
        <div style="font-size:12px;color:var(--text-light);margin-top:6px;line-height:1.6;">近2500年建城史，450年建都史</div>
      </div>
      <div style="background:var(--paper-light);border:1px solid var(--border);border-radius:12px;padding:20px;">
        <div style="font-size:10px;letter-spacing:2px;color:var(--text-lighter);margin-bottom:8px;">科教实力</div>
        <div style="font-size:14px;font-weight:600;color:var(--text);line-height:1.6;">中国高等教育第三城</div>
        <div style="font-size:12px;color:var(--text-light);margin-top:6px;line-height:1.6;">53所高等院校，在校大学生超85万</div>
      </div>
      <div style="background:var(--paper-light);border:1px solid var(--border);border-radius:12px;padding:20px;">
        <div style="font-size:10px;letter-spacing:2px;color:var(--text-lighter);margin-bottom:8px;">地理气候</div>
        <div style="font-size:14px;font-weight:600;color:var(--text);line-height:1.6;">北亚热带湿润气候</div>
        <div style="font-size:12px;color:var(--text-light);margin-top:6px;line-height:1.6;">四季分明，春秋宜人，年平均温度15.4°C</div>
      </div>
      <div style="background:var(--paper-light);border:1px solid var(--border);border-radius:12px;padding:20px;">
        <div style="font-size:10px;letter-spacing:2px;color:var(--text-lighter);margin-bottom:8px;">产业名片</div>
        <div style="font-size:14px;font-weight:600;color:var(--text);line-height:1.6;">六朝古都 · 创新名城</div>
        <div style="font-size:12px;color:var(--text-light);margin-top:6px;line-height:1.6;">软件谷、江北新区等国家级园区</div>
      </div>
    </div>
    <div style="background:var(--heritage-light);border-left:3px solid var(--heritage);border-radius:0 8px 8px 0;padding:16px 20px;">
      <p style="font-size:13px;color:var(--heritage);line-height:1.8;font-style:italic;margin:0;">"江南佳丽地，金陵帝王州。" 南京——世界文学之都，每一块砖瓦都是中华文明的注脚。</p>
    </div>
  </div>
</div>
"""

# ===== 三档价格HTML =====
def get_pricing(price_4d, price_7d, price_14d):
    return f"""
<div class="page">
  <div style="padding:56px 0;border-bottom:1px solid var(--border-light);">
    <div style="font-size:10px;letter-spacing:4px;color:var(--text-lighter);text-transform:uppercase;margin-bottom:8px;">Pricing</div>
    <div style="font-size:24px;font-weight:600;color:var(--text);letter-spacing:2px;margin-bottom:8px;">费用说明</div>
    <div style="font-size:13px;color:var(--text-mid);line-height:1.8;margin-bottom:32px;max-width:600px;">费用透明，按行程档位选择，无额外收费。报价为标准档价格，大咖定制内容另加费用。</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:32px;">
      <!-- 4日3晚 -->
      <div style="background:white;border:1.5px solid var(--border);border-radius:16px;padding:32px 20px;text-align:center;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--main),var(--amber));"></div>
        <div style="font-size:10px;letter-spacing:4px;color:var(--text-lighter);margin-bottom:12px;">行程方案一</div>
        <div style="font-size:18px;font-weight:700;color:var(--text);letter-spacing:1px;margin-bottom:6px;">4日3晚</div>
        <div style="font-size:36px;font-weight:700;color:var(--text);letter-spacing:1px;margin:16px 0 8px;">
          <span style="font-size:16px;font-weight:500;color:var(--main-dark);margin-right:2px;">¥</span>{price_4d}
        </div>
        <div style="font-size:11px;color:var(--text-light);margin-bottom:16px;">含国际往返机票（指定航班）及签证</div>
        <div style="text-align:left;font-size:11px;color:var(--text-mid);">
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>国际往返机票（指定航班）</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>中国签证办理</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>3晚四星级酒店住宿</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>全程餐饮 + 全部景点门票</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>非遗工坊材料费 + 书法课程</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>全程意外保险 + 接机送机</div>
        </div>
      </div>
      <!-- 7日6晚 -->
      <div style="background:white;border:1.5px solid var(--main);border-radius:16px;padding:32px 20px;text-align:center;position:relative;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.06);">
        <div style="position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--main),var(--amber));"></div>
        <div style="font-size:10px;letter-spacing:4px;color:var(--text-lighter);margin-bottom:12px;">行程方案二</div>
        <div style="font-size:18px;font-weight:700;color:var(--text);letter-spacing:1px;margin-bottom:6px;">7日6晚</div>
        <div style="font-size:36px;font-weight:700;color:var(--text);letter-spacing:1px;margin:16px 0 8px;">
          <span style="font-size:16px;font-weight:500;color:var(--main-dark);margin-right:2px;">¥</span>{price_7d}
        </div>
        <div style="font-size:11px;color:var(--text-light);margin-bottom:16px;">含国际往返机票（指定航班）及签证</div>
        <div style="text-align:left;font-size:11px;color:var(--text-mid);">
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>国际往返机票（指定航班）</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>中国签证办理</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>6晚四星级酒店住宿</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>全程餐饮 + AI创意课程费</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>非遗深度体验 + 名校科创</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>全程意外保险 + 接机送机</div>
        </div>
      </div>
      <!-- 14日13晚 -->
      <div style="background:white;border:1.5px solid var(--border);border-radius:16px;padding:32px 20px;text-align:center;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--main),var(--amber));"></div>
        <div style="font-size:10px;letter-spacing:4px;color:var(--text-lighter);margin-bottom:12px;">行程方案三</div>
        <div style="font-size:18px;font-weight:700;color:var(--text);letter-spacing:1px;margin-bottom:6px;">14日13晚</div>
        <div style="font-size:36px;font-weight:700;color:var(--text);letter-spacing:1px;margin:16px 0 8px;">
          <span style="font-size:16px;font-weight:500;color:var(--main-dark);margin-right:2px;">¥</span>{price_14d}
        </div>
        <div style="font-size:11px;color:var(--text-light);margin-bottom:16px;">含国际往返机票（指定航班）及签证</div>
        <div style="text-align:left;font-size:11px;color:var(--text-mid);">
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>国际往返机票（指定航班）</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>中国签证办理</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>13晚四星级酒店住宿</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>系统书法教育 + 深度非遗</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>AI创意全流程 + 多城文化</div>
          <div style="display:flex;align-items:center;gap:6px;padding:3px 0;"><div style="width:5px;height:5px;border-radius:50%;background:var(--main);flex-shrink:0;"></div>全程意外保险 + 接机送机</div>
        </div>
      </div>
    </div>
    <!-- 机票备注 -->
    <div style="background:var(--blue-light);border:1px solid rgba(74,158,184,0.2);border-radius:10px;padding:16px 20px;display:flex;align-items:center;gap:12px;margin-bottom:20px;">
      <div style="font-size:20px;flex-shrink:0;">✈️</div>
      <div style="font-size:13px;color:var(--blue-dark);line-height:1.6;"><strong>机票说明：</strong>报价含国际往返机票（指定航班），具体航班信息报名后统一通知。如需调整航班，请提前联系拓圈研学顾问。</div>
    </div>
    <!-- 价格备注 -->
    <div style="background:var(--amber-light);border:1px solid rgba(232,180,76,0.2);border-radius:10px;padding:16px 20px;display:flex;align-items:center;gap:12px;">
      <div style="font-size:20px;flex-shrink:0;">💡</div>
      <div style="font-size:13px;color:var(--amber-dark);line-height:1.6;font-weight:500;">报价为标准档价格，大咖定制内容另加费用。可根据需求定制专属研学方案。</div>
    </div>
  </div>
</div>
"""

# ===== 16个备选项目HTML =====
PROJECTS = """
<div class="page">
  <div style="padding:56px 0;">
    <div style="font-size:10px;letter-spacing:4px;color:var(--text-lighter);text-transform:uppercase;margin-bottom:8px;">Optional Programs</div>
    <div style="font-size:24px;font-weight:600;color:var(--text);letter-spacing:2px;margin-bottom:8px;">定制特色服务 · 备选项目</div>
    <div style="font-size:13px;color:var(--text-mid);line-height:1.8;margin-bottom:32px;max-width:600px;">除标准行程外，还可从以下16个精品研学项目中自由选择搭配，定制专属研学方案。</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">1</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">南京云锦研究所</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">国家级非遗，观摩大花楼木织机，动手制作云锦书签</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">2</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">金陵金箔</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">国家级非遗，观摩捶箔切箔，体验贴金DIY</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">3</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">苏州苏绣研究所</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">国家级苏绣非遗保护单位，学习劈丝针法</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">4</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">南通华艺集团</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">国家级文化产业示范基地，蓝印花布/扎染体验</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">5</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">南京1865创意产业园</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">金陵机器制造局遗址，AR工业考古体验</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">6</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">南航研学基地</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">航空航天科普，体验飞行模拟驾驶</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">7</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">苏州金龙（海格客车）</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">智能客车龙头，试乘自动驾驶小巴</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">8</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">卫岗乳业</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">百年中华老字号，DIY酸奶/奶片制作</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">9</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">镇江恒顺醋文化博物馆</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">国家4A级景区，体验原浆醋品鉴</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">10</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">苏州沙洲优黄文化园</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">江南黄酒文化地标，体验花雕酒坛彩绘</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">11</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">南京上汽南汽</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">南京老牌汽车工业基地，观摩新能源整车制造</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">12</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">元气森林江苏工厂</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">现代化无菌饮品工厂，饮品调配DIY</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">13</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">洋河酒厂</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">国家4A级景区，体验酿酒模拟/无醇调酒</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">14</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">今世缘</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">国家4A级景区，体验制曲/酒香香薰蜡烛DIY</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">15</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">观朴非遗木作</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">中式榫卯木作研学，实操鲁班锁拼装</div></div>
      </div>
      <div style="display:flex;gap:12px;padding:14px 16px;background:var(--paper-light);border:1px solid var(--border);border-radius:10px;align-items:flex-start;">
        <div style="width:24px;height:24px;border-radius:50%;background:var(--main);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">16</div>
        <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;">南京机器人科普教育基地</div><div style="font-size:11px;color:var(--text-light);line-height:1.5;">机器人+AI科普，观看机器狗表演</div></div>
      </div>
    </div>
  </div>
</div>
"""


REGIONS = [
    {"name": "港澳台",  "price_4d": "9,980", "price_7d": "15,980", "price_14d": "23,980"},
    {"name": "东盟",    "price_4d": "9,980", "price_7d": "15,980", "price_14d": "23,980"},
    {"name": "俄罗斯",  "price_4d": "9,980", "price_7d": "15,980", "price_14d": "23,980"},
    {"name": "欧洲大陆", "price_4d": "9,980", "price_7d": "15,980", "price_14d": "23,980"},
    {"name": "英国",    "price_4d": "9,980", "price_7d": "15,980", "price_14d": "23,980"},
    {"name": "美国",    "price_4d": "9,980", "price_7d": "15,980", "price_14d": "23,980"},
]


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {os.path.basename(path)}")


def process_template(template_html, region):
    """在模板基础上：改标题/封面，插入南京介绍、三档价格、16备选项目"""
    name = region["name"]
    html = template_html

    # 1. 替换<title>
    html = html.replace(
        "古都文脉探索营 · 海外4日3晚研学方案",
        f"古都文脉探索营 · {name}研学方案"
    )
    # 2. 替换封面文字
    html = html.replace("行走的课堂", name)
    html = html.replace(
        "4日3晚 · 海外学生中华文化研学之旅",
        f"{name} · 中华文化研学之旅"
    )
    html = html.replace(
        "International Study Program",
        f"International Study Program · {name}"
    )

    # 3. 在封面结束 </div> 后插入南京介绍
    # 找封面结束位置（cover-version那行之后）
    cover_end = html.find('<div class="cover-version">')
    if cover_end != -1:
        # 找到 cover-version 的 </div> 后面
        end_div = html.find('</div>', cover_end)
        if end_div != -1:
            insert_pos = end_div + 6  # </div> 长度=6
            html = html[:insert_pos] + "\n" + NANJING + html[insert_pos:]

    # 4. 删除旧的价格块（费用说明那整段），替换为三档价格
    price_start = html.find('<!-- ===== 费用说明 ===== -->')
    price_end = html.find('<!-- ===== 封底 ===== -->')
    if price_start != -1 and price_end != -1:
        new_price = get_pricing(region["price_4d"], region["price_7d"], region["price_14d"])
        html = html[:price_start] + new_price + "\n" + PROJECTS + html[price_end:]

    # 5. 替换封底文字
    html = html.replace("海外版", f"{name}版")
    html = html.replace("4日3晚", "三档行程")

    return html


def main():
    tpl_path = os.path.join(BASE_DIR, "拓圈研学·海外4日3晚·古都文脉探索营.html")
    print(f"读取模板: {tpl_path}")
    template = read_file(tpl_path)

    for region in REGIONS:
        name = region["name"]
        print(f"  生成: {name}...")
        out_html = process_template(template, region)
        out_path = os.path.join(BASE_DIR, f"拓圈研学·{name}·古都文脉探索营.html")
        write_file(out_path, out_html)

    print("\n✅ 全部生成完毕！")


if __name__ == "__main__":
    main()

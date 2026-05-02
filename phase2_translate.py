# -*- coding: utf-8 -*-
"""
Phase 2: Translate all study tour HTML files to English-only.
IMPORTANT: Already has correct prices from Phase 1. DO NOT touch ¥ patterns.
Strategy: read file, apply targeted string replacements (safe approach).
"""
import os, re

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

# ============================================================
# ENTRY PAGE TRANSLATIONS
# ============================================================

def translate_entry(filepath, region):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # lang
    c = c.replace('<html lang="zh-CN">', '<html lang="en">')

    # Title
    en_region = get_en_region(region)
    c = re.sub(r'<title>.*?</title>',
               f'<title>TOPOO Study Tour · {en_region} · Nanjing Cultural Camp</title>', c)

    # Cover eyebrow
    c = re.sub(r'<div class="cover-eyebrow">.*?</div>',
               '<div class="cover-eyebrow">Nanjing Cultural Camp</div>', c)

    # Cover title
    c = c.replace(f'<div class="cover-title">{region}</div>',
                  f'<div class="cover-title">{en_region}</div>')

    # Cover title accent
    c = re.sub(r'<span class="cover-title-accent">.*?</span>',
               f'<span class="cover-title-accent">{get_en_accent(region)}</span>', c)

    # Remove cover-title-en
    c = re.sub(r'\s*<span class="cover-title-en">.*?</span>', '', c)

    # Cover subtitle - remove Chinese part
    c = c.replace(
        '读万卷书，行万里路<br>在六朝古都中触摸中华文明的脉搏<br>\n    Read ten thousand books, walk ten thousand miles — Touch the pulse of Chinese civilization.',
        'Read ten thousand books, walk ten thousand miles.<br>Touch the pulse of Chinese civilization in the Ancient Capital of Six Dynasties.'
    )

    # Cover meta labels
    c = c.replace('适用学段 / Target', 'Target Group')
    c = c.replace('研学目的地 / Destination', 'Destination')
    c = c.replace('<div class="val">大学生</div>', '<div class="val">University</div>')
    c = c.replace('<div class="val">中小学生</div>', '<div class="val">K-12 Students</div>')

    # Cover version
    c = re.sub(r'<div class="cover-version">.*?</div>',
               f'<div class="cover-version">TOPOO STUDY TOUR · {en_region} · 2026</div>', c)

    # Nanjing section
    c = c.replace('City Profile / 城市介绍', 'City Profile')
    c = c.replace('南京城市介绍 / Nanjing City Profile', 'Nanjing City Profile')
    c = c.replace(
        '南京，江苏省省会，地处长江下游中部，是中国四大古都之一，有"六朝古都、十朝都会"之称。全市面积6587平方公里，常住人口约950万。<br>\n      Nanjing, capital of Jiangsu Province, is one of China\'s Four Great Ancient Capitals, known as the "Ancient Capital of Six Dynasties and Ten Regimes". Total area: 6,587 km\u00b2, permanent population: approx. 9.5 million.',
        'Nanjing, capital of Jiangsu Province, is one of China\'s Four Great Ancient Capitals, known as the "Ancient Capital of Six Dynasties and Ten Regimes". Total area: 6,587 km\u00b2, permanent population: approx. 9.5 million.'
    )

    # NJ card labels
    c = c.replace('历史地位 / Historical Status', 'Historical Status')
    c = c.replace('科教实力 / Education', 'Education')
    c = c.replace('地理气候 / Climate', 'Climate')
    c = c.replace('产业名片 / Industry', 'Industry')

    # NJ card values
    c = c.replace('六朝古都 · 十朝都会', 'Ancient Capital of Six Dynasties')
    c = c.replace(
        '近2500年建城史，450年建都史，与西安、洛阳、北京并称中国四大古都<br>Approx. 2,500 years of city history, 450 years as a capital',
        'Approx. 2,500 years of city history, 450 years as a capital — one of China\'s Four Great Ancient Capitals.'
    )
    c = c.replace('中国高等教育第三城', '3rd Largest Higher Education Hub in China')
    c = c.replace(
        '拥有53所高等院校，在校大学生超85万，仅次于北京、上海<br>53 universities, 850,000+ students — 3rd in China',
        '53 universities, 850,000+ students — ranked 3rd nationwide.'
    )
    c = c.replace('北亚热带湿润气候', 'Subtropical Humid Climate')
    c = c.replace(
        '四季分明，春秋宜人。年平均温度15.4°C，是理想研学目的地<br>Four distinct seasons, avg. temp 15.4\u00b0C — ideal for study tours',
        'Four distinct seasons with pleasant spring and autumn. Average temperature 15.4\u00b0C.'
    )
    c = c.replace('六朝古都 · 创新名城', 'Heritage City & Innovation Hub')
    c = c.replace(
        '拥有软件谷、江北新区等国家级园区，长三角特大城市<br>Home to Natl Software Valley, major Yangtze Delta city',
        'Home to the National Software Valley and Jiangbei New Area. A major Yangtze River Delta city.'
    )

    # Quote
    c = c.replace(
        '"江南佳丽地，金陵帝王州。" 南京——世界文学之都，联合国教科文组织"世界图书之都"。<br>\n      "Beautiful Jiangnan, imperial Jinling." Nanjing — UNESCO City of Literature.',
        '"Beautiful Jiangnan, imperial Jinling." Nanjing — UNESCO City of Literature.'
    )

    # Choose section
    c = c.replace('选择你的研学行程 / Choose Your Program', 'Choose Your Program')
    c = c.replace(
        '三大行程方案，按需选择，同样的文脉深度，不同的探索节奏。<br>Three programs, same cultural depth, different exploration rhythms.',
        'Three programs with the same cultural depth, but different exploration rhythms.'
    )

    # Duration labels
    c = c.replace('4日3晚 / 4Days3Nights', '4 Days 3 Nights')
    c = c.replace('7日6晚 / 7Days6Nights', '7 Days 6 Nights')
    c = c.replace('14日13晚 / 14Days13Nights', '14 Days 13 Nights')

    # Program names
    c = re.sub(r'<div class="choose-name">文脉初探<span class="choose-name-accent">.*?</span></div>',
               '<div class="choose-name">Cultural Primer</div>', c)
    c = re.sub(r'<div class="choose-name">深度探索<span class="choose-name-accent">.*?</span></div>',
               '<div class="choose-name">Deep Dive</div>', c)
    c = re.sub(r'<div class="choose-name">全面沉浸<span class="choose-name-accent">.*?</span></div>',
               '<div class="choose-name">Full Immersion</div>', c)

    # Tags
    c = c.replace('大学生 / University', 'University')
    c = c.replace('中小学生 / K-12', 'K-12 Students')
    c = c.replace('南京 / Nanjing', 'Nanjing')
    c = c.replace('中英双语 / Bilingual', 'Bilingual')

    # Price unit
    c = c.replace('/人 · per person', '/person')

    # View details
    c = c.replace('查看详情 / View Details', 'View Details')

    # Flight note
    c = c.replace(
        '<strong>机票说明 / Flight Info：</strong>往返机票需自行订购，或联系拓圈统一代订（指定航班）。报价不含往返南京大交通。<br>\n      Round-trip tickets can be self-booked or arranged by TOPOO (designated flights). Quotation excludes transport to/from Nanjing.',
        '<strong>Flight Info:</strong> Round-trip tickets can be self-booked or arranged by TOPOO (designated flights). Quotation excludes transport to/from Nanjing.'
    )

    # Price note
    c = c.replace(
        '报价为标准档价格，定制内容另加费用。可根据需求定制专属研学方案。<br>\n      Quotation is standard rate. Custom content incurs additional fees. Tailor-made programs available.',
        'Quotation is standard rate. Custom content incurs additional fees. Tailor-made programs available upon request.'
    )

    # Projects section
    c = c.replace('Optional Programs / 备选项目', 'Optional Programs')
    c = c.replace('定制特色服务 · 备选项目', 'Optional Premium Programs')
    c = c.replace(
        '除标准行程外，还可从以下16个精品研学项目中自由选择搭配，定制专属研学方案。<br>\n    In addition to the standard itinerary, choose from 16 curated programs to customize your study tour.',
        'In addition to the standard itinerary, choose from 16 curated programs to customize your study tour.'
    )

    # 16 project items
    projects = [
        ('南京云锦研究所 / Nanjing Yunjin', 'Nanjing Yunjin Institute',
         '国家级非遗，观摩大花楼木织机，动手制作云锦书签<br>Natl Intangible Heritage. Observe wooden looms, make bookmark',
         'National Intangible Heritage. Observe traditional wooden looms, hands-on brocade bookmark making.'),
        ('金陵金箔 / Jinling Gold Foil', 'Jinling Gold Foil',
         '国家级非遗，观摩捶箔切箔，体验贴金DIY<br>Natl Intangible Heritage. Gold foil hammering & 贴金 DIY',
         'National Intangible Heritage. Observe gold foil hammering & cutting, hands-on gilding DIY.'),
        ('苏州苏绣研究所 / Suzhou Embroidery', 'Suzhou Embroidery Institute',
         '国家级苏绣非遗保护单位，学习劈丝针法<br>Natl Suzhou embroidery. Learn splitting-silk technique',
         'National-level Suzhou Embroidery heritage site. Learn the art of silk splitting technique.'),
        ('南通华艺集团 / Nantong Huayi', 'Nantong Huayi Group',
         '国家级示范基地，蓝印花布/扎染体验<br>Natl demonstration base. Blue calico & tie-dye',
         'National demonstration base. Blue calico printing and tie-dye experience.'),
        ('南京1865创意产业园 / Nanjing 1865 Park', 'Nanjing 1865 Creative Park',
         '金陵机器制造局遗址，AR工业考古体验<br>Former arsenal site. AR industrial archaeology',
         'Former Jinling Arsenal site. AR-powered industrial archaeology experience.'),
        ('南航研学基地 / NUAA Base', 'NUAA Aerospace Base',
         '航空航天科普，体验飞行模拟驾驶<br>Aerospace science. Flight simulator experience',
         'Aerospace science education. Flight simulator hands-on experience.'),
        ('苏州金龙（海格客车）/ Suzhou Jinlong', 'Higer Bus (Suzhou)',
         '智能客车龙头，试乘自动驾驶小巴<br>Smart bus leader. Ride autonomous shuttle',
         'China\'s smart bus leader. Ride an autonomous shuttle bus.'),
        ('卫岗乳业 / Weigang Dairy', 'Weigang Dairy',
         '百年中华老字号，DIY酸奶/奶片制作<br>100-year-old brand. DIY yogurt & milk tablets',
         'Century-old heritage brand. DIY yogurt and milk tablet making.'),
        ('镇江恒顺醋文化博物馆 / Zhenjiang Vinegar Museum', 'Zhenjiang Vinegar Culture Museum',
         '国家4A级景区，体验原浆醋品鉴<br>Natl 4A scenic area. Original vinegar tasting',
         'National 4A scenic area. Original vinegar tasting experience.'),
        ('苏州沙洲优黄文化园 / Suzhou Rice Wine Park', 'Suzhou Rice Wine Culture Park',
         '江南黄酒文化地标，体验花雕酒坛彩绘<br>Jiangnan rice wine landmark. Wine jar painting',
         'Jiangnan rice wine cultural landmark. Paint your own Huadiao wine jar.'),
        ('南京上汽南汽 / SAIC Nanjing', 'SAIC Nanjing',
         '南京老牌汽车工业基地，观摩新能源制造<br>Legacy auto base. NEV manufacturing tour',
         'Legacy automotive base. New energy vehicle manufacturing tour.'),
        ('元气森林江苏工厂 / Genki Forest JS', 'Genki Forest Jiangsu Factory',
         '现代化无菌饮品工厂，饮品调配DIY<br>Modern aseptic plant. DIY drink blending',
         'Modern aseptic beverage factory. DIY drink blending experience.'),
        ('洋河酒厂 / Yanghe Distillery', 'Yanghe Distillery',
         '国家4A级景区，绵柔白酒国标制定者<br>Natl 4A. Mianrou baijiu standard-setter',
         'National 4A scenic area. Maker of China\'s mianrou baijiu standard.'),
        ('今世缘 / Jinshiyuan', 'Jinshiyuan Distillery',
         '国家4A级景区，"缘文化"主题体验<br>Natl 4A. "Yuan Culture" theme experience',
         'National 4A scenic area. "Yuan (Destiny) Culture" themed experience.'),
        ('观朴非遗木作 / Guanpu Woodwork', 'Guanpu Heritage Woodwork',
         '专注中式榫卯木作研学，鲁班锁拼装<br>Traditional mortise-tenon. Luban lock assembly',
         'Traditional Chinese mortise-and-tenon woodwork. Luban lock puzzle assembly.'),
        ('南京机器人科普教育基地 / Nanjing Robot Base', 'Nanjing Robot Education Base',
         '机器人与AI科普，机器狗表演体验<br>Robotics & AI popularization. Robot dog show',
         'Robotics and AI science education. Robot dog performance and interaction.'),
    ]
    for zh_t, en_t, zh_d, en_d in projects:
        pat = rf'<h5>{re.escape(zh_t)}</h5>\s*<p>{re.escape(zh_d)}</p>'
        c = re.sub(pat, f'<h5>{en_t}</h5><p>{en_d}</p>', c, flags=re.DOTALL)

    # Back cover
    c = c.replace('拓圈 / Topoo', 'Topoo')
    c = c.replace('让小而美被世界看见 / Let the Small and Beautiful Be Seen', 'Let the Small and Beautiful Be Seen')
    c = c.replace('本方案最终解释权归主办方所有<br>\n    Final interpretation right reserved by the organizer',
                  'Final interpretation right reserved by the organizer')

    # HTML comments
    c = c.replace('<!-- ===== 封面 / Cover ===== -->', '<!-- Cover -->')
    c = c.replace('<!-- ===== 南京城市介绍 ===== -->', '<!-- Nanjing -->')
    c = c.replace('<!-- ===== 选择行程 ===== -->', '<!-- Programs -->')
    c = c.replace('<!-- ===== 备选研学项目 ===== -->', '<!-- Optional -->')
    c = c.replace('<!-- ===== 封底 ===== -->', '<!-- Back Cover -->')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  Entry: {os.path.basename(filepath)}")

# ============================================================
# SUB PAGE TRANSLATIONS
# ============================================================

def translate_sub(filepath, region):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    dur = "4D3N"
    if "7日6晚" in filepath: dur = "7D6N"
    elif "14日13晚" in filepath: dur = "14D13N"
    en_region = get_en_region(region)

    # lang
    c = c.replace('<html lang="zh-CN">', '<html lang="en">')

    # Title
    c = re.sub(r'<title>.*?</title>',
               f'<title>TOPOO Study Tour · {en_region} · {dur} · Nanjing Cultural Camp</title>', c)

    # Cover eyebrow
    c = re.sub(r'<div class="cover-eyebrow">.*?</div>',
               '<div class="cover-eyebrow">Nanjing Cultural Camp</div>', c)

    # Cover title (region name)
    for cn, en in [("港澳台","Hong Kong, Macao & Taiwan"),("东盟","ASEAN"),("俄罗斯","Russia"),
                   ("欧洲大陆","Continental Europe"),("英国","United Kingdom"),("美国","United States")]:
        c = c.replace(f'<div class="cover-title">{cn}</div>', f'<div class="cover-title">{en}</div>')

    # Cover title accent
    c = re.sub(r'<span class="cover-title-accent">.*?</span>',
               f'<span class="cover-title-accent">{get_en_accent(region)}</span>', c)

    # Remove cover-title-en
    c = re.sub(r'\s*<span class="cover-title-en">.*?</span>', '', c)

    # Cover subtitle
    c = c.replace(
        '读万卷书，行万里路<br>在六朝古都中触摸中华文明的脉搏<br>\n    Read ten thousand books, walk ten thousand miles — Touch the pulse of Chinese civilization.',
        'Read ten thousand books, walk ten thousand miles.<br>Touch the pulse of Chinese civilization in the Ancient Capital of Six Dynasties.'
    )

    # Cover meta
    c = c.replace('适用学段 / Target', 'Target Group')
    c = c.replace('研学目的地 / Destination', 'Destination')
    c = c.replace('<div class="val">大学生</div>', '<div class="val">University</div>')
    c = c.replace('<div class="val">中小学生</div>', '<div class="val">K-12 Students</div>')

    # Cover version
    c = re.sub(r'<div class="cover-version">.*?</div>',
               f'<div class="cover-version">TOPOO STUDY TOUR · {en_region} · {dur} · 2026</div>', c)

    # === Nanjing section (same as entry) ===
    c = c.replace('City Profile / 城市介绍', 'City Profile')
    c = c.replace('南京城市介绍 / Nanjing City Profile', 'Nanjing City Profile')
    c = c.replace(
        '南京，江苏省省会，地处长江下游中部，是中国四大古都之一，有"六朝古都、十朝都会"之称。全市面积6587平方公里，常住人口约950万。<br>\n      Nanjing, capital of Jiangsu Province, is one of China\'s Four Great Ancient Capitals, known as the "Ancient Capital of Six Dynasties and Ten Regimes". Total area: 6,587 km\u00b2, permanent population: approx. 9.5 million.',
        'Nanjing, capital of Jiangsu Province, is one of China\'s Four Great Ancient Capitals, known as the "Ancient Capital of Six Dynasties and Ten Regimes". Total area: 6,587 km\u00b2, permanent population: approx. 9.5 million.'
    )
    c = c.replace('历史地位 / Historical Status', 'Historical Status')
    c = c.replace('科教实力 / Education', 'Education')
    c = c.replace('地理气候 / Climate', 'Climate')
    c = c.replace('产业名片 / Industry', 'Industry')
    c = c.replace('六朝古都 · 十朝都会', 'Ancient Capital of Six Dynasties')
    c = c.replace(
        '近2500年建城史，450年建都史，与西安、洛阳、北京并称中国四大古都<br>Approx. 2,500 years of city history, 450 years as a capital',
        'Approx. 2,500 years of city history, 450 years as a capital — one of China\'s Four Great Ancient Capitals.'
    )
    c = c.replace('中国高等教育第三城', '3rd Largest Higher Education Hub in China')
    c = c.replace(
        '拥有53所高等院校，在校大学生超85万，仅次于北京、上海<br>53 universities, 850,000+ students — 3rd in China',
        '53 universities, 850,000+ students — ranked 3rd nationwide.'
    )
    c = c.replace('北亚热带湿润气候', 'Subtropical Humid Climate')
    c = c.replace(
        '四季分明，春秋宜人。年平均温度15.4°C，是理想研学目的地<br>Four distinct seasons, avg. temp 15.4\u00b0C — ideal for study tours',
        'Four distinct seasons with pleasant spring and autumn. Average temperature 15.4\u00b0C.'
    )
    c = c.replace('六朝古都 · 创新名城', 'Heritage City & Innovation Hub')
    c = c.replace(
        '拥有软件谷、江北新区等国家级园区，长三角特大城市<br>Home to Natl Software Valley, major Yangtze Delta city',
        'Home to the National Software Valley and Jiangbei New Area. A major Yangtze River Delta city.'
    )
    c = c.replace(
        '"江南佳丽地，金陵帝王州。" 南京——世界文学之都，联合国教科文组织"世界图书之都"。<br>\n      "Beautiful Jiangnan, imperial Jinling." Nanjing — UNESCO City of Literature.',
        '"Beautiful Jiangnan, imperial Jinling." Nanjing — UNESCO City of Literature.'
    )

    # === Projects section (same as entry) ===
    c = c.replace('Optional Programs / 备选项目', 'Optional Programs')
    c = c.replace('定制特色服务 · 备选项目', 'Optional Premium Programs')
    c = c.replace(
        '除标准行程外，还可从以下16个精品研学项目中自由选择搭配，定制专属研学方案。<br>\n    In addition to the standard itinerary, choose from 16 curated programs to customize your study tour.',
        'In addition to the standard itinerary, choose from 16 curated programs to customize your study tour.'
    )

    projects = [
        ('南京云锦研究所 / Nanjing Yunjin', 'Nanjing Yunjin Institute',
         '国家级非遗，观摩大花楼木织机，动手制作云锦书签<br>Natl Intangible Heritage. Observe wooden looms, make bookmark',
         'National Intangible Heritage. Observe traditional wooden looms, hands-on brocade bookmark making.'),
        ('金陵金箔 / Jinling Gold Foil', 'Jinling Gold Foil',
         '国家级非遗，观摩捶箔切箔，体验贴金DIY<br>Natl Intangible Heritage. Gold foil hammering & 贴金 DIY',
         'National Intangible Heritage. Observe gold foil hammering & cutting, hands-on gilding DIY.'),
        ('苏州苏绣研究所 / Suzhou Embroidery', 'Suzhou Embroidery Institute',
         '国家级苏绣非遗保护单位，学习劈丝针法<br>Natl Suzhou embroidery. Learn splitting-silk technique',
         'National-level Suzhou Embroidery heritage site. Learn the art of silk splitting technique.'),
        ('南通华艺集团 / Nantong Huayi', 'Nantong Huayi Group',
         '国家级示范基地，蓝印花布/扎染体验<br>Natl demonstration base. Blue calico & tie-dye',
         'National demonstration base. Blue calico printing and tie-dye experience.'),
        ('南京1865创意产业园 / Nanjing 1865 Park', 'Nanjing 1865 Creative Park',
         '金陵机器制造局遗址，AR工业考古体验<br>Former arsenal site. AR industrial archaeology',
         'Former Jinling Arsenal site. AR-powered industrial archaeology experience.'),
        ('南航研学基地 / NUAA Base', 'NUAA Aerospace Base',
         '航空航天科普，体验飞行模拟驾驶<br>Aerospace science. Flight simulator experience',
         'Aerospace science education. Flight simulator hands-on experience.'),
        ('苏州金龙（海格客车）/ Suzhou Jinlong', 'Higer Bus (Suzhou)',
         '智能客车龙头，试乘自动驾驶小巴<br>Smart bus leader. Ride autonomous shuttle',
         'China\'s smart bus leader. Ride an autonomous shuttle bus.'),
        ('卫岗乳业 / Weigang Dairy', 'Weigang Dairy',
         '百年中华老字号，DIY酸奶/奶片制作<br>100-year-old brand. DIY yogurt & milk tablets',
         'Century-old heritage brand. DIY yogurt and milk tablet making.'),
        ('镇江恒顺醋文化博物馆 / Zhenjiang Vinegar Museum', 'Zhenjiang Vinegar Culture Museum',
         '国家4A级景区，体验原浆醋品鉴<br>Natl 4A scenic area. Original vinegar tasting',
         'National 4A scenic area. Original vinegar tasting experience.'),
        ('苏州沙洲优黄文化园 / Suzhou Rice Wine Park', 'Suzhou Rice Wine Culture Park',
         '江南黄酒文化地标，体验花雕酒坛彩绘<br>Jiangnan rice wine landmark. Wine jar painting',
         'Jiangnan rice wine cultural landmark. Paint your own Huadiao wine jar.'),
        ('南京上汽南汽 / SAIC Nanjing', 'SAIC Nanjing',
         '南京老牌汽车工业基地，观摩新能源制造<br>Legacy auto base. NEV manufacturing tour',
         'Legacy automotive base. New energy vehicle manufacturing tour.'),
        ('元气森林江苏工厂 / Genki Forest JS', 'Genki Forest Jiangsu Factory',
         '现代化无菌饮品工厂，饮品调配DIY<br>Modern aseptic plant. DIY drink blending',
         'Modern aseptic beverage factory. DIY drink blending experience.'),
        ('洋河酒厂 / Yanghe Distillery', 'Yanghe Distillery',
         '国家4A级景区，绵柔白酒国标制定者<br>Natl 4A. Mianrou baijiu standard-setter',
         'National 4A scenic area. Maker of China\'s mianrou baijiu standard.'),
        ('今世缘 / Jinshiyuan', 'Jinshiyuan Distillery',
         '国家4A级景区，"缘文化"主题体验<br>Natl 4A. "Yuan Culture" theme experience',
         'National 4A scenic area. "Yuan (Destiny) Culture" themed experience.'),
        ('观朴非遗木作 / Guanpu Woodwork', 'Guanpu Heritage Woodwork',
         '专注中式榫卯木作研学，鲁班锁拼装<br>Traditional mortise-tenon. Luban lock assembly',
         'Traditional Chinese mortise-and-tenon woodwork. Luban lock puzzle assembly.'),
        ('南京机器人科普教育基地 / Nanjing Robot Base', 'Nanjing Robot Education Base',
         '机器人与AI科普，机器狗表演体验<br>Robotics & AI popularization. Robot dog show',
         'Robotics and AI science education. Robot dog performance and interaction.'),
    ]
    for zh_t, en_t, zh_d, en_d in projects:
        pat = rf'<h5>{re.escape(zh_t)}</h5>\s*<p>{re.escape(zh_d)}</p>'
        c = re.sub(pat, f'<h5>{en_t}</h5><p>{en_d}</p>', c, flags=re.DOTALL)

    # === Itinerary section ===
    c = c.replace('行程概览 / Itinerary Overview', 'Itinerary Overview')
    c = c.replace('行程概览 · 每日亮点', 'Itinerary Overview — Daily Highlights')

    # Day headers
    c = re.sub(r'第(\d+)天 / Day (\d+)', r'Day \2', c)
    c = re.sub(r'第(\d+)天', r'Day \1', c)

    # Time slots
    c = c.replace('上午 / Morning', 'Morning')
    c = c.replace('下午 / Afternoon', 'Afternoon')
    c = c.replace('晚上 / Evening', 'Evening')
    c = c.replace('全天 / Full Day', 'Full Day')

    # Bilingual itinerary items - replace "Chinese text<br>English text" with just English
    # Pattern: Chinese paragraph<br>English paragraph
    c = re.sub(
        r'([\u4e00-\u9fff][\u4e00-\u9fff\s，。、；：（）·""''！？\d°C]+)<br>([A-Z][A-Za-z][A-Za-z\s,.\'&\(\)\d°C\-]+)',
        r'\2',
        c
    )

    # Section headers (bilingual -> English)
    section_headers = [
        '费用包含 / What\'s Included', '住宿 / Accommodation', '餐饮 / Meals',
        '交通 / Transport', '门票 / Tickets', '课程 / Programs', '保险 / Insurance',
        '费用不含 / What\'s Not Included', '签证 / Visa', '个人消费 / Personal Expenses',
        '服务保障 / Our Services', '师生配比 / Teacher-Student Ratio',
        '安全措施 / Safety Measures', '应急机制 / Emergency Response',
        '安全保障 / Safety Assurance', '注意事项 / Important Notes',
        '退改政策 / Cancellation Policy', '报名须知 / Registration Notes',
        '行前准备 / Pre-departure Prep', '服务标准 / Service Standards',
    ]
    for h in section_headers:
        parts = h.split(' / ')
        if len(parts) == 2:
            c = c.replace(h, parts[1])

    # Specific Chinese text replacements in include/service areas
    text_items = [
        ('四星级酒店标准间（含早）', '4-star hotel standard room (breakfast included)'),
        ('研学期间所有课程、讲座、体验活动费用', 'All programs, lectures, and activities during the tour'),
        ('研学期间所有景点门票', 'All attraction tickets during the tour'),
        ('全程中文/英文双语导师', 'Bilingual Chinese/English tour leader throughout'),
        ('全程跟拍摄影', 'Professional photographer throughout'),
        ('全程跟拍摄影师', 'Professional photographer throughout'),
        ('定制研学手册', 'Custom study tour handbook'),
        ('定制研学服装', 'Custom study tour T-shirt'),
        ('研学证书', 'Study tour certificate'),
        ('活动相册', 'Photo album'),
        ('视频集锦', 'Video highlights'),
        ('往返南京交通费用', 'Round-trip transport to/from Nanjing'),
        ('签证费用', 'Visa fees'),
        ('个人消费', 'Personal expenses'),
        ('行李超重费', 'Excess baggage fees'),
        ('研学行程外的自费项目', 'Activities outside the program'),
        ('不可抗力导致的额外费用', 'Additional costs from force majeure'),
        ('1:8 师生配比', '1:8 teacher-student ratio'),
        ('全程专业导师陪同', 'Professional tour leader throughout'),
        ('24小时应急联络', '24-hour emergency contact'),
        ('全程旅游意外险', 'Travel accident insurance throughout'),
        ('出发前7天可全额退款', 'Full refund available 7 days before departure'),
        ('出发前3-7天退款50%', '50% refund for cancellation 3-7 days before departure'),
        ('出发前3天内不可退款', 'No refund within 3 days of departure'),
        ('需提前30天报名', 'Registration required 30 days in advance'),
        ('行前线上说明', 'Pre-departure online briefing'),
        ('出发前线上家长说明会', 'Pre-departure online parent briefing'),
        ('结营成果邮寄', 'Post-camp materials mailing'),
        ('研学证书+活动相册+作品集', 'Certificate + photo album + portfolio'),
        ('安全保障说明', 'Safety Assurance'),
        ('全程配备急救包', 'First-aid kit throughout'),
        ('每团配备1名安全员', '1 safety officer per group'),
        ('合作医院绿色通道', 'Partner hospital fast-track access'),
        ('价格 / Price', 'Price'),
    ]
    for zh, en in text_items:
        c = c.replace(zh, en)

    # Fix specific Chinese section headers that might remain
    c = re.sub(r'住宿说明[^<]*', 'Accommodation Details', c)
    c = re.sub(r'餐饮说明[^<]*', 'Meal Arrangements', c)
    c = re.sub(r'交通说明[^<]*', 'Transportation', c)

    # Itinerary day themes (bilingual -> English)
    themes = [
        ('抵达 / Arrival', 'Arrival'), ('古都初见 / First Glimpse', 'First Glimpse of the Ancient Capital'),
        ('文脉深探 / Deep Dive', 'Deep Dive into Cultural Heritage'),
        ('文脉溯源 / Tracing Roots', 'Tracing Cultural Roots'),
        ('古城漫游 / City Walk', 'Ancient City Walking Tour'),
        ('非遗体验 / Heritage Crafts', 'Intangible Heritage Experience'),
        ('创新南京 / Innovation Nanjing', 'Innovation Nanjing'),
        ('创新之都 / Innovation Hub', 'Innovation Hub'),
        ('名校探访 / University Visit', 'University Visit'),
        ('名校交流 / University Exchange', 'University Exchange'),
        ('结营仪式 / Closing Ceremony', 'Closing Ceremony'),
        ('文化交融 / Cultural Fusion', 'Cultural Fusion'),
        ('自由探索 / Free Exploration', 'Free Exploration'),
        ('返程 / Departure', 'Departure'),
        ('自由活动 / Free Day', 'Free Day'),
        ('江南水乡 / Jiangnan Water Town', 'Jiangnan Water Town'),
        ('长江印象 / Yangtze Impressions', 'Yangtze River Impressions'),
        ('六朝风华 / Six Dynasties Splendor', 'Splendor of the Six Dynasties'),
        ('秦淮灯影 / Qinhuai Lanterns', 'Qinhuai Lantern Night'),
        ('钟山秋色 / Purple Mountain', 'Purple Mountain Scenery'),
        ('秦淮河夜游 / Qinhuai Night Cruise', 'Qinhuai River Night Cruise'),
        ('现代南京 / Modern Nanjing', 'Modern Nanjing'),
        ('科技前沿 / Tech Frontier', 'Tech Frontier'),
        ('创意南京 / Creative Nanjing', 'Creative Nanjing'),
        ('创意工坊 / Creative Workshop', 'Creative Workshop'),
        ('夜游秦淮 / Night Qinhuai', 'Night Tour along Qinhuai River'),
        ('毕业典礼 / Graduation', 'Graduation Ceremony'),
        ('总结分享 / Sharing & Reflection', 'Sharing & Reflection'),
        ('总结反思 / Reflection', 'Reflection'),
        ('文化深度体验 / Deep Cultural Experience', 'Deep Cultural Experience'),
        ('全日研学 / Full-Day Program', 'Full-Day Program'),
        ('名校参访 / Campus Tour', 'Campus Tour'),
        ('博物馆日 / Museum Day', 'Museum Day'),
        ('社会实践 / Social Practice', 'Social Practice'),
        ('拓展活动 / Team Building', 'Team Building'),
        ('文化考察 / Cultural Exploration', 'Cultural Exploration'),
        ('自然探索 / Nature Exploration', 'Nature Exploration'),
        ('研学总结 / Program Summary', 'Program Summary'),
        ('长江文化 / Yangtze Culture', 'Yangtze River Culture'),
        ('非遗手作 / Heritage Handicraft', 'Heritage Handicraft Workshop'),
        ('科教探索 / Science & Education', 'Science & Education Exploration'),
        ('创意产业 / Creative Industry', 'Creative Industry Visit'),
        ('文艺南京 / Artistic Nanjing', 'Artistic Nanjing'),
        ('美食探索 / Culinary Exploration', 'Culinary Exploration'),
        ('离别 / Farewell', 'Farewell'),
        ('中山陵 / Sun Yat-sen Mausoleum', 'Sun Yat-sen Mausoleum'),
        ('夫子庙 / Confucius Temple', 'Confucius Temple'),
        ('秦淮河 / Qinhuai River', 'Qinhuai River'),
        ('明城墙 / Ming City Wall', 'Ming City Wall'),
        ('科举文化 / Imperial Examination', 'Imperial Examination Culture'),
    ]
    for zh, en in themes:
        c = c.replace(zh, en)

    # Itinerary place names (bilingual -> English)
    places = [
        ('接机/接站 · 入住酒店', 'Airport/Station pickup · Hotel check-in'),
        ('接机 / 入住酒店', 'Airport pickup · Hotel check-in'),
        ('入住南京酒店', 'Check in at Nanjing hotel'),
        ('中山陵景区', 'Sun Yat-sen Mausoleum Scenic Area'),
        ('明孝陵', 'Ming Xiaoling Mausoleum'),
        ('明城墙（中华门段）', 'Ming City Wall (Zhonghua Gate Section)'),
        ('夫子庙秦淮风光带', 'Confucius Temple & Qinhuai Scenic Area'),
        ('南京博物院', 'Nanjing Museum'),
        ('总统府', 'Presidential Palace'),
        ('侵华日军南京大屠杀遇难同胞纪念馆', 'The Memorial Hall of the Victims in Nanjing Massacre'),
        ('南京云锦研究所', 'Nanjing Yunjin Institute'),
        ('南京大学', 'Nanjing University'),
        ('东南大学', 'Southeast University'),
        ('南京航空航天大学', 'Nanjing University of Aeronautics and Astronautics'),
        ('南京1865创意产业园', 'Nanjing 1865 Creative Park'),
        ('老门东历史街区', 'Laomendong Historic District'),
        ('南京科技馆', 'Nanjing Science and Technology Museum'),
        ('红山森林动物园', 'Hongshan Forest Zoo'),
        ('玄武湖公园', 'Xuanwu Lake Park'),
        ('鸡鸣寺', 'Jiming Temple'),
        ('阅江楼', 'Yuejiang Tower'),
        ('南京大牌档', 'Nanjing Da Pai Dang (Restaurant)'),
        ('老门东', 'Laomendong'),
        ('先锋书店', 'Librairie Avant-Garde'),
        ('科举博物馆', 'Imperial Examination Museum'),
        ('江南贡院', 'Jiangnan Examination Hall'),
        ('中华门瓮城', 'Zhonghua Gate Fortress'),
        ('瞻园', 'Zhanyuan Garden'),
        ('甘熙故居', 'Ganxi Mansion'),
        ('南京眼步行桥', 'Nanjing Eye Pedestrian Bridge'),
        ('青奥村', 'Youth Olympic Village'),
        ('河西新城', 'Hexi New City'),
        ('颐和路', 'Yihe Road Historic Area'),
        ('汤山温泉', 'Tangshan Hot Springs'),
        ('牛首山', 'Niushoushan Cultural Park'),
        ('紫金山', 'Purple Mountain (Zijinshan)'),
        ('栖霞山', 'Qixia Mountain'),
        ('美龄宫', 'Meiling Palace'),
        ('音乐台', 'Music Stage'),
        ('灵谷寺', 'Linggu Temple'),
        ('明故宫遗址', 'Ming Palace Ruins'),
        ('石头城', 'Stone City'),
        ('南京条约史料陈列馆', 'Nanjing Treaty Historical Exhibition'),
        ('渡江胜利纪念馆', 'Yangtze River Crossing Victory Memorial'),
        ('雨花台', 'Yuhuatai Memorial Park'),
        ('南京眼', 'Nanjing Eye Bridge'),
        ('老门东美食街', 'Laomendong Food Street'),
        ('科举文化体验', 'Imperial Examination Culture Experience'),
        ('非遗手工体验', 'Intangible Heritage Craft Experience'),
        ('大学交流分享', 'University Exchange & Sharing'),
        ('校园参观', 'Campus Tour'),
        ('教授讲座', 'Guest Lecture'),
        ('学生交流', 'Student Exchange Session'),
        ('结营仪式 · 颁发证书', 'Closing Ceremony & Certificate Presentation'),
        ('送机/送站', 'Airport/Station drop-off'),
        ('自由活动 · 推荐游览', 'Free time · Recommended visits'),
        ('自由活动', 'Free Time'),
        ('夜游', 'Night Tour'),
        ('秦淮画舫', 'Qinhuai Painted Boat Cruise'),
        ('江南贡院历史陈列馆', 'Jiangnan Examination Hall Museum'),
        ('南京中国传统建筑', 'Traditional Chinese Architecture in Nanjing'),
        ('南京城市规划', 'Nanjing Urban Planning'),
        ('南京科技创新', 'Nanjing Tech Innovation'),
        ('四星级酒店标准间（含早）/ 4-star hotel (breakfast included)', '4-star hotel standard room (breakfast included)'),
    ]
    for zh, en in places:
        # Replace bilingual "ZH / EN" pattern
        c = re.sub(rf'{re.escape(zh)}\s*/\s*[A-Za-z][A-Za-z\s,.\'&\(\)\d\-]+', en, c)
        # Also replace standalone Chinese
        c = c.replace(zh, en)

    # Back cover
    c = c.replace('拓圈 / Topoo', 'Topoo')
    c = c.replace('让小而美被世界看见 / Let the Small and Beautiful Be Seen', 'Let the Small and Beautiful Be Seen')
    c = c.replace('本方案最终解释权归主办方所有<br>\n    Final interpretation right reserved by the organizer',
                  'Final interpretation right reserved by the organizer')
    c = c.replace('本方案最终解释权归主办方所有\nFinal interpretation right reserved by the organizer',
                  'Final interpretation right reserved by the organizer')
    c = c.replace('本方案最终解释权归主办方所有', 'Final interpretation right reserved by the organizer')

    # HTML comments
    c = re.sub(r'<!--\s*=====.*?=====\s*-->', '', c)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"  Sub: {os.path.basename(filepath)}")


def get_en_region(region):
    return {"港澳台":"HK, Macao & Taiwan","东盟":"ASEAN","俄罗斯":"Russia",
            "欧洲大陆":"Continental Europe","英国":"United Kingdom","美国":"United States",
            "国内中小学生":"Domestic K-12"}.get(region, region)

def get_en_accent(region):
    return {"港澳台":"Chinese Culture Study Tour for University Students",
            "东盟":"Cultural Exchange Study Tour for University Students",
            "俄罗斯":"Culture & Innovation Study Tour for University Students",
            "欧洲大陆":"Heritage & Innovation Study Tour for University Students",
            "英国":"British Culture & Education Study Tour for University Students",
            "美国":"American Innovation & Culture Study Tour for University Students",
            }.get(region, "Study Tour for University Students")


def main():
    entries = [
        ("拓圈研学·港澳台·入口页.html", "港澳台"),
        ("拓圈研学·东盟·入口页.html", "东盟"),
        ("拓圈研学·俄罗斯·入口页.html", "俄罗斯"),
        ("拓圈研学·欧洲大陆·入口页.html", "欧洲大陆"),
        ("拓圈研学·英国·入口页.html", "英国"),
        ("拓圈研学·美国·入口页.html", "美国"),
        ("拓圈研学·国内中小学生·入口页.html", "国内中小学生"),
    ]
    subs = []
    for r in ["港澳台","东盟","俄罗斯","欧洲大陆","英国","美国"]:
        for d in ["4日3晚","7日6晚","14日13晚"]:
            subs.append((f"拓圈研学·{r}·{d}·古都文脉探索营.html", r))

    print("=== Translating entry pages ===")
    for f, r in entries:
        translate_entry(os.path.join(BASE, f), r)

    print("\n=== Translating sub pages ===")
    for f, r in subs:
        translate_sub(os.path.join(BASE, f), r)

    print("\n=== All done! ===")

if __name__ == "__main__":
    main()

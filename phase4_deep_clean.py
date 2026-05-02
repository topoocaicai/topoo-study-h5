# -*- coding: utf-8 -*-
"""
Phase 4: Deep cleanup of remaining Chinese in sub-pages.
"""
import os, re, glob

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"

def has_many_cn(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s)) >= 3

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # CSS comments
    css_map = {
        '/* 本方案主色 = 土 */': '/* Main accent color */',
        '/* ===== 内容区通用 ===== */': '/* Content area */',
        '/* ===== 行程时间轴 ===== */': '/* Timeline */',
        '/* ===== 概览卡片 ===== */': '/* Overview cards */',
        '/* ===== 课程亮点 ===== */': '/* Highlights */',
        '/* ===== 价格 ===== */': '/* Pricing */',
        '/* ===== 引言 ===== */': '/* Introduction */',
        '/* ===== 安全保障 ===== */': '/* Safety */',
        '/* ===== 服务标准 ===== */': '/* Service standards */',
        '/* ===== 退改政策 ===== */': '/* Cancellation */',
        '/* ===== 费用说明 ===== */': '/* Fees */',
        '/* 封面 */': '/* Cover */',
        '/* 城市介绍 */': '/* City profile */',
        '/* 备选项目 */': '/* Optional programs */',
    }
    for zh, en in css_map.items():
        c = c.replace(zh, en)

    # Cover subtitle
    c = c.replace(
        '在六朝古都中触摸中华文明脉搏<br>让世界看见中国文化的厚度与温度<br>Same Roots, Shared Heritage',
        'Touch the pulse of Chinese civilization in the Ancient Capital.<br>Experience the depth and warmth of Chinese culture.<br>Same Roots, Shared Heritage.'
    )

    # Cover meta - pure Chinese labels
    c = re.sub(r'<div class="val">(\d+)<span class="unit">天</span>(\d+)<span class="unit">晚</span></div>',
               r'<div class="val">\1 Days \2 Nights</div>', c)
    c = c.replace('<div class="label">行程时长</div>', '<div class="label">Duration</div>')
    c = c.replace('<div class="label">适用学段</div>', '<div class="label">Target Group</div>')
    c = c.replace('<div class="label">研学目的地</div>', '<div class="label">Destination</div>')
    c = c.replace('<div class="label">含机票签证</div>', '<div class="label">Flights & Visa Included</div>')
    c = c.replace('<div class="val">大学生 / University</div>', '<div class="val">University</div>')
    c = c.replace('<div class="val">中小学生</div>', '<div class="val">K-12 Students</div>')
    c = c.replace('<div class="val">南京</div>', '<div class="val">Nanjing</div>')
    c = re.sub(r'<span class="unit">元</span>', '', c)

    # Section titles
    for zh, en in [
        ('项目概述','Program Overview'),('行程亮点','Program Highlights'),
        ('课程特色','Course Features'),('安全与保障','Safety & Assurance'),
        ('服务标准','Service Standards'),('退改政策','Cancellation Policy'),
        ('报名须知','Registration Notes'),('费用说明','Fee Details'),
        ('联系我们','Contact Us'),('行程安排','Itinerary'),
        ('每日亮点','Daily Highlights'),('备选项目','Optional Programs'),
        ('服务保障','Service Guarantee'),
    ]:
        c = c.replace(f'<div class="section-title">{zh}</div>', f'<div class="section-title">{en}</div>')
        c = c.replace(f'>{zh}</', f'>{en}</')

    # OC labels
    for zh, en in [
        ('项目名称','Program Name'),('适用对象','Target Participants'),
        ('行程规模','Group Size'),('研学城市','Study City'),
        ('项目类型','Program Type'),('住宿标准','Accommodation'),
        ('课程语言','Language'),('交通方式','Transportation'),
        ('成团人数','Min. Group Size'),
    ]:
        c = c.replace(f'<div class="oc-label">{zh}</div>', f'<div class="oc-label">{en}</div>')

    # OC values
    c = c.replace('古都文脉探索营 · 南京站', 'Ancient Capital Cultural Camp - Nanjing')
    c = c.replace('面向海外学生的中华文化沉浸式研学项目（大中小学通用版）',
                  'Immersive Chinese culture study program for international students')
    c = c.replace('HK, Macao & Taiwan大学生 / University Students from HK, Macao & Taiwan',
                  'University Students from HK, Macao & Taiwan')
    c = c.replace('新加坡、柬埔寨、俄罗斯等国学生通用，按年龄段分层活动',
                  'Suitable for students from Singapore, Cambodia, Russia, etc.')
    c = c.replace('含国际往返机票及中国签证办理，全程落地接待',
                  'Includes international flights, China visa, full reception')
    c = c.replace('世界文学之都，六朝古都，联合国教科文组织"世界图书之都"',
                  'UNESCO City of Literature, Ancient Capital of Six Dynasties')

    # Pure Chinese paragraphs
    c = c.replace(
        '面向海外大小学学生，以南京千年文脉为载体，通过沉浸式实地探访、非遗手作体验、书法教育实践、AI创意实践和中外文化交流，构建一场有深度、有温度、有成果的中华文化研学之旅。',
        'An immersive Chinese culture study program in Nanjing. Through on-site explorations, heritage workshops, calligraphy, AI creative labs, and cross-cultural exchanges.'
    )
    c = c.replace(
        '"江南佳丽地，金陵帝王州。" 南京——世界文学之都，十朝都会，450年建都史，每一块砖瓦都是中华文明的注脚。',
        '"Beautiful Jiangnan, imperial Jinling." Nanjing — UNESCO City of Literature, 450 years of capital history.'
    )

    # Bilingual "Chinese<br>English" -> English
    cn_chars = '\u4e00-\u9fff'
    cn_punct = '\uff0c\u3002\uff1b\uff1a\uff08\uff09\xb7\u201c\u201d\u2018\u2019\uff01\uff1f'
    c = re.sub(
        rf'([{cn_chars}][{cn_chars}{cn_punct}\s\d\u00b0C]+)\s*<br>\s*([A-Z][A-Za-z0-9\s,.\'&\(\)/\-\u00b0C]+)',
        lambda m: m.group(2) if has_many_cn(m.group(1)) else m.group(0),
        c
    )

    # Bilingual "Chinese / English" -> English
    c = re.sub(
        rf'([{cn_chars}][{cn_chars}{cn_punct}\s\d\u00b0C]+)\s*/\s*([A-Z][A-Za-z0-9\s,.\'&\(\)/\-\u00b0C]+)',
        lambda m: m.group(2) if has_many_cn(m.group(1)) else m.group(0),
        c
    )

    # UI text
    for zh, en in [
        ('查看详情','View Details'),('返回入口','Back'),('返回总览','Overview'),
        ('下载完整方案','Download'),('立即报名','Register Now'),('咨询详情','Inquire'),
        ('了解更多','Learn More'),('报名咨询','Contact'),('扫码报名','Scan to Register'),
        ('名额有限','Limited Spots'),('早鸟优惠','Early Bird'),('品质研学','Quality Tour'),
        ('全程跟拍','Photography'),('专属客服','Support'),('小班教学','Small Class'),
        ('证书颁发','Certificate'),('温馨提示','Note'),('注意事项','Important Notes'),
        ('往期反馈','Feedback'),('学员评价','Reviews'),('精彩瞬间','Highlights'),
        ('携带物品','What to Bring'),('着装建议','Dress Code'),('紧急联系','Emergency'),
        ('保险说明','Insurance'),('退款说明','Refund Policy'),('成团说明','Group Info'),
        ('接机说明','Pickup Info'),('特别说明','Special Notes'),
    ]:
        c = c.replace(f'>{zh}<', f'>{en}<')

    # Day headers
    c = re.sub(r'第(\d+)天', r'Day \1', c)
    c = c.replace('上午 / Morning', 'Morning')
    c = c.replace('下午 / Afternoon', 'Afternoon')
    c = c.replace('晚上 / Evening', 'Evening')
    c = c.replace('全天 / Full Day', 'Full Day')

    # Back cover
    c = c.replace('本方案最终解释权归主办方所有', 'Final interpretation right reserved by the organizer')

    # Remove Chinese HTML comments
    c = re.sub(r'<!--\s*[^-]*[\u4e00-\u9fff]+[^-]*\s*-->', '', c)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)

    c_check = re.sub(r'(?:href|src)="[^"]*"', '', c)
    return len(re.findall(r'[\u4e00-\u9fff]', c_check))

def main():
    for region in ["港澳台", "东盟", "俄罗斯", "欧洲大陆", "英国", "美国"]:
        for dur in ["4日3晚", "7日6晚", "14日13晚"]:
            fname = f"拓圈研学·{region}·{dur}·古都文脉探索营.html"
            fpath = os.path.join(BASE, fname)
            if os.path.exists(fpath):
                r = clean_file(fpath)
                print(f"  {fname}: {r} Chinese chars left")

    for region in ["港澳台", "东盟", "俄罗斯", "欧洲大陆", "英国", "美国"]:
        fname = f"拓圈研学·{region}·入口页.html"
        fpath = os.path.join(BASE, fname)
        if os.path.exists(fpath):
            r = clean_file(fpath)
            if r > 0:
                print(f"  {fname}: {r} Chinese chars left")

    print("\n=== Phase 4 Done ===")

if __name__ == "__main__":
    main()

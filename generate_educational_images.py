import os, math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('assets/img', exist_ok=True)
font_path = 'C:/Windows/Fonts/msjh.ttc'

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(font_path, size, index=1 if bold else 0)
    except:
        return ImageFont.load_default()

def create_card(title, tag, color_theme, width=800, height=520):
    im = Image.new('RGB', (width, height), (250, 250, 252))
    d = ImageDraw.Draw(im)
    
    # Outer border & subtle inner card
    d.rounded_rectangle([(4, 4), (width-5, height-5)], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    
    # Header bar
    d.rounded_rectangle([(4, 4), (width-5, 76)], radius=16, fill=color_theme[0])
    d.rectangle([(4, 40), (width-5, 76)], fill=color_theme[0]) # flat bottom for header
    
    # Header text
    f_title = get_font(25, bold=True)
    f_tag = get_font(13, bold=True)
    d.text((24, 22), title, fill=(255, 255, 255), font=f_title)
    
    # Tag badge in header
    tag_w = d.textlength(tag, font=f_tag) + 20
    tag_x = width - tag_w - 24
    d.rounded_rectangle([(tag_x, 22), (tag_x + tag_w, 54)], radius=8, fill=color_theme[1])
    d.text((tag_x + 10, 28), tag, fill=(255, 255, 255), font=f_tag)
    
    return im, d

# -------------------------------------------------------------
# 1. 營地建設與一般帳棚
# -------------------------------------------------------------
def gen_tent_general():
    im, d = create_card("🏕️ 營地建設 · 標準一般露營帳棚（蒙古包帳）", "手冊野營標準器材", ((21, 128, 61), (15, 118, 54)), 800, 520)
    
    d.rounded_rectangle([(24, 96), (480, 496)], radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    
    d.line([(40, 450), (464, 450)], fill=(148, 163, 184), width=4)
    d.chord([(80, 160), (424, 470)], start=180, end=360, fill=(34, 197, 94), outline=(21, 128, 61), width=4)
    d.polygon([(252, 230), (160, 450), (344, 450)], fill=(254, 240, 138), outline=(202, 138, 4), width=3)
    d.line([(252, 230), (252, 450)], fill=(161, 98, 7), width=2)
    d.polygon([(220, 165), (284, 165), (252, 140)], fill=(234, 88, 12))
    d.line([(120, 260), (45, 450)], fill=(239, 68, 68), width=3)
    d.line([(384, 260), (459, 450)], fill=(239, 68, 68), width=3)
    d.line([(45, 445), (35, 470)], fill=(71, 85, 105), width=4)
    d.line([(459, 445), (469, 470)], fill=(71, 85, 105), width=4)
    
    f_lbl = get_font(13, bold=True)
    f_sm = get_font(12, bold=False)
    d.text((200, 122), "頂部透氣通風窗 ⮯", fill=(194, 65, 12), font=f_lbl)
    d.text((310, 185), "⮰ 防雨外帳 (Mark朝外)", fill=(21, 128, 61), font=f_lbl)
    d.text((215, 310), "雙向紗網營門", fill=(161, 98, 7), font=f_lbl)
    d.text((385, 320), "副營繩 45° ⮲", fill=(220, 38, 38), font=f_lbl)
    d.text((360, 465), "營釘 45° 斜向釘入 ⮵", fill=(71, 85, 105), font=f_sm)

    rx = 500
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    
    d.text((rx, 106), "📦 一般露營帳標準配件：", fill=(15, 23, 42), font=f_h2)
    items = [
        "1. 防水外帳：防雨水露水，商標朝外",
        "2. 透氣內帳：紗網防蚊通風透氣",
        "3. 玻璃纖維/鋁合金營柱：支撐交叉拱架",
        "4. 鋼質營釘：14支，45度角扎實釘入",
        "5. 營繩：主副營繩調節張力緊度",
        "6. 防潮地布：阻絕地面濕氣反潮"
    ]
    y = 142
    for it in items:
        d.text((rx, y), it, fill=(51, 65, 85), font=f_p)
        y += 26
        
    d.rounded_rectangle([(rx, 315), (776, 496)], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    d.text((rx + 14, 328), "🗣️ 手冊搭帳金科玉律：", fill=(21, 128, 61), font=f_h2)
    tips = [
        "• 營門緊閉：搭帳收帳前關閉營門保持形狀",
        "• 排水順暢：避開低窪積水與樹下枯枝",
        "• 內外分離：外帳勿緊貼內帳以防冷凝滲水",
        "• 飽滿挺立：營繩拉緊45度，通風透氣保溫"
    ]
    y2 = 362
    for tp in tips:
        d.text((rx + 14, y2), tp, fill=(22, 101, 52), font=f_p)
        y2 += 28

    im.save('assets/img/tent_general_camp.jpg', quality=95)
    print("Generated: tent_general_camp.jpg")

# -------------------------------------------------------------
# 2. 自然方向辨識 (6種)
# -------------------------------------------------------------
def gen_dir_compass_map():
    im, d = create_card("🧭 自然方向辨識 ① · 指南針與地圖定向三步驟", "童軍必備定位技能", ((3, 105, 161), (2, 132, 199)))
    
    # Compass graphic
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(240, 249, 255), outline=(186, 230, 253))
    cx, cy, r = 202, 280, 140
    d.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(255, 255, 255), outline=(3, 105, 161), width=4)
    d.ellipse([(cx-r+15, cy-r+15), (cx+r-15, cy+r-15)], outline=(203, 213, 225), width=2)
    
    # 16-point directions
    f_card = get_font(15, bold=True)
    d.text((cx-8, cy-r+20), "北 N", fill=(220, 38, 38), font=f_card)
    d.text((cx-8, cy+r-35), "南 S", fill=(15, 23, 42), font=f_card)
    d.text((cx+r-38, cy-8), "東 E", fill=(15, 23, 42), font=f_card)
    d.text((cx-r+12, cy-8), "西 W", fill=(15, 23, 42), font=f_card)
    
    # Compass Needle (Red pointing North, Blue pointing South)
    d.polygon([(cx, cy-r+45), (cx-16, cy), (cx+16, cy)], fill=(239, 68, 68))
    d.polygon([(cx, cy+r-45), (cx-16, cy), (cx+16, cy)], fill=(59, 130, 246))
    d.ellipse([(cx-10, cy-10), (cx+10, cy+10)], fill=(255, 255, 255), outline=(71, 85, 105), width=3)
    d.text((cx-55, cy+r+10), "磁北針 Red to North", fill=(2, 132, 199), font=get_font(13, bold=True))

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🗺️ 地圖與指南針「定向三步驟」：", fill=(15, 23, 42), font=f_h2)
    steps = [
        "步驟一【水平持平】：將指南針平放於掌心或地圖上，避開金屬與電子干擾。",
        "步驟二【磁北對正】：轉動身體或羅盤刻度環，讓磁針紅端對準底盤「北 (N)」。",
        "步驟三【地圖正置】：將地圖南北方位線與指南針紅針平行，此時眼前即實際北方！"
    ]
    y = 146
    for s in steps:
        d.text((rx, y), s[:16], fill=(3, 105, 161), font=get_font(14, bold=True))
        d.text((rx, y+22), s[16:], fill=(51, 65, 85), font=f_p)
        y += 50
        
    d.rounded_rectangle([(rx, 320), (776, 496)], radius=10, fill=(240, 253, 250), outline=(204, 251, 241))
    d.text((rx+14, 332), "📌 16 方位角度常考基準：", fill=(13, 148, 136), font=f_h2)
    facts = [
        "• 正北(N) 0° / 360° ｜ 正東(E) 90°",
        "• 正南(S) 180° ｜ 正西(W) 270°",
        "• 東北(NE) 45° ｜ 東南(SE) 135°",
        "• 尖山埤定向越野闖關時，隨時手持指針確認前進方位角！"
    ]
    y2 = 368
    for f in facts:
        d.text((rx+14, y2), f, fill=(15, 118, 110), font=f_p)
        y2 += 28

    im.save('assets/img/dir_compass_map.jpg', quality=95)
    print("Generated: dir_compass_map.jpg")

def gen_dir_sun_moon():
    im, d = create_card("☀️ 自然方向辨識 ② · 太陽與月亮規律（立竿見影法）", "日夜天體規律判斷", ((217, 119, 6), (180, 83, 9)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(255, 251, 235), outline=(254, 243, 199))
    # Sun path arc
    d.arc([(40, 160), (364, 450)], start=180, end=360, fill=(245, 158, 11), width=4)
    # Sun graphic morning
    d.ellipse([(50, 290), (90, 330)], fill=(251, 191, 36), outline=(217, 119, 6), width=2)
    # Sun graphic noon
    d.ellipse([(182, 140), (222, 180)], fill=(245, 158, 11), outline=(180, 83, 9), width=2)
    # Sun graphic evening
    d.ellipse([(314, 290), (354, 330)], fill=(234, 88, 12), outline=(194, 65, 12), width=2)
    # Ground & Stick
    d.line([(40, 430), (364, 430)], fill=(120, 113, 108), width=3)
    d.line([(202, 350), (202, 430)], fill=(68, 64, 60), width=5) # vertical stick
    # Shadow line
    d.line([(202, 430), (140, 430)], fill=(168, 162, 158), width=5) # morning shadow to West
    d.line([(202, 430), (264, 430)], fill=(168, 162, 158), width=5) # evening shadow to East
    
    f_lbl = get_font(13, bold=True)
    d.text((45, 338), "東方日出 6:00", fill=(180, 83, 9), font=f_lbl)
    d.text((165, 115), "正午 12:00 (正南方)", fill=(180, 83, 9), font=f_lbl)
    d.text((295, 338), "西方日落 18:00", fill=(194, 65, 12), font=f_lbl)
    d.text((80, 440), "西側影(晨)", fill=(87, 83, 78), font=f_lbl)
    d.text((250, 440), "東側影(昏)", fill=(87, 83, 78), font=f_lbl)
    d.text((150, 465), "立竿見影法測東西", fill=(180, 83, 9), font=f_lbl)

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🌞 太陽規律與時針辨向法：", fill=(15, 23, 42), font=f_h2)
    rules = [
        "1. 日出東升、日落西沉：上午影子偏西，下午影子偏東。",
        "2. 正午 12:00 影子正指向北方（台灣位於北半球北回歸線一帶）。",
        "3. 手錶時針辨向法：將「時針指向太陽」，時針與 12 點刻度之間的「夾角角平分線」，指向正南方！"
    ]
    y = 142
    for r in rules:
        d.text((rx, y), r, fill=(51, 65, 85), font=f_p)
        y += 46
        
    d.rounded_rectangle([(rx, 310), (776, 496)], radius=10, fill=(254, 243, 199), outline=(253, 230, 138))
    d.text((rx+14, 324), "🌙 月亮月相觀測秘訣：", fill=(180, 83, 9), font=f_h2)
    m_tips = [
        "• 上弦月（初七、初八）：黃昏出現在正南方，半夜在西方落下。",
        "• 滿月（農曆十五）：下午 6 點東升，午夜 12 點高懸正南方！",
        "• 下弦月（廿二、廿三）：半夜自東方升起，清晨 6 點在正南方。",
        "• 只要記住「正午太陽在南方、午夜滿月在正南方」即不迷向！"
    ]
    y2 = 360
    for mt in m_tips:
        d.text((rx+14, y2), mt, fill=(146, 64, 14), font=f_p)
        y2 += 28

    im.save('assets/img/dir_sun_moon.jpg', quality=95)
    print("Generated: dir_sun_moon.jpg")

def gen_dir_stars():
    im, d = create_card("✨ 自然方向辨識 ③ · 星象觀測（北斗七星尋北極星）", "夜間迷途定位之王", ((30, 27, 75), (49, 46, 129)))
    
    # Night sky
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85))
    
    # Big Dipper stars (7 stars)
    dipper = [
        (80, 220), (130, 205), (175, 235), (205, 280),
        (260, 270), (285, 340), (225, 350)
    ]
    # Draw constellation lines
    for i in range(len(dipper)-1):
        d.line([dipper[i], dipper[i+1]], fill=(148, 163, 184), width=2)
    d.line([dipper[3], dipper[6]], fill=(148, 163, 184), width=2)
    for pt in dipper:
        d.ellipse([(pt[0]-4, pt[1]-4), (pt[0]+4, pt[1]+4)], fill=(255, 255, 255))
        
    # Pointer line from TianXuan(6) to TianShu(5) extending 5x to Polaris
    p1 = dipper[6] # (225, 350)
    p2 = dipper[5] # (285, 340)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    
    # Polaris at top right
    polaris = (285 + dx*2, 340 + dy*2 - 180) # approx (350, 140)
    polaris = (320, 160)
    d.line([(p2[0], p2[1]), polaris], fill=(234, 179, 8), width=2)
    # Polaris star glow
    px, py = polaris
    d.ellipse([(px-12, py-12), (px+12, py+12)], fill=(254, 240, 138))
    d.ellipse([(px-6, py-6), (px+6, py+6)], fill=(255, 255, 255))
    
    f_lbl = get_font(13, bold=True)
    d.text((px-70, py-18), "北極星 Polaris", fill=(253, 224, 71), font=f_lbl)
    d.text((px-55, py+15), "★ 正北方 (0°)", fill=(250, 204, 21), font=f_lbl)
    d.text((100, 175), "北斗七星 (大熊座)", fill=(203, 213, 225), font=f_lbl)
    d.text((250, 365), "延長 5 倍距離 ⮵", fill=(251, 191, 36), font=get_font(12, bold=False))

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🌌 夜間星空北極星定位口訣：", fill=(15, 23, 42), font=f_h2)
    steps = [
        "1. 尋找「北斗七星」：形狀如大湯匙，勺口兩顆星為「天璇」與「天樞」。",
        "2. 連線延長五倍：由天璇向天樞方向連成一直線，向勺口外延長 5 倍距離！",
        "3. 抵達「北極星」：正好會碰上一顆亮度約二等的恆星（小熊座尾端）。",
        "4. 面對北極星即正北：背後為正南、右手為正東、左手為正西！"
    ]
    y = 144
    for s in steps:
        d.text((rx, y), s, fill=(51, 65, 85), font=f_p)
        y += 42
        
    d.rounded_rectangle([(rx, 315), (776, 496)], radius=10, fill=(238, 242, 255), outline=(199, 210, 254))
    d.text((rx+14, 328), "👑 備案：秋季仙后座 (W星) 辨識法：", fill=(67, 56, 202), font=f_h2)
    cass = [
        "• 當春夏季北斗七星地平線過低時，改用「仙后座 (Cassiopeia)」。",
        "• 五顆亮星呈「W」形狀，將兩側開口延伸線交叉於頂點，",
        "• 再由頂點向中間主星作中垂線延伸 5 倍距離，亦直指北極星！"
    ]
    y2 = 368
    for c in cass:
        d.text((rx+14, y2), c, fill=(55, 48, 163), font=f_p)
        y2 += 30

    im.save('assets/img/dir_stars_polaris.jpg', quality=95)
    print("Generated: dir_stars_polaris.jpg")

def gen_dir_tree_rings():
    im, d = create_card("🌲 自然方向辨識 ④ · 樹木年輪與枝葉疏密", "大自然植物指南針", ((22, 101, 52), (21, 128, 61)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(240, 253, 244), outline=(187, 247, 208))
    
    # Stump cross section with off-center rings
    cx, cy = 202, 280
    # Outer bark
    d.ellipse([(cx-130, cy-120), (cx+130, cy+140)], fill=(120, 53, 15), outline=(69, 26, 3), width=4)
    # Inner wood
    d.ellipse([(cx-120, cy-110), (cx+120, cy+130)], fill=(254, 243, 199))
    
    # Eccentric tree rings: denser towards North (top), wider towards South (bottom)
    for i in range(1, 7):
        offset_y = i * 8 # shift towards south
        rx = i * 18
        ry = i * 17
        d.ellipse([(cx-rx, cy-ry + offset_y), (cx+rx, cy+ry + offset_y)], outline=(180, 83, 9), width=2)
        
    f_lbl = get_font(13, bold=True)
    d.text((cx-35, 120), "北方 North ⮵", fill=(185, 28, 28), font=f_lbl)
    d.text((cx-75, 142), "(年輪密集 · 日照短寒冷)", fill=(185, 28, 28), font=get_font(12, bold=False))
    
    d.text((cx-35, 435), "南方 South ⮯", fill=(21, 128, 61), font=f_lbl)
    d.text((cx-85, 458), "(年輪寬疏 · 向陽生長快速)", fill=(21, 128, 61), font=get_font(12, bold=False))

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🌳 手冊記載：植物生長辨向法三大鐵則：", fill=(15, 23, 42), font=f_h2)
    rules = [
        "1. 樹木年輪：南寬北密",
        "   北半球向南面終年陽光充足，形成層細胞分裂快，年輪寬疏；北面寒冷年輪緊密。",
        "2. 枝葉茂密程度：南盛北衰",
        "   樹冠南側受光面生長茂密繁盛；北側背光枝葉較為稀疏。",
        "3. 樹幹青苔分布：青苔多者為北",
        "   北面陰暗潮濕，樹幹、岩石多生長濃密青苔地衣；南面乾燥青苔較少。"
    ]
    y = 142
    for r in rules:
        if r.startswith("1.") or r.startswith("2.") or r.startswith("3."):
            d.text((rx, y), r, fill=(21, 128, 61), font=get_font(14, bold=True))
            y += 24
        else:
            d.text((rx+16, y), r, fill=(51, 65, 85), font=f_p)
            y += 34
            
    d.rounded_rectangle([(rx, 350), (776, 496)], radius=10, fill=(254, 252, 232), outline=(254, 240, 138))
    d.text((rx+14, 362), "⚠️ 野外觀察注意事項：", fill=(161, 98, 7), font=f_h2)
    d.text((rx+14, 396), "• 密林深處應綜合多棵樹木判斷，避免單一風向或遮蔽干擾。", fill=(113, 63, 18), font=f_p)
    d.text((rx+14, 426), "• 搭配地貌水流與指北針交互驗證，提升定向精確度！", fill=(113, 63, 18), font=f_p)

    im.save('assets/img/dir_tree_rings.jpg', quality=95)
    print("Generated: dir_tree_rings.jpg")

def gen_dir_sunflower():
    im, d = create_card("🌻 自然方向辨識 ⑤ · 向日葵花盤朝向規律", "手冊官方指定植物指標", ((202, 138, 4), (161, 98, 7)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(254, 252, 232), outline=(254, 240, 138))
    
    # Draw Sunflower
    cx, cy = 202, 260
    # Stem & Leaf
    d.line([(cx, cy), (cx, 440)], fill=(22, 101, 52), width=8)
    d.polygon([(cx, 350), (cx-50, 320), (cx, 380)], fill=(34, 197, 94))
    d.polygon([(cx, 380), (cx+50, 350), (cx, 410)], fill=(34, 197, 94))
    
    # Petals
    for deg in range(0, 360, 20):
        rad = math.radians(deg)
        px1 = cx + math.cos(rad) * 45
        py1 = cy + math.sin(rad) * 45
        px2 = cx + math.cos(rad) * 90
        py2 = cy + math.sin(rad) * 90
        d.line([(px1, py1), (px2, py2)], fill=(234, 179, 8), width=10)
    # Center seed disk
    d.ellipse([(cx-45, cy-45), (cx+45, cy+45)], fill=(120, 53, 15), outline=(69, 26, 3), width=3)
    
    f_lbl = get_font(13, bold=True)
    d.text((45, 120), "上午 12:00 前", fill=(180, 83, 9), font=f_lbl)
    d.text((45, 140), "⮯ 朝向東南方 (SE)", fill=(194, 65, 12), font=f_lbl)
    d.text((250, 120), "下午 12:00 後", fill=(180, 83, 9), font=f_lbl)
    d.text((250, 140), "朝向西南方 (SW) ⮯", fill=(194, 65, 12), font=f_lbl)
    d.text((120, 455), "向陽追日運動 (Helio)", fill=(161, 98, 7), font=f_lbl)

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🌻 手冊第 17 頁向日葵定向鐵則：", fill=(15, 23, 42), font=f_h2)
    rules = [
        "1. 上午 12:00 以前：花盤普遍朝向「東南方 (SE)」迎接朝陽。",
        "2. 正午 12:00 前後：花盤隨太陽運行至「正南方 (S)」上方。",
        "3. 下午 12:00 以後：花盤轉向朝向「西南方 (SW)」追隨西斜夕陽。",
        "4. 入夜後：幼嫩花盤於夜間會緩慢轉回東方，等待次日黎明！"
    ]
    y = 144
    for r in rules:
        d.text((rx, y), r, fill=(51, 65, 85), font=f_p)
        y += 42
        
    d.rounded_rectangle([(rx, 320), (776, 496)], radius=10, fill=(255, 247, 237), outline=(254, 215, 170))
    d.text((rx+14, 334), "🌿 植物向光性 (Phototropism) 科學原理：", fill=(194, 65, 12), font=f_h2)
    notes = [
        "• 生長素 (Auxin) 背光分布多，使背光側生長快而推動花盤朝向陽光。",
        "• 盛開成熟期的向日葵通常固定朝向東南～東方，以利早晨蜜蜂授粉。",
        "• 在台南柳營尖山埤附近農田與花圃，是極佳的天然方位觀察標的！"
    ]
    y2 = 370
    for n in notes:
        d.text((rx+14, y2), n, fill=(154, 52, 18), font=f_p)
        y2 += 30

    im.save('assets/img/dir_sunflower.jpg', quality=95)
    print("Generated: dir_sunflower.jpg")

def gen_dir_trad_building():
    im, d = create_card("🏛️ 自然方向辨識 ⑥ · 傳統建築坐向（坐北朝南）", "閩南聚落合院古老智慧", ((194, 65, 12), (154, 52, 18)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(255, 247, 237), outline=(254, 215, 170))
    
    # Sanheyuan courtyard diagram
    # North Main Hall (正身)
    d.rectangle([(110, 160), (294, 230)], fill=(234, 88, 12), outline=(154, 52, 18), width=3)
    # Left Wing (左護龍)
    d.rectangle([(80, 230), (140, 380)], fill=(251, 146, 60), outline=(154, 52, 18), width=2)
    # Right Wing (右護龍)
    d.rectangle([(264, 230), (324, 380)], fill=(251, 146, 60), outline=(154, 52, 18), width=2)
    # Courtyard (中庭 / 埕)
    d.rectangle([(140, 230), (264, 380)], fill=(254, 215, 170))
    # Entrance gate facing South
    d.line([(170, 420), (234, 420)], fill=(154, 52, 18), width=4)
    
    f_lbl = get_font(13, bold=True)
    d.text((150, 130), "北 N (正身背後)", fill=(185, 28, 28), font=f_lbl)
    d.text((150, 185), "正廳公媽神明堂", fill=(255, 255, 255), font=get_font(11, bold=True))
    d.text((45, 290), "東 E\n(左護龍)", fill=(154, 52, 18), font=f_lbl)
    d.text((330, 290), "西 W\n(右護龍)", fill=(154, 52, 18), font=f_lbl)
    d.text((130, 435), "南 S (大門出入口朝向) ⮯", fill=(21, 128, 61), font=f_lbl)

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🏡 台灣傳統民居「坐北朝南」環境適應：", fill=(15, 23, 42), font=f_h2)
    rules = [
        "1. 坐北朝南（面南向背北向）：",
        "   正身（主廳堂）背靠北方、大門與中庭面向正南方。",
        "2. 避開冬季強烈東北季風：",
        "   台灣冬季盛行濕冷東北季風，背北設計阻絕寒風灌入屋內。",
        "3. 夏季迎向清涼西南季風：",
        "   夏季向南開口引進西南氣流，促進穿堂風自然降溫對流。",
        "4. 墓碑與古老宗祠坐向：",
        "   傳統祖塋古墓亦大多依山面水、坐北朝南，可作為迷途重要輔助判斷！"
    ]
    y = 144
    for r in rules:
        d.text((rx, y), r, fill=(51, 65, 85), font=f_p)
        y += 42
        
    d.rounded_rectangle([(rx, 330), (776, 496)], radius=10, fill=(240, 253, 244), outline=(187, 247, 208))
    d.text((rx+14, 344), "🗣️ 手冊古諺口訣：", fill=(21, 128, 61), font=f_h2)
    d.text((rx+14, 378), "「坐北朝南，賺錢輕鬆賺；冬暖夏涼，子孫滿堂！」", fill=(22, 101, 52), font=get_font(14, bold=True))
    d.text((rx+14, 410), "在鄉間古厝行走時，只要確認正身大廳方位，即可立即判定正南北線！", fill=(51, 65, 85), font=f_p)

    im.save('assets/img/dir_trad_building.jpg', quality=95)
    print("Generated: dir_trad_building.jpg")

# -------------------------------------------------------------
# 3. 野外簡易急救 (4種)
# -------------------------------------------------------------
def gen_fa_cut_bleeding():
    im, d = create_card("🩹 野外簡易急救 ① · 意外割傷與大出血「加壓止血」", "手冊官方急救規範", ((220, 38, 38), (185, 28, 28)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(254, 242, 242), outline=(254, 202, 202))
    # Wound & Sterile Pad Diagram
    d.rectangle([(110, 200), (294, 360)], fill=(255, 255, 255), outline=(220, 38, 38), width=3)
    # Red cross
    d.rectangle([(187, 230), (217, 330)], fill=(239, 68, 68))
    d.rectangle([(152, 265), (252, 295)], fill=(239, 68, 68))
    
    f_lbl = get_font(14, bold=True)
    d.text((115, 130), "① 清潔沖洗", fill=(185, 28, 28), font=f_lbl)
    d.text((85, 155), "生水或生理食鹽水沖淨", fill=(87, 83, 78), font=get_font(12, bold=False))
    
    d.text((115, 385), "② 加壓止血 + 抬高", fill=(185, 28, 28), font=f_lbl)
    d.text((80, 415), "無菌紗布直接加壓傷口", fill=(87, 83, 78), font=get_font(12, bold=False))
    d.text((80, 435), "患肢抬高於「心臟」之上", fill=(220, 38, 38), font=get_font(12, bold=True))

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🩸 意外割傷處理四步驟（手冊第 18 頁）：", fill=(15, 23, 42), font=f_h2)
    steps = [
        "1. 清洗傷口：以生水或稀釋消毒藥水將傷口周遭洗淨。",
        "2. 加壓止血：無菌清潔紗布直接「加壓傷口」5~10 分鐘，嚴禁亂用未經消毒粉末、中藥粉或萬用油。",
        "3. 繃帶紮妥：以三角巾或彈性繃帶固定敷料包紮，避免再度污染。",
        "4. 抬高送醫：盡可能將傷處「抬高高於心臟」，減緩動脈出血，儘速送隨隊醫護站或就醫！"
    ]
    y = 144
    for s in steps:
        d.text((rx, y), s, fill=(51, 65, 85), font=f_p)
        y += 44
        
    d.rounded_rectangle([(rx, 335), (776, 496)], radius=10, fill=(255, 241, 242), outline=(254, 205, 211))
    d.text((rx+14, 348), "⚠️ 野外止血三大禁忌：", fill=(190, 18, 60), font=f_h2)
    d.text((rx+14, 382), "• 絕不可任意揭開第一層紗布：若血液滲透，直接覆蓋第二層加壓！", fill=(159, 18, 57), font=f_p)
    d.text((rx+14, 410), "• 非動脈噴血嚴禁亂綁止血帶，避免局部組織缺血壞死。", fill=(159, 18, 57), font=f_p)
    d.text((rx+14, 438), "• 割傷生鏽鐵釘或髒土，務必就醫評估施打破傷風疫苗。", fill=(159, 18, 57), font=f_p)

    im.save('assets/img/fa_cut_bleeding.jpg', quality=95)
    print("Generated: fa_cut_bleeding.jpg")

def gen_fa_muscle_cramp():
    im, d = create_card("🦵 野外簡易急救 ② · 肌肉抽筋反向伸展與緩解手法", "戶外山訓運動必備", ((194, 65, 12), (154, 52, 18)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(255, 247, 237), outline=(254, 215, 170))
    # Calf cramp stretch diagram
    # Leg extended
    d.line([(80, 320), (280, 320)], fill=(217, 119, 6), width=16) # leg
    d.line([(280, 320), (320, 240)], fill=(180, 83, 9), width=14) # foot flexed upward
    # Hand pressing foot towards body
    d.polygon([(340, 220), (320, 250), (300, 220)], fill=(220, 38, 38)) # arrow pushing toes
    d.text((250, 195), "反向背屈 ⮯", fill=(220, 38, 38), font=get_font(13, bold=True))
    d.text((120, 280), "小腿肌肉放鬆", fill=(180, 83, 9), font=get_font(12, bold=False))
    
    f_lbl = get_font(13, bold=True)
    d.text((85, 360), "手法核心：反向伸展 + 輕柔按摩", fill=(194, 65, 12), font=f_lbl)
    d.text((65, 390), "膝蓋慢慢伸直，將腳掌向上朝小腿扳", fill=(87, 83, 78), font=get_font(12, bold=False))
    d.text((85, 420), "補充電解質運動飲料與溫水", fill=(21, 128, 61), font=f_lbl)

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🧘 手冊第 18 頁四部位抽筋緩解手法：", fill=(15, 23, 42), font=f_h2)
    cramps = [
        "1. 小腿抽筋（最常見）：小心慢慢伸直膝蓋抬高腿部，將腳掌與腳趾用力向上朝小腿屈壓，同時輕柔按摩小腿肚。",
        "2. 大腿抽筋：腿部膝關節拉直，一手放腳跟抬高腿部，一手輕輕施力順時針按摩大腿肌肉群。",
        "3. 腳趾抽筋：慢慢拉直抽筋腳趾，輕輕向上扳動伸展，並按壓足底湧泉穴位。",
        "4. 手指抽筋：慢慢拉直手指，反向握持向後伸展，輕揉手掌與前臂肌肉。"
    ]
    y = 144
    for c in cramps:
        d.text((rx, y), c, fill=(51, 65, 85), font=f_p)
        y += 44
        
    d.rounded_rectangle([(rx, 335), (776, 496)], radius=10, fill=(254, 243, 199), outline=(253, 230, 138))
    d.text((rx+14, 348), "💡 預防抽筋三大守則：", fill=(180, 83, 9), font=f_h2)
    d.text((rx+14, 382), "• 充分熱身：進行山訓繩索攀爬與水彈遊戲前，落實關節操！", fill=(146, 64, 14), font=f_p)
    d.text((rx+14, 410), "• 定時補水：每小時補充水分與微量鹽分，防止脫水鈉流失。", fill=(146, 64, 14), font=f_p)
    d.text((rx+14, 438), "• 抽筋時嚴禁強行激烈對抗拉扯，避免肌肉纖維撕裂傷。", fill=(146, 64, 14), font=f_p)

    im.save('assets/img/fa_muscle_cramp.jpg', quality=95)
    print("Generated: fa_muscle_cramp.jpg")

def gen_fa_nosebleed():
    im, d = create_card("🩸 野外簡易急救 ③ · 流鼻血「頭前傾＋壓鼻翼」正確處置", "破除仰頭拍脖子迷思", ((185, 28, 28), (153, 27, 27)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(254, 242, 242), outline=(254, 202, 202))
    
    # Head leaning forward diagram
    cx, cy = 202, 250
    # Head circle
    d.ellipse([(cx-60, cy-70), (cx+60, cy+50)], fill=(254, 226, 226), outline=(220, 38, 38), width=3)
    # Nose
    d.polygon([(cx+30, cy-15), (cx+70, cy), (cx+30, cy+15)], fill=(254, 202, 202), outline=(220, 38, 38))
    # Fingers pinching nose
    d.ellipse([(cx+50, cy-18), (cx+75, cy+18)], fill=(239, 68, 68))
    
    f_lbl = get_font(13, bold=True)
    d.text((cx-65, cy-105), "✅ 頭部微微向前傾", fill=(21, 128, 61), font=f_lbl)
    d.text((cx+40, cy-45), "⮯ 捏住兩側鼻翼軟骨", fill=(185, 28, 28), font=f_lbl)
    
    d.text((95, 345), "❌ 嚴禁頭向後仰！(嗆血窒息)", fill=(220, 38, 38), font=f_lbl)
    d.text((95, 375), "❌ 嚴禁拍打後頸！(毫無止血效用)", fill=(220, 38, 38), font=f_lbl)
    d.text((95, 410), "✅ 改用嘴巴呼吸，持續加壓 5~10分", fill=(21, 128, 61), font=f_lbl)
    d.text((95, 440), "✅ 冰敷鼻樑與前額促使血管收縮", fill=(3, 105, 161), font=f_lbl)

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "👃 流鼻血標準急救流程（手冊第 18 頁）：", fill=(15, 23, 42), font=f_h2)
    steps = [
        "1. 安靜坐椅，頭向前傾：傷患保持安靜坐姿，頭部微向前傾，切勿平躺或向後仰，以防血液倒流氣管引發嗆咳窒息或吞入胃部引起嘔吐。",
        "2. 捏緊兩側鼻翼：大拇指與食指用力捏住兩側鼻翼軟骨部，直接壓迫 Kiesselbach 出血點 5~10 分鐘。",
        "3. 改以口呼吸：暫時用嘴巴呼吸，口中血液請輕輕吐出，切勿嚥下。",
        "4. 冰敷前額鼻樑：以冷毛巾或冰塊冰敷鼻樑前額促使微血管收縮止血。"
    ]
    y = 144
    for s in steps:
        d.text((rx, y), s, fill=(51, 65, 85), font=f_p)
        y += 44
        
    d.rounded_rectangle([(rx, 340), (776, 496)], radius=10, fill=(255, 241, 242), outline=(254, 205, 211))
    d.text((rx+14, 354), "🏥 送醫指標提醒：", fill=(190, 18, 60), font=f_h2)
    d.text((rx+14, 388), "• 加壓超過 15 分鐘仍血流不止，應立即向隨隊醫護報告並送醫。", fill=(159, 18, 57), font=f_p)
    d.text((rx+14, 416), "• 若因頭部碰撞劇烈外傷流鼻血，可能伴隨顱底骨折，勿堵塞鼻孔！", fill=(159, 18, 57), font=f_p)

    im.save('assets/img/fa_nosebleed.jpg', quality=95)
    print("Generated: fa_nosebleed.jpg")

def gen_fa_fracture():
    im, d = create_card("🦴 野外簡易急救 ④ · 骨折固定「超過上下兩關節」夾板法", "避免二次神經血管損傷", ((13, 148, 136), (15, 118, 110)))
    
    d.rounded_rectangle([(24, 96), (380, 496)], radius=12, fill=(240, 253, 250), outline=(204, 251, 241))
    
    # Arm & Splint diagram
    cx, cy = 202, 280
    # Arm
    d.line([(80, cy), (324, cy)], fill=(251, 146, 60), width=24)
    # Splint (Board below)
    d.rectangle([(60, cy+20), (344, cy+36)], fill=(120, 53, 15), outline=(69, 26, 3), width=2)
    # Bandages securing splint
    for bx in [100, 170, 240, 310]:
        d.rectangle([(bx-8, cy-18), (bx+8, cy+42)], fill=(255, 255, 255), outline=(220, 38, 38), width=2)
    
    f_lbl = get_font(13, bold=True)
    d.text((105, 160), "骨折夾板固定標準要領：", fill=(13, 148, 136), font=f_lbl)
    d.text((70, 195), "夾板長度必須「超過上下兩關節」", fill=(185, 28, 28), font=get_font(14, bold=True))
    d.text((70, 375), "就地取材：木板、竹竿、折疊硬紙板", fill=(87, 83, 78), font=get_font(12, bold=False))
    d.text((70, 405), "三角巾妥善綑綁固定，留指端檢視循環", fill=(87, 83, 78), font=get_font(12, bold=False))
    d.text((70, 435), "無材料時：上肢固定於胸壁、下肢與健側綑綁", fill=(15, 118, 110), font=get_font(12, bold=True))

    rx = 404
    f_h2 = get_font(17, bold=True)
    f_p = get_font(13, bold=False)
    d.text((rx, 106), "🦴 骨折處理四大黃金原則（手冊第 18 頁）：", fill=(15, 23, 42), font=f_h2)
    steps = [
        "1. 評估生命徵象：先檢查意識、呼吸與脈搏，休克者先行保暖與心肺復甦處置。",
        "2. 就地取材長度超兩關節：使用夾板（木板、登山杖、雨傘），長度務必「超過骨折處上下兩關節」並加襯墊減輕疼痛。",
        "3. 自體固定備案：無夾板材料時，上肢以三角巾懸吊固定於胸壁，下肢受傷側與健側健康肢體綁在一起固定！",
        "4. 嚴禁推擠推拿復位：嚴禁任意推拉或嘗試將突出斷骨推回，立即以硬板床平臥送醫！"
    ]
    y = 144
    for s in steps:
        d.text((rx, y), s, fill=(51, 65, 85), font=f_p)
        y += 44
        
    d.rounded_rectangle([(rx, 340), (776, 496)], radius=10, fill=(240, 253, 244), outline=(187, 247, 208))
    d.text((rx+14, 354), "🚑 脊椎骨折特別戒律：", fill=(21, 128, 61), font=f_h2)
    d.text((rx+14, 388), "• 懷疑頸椎或脊椎受傷時，嚴禁抱起、背負或彎曲傷患身體！", fill=(22, 101, 52), font=f_p)
    d.text((rx+14, 416), "• 必須維持頭頸身成一直線，由受訓人員使用長背板進行搬運。", fill=(22, 101, 52), font=f_p)

    im.save('assets/img/fa_fracture.jpg', quality=95)
    print("Generated: fa_fracture.jpg")

# -------------------------------------------------------------
# 4. 臺灣四種毒蛇專屬圖卡
# -------------------------------------------------------------
def gen_snake_cards():
    snakes = [
        ("百步蛇 (Deinagkistrodon acutus)", "出血性毒 · 蝮蛇科", "snake_hundred_pacer.jpg",
         (185, 28, 28), (153, 27, 27),
         [
             "• 外觀特徵：頭大呈明顯三角形，吻端極度向上突出翹起，體側具大型黑褐色尖頂三角形斑紋。",
             "• 毒性危險：排毒量為台灣毒蛇之冠！台灣毒蛇咬人率第 5，但「致死率第 1」！",
             "• 傷口症狀：強烈出血性毒素破壞血管內皮，引發局部大量滲血、嚴重腫脹發黑壞疽。",
             "• 棲地習性：喜棲於落葉堆、原始林底層，保護色極佳，夜間出沒，遇人多靜止不動。",
             "• 急救血清：抗百步蛇毒血清（專用血清，須火速就醫施打）。"
         ]),
        ("雨傘節 (Bungarus multicinctus)", "神經性毒 · 蝙蝠蛇科", "snake_many_banded_krait.jpg",
         (30, 41, 59), (15, 23, 42),
         [
             "• 外觀特徵：全身體背具有鮮明「黑白相間等寬環紋」，背脊中央呈顯著菱形隆起線條。",
             "• 毒性危險：台灣陸生蛇毒性最強！咬人率第 3，致死率高居第 2！",
             "• 傷口症狀：咬傷處僅有微小齒痕，初期「不痛、不腫、不出血」，但數小時內呼吸肌痲痺衰竭！",
             "• 棲地習性：夜行性，性情溫和膽小，常出現在農田、水溝、近水低窪草叢，受驚擾時會將頭部藏於身下。",
             "• 急救血清：抗雨傘節及眼鏡蛇神經性抗蛇毒血清。"
         ]),
        ("赤尾青竹絲 (Trimeresurus stejnegeri)", "出血性毒 · 蝮蛇科", "snake_bamboo_viper.jpg",
         (21, 128, 61), (15, 118, 54),
         [
             "• 外觀特徵：體色翠綠如竹葉，尾端呈現特徵性「焦磚紅色」，體側常有一條細白縱線。",
             "• 毒性危險：全台灣「咬人率第 1 名」（常攀附於茶園、果樹與低矮灌木草叢被誤觸）。",
             "• 傷口症狀：出血性毒，咬傷後局部迅速劇烈紅腫、劇痛、皮下瘀血與水泡。",
             "• 辨識口訣：頭大呈烙鐵三角形，瞳孔垂直垂直如貓眼；青蛇則是圓頭圓眼無毒無尾紅。",
             "• 急救血清：抗龜殼花及赤尾鮐出血性抗蛇毒血清。"
         ]),
        ("龜殼花 (Protobothrops mucrosquamatus)", "出血性毒 · 蝮蛇科", "snake_habu.jpg",
         (180, 83, 9), (146, 64, 14),
         [
             "• 外觀特徵：頭部呈烙鐵三角形，頸部細小，體背有暗褐色不規則龜裂波浪狀斑塊。",
             "• 毒性危險：攻擊性強，夜間常在廢棄農舍、石縫、竹林枯枝堆中捕食鼠類。",
             "• 傷口症狀：出血性毒素強烈，傷口腫脹劇痛擴散極快，皮下出血起大血泡、組織壞死。",
             "• 野外防範：夜間行走必攜手電筒「打草驚蛇」，嚴禁徒手翻動枯木石塊。",
             "• 急救血清：抗龜殼花及赤尾鮐出血性抗蛇毒血清。"
         ])
    ]

    for title, tag, fname, c1, c2, facts in snakes:
        im, d = create_card(f"🐍 臺灣毒蛇辨識 · {title}", tag, (c1, c2), 800, 500)
        
        # Left visual container
        d.rounded_rectangle([(24, 96), (280, 476)], radius=12, fill=(248, 250, 252), outline=(226, 232, 240))
        d.text((45, 120), "生態特徵摘要：", fill=c1, font=get_font(16, bold=True))
        
        # Characteristic badges
        f_badge = get_font(13, bold=True)
        if "百步蛇" in title:
            badges = ["👑 致死率第 1 名", "👃 吻端翹起特徵", "🔺 體側大三角斑", "🩸 出血毒破壞血管"]
        elif "雨傘節" in title:
            badges = ["⚠️ 毒性全台最強", "⚪⚫ 黑白環紋相間", "🫁 呼吸神經衰竭", "😶 咬傷不痛不腫"]
        elif "青竹絲" in title:
            badges = ["💥 咬人率第 1 名", "🍃 全身翠綠偽裝", "🧱 尾端焦磚紅色", "📐 三角形烙鐵頭"]
        else:
            badges = ["🐁 常出沒廢農舍", "🐢 龜裂波浪暗斑", "⚡ 攻擊出擊迅捷", "🩸 局部劇痛起血泡"]
            
        by = 160
        for b in badges:
            d.rounded_rectangle([(40, by), (264, by+40)], radius=8, fill=(255, 255, 255), outline=c1, width=2)
            d.text((50, by+10), b, fill=c1, font=f_badge)
            by += 54
            
        d.text((40, 410), "打草驚蛇 · 穿著長褲鞋襪", fill=(100, 116, 139), font=get_font(12, bold=False))
        d.text((40, 435), "攜帶手電筒 · 嚴禁徒手翻石", fill=(100, 116, 139), font=get_font(12, bold=False))

        # Right facts list
        rx = 304
        f_h2 = get_font(17, bold=True)
        f_p = get_font(13, bold=False)
        d.text((rx, 106), "📖 生態習性與毒理特徵詳解：", fill=(15, 23, 42), font=f_h2)
        
        y = 144
        for f in facts:
            d.text((rx, y), f[:7], fill=c1, font=get_font(14, bold=True))
            d.text((rx, y+22), f[7:], fill=(51, 65, 85), font=f_p)
            y += 50
            
        d.rounded_rectangle([(rx, 400), (776, 476)], radius=10, fill=(254, 242, 242), outline=(254, 202, 202))
        d.text((rx+14, 412), "🚑 蛇傷急救處置要領：", fill=(185, 28, 28), font=get_font(14, bold=True))
        d.text((rx+14, 438), "拍照記住特徵 ｜ 拔下戒指手錶 ｜ 彈性包紮患肢低於心臟 ｜ 火速就醫！", fill=(153, 27, 27), font=f_p)

        im.save(f'assets/img/{fname}', quality=95)
        print(f"Generated: {fname}")

gen_dir_compass_map()
gen_dir_sun_moon()
gen_dir_stars()
gen_dir_tree_rings()
gen_dir_sunflower()
gen_dir_trad_building()

gen_fa_cut_bleeding()
gen_fa_muscle_cramp()
gen_fa_nosebleed()
gen_fa_fracture()

gen_snake_cards()
print("All educational graphics generated successfully!")

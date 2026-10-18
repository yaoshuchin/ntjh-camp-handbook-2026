import openpyxl, docx, json, re, os, sys

def mask_name(name):
    if not name or not isinstance(name, str):
        return ''
    name = name.strip()
    if name in ['—', '-', '無']:
        return '—'
    suffix = ''
    if '(素)' in name:
        name = name.replace('(素)', '').strip()
        suffix = '(素)'
    elif '（素）' in name:
        name = name.replace('（素）', '').strip()
        suffix = '(素)'
    if len(name) <= 1:
        return name + suffix
    elif len(name) == 2:
        return name[0] + 'O' + suffix
    else:
        return name[0] + 'O' + name[2:] + suffix

def mask_person_entry(text):
    if not text or text in ['—', '-', '無']:
        return '—'
    text = text.strip()
    m = re.match(r'^(\d+號)?\s*(.+)$', text)
    if m:
        num = m.group(1) or ''
        nm = m.group(2) or ''
        return f'{num} {mask_name(nm)}'.strip()
    return mask_name(text)

def mask_member_list(text):
    if not text or text in ['—', '-', '無']:
        return '—'
    items = re.split(r'[、,，]\s*', text.strip())
    masked = [mask_person_entry(it) for it in items if it.strip()]
    return '、'.join(masked)

# 1. Load Excel
excel_path = '南投國中115二年級隔宿手寫資料電子檔(完整試算表) (1).xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

mentors_raw = {
    '201': '黃麗月',
    '202': '黃惠君',
    '203': '林宜玟',
    '204': '李佩儒',
    '205': '林富銓',
    '206': '許招玉',
    '207': '黃瓊慧',
}
mentors_masked = {k: mask_name(v) for k, v in mentors_raw.items()}

# Parse Students
ws_students = wb['全校學生清冊']
students = []
for r in range(5, ws_students.max_row + 1):
    c_class = ws_students.cell(r, 1).value
    if not c_class:
        continue
    c_teacher = ws_students.cell(r, 2).value or ''
    c_seat = ws_students.cell(r, 3).value or 0
    c_name = ws_students.cell(r, 4).value or ''
    c_gender = ws_students.cell(r, 5).value or ''
    c_tent = ws_students.cell(r, 6).value or ''
    c_leader = ws_students.cell(r, 7).value or ''
    c_squad = ws_students.cell(r, 8).value or ''
    c_role = ws_students.cell(r, 9).value or ''
    c_diet = ws_students.cell(r, 10).value or '葷食'

    students.append({
        'id': len(students) + 1,
        'class': str(c_class).strip(),
        'classNum': str(c_class).strip()[:3],
        'teacher': mask_name(str(c_teacher).strip()),
        'seat': int(c_seat),
        'name': mask_name(str(c_name).strip()),
        'gender': str(c_gender).strip(),
        'tent': str(c_tent).strip(),
        'isLeader': '室長' in str(c_leader),
        'leaderLabel': '室長 (負責人)' if '室長' in str(c_leader) else '成員',
        'squad': str(c_squad).strip(),
        'role': str(c_role).strip(),
        'diet': str(c_diet).strip(),
        'isVeg': '素' in str(c_diet)
    })

# Parse Tents
ws_tents = wb['帳篷住宿分配總表']
tents = []
for r in range(5, ws_tents.max_row + 1):
    c_class = ws_tents.cell(r, 1).value
    if not c_class or '全體' in str(c_class) or '合計' in str(c_class):
        continue
    gender = str(ws_tents.cell(r, 2).value or '').strip()
    tent_id = str(ws_tents.cell(r, 3).value or '').strip()
    l_seat = ws_tents.cell(r, 4).value or 0
    l_name = str(ws_tents.cell(r, 5).value or '').strip()
    count_str = str(ws_tents.cell(r, 6).value or '').strip()
    members_raw = str(ws_tents.cell(r, 7).value or '').strip()
    notes = str(ws_tents.cell(r, 8).value or '').strip()
    if notes and notes not in ['—', '-']:
        # Mask any student name in notes
        for s in students:
            raw_nm = ws_students.cell(s['id'] + 4, 4).value
            if raw_nm and isinstance(raw_nm, str) and raw_nm in notes:
                notes = notes.replace(raw_nm, s['name'])
    else:
        notes = ''

    tents.append({
        'id': len(tents) + 1,
        'class': str(c_class).strip(),
        'classNum': str(c_class).strip()[:3],
        'gender': gender,
        'tentName': tent_id,
        'fullTentName': f"{str(c_class).strip()[:3]} {tent_id}",
        'leaderSeat': int(l_seat) if isinstance(l_seat, (int, float)) and l_seat > 0 else 0,
        'leaderName': mask_name(l_name),
        'count': count_str,
        'members': mask_member_list(members_raw),
        'notes': notes
    })

# Parse Squads
ws_squads = wb['野炊烤肉小隊編組表']
squads = []
for r in range(5, ws_squads.max_row + 1):
    c_class = ws_squads.cell(r, 1).value
    if not c_class or '全校' in str(c_class) or '合計' in str(c_class):
        continue
    sq_num = str(ws_squads.cell(r, 2).value or '').strip()
    sq_cnt = str(ws_squads.cell(r, 3).value or '').strip()
    leader = str(ws_squads.cell(r, 4).value or '').strip()
    deputy = str(ws_squads.cell(r, 5).value or '').strip()
    chef1 = str(ws_squads.cell(r, 6).value or '').strip()
    chef2 = str(ws_squads.cell(r, 7).value or '').strip()
    fire = str(ws_squads.cell(r, 8).value or '').strip()
    water = str(ws_squads.cell(r, 9).value or '').strip()
    affairs = str(ws_squads.cell(r, 10).value or '').strip()
    members = str(ws_squads.cell(r, 11).value or '').strip()

    squads.append({
        'id': len(squads) + 1,
        'class': str(c_class).strip(),
        'classNum': str(c_class).strip()[:3],
        'squadName': sq_num,
        'fullSquadName': f"{str(c_class).strip()[:3]} {sq_num}",
        'count': sq_cnt,
        'leader': mask_person_entry(leader),
        'deputy': mask_person_entry(deputy),
        'chef1': mask_person_entry(chef1),
        'chef2': mask_person_entry(chef2),
        'fire': mask_person_entry(fire),
        'water': mask_person_entry(water),
        'affairs': mask_person_entry(affairs),
        'members': mask_member_list(members),
    })

# Parse Word Doc Itinerary
doc = docx.Document('南投國中115學年度二年級(尖山埤)1(名間親子).docx')
day1_schedule = []
for row in doc.tables[0].rows[1:]:
    cells = [c.text.strip() for c in row.cells]
    day1_schedule.append({
        'time': cells[0],
        'activity': cells[1],
        'note': cells[2]
    })

day2_schedule = []
for row in doc.tables[1].rows[1:]:
    cells = [c.text.strip() for c in row.cells]
    day2_schedule.append({
        'time': cells[0],
        'activity': cells[1],
        'note': cells[2]
    })

# Classes stats
class_summaries = [
    {'class': '201 班', 'teacher': mentors_masked['201'], 'boys': 10, 'girls': 7, 'total': 17, 'veg': 0, 'squads': 2, 'boyTents': 2, 'girlTents': 2, 'totalTents': 4},
    {'class': '202 班', 'teacher': mentors_masked['202'], 'boys': 6, 'girls': 12, 'total': 18, 'veg': 0, 'squads': 3, 'boyTents': 2, 'girlTents': 3, 'totalTents': 5},
    {'class': '203 班', 'teacher': mentors_masked['203'], 'boys': 6, 'girls': 9, 'total': 15, 'veg': 0, 'squads': 2, 'boyTents': 2, 'girlTents': 2, 'totalTents': 4},
    {'class': '204 班', 'teacher': mentors_masked['204'], 'boys': 7, 'girls': 8, 'total': 15, 'veg': 0, 'squads': 2, 'boyTents': 2, 'girlTents': 2, 'totalTents': 4},
    {'class': '205 班', 'teacher': mentors_masked['205'], 'boys': 7, 'girls': 4, 'total': 11, 'veg': 1, 'squads': 2, 'boyTents': 2, 'girlTents': 1, 'totalTents': 3},
    {'class': '206 班', 'teacher': mentors_masked['206'], 'boys': 4, 'girls': 5, 'total': 9, 'veg': 0, 'squads': 1, 'boyTents': 1, 'girlTents': 1, 'totalTents': 2},
    {'class': '207 班', 'teacher': mentors_masked['207'], 'boys': 8, 'girls': 13, 'total': 21, 'veg': 0, 'squads': 3, 'boyTents': 2, 'girlTents': 3, 'totalTents': 5},
]

full_camp_dict = {
  "info": {
    "school": "南投縣立南投國民中學",
    "title": "115學年度 二年級戶外教育隔宿露營行動手冊",
    "subtitle": "尖山埤山訓探索・野營炊事・名間生態共融之旅（去個資版）",
    "dates": "115學年度",
    "duration": "兩天一夜",
    "assembly": {
      "time": "07:30 - 08:00",
      "location": "學校集合（921地震公園逃生演練）",
      "departure": "08:00 準時發車出發",
      "note": "清點全班人數、行車安全逃生演練與繫妥安全帶"
    },
    "locations": [
      {
        "name": "台南柳營尖山埤渡假村",
        "tag": "露營營地 · 山訓 · 營火晚會 · 野炊烤肉",
        "phone": "06-6233888",
        "telLink": "tel:066233888",
        "address": "台南市柳營區旭山里60號",
        "mapUrl": "https://maps.google.com/?q=柳營尖山埤渡假村",
        "desc": "台糖旗艦渡假勝地，坐擁尖山埤水庫湖光山色，配備完善露營區、野炊烤肉場、高空山訓攀岩場與營火晚會大草坪。"
      },
      {
        "name": "南投名間親子生態園區",
        "tag": "共融生態樂園 · 5米彩虹滑梯",
        "phone": "049-2222106",
        "telLink": "tel:0492222106",
        "address": "南投縣名間鄉彰南路256號",
        "mapUrl": "https://maps.google.com/?q=名間親子生態園區",
        "desc": "南投縣最大 2.6 公頃全齡共融式生態公園，擁有超吸睛 5 米高彩虹磨石子溜滑梯、攀爬草坡、大型複合遊具與景觀空中步道。"
      }
    ],
    "stats": {
      "studentsTotal": len(students),
      "maleStudents": len([s for s in students if s['gender'] == '男']),
      "femaleStudents": len([s for s in students if s['gender'] == '女']),
      "vegetarianStudents": len([s for s in students if s['isVeg']]),
      "classesCount": 7,
      "tentsTotal": len(tents),
      "maleTents": len([t for t in tents if '男' in t['gender']]),
      "femaleTents": len([t for t in tents if '女' in t['gender']]),
      "squadsTotal": len(squads)
    },
    "staff": [
      { "title": "校長", "name": "劉O彥" },
      { "title": "學務主任", "name": "董O遠" },
      { "title": "訓育組長", "name": "姚O勤" },
      { "title": "生教組長", "name": "生O組" },
      { "title": "隨隊護理師", "name": "校O醫" }
    ],
    "mentors": mentors_masked
  },
  "classes": class_summaries,
  "itinerary": [
    {
      "day": 1,
      "title": "出發集結・野營搭帳・童軍技能與超ㄅ一ㄤˋ營火晚會",
      "meals": { "breakfast": "自理", "lunch": "中式便當", "dinner": "野炊競賽 (晚餐)", "night": "宵夜" },
      "timeline": [
        { "time": "07:30-08:00", "title": "學校集合", "desc": "各班於指定位置集合清點人數，實施 921 地震公園逃生演練與行前精神訓勉。", "icon": "school" },
        { "time": "08:00-10:00", "title": "乘車出發、安全檢查", "desc": "專車南下國道奔馳，車上安全逃生解說、滅火器與車窗擊破器操作說明，抵達營地時實施人員與裝備安全檢查。", "icon": "bus" },
        { "time": "10:00-11:00", "title": "喜相逢～環境認識", "desc": "抵達台南柳營尖山埤渡假村，各班活動小隊編組集合，熟悉營區地理環境、飲水站與醫護站位置。", "icon": "map-pin" },
        { "time": "11:00-11:30", "title": "始業式～營規介紹、工作人員介紹", "desc": "隆重開訓！大會營規介紹、生活輔導員與值星官介紹，宣佈生活競賽與精神總錦標評比規範。", "icon": "flag" },
        { "time": "11:30-12:30", "title": "我們這一班", "desc": "班級向心力大考驗！班旗揮舞、創意班歌與震撼班呼競賽，展現班級無敵氣勢與榮譽感。", "icon": "trophy" },
        { "time": "12:30-13:30", "title": "午餐時間", "desc": "各班依指定席位整齊就座，享用營養豐盛的中式便當，餐後確實做好垃圾分類與桌面清潔。", "icon": "utensils" },
        { "time": "13:30-14:30", "title": "野營常識介紹：帳棚搭設與器材領取", "desc": "專業教官講解標準營地配置、六人蒙古包帳篷結構（內帳、外帳、營柱、營釘、地布）、搭帳技巧演練與器材領取。", "icon": "campground" },
        { "time": "14:30-17:00", "title": "分站教育 Part 1：童軍技能教育", "desc": "分站輪動實作：（1）生火技巧與野炊烹調 （2）戰術偽裝與方向辨識 （3）出神入化童軍繩結 （4）臺灣六大毒蛇辨識與急救 （5）晚會預習彩排與音樂律動。", "icon": "compass" },
        { "time": "17:00-19:00", "title": "晚餐 (炊事競賽)", "desc": "野炊大考驗！各小隊隊長、大廚、二廚、伙夫、水夫、事務分工合作，洗菜切配、生火掌勺、野炊烹調、擺盤評比。", "icon": "fire" },
        { "time": "19:10-21:30", "title": "超ㄅ一ㄤˋ的營火晚會喔！燭光夜語", "desc": "熱力引燃營火！隊輔勁歌熱舞、各班精采創意節目競賽、全場師生狂歡團康動唱；最後圍繞餘燼進行【薪火相傳～燭光夜語】，與導師深刻分享成長記憶。", "icon": "flame" },
        { "time": "21:30-22:30", "title": "盥洗、宵夜", "desc": "輪流盥洗、享用熱騰騰宵夜甜品，補充水分與體力，準備夜間就寢。", "icon": "coffee" },
        { "time": "22:30---", "title": "就寢＆查舖", "desc": "回到分配帳篷，各帳室長確實清點同帳成員，導師與值星幹部晚間查舖，熄燈保持營區肅靜。", "icon": "moon" }
      ]
    },
    {
      "day": 2,
      "title": "活力晨操・山訓極限探索・BBQ烤肉・名間生態園區・賦歸",
      "meals": { "breakfast": "中式早餐 (合菜)", "lunch": "BBQ 烤肉大餐", "dinner": "平安返家自理", "night": "-" },
      "timeline": [
        { "time": "06:00-06:30", "title": "起床～做個跟太陽賽跑的人", "desc": "晨喚起床！清晨鳥鳴中舒展筋骨，整理個人內務裝備與睡袋。", "icon": "sun" },
        { "time": "06:30-07:20", "title": "活力有氧晨操、拆帳收整", "desc": "營區大草坪跳活力早操！全體分工快速拆卸帳篷、清潔地布、摺疊收整營柱營釘，實施內務晨檢評分。", "icon": "smile" },
        { "time": "07:20-08:00", "title": "享用活力早餐", "desc": "在餐廳享用熱騰騰的中式合菜早餐，各桌打飯分菜，補足充沛活力。", "icon": "utensils" },
        { "time": "08:00-11:30", "title": "分站教育 Part 2：山訓、探索教育", "desc": "挑戰極限，超越自我！（1）膽量大考驗、進擊の高空垂降 （2）PA探索解手結、團隊跳繩 （3）超級蜘蛛人～攀岩絕技 （4）生存遊戲～水彈射擊競賽 （5）獨木橋平衡橫渡。", "icon": "mountain" },
        { "time": "11:00-13:00", "title": "午餐～BBQ 烤肉餐", "desc": "圍爐生火歡樂烤肉！香氣四溢的烤肉食材、團隊合作串烤，慶祝各項挑戰圓滿成功。", "icon": "drumstick-bite" },
        { "time": "13:00-14:00", "title": "結訓典禮～～ I’m the Best！！", "desc": "榮耀時刻！頒發炊事比賽、營火節目、晨檢內務、分站山訓、生活教育與【精神總錦標】競賽榮譽大獎，師生感言與結訓互道感謝。", "icon": "award" },
        { "time": "14:00-17:00", "title": "名間親子生態公園巡禮", "desc": "造訪南投名間 2.6 公頃全齡共融生態公園！體驗 5 米高彩虹磨石子溜滑梯、攀爬草坡、環狀空中無障礙步道與心型大草坪合影，順道參觀豬事文化園區。", "icon": "camera" },
        { "time": "17:00-17:10", "title": "平安抵校 ～～ Bye-Bye！", "desc": "專車平安抵達南投國中，清點隨身行囊，互道珍重再見，帶著滿滿成長回憶與榮譽回到溫暖的家！", "icon": "home" }
      ]
    }
  ],
  "students": students,
  "tents": tents,
  "squads": squads,
  "teachingGuides": {
    "campingBasics": {
      "title": "野營常識與帳篷搭設教學指引",
      "subtitle": "六人蒙古包標準搭設六部曲與無痕山林守則",
      "steps": [
        { "step": "1. 選地整平", "desc": "挑選平坦地勢，清除地面碎石、硬樹枝、松果雜物。避開低窪積水坑洞、傾斜斜坡與枯枝下方，保持與廚房、廁所適當距離。" },
        { "step": "2. 鋪設地布", "desc": "在帳位上攤平防水地布。注意：地布面積不可超出帳篷外帳底緣，四周多餘地布需向內往底下摺入，防止雨水沿著地布流入內帳底層！" },
        { "step": "3. 穿插營柱", "desc": "將兩組長營柱組裝打直，沿對角線交叉穿入內帳通管（或先扣掛鉤），營柱插入四角金屬插銷。記得穿管時以『推』代『拉』，以免營柱接頭脫節卡住！" },
        { "step": "4. 立起內帳", "desc": "兩人站在對角同時將營柱向上彎曲拱起，將另一端插銷插入固定，扣上內帳塑料掛勾，內帳即刻自然挺立。" },
        { "step": "5. 披上外帳", "desc": "確認外帳前後進出口方向，覆蓋在內帳上方。將外帳內側魔鬼氈確實繫綁於營柱交叉點，四角插扣扣緊調勻張力。" },
        { "step": "6. 打釘拉水線", "desc": "將營釘以與地面呈 45°～60° 夾角（釘尖朝向帳篷，背向營繩）敲入土壤，拉開外帳前庭與四角防風水線，使內外帳完全分離，保持空氣對流並防止反潮！" }
      ],
      "teardown": [
        "清空內帳所有物品，將門窗拉鍊留一小段透氣縫，利於氣體排出。",
        "依序拔除營釘、鬆開營繩，解開外帳四角插扣與魔鬼氈，將外帳平鋪甩乾水珠折疊。",
        "兩人配合取出四角插銷，將營柱輕輕推退抽出，營柱收折時應由『中央』對折向兩端，受力均勻保護內部彈力繩。",
        "將內帳整齊對折，連同外帳緊密捲起成圓筒狀，裝入收納袋，點齊營釘與營柱配件。"
      ],
      "lntRules": [
        { "title": "事前充分規劃與準備", "desc": "熟知營地規章、天氣狀況與必要裝備，確保團體行動安全。" },
        { "title": "在堅實地面露營與活動", "desc": "集中在指定營位紮營，避免踩踏破壞周圍植被與幼苗草皮。" },
        { "title": "妥善處理垃圾與廢棄物", "desc": "落實『垃圾不落地』，廚餘湯汁倒入指定廚餘桶，不可傾倒於洗手台或草叢。" },
        { "title": "保持環境原有風貌", "desc": "不攀折花木、不採摘果實，欣賞大自然而不帶走任何自然物。" },
        { "title": "減低用火的負面影響", "desc": "野炊生火僅限於指定爐灶區，嚴禁在草皮直接生火，熄火後確實清理木炭灰燼。" },
        { "title": "尊重野生動植物", "desc": "遠距離觀察野生動物，不追逐、不餵食，夜晚收妥食材防止流浪動物翻咬。" },
        { "title": "考量其他營地使用者", "desc": "遵守營地安寧時間（22:30後全面輕聲細語），尊重彼此的露營休閒品質。" }
      ]
    },
    "scoutSkills": {
      "title": "童軍技能教育實作教學指引",
      "subtitle": "野外生火、定向偽裝、童軍繩結、臺灣毒蛇辨識與營火晚會",
      "sections": [
        {
          "id": "fire_cooking",
          "title": "（1）生火技巧與野炊控火",
          "icon": "fire",
          "content": [
            "【火媒棒製作】：選擇乾燥易燃木條，持童軍刀以 45 度角向前輕推，削出層層翻卷而不脫落的羽狀木屑，極易被火星引燃。",
            "【柴火三級分類】：① 引火柴（乾枯針葉、芒草、火種）② 助燃柴（牙籤至小指粗的乾燥小枯枝）③ 燃燒柴（腕粗大乾木塊、耐燒木炭）。",
            "【柴堆架構】：① 井字型柴堆（通風性最佳、受熱均勻，適合架設野炊鐵鍋）② 金字塔型柴堆（火焰向上竄升快，適合晚會引火）。",
            "【野炊烹煮米飯秘訣】：米洗淨後浸泡 20 分鐘；米與水比例約為 1 : 1.1～1.2。先用大火煮滾至鍋邊冒出蒸氣（約 8～10 分鐘），轉中火收乾水分（聞到米香），轉微火慢煨，最後移開火源【加蓋悶飯 15 分鐘】，飯粒飽滿香Q！"
          ]
        },
        {
          "id": "camo_navigation",
          "title": "（2）戰術偽裝與方向辨識",
          "icon": "eye-slash",
          "content": [
            "【面部迷彩戰術原則】：利用深綠色、棕色、黑色迷彩膏，遵循『凸暗凹亮』原則——將容易反射高光的部位（額頭、鼻樑、顴骨、下巴）塗深色；將陰影凹陷處（眼窩、鼻下、法令處、脖子）塗淺綠色，打破臉部對稱輪廓線。",
            "【指北針地圖定向】：紅色磁針恆指向地磁北方（N）。將指北針基板邊緣對準地圖起點與終點，旋轉分度盤使紅箭頭與磁針重合，判讀前進方位角（Azimuth）。",
            "【手錶指針定向法】：在北半球，將指針式手錶放平，將『時針』對準太陽位置，則時針與表面『12點刻度』之間的夾角角平分線，所指方向即為【正南方】！",
            "【自然生態辨向】：獨立樹木朝南面的枝葉通常較為繁茂，朝北面的樹皮較潮濕易長青苔；觀察伐木樹樁的年輪，年輪較寬疏的一側朝南，密集緊窄的一側朝北。"
          ]
        },
        {
          "id": "knots",
          "title": "（3）出神入化・童軍實用繩結",
          "icon": "link",
          "knotsList": [
            { "name": "單結 (Overhand Knot)", "usage": "防脫結", "desc": "最基礎的繩結，打在繩端防止繩索自滑輪或孔眼中脫落。" },
            { "name": "平結 (Reef Knot)", "usage": "接繩結 (等粗)", "desc": "左壓右、右壓左，用於連接兩條粗細相同之繩索，受力牢固且容易解開。" },
            { "name": "接繩結 (Sheet Bend)", "usage": "接繩結 (粗細不同)", "desc": "粗繩彎成套環，細繩穿繞打結。用於粗細不同或乾濕不同的兩條繩索相接。" },
            { "name": "雙半結 (Two Half Hitches)", "usage": "固著結", "desc": "將繩索固定在樹幹、柱子或圓環上，結形緊密且越拉越緊。" },
            { "name": "營繩結 / 齊來結 (Taut-line Hitch)", "usage": "調節張力結", "desc": "可在繩索上自由滑動以收緊或放鬆帳篷營繩，受風力拉扯時自動咬死固定。" },
            { "name": "稱人結 (Bowline)", "usage": "繩結之王", "desc": "形成一個永不收緊縮小的固定繩圈，被譽為童軍繩結之王，廣泛用於高空垂降、救生套圈與吊掛重物。" },
            { "name": "雙套結 (Clove Hitch)", "usage": "工程架起結", "desc": "繞木樁兩圈交叉壓住，為搭建營門、旗桿、置物架等各類先鋒工程十字結與剪立結的起頭與收尾結。" },
            { "name": "十字結 (Square Lashing)", "usage": "木桿交叉捆紮", "desc": "將兩根呈 90 度十字交叉的木桿牢固捆綁，為工程搭建的核心技藝。" }
          ]
        },
        {
          "id": "snakes",
          "title": "（4）臺灣六大毒蛇辨識與『五要五不』",
          "icon": "shield-alt",
          "snakesList": [
            { "name": "雨傘節", "toxin": "神經毒 (劇毒)", "feature": "黑白相間均勻環節、背脊微突出成稜脊", "habit": "性情溫馴夜間活動，被咬傷時無劇痛腫脹，但數小時內會因呼吸麻痺衰竭致死！" },
            { "name": "眼鏡蛇 (飯匙倩)", "toxin": "神經毒兼細胞毒", "feature": "遭受威脅時前半身直立、頸部擴張成扁平飯匙狀、背部有眼鏡斑紋", "habit": "發出威脅嘶嘶聲，咬傷劇烈疼痛組織快速腫脹壞死。" },
            { "name": "龜殼花", "toxin": "出血毒 (強烈溶血)", "feature": "頭呈明顯三角形（烙鐵頭），體背棕褐色有波浪狀斑塊", "habit": "多夜間活動於落葉堆或草叢，咬傷後傷口劇烈劇痛、大量出血腫脹與組織壞死。" },
            { "name": "赤尾青竹絲", "toxin": "出血毒", "feature": "全身體色翠綠、尾端焦紅褐色、腹部兩側各有一條白色縱線", "habit": "常盤踞於矮灌木叢、竹林或溪流旁枝條，臺灣咬人案例最多但致死率較低。" },
            { "name": "百步蛇", "toxin": "出血毒 (出血量大)", "feature": "頭大呈三角形、吻端尖銳向上翹起、體側有黑褐色三角形斑紋", "habit": "臺灣體型最大毒蛇，排毒量極大，咬傷後皮下出血、起大血泡、組織壞死劇烈。" },
            { "name": "鎖鏈蛇", "toxin": "混合毒 (兼具神經與出血)", "feature": "背部有三條深褐色橢圓鏈狀圓斑，體側圓斑相連如鎖鏈", "habit": "受威脅時盤成圓形劇烈噴氣，臺灣南部與東部特有，毒性猛烈。" }
          ],
          "aidRules": {
            "fiveDo": [
              "【要】保持冷靜：安撫患者坐下或躺平休息，避免奔跑走動加速血液循環毒液擴散。",
              "【要】脫除束縛物：立即取下受傷肢體的戒指、手錶、手鐲、緊身鞋襪，避免肢體腫脹後造成缺血壞死。",
              "【要】彈性包紮：使用彈性繃帶由遠心端向近心端寬鬆包紮（鬆緊度以可插入一根手指為原則），固定傷肢於低於心臟位置。",
              "【要】認清特徵：盡可能看清或用手機拍下蛇類外觀、顏色、頭型，供醫師施打對應抗蛇毒血清。",
              "【要】迅速送醫：撥打 119 或由營地專車火速送往具備抗蛇毒血清的大型醫院救治。"
            ],
            "fiveDont": [
              "【不】切開傷口：嚴禁用刀片或尖銳物切開傷口，以免切斷肌腱血管並造成嚴重二次感染。",
              "【不】用嘴吸吮：口中微小潰瘍會使毒液從口腔黏膜進入施救者體內，極度危險。",
              "【不】冰敷患處：冰敷會使局部血管急劇收縮，導致局部組織缺血壞疽風險暴增。",
              "【不】緊勒止血帶：嚴禁用止血帶或細繩過度緊勒阻斷動脈血液，易導致肢體缺血截肢！",
              "【不】飲用刺激飲品：切勿給傷者飲用酒類、濃茶或咖啡，否則會加速心跳與毒素循環。"
            ]
          }
        },
        {
          "id": "campfire",
          "title": "（5）營火晚會儀式、歡呼與音樂律動",
          "icon": "music",
          "content": [
            "【營火晚會三部曲】：① 神聖迎火（拜火神、引火入場、宣讀拜火詞） ➔ ② 歡狂動唱（班級競賽、隊輔熱舞、萬人齊嗨） ➔ ③ 薪火相傳（燭光夜語、心靈沈澱與師生互道感謝）。",
            "【神聖拜火詞】：『阿給拉～魯巴～魯巴！萬能的火神，請賜予南投國中無比的光明、勇氣與友誼！熊熊營火，燃燒吧！』",
            "【經典營火歌曲】：",
            "  ▶ 《營火歌》：「朋友！燃起這營火，照耀著我們的友誼，火花在黑夜裡飛舞，照亮了少年的夢想...」",
            "  ▶ 《成吉思汗》：「風沙滾滾，戰馬奔馳，嘿！喝！嘿！喝！我們是無敵的南投健兒！」",
            "  ▶ 《第一支舞》：「帶著笑容，你走向我，做個邀請的動作...美麗的夜晚，難忘的旋律...」",
            "  ▶ 《萍聚》：「只要我們曾經擁有過，對你我來講已經足夠...何必在乎天長地久...」"
          ]
        }
      ]
    },
    "mountainTraining": {
      "title": "分站山訓與探索教育教學指引",
      "subtitle": "極限突破・高空垂降・探索解手結・攀岩巨璧・水彈射擊與獨木橋",
      "activities": [
        {
          "id": "rappel",
          "title": "① 膽量大考驗、進擊の垂降",
          "desc": "從高空塔台垂直攀附而下，直面高度恐懼，鍛鍊極限膽識！",
          "equip": "合格攀登岩盔、全身/坐式安全吊帶、雙向自動鎖大D主鎖、八字環/ATC下降器、耐磨防護手套。",
          "steps": [
            "穿戴裝備由專業教官進行雙重檢查（Buddy Check），確保吊帶反扣無鬆脫、岩盔扣緊。",
            "走到平台邊緣，面向塔台，雙腳與肩同寬平踏在壁緣，膝蓋微彎。",
            "身體放膽向後傾斜約 45°～60°，讓背部與岩壁保持直角垂直，重心放低壓在腳底。",
            "上方導向手（左手）輕握主繩保持平衡不握死；下方制動手（右手）握繩置於右後臀部，【右手向前繩鬆即下降、右手往後貼臀即煞停】！"
          ]
        },
        {
          "id": "puzzle_rope",
          "title": "② 解手結 ＆ 團隊跳繩 (PA探索教育)",
          "desc": "打破思維慣性，靠全員溝通協調與步調一致贏得榮譽！",
          "equip": "長拔河繩 / 團隊大跳繩、開闊安全草坪。",
          "steps": [
            "【解手結規則】：全班圍成圓圈，所有人向前伸出右手，隨意握住非相鄰同學的右手；再伸出左手握住另一人的左手。在手不放開的原則下，透過翻轉、跨步、鑽身，將糾纏的人體繩結解成一個大圓圈！",
            "【解手結心法】：不急躁、聽從一人指揮指令、彼此信任肢體柔韌度，培養冷靜分析與集體共識。",
            "【團隊跳繩技巧】：兩位搖繩手保持勻速深幅擺動，全班進場時踩準大繩落地彈起瞬間，齊聲喊『1、2、3！』口號，考驗全班心跳共振。"
          ]
        },
        {
          "id": "rock_climbing",
          "title": "③ 超級蜘蛛人～攀岩絕技",
          "desc": "手腳並用向上攀登，考驗核心力量與路徑規劃！",
          "equip": "人工岩壁、攀岩確保主繩、動力繩、岩盔、坐式吊帶、教官頂繩確保系統。",
          "steps": [
            "【三點不動一點動】：攀爬過程中，四肢永遠保持至少『三點固定接觸岩壁』，一次只移動一隻手或一隻腳。",
            "【腿部蹬起而非手拉】：人體腿部肌力遠大於手臂，手臂微彎放鬆貼壁主要負責平衡，每一步由大腿骨骼發力向上踩蹬！",
            "【三米攀爬原則】：攀登前先在岩下觀察路線，預判踩點與抓握點；登頂後按鈴或拍板，雙手握住主繩坐回吊帶，由教官平穩放下。"
          ]
        },
        {
          "id": "water_battle",
          "title": "④ 生存遊戲～水彈射擊競賽",
          "desc": "刺激震撼的戰術攻防對抗，凝聚小隊無間合作！",
          "equip": "安全電動水彈槍（環保吸水凝膠彈）、全罩式戰術護目面罩、號碼識別背心、充氣掩體陣地。",
          "steps": [
            "【鐵律第一】：從進入射擊場地到結束哨音響起前，【嚴禁私自脫下護目面罩】！",
            "【小隊戰術編制】：隊長指揮佈陣，分為前線突擊組、側翼迂迴組與掩護壓制組。",
            "【掩體射擊要領】：不盲射（伸出槍口前必須看準目標）、不在同一個掩體窗口探頭超過 3 秒、換彈夾退入掩體後方。",
            "【運動家風範】：中彈者自覺高舉雙手示意陣亡並退回安全區，展現誠實與團體風度。"
          ]
        },
        {
          "id": "single_log",
          "title": "⑤ 獨木橋橫渡平衡挑戰",
          "desc": "漫步高空或水上獨木橋，戰勝內心動搖，穩健通往彼岸！",
          "equip": "高空/低空獨木圓木、安全保護網/雙索保護繩、岩盔與吊帶。",
          "steps": [
            "踏上圓木前先做深呼吸調整心率，雙腳微微八字踏穩。",
            "雙臂水平展開微曲，重心沉於肚臍下方，膝蓋保持彈性微彎吸震。",
            "視線鎖定前方橋頭終點，切忌低頭看腳下懸空，一步步勻速平穩滑步前行。"
          ]
        }
      ]
    }
  },
  "checklist": [
    { "category": "證件與個人隨身", "items": ["健保IC卡 (必備！)", "家長聯絡小卡", "個人隨身零用錢 (建議200-300元即可)", "隨身小背包 (活動時攜帶水壺與輕便物品)", "手帕 / 面紙 / 濕紙巾"] },
    { "category": "服裝與防護", "items": ["換洗衣物 1～2 套 (運動休閒排汗為佳)", "防風薄外套 / 保暖衣物 (早晚溫差大)", "運動長褲 (山訓防刮必備，嚴禁穿著裙子或拖鞋)", "好穿耐磨的運動布鞋 / 運動厚襪兩雙", "防曬遮陽帽 / 太陽眼鏡", "輕便雨衣 (防天候變化)"] },
    { "category": "盥洗與生活用品", "items": ["個人衛生毛巾", "牙刷、牙膏、梳子 (響應環保自備)", "水壺 / 保溫水瓶 (隨時補充水分)", "個人常備藥品 (防蚊液、暈車藥、腸胃藥、止痛藥、個人過敏藥等)", "手電筒 / 頭燈 (夜間露營照明用)", "大型耐磨塑膠袋 (裝換洗衣物防潮用)"] },
    { "category": "童軍與活動專用", "items": ["童軍繩 (童軍技能課程用)", "個人環保餐具組 (碗筷湯匙，野炊/BBQ使用)", "手寫筆記本與原子筆", "滿滿的活力與團隊榮譽心！"] }
  ],
  "rules": [
    "1. 團隊紀律：全程聽從導師、值星官及隊輔教官指令，按作息時間集合，嚴禁無故遲到或擅自脫隊離營。",
    "2. 營地安全：營區內禁止奔跑追逐、不攀爬危險欄杆與陡坡；夜間禁止擅自離開分配帳篷。",
    "3. 用火用電：嚴禁在帳篷內使用打火機、蠟燭或任何火源；野炊用火必須有幹部在旁看顧，離去前確實澆熄灰燼。",
    "4. 內務晨檢：隔日早晨各帳篷需依規範折疊睡袋、清掃帳內泥沙、收妥隨身行李，評定內務競賽成績。",
    "5. 競賽精神：炊事競賽、營火表演、山訓挑戰與精神總錦標均採班級團體積分制，勝不驕、敗不餒，展現南投國中優良風範。",
    "6. 緊急應變：活動期間如感身體不適、受傷或中暑暈眩，立即向同帳室長、小隊長、隨隊老師或隊輔通報送醫護站。"
  ]
}

# 1. Save camp_data.json
with open('camp_data.json', 'w', encoding='utf-8') as f:
    json.dump(full_camp_dict, f, ensure_ascii=False, indent=2)
print("Saved camp_data.json successfully!")

# 2. Save data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write('// 南投縣立南投國民中學 115學年度 二年級戶外教育（隔宿露營）資料庫（去個資版）\\n')
    f.write('const CAMP_DATA = ')
    json.dump(full_camp_dict, f, ensure_ascii=False, indent=2)
    f.write(';\\n')
    f.write("if (typeof module !== 'undefined' && module.exports) { module.exports = CAMP_DATA; }\\n")
print("Saved data.js successfully!")

# Write Markdown Handbook
md_content = f"""# 南投縣立南投國民中學 115學年度 二年級戶外教育（隔宿露營）行動手冊（去個資版）

> **活動時間**：115學年度 · 兩天一夜
> **活動地點**：台南柳營尖山埤渡假村（山訓露營）＆ 南投名間親子生態園區
> **參與對象**：南投國中二年級全體師生（共 7 班、106 位同學、7 位導師與隨隊行政師長）
> **手冊說明**：本手冊依據個資保護原則，全體師生人名第二個字均以「O」進行去識別化遮罩處理。

---

## 一、 活動總體統計與行政摘要

- **全校班級數**：7 班（201 ～ 207 班）
- **學生總人數**：106 人（男生 48 人、女生 58 人）
- **飲食習慣統計**：葷食 105 人、素食 1 人（205 班 21 號 張O瑜）
- **帳篷住宿編組**：全校共使用 27 頂帳篷（男生 13 頂、女生 14 頂），每帳配置室長負責點名與安全管理。
- **野炊烤肉編組**：全校共編成 15 個野炊小隊，各隊落實小隊長、副小隊長、大廚、二廚、伙夫、水夫、事務等幹部職能分工。
- **隨隊各班導師名單**：
  - 201 班：黃O月 老師
  - 202 班：黃O君 老師
  - 203 班：林O玟 老師
  - 204 班：李O儒 老師
  - 205 班：林O銓 老師
  - 206 班：許O玉 老師
  - 207 班：黃O慧 老師

---

## 二、 兩天一夜 完整行程時間表

### 📅 第一天（Day 1）
| 時間節點 | 活動項目 | 活動說明與重點指引 | 備註事項 |
| :--- | :--- | :--- | :--- |
| **07:30 - 08:00** | 學校集合 | 各班集合清點人數，實施 921 地震公園逃生演練與行前精神訓勉 | 掌握到齊人數 |
| **08:00 - 10:00** | 乘車出發、安全檢查 | 專車南下國道奔馳，行車安全逃生教育，抵達營地時實施人員與裝備安全檢查 | 繫妥安全帶 |
| **10:00 - 11:00** | 喜相逢～環境認識 | 抵達尖山埤渡假村，活動小隊編組集合，熟悉營地環境、醫護站與安全設施 | 隊伍整齊 |
| **11:00 - 11:30** | 始業式～營規與工作人員介紹 | 開訓典禮！生活輔導員與值星官介紹，宣讀生活競賽與精神總錦標評比要點 | 頒發生活競賽獎項 |
| **11:30 - 12:30** | 我們這一班 | 班級向心力競賽！班旗揮舞、創意班歌與震撼班呼大對決 | 班歌、班呼競賽 |
| **12:30 - 13:30** | 午餐時間 | 各班依席位就座，享用營養豐盛的中式便當，落實垃圾分類 | 中式便當 |
| **13:30 - 14:30** | 野營常識介紹：帳棚搭設講解 | 標準營地配置教學、六人蒙古包帳篷結構（內帳、外帳、營柱、營釘、地布）及搭帳實作領取 | 標準營地教學、搭帳教學 |
| **14:30 - 17:00** | 分站教育 Part 1：童軍技能教育 | 分站輪動課程：<br>（1）生火技巧、烹調方式<br>（2）戰術偽裝、方向辨識<br>（3）出神入化、繩結運用<br>（4）臺灣六大毒蛇、蛇類辨識<br>（5）晚會預習彩排、音樂律動 | 童軍技能教育實作 |
| **17:00 - 19:00** | 晚餐 (炊事競賽) | 各小隊合作野炊，洗菜烹煮、生火控火、擺盤評分，考驗廚藝與團隊默契 | 野炊大考驗 |
| **19:10 - 21:30** | 超ㄅ一ㄤˋ的營火晚會喔！燭光夜語 | 點燃營火！隊輔勁歌熱舞、各班創意節目競賽、團康動唱；【薪火相傳～燭光夜語】與導師分享成長印記 | 晚會評分、真情分享 |
| **21:30 - 22:30** | 盥洗、宵夜 | 依序分批盥洗、享用熱騰騰宵夜，整理個人內務 | 補充水分 |
| **22:30 ---** | 就寢＆查舖 | 回到帳篷，室長確實清點人數，導師巡房查舖，保持營區肅靜進入夢鄉 | 熄燈就寢 |

---

### 📅 第二天（Day 2）
| 時間節點 | 活動項目 | 活動說明與重點指引 | 備註事項 |
| :--- | :--- | :--- | :--- |
| **06:00 - 06:30** | 起床～做個跟太陽賽跑的人 | 晨喚起床！清晨新鮮空氣中梳洗，整理個人睡袋與隨身行囊 | 精神抖擻 |
| **06:30 - 07:20** | 活力有氧、拆帳收整 | 營區大草坪跳活力晨操！全員合作拆卸帳篷、收整營柱營釘，實施內務評分 | 早操時間、拆帳 |
| **07:20 - 08:00** | 早餐時間 | 在營地餐廳享用熱騰騰中式合菜早餐，各桌打飯盛湯，蓄積滿滿活力 | 中式合菜早餐 |
| **08:00 - 11:30** | 分站教育 Part 2：山訓、探索教育 | 突破自我、勇氣激發！分為五大項次：<br>（1）膽量大考驗、進擊の垂降<br>（2）解手結、團隊跳繩<br>（3）超級蜘蛛人～攀岩絕技<br>（4）生存遊戲～水彈競賽<br>（5）獨木橋平衡挑戰 | 山訓探索極限挑戰 |
| **11:00 - 13:00** | 午餐～BBQ 烤肉餐 | 歡樂炭烤大餐！美味肉排、熱狗、時蔬香氣四溢，慶祝各項任務達成 | BBQ烤肉餐 |
| **13:00 - 14:00** | 結訓典禮～～ I’m the Best！！ | 隆重頒獎時間！表揚炊事比賽、營火節目、晨檢內務、分站活動、生活教育與【精神總錦標】大獎 | 榮譽頒獎 |
| **14:00 - 17:00** | 名間親子生態公園巡禮 | 走訪南投 2.6 公頃全齡共融生態公園，暢玩 5 米高彩虹磨石子溜滑梯、攀爬坡與心型草坪 | 名間親子樂園介紹、豬事樂園 |
| **17:00 - 17:10** | 平安抵校 ～～ Bye-Bye！ | 專車平安抵達南投國中，清點行囊互道再見，平安滿載回憶歸來 | 預計抵達學校時間 16:30~17:10 |

---

## 三、 全校帳篷住宿分配總表（去個資版）

| 班級 | 性別 | 帳號/帳別 | 室長座號 | 室長姓名 | 人數 | 同帳成員名單 (座號+姓名) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

for t in tents:
    md_content += f"| {t['class']} | {t['gender']} | {t['tentName']} | {t['leaderSeat']} | {t['leaderName']} | {t['count']} | {t['members']} |\n"

md_content += f"""
---

## 四、 全校野炊/烤肉活動小隊編組總表（去個資版）

| 班級 | 小隊序號 | 人數 | 小隊長 | 副小隊長 | 大廚 | 二廚 | 伙夫 | 水夫 | 事務 | 一般隊員名單 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

for s in squads:
    md_content += f"| {s['class']} | {s['squadName']} | {s['count']} | {s['leader']} | {s['deputy']} | {s['chef1']} | {s['chef2']} | {s['fire']} | {s['water']} | {s['affairs']} | {s['members']} |\n"

md_content += f"""
---

## 五、 教學參考指引專題

### 🏕️ 專題一：野營常識與帳篷搭設指引
1. **蒙古包標準搭設六部曲**：
   - **選地整平**：選擇平坦無積水地面，剔除碎石、硬樹根與帶刺植物。
   - **鋪設地布**：地布邊緣向內折入，絕對不可露在外帳邊緣之外（防止接雨水漏水）。
   - **穿插營柱**：組裝兩根長玻璃纖維營柱，以「推入」方式交叉穿入內帳通管。
   - **立起內帳**：兩人合作將營柱頂彎，插入四角插銷並扣妥內帳掛鉤。
   - **披上外帳**：前後門對齊覆蓋外帳，綁緊內部魔鬼氈，扣緊四角插扣。
   - **打釘拉水線**：營釘以 45°~60° 斜角背對營繩敲入土中，拉緊前庭水線與防風繩，確保內外帳分離通風。
2. **無痕山林 (LNT) 七大準則**：落實垃圾不落地、自備個人環保餐具、營區晚上 22:30 後輕聲細語。

### ⚜️ 專題二：童軍技能教育實作指引
1. **生火技巧與野炊控火**：
   - 火媒棒製作：以小刀 45 度角削出羽毛狀卷屑增加受熱面積。
   - 柴堆類型：井字型（通風好、蓄熱長、適合放鐵鍋煮飯）、金字塔型（引火快火勢旺）。
   - 煮飯火候秘訣：「大火煮滾 ➔ 中火收水 ➔ 轉小火收乾 ➔ 離火加蓋悶飯 15 分鐘」。
2. **戰術偽裝與方向辨識**：
   - 面部迷彩：臉部突出高光處塗深黑/深綠色，凹陷陰影處塗淺綠色，打破面部輪廓特徵。
   - 手錶太陽定向法：時針指向太陽，時針與錶盤 12 點刻度夾角之中分線即為【南方】。
3. **童軍八大繩結**：
   - 單結（防脫）、平結（等粗繩相接）、接繩結（不同粗細繩相接）、雙半結（綁樹幹）、營繩結（自由滑動調營繩張力）、稱人結（繩結之王，固定圈不收縮）、雙套結（綁桿起頭與收尾）、十字結（先鋒工程木桿交叉捆紮）。
4. **臺灣六大毒蛇辨識與「五要五不」急救原則**：
   - 雨傘節（神經毒、黑白等寬）、眼鏡蛇（神經毒、膨頸嘶叫）、龜殼花（出血毒、烙鐵頭）、赤尾青竹絲（出血毒、綠身焦尾）、百步蛇（出血毒、鼻翹吻尖）、鎖鏈蛇（混合毒、鏈狀圓斑）。
   - **五要**：要冷靜坐下、要脫飾品束縛、要彈性繃帶寬鬆包紮、要記蛇特徵、要迅速送醫。
   - **五不**：不切開傷口、不用嘴吸吮、不冰敷、不緊勒止血帶、不喝刺激性飲料。
5. **營火晚會狂歡與燭光夜語**：
   - 拜火詞：「阿給拉～魯巴～魯巴！偉大的火神，請賜予我們光明與勇氣！」
   - 經典歌謠：《營火歌》、《成吉思汗》、《第一支舞》、《萍聚》。

### 🧗 專題三：分站山訓與探索教育指引
1. **進擊の高空垂降**：
   - 配備岩盔、坐式吊帶、大D主鎖、八字環、防磨手套。
   - 雙腳與肩同寬平踏壁面，身體後傾 45°~60°，重心放低；右制動手置於右後臀部，放繩下降、收繩煞停。
2. **PA探索解手結 ＆ 團隊跳繩**：
   - 解手結：雙手隨機握住不同同學雙手，在不鬆手下翻轉鑽爬解開圓圈，考驗耐心與溝通。
   - 團隊跳繩：兩人甩大長繩，全員齊跳齊喊口號，考驗默契與心跳共振。
3. **超級蜘蛛人～攀岩絕技**：
   - 「三點不動一點動」、「重量在腳不在手」，手臂放鬆維持平衡，大腿發力向上蹬起。
4. **水彈射擊生存遊戲**：
   - 嚴禁在場內脫下全罩護目面罩，靈活運用充氣掩體與小隊戰術包抄。
5. **獨木橋橫渡平衡**：
   - 膝蓋微曲放低重心，雙臂平展，視線注視前方終點，克服恐懼平穩過橋。

---

## 六、 行前裝備與行李打包清單

- [ ] **證件與個人隨身**：健保卡（必備）、家長聯絡卡、輕便隨身小背包、面紙、濕紙巾、零用錢約 200~300 元。
- [ ] **服裝與保暖鞋襪**：換洗衣物 1~2 套（排汗運動服為佳）、防風薄外套、運動長褲（山訓防刮必備，嚴禁穿裙子拖鞋）、好走球鞋與厚襪 2 雙、遮陽帽、輕便雨衣。
- [ ] **盥洗與生活用品**：毛巾、自備牙刷牙膏（響應環保）、水壺或保溫瓶、防蚊液、個人常備用藥（暈車藥、過敏藥）、手電筒、衣物防潮塑膠袋。
- [ ] **童軍野炊專用**：童軍繩、個人環保餐具組（碗筷湯匙）、筆記本與原子筆。

---

## 七、 營規公約與緊急聯絡應變網

1. 全程服從導師、值星官與教官指揮，禁止擅自脫離營隊與無故遲到。
2. 營區內禁止奔跑推擠，嚴禁靠近深水危險水域。
3. 嚴禁在帳篷內點火使用打火機；野炊用火必須確實看管撲滅。
4. 身體如有不適、中暑、發燒或意外碰撞，第一時間向同帳室長、小隊長或導師通報處置。
"""

with open('南投國中隔宿手冊-去個資.md', 'w', encoding='utf-8') as f:
    f.write(md_content)
print("Saved 南投國中隔宿手冊-去個資.md successfully!")

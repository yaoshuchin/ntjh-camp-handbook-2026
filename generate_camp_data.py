# -*- coding: utf-8 -*-
import openpyxl
import json
import re

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

excel_path = '../1151019二年級隔宿手冊/南投國中115二年級隔宿手寫資料電子檔(完整試算表) (1).xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

# 導師名單（全部第二字替換為 O）
classes_meta = {
    '801': {'classNum': '801', 'className': '801 班', 'alias': '201', 'bus': '3 車', 'mentor': '黃O月', 'mentorMasked': '黃O月', 'maleCount': 10, 'femaleCount': 7, 'total': 17},
    '802': {'classNum': '802', 'className': '802 班', 'alias': '202', 'bus': '2 車', 'mentor': '黃O君', 'mentorMasked': '黃O君', 'maleCount': 6, 'femaleCount': 12, 'total': 18},
    '803': {'classNum': '803', 'className': '803 班', 'alias': '203', 'bus': '3 車', 'mentor': '林O玟', 'mentorMasked': '林O玟', 'maleCount': 6, 'femaleCount': 9, 'total': 15},
    '804': {'classNum': '804', 'className': '804 班', 'alias': '204', 'bus': '2 車', 'mentor': '李O儒', 'mentorMasked': '李O儒', 'maleCount': 7, 'femaleCount': 8, 'total': 15},
    '805': {'classNum': '805', 'className': '805 班', 'alias': '205', 'bus': '1 車', 'mentor': '林O銓', 'mentorMasked': '林O銓', 'maleCount': 7, 'femaleCount': 4, 'total': 11},
    '806': {'classNum': '806', 'className': '806 班', 'alias': '206', 'bus': '1 車', 'mentor': '許O玉', 'mentorMasked': '許O玉', 'maleCount': 4, 'femaleCount': 5, 'total': 9},
    '807': {'classNum': '807', 'className': '807 班', 'alias': '207', 'bus': '丁 車', 'mentor': '黃O慧', 'mentorMasked': '黃O慧', 'maleCount': 8, 'femaleCount': 13, 'total': 21},
}

# 1. 學生資料解析（全部姓名第二字替換為 O）
ws_students = wb['全校學生清冊']
student_dict_by_name_class = {}
students = []

for r in range(5, ws_students.max_row + 1):
    c_class = str(ws_students.cell(r, 1).value or '').strip()
    if not c_class:
        continue
    c_num = ''
    for k, v in classes_meta.items():
        if v['alias'] in c_class or k in c_class:
            c_num = k
            break
    
    seat = int(ws_students.cell(r, 3).value or 0)
    raw_name = str(ws_students.cell(r, 4).value or '').strip()
    gender = str(ws_students.cell(r, 5).value or '').strip()
    tent_raw = str(ws_students.cell(r, 6).value or '').strip()
    leader_raw = str(ws_students.cell(r, 7).value or '').strip()
    squad_raw = str(ws_students.cell(r, 8).value or '').strip()
    role_raw = str(ws_students.cell(r, 9).value or '').strip()
    diet_raw = str(ws_students.cell(r, 10).value or '葷食').strip()
    
    clean_raw_name = raw_name.replace('(素)', '').replace('（素）', '').strip()
    is_leader = ('室長' in leader_raw)
    is_veg = ('素' in diet_raw or '素' in raw_name)
    masked_student_name = mask_name(clean_raw_name)

    st_obj = {
        'id': len(students) + 1,
        'classNum': c_num,
        'className': classes_meta[c_num]['className'],
        'bus': classes_meta[c_num]['bus'],
        'mentor': classes_meta[c_num]['mentor'],
        'mentorMasked': classes_meta[c_num]['mentorMasked'],
        'seat': seat,
        'realName': masked_student_name,  # 確實寫入去個資名字
        'name': masked_student_name,
        'gender': gender,
        'tentRaw': tent_raw,
        'tentId': '',
        'isLeader': is_leader,
        'leaderLabel': '室長' if is_leader else '成員',
        'squadRaw': squad_raw,
        'squadId': 0,
        'role': role_raw,
        'diet': '素食' if is_veg else '葷食',
        'isVeg': is_veg
    }
    students.append(st_obj)
    student_dict_by_name_class[(c_num, clean_raw_name)] = st_obj

# 2. PDF 帳棚對照表
pdf_tents_data = [
    # 801
    {"tentId": "A01", "classNum": "801", "gender": "男", "members": ["林辰諼", "張竤鈞", "張群偉", "吳駿岷", "谷詠恩"]},
    {"tentId": "A02", "classNum": "801", "gender": "男", "members": ["湯凱丞", "陳致廷", "許宸瑋", "陳揚宗", "賴柏豪"]},
    {"tentId": "B01", "classNum": "801", "gender": "女", "members": ["林頁言", "劉芷含", "藍思詒"]},
    {"tentId": "B02", "classNum": "801", "gender": "女", "members": ["林育嫻", "江姝婷", "陳綵翎", "陳詩涵"]},
    # 802
    {"tentId": "A03", "classNum": "802", "gender": "男", "members": ["黃士睿", "葉品毅", "廖梓惟"]},
    {"tentId": "A04", "classNum": "802", "gender": "男", "members": ["劉軒宇", "張哲瑋", "簡伯宸"]},
    {"tentId": "B03", "classNum": "802", "gender": "女", "members": ["李芮妮", "李聿甯", "鄭綵琳", "黃馨蒂"]},
    {"tentId": "B04", "classNum": "802", "gender": "女", "members": ["簡觀懿", "黃艾薇", "賴翊其", "鐘云彤"]},
    {"tentId": "B05", "classNum": "802", "gender": "女", "members": ["郭音琪", "廖子昕", "胡詠薰", "張苡桔"]},
    # 803
    {"tentId": "A05", "classNum": "803", "gender": "男", "members": ["許泳煜", "陳宥熙", "蔡宇呈"]},
    {"tentId": "A06", "classNum": "803", "gender": "男", "members": ["陳倚天", "陳訢瑜", "李佳成"]},
    {"tentId": "B06", "classNum": "803", "gender": "女", "members": ["王妍芝", "石榮芳", "吳予恩", "吳欣蓉", "潘芝汝"]},
    {"tentId": "B07", "classNum": "803", "gender": "女", "members": ["邱炘慈", "陳姿羽", "謝雨璇", "沈芳愉"]},
    # 804
    {"tentId": "A07", "classNum": "804", "gender": "男", "members": ["陳律光", "蕭敏皓", "陳佑昇"]},
    {"tentId": "A08", "classNum": "804", "gender": "男", "members": ["林伸澄", "許富翔", "劉宇振", "張俊帆"]},
    {"tentId": "B08", "classNum": "804", "gender": "女", "members": ["王語涵", "陳紅妘", "張亦晴", "劉芷硯"]},
    {"tentId": "B09", "classNum": "804", "gender": "女", "members": ["羅凡茜", "簡傳璇", "余宥婷", "洪妤瑄"]},
    # 805
    {"tentId": "A09", "classNum": "805", "gender": "男", "members": ["林彥竹", "郭品佑", "陳樂庭", "嚴黃諭"]},
    {"tentId": "A10", "classNum": "805", "gender": "男", "members": ["吳宸鋒", "簡宏宇", "張哲瑜"]},
    {"tentId": "B10", "classNum": "805", "gender": "女", "members": ["劉芷硯", "吳子瑜", "黃羽薇", "鄭芯妮"]},
    # 806
    {"tentId": "A11", "classNum": "806", "gender": "男", "members": ["吳成文", "曾宣承", "洪偉倫", "張景棋"]},
    {"tentId": "B11", "classNum": "806", "gender": "女", "members": ["陳渝臻", "李珮榕", "林宣妤", "范雯英", "廖云慈"]},
    # 807
    {"tentId": "A12", "classNum": "807", "gender": "男", "members": ["吳冠霆", "洪圓熙", "張祐睿", "黃宇壬"]},
    {"tentId": "A13", "classNum": "807", "gender": "男", "members": ["呂冠辰", "林有福", "林羿旻", "許譽瀚"]},
    {"tentId": "B12", "classNum": "807", "gender": "女", "members": ["張羽瑄", "郭俞岑", "黃楥浠", "詹依靜"]},
    {"tentId": "B13", "classNum": "807", "gender": "女", "members": ["林亮妤", "吳語桐", "陳柔錥", "蕭奕晨", "簡宓緹"]},
    {"tentId": "B14", "classNum": "807", "gender": "女", "members": ["廖婕涵", "陳宥伶", "古采潼", "胡芸熙"]},
]

# 3. PDF 野炊分組對照表
pdf_squads_data = [
    # 801
    {"squadId": 1, "classNum": "801", "members": ["劉芷含", "林頁言", "谷詠恩", "張竤鈞", "張群偉", "林辰諼", "陳揚宗", "賴柏豪", "藍思詒"]},
    {"squadId": 2, "classNum": "801", "members": ["林育嫻", "陳綵翎", "江姝婷", "陳詩涵", "湯凱丞", "吳駿岷", "許宸瑋", "陳致廷"]},
    # 802
    {"squadId": 3, "classNum": "802", "members": ["黃艾薇", "廖梓惟", "賴翊其", "簡觀懿", "鐘云彤", "張哲瑋"]},
    {"squadId": 4, "classNum": "802", "members": ["葉品毅", "李聿甯", "李芮妮", "鄭綵琳", "黃馨蒂", "黃士睿"]},
    {"squadId": 5, "classNum": "802", "members": ["廖子昕", "胡詠薰", "郭音琪", "張苡桔", "簡伯宸", "劉軒宇"]},
    # 803
    {"squadId": 6, "classNum": "803", "members": ["王妍芝", "石榮芳", "吳予恩", "吳欣蓉", "潘芝汝", "許泳煜", "陳宥熙", "蔡宇呈"]},
    {"squadId": 7, "classNum": "803", "members": ["邱炘慈", "陳姿羽", "謝雨璇", "沈芳愉", "陳倚天", "陳訢瑜", "李佳成"]},
    # 804
    {"squadId": 8, "classNum": "804", "members": ["陳律光", "張俊帆", "林伸澄", "劉宇振", "許富翔", "蕭敏皓", "陳佑昇"]},
    {"squadId": 9, "classNum": "804", "members": ["張亦晴", "洪妤瑄", "余宥婷", "簡傳璇", "陳紅妘", "羅凡茜", "王語涵", "劉芷硯"]},
    # 805
    {"squadId": 10, "classNum": "805", "members": ["林彥竹", "吳宸鋒", "簡宏宇", "郭品佑", "陳樂庭", "嚴黃諭", "張哲瑜"]},
    {"squadId": 11, "classNum": "805", "members": ["劉芷硯", "吳子瑜", "黃羽薇", "鄭芯妮"]},
    # 806
    {"squadId": 12, "classNum": "806", "members": ["廖云慈", "洪偉倫", "范雯英", "林宣妤", "張景棋", "吳成文", "陳渝臻", "李珮榕", "曾宣承"]},
    # 807
    {"squadId": 13, "classNum": "807", "members": ["郭俞岑", "黃楥浠", "詹依靜", "張羽瑄", "胡芸熙", "古采潼", "陳宥伶"]},
    {"squadId": 14, "classNum": "807", "members": ["吳語桐", "林亮妤", "陳柔錥", "廖婕涵", "蕭奕晨", "簡宓緹"]},
    {"squadId": 15, "classNum": "807", "members": ["吳冠霆", "呂冠辰", "林有福", "林羿旻", "洪圓熙", "張祐睿", "許譽瀚", "黃宇壬"]},
]

# 關聯帳棚與野炊至學生
for t_data in pdf_tents_data:
    c_num = t_data['classNum']
    t_id = t_data['tentId']
    for m_name in t_data['members']:
        st = student_dict_by_name_class.get((c_num, m_name))
        if st:
            st['tentId'] = t_id

for s_data in pdf_squads_data:
    c_num = s_data['classNum']
    sq_id = s_data['squadId']
    for m_name in s_data['members']:
        st = student_dict_by_name_class.get((c_num, m_name))
        if st:
            st['squadId'] = sq_id
            st['squadName'] = f"第 {sq_id} 組"

# 建構帳棚列表
tents_list = []
for idx, t in enumerate(pdf_tents_data):
    c_num = t['classNum']
    t_id = t['tentId']
    gender = t['gender']
    member_objs = []
    leader_obj = None
    
    for m_name in t['members']:
        st = student_dict_by_name_class.get((c_num, m_name))
        if st:
            m_info = {
                'seat': st['seat'],
                'realName': st['name'],
                'name': st['name'],
                'isLeader': st['isLeader'],
                'role': st['role'],
                'diet': st['diet'],
                'isVeg': st['isVeg']
            }
            member_objs.append(m_info)
            if st['isLeader']:
                leader_obj = m_info
    
    if not leader_obj and member_objs:
        leader_obj = member_objs[0]

    tents_list.append({
        'id': idx + 1,
        'tentId': t_id,
        'classNum': c_num,
        'className': classes_meta[c_num]['className'],
        'bus': classes_meta[c_num]['bus'],
        'mentor': classes_meta[c_num]['mentor'],
        'gender': gender,
        'genderLabel': f"{gender}生帳",
        'count': len(member_objs),
        'leader': leader_obj,
        'members': member_objs,
        'notes': '包含室長' if any(m['isLeader'] for m in member_objs) else ''
    })

# 建構野炊小隊列表
squads_list = []
for idx, sq in enumerate(pdf_squads_data):
    c_num = sq['classNum']
    sq_id = sq['squadId']
    member_objs = []
    
    officers = {
        'leader': None,
        'deputy': None,
        'chef1': None,
        'chef2': None,
        'fire': None,
        'water': None,
        'affairs': None,
    }
    
    has_veg = False
    for m_name in sq['members']:
        st = student_dict_by_name_class.get((c_num, m_name))
        if st:
            if st['isVeg']:
                has_veg = True
            m_info = {
                'seat': st['seat'],
                'realName': st['name'],
                'name': st['name'],
                'role': st['role'],
                'diet': st['diet'],
                'isVeg': st['isVeg']
            }
            member_objs.append(m_info)
            
            r = st['role']
            if '小隊長' == r:
                officers['leader'] = m_info
            elif '副小隊長' in r or '副' in r:
                officers['deputy'] = m_info
            elif '大廚' in r:
                officers['chef1'] = m_info
            elif '二廚' in r:
                officers['chef2'] = m_info
            elif '伙夫' in r:
                officers['fire'] = m_info
            elif '水夫' in r:
                officers['water'] = m_info
            elif '事務' in r:
                officers['affairs'] = m_info

    squads_list.append({
        'id': idx + 1,
        'squadId': sq_id,
        'squadName': f"第 {sq_id} 組",
        'classNum': c_num,
        'className': classes_meta[c_num]['className'],
        'bus': classes_meta[c_num]['bus'],
        'mentor': classes_meta[c_num]['mentor'],
        'count': len(member_objs),
        'officers': officers,
        'members': member_objs,
        'hasVeg': has_veg,
        'vegNote': '含素食餐 1 人' if has_veg else '全組葷食'
    })

# 4. 遊覽車編組 (4 車，隨車師長全部第二字替換為 O)
bus_data = [
    {
        'busId': '1車',
        'busTitle': '遊覽車 1 車',
        'classes': ['805 班', '806 班'],
        'staff': [
            {'title': '學務主任', 'realName': '董O遠', 'name': '董O遠'},
            {'title': '805 導師', 'realName': '林O銓', 'name': '林O銓'},
            {'title': '806 導師', 'realName': '許O玉', 'name': '許O玉'}
        ],
        'studentCounts': {'male': 11, 'female': 9, 'total': 20},
        'students': [s for s in students if s['classNum'] in ['805', '806']]
    },
    {
        'busId': '2車',
        'busTitle': '遊覽車 2 車',
        'classes': ['802 班', '804 班'],
        'staff': [
            {'title': '802 導師', 'realName': '黃O君', 'name': '黃O君'},
            {'title': '804 導師', 'realName': '李O儒', 'name': '李O儒'}
        ],
        'studentCounts': {'male': 13, 'female': 20, 'total': 33},
        'students': [s for s in students if s['classNum'] in ['802', '804']]
    },
    {
        'busId': '3車',
        'busTitle': '遊覽車 3 車',
        'classes': ['801 班', '803 班'],
        'staff': [
            {'title': '801 導師', 'realName': '黃O月', 'name': '黃O月'},
            {'title': '803 導師', 'realName': '林O玟', 'name': '林O玟'}
        ],
        'studentCounts': {'male': 16, 'female': 16, 'total': 32},
        'students': [s for s in students if s['classNum'] in ['801', '803']]
    },
    {
        'busId': '丁車',
        'busTitle': '遊覽車 丁車',
        'classes': ['807 班'],
        'staff': [
            {'title': '訓育組長', 'realName': '姚O勤', 'name': '姚O勤'},
            {'title': '807 導師', 'realName': '黃O慧', 'name': '黃O慧'}
        ],
        'studentCounts': {'male': 8, 'female': 13, 'total': 21},
        'students': [s for s in students if s['classNum'] in ['807']]
    }
]

# 5. 行程時間表
itinerary_data = [
    {
        'day': 1,
        'date': '115年10月27日 (星期二)',
        'title': '第一天：啟程開訓 · 營地建設 · 童軍技能 · 營火晚會',
        'events': [
            {
                'time': '07:30 - 08:00',
                'title': '學校集合、逃生演練',
                'location': '南投國中 / 921地震公園暨國際會展中心園區',
                'type': 'gather',
                'desc': '各班集合清點人數，實施 921 地震公園逃生避難演練與行前安全叮嚀。',
                'keyPoint': '掌握到齊人數，聽從導師與行政師長指揮'
            },
            {
                'time': '08:00 - 10:00',
                'title': '乘車出發、安全檢查',
                'location': '國道專車南下',
                'type': 'travel',
                'desc': '全員準時發車！行車安全逃生教育，抵達尖山埤營地時實施人員與裝備安全檢查。',
                'keyPoint': '全體師生全程繫妥安全帶，車內保持整潔'
            },
            {
                'time': '10:00 - 11:00',
                'title': '喜相逢～環境認識',
                'location': '尖山埤渡假村大草坪',
                'type': 'activity',
                'desc': '活動小隊編組集合、確認各項裝備，熟悉營地環境、醫護站與安全設施。',
                'keyPoint': '各中隊迅速成形，培養班級小隊向心力'
            },
            {
                'time': '11:00 - 12:00',
                'title': '始業式～營規與工作人員介紹',
                'location': '大會場 / 司令台',
                'type': 'ceremony',
                'desc': '開訓典禮！介紹隨隊工作人員、生活輔導員與值星官，宣讀營規與生活競賽精神總錦標計分方式。',
                'keyPoint': '服從值星官指令，展現南投國中榮譽精神'
            },
            {
                'time': '12:00 - 13:00',
                'title': '午餐時間（中式便當）',
                'location': '營地休息區',
                'type': 'meal',
                'desc': '各班就座享用豐盛營養中式便當，用餐後落實垃圾減量與資源回收分類。',
                'keyPoint': '飯前洗手、餐後落實廚餘與垃圾分類'
            },
            {
                'time': '13:00 - 14:00',
                'title': '野營常識介紹：帳棚搭設與器材領取',
                'location': '露營區露營帳位',
                'type': 'scout',
                'desc': '標準營地教學與搭帳教學：①帳棚搭設講解 ②環境認識 ③器材使用領取。熟記搭帳口訣：「一拉對角、二立中柱、三拉角繩、四拉邊繩、五加外帳膨內帳」。',
                'keyPoint': '小隊分工合作，內外帳不能貼緊，鞋子倒放防止蟲蛇'
            },
            {
                'time': '14:00 - 17:00',
                'title': '分站教育 Part 1：童軍技能教育',
                'location': '各大分站教育站點',
                'type': 'scout',
                'desc': '五大輪動實作課程：\n（1）生火技巧、烹調方式\n（2）戰術偽裝、方向辨識\n（3）出神入化、繩結運用（八大繩結）\n（4）六大毒蛇、蛇類辨識與急救處置\n（5）晚會預習、音樂律動動唱。',
                'keyPoint': '全員參與做中學，累積小隊積分'
            },
            {
                'time': '17:00 - 19:00',
                'title': '晚餐時間：野炊炊事競賽',
                'location': '炊事野炊烤肉區',
                'type': 'meal',
                'desc': '全校 15 個野炊小隊廚藝大比拚！小隊長掌控時間、大廚二廚洗切炒煮、伙夫水夫生火控火與供水。評比標準：菜色美味、衛生安全、團隊分工、環境復原。',
                'keyPoint': '注意用火安全與食材生熟分開，素食單獨料理'
            },
            {
                'time': '19:10 - 21:30',
                'title': '超ㄅ一ㄤˋ的營火晚會喔！～燭光夜語',
                'location': '營火晚會中央大草坪',
                'type': 'campfire',
                'desc': '高潮登場！拜火儀式燃起熊熊營火，隊輔勁歌熱舞、班級創意節目競賽、師生趣味動唱；「薪火相傳～燭光夜語」，手捧燭光，與班導師分享青春成長記憶與真情告白。',
                'keyPoint': '全場熱情喝采，注意火源安全，真情凝聚班級力量'
            },
            {
                'time': '21:30 - 22:30',
                'title': '盥洗、享用熱騰騰宵夜',
                'location': '營地浴室 / 各帳區',
                'type': 'activity',
                'desc': '依序分批盥洗、整理內務行囊，領取熱騰騰宵夜補充體力。',
                'keyPoint': '節約用水，注意地板濕滑'
            },
            {
                'time': '22:30 -----',
                'title': '就寢＆夜間查舖',
                'location': '露營帳區（A01~A13 / B01~B14）',
                'type': 'night',
                'desc': '室長確實清點全帳人數回報，導師與值星官巡視查舖，營區保持肅靜，互道晚安進入夢鄉。',
                'keyPoint': '嚴禁私自跨帳或擅自夜遊，鞋子反扣置於外帳下'
            }
        ]
    },
    {
        'day': 2,
        'date': '115年10月28日 (星期三)',
        'title': '第二天：晨喚有氧 · 山訓探索 · BBQ盛宴 · 榮譽結訓',
        'events': [
            {
                'time': '06:00 - 06:30',
                'title': '起床～做個跟太陽賽跑的人',
                'location': '露營帳區',
                'type': 'gather',
                'desc': '晨喚號角響起！走出帳篷迎接晨曦，整理個人睡袋與防潮墊，清潔梳洗。',
                'keyPoint': '迅速整裝，精神抖擻'
            },
            {
                'time': '06:30 - 07:20',
                'title': '活力有氧（早操時間）與內務曬帳',
                'location': '大草坪 / 營區',
                'type': 'activity',
                'desc': '在晨光中跳活力早操！實施帳篷晨檢與曬帳技巧（拔四角釘、調鬆邊繩、抬高固定通風乾燥）。',
                'keyPoint': '拔內帳四角營釘、曬帳乾燥才能收帳'
            },
            {
                'time': '07:20 - 08:00',
                'title': '早餐時間（中式合菜）',
                'location': '渡假村餐廳',
                'type': 'meal',
                'desc': '在營地餐廳享用熱騰騰中式合菜早餐，各桌打飯盛湯，補足上午山訓挑戰所需熱量。',
                'keyPoint': '落實餐桌禮儀，多吃蔬菜與熱稀飯'
            },
            {
                'time': '08:00 - 11:30',
                'title': '分站教育 Part 2：山訓、探索教育極限挑戰',
                'location': '尖山埤高空山訓設施與探索場地',
                'type': 'mountain',
                'desc': '極限挑戰與團隊信任大考驗：\n（1）膽量大考驗、進擊の垂降（高空垂直垂降）\n（2）解手結、團隊跳繩（PA團隊默契）\n（3）超級蜘蛛人～攀岩絕技（人工岩壁攀爬）\n（4）生存遊戲、水彈競賽（團隊掩護對抗）\n（5）獨木橋（雙索、三索突擊吊橋橫渡）。',
                'keyPoint': '穿戴合格護具，絕對服從教官口令，三點不動一點動'
            },
            {
                'time': '11:30 - 14:00',
                'title': '歡樂午餐：BBQ 烤肉大餐',
                'location': '尖山埤戶外烤肉場',
                'type': 'meal',
                'desc': '歡慶挑戰成功！各小隊大快朵頤炭烤美味肉片、香腸、甜不辣、青椒時蔬，共享團隊榮耀。',
                'keyPoint': '生熟食夾子分開，徹底烤熟再食用，火苗妥善熄滅'
            },
            {
                'time': '14:00 - 15:00',
                'title': '結訓典禮～～I’m the Best！！頒獎典禮',
                'location': '大會場',
                'type': 'ceremony',
                'desc': '各項競賽榮譽揭曉！頒發：炊事比賽、晚會節目、晨檢內務、分站活動、生活教育與最受矚目的【精神總錦標】！',
                'keyPoint': '展現勝不驕敗不餒的風度，為同儕熱情喝采'
            },
            {
                'time': '15:00 - 16:20',
                'title': '平安抵校～～Bye-Bye！滿載回憶平安返家',
                'location': '國道專車北上返抵南投國中',
                'type': 'travel',
                'desc': '清點行李行囊，向尖山埤營地揮手道別，專車平安返抵學校，家長接送溫暖返家。',
                'keyPoint': '預計抵達學校時間 16:20，記得向家人報平安'
            }
        ]
    }
]

# 6. 行李打包檢核清單
checklist_data = [
    {'id': 'c1', 'category': '重要證件與金錢', 'name': '健保 IC 卡', 'icon': '🪪', 'desc': '身分識別與就醫必備，請放在隨身背包內層夾鏈袋。', 'required': True},
    {'id': 'c2', 'category': '重要證件與金錢', 'name': '少量零錢零食', 'icon': '🪙', 'desc': '適量隨身零錢（勿帶過多貴重財物）與少許高熱量行動乾糧。', 'required': False},
    {'id': 'c3', 'category': '服裝與穿著', 'name': '換洗衣物及保暖外套', 'icon': '👕', 'desc': '2套透氣換洗衣物、內衣褲、襪子（多備1雙）、早晚防風保暖外套。', 'required': True},
    {'id': 'c4', 'category': '服裝與穿著', 'name': '運動鞋與耐磨長褲', 'icon': '👟', 'desc': '進行山訓攀岩、垂降與草地活動必備，禁止穿拖鞋進行訓練。', 'required': True},
    {'id': 'c5', 'category': '服裝與穿著', 'name': '涼拖鞋', 'icon': '🩴', 'desc': '盥洗與夜間帳篷周邊換穿使用（山訓時不可穿）。', 'required': False},
    {'id': 'c6', 'category': '個人衛生與清潔', 'name': '盥洗用具（牙刷、牙膏、毛巾）', 'icon': '🪥', 'desc': '個人衛生用品、洗髮精/沐浴乳旅行組、小毛巾。', 'required': True},
    {'id': 'c7', 'category': '個人衛生與清潔', 'name': '衛生紙與濕紙巾', 'icon': '🧻', 'desc': '隨身攜帶袖珍面紙、濕紙巾，野炊與如廁方便清潔。', 'required': True},
    {'id': 'c8', 'category': '個人衛生與清潔', 'name': '個人備用口罩', 'icon': '😷', 'desc': '多備2-3片乾淨口罩以備不時之需。', 'required': True},
    {'id': 'c9', 'category': '防護與應急用品', 'name': '雨具（輕便型雨衣）', 'icon': '🌧️', 'desc': '攜帶輕便型雨衣，防止活動期間山區偶發陣雨。', 'required': True},
    {'id': 'c10', 'category': '防護與應急用品', 'name': '手電筒（含充足電池）', 'icon': '🔦', 'desc': '夜間查舖、營地行走與突發停電指引必備照明工具。', 'required': True},
    {'id': 'c11', 'category': '防護與應急用品', 'name': '防曬及防蚊保養用品', 'icon': '🧴', 'desc': '遮陽帽、防曬乳、防蚊液（避免被戶外小黑蚊或昆蟲叮咬）。', 'required': False},
    {'id': 'c12', 'category': '防護與應急用品', 'name': '私人個人常用藥品', 'icon': '💊', 'desc': '氣喘吸入劑、過敏藥、感冒藥、暈車藥等經醫師處方之常備藥品。', 'required': False},
    {'id': 'c13', 'category': '收納與數位設備', 'name': '旅行雙肩大背包', 'icon': '🎒', 'desc': '堅固耐用雙肩背包，可收納所有行李，避免手提散落。', 'required': True},
    {'id': 'c14', 'category': '收納與數位設備', 'name': '塑膠袋 / 髒衣收納袋', 'icon': '🛍️', 'desc': '備用 2-3 個塑膠袋，用於分隔換洗髒衣服或潮濕物品。', 'required': True},
    {'id': 'c15', 'category': '收納與數位設備', 'name': '手機與行動電源', 'icon': '🔋', 'desc': '配合學校規範於指定時段聯絡家人報平安，注意妥善保管。', 'required': False}
]

# 7. 營規與生活公約
rules_data = [
    {
        'title': '營地生活規範',
        'icon': '🏕️',
        'items': [
            '一切行動聽從隨隊師長、值星官及隊輔教官指揮，嚴禁私自離隊或擅自前往非活動區域。',
            '各小隊隨時保持隊形整齊，行走步伐一致，班呼與精神口號宏亮。',
            '愛護營地公物與花草樹木，損壞公物照價賠償。',
            '遇任何身體不適、蚊蟲叮咬或突發狀況，第一時間向班導師或醫護站回報。'
        ]
    },
    {
        'title': '帳篷與夜間管理規範',
        'icon': '⛺',
        'items': [
            '各帳室長負有點名回報之責，22:30 就寢號響後一律進帳熄燈，不得喧嘩走動。',
            '嚴格禁止男同學擅入女生帳區，亦禁止女同學擅入男生帳區。',
            '鞋子倒扣平放在外帳之下，防止晨露浸濕及蜈蚣、蟲蛇鑽入。',
            '出帳篷隨手拉緊紗門拉鍊，保持帳內乾爽與防蚊蟲。'
        ]
    },
    {
        'title': '野炊與飲食衛生守則',
        'icon': '🍳',
        'items': [
            '野炊時嚴格注意火源安全，生食與熟食餐具砧板徹底分開，避免交叉污染。',
            '食材必須徹底煮熟後方可食用；素食者設有專屬獨立炊具，不可混雜。',
            '野炊完畢後，小隊全體務必徹底刷洗鍋碗瓢盆、擦乾器具並清點交回，恢復營地清潔。'
        ]
    },
    {
        'title': '山訓與水彈活動鐵律',
        'icon': '🧗',
        'items': [
            '進入山訓場嚴禁嬉戲打鬧，確實穿戴頭盔、安全吊帶與各項防護用具。',
            '山訓設施如高空垂降、人工攀岩、突擊吊橋橫渡，務必遵從「三點不動一點動」口訣。',
            '水彈射擊遊戲全程嚴禁取下護目面罩，非射擊區一律槍口朝下並關閉保險，嚴禁對近距離或無裝備人員射擊。'
        ]
    }
]

# # 8. 童軍技能指引（包含每單元圖片、步驟分圖、8種繩結圖影、6種方向圖影、4種急救圖影、4種毒蛇圖影、5要5不圖示）
scout_knowledge = [
    {
        'id': 'camp_ridge',
        'category': '營地建設與屋式帳',
        'icon': '🏕️',
        'image': 'assets/img/tent_general_camp.jpg',
        'imageCaption': '南投國中露營營地標準露營帳棚（蒙古包帳）結構與營地規劃圖解',
        'videos': [
            {'title': '蒙古包露營帳篷標準搭設六部曲教學', 'url': 'https://www.youtube.com/watch?v=AcHiBUqwBQc'},
            {'title': '蔡興隆老師：帳篷搭設與露營常識', 'url': 'https://www.youtube.com/watch?v=HLJ6EbRRk08'},
            {'title': '六人帳篷搭建分解動作實作示範', 'url': 'https://www.youtube.com/watch?v=kYnLsrpQwMQ'}
        ],
        'desc': '標準露營場地規劃包含：搭帳區（門口順風）、炊事區（靠近水源）、活動場地、洗手間與垃圾分類場。',
        'tentPitchSteps': [
            '步驟 1【取出鋪平】：將內帳取出，攤開鋪平。「如何取，就如何收，簡單又輕鬆」。',
            '步驟 2【組合營柱】：組合四邊營柱，視帳篷規格一般而言有 2~4 根，接節緊密確實。',
            '步驟 3【固定地布】：將營柱與地布四邊小釘固定，對齊帳位，準備立起。',
            '步驟 4【吊掛內帳】：將內帳掛勾與營柱吊掛接合，平穩撐起內帳主體結構。',
            '步驟 5【穿架外帳】：將支撐外帳短營柱組合好，與門方向平行垂直，穿過內帳頂端與外帳組合。',
            '步驟 6【拉繩固定】：加外帳（Mark商標朝外），副營繩 45° 釘入固定，保持內外帳分離不反潮。'
        ],
        'stepImages': [
            {'step': 1, 'title': '1. 取出鋪平', 'image': 'assets/img/tent_pitch_step_1.jpg', 'desc': '將內帳取出攤開鋪平，確認營門位置與拉鍊閉合。'},
            {'step': 2, 'title': '2. 組合營柱', 'image': 'assets/img/tent_pitch_step_2.jpg', 'desc': '組合交叉主營柱，檢查金屬套管確實緊扣。'},
            {'step': 3, 'title': '3. 固定插銷', 'image': 'assets/img/tent_pitch_step_3.jpg', 'desc': '將營柱四端插入地布四角插銷或固定小釘。'},
            {'step': 4, 'title': '4. 吊掛內帳', 'image': 'assets/img/tent_pitch_step_4.jpg', 'desc': '將內帳外緣塑膠掛勾依序扣在營柱上，撐起圓頂。'},
            {'step': 5, 'title': '5. 穿架外帳', 'image': 'assets/img/tent_pitch_step_5.jpg', 'desc': '短營柱橫向支撐門簷前廳，組裝外帳頂部。'},
            {'step': 6, 'title': '6. 拉繩打釘', 'image': 'assets/img/tent_pitch_step_6.jpg', 'desc': '覆蓋防水外帳，拉副營繩45度釘入地面，完成搭設。'}
        ],
        'mnemonics': {
            'pitch': '一拉對角、二立中柱、三拉角繩、四拉邊繩、五加外帳膨內帳。',
            'pack': '一拜天地，二拜高堂，夫妻相拜，送入洞房。',
            'sunTents': '拔內帳四角營釘 ➔ 調鬆內帳邊繩 ➔ 抬高內帳透氣 ➔ 固定內帳曬乾收帳。'
        }
    },
    {
        'id': 'scout_knots',
        'category': '童軍常用八大繩結',
        'icon': '🪢',
        'image': 'assets/img/rope_knots_manual.jpg',
        'imageCaption': '南投國中露營手冊第 15 頁：常用八大繩結完整圖解',
        'videos': [
            {'title': '童軍初級必學八大繩結全攻略', 'url': 'https://www.youtube.com/watch?v=CcbWx_sKo08'},
            {'title': '平結、雙套結與營繩結搭帳實作教學', 'url': 'https://www.youtube.com/watch?v=wXQJd770cK4'},
            {'title': '八大繩結操作要領與快速記憶法', 'url': 'https://www.youtube.com/watch?v=68E6pA40kXg'}
        ],
        'knots': [
            {
                'name': '單結 (Overhand Knot)',
                'type': '防脫結',
                'desc': '最基本的繩結，打於繩端防止脫線滑脫，亦為許多複合繩結之起手基礎。',
                'image': 'assets/img/knot_single.jpg',
                'video': {'title': '單結打法教學', 'url': 'https://www.youtube.com/watch?v=S0Tq422Q8h8'}
            },
            {
                'name': '八字結 (Figure-of-Eight Knot)',
                'type': '繩端防脫結',
                'desc': '強度顯著優於單結，受強烈拉力後依然極易解開，廣泛應用於攀登登山繩索末端。',
                'image': 'assets/img/knot_eight.jpg',
                'video': {'title': '八字結打法教學', 'url': 'https://www.youtube.com/watch?v=68E6pA40kXg'}
            },
            {
                'name': '平結 (Reef Knot / Square Knot)',
                'type': '接等粗繩結',
                'desc': '口訣「左壓右、右壓左」，連接兩條粗細相同之繩索，常用於急救三角巾包紮與打包。',
                'image': 'assets/img/knot_reef.jpg',
                'video': {'title': '平結打法教學', 'url': 'https://www.youtube.com/watch?v=wXQJd770cK4'}
            },
            {
                'name': '接繩結 (Sheet Bend)',
                'type': '接異徑繩結',
                'desc': '粗繩彎成套環、細繩穿繞咬合，專用於連接粗細不同或乾濕不同的兩條繩索。',
                'image': 'assets/img/knot_sheetbend.jpg',
                'video': {'title': '接繩結打法教學', 'url': 'https://www.youtube.com/watch?v=kYx9y9m1h3o'}
            },
            {
                'name': '雙套結 (Clove Hitch)',
                'type': '工程起手王',
                'desc': '繞桿兩圈交叉扣入，將繩索牢靠固定於圓木營柱或雷管，為所有童軍工程之起手與收尾。',
                'image': 'assets/img/knot_clovehitch.jpg',
                'video': {'title': '雙套結打法教學', 'url': 'https://www.youtube.com/watch?v=aG0gW7ZzL70'}
            },
            {
                'name': '營繩結 (Taut-line Hitch)',
                'type': '張力調節結',
                'desc': '可在主繩上滑動微調鬆緊度，受力時自我咬死固定，搭帳拉營繩調節張力必學之結。',
                'image': 'assets/img/knot_tautline.jpg',
                'video': {'title': '營繩結打法教學', 'url': 'https://www.youtube.com/watch?v=HLJ6EbRRk08'}
            },
            {
                'name': '雙半結 (Two Half Hitches)',
                'type': '繫固結',
                'desc': '繩端連續兩次半結繞扣於樹幹或圓環，越拉越牢靠，便於迅速微調與解開。',
                'image': 'assets/img/knot_twohalfhitches.jpg',
                'video': {'title': '雙半結打法教學', 'url': 'https://www.youtube.com/watch?v=vV95R-1g9qY'}
            },
            {
                'name': '活結 (Slip Knot)',
                'type': '束口便利結',
                'desc': '打於繩身成活套，輕拉繩尾即可瞬間解開，適用於臨時繫掛裝備或收攏袋口。',
                'image': 'assets/img/knot_slip.jpg',
                'video': {'title': '活結打法教學', 'url': 'https://www.youtube.com/watch?v=CcbWx_sKo08'}
            }
        ]
    },
    {
        'id': 'direction_camo',
        'category': '自然方向辨識',
        'icon': '🧭',
        'image': 'assets/img/direction_16_compass.jpg',
        'imageCaption': '南投國中露營手冊第 17 頁：16 方位盤方位角圖解',
        'videos': [
            {'title': '指北針使用教學與地圖定向三步驟', 'url': 'https://www.youtube.com/watch?v=7ie52VsGiSA'},
            {'title': '野外求生：無指針大自然方位辨識', 'url': 'https://www.youtube.com/watch?v=eYkZgW8kS74'},
            {'title': '太陽影子手錶日晷定向法', 'url': 'https://www.youtube.com/watch?v=1xN5Rk76Z70'}
        ],
        'desc': '身處野外沒有手機或指南針時，可透過大自然天體與生物徵兆辨識方位：',
        'methods': [
            {
                'name': '指南針與地圖',
                'desc': '磁針紅色端永遠指向磁北（360°/0°），搭配「水平持平、磁北對正、地圖正置」三步驟精準定向。',
                'image': 'assets/img/dir_compass_map.jpg',
                'video': {'title': '指北針與地圖定向教學', 'url': 'https://www.youtube.com/watch?v=7ie52VsGiSA'}
            },
            {
                'name': '太陽與月亮規律',
                'desc': '日出東方、日落西方；北半球正午 12:00 太陽在正南方、物體影子指向正北方。亦可使用立竿見影法或時針角平分線法。',
                'image': 'assets/img/dir_sun_moon.jpg',
                'video': {'title': '太陽與月相辨向教學', 'url': 'https://www.youtube.com/watch?v=eYkZgW8kS74'}
            },
            {
                'name': '星象觀測',
                'desc': '尋找北斗七星天璇與天樞兩星連線向勺口外延長 5 倍距離即可找到「北極星」（小熊座尾端），直指正北方！',
                'image': 'assets/img/dir_stars_polaris.jpg',
                'video': {'title': '北斗七星尋北極星教學', 'url': 'https://www.youtube.com/watch?v=1xN5Rk76Z70'}
            },
            {
                'name': '年輪與枝葉疏密',
                'desc': '樹木截面年輪「南寬疏、北緊密」（向南日照充沛生長快）；樹冠南側繁茂、北側陰涼多生長青苔地衣。',
                'image': 'assets/img/dir_tree_rings.jpg',
                'video': {'title': '樹木年輪與青苔辨向教學', 'url': 'https://www.youtube.com/watch?v=kR0tZ8x4u5Q'}
            },
            {
                'name': '向日葵花盤朝向',
                'desc': '手冊第 17 頁官方記載：向日葵花盤上午 12:00 以前普遍朝向「東南方」，下午 12:00 以後追隨陽光偏向「西南方」。',
                'image': 'assets/img/dir_sunflower.jpg',
                'video': {'title': '向日葵追日辨向教學', 'url': 'https://www.youtube.com/watch?v=GCR36w72YjM'}
            },
            {
                'name': '傳統建築坐向',
                'desc': '手冊第 17 頁官方記載：臺灣閩南傳統三合院與古老墓碑大抵採「坐北朝南」，冬避東北季風、夏迎涼爽西南風。',
                'image': 'assets/img/dir_trad_building.jpg',
                'video': {'title': '傳統建築坐北朝南辨向教學', 'url': 'https://www.youtube.com/watch?v=qT5vL0G7_kM'}
            }
        ]
    },
    {
        'id': 'first_aid',
        'category': '野外簡易急救處置',
        'icon': '🩹',
        'image': 'assets/img/firstaid_heatstroke.jpg',
        'imageCaption': '南投國中露營手冊第 22 頁：中暑急救標準處理流程圖',
        'videos': [
            {'title': '紅十字會：戶外緊急包紮止血法', 'url': 'https://www.youtube.com/watch?v=ah7ZRuEL2yE'},
            {'title': '中暑熱衰竭與抽筋急救流程教學', 'url': 'https://www.youtube.com/watch?v=7uK3W0rV9x4'},
            {'title': '骨折夾板固定與流鼻血正確處置', 'url': 'https://www.youtube.com/watch?v=8kP2qX5tY9w'}
        ],
        'desc': '戶外野營活動遭遇突發傷病之標準黃金應急處置流程：',
        'firstAid': [
            {
                'title': '意外割傷止血',
                'desc': '1. 以生理食鹽水或乾淨生水將傷口周遭沖洗乾淨。\n2. 無菌清潔紗布直接「加壓止血」5~10 分鐘，嚴禁亂塗未消毒粉末或藥膏。\n3. 傷肢「抬高高於心臟」減緩出血。\n4. 包紮妥當後送醫評估破傷風疫苗。',
                'image': 'assets/img/fa_cut_bleeding.jpg',
                'video': {'title': '意外割傷加壓止血教學', 'url': 'https://www.youtube.com/watch?v=ah7ZRuEL2yE'}
            },
            {
                'title': '肌肉抽筋緩解',
                'desc': '核心原則「反向緩慢伸展並輕柔按摩」：\n- 小腿抽筋：伸直膝蓋，手將腳掌朝小腿方向扳折拉伸小腿肚。\n- 大腿抽筋：膝部拉直，一手放腳跟抬高腿部，一手輕柔按摩。\n- 補充電解質運動飲料與溫開水，嚴禁暴力拉扯。',
                'image': 'assets/img/fa_muscle_cramp.jpg',
                'video': {'title': '小腿抽筋反向伸展教學', 'url': 'https://www.youtube.com/watch?v=7uK3W0rV9x4'}
            },
            {
                'title': '流鼻血緊急處理',
                'desc': '1. 患者採安靜坐姿，「頭部微微向前傾」（切勿後仰，避免鼻血倒流嗆入氣管或吞入胃部引起嘔吐；亦切勿拍打後頸部）。\n2. 拇指與食指緊捏兩側鼻翼軟骨 5~10 分鐘，改由嘴巴呼吸。\n3. 鼻樑以毛巾冷敷促進微血管收縮，口中血液儘速吐出。',
                'image': 'assets/img/fa_nosebleed.jpg',
                'video': {'title': '流鼻血正確處置教學', 'url': 'https://www.youtube.com/watch?v=y9pL4k3oV2M'}
            },
            {
                'title': '骨折緊急固定',
                'desc': '1. 優先確認意識與呼吸脈搏，切勿嘗試推回移位斷骨。\n2. 就地取材（木板、傘骨、健行杖），固定夾板長度必須「超過骨折處上下兩個關節」！\n3. 無夾板時：上肢固定於胸壁、下肢與健康肢體綑綁在一起。\n4. 脊椎骨折平臥硬板床，由受訓人員長背板搬運送醫。',
                'image': 'assets/img/fa_fracture.jpg',
                'video': {'title': '骨折夾板固定教學', 'url': 'https://www.youtube.com/watch?v=8kP2qX5tY9w'}
            }
        ]
    },
    {
        'id': 'snakes_safety',
        'category': '臺灣六大毒蛇與急救「五要五不」',
        'icon': '🐍',
        'image': 'assets/img/snakes_manual.jpg',
        'imageCaption': '南投國中露營手冊第 16 頁：百步蛇與雨傘節特徵對照圖',
        'videos': [
            {'title': '臺灣六大毒蛇生態特徵辨識全集', 'url': 'https://www.youtube.com/watch?v=fIWV-E_q45o'},
            {'title': '急診專科醫師詳解：毒蛇咬傷黃金處置【五要五不】', 'url': 'https://www.youtube.com/watch?v=ZfRk3B6x_vI'},
            {'title': '野外遇蛇打草驚蛇防範與抗蛇毒血清知識', 'url': 'https://www.youtube.com/watch?v=3gR2kM8zN6Y'}
        ],
        'desc': '臺灣常見四大毒蛇生態辨識與遭蛇咬傷時之標準「五要五不」急救 SOP：',
        'snakes': [
            {
                'name': '百步蛇 (出血性毒 · 蝮蛇科)',
                'venom': '出血性毒',
                'desc': '頭大呈三角形，吻端明顯向上突出翹起，體側具黑褐色大型三角形斑紋。排毒量全台第一，致死率居臺灣毒蛇之首！',
                'image': 'assets/img/snake_hundred_pacer.jpg',
                'video': {'title': '百步蛇特徵與出血毒介紹', 'url': 'https://www.youtube.com/watch?v=fIWV-E_q45o'}
            },
            {
                'name': '雨傘節 (神經性毒 · 蝙蝠蛇科)',
                'venom': '神經性毒',
                'desc': '全身體背有「黑白相間等寬環紋」，背脊呈顯著菱形隆起。毒性全台最強，傷口不痛不腫，數小時內呼吸肌痲痺致死！',
                'image': 'assets/img/snake_many_banded_krait.jpg',
                'video': {'title': '雨傘節黑白環紋神經毒教學', 'url': 'https://www.youtube.com/watch?v=ZfRk3B6x_vI'}
            },
            {
                'name': '赤尾青竹絲 (出血性毒 · 蝮蛇科)',
                'venom': '出血性毒',
                'desc': '全身翠綠，尾端呈特徵性「焦磚紅色」，體側常具白縱線。全台「咬人率第 1 名」，常攀附於茶園、果樹與灌木草叢。',
                'image': 'assets/img/snake_bamboo_viper.jpg',
                'video': {'title': '赤尾青竹絲與青蛇辨識教學', 'url': 'https://www.youtube.com/watch?v=3gR2kM8zN6Y'}
            },
            {
                'name': '龜殼花 (出血性毒 · 蝮蛇科)',
                'venom': '出血性毒',
                'desc': '頭部呈烙鐵三角形，頸部細小，體背有暗褐色不規則波浪龜裂斑塊。夜行出沒廢棄農舍石縫，攻擊迅捷，局部腫脹起血泡。',
                'image': 'assets/img/snake_habu.jpg',
                'video': {'title': '龜殼花夜行攻擊與習性教學', 'url': 'https://www.youtube.com/watch?v=t5J7nL6pQ1k'}
            }
        ],
        'firstAidFiveDos': [
            {'icon': '🐍', 'title': '要視為毒蛇', 'desc': '凡遭蛇咬，第一時間皆以毒蛇咬傷標準謹慎處置，切勿心存僥倖。'},
            {'icon': '🧘', 'title': '要保持冷靜', 'desc': '安撫傷患靜臥休息，嚴禁奔跑與劇烈運動，避免加速血液循環使毒液擴散。'},
            {'icon': '💍', 'title': '要脫下束縛', 'desc': '迅速取下傷肢之戒指、手錶、手鐲、鞋襪，避免局部腫脹後造成缺血壞疽。'},
            {'icon': '🩹', 'title': '要包紮置心臟下', 'desc': '以彈性繃帶寬鬆包紮固定，傷肢務必保持在「低於心臟」位置減緩毒液回流。'},
            {'icon': '🏥', 'title': '要火速就醫記蛇貌', 'desc': '記住或用手機拍下蛇類外觀特徵，火速送醫施打對應抗蛇毒血清！'}
        ],
        'firstAidFiveDonts': [
            {'icon': '🚫🔪', 'title': '不要切開傷口', 'desc': '切開傷口會切斷肌腱血管與神經，造成大量失血與嚴重次發性細菌感染。'},
            {'icon': '🚫👄', 'title': '不要用嘴吸吮', 'desc': '施救者口腔微小黏膜創口極易吸收毒素，反而導致施救者共同中毒！'},
            {'icon': '🚫🧊', 'title': '不要冰敷傷口', 'desc': '冰敷會造成局部微血管劇烈痙攣缺血，加速患部組織發黑壞死。'},
            {'icon': '🚫🪢', 'title': '不要緊勒止血帶', 'desc': '過度緊勒阻斷動脈血流，極易引發肢體缺血性壞死而面臨截肢危機。'},
            {'icon': '🚫☕', 'title': '不要飲用刺激品', 'desc': '嚴禁飲用含酒精飲料、濃茶或咖啡，避免刺激心臟跳動加速毒素擴散。'}
        ]
    }
]

# 整合為完整 CAMP_DATA（去個資版）
full_camp_data = {
    'info': {
        'school': '南投縣立南投國民中學',
        'title': '115學年度 二年級戶外教育（隔宿露營）行動數位手冊',
        'subtitle': '尖山埤山訓探索 · 野營炊事 · 團結成長之旅（去個資版）',
        'dates': '115年10月27日(星期二) ～ 10月28日(星期三)',
        'duration': '兩天一夜',
        'contractor': '中國青年旅行社有限公司中部分公司',
        'manager': {'title': '團控經理', 'name': '邱O凱', 'realName': '邱O凱', 'phone': '0972-721756', 'telLink': 'tel:0972721756'},
        'campLocation': {
            'name': '台南柳營尖山埤渡假村露營區',
            'phone': '06-6233888',
            'telLink': 'tel:066233888',
            'address': '台南市柳營區旭山里60號',
            'mapUrl': 'https://maps.google.com/?q=柳營尖山埤渡假村',
            'desc': '坐擁尖山埤水庫百甲湖光山色，配備完善露營草坪區、野炊烤肉場、高空山訓攀岩場與大營火晚會草坪。'
        },
        'schoolLocation': {
            'name': '南投縣立南投國民中學',
            'phone': '049-2222549',
            'telLink': 'tel:0492222549',
            'address': '南投縣南投市祖祠路361號',
            'mapUrl': 'https://maps.google.com/?q=南投市立南投國民中學',
            'desc': '集合出發（921地震公園逃生演練）與平安賦歸之起訖點。'
        },
        'stats': {
            'studentsTotal': 106,
            'maleStudents': 48,
            'femaleStudents': 58,
            'vegetarianStudents': 1,
            'classesCount': 7,
            'tentsTotal': 27,
            'maleTents': 13,
            'femaleTents': 14,
            'squadsTotal': 15,
            'busesTotal': 4
        },
        'staff': [
            {'title': '校長', 'realName': '劉O彥', 'name': '劉O彥', 'bus': '公務'},
            {'title': '學務主任', 'realName': '董O遠', 'name': '董O遠', 'bus': '1 車'},
            {'title': '訓育組長', 'realName': '姚O勤', 'name': '姚O勤', 'bus': '丁 車'},
            {'title': '801 導師', 'realName': '黃O月', 'name': '黃O月', 'bus': '3 車'},
            {'title': '802 導師', 'realName': '黃O君', 'name': '黃O君', 'bus': '2 車'},
            {'title': '803 導師', 'realName': '林O玟', 'name': '林O玟', 'bus': '3 車'},
            {'title': '804 導師', 'realName': '李O儒', 'name': '李O儒', 'bus': '2 車'},
            {'title': '805 導師', 'realName': '林O銓', 'name': '林O銓', 'bus': '1 車'},
            {'title': '806 導師', 'realName': '許O玉', 'name': '許O玉', 'bus': '1 車'},
            {'title': '807 導師', 'realName': '黃O慧', 'name': '黃O慧', 'bus': '丁 車'},
            {'title': '團控經理', 'realName': '邱O凱', 'name': '邱O凱', 'bus': '旅行社'}
        ]
    },
    'classes': classes_meta,
    'buses': bus_data,
    'students': students,
    'tents': tents_list,
    'squads': squads_list,
    'itinerary': itinerary_data,
    'checklist': checklist_data,
    'rules': rules_data,
    'scoutKnowledge': scout_knowledge
}

# 輸出 JSON
with open('camp_data.json', 'w', encoding='utf-8') as f:
    json.dump(full_camp_data, f, ensure_ascii=False, indent=2)

# 輸出 data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write('// 南投縣立南投國民中學 115學年度 二年級隔宿露營行動數位手冊資料庫（去個資版）\n')
    f.write('const CAMP_DATA = ')
    json.dump(full_camp_data, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print("Successfully generated camp_data.json and data.js with strict masked names and scout media!")

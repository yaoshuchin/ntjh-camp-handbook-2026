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

classes_meta = {
    '801': {'classNum': '801', 'className': '801 班', 'alias': '201', 'bus': '3 車', 'mentor': '黃麗月', 'mentorMasked': '黃O月', 'maleCount': 10, 'femaleCount': 7, 'total': 17},
    '802': {'classNum': '802', 'className': '802 班', 'alias': '202', 'bus': '2 車', 'mentor': '黃惠君', 'mentorMasked': '黃O君', 'maleCount': 6, 'femaleCount': 12, 'total': 18},
    '803': {'classNum': '803', 'className': '803 班', 'alias': '203', 'bus': '3 車', 'mentor': '林宜玟', 'mentorMasked': '林O玟', 'maleCount': 6, 'femaleCount': 9, 'total': 15},
    '804': {'classNum': '804', 'className': '804 班', 'alias': '204', 'bus': '2 車', 'mentor': '李佩儒', 'mentorMasked': '李O儒', 'maleCount': 7, 'femaleCount': 8, 'total': 15},
    '805': {'classNum': '805', 'className': '805 班', 'alias': '205', 'bus': '1 車', 'mentor': '林富銓', 'mentorMasked': '林O銓', 'maleCount': 7, 'femaleCount': 4, 'total': 11},
    '806': {'classNum': '806', 'className': '806 班', 'alias': '206', 'bus': '1 車', 'mentor': '許招玉', 'mentorMasked': '許O玉', 'maleCount': 4, 'femaleCount': 5, 'total': 9},
    '807': {'classNum': '807', 'className': '807 班', 'alias': '207', 'bus': '丁 車', 'mentor': '黃瓊慧', 'mentorMasked': '黃O慧', 'maleCount': 8, 'femaleCount': 13, 'total': 21},
}

# 1. 學生資料解析
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
    real_name = str(ws_students.cell(r, 4).value or '').strip()
    gender = str(ws_students.cell(r, 5).value or '').strip()
    tent_raw = str(ws_students.cell(r, 6).value or '').strip()
    leader_raw = str(ws_students.cell(r, 7).value or '').strip()
    squad_raw = str(ws_students.cell(r, 8).value or '').strip()
    role_raw = str(ws_students.cell(r, 9).value or '').strip()
    diet_raw = str(ws_students.cell(r, 10).value or '葷食').strip()
    
    clean_real_name = real_name.replace('(素)', '').replace('（素）', '').strip()
    is_leader = ('室長' in leader_raw)
    is_veg = ('素' in diet_raw or '素' in real_name)

    st_obj = {
        'id': len(students) + 1,
        'classNum': c_num,
        'className': classes_meta[c_num]['className'],
        'bus': classes_meta[c_num]['bus'],
        'mentor': classes_meta[c_num]['mentor'],
        'mentorMasked': classes_meta[c_num]['mentorMasked'],
        'seat': seat,
        'realName': clean_real_name,
        'name': mask_name(clean_real_name),
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
    student_dict_by_name_class[(c_num, clean_real_name)] = st_obj

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
                'realName': st['realName'],
                'name': st['name'],
                'isLeader': st['isLeader'],
                'role': st['role'],
                'diet': st['diet'],
                'isVeg': st['isVeg']
            }
            member_objs.append(m_info)
            if st['isLeader']:
                leader_obj = m_info
    
    # 若無標註室長，預設第一位為代表
    if not leader_obj and member_objs:
        leader_obj = member_objs[0]

    tents_list.append({
        'id': idx + 1,
        'tentId': t_id,
        'classNum': c_num,
        'className': classes_meta[c_num]['className'],
        'bus': classes_meta[c_num]['bus'],
        'mentor': classes_meta[c_num]['mentor'],
        'mentorMasked': classes_meta[c_num]['mentorMasked'],
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
                'realName': st['realName'],
                'name': st['name'],
                'role': st['role'],
                'diet': st['diet'],
                'isVeg': st['isVeg']
            }
            member_objs.append(m_info)
            
            # 分工指派
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
        'mentorMasked': classes_meta[c_num]['mentorMasked'],
        'count': len(member_objs),
        'officers': officers,
        'members': member_objs,
        'hasVeg': has_veg,
        'vegNote': '含素食餐 1 人' if has_veg else '全組葷食'
    })

# 4. 遊覽車編組 (4 車)
bus_data = [
    {
        'busId': '1車',
        'busTitle': '遊覽車 1 車',
        'classes': ['805 班', '806 班'],
        'staff': [
            {'title': '學務主任', 'realName': '董勳遠', 'name': '董O遠'},
            {'title': '805 導師', 'realName': '林富銓', 'name': '林O銓'},
            {'title': '806 導師', 'realName': '許招玉', 'name': '許O玉'}
        ],
        'studentCounts': {'male': 11, 'female': 9, 'total': 20},
        'students': [s for s in students if s['classNum'] in ['805', '806']]
    },
    {
        'busId': '2車',
        'busTitle': '遊覽車 2 車',
        'classes': ['802 班', '804 班'],
        'staff': [
            {'title': '802 導師', 'realName': '黃惠君', 'name': '黃O君'},
            {'title': '804 導師', 'realName': '李佩儒', 'name': '李O儒'}
        ],
        'studentCounts': {'male': 13, 'female': 20, 'total': 33},
        'students': [s for s in students if s['classNum'] in ['802', '804']]
    },
    {
        'busId': '3車',
        'busTitle': '遊覽車 3 車',
        'classes': ['801 班', '803 班'],
        'staff': [
            {'title': '801 導師', 'realName': '黃麗月', 'name': '黃O月'},
            {'title': '803 導師', 'realName': '林宜玟', 'name': '林O玟'}
        ],
        'studentCounts': {'male': 16, 'female': 16, 'total': 32},
        'students': [s for s in students if s['classNum'] in ['801', '803']]
    },
    {
        'busId': '丁車',
        'busTitle': '遊覽車 丁車',
        'classes': ['807 班'],
        'staff': [
            {'title': '訓育組長', 'realName': '姚述勤', 'name': '姚O勤'},
            {'title': '807 導師', 'realName': '黃瓊慧', 'name': '黃O慧'}
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

# 8. 童軍技能指引
scout_knowledge = [
    {
        'category': '營地建設與屋式帳',
        'icon': '🏕️',
        'desc': '標準露營場地規劃包含：搭帳區（門口順風）、炊事區（靠近水源）、活動場地、洗手間與垃圾分類場。',
        'tentPitchSteps': [
            '第 1 步：清點器材與分配工作，確認營釘14支、主營繩2條、副營繩16條、營柱、雷管雷帽與內外帳。',
            '第 2 步：整地，清除碎石枯枝，選定平坦避風排水良好之地點。',
            '第 3 步：攤開鋪平內帳，營門關上保持形狀，完成帳篷四邊小釘定位。',
            '第 4 步：對角 90° 釘下營釘，組合營柱。',
            '第 5 步：主營繩拉 45°，接雷管使用雙套結，接營釘使用營繩結，營釘以 45° 朝外反向釘入地面。',
            '第 6 步：副營繩拉 45° 釘入固定，撐起內帳。',
            '第 7 步：加上外帳，外帳商標 (Mark) 朝外，內外帳切忌貼緊（避免反潮透水）。',
            '第 8 步：剩餘器材與外袋整齊收入帳篷營門下方。'
        ],
        'mnemonics': {
            'pitch': '一拉對角、二立中柱、三拉角繩、四拉邊繩、五加外帳膨內帳。',
            'pack': '一拜天地，二拜高堂，夫妻相拜，送入洞房。',
            'sunTents': '拔內帳四角營釘 ➔ 調鬆內帳邊繩 ➔ 抬高內帳透氣 ➔ 固定內帳曬乾收帳。'
        }
    },
    {
        'category': '童軍常用八大繩結',
        'icon': '🪢',
        'knots': [
            {'name': '單結 (Overhand Knot)', 'desc': '最基本的繩結，防止繩端脫線鬆開，也是許多複合繩結的基礎。'},
            {'name': '八字結 (Figure-of-Eight Knot)', 'desc': '繩端防滑脫結，強度優於單結，受力後依然容易解開，常應用於攀登繩索末端。'},
            {'name': '平結 (Reef Knot / Square Knot)', 'desc': '連接兩條等粗繩索的最佳繩結，常用於三角巾急救包紮、綑綁包裹，易結易解。'},
            {'name': '接繩結 (Sheet Bend)', 'desc': '連接粗細不同或乾濕不同的兩條繩索，受力後咬合緊密不滑脫。'},
            {'name': '雙套結 (Clove Hitch)', 'desc': '童軍工程必備之王！用於將繩索固定於圓木、營柱或雷管上，為所有繫縛結之開端與結尾。'},
            {'name': '營繩結 (Taut-line Hitch)', 'desc': '可自由滑動調節繩索鬆緊度，受力時能自我咬死固定，專用於搭帳營繩與營釘拉緊調整。'},
            {'name': '雙半結 (Two Half Hitches)', 'desc': '用於將繩索繫緊於樹木或圓環上，結形穩固且容易微調。'},
            {'name': '活結 (Slip Knot)', 'desc': '一拉繩尾即可瞬間解開的便利繩結，用於臨時吊掛物品或束口。'}
        ]
    },
    {
        'category': '自然方向辨識',
        'icon': '🧭',
        'desc': '身處野外沒有手機或指南針時，可透過大自然徵兆辨識方位：',
        'methods': [
            {'name': '指南針與地圖', 'desc': '磁針紅色端永遠指向磁北（360°/0°），藍色或白色指向南（180°）。'},
            {'name': '太陽與月亮規律', 'desc': '日出東方、日落西方；北半球正午 12:00 太陽在正南方，物體影子指向正北方。'},
            {'name': '星象觀測', 'desc': '尋找北斗七星天璇與天樞延伸5倍距離找到「北極星」，即為正北方。'},
            {'name': '年輪與枝葉疏密', 'desc': '樹木年輪較寬疏的一面朝向南方（陽光充沛）、較密集的一面朝向北方；樹葉茂盛翠綠側朝南。'},
            {'name': '向日葵花盤朝向', 'desc': '上午 12:00 以前朝向東南，下午 12:00 以後追隨陽光偏向西南。'},
            {'name': '傳統建築坐向', 'desc': '臺灣傳統閩南古厝與墓碑大抵「坐北朝南」，背風向陽。'}
        ]
    },
    {
        'category': '野外簡易急救處置',
        'icon': '🩹',
        'desc': '戶外活動遭遇突發傷病之黃金應急處置原則：',
        'firstAid': [
            {'title': '意外割傷止血', 'desc': '1. 以生理食鹽水或乾淨清水沖洗傷口。\n2. 使用清潔無菌紗布直接覆蓋傷口「加壓止血」。\n3. 抬高傷肢高於心臟位置。\n4. 切勿亂灑未經消毒之藥粉或藥油，包紮後視情況送醫。'},
            {'title': '肌肉抽筋緩解', 'desc': '大原則「往抽筋的反方向緩慢伸展拉直並輕柔按摩」：\n- 手抽筋：輕緩拉直抽筋手指，輕揉手掌。\n- 小腿抽筋：伸直膝蓋，手扶腳掌往小腿方向扳折拉伸小腿肚。\n- 大腿抽筋：大腿前側抽筋向後彎曲膝蓋拉伸股四頭肌；後側抽筋伸直膝蓋抬腿壓腳掌。'},
            {'title': '流鼻血緊急處理', 'desc': '1. 保持冷靜，患者採「坐姿、頭部微微向前傾」（切勿後仰，以免鼻血倒流嗆入氣管）。\n2. 拇指與食指緊捏兩側鼻翼軟骨 5~10 分鐘，改由嘴巴呼吸。\n3. 在鼻樑敷冰毛巾冷敷促進血管收縮，口中血液儘速吐出。\n4. 若 15 分鐘後仍無法止血應立即就醫。'},
            {'title': '骨折緊急固定', 'desc': '1. 優先確認意識與呼吸道通暢，切勿任意搬動骨折部位。\n2. 就地取材（木板、傘骨、健行杖），固定夾板長度必須「超過骨折上下兩個關節」。\n3. 傷肢固定後儘速聯絡醫護送醫。'}
        ]
    },
    {
        'category': '臺灣六大毒蛇與急救「五要五不」',
        'icon': '🐍',
        'desc': '臺灣常見主要毒蛇辨識與被蛇咬傷時之標準急救 SOP：',
        'snakes': [
            {'name': '百步蛇 (出血性毒)', 'desc': '鼻端向上突出，體背有明顯黑褐色三角形斑紋，體型粗壯，致死率居首。'},
            {'name': '雨傘節 (神經性毒)', 'desc': '體背有黑白相間之規則環紋，咬人率高但傷口不腫不痛，容易延誤就醫導致呼吸麻痺。'},
            {'name': '赤尾青竹絲 (出血性毒)', 'desc': '全身翠綠，尾端磚紅色，臺灣咬人率最高的毒蛇，常棲息於草叢灌木。'},
            {'name': '龜殼花 (出血性毒)', 'desc': '體背為棕褐色不規則碎斑如龜殼，夜間活動力強。'}
        ],
        'firstAidRules': {
            'do': '【五要】1.要冷靜記住蛇類特徵或拍照。2.要脫下戒指手鐲等束縛物防止腫脹壞死。3.要用彈性繃帶包紮患肢（不可太緊）。4.要讓傷肢保持低於心臟位置。5.要儘速送醫施打抗蛇毒血清。',
            'dont': '【五不】1.不割開傷口。2.不用嘴巴吸吮毒液。3.不冰敷。4.不使用止血帶束緊動脈。5.不飲用刺激性咖啡或含酒精飲料。'
        }
    }
]

# 整合為完整 CAMP_DATA
full_camp_data = {
    'info': {
        'school': '南投縣立南投國民中學',
        'title': '115學年度 二年級戶外教育（隔宿露營）行動數位手冊',
        'subtitle': '尖山埤山訓探索 · 野營炊事 · 團結成長之旅',
        'dates': '115年10月27日(星期二) ～ 10月28日(星期三)',
        'duration': '兩天一夜',
        'contractor': '中國青年旅行社有限公司中部分公司',
        'manager': {'title': '團控經理', 'name': '邱麟凱', 'phone': '0972-721756', 'telLink': 'tel:0972721756'},
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
            {'title': '校長', 'realName': '劉松彥', 'name': '劉O彥', 'bus': '公務'},
            {'title': '學務主任', 'realName': '董勳遠', 'name': '董O遠', 'bus': '1 車'},
            {'title': '訓育組長', 'realName': '姚述勤', 'name': '姚O勤', 'bus': '丁 車'},
            {'title': '801 導師', 'realName': '黃麗月', 'name': '黃O月', 'bus': '3 車'},
            {'title': '802 導師', 'realName': '黃惠君', 'name': '黃O君', 'bus': '2 車'},
            {'title': '803 導師', 'realName': '林宜玟', 'name': '林O玟', 'bus': '3 車'},
            {'title': '804 導師', 'realName': '李佩儒', 'name': '李O儒', 'bus': '2 車'},
            {'title': '805 導師', 'realName': '林富銓', 'name': '林O銓', 'bus': '1 車'},
            {'title': '806 導師', 'realName': '許招玉', 'name': '許O玉', 'bus': '1 車'},
            {'title': '807 導師', 'realName': '黃瓊慧', 'name': '黃O慧', 'bus': '丁 車'},
            {'title': '團控經理', 'realName': '邱麟凱', 'name': '邱O凱', 'bus': '旅行社'}
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
    f.write('// 南投縣立南投國民中學 115學年度 二年級隔宿露營行動數位手冊資料庫\n')
    f.write('const CAMP_DATA = ')
    json.dump(full_camp_data, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print("Successfully generated camp_data.json and data.js!")

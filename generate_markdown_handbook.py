# -*- coding: utf-8 -*-
import json

with open('camp_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

info = d['info']
classes = d['classes']
buses = d['buses']
students = d['students']
tents = d['tents']
squads = d['squads']
itinerary = d['itinerary']
checklist = d['checklist']
rules = d['rules']
scoutKnowledge = d['scoutKnowledge']

md_lines = []
md_lines.append("# 南投縣立南投國民中學 115學年度 二年級戶外教育（隔宿露營）行動手冊（去個資版）\n")
md_lines.append("> **活動名稱**：南投國民中學 115 學年度二年級戶外教育活動（隔宿露營）  ")
md_lines.append("> **活動時間**：115 年 10 月 27 日 (星期二) 至 10 月 28 日 (星期三)，兩天一夜  ")
md_lines.append("> **活動地點**：台南-尖山埤露營區（06-6233888，台南市柳營區旭山里 60 號）  ")
md_lines.append("> **參加對象**：南投國中二年級全體師生，學生 106 人（男 48 人、女 58 人），全體師生共計 116 人  ")
md_lines.append("> **承辦單位**：中國青年旅行社有限公司中部分公司（團控經理 邱O凱 0972-721756）  ")
md_lines.append("> **手冊說明**：本手冊全體師生人名第二個字均以「O」進行去識別化遮罩（如 劉O彥、董O遠、黃O月、林O諼、張O鈞），完全符合個人資料保護法規。\n")
md_lines.append("---\n")

md_lines.append("## 一、 工作人員與班級人數統計表\n")
md_lines.append("| 職稱 / 班級 | 姓名 | 男生 | 女生 | 合計 | 搭乘車次 |")
md_lines.append("| :--- | :--- | :---: | :---: | :---: | :---: |")
md_lines.append("| 校長 | 劉O彥 | — | — | — | 公務車 |")
md_lines.append("| 學務主任 | 董O遠 | — | — | — | 1 車 |")
md_lines.append("| 訓育組長 | 姚O勤 | — | — | — | 丁 車 |")
for c_num, c_info in classes.items():
    md_lines.append(f"| {c_num} 導師 | {c_info['mentorMasked']} | {c_info['maleCount']} | {c_info['femaleCount']} | {c_info['total']} | {c_info['bus']} |")
md_lines.append("| 團控經理 | 邱O凱 | 48 | 58 | 106 | 旅行社 |\n")
md_lines.append("---\n")

md_lines.append("## 二、 兩天一夜 完整行程時間表\n")
for day in itinerary:
    md_lines.append(f"### 📅 {day['date']}（{day['title']}）\n")
    md_lines.append("| 時間節點 | 活動內容 | 重點備註與實施指引 |")
    md_lines.append("| :--- | :--- | :--- |")
    for ev in day['events']:
        md_lines.append(f"| **{ev['time']}** | **{ev['title']}** | {ev['desc']}（地點：{ev['location']} ｜ 提醒：{ev['keyPoint']}） |")
    md_lines.append("\n---\n")

md_lines.append("## 三、 帳篷住宿分配一覽表（全校共 27 頂帳篷）\n")
md_lines.append("| 班級 | 帳號 | 性別 | 車次 | 人數 | 全體住宿名冊（名字第二字 O 遮罩） |")
md_lines.append("| :--- | :--- | :---: | :---: | :---: | :--- |")
for t in tents:
    members_str = "、".join([f"{m['seat']}號 {m['name']}{' (室長)' if m['isLeader'] else ''}{' (素)' if m['isVeg'] else ''}" for m in t['members']])
    md_lines.append(f"| {t['className']} | **{t['tentId']}** | {t['genderLabel']} | {t['bus']} | {t['count']}人 | {members_str} |")
md_lines.append("\n---\n")

md_lines.append("## 四、 野炊炊事分組一覽表（全校共 15 個野炊小隊）\n")
md_lines.append("| 組別 | 班級 | 車次 | 人數 | 小隊全體名冊與分工職掌（名字第二字 O 遮罩） | 飲食習慣 |")
md_lines.append("| :--- | :--- | :---: | :---: | :--- | :---: |")
for sq in squads:
    members_str = "、".join([f"{m['seat']}號 {m['name']}{' [' + m['role'] + ']' if m['role'] else ''}" for m in sq['members']])
    md_lines.append(f"| **{sq['squadName']}** | {sq['className']} | {sq['bus']} | {sq['count']}人 | {members_str} | {sq['vegNote']} |")
md_lines.append("\n---\n")

md_lines.append("## 五、 課程教學專題：野營常識介紹\n")
md_lines.append("### 1. 營地規劃與營地選擇")
md_lines.append("- **營地規劃**：1.搭帳區(門口順風) 2.炊事區(靠近水源) 3.活動場地 4.WC 5.垃圾場。")
md_lines.append("- **營地選擇**：草地、沙地、沙灘、雪地；三大要素：1.靠近水源 2.地勢平坦 3.安全舒適。\n")
md_lines.append("### 2. 屋式帳標準器具與搭設步驟")
md_lines.append("- **器具**：營釘 14 支、主營繩 2 條、副營繩 16 條、營柱、雷管、雷帽、營樑、內帳、外帳。")
md_lines.append("- **十步驟**：(1)清點器材工作分配 (2)整地 (3)營門關上 (4)帳篷定位 (5)對角 90°釘下營釘 (6)組合營柱 (7)主營繩拉45°，接雷管用雙套結，接營釘用營繩結，營釘45°釘入 (8)副營繩拉45°，營釘45°釘入 (9)加外帳，Mark 朝外 (10)剩餘器材和袋子收入帳篷營門下。")
md_lines.append("- **搭帳口訣**：一拉對角、二立中柱、三拉角繩、四拉邊繩、五加外帳膨內帳。")
md_lines.append("- **收外帳口訣**：一拜天地，二拜高堂，夫妻相拜，送入洞房。")
md_lines.append("- **曬帳技巧**：1.拔內帳四角營釘 2.調鬆內帳邊繩 3.抬高內帳 4.固定內帳。")
md_lines.append("- **注意事項**：1.內外帳不能貼緊，否則外面下大雨，裡面下小雨。 2.晚上鞋子倒放在外帳下，防止蛇跑入冬眠。 3.搭帳兩分鐘，收帳三分鐘。\n")
md_lines.append("---\n")

md_lines.append("## 六、 課程教學專題：童軍技能教育\n")
md_lines.append("### 1. 常用八大繩結")
md_lines.append("- **單結**：防脫結，打於繩尾。")
md_lines.append("- **八字結**：防滑脫結，強度優於單結，受力後易解。")
md_lines.append("- **活結**：臨時繫縛，一拉繩尾瞬間解開。")
md_lines.append("- **平結**：左壓右右壓左，連接兩條等粗繩索。")
md_lines.append("- **接繩結**：粗繩成環細繩穿繞，連接粗細不同繩索。")
md_lines.append("- **雙套結**：繞桿交叉扣入，搭帳固定於營柱雷管必備。")
md_lines.append("- **雙半結**：繫緊於樹木或圓環，越拉越牢。")
md_lines.append("- **營繩結**：滑動調節營繩長度張力，受力自我咬死。\n")
md_lines.append("### 2. 自然方向辨識與 16 方位")
md_lines.append("- **工具**：指南針、地圖。")
md_lines.append("- **方法**：追蹤記號、地形、日月規律、星象（北極星）、年輪（密者為北）、樹木茂密（密者為南）、向日葵（12:00前向東南，12:00後向西南）、古老房舍與墓碑坐北朝南。\n")
md_lines.append("### 3. 野外簡易急救處置")
md_lines.append("- **意外割傷**：清水洗淨，紗布直接加壓止血，傷處抬高於心臟，送醫救治。")
md_lines.append("- **肌肉抽筋**：手指拉直輕按；腳趾伸直按摩；大腿膝部拉直抬高腿部按摩；小腿膝蓋伸直腳掌上屈壓向小腿按摩。")
md_lines.append("- **流鼻血**：患者坐椅頭向前傾（切勿後仰或拍打脖子），手指用力捏住兩側鼻部軟骨 5~10 分鐘，冰敷鼻樑，口中血液吐出。")
md_lines.append("- **骨折處理**：就地取材（木板、竹竿），夾板長度超過上下兩關節，固定後送醫。\n")
md_lines.append("### 4. 臺灣毒蛇與急救【五要五不】")
md_lines.append("- **百步蛇**：出血性毒，吻端上翹，體側三角形斑，致死率第一。")
md_lines.append("- **雨傘節**：神經性毒，黑白相間環紋，咬傷不痛不腫易延誤，致死率第二。")
md_lines.append("- **五要**：要視為毒蛇、要保持冷靜、要脫除束縛物、要彈性包紮患肢低於心臟、要迅速就醫。")
md_lines.append("- **五不**：不切開傷口、不用口吸毒、不冰敷患處、不束緊止血帶、不喝刺激性飲品。\n")
md_lines.append("---\n")

md_lines.append("## 七、 課程教學專題：山訓與探索教育\n")
md_lines.append("### 1. 探索教育三哲學與四大執行精神")
md_lines.append("- **體驗學習**：Learning by doing, Everything for fun, Open space, Master。")
md_lines.append("- **三哲學 Full Value Contract**：像團體一樣工作；堅守安全與行動方針；誠懇給予與接受回饋並改變。")
md_lines.append("- **Challenge by Choice**：所有挑戰皆是自主選擇並為選擇承擔責任。\n")
md_lines.append("### 2. 山訓與突擊吊橋技術")
md_lines.append("- **雙索突擊吊橋**：兩手兩足向對岸橫移，步幅每步約 45 公分，手不離手索足不離足索，重心在足索微向前傾。")
md_lines.append("- **三索突擊吊橋**：雙手握兩側繩索，雙腳外八字行走於足索，雙眼注視足索，重心落於足索穩步前進。")
md_lines.append("- **進擊の垂降**：雙腳打開與肩同寬，身體大膽後傾45°~60°，左手導繩、右手置臀側制動煞車。")
md_lines.append("- **人工攀岩**：三點不動一點動、重量在腳不在手、重心貼近岩壁、下方先讀線。\n")
md_lines.append("### 3. 水彈生存競技 13 條安全守則")
md_lines.append("1. 遵守水彈場規則 2. 著個人裝備 3. 嚴禁持槍指人 4. 不得窺視槍口 5. 注意射擊方向距離 6. 槍存安全處 7. **遊戲進行中嚴禁取下護目面罩** 8. 禁止非射擊區射擊 9. 非遊戲時上保險套槍口塞 10. 禁止十英呎內近距射擊 11. 嚴禁對裁判與出局者射擊 12. 嚴禁對非玩家射擊 13. 嚴格遵守各項安全規定。\n")
md_lines.append("---\n")

md_lines.append("## 八、 行前行李打包清單（想一想，準備好了，出發！）\n")
for it in checklist:
    md_lines.append(f"- [{'x' if it['required'] else ' '}] **{it['name']}**{' (必備)' if it['required'] else ''}：{it['desc']}")
md_lines.append("\n---\n")

md_lines.append("## 九、 營規生活須知與考核指標\n")
for r in rules:
    md_lines.append(f"### {r['icon']} {r['title']}")
    for item in r['items']:
        md_lines.append(f"- {item}")
    md_lines.append("")

md_lines.append("---\n")
md_lines.append("## 十、 美好回憶\n")
md_lines.append("> 「在休閒旅遊的地圖上，找到失落已久的寶藏；  ")
md_lines.append("> 發現真實的自己，以及與心靈對話的樂趣；  ")
md_lines.append("> 而福爾摩沙的星空，有我最美的記憶。」  \n")
md_lines.append("南投縣立南投國民中學 115 學年度二年級全體師生 留念\n")

with open('南投國中隔宿手冊-去個資.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))

print("Successfully generated 南投國中隔宿手冊-去個資.md!")

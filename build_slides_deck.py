import json

with open('camp_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

info = data['info']
stats = info['stats']
mentors = info['mentors']
classes = data['classes']
itinerary = data['itinerary']
students = data['students']
tents = data['tents']
squads = data['squads']
guides = data['teachingGuides']
checklist = data['checklist']
rules = data['rules']

day1 = itinerary[0]
day2 = itinerary[1]

# Build HTML
html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>南投國中 115學年度二年級隔宿露營 行動簡報手冊（去個資版）</title>
<meta name="description" content="南投縣立南投國民中學 115學年度二年級戶外教育隔宿露營 簡報式行動手冊，提供投影片全螢幕簡報模式與捲動閱讀模式，支援快速查詢行程、去個資帳篷住宿分配、野炊小隊編組、野營常識、童軍技能、山訓探索教育與生活營規。">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500;700&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="deck.css?v=202610190200">
<style>
  /* 投中二年級隔宿露營專屬風格微調：森林綠與營火橙 */
  :root {{
    --cf-accent: #22c55e;
    --cf-accent-dim: #16a34a;
    --cf-bg-glow: #064e3b;
    --tag-pill: #15803d;
    --fire-orange: #f97316;
  }}
  .tag-badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 700;
    background: rgba(34, 197, 94, 0.18);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.35);
  }}
  .tag-badge.orange {{
    background: rgba(249, 115, 22, 0.18);
    color: #fb923c;
    border-color: rgba(249, 115, 22, 0.35);
  }}
  .tag-badge.blue {{
    background: rgba(56, 189, 248, 0.18);
    color: #38bdf8;
    border-color: rgba(56, 189, 248, 0.35);
  }}
  .table-deck {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 6px;
  }}
  .table-deck th {{
    background: rgba(255, 255, 255, 0.08);
    color: var(--cf-text);
    padding: 6px 8px;
    border: 1px solid var(--cf-rule);
    text-align: left;
    font-weight: 700;
  }}
  .table-deck td {{
    padding: 5px 8px;
    border: 1px solid var(--cf-rule);
    color: var(--cf-text-dim);
  }}
  .table-deck tr:nth-child(even) td {{
    background: rgba(255, 255, 255, 0.02);
  }}
  .table-deck strong {{
    color: #ffffff;
  }}
  .grid-deck-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}
  .grid-deck-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
  }}
  .card-slide {{
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--cf-rule);
    border-radius: 8px;
    padding: 11px 13px;
  }}
  .card-slide h4 {{
    font-size: 14.5px;
    color: var(--cf-accent);
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .card-slide h4.orange {{
    color: var(--fire-orange);
  }}
  .img-slide {{
    width: 100%;
    height: 185px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--cf-rule);
  }}
  .deck-res-box {{
    margin-top: 8px;
    background: rgba(0, 0, 0, 0.28);
    border: 1px solid var(--cf-rule);
    border-radius: 6px;
    padding: 6px 10px;
  }}
  .deck-res-row {{
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 4px;
    font-size: 11px;
  }}
  .deck-res-row:last-child {{
    margin-bottom: 0;
  }}
  .deck-res-label {{
    font-weight: 700;
    color: var(--cf-text);
    min-width: 44px;
  }}
  .deck-res-chip {{
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 1px 6px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 11px;
    color: #cbd5e1;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    transition: all 0.15s ease;
  }}
  .deck-res-chip.map {{
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border-color: rgba(34, 197, 94, 0.35);
  }}
  .deck-res-chip.web {{
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border-color: rgba(56, 189, 248, 0.35);
  }}
  .deck-res-chip.video {{
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border-color: rgba(239, 68, 68, 0.35);
  }}
  .deck-res-chip:hover {{
    filter: brightness(1.25);
    transform: translateY(-1px);
  }}
</style>
</head>
<body class="deck" data-mode="present">
<header class="deck-bar">
  <span class="deck-id">南投國中 115 隔宿露營</span>
  <span class="deck-name">二年級隔宿露營行動簡報手冊（去個資版）</span>
  <div class="deck-tools">
    <a href="app.html" class="deck-btn" style="text-decoration:none; color:var(--cf-accent); border-color:rgba(34,197,94,0.4); margin-right:4px;">📱 手冊網頁版</a>
    <button class="deck-btn" id="toc-btn" type="button">目錄總覽</button>
    <button class="deck-btn is-on" id="mode-btn" type="button">閱讀模式</button>
    <button class="deck-btn" id="fs-btn" type="button">全螢幕</button>
    <span class="deck-count" id="deck-count"></span>
  </div>
</header>
<main class="deck-stage" id="deck-stage">

  <!-- Slide 01: 封面 -->
  <section class="slide slide-cover" id="slide-cover">
    <p class="s-eyebrow">南投縣立南投國民中學 · 115 學年度 · 二年級戶外教育</p>
    <h1 class="s-title-xl" style="font-size: 44px; line-height: 1.25;">隔宿露營 行前說明簡報<br><span style="font-size:30px; color:var(--cf-accent);">尖山埤山訓探索 · 野營炊事 · 名間生態共融（去個資版）</span></h1>
    <p class="s-sub" style="font-size: 18px; margin-top: 14px;">
      活動規劃：兩天一夜 ｜ 集合時間：07:30～08:00 學校集合（921地震公園逃生演練） 08:00 準時發車<br>
      隨隊指導：劉O彥 校長、董O遠 學務主任、姚O勤 訓育組長 暨 二年級全體導師（201~207班）
    </p>
    <div style="margin-top: 16px; display: flex; gap: 10px; justify-content: center;">
      <span class="tag-badge">⛺ 全校 27 頂帳篷</span>
      <span class="tag-badge orange">🍳 15 個野炊小隊</span>
      <span class="tag-badge blue">👥 106 位學生（男48/女58）</span>
    </div>
  </section>

  <!-- Slide 02: 總覽與營地資訊 -->
  <section class="slide" id="slide-overview">
    <p class="s-eyebrow">AGENDA ＆ RESORT INFO</p>
    <h2 class="s-title">活動概況 · 尖山埤渡假村 ＆ 名間生態園區</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <ul class="s-list">
            <li><b>Day 1</b>：學校集合（921逃生演練） ➔ 乘車出發安全檢查 ➔ 抵達尖山埤渡假村 ➔ 始業式 ➔ 我們這一班（班呼/班歌） ➔ 中式便當午餐 ➔ 野營常識/搭帳教學 ➔ 童軍分站技能 ➔ 晚餐野炊競賽 ➔ 超ㄅ一ㄤˋ營火晚會＆燭光夜語 ➔ 盥洗宵夜就寢。</li>
            <li><b>Day 2</b>：活力早操晨檢拆帳 ➔ 中式合菜早餐 ➔ 分站山訓探索教育（高空垂降、解手結、攀岩、水彈、獨木橋） ➔ BBQ烤肉午餐 ➔ 結訓頒獎典禮 ➔ 名間親子生態公園巡禮 ➔ 平安抵校。</li>
          </ul>
        </div>
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>⛺ 台南柳營尖山埤渡假村</h4>
            <div style="font-size:12.5px; color:var(--cf-text-dim);">
              電話：(06) 623-3888 ｜ 台南市柳營區旭山里60號<br>
              特色：台糖旗艦綠意湖景渡假勝地，擁完整露營場地、野炊烤肉區、高空山訓設施與營火晚會草坪。
            </div>
            <div class="deck-res-box">
              <div class="deck-res-row">
                <span class="deck-res-label">地圖：</span>
                <a class="deck-res-chip map" href="https://maps.google.com/?q=柳營尖山埤渡假村" target="_blank">🗺️ Google Map</a>
                <a class="deck-res-chip web" href="https://www.taisugar.com.tw/chinese/CP.aspx?s=357&n=10433" target="_blank">🌐 尖山埤官方網站</a>
              </div>
            </div>
          </div>
          <div class="card-slide">
            <h4>🌿 南投名間親子生態園區</h4>
            <div style="font-size:12.5px; color:var(--cf-text-dim);">
              電話：(049) 222-2106 ｜ 南投縣名間鄉彰南路256號<br>
              特色：南投最大 2.6 公頃全齡共融特色公園，具備 5 米彩虹磨石子滑梯、攀爬坡與心型大草坪。
            </div>
            <div class="deck-res-box">
              <div class="deck-res-row">
                <span class="deck-res-label">地圖：</span>
                <a class="deck-res-chip map" href="https://maps.google.com/?q=名間親子生態園區" target="_blank">🗺️ Google Map</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 03: Day 1 行程 -->
  <section class="slide" id="slide-day1">
    <p class="s-eyebrow">DAY 1 行程細節 · 第一天</p>
    <h2 class="s-title">集結出發・野營搭帳・童軍技能與營火晚會</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <thead><tr><th>時間</th><th>行程項目</th><th>說明與指引</th></tr></thead>
            <tbody>
              <tr><td>07:30-08:00</td><td><strong>學校集合</strong></td><td>各班點名，921地震公園逃生演練</td></tr>
              <tr><td>08:00-10:00</td><td><strong>乘車出發、安全檢查</strong></td><td>行車安全宣導，抵達營地安全檢查</td></tr>
              <tr><td>10:00-11:00</td><td><strong>喜相逢～環境認識</strong></td><td>活動小隊編組集合，熟悉營地環境</td></tr>
              <tr><td>11:00-11:30</td><td><strong>始業式</strong></td><td>營規介紹、工作人員介紹、頒生活競賽獎</td></tr>
              <tr><td>11:30-12:30</td><td><strong>我們這一班</strong></td><td>班旗揮舞、創意班歌班呼競賽</td></tr>
              <tr><td>12:30-13:30</td><td><strong>午餐時間</strong></td><td>營養中式便當，垃圾分類</td></tr>
              <tr><td>13:30-14:30</td><td><strong>野營常識與搭帳教學</strong></td><td>六人帳篷結構講解、搭帳演練與領器材</td></tr>
              <tr><td>14:30-17:00</td><td><strong>童軍技能教育 Part 1</strong></td><td>生火、偽裝定向、繩結、毒蛇、晚會彩排</td></tr>
              <tr><td>17:00-19:00</td><td><strong>晚餐(炊事競賽)</strong></td><td>各隊分工野炊烹調，廚藝擺盤評比</td></tr>
              <tr><td>19:10-21:30</td><td><strong>超ㄅ一ㄤˋ營火晚會！</strong></td><td>引燃營火、班級狂歡動唱、燭光夜語</td></tr>
              <tr><td>21:30-22:30</td><td><strong>盥洗、宵夜</strong></td><td>分批盥洗、熱騰騰宵夜甜品補充水分</td></tr>
              <tr><td>22:30---</td><td><strong>就寢＆查舖</strong></td><td>室長清點人數，導師巡帳查舖熄燈</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <img class="img-slide" src="assets/img/campfire.jpg" alt="營火晚會">
          <div class="tip warn" style="margin-top:8px;">
            <span class="tip-tag">Day 1 叮嚀</span>
            <div class="tip-body">搭帳篷時以<b>推入</b>營柱為主切勿硬拉；野炊生火專人看顧注意用火安全；營火晚會熱情投入，燭光夜語與老師真情分享。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 04: Day 2 行程 -->
  <section class="slide" id="slide-day2">
    <p class="s-eyebrow">DAY 2 行程細節 · 第二天</p>
    <h2 class="s-title">活力晨操・山訓極限探索・BBQ烤肉・名間生態園區</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <thead><tr><th>時間</th><th>行程項目</th><th>說明與指引</th></tr></thead>
            <tbody>
              <tr><td>06:00-06:30</td><td><strong>起床～做個跟太陽賽跑的人</strong></td><td>晨喚梳洗，整理個人睡袋與行囊</td></tr>
              <tr><td>06:30-07:20</td><td><strong>活力有氧、拆帳收整</strong></td><td>大草坪早操、拆卸收帳、內務晨檢評分</td></tr>
              <tr><td>07:20-08:00</td><td><strong>中式合菜早餐</strong></td><td>營地餐廳享用熱騰騰早餐補足元氣</td></tr>
              <tr><td>08:00-11:30</td><td><strong>分站教育 Part 2：山訓探索</strong></td><td>高空垂降、解手結、攀岩、水彈、獨木橋</td></tr>
              <tr><td>11:00-13:00</td><td><strong>午餐～BBQ 烤肉餐</strong></td><td>小隊圍爐BBQ烤肉，香氣四溢慶祝過關</td></tr>
              <tr><td>13:00-14:00</td><td><strong>結訓典禮～～ I’m the Best！！</strong></td><td>頒發炊事、營火、分站、精神總錦標大獎</td></tr>
              <tr><td>14:00-17:00</td><td><strong>名間親子生態公園</strong></td><td>5米彩虹溜滑梯、草坡攀爬、名間豬事樂園</td></tr>
              <tr><td>17:00-17:10</td><td><strong>平安抵校 ～～ Bye-Bye！</strong></td><td>平安返抵南投國中，滿載青春回憶歸賦</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <img class="img-slide" src="assets/img/rappel.jpg" alt="山訓探索">
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">Day 2 叮嚀</span>
            <div class="tip-body">高空山訓嚴格遵從教官口令，<b>手套岩盔吊帶</b>缺一不可；水彈生存遊戲戰場內<b>全程嚴禁脫下護目面罩</b>！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 05: 尖山埤渡假村導覽 -->
  <section class="slide" id="slide-jianshanpi">
    <p class="s-eyebrow">CAMP SITE GUIDE</p>
    <h2 class="s-title">營地導覽 · 柳營尖山埤渡假村</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:10px;">
            <h4>🏕️ 尖山埤水庫湖光生態</h4>
            <p style="font-size:13px; line-height:1.5; color:var(--cf-text-dim);">
              由台灣糖業公司營運之頂級休閒勝地，座落於尖山埤水庫畔。園區林木蓊鬱、空氣清新，富含五百種野生動植物生態，四季湖光倒影宛如江南水鄉。
            </p>
          </div>
          <div class="card-slide">
            <h4>🎯 專業山訓場與露營基地</h4>
            <p style="font-size:13px; line-height:1.5; color:var(--cf-text-dim);">
              園區擁有標準高空塔台垂降場、人工抱石攀岩壁、低空PA探索團隊訓練設施、安全水彈生存遊戲陣地，以及可容納數百人野炊烹飪與圍火歡呼之大型草坪。
            </p>
          </div>
          <div class="deck-res-box">
            <div class="deck-res-row">
              <span class="deck-res-label">電話：</span>
              <span style="color:#cbd5e1;">(06) 623-3888</span>
              <span class="deck-res-label" style="margin-left:10px;">地址：</span>
              <span style="color:#cbd5e1;">台南市柳營區旭山里60號</span>
            </div>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/jianshanpi_2.jpg" alt="尖山埤營地">
          <div style="font-size:12px; color:var(--cf-text-dim); margin-top:6px; text-align:center;">
            翠綠林蔭環繞的尖山埤營區，是全台灣學校露營山訓首選場地
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 06: 名間親子生態公園 -->
  <section class="slide" id="slide-mingjian">
    <p class="s-eyebrow">ATTRACTION GUIDE</p>
    <h2 class="s-title">共融景點 · 南投名間親子生態園區</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:10px;">
            <h4>🌈 5 米高巨型彩虹溜滑梯</h4>
            <p style="font-size:13px; line-height:1.5; color:var(--cf-text-dim);">
              園區最吸睛代表性地標！兩道長達 15 公尺的磨石子滑梯（彎道與直線道），頂部貼心配備大型遮陽天幕，速度感十足，是暢快放電絕佳去處。
            </p>
          </div>
          <div class="card-slide">
            <h4>⛰️ 草坡攀爬坡與無障礙環狀空中步道</h4>
            <p style="font-size:13px; line-height:1.5; color:var(--cf-text-dim);">
              規劃 25° 與 50° 雙坡度草皮攀岩攀繩區，考驗四肢攀登肌耐力；長達 74 公尺的高架無障礙景觀緩坡步道，可居高臨下俯瞰心型大草坪。
            </p>
          </div>
          <div class="deck-res-box">
            <div class="deck-res-row">
              <span class="deck-res-label">順遊：</span>
              <span style="color:#cbd5e1;">南投縣農產運銷園區（南投豬事文化園區）</span>
            </div>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/mingjian_1.jpg" alt="名間親子生態公園">
          <div style="font-size:12px; color:var(--cf-text-dim); margin-top:6px; text-align:center;">
            名間親子生態園區五米巨型彩虹滑梯與共融攀爬草坡
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 07: 野營教學 ① 帳篷搭設六部曲 -->
  <section class="slide" id="slide-tent-setup">
    <p class="s-eyebrow">CAMPING SKILLS · 專題教學 ①</p>
    <h2 class="s-title">野營常識 · 蒙古包帳篷標準搭設六部曲</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <div class="card-slide">
              <h4 style="font-size:13px;">1. 選地整平</h4>
              <p style="font-size:11.5px; color:var(--cf-text-dim);">挑平坦處清除碎石硬枝，避開低窪積水與樹下蜂窩枯枝。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:13px;">2. 鋪設地布</h4>
              <p style="font-size:11.5px; color:var(--cf-text-dim);">防水地布不可露出外帳底緣，四周多餘向內摺入防雨水滲漏。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:13px;">3. 交叉穿柱</h4>
              <p style="font-size:11.5px; color:var(--cf-text-dim);">兩長營柱沿對角線交叉穿入內帳通管，務必以<b>「推」</b>代拉防脫節。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:13px;">4. 撐起立帳</h4>
              <p style="font-size:11.5px; color:var(--cf-text-dim);">兩人對角同時將營柱頂彎拱起，插進插銷，扣上內帳塑料掛勾。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:13px;">5. 披上外帳</h4>
              <p style="font-size:11.5px; color:var(--cf-text-dim);">對準進出口覆蓋，綁緊內部魔鬼氈，四角插扣拉緊調平。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:13px;">6. 打釘拉線</h4>
              <p style="font-size:11.5px; color:var(--cf-text-dim);">營釘以 45°～60° 斜背營繩敲入地面，拉開前庭使內外帳分離通風。</p>
            </div>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/tent_setup.jpg" alt="帳篷搭設教學">
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">搭帳黃金口訣</span>
            <div class="tip-body"><b>一選平地二鋪布、三推營柱四拱起、五披外帳六拉線</b>！確保內外帳分開不反潮。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 08: 野營教學 ② 拆帳與無痕山林 -->
  <section class="slide" id="slide-lnt">
    <p class="s-eyebrow">CAMPING SKILLS · 專題教學 ②</p>
    <h2 class="s-title">拆帳收整要訣 ＆ 無痕山林 (LNT) 守則</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>⛺ 快速拆帳四大順序</h4>
            <ul style="font-size:12.5px; line-height:1.5; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>清空內帳</b>：徹底檢查遺落物，門窗拉鍊留一拳透氣縫排出空氣。</li>
              <li><b>拔釘解繩</b>：依序拔除營釘收繩，外帳甩落露水與泥沙對折平鋪。</li>
              <li><b>推退營柱</b>：拔下四角插銷，將營柱推移抽出，由中央對折向兩側收納。</li>
              <li><b>捲收裝袋</b>：內外帳平整對折成收納袋等寬，緊密滾捲擠出空氣，收納整齊。</li>
            </ul>
          </div>
          <div class="tip warn">
            <span class="tip-tag">晨檢評分重點</span>
            <div class="tip-body">睡袋摺疊方正、帳內無雜物垃圾、營釘營柱配件點齊，納入生活競賽重大計分！</div>
          </div>
        </div>
        <div>
          <div class="card-slide">
            <h4>🌿 無痕山林 (Leave No Trace) 七大原則</h4>
            <div style="font-size:12px; line-height:1.5; color:var(--cf-text-dim);">
              1. <b>事前充分準備</b>：裝備齊全、遵守作息。<br>
              2. <b>在堅實地面活動</b>：不隨意踩踏踐踏植被草皮。<br>
              3. <b>妥善處理垃圾廢棄物</b>：落實垃圾分類，廚餘入桶不傾倒水槽。<br>
              4. <b>保持環境原有風貌</b>：不攀折花木，欣賞而不破壞。<br>
              5. <b>減低用火影響</b>：限指定野炊區用火，確實熄火清理木炭灰燼。<br>
              6. <b>尊重野生動物</b>：遠距觀察不餵食追打。<br>
              7. <b>考量其他營地夥伴</b>：22:30後維持營區安寧。
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 09: 童軍技能 ① 生火技巧與野炊控火 -->
  <section class="slide" id="slide-scout-fire">
    <p class="s-eyebrow">SCOUT SKILLS · 專題教學 ③</p>
    <h2 class="s-title">童軍技能 · 生火技巧、柴火分類與野炊煮飯</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4 class="orange">🔥 火媒棒製作與三級柴火</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>火媒棒</b>：小刀 45° 削出薄羽狀木屑，增加接觸氧氣面積。<br>
              <b>引火柴</b>：乾燥枯松針、火種、細枯草，一星即燃。<br>
              <b>助燃柴</b>：牙籤至小指粗之乾燥小枝條，迅速擴大火勢。<br>
              <b>燃燒柴</b>：手腕粗大木塊與耐燒木炭，提供穩定持久核心熱源。
            </p>
          </div>
          <div class="card-slide">
            <h4 class="orange">🍚 野炊煮出香Ｑ白飯四步驟</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>比例</b>：米洗淨浸泡20分，米與水黃金比例 <b>1 : 1.1～1.2</b>。<br>
              <b>大火煮滾</b>：井字柴架大火燒至鍋邊大量冒出白煙水氣。<br>
              <b>中火收乾</b>：轉中火煮約5分鐘，至鍋內水分吸收散發飯香。<br>
              <b>微火悶飯</b>：移至火堆旁微火燜煨，最後【離火加蓋悶15分鐘】！
            </p>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/cooking.jpg" alt="野炊烹調">
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">野炊幹部守則</span>
            <div class="tip-body"><b>大廚掌勺、二廚切配、伙夫控火、水夫洗滌、事務清點</b>，全員合作煮出冠軍美饌！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 10: 童軍技能 ② 戰術偽裝與方向辨識 -->
  <section class="slide" id="slide-scout-camo">
    <p class="s-eyebrow">SCOUT SKILLS · 專題教學 ④</p>
    <h2 class="s-title">童軍技能 · 戰術偽裝原則與自然方向辨識</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🪖 面部迷彩「凸暗凹亮」戰術原則</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>凸處塗暗</b>：額頭、鼻樑、顴骨、下巴等容易反射光線部位塗深綠/黑色。<br>
              <b>凹處塗亮</b>：眼窩、人中、法令紋、頸下陰影處塗淺草綠色。<br>
              <b>打破輪廓</b>：以斜線、斑紋塗抹，破壞人臉原有對稱特徵，融於草叢環境。
            </p>
          </div>
          <div class="card-slide">
            <h4>🧭 實用定向四大絕技</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>指北針定向</b>：紅色磁針恆指北方（N），轉動刻度盤使紅標重合。<br>
              <b>手錶指針太陽法</b>：時針指向太陽，時針與表面 12 點角平分線為【南方】。<br>
              <b>北極星法</b>：北斗七星勺口天璇、天樞連線延伸 5 倍即為正北極星。<br>
              <b>年輪與植被</b>：樹木南面枝繁葉茂，年輪南疏北密；北側樹皮易生青苔。
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="height:100%; display:flex; flex-direction:column; justify-content:center;">
            <h4 style="font-size:15px; margin-bottom:12px;">🌟 戰術偽裝定向實例示意</h4>
            <div style="background:rgba(0,0,0,0.3); border:1px solid var(--cf-rule); border-radius:8px; padding:12px; font-size:12px; line-height:1.6; color:#cbd5e1;">
              <b style="color:var(--cf-accent);">實作演練情境：</b><br>
              全體同學將於尖山埤森林步道實施戰術偽裝演練，以小隊為單位運用指北針尋找藏匿目標點。
              <div style="margin-top:10px; border-top:1px dashed var(--cf-rule); padding-top:8px;">
                💡 <b>教官評分</b>：偽裝細緻度、團隊行進隱蔽性、定向坐標判讀精準度。
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 11: 童軍技能 ③ 實用八大繩結 -->
  <section class="slide" id="slide-scout-knots">
    <p class="s-eyebrow">SCOUT SKILLS · 專題教學 ⑤</p>
    <h2 class="s-title">童軍技能 · 出神入化！實用八大繩結圖解</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <thead><tr><th>繩結名稱</th><th>核心用途</th><th>打法特點與應用場合</th></tr></thead>
            <tbody>
              <tr><td><strong>單結</strong> (Overhand)</td><td>防脫結</td><td>最基礎繩結，打於繩尾防止滑出孔環</td></tr>
              <tr><td><strong>平結</strong> (Reef Knot)</td><td>接繩 (同粗)</td><td>左壓右右壓左，兩條等粗繩相接，易解好用</td></tr>
              <tr><td><strong>接繩結</strong> (Sheet Bend)</td><td>接繩 (不同粗)</td><td>粗繩成圈細繩穿繞，連接粗細不同繩索</td></tr>
              <tr><td><strong>雙半結</strong> (Two Half Hitches)</td><td>固著於物</td><td>固定繩於樹幹柱子，越拉越緊不易脫落</td></tr>
              <tr><td><strong>營繩結</strong> (Taut-line)</td><td>調節張力</td><td>可上下滑動調整鬆緊，帳篷拉水線必學</td></tr>
              <tr><td><strong>稱人結</strong> (Bowline)</td><td>繩結之王</td><td>繩圈受力不緊縮，高空垂降、救生吊掛</td></tr>
              <tr><td><strong>雙套結</strong> (Clove Hitch)</td><td>工程起頭結</td><td>繞桿兩圈交叉，搭建先鋒工程旗桿起手式</td></tr>
              <tr><td><strong>十字結</strong> (Square Lashing)</td><td>木桿十字綁紮</td><td>兩垂直木桿緊密交叉捆紮，營門搭建</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <img class="img-slide" src="assets/img/rope_knots.jpg" alt="童軍繩結">
          <div class="tip" style="margin-top:6px;">
            <span class="tip-tag">練習口訣</span>
            <div class="tip-body"><b>平結接等粗、接繩接異徑；繩結之王稱人結、營繩鬆緊靠齊來</b>！童軍繩隨身帶隨手練。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 12: 童軍技能 ④ 臺灣六大毒蛇辨識 -->
  <section class="slide" id="slide-snakes-id">
    <p class="s-eyebrow">OUTDOOR SAFETY · 專題教學 ⑥</p>
    <h2 class="s-title">野外安全 · 臺灣六大毒蛇特徵與習性辨識</h2>
    <div class="s-body">
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
        <div class="card-slide">
          <h4 style="color:#ef4444; font-size:13.5px;">雨傘節 (神經毒)</h4>
          <p style="font-size:11.5px; line-height:1.45; color:var(--cf-text-dim);">
            <b>外觀</b>：黑白相間等寬條紋，背脊微隆起。<br>
            <b>特點</b>：性溫馴夜行，咬傷無劇痛腫脹，但數小時內會引發呼吸衰竭致死！
          </p>
        </div>
        <div class="card-slide">
          <h4 style="color:#ef4444; font-size:13.5px;">眼鏡蛇 (神經/細胞毒)</h4>
          <p style="font-size:11.5px; line-height:1.45; color:var(--cf-text-dim);">
            <b>外觀</b>：全身黑褐，受威脅頸部擴張如飯匙狀。<br>
            <b>特點</b>：發出嘶嘶警告聲，毒牙深，咬傷局部組織迅速劇烈腫脹壞死。
          </p>
        </div>
        <div class="card-slide">
          <h4 style="color:#f59e0b; font-size:13.5px;">龜殼花 (出血毒)</h4>
          <p style="font-size:11.5px; line-height:1.45; color:var(--cf-text-dim);">
            <b>外觀</b>：烙鐵三角形頭，背部暗褐色龜殼斑紋。<br>
            <b>特點</b>：夜行於落葉堆，出血毒性強烈，傷口血流不止、起大血泡。
          </p>
        </div>
        <div class="card-slide">
          <h4 style="color:#f59e0b; font-size:13.5px;">赤尾青竹絲 (出血毒)</h4>
          <p style="font-size:11.5px; line-height:1.45; color:var(--cf-text-dim);">
            <b>外觀</b>：翠綠體色、尾端焦紅、兩側白縱線。<br>
            <b>特點</b>：常棲於樹枝灌木，保護色極佳，台灣咬人案例最多但致死率較低。
          </p>
        </div>
        <div class="card-slide">
          <h4 style="color:#f59e0b; font-size:13.5px;">百步蛇 (出血毒)</h4>
          <p style="font-size:11.5px; line-height:1.45; color:var(--cf-text-dim);">
            <b>外觀</b>：頭大吻端向上翹，體側黑褐三角形斑。<br>
            <b>特點</b>：台灣最大毒蛇，毒液排毒量驚人，皮下嚴重出血壞死。
          </p>
        </div>
        <div class="card-slide">
          <h4 style="color:#8b5cf6; font-size:13.5px;">鎖鏈蛇 (混合毒)</h4>
          <p style="font-size:11.5px; line-height:1.45; color:var(--cf-text-dim);">
            <b>外觀</b>：背部三列深褐色橢圓形鎖鏈狀斑。<br>
            <b>特點</b>：盤捲發出劇烈噴氣，兼具神經麻痺與溶血症狀，危險性極高。
          </p>
        </div>
      </div>
      <div class="tip" style="margin-top:8px;">
        <span class="tip-tag">防蛇鐵則</span>
        <div class="tip-body">戶外野外行進落實<b>「打草驚蛇」</b>；穿著長褲布鞋、夜間攜帶手電筒照明，切勿徒手翻動草叢與石塊！</div>
      </div>
    </div>
  </section>

  <!-- Slide 13: 毒蛇急救五要五不 -->
  <section class="slide" id="slide-snakes-firstaid">
    <p class="s-eyebrow">FIRST AID · 專題教學 ⑦</p>
    <h2 class="s-title">毒蛇咬傷黃金自救處置 ·【五要五不】原則</h2>
    <div class="s-body">
      <div class="cols c2">
        <div class="card-slide" style="border-left:4px solid #22c55e;">
          <h4 style="color:#4ade80; font-size:15px;">✅ 毒蛇咬傷【五要】原則</h4>
          <ul style="font-size:12.5px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
            <li><b>要視為毒蛇</b>：凡遭蛇咬傷，第一時間皆依毒蛇標準處置。</li>
            <li><b>要保持冷靜</b>：安撫傷者靜坐或平躺，避免跑步加速血液毒液循環。</li>
            <li><b>要脫除束縛物</b>：迅速取下傷肢之戒指、手錶、手鐲，防止肢體腫脹後缺血壞死。</li>
            <li><b>要彈性包紮</b>：以彈性繃帶寬鬆包紮（可插一指鬆緊），傷肢固定於<b>低於心臟</b>位置。</li>
            <li><b>要迅速就醫</b>：記清或拍下蛇類外貌特徵，火速送醫施打對應抗蛇毒血清。</li>
          </ul>
        </div>
        <div class="card-slide" style="border-left:4px solid #ef4444;">
          <h4 style="color:#f87171; font-size:15px;">❌ 毒蛇咬傷【五不】禁忌</h4>
          <ul style="font-size:12.5px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
            <li><b>不要切開傷口</b>：切開會損傷肌腱血管，極易造成大量出血與細菌二次感染。</li>
            <li><b>不要用嘴吸吮</b>：口腔微創黏膜會吸收蛇毒，導致施救者同樣中毒！</li>
            <li><b>不要冰敷患處</b>：冰敷會使血管極端痙攣收縮，加劇局部組織缺血壞疽。</li>
            <li><b>不要緊勒止血帶</b>：過度勒緊阻斷動脈血流，極易引發缺血截肢災難！</li>
            <li><b>不要飲用刺激品</b>：嚴禁飲用酒類、濃茶或咖啡，避免刺激心率擴散毒素。</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 14: 童軍技能 ⑤ 營火晚會與動唱 -->
  <section class="slide" id="slide-scout-campfire">
    <p class="s-eyebrow">SCOUT SKILLS · 專題教學 ⑧</p>
    <h2 class="s-title">童軍技能 · 營火晚會儀式、歡呼與音樂律動</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4 class="orange">🔥 營火晚會三部曲</h4>
            <p style="font-size:12.5px; color:var(--cf-text-dim); line-height:1.5;">
              <b>神聖迎火</b>：火神引火入場、全場靜肅，齊誦神聖拜火詞。<br>
              <b>歡狂動唱</b>：班級創意節目競賽、隊輔狂熱動唱、嗨翻星空！<br>
              <b>薪火相傳</b>：營火轉為燭光，圍繞火堆與導師分享成長印記。
            </p>
          </div>
          <div class="card-slide">
            <h4 class="orange">🗣️ 經典神聖拜火詞</h4>
            <p style="font-size:13px; color:#fde047; font-weight:700; line-height:1.5;">
              「阿給拉～魯巴～魯巴！偉大的火神，請賜予南投國中光明、勇氣與榮耀！熊熊營火，燃燒吧！」
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide">
            <h4>🎵 經典營火歡唱曲目</h4>
            <ul style="font-size:12px; line-height:1.5; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>《營火歌》</b>：朋友！燃起這營火，照耀著我們的友誼...火花在黑夜裡飛舞...</li>
              <li><b>《成吉思汗》</b>：風沙滾滾，戰馬奔馳，嘿！喝！嘿！喝！無敵南投健兒！</li>
              <li><b>《第一支舞》</b>：帶著笑容，你走向我，做個邀請的動作...難忘的夜晚...</li>
              <li><b>《萍聚》</b>：只要我們曾經擁有過，對你我來講已經足夠...</li>
            </ul>
          </div>
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">精神象徵</span>
            <div class="tip-body">營火燃燒的是青春的熱血，燭光映照的是師生真誠的心聲。盡情吶喊、用心感受！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 15: 山訓探索 ① 高空垂降 -->
  <section class="slide" id="slide-rappel-guide">
    <p class="s-eyebrow">MOUNTAIN TRAINING · 專題教學 ⑨</p>
    <h2 class="s-title">山訓探索 · 膽量大考驗！進擊の高空垂直垂降</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🧗 核心安全裝備</h4>
            <p style="font-size:12.5px; color:var(--cf-text-dim); line-height:1.5;">
              UIAA認證岩盔、全身/坐式安全吊帶（貼合一指寬）、雙向自動大D主鎖、八字環下降器、耐磨防護手套。由教官與夥伴實施雙重檢查（Buddy Check）。
            </p>
          </div>
          <div class="card-slide">
            <h4>🦵 站姿與重心四部曲</h4>
            <ul style="font-size:12px; line-height:1.45; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>雙腳微開</b>：雙腳打開與肩同寬，腳底平實踩踏塔台岩壁邊緣。</li>
              <li><b>大膽後傾</b>：身體勇敢向後傾斜 45°～60°，背部與壁面垂直，重心下沉於腳底。</li>
              <li><b>雙手分工</b>：上方導繩手（左手）輕握繩索不出力；下方制動手（右手）置於右後臀。</li>
              <li><b>制動煞停</b>：【右手往前繩鬆即下滑、右手貼臀扣緊即煞停】！</li>
            </ul>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/rappel.jpg" alt="高空垂降">
          <div class="tip warn" style="margin-top:8px;">
            <span class="tip-tag">心理突破</span>
            <div class="tip-body">恐懼來自未知，相信專業裝備與確保系統！深呼吸跨出第一步，你就是最勇敢的戰士！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 16: 山訓探索 ② 解手結與團隊跳繩 -->
  <section class="slide" id="slide-puzzle-guide">
    <p class="s-eyebrow">PA ADVENTURE · 專題教學 ⑩</p>
    <h2 class="s-title">探索教育 · 解手結謎題 ＆ 團隊跳繩心跳同步</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🤝 PA探索遊戲：解手結 (Human Knot)</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>規則</b>：全班圍圈向前伸手，隨機握住不同同學的左右手（不握鄰居、同一人不重複）。在<b>雙手不鬆開</b>前提下，跨步鑽爬解成一個大圓圈。<br>
              <b>核心價值</b>：考驗團隊傾聽、溝通協調、冷靜決策與肢體柔韌信任感。
            </p>
          </div>
          <div class="card-slide">
            <h4>🪢 團隊跳繩 (Team Jump Rope)</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>甩繩要領</b>：兩位甩繩手節奏穩定大弧度擺盪，大繩擊地發出清脆「啪」聲。<br>
              <b>全員同步</b>：進場踩準大繩反彈瞬間，全班齊呼口號「一、二、跳！」，呼吸步伐完全一致。
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="height:100%; display:flex; flex-direction:column; justify-content:center;">
            <h4 style="font-size:15px; margin-bottom:10px;">🏆 團隊突破三大心法</h4>
            <div style="background:rgba(0,0,0,0.3); border:1px solid var(--cf-rule); border-radius:8px; padding:12px; font-size:12.5px; line-height:1.6; color:#cbd5e1;">
              1. <b>不抱怨、不責怪</b>：失敗是累積默契的必經之路。<br>
              2. <b>專注指揮核心</b>：一人發號施令，全員專注配合執行。<br>
              3. <b>團結就是力量</b>：個人的堅持成就班級集體的最高榮譽！
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 17: 山訓探索 ③ 攀岩絕技 -->
  <section class="slide" id="slide-rock-guide">
    <p class="s-eyebrow">MOUNTAIN TRAINING · 專題教學 ⑪</p>
    <h2 class="s-title">山訓探索 · 超級蜘蛛人～人工岩場攀登絕技</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🕷️ 攀岩三大黃金法則</h4>
            <ul style="font-size:12.5px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>三點不動一點動</b>：保持三點支撐三角形，一次僅移動一肢，維持平衡重心。</li>
              <li><b>重量在腳不在手</b>：人體腿肌比臂肌大三倍！手臂主要放鬆貼壁導向，發力全靠雙腳蹬起！</li>
              <li><b>重心貼近岩壁</b>：肚臍核心貼壁，避免「屁股外凸」，大幅減輕手臂抓握負擔。</li>
            </ul>
          </div>
          <div class="card-slide">
            <h4>🔔 頂峰敲鈴與安全下降</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              登頂後伸手擊打頂峰鈴鐺！下降時雙手抓緊胸前主繩，雙腳自然張開大字型輕觸岩壁，由地面確保教官平穩緩慢放繩至地面。
            </p>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/jianshanpi_3.jpg" alt="戶外活動">
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">攀岩技巧</span>
            <div class="tip-body">攀登前先在岩壁下方<b>「讀線」</b>，用眼睛找出最佳抓握點與踩腳點，有條不紊步步高升！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 18: 山訓探索 ④ 水彈生存遊戲 -->
  <section class="slide" id="slide-water-guide">
    <p class="s-eyebrow">TACTICAL GAME · 專題教學 ⑫</p>
    <h2 class="s-title">山訓探索 · 水彈生存競技 ＆ 小隊戰術防守</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4 style="color:#ef4444;">🛡️ 絕對安全第一鐵律</h4>
            <p style="font-size:12.5px; color:#fca5a5; font-weight:700; line-height:1.5;">
              從進入對抗場地到哨音結束前，【嚴禁私自脫除全罩式護目面罩】！即使護目鏡起霧亦不可摘下，違者立即判出場。
            </p>
          </div>
          <div class="card-slide">
            <h4>🎯 小隊戰術攻防佈陣</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>前鋒突擊組</b>：善用掩體靈活推進、包抄側翼奪取旗幟。<br>
              <b>火力壓制組</b>：中距離連續點射，壓制敵方火力掩護隊友轉移。<br>
              <b>後方防守組</b>：據守核心陣地，防範敵方突襲。
            </p>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/water_gun.jpg" alt="水彈生存遊戲">
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">運動家風度</span>
            <div class="tip-body">中彈者自覺高舉雙手喊「陣亡」退入安全區，展現誠信榮譽；安全交戰距離內不貼臉射擊。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 19: 山訓探索 ⑤ 獨木橋平衡挑戰 -->
  <section class="slide" id="slide-log-guide">
    <p class="s-eyebrow">BALANCE CHALLENGE · 專題教學 ⑬</p>
    <h2 class="s-title">山訓探索 · 獨木橋橫渡平衡挑戰與恐懼克服</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🪵 平衡三要點</h4>
            <ul style="font-size:12.5px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>重心壓低</b>：雙膝微彎吸收晃動，重心沉於腹部下丹田。</li>
              <li><b>雙臂平展</b>：雙手水平張開如天平兩側，隨時微調平衡。</li>
              <li><b>視線向前</b>：雙眼鎖定前方橋頭終點，<b>切忌低頭看腳底或深淵</b>！</li>
            </ul>
          </div>
          <div class="card-slide">
            <h4>🧘 心理突破技巧</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              踏上獨木橋前做三次深呼吸，一步一吸吐氣，維持均勻節奏向前滑步，讓身心合一戰勝動搖恐懼！
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="height:100%; display:flex; flex-direction:column; justify-content:center;">
            <h4 style="font-size:15px; margin-bottom:10px;">🌟 山訓總結精神</h4>
            <div style="background:rgba(0,0,0,0.3); border:1px solid var(--cf-rule); border-radius:8px; padding:12px; font-size:12.5px; line-height:1.6; color:#cbd5e1;">
              高空垂降練<b>「膽識」</b>、<br>
              解手結探索練<b>「默契」</b>、<br>
              人工攀岩練<b>「毅力」</b>、<br>
              水彈生存練<b>「協同」</b>、<br>
              獨木橋橫渡練<b>「定力」</b>！<br>
              五大挑戰全面淬鍊，成為頂天立地的南投國中青年！
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 20: 行前行李打包清單 -->
  <section class="slide" id="slide-checklist">
    <p class="s-eyebrow">PACKING LIST</p>
    <h2 class="s-title">行前必備 · 行李裝備打包與防護清單</h2>
    <div class="s-body">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
        <div class="card-slide">
          <h4>🪪 證件與個人隨身</h4>
          <ul style="font-size:12px; line-height:1.5; color:var(--cf-text-dim); padding-left:16px;">
            <li><b>健保卡 (必帶！)</b>、家長聯絡卡</li>
            <li>零用錢約 200~300 元 (活動無需大額花費)</li>
            <li>隨身輕便小背包 (攜帶水壺面紙雨衣)</li>
            <li>衛生紙、濕紙巾</li>
          </ul>
        </div>
        <div class="card-slide">
          <h4>👕 服裝與保暖鞋襪</h4>
          <ul style="font-size:12px; line-height:1.5; color:var(--cf-text-dim); padding-left:16px;">
            <li>換洗衣物 1～2 套 (吸汗排汗材質為佳)</li>
            <li>運動長褲 (山訓防刮，嚴禁裙子拖鞋)</li>
            <li>耐磨運動球鞋 ＆ 運動厚襪兩雙</li>
            <li>防風薄外套 (早晚溫差大)、遮陽帽、輕便雨衣</li>
          </ul>
        </div>
        <div class="card-slide">
          <h4>🧼 盥洗與生活保健</h4>
          <ul style="font-size:12px; line-height:1.5; color:var(--cf-text-dim); padding-left:16px;">
            <li>毛巾、自備牙刷牙膏梳子 (響應環保)</li>
            <li>個人水壺 / 保溫杯 (隨時補充水分)</li>
            <li>防蚊液、暈車藥、個人常備過敏用藥</li>
            <li>小型手電筒 / 頭燈、髒衣物防潮塑膠袋</li>
          </ul>
        </div>
        <div class="card-slide">
          <h4>⚜️ 童軍與活動專用</h4>
          <ul style="font-size:12px; line-height:1.5; color:var(--cf-text-dim); padding-left:16px;">
            <li>童軍繩 (童軍結實習必備)</li>
            <li>個人環保餐具組 (碗筷湯匙，野炊烤肉用)</li>
            <li>手寫筆記本與原子筆</li>
            <li>無比的熱忱與團隊榮譽心！</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 21: 營規與生活公約 -->
  <section class="slide" id="slide-rules">
    <p class="s-eyebrow">CAMP REGULATIONS</p>
    <h2 class="s-title">營地公約 · 生活常規與緊急聯絡應變網</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>📋 營區六大生活紀律</h4>
            <ul style="font-size:12px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>聽從指揮</b>：全員服從導師、值星官指令，按作息集合，不遲到脫隊。</li>
              <li><b>安全第一</b>：營內嚴禁追逐奔跑、嚴禁擅近深水水域。</li>
              <li><b>用火鐵律</b>：帳篷內嚴禁使用火源！野炊專人看管，完畢徹底熄火。</li>
              <li><b>夜間就寢</b>：22:30後熄燈保持肅靜，嚴禁擅離分配帳篷。</li>
              <li><b>競賽風度</b>：各項競賽計入精神總錦標，展現勝不驕敗不餒風範。</li>
            </ul>
          </div>
        </div>
        <div>
          <div class="card-slide">
            <h4>🚑 緊急聯絡與通報管道</h4>
            <div style="font-size:12px; line-height:1.6; color:var(--cf-text-dim);">
              遇身體不適、意外撞傷、發燒或蜂蛇咬傷，第一時間通報：<br>
              1. <b>同帳室長 / 野炊小隊長</b><br>
              2. <b>各班隨隊導師</b>（黃O月、黃O君、林O玟、李O儒、林O銓、許O玉、黃O慧）<br>
              3. <b>隨隊學務處行政團隊</b>：劉O彥校長、董O遠主任、姚O勤組長<br>
              4. <b>營地醫護站與值星教官</b><br>
              營地專車隨時待命，直通柳營奇美醫院急診照護！
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 22: 帳篷住宿分配總表 -->
  <section class="slide" id="slide-tents">
    <p class="s-eyebrow">TENT ALLOCATION (MASKED)</p>
    <h2 class="s-title">帳篷住宿分配總表 · 全校 27 頂帳篷（去個資版）</h2>
    <div class="s-body">
      <div style="max-height:480px; overflow-y:auto; padding-right:6px;">
        <table class="table-deck">
          <thead><tr><th>班級</th><th>性別</th><th>帳別</th><th>室長</th><th>人數</th><th>同帳成員名單 (座號+姓名)</th></tr></thead>
          <tbody>
"""

for t in tents:
    html += f"            <tr><td><strong>{t['class']}</strong></td><td>{t['gender']}</td><td>{t['tentName']}</td><td>{t['leaderSeat']}號 {t['leaderName']}</td><td>{t['count']}</td><td>{t['members']}</td></tr>\n"

html += f"""          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- Slide 23: 野炊小隊編組總表 -->
  <section class="slide" id="slide-squads">
    <p class="s-eyebrow">SQUAD ROSTER (MASKED)</p>
    <h2 class="s-title">野炊烤肉活動小隊編組總表 · 15 個小隊（去個資版）</h2>
    <div class="s-body">
      <div style="max-height:480px; overflow-y:auto; padding-right:6px;">
        <table class="table-deck">
          <thead><tr><th>班級</th><th>小隊</th><th>人數</th><th>隊長</th><th>副隊</th><th>大廚</th><th>二廚</th><th>伙夫</th><th>水夫</th><th>事務</th><th>隊員</th></tr></thead>
          <tbody>
"""

for s in squads:
    html += f"            <tr><td><strong>{s['class']}</strong></td><td>{s['squadName']}</td><td>{s['count']}</td><td>{s['leader']}</td><td>{s['deputy']}</td><td>{s['chef1']}</td><td>{s['chef2']}</td><td>{s['fire']}</td><td>{s['water']}</td><td>{s['affairs']}</td><td>{s['members']}</td></tr>\n"

html += f"""          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- Slide 24: 封底 -->
  <section class="slide slide-cover" id="slide-backcover">
    <p class="s-eyebrow">南投縣立南投國民中學 · 二年級隔宿露營</p>
    <h1 class="s-title-xl" style="font-size: 46px; line-height: 1.3;">齊心同舟 · 突破自我<br><span style="font-size:32px; color:var(--cf-accent);">預祝全體師生露營圓滿順利、平安滿載！</span></h1>
    <p class="s-sub" style="font-size: 19px; margin-top: 14px;">
      熱情揮灑青春 · 烙印成長足跡 ｜ 點燃營火熱力 · 譜出青春無敵樂章
    </p>
    <div style="margin-top: 20px;">
      <a href="app.html" class="tag-badge" style="font-size:16px; padding:6px 16px; text-decoration:none;">📱 開啟行動手冊網頁版 (RWD 查詢系統)</a>
    </div>
  </section>

</main>

<!-- 目錄彈出視窗 -->
<div class="toc-modal" id="toc-modal">
  <div class="toc-inner">
    <div class="toc-header">
      <h3 class="toc-title">簡報章節目錄總覽</h3>
      <button class="toc-close" id="toc-close" type="button">✕</button>
    </div>
    <div class="toc-list" id="toc-list"></div>
  </div>
</div>

<script src="lesson-deck.js?v=202610190200"></script>
</body>
</html>
"""

with open('slides.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved slides.html successfully!")

# -*- coding: utf-8 -*-
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

with open('camp_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

info = data['info']
classes = data['classes']
buses = data['buses']
students = data['students']
tents = data['tents']
squads = data['squads']
itinerary = data['itinerary']
checklist = data['checklist']
rules = data['rules']
scoutKnowledge = data['scoutKnowledge']

html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>南投國中 115學年度二年級隔宿露營 專屬行動簡報手冊（去個資版）</title>
<meta name="description" content="南投縣立南投國民中學 115學年度二年級戶外教育隔宿露營 網頁式簡報手冊。全台南尖山埤兩天一夜山訓探索、野營炊事、童軍技能教學參考，全校27頂帳篷與15個野炊小隊去個資速查。">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500;700&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="deck.css?v=20261019_v1">
<style>
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
    font-size: 12.5px;
    margin-top: 5px;
  }}
  .table-deck th {{
    background: rgba(255, 255, 255, 0.08);
    color: var(--cf-text);
    padding: 5px 8px;
    border: 1px solid var(--cf-rule);
    text-align: left;
    font-weight: 700;
  }}
  .table-deck td {{
    padding: 4px 8px;
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
    gap: 14px;
  }}
  .grid-deck-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
  }}
  .card-slide {{
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--cf-rule);
    border-radius: 8px;
    padding: 10px 12px;
  }}
  .card-slide h4 {{
    font-size: 14px;
    color: var(--cf-accent);
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .card-slide h4.orange {{
    color: var(--fire-orange);
  }}
  .img-slide {{
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--cf-rule);
  }}
  .deck-res-box {{
    margin-top: 6px;
    background: rgba(0, 0, 0, 0.28);
    border: 1px solid var(--cf-rule);
    border-radius: 6px;
    padding: 5px 8px;
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
  }}
  .deck-res-chip.map {{
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border-color: rgba(34, 197, 94, 0.35);
  }}
  .deck-res-chip.video {{
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border-color: rgba(239, 68, 68, 0.35);
  }}
</style>
</head>
<body class="deck" data-mode="present">
<header class="deck-bar">
  <span class="deck-id">南投國中 115 隔宿露營</span>
  <span class="deck-name">二年級隔宿露營行動簡報手冊（去個資版）</span>
  <div class="deck-tools">
    <!-- 6 色淡色系背景切換 -->
    <div class="theme-picker" title="切換簡報底色">
      <span style="font-size:11px; font-weight:700; color:var(--cf-text-dim); margin-right:2px;">🎨 底色：</span>
      <button type="button" class="theme-chip" data-set-theme="green" title="淡綠色">淡綠</button>
      <button type="button" class="theme-chip" data-set-theme="purple" title="淡紫色">淡紫</button>
      <button type="button" class="theme-chip" data-set-theme="red" title="淡紅色">淡紅</button>
      <button type="button" class="theme-chip" data-set-theme="blue" title="淡藍色">淡藍</button>
      <button type="button" class="theme-chip" data-set-theme="gray" title="淺灰色">淺灰</button>
      <button type="button" class="theme-chip" data-set-theme="orange" title="淺橙色">淺橙</button>
    </div>

    <!-- 上一頁 / 下一頁切換鍵 -->
    <button class="deck-btn nav-btn-primary" id="nav-prev-top" type="button" title="上一頁 (←)">◀ 上一頁</button>
    <button class="deck-btn nav-btn-primary" id="nav-next-top" type="button" title="下一頁 (→)">下一頁 ▶</button>
    <button class="deck-btn" id="toc-btn" type="button" title="目錄總覽 (T)">📑 目錄總覽</button>
    <button class="deck-btn is-on" id="mode-btn" type="button">📖 閱讀模式</button>
    <button class="deck-btn" id="fs-btn" type="button">⛶ 全螢幕</button>
    <a href="index.html" class="deck-btn" style="text-decoration:none; color:var(--cf-accent); border-color:var(--cf-accent); font-weight:700;">📱 手冊網頁版</a>
    <span class="deck-count" id="deck-count"></span>
  </div>
</header>
<main class="deck-stage" id="deck-stage">

  <!-- Slide 01: 封面 -->
  <section class="slide slide-cover" id="slide-01">
    <p class="s-eyebrow">南投縣立南投國民中學 · 115 學年度 · 二年級戶外教育活動</p>
    <h1 class="s-title-xl" style="font-size: 44px; line-height: 1.25;">隔宿露營 行動簡報手冊<br><span style="font-size:30px; color:var(--cf-accent);">尖山埤山訓探索 · 野營炊事 · 團結成長之旅（去個資版）</span></h1>
    <p class="s-sub" style="font-size: 17px; margin-top: 14px;">
      活動規劃：兩天一夜（115年10月27日 ～ 10月28日） ｜ 營訓基地：台南-尖山埤露營區（06-6233888）<br>
      隨隊長官：劉O彥 校長、董O遠 學務主任、姚O勤 訓育組長 暨 二年級全體導師（801～807班）
    </p>
    <div style="margin-top: 16px; display: flex; gap: 10px; justify-content: center;">
      <span class="tag-badge">⛺ 全校 27 頂帳篷 (A01~A13 / B01~B14)</span>
      <span class="tag-badge orange">🍳 15 個野炊小隊 (第1組~第15組)</span>
      <span class="tag-badge blue">👥 107 位學生（男48 / 女59）</span>
    </div>
  </section>

  <!-- Slide 02: 實施計畫與基地概況 -->
  <section class="slide" id="slide-02">
    <p class="s-eyebrow">PLAN & LOCATION · 官方實施計畫</p>
    <h2 class="s-title">實施計畫與活動基地 · 台南尖山埤露營區</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <tbody>
              <tr><th style="width:90px;">活動主旨</th><td>自立自強、主動敏捷、互助合作，於「做中學、學中做」熟練各項童軍野外求生技能。</td></tr>
              <tr><th>活動時間</th><td><strong>115年10月27日 (二) 至 10月28日 (三)</strong>，兩天一夜。</td></tr>
              <tr><th>起訖時間</th><td>10/27 (二) 07:30 校園集合（921地震公園逃生演練），08:00 準時出發；10/28 (三) 16:20 返抵學校。</td></tr>
              <tr><th>參加對象</th><td>二年級全體師生，學生 107 人、隨隊師長，共計 117 人。</td></tr>
              <tr><th>承辦單位</th><td>中國青年旅行社中部分公司 ｜ 團控經理：邱O凱 (0972-721756)。</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🏕️ 台南柳營尖山埤露營區（台糖尖山埤渡假村）</h4>
            <div style="font-size:12px; color:var(--cf-text-dim);">
              電話：(06) 623-3888 ｜ 地址：台南市柳營區旭山里 60 號<br>
              特色：尖山埤水庫湖光山色，配備標準高空山訓塔台、人工攀岩壁、低空PA探索場、安全水彈生存遊戲戰場與大營火晚會草坪。
            </div>
            <div class="deck-res-box" style="margin-top:6px;">
              <div class="deck-res-row">
                <span class="deck-res-label">地圖：</span>
                <a class="deck-res-chip map" href="https://maps.google.com/?q=柳營尖山埤渡假村" target="_blank">🗺️ Google 地圖導航</a>
                <a class="deck-res-chip video" href="https://www.youtube.com/watch?v=lDcxvZLpFzg" target="_blank">🎬 尖山埤空拍巡禮</a>
              </div>
            </div>
          </div>
          <div class="tip">
            <span class="tip-tag">全體守則</span>
            <div class="tip-body">各項活動採中隊競賽，落實生活教育、技能教育與團體合作，爭取最高精神總錦標！</div>
          </div>
        </div>
      </div>
    </div>
  </section>


  <!-- Slide 03: 10/23（五)隔宿露營行前說明會 -->
  <section class="slide" id="slide-03">
    <p class="s-eyebrow">BRIEFING · 行前說明會宣導</p>
    <h2 class="s-title">📢 10/23（五) 隔宿露營行前說明會 · 四大生活常規與違紀處分叮嚀</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="border-left: 5px solid #ea580c; margin-bottom: 10px;">
            <h4 class="orange">🚫 一、違禁品出發前再檢查一次</h4>
            <p style="font-size: 13.5px; color: var(--cf-text); line-height: 1.6; font-weight: 700;">
              一、違禁品(菸酒檳榔、刀械…) 出發前再檢查一次
            </p>
            <p style="font-size: 12px; color: var(--cf-text-dim); line-height: 1.5; margin-top: 4px;">
              出發前請在家徹底檢視隨身行李，嚴禁攜帶任何危險品、菸品、酒類、檳榔或刀械。出發當日於 921 地震公園集合時，隨隊導師將實施嚴格安全檢查。
            </p>
          </div>
          <div class="card-slide" style="border-left: 5px solid #2563eb;">
            <h4 style="color:#2563eb;">🪪 二、個人物品與通訊報平安</h4>
            <p style="font-size: 13.5px; color: var(--cf-text); line-height: 1.6; font-weight: 700;">
              二、個人物品(健保卡、醫藥、錢600元內、體育服晚上穿)，手機會統一保管，晚上會有約１小時打回家報平安…
            </p>
            <p style="font-size: 12px; color: var(--cf-text-dim); line-height: 1.5; margin-top: 4px;">
              健保卡正本隨身放內層，零用錢限 600 元內勿攜帶貴重物品。手機由隨隊人員統一保管，於第一天晚間安排約 1 小時開放通話向家長報平安。
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="border-left: 5px solid #16a34a; margin-bottom: 10px;">
            <h4 style="color:#16a34a;">👕 三、服裝儀容規範與畢旅連動機制</h4>
            <p style="font-size: 13.5px; color: var(--cf-text); line-height: 1.6; font-weight: 700;">
              三、服裝儀容著便服或班服（深色長褲）畢旅服裝看表現！
            </p>
            <p style="font-size: 12px; color: var(--cf-text-dim); line-height: 1.5; margin-top: 4px;">
              出發請著乾淨便服或班服，下身務必穿著深色長褲（防蚊蟲及山訓攀岩磨損）。未來國三畢業旅行服裝穿著開放彈性，完全看大家在本次隔宿露營日常紀律的整體表現！
            </p>
          </div>
          <div class="card-slide" style="border-left: 5px solid #dc2626;">
            <h4 style="color:#dc2626;">🚨 四、機動車待命！重大違紀即刻遣返</h4>
            <p style="font-size: 13.5px; color: #dc2626; line-height: 1.6; font-weight: 800;">
              四、機動車！違犯校規之打架、抽菸、喝酒、吃檳檳等 即刻送回學校,家長帶回家管教！記大過！
            </p>
            <p style="font-size: 12px; color: var(--cf-text-dim); line-height: 1.5; margin-top: 4px;">
              營地現場備有機動專車專人待命，若有打架滋事、抽菸、喝酒、嚼食檳榔等重大違犯校規情事，【即刻專車送回學校】，通知家長到校帶回管教，並嚴厲【記大過】處分！
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 04: 行程一覽 Day 1 -->
  <section class="slide" id="slide-04">
    <p class="s-eyebrow">SCHEDULE · 第一天行程</p>
    <h2 class="s-title">Day 1：啟程開訓 · 營地建設 · 童軍分站 · 野炊競賽 · 營火晚會</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <thead><tr><th>時間</th><th>活動項目</th><th>重點備註與實施內容</th></tr></thead>
            <tbody>
              <tr><td>07:30-08:00</td><td><strong>學校集合</strong></td><td>921地震公園暨南投國際會展中心園區（逃生演練）</td></tr>
              <tr><td>08:00-10:00</td><td><strong>乘車出發、安全檢查</strong></td><td>專車國道南下，抵達營地時實施人員與裝備安全檢查</td></tr>
              <tr><td>10:00-11:00</td><td><strong>喜相逢～環境認識</strong></td><td>活動小隊編組、環境認識、安全檢查</td></tr>
              <tr><td>11:00-12:00</td><td><strong>始業式～營規介紹</strong></td><td>值星官宣佈營規、介紹工作人員、環境設施介紹</td></tr>
              <tr><td>12:00-13:00</td><td><strong>午餐時間</strong></td><td>各班就座享用營養中式便當，垃圾分類</td></tr>
              <tr><td>13:00-14:00</td><td><strong>野營常識介紹</strong></td><td>①帳棚搭設講解 ②環境認識 ③器材使用領取</td></tr>
              <tr><td>14:00-17:00</td><td><strong>分站教育 Part 1</strong></td><td>童軍技能教育：（1）生火技巧烹調（2）戰術偽裝方向（3）繩結運用（4）六大毒蛇辨識（5）晚會預習動唱</td></tr>
              <tr><td>17:00-19:00</td><td><strong>晚餐(炊事競賽)</strong></td><td>全校15個野炊小隊炊事競賽，廚藝美味評比</td></tr>
              <tr><td>19:10-21:30</td><td><strong>超ㄅ一ㄤˋ營火晚會！</strong></td><td>班級節目競賽、隊輔勁歌熱舞、團體趣味動唱、薪火相傳燭光夜語</td></tr>
              <tr><td>21:30-22:30</td><td><strong>盥洗、宵夜</strong></td><td>分批盥洗、領取熱騰騰宵夜甜品補充體力</td></tr>
              <tr><td>22:30-----</td><td><strong>就寢＆查舖</strong></td><td>進帳熄燈，室長確實清點人數，導師巡房查舖</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <img class="img-slide" src="assets/img/campfire.jpg" alt="營火晚會">
          <div class="tip warn" style="margin-top:8px;">
            <span class="tip-tag">Day 1 叮嚀</span>
            <div class="tip-body">搭帳以「推入」營柱為原則切勿硬拉；野炊火源專人看顧注意安全；營火晚會熱情投入，燭光夜語與老師真情分享。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 05: 行程一覽 Day 2 -->
  <section class="slide" id="slide-05">
    <p class="s-eyebrow">SCHEDULE · 第二天行程</p>
    <h2 class="s-title">Day 2：晨喚有氧 · 分站山訓極限探索 · BBQ盛宴 · 結訓頒獎</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <thead><tr><th>時間</th><th>活動項目</th><th>重點備註與實施內容</th></tr></thead>
            <tbody>
              <tr><td>06:00-06:30</td><td><strong>起床～做個跟太陽賽跑的人</strong></td><td>晨喚梳洗，整理個人睡袋與防潮墊行囊</td></tr>
              <tr><td>06:30-07:20</td><td><strong>活力有氧、曬帳拆帳</strong></td><td>早操時間、大草坪晨操，內務晨檢評分與曬帳收整</td></tr>
              <tr><td>07:20-08:00</td><td><strong>早餐時間</strong></td><td>渡假村營地餐廳享用熱騰騰中式合菜早餐</td></tr>
              <tr><td>08:00-11:30</td><td><strong>分站教育 Part 2：山訓探索</strong></td><td>五大項次：<br>（1）膽量大考驗、進擊の垂降<br>（2）解手結、團隊跳繩<br>（3）超級蜘蛛人～攀岩絕技<br>（4）生存遊戲、水彈競賽<br>（5）獨木橋（雙索、三索吊橋）</td></tr>
              <tr><td>11:30-14:00</td><td><strong>午餐時間</strong></td><td>歡樂 BBQ 炭烤大餐！慶祝各項任務過關達成</td></tr>
              <tr><td>14:00-15:00</td><td><strong>結訓典禮～～I’m the Best！！</strong></td><td>頒發：炊事比賽、晚會節目、晨檢、分站活動、生活教育與【精神總錦標】競賽獎項</td></tr>
              <tr><td>15:00-16:20</td><td><strong>平安抵校～～Bye-Bye！</strong></td><td>專車啟程返校，預計 16:20 返抵南投國中，互道珍重</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <img class="img-slide" src="assets/img/rappel.jpg" alt="山訓垂降">
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">Day 2 叮嚀</span>
            <div class="tip-body">高空垂降嚴格遵守教官口令；水彈對抗戰場內<b>全程嚴禁取下面罩</b>；BBQ生熟食徹底分開確保飲食衛生。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 06: 遊覽車編組與隨車師長 -->
  <section class="slide" id="slide-06">
    <p class="s-eyebrow">TRANSPORTATION · 官方車次團務表</p>
    <h2 class="s-title">遊覽車編組與隨車師長團務表（去個資版）</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <thead>
              <tr><th>車次</th><th>搭乘班級</th><th>男</th><th>女</th><th>人數</th><th>素食</th><th>隨車行政與導師</th></tr>
            </thead>
            <tbody>
              <tr>
                <td rowspan="2"><strong>1車</strong></td>
                <td>805 班 (205)</td><td>7</td><td>4</td><td rowspan="2"><strong>20</strong></td><td rowspan="2" style="color:#4ade80;">1</td><td rowspan="2">董O遠 (學務主任)、林O銓 (805導師)、許O玉 (806導師)</td>
              </tr>
              <tr>
                <td>806 班 (206)</td><td>4</td><td>5</td>
              </tr>
              <tr>
                <td rowspan="2"><strong>2車</strong></td>
                <td>802 班 (202)</td><td>6</td><td>13</td><td rowspan="2"><strong>34</strong></td><td rowspan="2">0</td><td rowspan="2">黃O君 (802導師)、李O儒 (804導師)</td>
              </tr>
              <tr>
                <td>804 班 (204)</td><td>7</td><td>8</td>
              </tr>
              <tr>
                <td rowspan="2"><strong>3車</strong></td>
                <td>801 班 (201)</td><td>10</td><td>7</td><td rowspan="2"><strong>32</strong></td><td rowspan="2">0</td><td rowspan="2">黃O月 (801導師)、林O玟 (803導師)</td>
              </tr>
              <tr>
                <td>803 班 (203)</td><td>6</td><td>9</td>
              </tr>
              <tr>
                <td><strong>丁車</strong></td>
                <td>807 班 (207)</td><td>8</td><td>13</td><td><strong>21</strong></td><td>0</td><td>姚O勤 (訓育組長)、黃O慧 (807導師)</td>
              </tr>
              <tr style="background:rgba(255,255,255,0.08); font-weight:700;">
                <td colspan="2">全校合計</td><td>48</td><td>59</td><td style="color:var(--cf-accent);">107</td><td style="color:#4ade80;">1</td><td>校長劉O彥、團控經理邱O凱</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🚌 行車安全四大守則</h4>
            <ul style="font-size:12px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>全員繫妥安全帶</b>：車輛發動前至抵達營地全程繫好安全帶。</li>
              <li><b>走道淨空</b>：背包置於上方行李架或下方行李艙，保持逃生通道暢通。</li>
              <li><b>逃生演練落實</b>：發車前確認車頂逃生窗、安全門與車窗擊破器位置。</li>
              <li><b>維護車內清潔</b>：車內不奔跑走動、垃圾隨手打包，下車聽從指揮。</li>
            </ul>
          </div>
          <div class="tip">
            <span class="tip-tag">乘車紀律</span>
            <div class="tip-body">各車車長協助導師確實清點上車人數，互相關照暈車同學，平安順利抵達營地。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 07: 野營常識 ① 營地建設與屋式帳 -->
  <section class="slide" id="slide-07">
    <p class="s-eyebrow">CAMPING SKILLS · 教學參考 ①</p>
    <h2 class="s-title">野營常識 · 營地規劃原則與屋式帳器材步驟</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🏕️ 營地規劃五大分區</h4>
            <div style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              1. <b>搭帳區</b>：門口順風方向，避開低窪積水與枯枝樹下。<br>
              2. <b>炊事區</b>：靠近水源與洗手台，備妥滅火水源與滅火器。<br>
              3. <b>活動場地</b>：中央平坦草坪，供晨操集合與動態訓練。<br>
              4. <b>洗手間 WC</b>：動線清晰、夜間備有照明。<br>
              5. <b>垃圾資源回收場</b>：落實廚餘與乾淨分類，遠離寢帳。
            </div>
          </div>
          <div class="card-slide">
            <h4>📦 屋式帳標準器材</h4>
            <div style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              營釘 14 支 ｜ 主營繩 2 條、副營繩 16 條 ｜ 營柱、雷管、雷帽 ｜ 營樑、內帳、外帳。
            </div>
          </div>
        </div>
        <div>
          <div class="card-slide">
            <h4>⛺ 屋式帳搭設十步驟（手冊官方標準）</h4>
            <ol style="font-size:11.5px; color:var(--cf-text-dim); line-height:1.45; padding-left:18px;">
              <li>先清點器材，分配工作 ｜ 2. 整地排除尖石枯枝</li>
              <li>營門關上保持帳形 ｜ 4. 所有的帳篷定位對齊</li>
              <li>對角 90° 釘下營釘 ｜ 6. 組合金屬營柱</li>
              <li>主營繩拉 45°，接雷管用<b>雙套結</b>，接營釘用<b>營繩結</b>，營釘 45° 釘入</li>
              <li>副營繩拉 45°，營釘 45° 釘入固定</li>
              <li>加外帳，Mark（商標）朝外</li>
              <li>剩餘器材和袋子整齊收入帳篷營門下方</li>
            </ol>
          </div>
          <div class="tip" style="margin-top:6px;">
            <span class="tip-tag">搭帳口訣</span>
            <div class="tip-body"><b>一拉對角、二立中柱、三拉角繩、四拉邊繩、五加外帳膨內帳</b>！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 08: 野營常識 ② 帳棚搭設圖文與無痕山林 -->
  <section class="slide" id="slide-08">
    <p class="s-eyebrow">CAMPING SKILLS · 教學參考 ②</p>
    <h2 class="s-title">野營常識 · 帳棚搭設四步驟圖解 ＆ 無痕山林 (LNT)</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
            <div class="card-slide">
              <h4 style="font-size:12.5px;">1. 取出鋪平</h4>
              <p style="font-size:11px; color:var(--cf-text-dim);">將內帳取出攤開鋪平。「如何取就如何收，簡單又輕鬆」。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:12.5px;">2. 組合營柱</h4>
              <p style="font-size:11px; color:var(--cf-text-dim);">組合四邊營柱，視帳篷規格一般而言有 2-4 根，接節緊密。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:12.5px;">3. 吊掛內帳</h4>
              <p style="font-size:11px; color:var(--cf-text-dim);">營柱與地布四邊小釘固定，內帳與營柱吊掛接合撐起內帳。</p>
            </div>
            <div class="card-slide">
              <h4 style="font-size:12.5px;">4. 穿架外帳</h4>
              <p style="font-size:11px; color:var(--cf-text-dim);">短營柱組合好與營門方向平行垂直，穿過內帳頂端與外帳組合。</p>
            </div>
          </div>
          <div class="card-slide" style="margin-top:6px;">
            <h4>🌿 無痕山林 (LNT) 七大原則</h4>
            <div style="font-size:11.5px; color:var(--cf-text-dim); line-height:1.45;">
              1.事前充分準備 2.在堅實地面紮營 3.妥善處理廢棄物 4.保持環境原貌 5.減低用火影響 6.尊重野生動物 7.考量其他使用者。
            </div>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/tent_setup.jpg" alt="帳棚搭設">
          <div class="deck-res-box" style="margin-top:6px;">
            <div class="deck-res-row">
              <span class="deck-res-label">影片：</span>
              <a class="deck-res-chip video" href="https://www.youtube.com/watch?v=AcHiBUqwBQc" target="_blank">🎬 蒙古包帳篷搭設</a>
              <a class="deck-res-chip video" href="https://www.youtube.com/watch?v=HLJ6EbRRk08" target="_blank">🎬 6人帳實作教學</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 09: 野營常識 ③ 曬帳技巧與防蛇避蟲 -->
  <section class="slide" id="slide-09">
    <p class="s-eyebrow">CAMPING SKILLS · 教學參考 ③</p>
    <h2 class="s-title">野營常識 · 收外帳口訣、曬帳技巧與營地注意事項</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4 class="orange">🗣️ 經典收外帳口訣</h4>
            <p style="font-size:14px; font-weight:700; color:#fed7aa; line-height:1.6;">
              「一拜天地，二拜高堂，夫妻相拜，送入洞房。」<br>
              <span style="font-size:12px; font-weight:400; color:var(--cf-text-dim);">（形容四角平整對摺、中央緊密合摺並滾捲收納入袋）</span>
            </p>
          </div>
          <div class="card-slide">
            <h4>☀️ 隔日清晨曬帳技巧（晨檢評分關鍵）</h4>
            <ol style="font-size:12px; color:var(--cf-text-dim); line-height:1.55; padding-left:18px;">
              <li><b>拔內帳四角營釘</b>：鬆開地面拉力。</li>
              <li><b>調鬆內帳邊繩</b>：使骨架留有活動裕度。</li>
              <li><b>抬高內帳</b>：讓晨風通風對流，排乾帳底濕氣。</li>
              <li><b>固定內帳</b>：曝曬乾燥後才能進行收帳折疊，避免反潮發霉！</li>
            </ol>
          </div>
        </div>
        <div>
          <div class="card-slide" style="border-left:4px solid #ef4444; margin-bottom:8px;">
            <h4 style="color:#f87171;">⚠️ 營地三大安全注意事項（手冊明載）</h4>
            <ul style="font-size:12px; color:var(--cf-text-dim); line-height:1.55; padding-left:16px;">
              <li><b>內外帳不能貼緊</b>：貼合會導致冷凝反潮，「外面下大雨，裡面下小雨」！</li>
              <li><b>晚上鞋子倒放在外帳下</b>：開口朝下傾斜，防止晨露打濕，並防止蛇類與蜈蚣跑入冬眠。</li>
              <li><b>搭帳標準</b>：搭帳兩分鐘，收帳三分鐘，團隊分工展現默契。</li>
            </ul>
          </div>
          <div class="tip">
            <span class="tip-tag">營地選擇要素</span>
            <div class="tip-body"><b>1. 靠近水源 2. 地勢平坦 3. 安全舒適</b>，避開山溝水道與落石區。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 10: 童軍技能 ① 生火技巧與野炊煮飯 -->
  <section class="slide" id="slide-10">
    <p class="s-eyebrow">SCOUT SKILLS · 教學參考 ④</p>
    <h2 class="s-title">童軍技能 · 生火技巧、三級柴火與野炊煮飯要領</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4 class="orange">🔥 削火媒棒與三級柴火堆疊</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>火媒棒</b>：小刀 45° 削出薄羽狀木屑，增加與空氣接觸面積。<br>
              <b>引火柴 (Tinder)</b>：火種、枯乾細草、細枯松針，一星即著。<br>
              <b>助燃柴 (Kindling)</b>：牙籤至小指粗乾燥枯枝，交叉搭建通風塔型。<br>
              <b>燃燒柴 (Fuel)</b>：耐燒木炭與腕粗木塊，提供持久穩定紅火熱源。
            </p>
          </div>
          <div class="card-slide">
            <h4 class="orange">🍚 野炊煮出香Ｑ白飯金牌秘訣</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>洗米浸泡</b>：米泡水 15~20 分鐘，米水比 <b>1 : 1.1～1.2</b>。<br>
              <b>大火煮滾</b>：井字柴大火燒滾至鍋蓋邊緣噴出濃白蒸氣。<br>
              <b>小火收乾</b>：轉微火慢煨約 5 分鐘，聞到微焦飯香。<br>
              <b>離火燜飯</b>：【不可掀蓋！離火燜放 15 分鐘】，米粒香Ｑ透心！
            </p>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/cooking.jpg" alt="野炊炊事">
          <div class="tip" style="margin-top:6px;">
            <span class="tip-tag">野炊小隊分工</span>
            <div class="tip-body"><b>小隊長調度、大廚二廚洗切炒調、伙夫控火、水夫供水、事務清點</b>，素食專鍋專鏟！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 11: 童軍技能 ② 戰術偽裝與方向辨識 -->
  <section class="slide" id="slide-11">
    <p class="s-eyebrow">SCOUT SKILLS · 教學參考 ⑤</p>
    <h2 class="s-title">童軍技能 · 戰術偽裝原則與自然方向辨識 (16方位)</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🪖 面部偽裝「凸暗凹亮」打破輪廓原則</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>凸處塗暗</b>：額頭、鼻樑、顴骨、下巴等反光面塗深綠/黑色迷彩。<br>
              <b>凹處塗亮</b>：眼窩、人中、頸項陰影部位塗淡草綠色。<br>
              <b>破壞對稱</b>：以斜斑紋塗抹，破壞人臉原有生理輪廓，完美隱身草叢。
            </p>
          </div>
          <div class="card-slide">
            <h4>🧭 自然方向辨識（手冊官方記載）</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.45;">
              1. <b>指針與地圖</b>：指南針磁北校正。<br>
              2. <b>日月星象</b>：日出東日落西；北斗七星尋北極星（正北方）。<a href="https://gemini.google.com/share/90fe02a031a5?social_preview=false&skid=498c1de2-4192-4fb7-9b14-92d3a058c761" target="_blank" rel="noopener noreferrer" class="deck-res-chip" style="background:#4338ca; color:#ffffff; border-color:#6366f1; font-weight:700; margin-left:6px; padding:2px 8px;">🌓 月相模擬器 ↗</a><br>
              3. <b>樹木年輪</b>：密者為北（南向陽光多年輪疏寬，北向年輪密集）。<br>
              4. <b>樹木茂密</b>：密者為南、青苔多者為北。<br>
              5. <b>向日葵</b>：12:00 以前朝向東南，12:00 以後朝向西南。<br>
              6. <b>古老房舍與墓碑</b>：閩南傳統建築大多「坐北朝南」。
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="margin-bottom:6px;">
            <h4>🧭 16 方位盤角度速查</h4>
            <div style="font-size:11.5px; color:var(--cf-text-dim); line-height:1.45;">
              1. 北 0° ｜ 2. 北北東 22.5° ｜ 3. 東北 45° ｜ 4. 東東北 67.5°<br>
              5. 東 90° ｜ 6. 東南東 112.5° ｜ 7. 東南 135° ｜ 8. 南南東 157.5°<br>
              9. 南 180° ｜ 10. 南南西 202.5° ｜ 11. 西南 225° ｜ 12. 西南西 247.5°<br>
              13. 西 270° ｜ 14. 西西北 292.5° ｜ 15. 西北 315° ｜ 16. 北西北 337.5°
            </div>
          </div>
          <div class="tip">
            <span class="tip-tag">追蹤記號</span>
            <div class="tip-body">以落葉、枯枝或石塊擺成箭頭、叉號或藏寶信號，引導隊友行進定向。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 12: 童軍技能 ③ 常用八大繩結 -->
  <section class="slide" id="slide-12">
    <p class="s-eyebrow">SCOUT SKILLS · 教學參考 ⑥</p>
    <h2 class="s-title">童軍技能 · 出神入化！手冊常用八大繩結</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck">
            <thead><tr><th>繩結名稱</th><th>用途類別</th><th>操作要領與應用場合</th></tr></thead>
            <tbody>
              <tr><td><strong>單結</strong></td><td>防脫結</td><td>最基礎繩結，打於繩尾防止脫線滑脫</td></tr>
              <tr><td><strong>八字結</strong></td><td>繩端結</td><td>強度優於單結，受力後極易解開，登山攀岩必備</td></tr>
              <tr><td><strong>活結</strong></td><td>束口吊掛</td><td>輕拉繩尾即可瞬間解開，臨時繫綁行李</td></tr>
              <tr><td><strong>平結</strong></td><td>接等粗繩</td><td>左壓右右壓左，連接粗細相同之繩索，急救三角巾包紮</td></tr>
              <tr><td><strong>接繩結</strong></td><td>接異徑繩</td><td>粗繩成環細繩穿繞，連接粗細不同或乾濕不同之繩</td></tr>
              <tr><td><strong>雙套結</strong></td><td>工程起手</td><td>繞桿兩圈交叉扣入，搭帳固定於營柱雷管必備之王</td></tr>
              <tr><td><strong>雙半結</strong></td><td>繫固於樁</td><td>兩次半結繞固定於樹木或圓環，越拉越牢</td></tr>
              <tr><td><strong>營繩結</strong></td><td>張力調節</td><td>可滑動微調長度張力，受力咬死，搭帳拉營繩必備</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <img class="img-slide" src="assets/img/rope_knots.jpg" alt="八大繩結">
          <div class="tip" style="margin-top:6px;">
            <span class="tip-tag">練習口訣</span>
            <div class="tip-body"><b>平結接等粗、接繩接異徑；雷管用雙套、營繩結調拉線</b>！童軍繩隨身帶隨手練。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 13: 野外安全 ① 臺灣毒蛇辨識 -->
  <section class="slide" id="slide-13">
    <p class="s-eyebrow">OUTDOOR SAFETY · 教學參考 ⑦</p>
    <h2 class="s-title">野外安全 · 臺灣主要毒蛇辨識與習性</h2>
    <div class="s-body">
      <div class="grid-deck-2">
        <div class="card-slide" style="border-left:4px solid #ef4444;">
          <h4 style="color:#f87171;">百步蛇 (出血性毒 · 蝮蛇科)</h4>
          <p style="font-size:12px; line-height:1.5; color:var(--cf-text-dim);">
            <b>特徵</b>：頭大呈三角形，吻端明顯向上突出翹起，體側黑褐色大三角形斑紋。<br>
            <b>危險</b>：排毒量大，咬人率第五，<b>致死率第一</b>！皮下嚴重出血壞死。
          </p>
        </div>
        <div class="card-slide" style="border-left:4px solid #ef4444;">
          <h4 style="color:#f87171;">雨傘節 (神經性毒 · 蝙蝠蛇科)</h4>
          <p style="font-size:12px; line-height:1.5; color:var(--cf-text-dim);">
            <b>特徵</b>：體背黑白相間等寬環紋，背脊呈菱形隆起。<br>
            <b>危險</b>：咬人率第三，<b>致死率第二</b>！咬傷不痛不腫，數小時內呼吸衰竭！
          </p>
        </div>
        <div class="card-slide" style="border-left:4px solid #f59e0b;">
          <h4 style="color:#fbbf24;">赤尾青竹絲 (出血性毒 · 蝮蛇科)</h4>
          <p style="font-size:12px; line-height:1.5; color:var(--cf-text-dim);">
            <b>特徵</b>：體色翠綠，尾端磚紅色，體側有一條白色縱線。<br>
            <b>危險</b>：台灣咬人率最高（常棲於草叢灌木），毒性相對較溫和。
          </p>
        </div>
        <div class="card-slide" style="border-left:4px solid #f59e0b;">
          <h4 style="color:#fbbf24;">龜殼花 (出血性毒 · 蝮蛇科)</h4>
          <p style="font-size:12px; line-height:1.5; color:var(--cf-text-dim);">
            <b>特徵</b>：頭部呈烙鐵三角形，背部有褐色不規則波浪龜裂狀斑塊。<br>
            <b>危險</b>：夜間出沒於枯枝落葉堆，出血毒性強，咬傷腫脹血泡。
          </p>
        </div>
      </div>
      <div class="tip" style="margin-top:8px;">
        <span class="tip-tag">防蛇鐵則</span>
        <div class="tip-body">戶外野外行進落實<b>「打草驚蛇」</b>；穿著長褲布鞋、夜間攜手電筒，嚴禁徒手翻動草叢與石塊！</div>
      </div>
    </div>
  </section>

  <!-- Slide 14: 野外安全 ② 蛇傷急救【五要五不】 -->
  <section class="slide" id="slide-14">
    <p class="s-eyebrow">FIRST AID · 教學參考 ⑧</p>
    <h2 class="s-title">野外安全 · 毒蛇咬傷黃金自救【五要五不】原則</h2>
    <div class="s-body">
      <div class="cols c2">
        <div class="card-slide" style="border-left:4px solid #22c55e;">
          <h4 style="color:#4ade80;">✅ 毒蛇咬傷【五要】原則</h4>
          <ul style="font-size:12.5px; line-height:1.6; color:var(--cf-text-dim); padding-left:16px;">
            <li><b>要視為毒蛇</b>：凡遭蛇咬，第一時間皆以毒蛇咬傷處理。</li>
            <li><b>要保持冷靜</b>：安撫傷患靜坐，避免奔跑劇烈運動加速血液循環。</li>
            <li><b>要脫下束縛物</b>：迅速取下傷肢之戒指、手錶、手鐲，避免腫脹缺血壞死。</li>
            <li><b>要彈性包紮固定</b>：以彈性繃帶寬鬆包紮，患肢保持<b>低於心臟</b>位置。</li>
            <li><b>要火速送醫</b>：記下或拍下蛇類外觀特徵，儘速送醫施打對應抗蛇毒血清。</li>
          </ul>
        </div>
        <div class="card-slide" style="border-left:4px solid #ef4444;">
          <h4 style="color:#f87171;">❌ 毒蛇咬傷【五不】禁忌</h4>
          <ul style="font-size:12.5px; line-height:1.6; color:var(--cf-text-dim); padding-left:16px;">
            <li><b>不要切開傷口</b>：切開會破壞血管肌腱，造成大量失血與細菌感染。</li>
            <li><b>不要用嘴吸吮</b>：口腔微創黏膜會吸收毒素，造成施救者中毒！</li>
            <li><b>不要冰敷傷口</b>：冰敷造成極度血管痙攣，加速局部組織壞疽。</li>
            <li><b>不要使用止血帶勒緊</b>：過度束緊阻斷動脈，易引發缺血截肢危機！</li>
            <li><b>不要飲用刺激品</b>：嚴禁飲酒、濃茶或咖啡，避免擴散毒素。</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 15: 簡易急救專題 -->
  <section class="slide" id="slide-15">
    <p class="s-eyebrow">FIRST AID · 手冊官方課程</p>
    <h2 class="s-title">簡易急救 · 意外割傷、抽筋、流鼻血與骨折緊急處理</h2>
    <div class="s-body">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
        <div class="card-slide">
          <h4>🩹 意外割傷處理</h4>
          <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
            1. 生水或稀釋消毒藥水洗淨傷口。<br>
            2. 無菌清潔紗布直接「加壓止血」，不可亂用未經消毒粉末或藥油。<br>
            3. 繃帶紮好並儘可能將傷處「抬高高於心臟」。<br>
            4. 趕緊送醫救治。
          </p>
        </div>
        <div class="card-slide">
          <h4>🦵 肌肉抽筋緩解四部位手法</h4>
          <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
            <b>手抽筋</b>：慢慢拉直抽筋手指，輕輕施力按摩。<br>
            <b>腳抽筋</b>：慢慢拉直腳趾，輕輕按摩腳部肌肉。<br>
            <b>大腿抽筋</b>：膝部拉直，一手放腳跟抬高腿部，一手按壓按摩。<br>
            <b>小腿抽筋</b>：小心伸直膝蓋抬腿，腳掌向上屈壓向小腿，輕柔按摩。
          </p>
        </div>
        <div class="card-slide">
          <h4>🩸 流鼻血緊急處理（大原則）</h4>
          <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
            1. 安靜坐椅上，<b>「頭向前傾」</b>（千萬不要後仰避免嗆血，勿拍脖子）。<br>
            2. 改用口呼吸，手用力捏住兩側鼻部軟骨 5~10 分鐘設法止血。<br>
            3. 鼻樑以毛巾冷敷，口中血液吐出；10~15 分鐘未止血儘速就醫。
          </p>
        </div>
        <div class="card-slide">
          <h4>🦴 骨折緊急處理</h4>
          <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
            1. 檢查意識呼吸，休克時心肺復甦。<br>
            2. 固定傷肢減輕疼痛，就地取材（木板、竹竿），<b>夾板長度超過上下兩關節</b>！<br>
            3. 無材料時上肢固定胸壁、下肢與未受傷側綑綁。<br>
            4. 脊椎骨折平臥硬板，等待救護人員。
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 16: 營火晚會與動唱律動 -->
  <section class="slide" id="slide-16">
    <p class="s-eyebrow">CAMPFIRE NIGHT · 青春高潮</p>
    <h2 class="s-title">童軍技能 · 超ㄅ一ㄤˋ營火晚會儀式、拜火詞與燭光夜語</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4 class="orange">🔥 營火晚會三部曲</h4>
            <p style="font-size:12.5px; color:var(--cf-text-dim); line-height:1.5;">
              <b>神聖迎火</b>：火神引火入場、全場靜肅，齊誦神聖拜火詞。<br>
              <b>歡狂動唱</b>：班級創意節目競賽、隊輔勁歌熱舞、趣味動唱嗨翻星空！<br>
              <b>薪火相傳</b>：營火轉為溫暖燭光，圍坐草坪與導師分享成長印記。
            </p>
          </div>
          <div class="card-slide">
            <h4 class="orange">🗣️ 神聖拜火詞</h4>
            <p style="font-size:13px; color:#fde047; font-weight:700; line-height:1.5;">
              「阿給拉～魯巴～魯巴！偉大的火神，請賜予南投國中光明、勇氣與熱情！熊熊營火，燃燒吧！」
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide">
            <h4>🎵 經典營火歡唱歌謠</h4>
            <ul style="font-size:12px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>《營火歌》</b>：朋友！燃起這營火，照耀著我們的友誼...火花在黑夜裡飛舞...</li>
              <li><b>《成吉思汗》</b>：風沙滾滾，戰馬奔馳，嘿！喝！嘿！喝！無敵南投健兒！</li>
              <li><b>《第一支舞》</b>：帶著笑容，你走向我，做個邀請的動作...難忘的夜晚...</li>
              <li><b>《薪火相傳》</b>：手捧溫暖燭光，敞開心扉，感謝導師與同儕陪伴。</li>
            </ul>
          </div>
          <div class="deck-res-box" style="margin-top:6px;">
            <div class="deck-res-row">
              <span class="deck-res-label">影片：</span>
              <a class="deck-res-chip video" href="https://www.youtube.com/watch?v=7gkjhNzvaB0" target="_blank">🎬 第一支舞帶動跳</a>
              <a class="deck-res-chip video" href="https://www.youtube.com/watch?v=EarIVtT71uk" target="_blank">🎬 成吉思汗大會動唱</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 17: 探索教育哲學與精神 -->
  <section class="slide" id="slide-17">
    <p class="s-eyebrow">ADVENTURE EDUCATION · 探索教育</p>
    <h2 class="s-title">探索教育 · 體驗式學習四大精神 ＆ FVC 三哲學</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>📖 體驗式學習 (Learning by Doing)</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              「閱讀的資訊能學到 10%；聽到的資訊能學到 15%；但<b>所經驗過的事，我們卻能學習到 80%</b>！」<br>
              身心合一，去感受、在實踐中超越自己。
            </p>
          </div>
          <div class="card-slide">
            <h4>🌟 體驗式學習四大執行精神</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.45;">
              1. <b>Learning by doing</b>：做中學，身心合一團隊參與。<br>
              2. <b>Everything for fun</b>：有趣放鬆的模式，進入深度心靈學習。<br>
              3. <b>Open space</b>：開放思維，解構心智、歸零學習。<br>
              4. <b>Master</b>：自發性學習意願，彼此尊重與成長喜悅。
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="border-left:4px solid var(--cf-accent); margin-bottom:8px;">
            <h4>🤝 探索教育三哲學 (Full Value Contract)</h4>
            <ol style="font-size:12px; color:var(--cf-text-dim); line-height:1.5; padding-left:16px;">
              <li>同意像一個團隊一樣地工作，為個人及團隊目標而努力。</li>
              <li>同意堅守安全規則及團體行動方針。</li>
              <li>無論是積極或消極的回饋，都願意貢獻或自團體接收，並朝向適當的行為改變。</li>
            </ol>
          </div>
          <div class="card-slide">
            <h4>🎯 選擇性挑戰 (Challenge by Choice)</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              所有的挑戰都是參加者自己選擇的，做不同選擇的背後要付出不同代價。當你不確定自己在做什麼的時候，恭喜你，表示你正在成長！
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 18: 山訓探索 ① 高空垂直垂降 -->
  <section class="slide" id="slide-18">
    <p class="s-eyebrow">MOUNTAIN TRAINING · 山訓探索 ①</p>
    <h2 class="s-title">山訓探索 · 膽量大考驗！進擊の高空垂直垂降</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🧗 裝備與安全檢核 (Buddy Check)</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              UIAA 認證岩盔、坐式安全吊帶（貼合一指寬反扣）、八字環下降器、主鎖大D扣死、防磨手套。兩人一組相互檢核。
            </p>
          </div>
          <div class="card-slide">
            <h4>🦵 站姿與制動四要領</h4>
            <ul style="font-size:12px; color:var(--cf-text-dim); line-height:1.5; padding-left:16px;">
              <li><b>雙腳微開</b>：與肩同寬，腳底平實踩踏塔台岩壁邊緣。</li>
              <li><b>大膽後傾</b>：身體勇敢後傾 45°～60°，背與壁垂直，重心下沉於腳底。</li>
              <li><b>雙手分工</b>：上方導繩手（左手）輕握繩索導向；下方制動手（右手）置於右後臀。</li>
              <li><b>制動煞停</b>：【右手往前往上繩鬆即下滑、右手貼臀扣緊即煞停】！</li>
            </ul>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/rappel.jpg" alt="高空垂降">
          <div class="tip warn" style="margin-top:6px;">
            <span class="tip-tag">心理突破</span>
            <div class="tip-body">恐懼來自未知，相信確保系統！深呼吸跨出塔台邊緣第一步，你就是征服高空的勇者！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 19: 山訓探索 ② 超級蜘蛛人攀岩 -->
  <section class="slide" id="slide-19">
    <p class="s-eyebrow">MOUNTAIN TRAINING · 山訓探索 ②</p>
    <h2 class="s-title">山訓探索 · 超級蜘蛛人～人工岩場攀登絕技</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🕷️ 攀岩三大黃金法則</h4>
            <ul style="font-size:12.5px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
              <li><b>三點不動一點動</b>：保持三點支撐三角形，一次僅移動一肢，維持平衡重心。</li>
              <li><b>重量在腳不在手</b>：腿肌力量比手臂大三倍！手臂主要貼壁導向，發力全靠雙腳蹬起！</li>
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
          <img class="img-slide" src="assets/img/jianshanpi_3.jpg" alt="人工攀岩">
          <div class="tip" style="margin-top:6px;">
            <span class="tip-tag">攀岩心法</span>
            <div class="tip-body">攀登前先在岩壁下方<b>「讀線」</b>，用眼睛找出最佳抓握點與踩腳點，有條不紊步步高升！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 20: 山訓探索 ③ 獨木橋橫渡平衡 -->
  <section class="slide" id="slide-20">
    <p class="s-eyebrow">MOUNTAIN TRAINING · 山訓探索 ③</p>
    <h2 class="s-title">山訓探索 · 獨木橋橫渡 ＆ 雙索、三索突擊吊橋走法</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>※ 雙索突擊吊橋走法（手冊規範）</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              通過人員行進時兩手兩足同時向對岸橫移，<b>步幅每步約 45 公分</b>，不宜過大。手掌不得離開手索，足掌不得離開足索，體重落於足索上，微向前傾，身心盡量保持平衡與安定。
            </p>
          </div>
          <div class="card-slide">
            <h4>※ 三索突擊吊橋走法（手冊規範）</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              通過人員前進時雙手握兩側繩索，<b>雙腳外八字行走於足索</b>，兩眼注視足索，步幅不宜過大，身體重心落於足索，力求穩步前進。
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🪵 獨木橋平衡三要素</h4>
            <ul style="font-size:12px; color:var(--cf-text-dim); line-height:1.5; padding-left:16px;">
              <li><b>重心壓低</b>：雙膝微彎吸收木橋晃動，重心沉於腹部下丹田。</li>
              <li><b>雙臂平展</b>：雙手水平張開如天平兩側微調平衡。</li>
              <li><b>視線向前</b>：雙眼鎖定前方終點，<b>切忌低頭看腳底</b>！</li>
            </ul>
          </div>
          <div class="tip">
            <span class="tip-tag">山訓場紀律</span>
            <div class="tip-body">進入山訓場嚴禁打鬧嘻戲，人人保持嚴肅，確實服從教官指導，訓練中嚴禁吸菸。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 21: 探索教育 ② 解手結與團隊跳繩 -->
  <section class="slide" id="slide-21">
    <p class="s-eyebrow">ADVENTURE EDUCATION · 探索教育 ②</p>
    <h2 class="s-title">探索教育 · 解手結謎題 (Human Knot) ＆ 團隊跳繩心跳同頻</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🤝 PA 經典探索：解手結 (Human Knot)</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>遊戲規則</b>：小隊圍圈伸出雙手，隨機牽住不同隊友左右手（不牽相鄰者、同人不重複）。在<b>「雙手絕不鬆開」</b>的前提下，藉由跨步、翻轉、鑽身，將糾結的手結還原為一個完整大圓圈。<br>
              <b>團隊意涵</b>：考驗傾聽他人聲音、溝通協調、系統化思考與彼此的肢體信任。
            </p>
          </div>
          <div class="card-slide">
            <h4>🪢 團隊跳繩 (Team Jump Rope)</h4>
            <p style="font-size:12px; color:var(--cf-text-dim); line-height:1.5;">
              <b>甩繩手穩定</b>：兩名甩繩手保持均勻大弧度擺盪，大繩觸地發出穩定節奏「啪」。<br>
              <b>全員同步</b>：進場踩準反彈節拍，齊呼口號「一、二、跳！」，呼吸與步伐完全一致。
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="height:100%; display:flex; flex-direction:column; justify-content:center;">
            <h4 style="font-size:15px; margin-bottom:10px;">🏆 團隊突破三大心法</h4>
            <div style="background:rgba(0,0,0,0.3); border:1px solid var(--cf-rule); border-radius:8px; padding:12px; font-size:12.5px; line-height:1.6; color:#cbd5e1;">
              1. <b>不抱怨、不責怪</b>：每一次失敗都是累積團隊默契的養分。<br>
              2. <b>專注指揮核心</b>：一人發號施令，全員專注配合執行。<br>
              3. <b>團結就是力量</b>：個人的堅持成就班級集體的最高榮譽！
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 22: 探索教育 ③ 水彈生存競技與13條安全守則 -->
  <section class="slide" id="slide-22">
    <p class="s-eyebrow">TACTICAL GAME · 山訓探索 ④</p>
    <h2 class="s-title">探索教育 · 水彈生存競技戰術 ＆ 13 條安全守則</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="border-left:4px solid #ef4444; margin-bottom:8px;">
            <h4 style="color:#f87171;">🛡️ 水彈 13 條安全守則（手冊明載）</h4>
            <ol style="font-size:11px; color:var(--cf-text-dim); line-height:1.4; padding-left:16px;">
              <li>遵守水彈場內遊戲規則。 ｜ 2. 遊戲中請著個人裝備。</li>
              <li>嚴禁持槍朝向他人。 ｜ 4. 任何狀況下不得窺視水彈槍口。</li>
              <li>射擊時應注意方向與距離。 ｜ 6. 水彈槍應存放安全位置。</li>
              <li><b>在遊戲進行中嚴禁取下護目面罩！</b></li>
              <li>禁止在非指定射擊區域進行射擊。</li>
              <li>非遊戲時請將水彈槍上保險，並套上槍口塞。</li>
              <li>禁止近距離內對人體射擊（國際以十英呎為界定）。</li>
              <li>嚴禁對裁判員、觀察員及出局者射擊。</li>
              <li>嚴禁對非參與遊戲者或護具不全者射擊。</li>
              <li>嚴格遵守各遊戲場特殊規定，確保遊戲安全。</li>
            </ol>
          </div>
        </div>
        <div>
          <img class="img-slide" src="assets/img/water_gun.jpg" alt="水彈生存遊戲">
          <div class="card-slide" style="margin-top:6px;">
            <h4>🎯 團隊戰術佈陣</h4>
            <p style="font-size:11.5px; color:var(--cf-text-dim); line-height:1.45;">
              <b>前鋒推進</b>：利用掩體交替掩護前進。<br>
              <b>中鋒壓制</b>：點射壓制敵方火力掩護轉移。<br>
              <b>後方陣地</b>：保全隊旗，中彈者自覺高舉雙手退場展現榮譽！
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 23: 行前行李打包清單 -->
  <section class="slide" id="slide-23">
    <p class="s-eyebrow">PACKING LIST · 想一想，準備好了，出發！</p>
    <h2 class="s-title">行前必備 · 行李清單與打包防護（手冊官方標準）</h2>
    <div class="s-body">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
        <div class="card-slide">
          <h4>🪪 重要證件與個人隨身</h4>
          <ul style="font-size:12px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
            <li><b>健保 IC 卡 (必備！)</b>：隨身背包內層防水收納</li>
            <li>少量零錢、少許行動零食</li>
            <li>帽子、雨具（輕便型雨衣）</li>
            <li>行動電話或充電器、行動電源</li>
          </ul>
        </div>
        <div class="card-slide">
          <h4>👕 服裝與鞋襪</h4>
          <ul style="font-size:12px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
            <li>換洗衣物及保暖外套（長袖防風、早晚溫差）</li>
            <li>運動鞋（山訓活動全程穿著，禁穿涼拖鞋訓練）</li>
            <li>拖鞋（盥洗與夜間帳區換穿）</li>
            <li>運動厚襪（多備 1~2 雙）</li>
          </ul>
        </div>
        <div class="card-slide">
          <h4>🧼 衛生保健與防護</h4>
          <ul style="font-size:12px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
            <li>盥洗用具（牙刷、牙膏、毛巾）</li>
            <li>個人備用口罩 2~3 片</li>
            <li>防曬及保養用品、防蚊液</li>
            <li>私人藥品（氣喘、感冒、暈車藥等醫師處方藥）</li>
          </ul>
        </div>
        <div class="card-slide">
          <h4>🎒 裝備與收納袋</h4>
          <ul style="font-size:12px; line-height:1.55; color:var(--cf-text-dim); padding-left:16px;">
            <li>旅行雙肩背包（裝載全部個人裝備，勿手提散落）</li>
            <li>乾淨塑膠袋 2~3 個（換洗髒衣與防潮使用）</li>
            <li>相機、電池或充電器（選帶）</li>
            <li>水壺 / 環保杯（隨時補充水分）</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 24: 營規生活須知與考核評分 -->
  <section class="slide" id="slide-24">
    <p class="s-eyebrow">CAMP RULES & HONORS</p>
    <h2 class="s-title">營規生活須知 · 精神總錦標計分 ＆ 緊急應變聯絡</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="margin-bottom:8px;">
            <h4>🏆 精神總錦標與競賽獎項評比</h4>
            <div style="font-size:12px; color:var(--cf-text-dim); line-height:1.55;">
              結訓典禮頒發：<b>炊事比賽、晚會節目、晨檢內務、分站活動、生活教育、精神總錦標</b>！<br>
              評比要點：集合守時、服從值星官、帳篷內務整潔、野炊環境復原、團隊歡呼與勝不驕敗不餒風度。
            </div>
          </div>
          <div class="card-slide">
            <h4>📋 營區四大紀律</h4>
            <ul style="font-size:12px; color:var(--cf-text-dim); line-height:1.5; padding-left:16px;">
              <li>全體行動聽從師長指揮，嚴禁私自離隊夜遊。</li>
              <li>22:30 就寢號響一律熄燈就寢，男生嚴禁入女帳、女生嚴禁入男帳。</li>
              <li>愛護營地公物花草，垃圾分類廚餘入桶。</li>
              <li>遇任何身心不適或突發狀況，第一時間向導師或醫護站反應。</li>
            </ul>
          </div>
        </div>
        <div>
          <div class="card-slide" style="border-left:4px solid var(--fire-orange);">
            <h4 class="orange">📞 緊急應變聯絡網</h4>
            <div style="font-size:12px; color:var(--cf-text-dim); line-height:1.6;">
              <b>南投市立南投國民中學</b>：(049) 222-2549<br>
              <b>台南尖山埤露營渡假村</b>：(06) 623-3888<br>
              <b>承辦旅行社</b>：中國青年旅行社中部分公司<br>
              <b>團控經理</b>：邱O凱 0972-721756<br>
              <b>隨隊行政主管</b>：學務主任 董O遠、訓育組長 姚O勤
            </div>
          </div>
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">遊必有方</span>
            <div class="tip-body">每天依規定時段向家人報平安，讓家人放心，讓青春留下最驕傲的足跡！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 25: 去個資帳篷住宿分配總表（一） -->
  <section class="slide" id="slide-25">
    <p class="s-eyebrow">TENT ALLOCATION · 帳篷住宿表 ①</p>
    <h2 class="s-title">801 班 ＆ 802 班 帳篷住宿分配一覽表（去個資版）</h2>
    <div class="s-body">
      <table class="table-deck">
        <thead>
          <tr><th>班級</th><th>帳棚</th><th>車次</th><th>性別</th><th>人數</th><th>全體住宿名冊（名字第二字 O 遮罩）</th></tr>
        </thead>
        <tbody>
          <tr>
            <td rowspan="4"><strong>801 班</strong><br><span style="font-size:11px; color:var(--cf-text-dim);">導師：黃O月</span></td>
            <td><strong>A01</strong></td><td>3車</td><td>男帳</td><td>5人</td>
            <td>林O諼、張O鈞、張O偉、吳O岷、谷O恩</td>
          </tr>
          <tr>
            <td><strong>A02</strong></td><td>3車</td><td>男帳</td><td>5人</td>
            <td>湯O丞、陳O廷、許O瑋、陳O宗、賴O豪</td>
          </tr>
          <tr>
            <td><strong>B01</strong></td><td>3車</td><td>女帳</td><td>3人</td>
            <td>林O言、劉O含、藍O詒</td>
          </tr>
          <tr>
            <td><strong>B02</strong></td><td>3車</td><td>女帳</td><td>4人</td>
            <td>林O嫻、江O婷、陳O翎、陳O涵</td>
          </tr>
          <tr>
            <td rowspan="5"><strong>802 班</strong><br><span style="font-size:11px; color:var(--cf-text-dim);">導師：黃O君</span></td>
            <td><strong>A03</strong></td><td>2車</td><td>男帳</td><td>3人</td>
            <td>黃O睿、葉O毅、廖O惟</td>
          </tr>
          <tr>
            <td><strong>A04</strong></td><td>2車</td><td>男帳</td><td>3人</td>
            <td>劉O宇、張O瑋、簡O宸</td>
          </tr>
          <tr>
            <td><strong>B03</strong></td><td>2車</td><td>女帳</td><td>4人</td>
            <td>李O妮、李O甯、鄭O琳、黃O蒂</td>
          </tr>
          <tr>
            <td><strong>B04</strong></td><td>2車</td><td>女帳</td><td>4人</td>
            <td>簡O懿、黃O薇、賴O其、鐘O彤</td>
          </tr>
          <tr>
            <td><strong>B05</strong></td><td>2車</td><td>女帳</td><td>5人</td>
            <td>郭O琪、廖O昕、胡O薰、張O桔、詹O彤</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- Slide 26: 去個資帳篷住宿分配總表（二） -->
  <section class="slide" id="slide-26">
    <p class="s-eyebrow">TENT ALLOCATION · 帳篷住宿表 ②</p>
    <h2 class="s-title">803 班 ＆ 804 班 帳篷住宿分配一覽表（去個資版）</h2>
    <div class="s-body">
      <table class="table-deck">
        <thead>
          <tr><th>班級</th><th>帳棚</th><th>車次</th><th>性別</th><th>人數</th><th>全體住宿名冊（名字第二字 O 遮罩）</th></tr>
        </thead>
        <tbody>
          <tr>
            <td rowspan="4"><strong>803 班</strong><br><span style="font-size:11px; color:var(--cf-text-dim);">導師：林O玟</span></td>
            <td><strong>A05</strong></td><td>3車</td><td>男帳</td><td>3人</td>
            <td>許O煜、陳O熙、蔡O呈</td>
          </tr>
          <tr>
            <td><strong>A06</strong></td><td>3車</td><td>男帳</td><td>3人</td>
            <td>陳O天、陳O瑜、李O成</td>
          </tr>
          <tr>
            <td><strong>B06</strong></td><td>3車</td><td>女帳</td><td>5人</td>
            <td>王O芝、石O芳、吳O恩、吳O蓉、潘O汝</td>
          </tr>
          <tr>
            <td><strong>B07</strong></td><td>3車</td><td>女帳</td><td>4人</td>
            <td>邱O慈、陳O羽、謝O璇、沈O愉</td>
          </tr>
          <tr>
            <td rowspan="4"><strong>804 班</strong><br><span style="font-size:11px; color:var(--cf-text-dim);">導師：李O儒</span></td>
            <td><strong>A07</strong></td><td>2車</td><td>男帳</td><td>3人</td>
            <td>陳O光、蕭O皓、陳O昇</td>
          </tr>
          <tr>
            <td><strong>A08</strong></td><td>2車</td><td>男帳</td><td>4人</td>
            <td>林O澄、許O翔、劉O振、張O帆</td>
          </tr>
          <tr>
            <td><strong>B08</strong></td><td>2車</td><td>女帳</td><td>4人</td>
            <td>王O涵、陳O妘、張O晴、劉O硯</td>
          </tr>
          <tr>
            <td><strong>B09</strong></td><td>2車</td><td>女帳</td><td>4人</td>
            <td>羅O茜、簡O璇、余O婷、洪O瑄</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- Slide 27: 去個資帳篷住宿分配總表（三） -->
  <section class="slide" id="slide-27">
    <p class="s-eyebrow">TENT ALLOCATION · 帳篷住宿表 ③</p>
    <h2 class="s-title">805班、806班 ＆ 807班 帳篷住宿分配一覽表（去個資版）</h2>
    <div class="s-body">
      <table class="table-deck">
        <thead>
          <tr><th>班級</th><th>帳棚</th><th>車次</th><th>性別</th><th>人數</th><th>全體住宿名冊（名字第二字 O 遮罩）</th></tr>
        </thead>
        <tbody>
          <tr>
            <td rowspan="3"><strong>805 班</strong><br><span style="font-size:11px; color:var(--cf-text-dim);">導師：林O銓</span></td>
            <td><strong>A09</strong></td><td>1車</td><td>男帳</td><td>4人</td>
            <td>林O竹、郭O佑、陳O庭、嚴O諭</td>
          </tr>
          <tr>
            <td><strong>A10</strong></td><td>1車</td><td>男帳</td><td>3人</td>
            <td>吳O鋒、簡O宇、張O瑜</td>
          </tr>
          <tr>
            <td><strong>B10</strong></td><td>1車</td><td>女帳</td><td>4人</td>
            <td>劉O硯、吳O瑜、黃O薇、鄭O妮</td>
          </tr>
          <tr>
            <td rowspan="2"><strong>806 班</strong><br><span style="font-size:11px; color:var(--cf-text-dim);">導師：許O玉</span></td>
            <td><strong>A11</strong></td><td>1車</td><td>男帳</td><td>4人</td>
            <td>吳O文、曾O承、洪O倫、張O棋</td>
          </tr>
          <tr>
            <td><strong>B11</strong></td><td>1車</td><td>女帳</td><td>5人</td>
            <td>陳O臻、李O榕、林O妤、范O英、廖O慈</td>
          </tr>
          <tr>
            <td rowspan="5"><strong>807 班</strong><br><span style="font-size:11px; color:var(--cf-text-dim);">導師：黃O慧</span></td>
            <td><strong>A12</strong></td><td>丁車</td><td>男帳</td><td>4人</td>
            <td>吳O霆、洪O熙、張O睿、黃O壬</td>
          </tr>
          <tr>
            <td><strong>A13</strong></td><td>丁車</td><td>男帳</td><td>4人</td>
            <td>呂O辰、林O福、林O旻、許O瀚</td>
          </tr>
          <tr>
            <td><strong>B12</strong></td><td>丁車</td><td>女帳</td><td>4人</td>
            <td>張O瑄、郭O岑、黃O浠、詹O靜</td>
          </tr>
          <tr>
            <td><strong>B13</strong></td><td>丁車</td><td>女帳</td><td>5人</td>
            <td>林O妤、吳O桐、陳O錥、蕭O晨、簡O緹</td>
          </tr>
          <tr>
            <td><strong>B14</strong></td><td>丁車</td><td>女帳</td><td>4人</td>
            <td>廖O涵、陳O伶、古O潼、胡O熙</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- Slide 28: 去個資野炊分組表（一） -->
  <section class="slide" id="slide-28">
    <p class="s-eyebrow">COOKING SQUADS · 野炊炊事表 ①</p>
    <h2 class="s-title">第 1 組 ～ 第 5 組 野炊分組名冊（801 班、802 班 去個資版）</h2>
    <div class="s-body">
      <table class="table-deck">
        <thead>
          <tr><th>組別</th><th>班級</th><th>車次</th><th>人數</th><th>小隊全體名冊及分工（去個資版）</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>第 1 組</strong></td><td>801 班</td><td>3車</td><td>9人</td>
            <td>劉O含、林O言、谷O恩、張O鈞、張O偉、林O諼、陳O宗、賴O豪、藍O詒</td>
          </tr>
          <tr>
            <td><strong>第 2 組</strong></td><td>801 班</td><td>3車</td><td>8人</td>
            <td>林O嫻、陳O翎、江O婷、陳O涵、湯O丞、吳O岷、許O瑋、陳O廷</td>
          </tr>
          <tr>
            <td><strong>第 3 組</strong></td><td>802 班</td><td>2車</td><td>6人</td>
            <td>黃O薇、廖O惟、賴O其、簡O懿、鐘O彤、張O瑋</td>
          </tr>
          <tr>
            <td><strong>第 4 組</strong></td><td>802 班</td><td>2車</td><td>6人</td>
            <td>葉O毅、李O甯、李O妮、鄭O琳、黃O蒂、黃O睿</td>
          </tr>
          <tr>
            <td><strong>第 5 組</strong></td><td>802 班</td><td>2車</td><td>7人</td>
            <td>廖O昕、胡O薰、郭O琪、張O桔、簡O宸、劉O宇、詹O彤</td>
          </tr>
        </tbody>
      </table>
      <div class="tip" style="margin-top:10px;">
        <span class="tip-tag">野炊要訣</span>
        <div class="tip-body">生食熟食砧板刀具徹底分開；小隊長掌控火候進度；餐後徹底刷洗洗淨器材交還。</div>
      </div>
    </div>
  </section>

  <!-- Slide 29: 去個資野炊分組表（二） -->
  <section class="slide" id="slide-29">
    <p class="s-eyebrow">COOKING SQUADS · 野炊炊事表 ②</p>
    <h2 class="s-title">第 6 組 ～ 第 10 組 野炊分組名冊（803 班、804 班、805 班 去個資版）</h2>
    <div class="s-body">
      <table class="table-deck">
        <thead>
          <tr><th>組別</th><th>班級</th><th>車次</th><th>人數</th><th>小隊全體名冊及分工（去個資版）</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>第 6 組</strong></td><td>803 班</td><td>3車</td><td>8人</td>
            <td>王O芝、石O芳、吳O恩、吳O蓉、潘O汝、許O煜、陳O熙、蔡O呈</td>
          </tr>
          <tr>
            <td><strong>第 7 組</strong></td><td>803 班</td><td>3車</td><td>7人</td>
            <td>邱O慈、陳O羽、謝O璇、沈O愉、陳O天、陳O瑜、李O成</td>
          </tr>
          <tr>
            <td><strong>第 8 組</strong></td><td>804 班</td><td>2車</td><td>7人</td>
            <td>陳O光、張O帆、林O澄、劉O振、許O翔、蕭O皓、陳O昇</td>
          </tr>
          <tr>
            <td><strong>第 9 組</strong></td><td>804 班</td><td>2車</td><td>8人</td>
            <td>張O晴、洪O瑄、余O婷、簡O璇、陳O妘、羅O茜、王O涵、劉O硯</td>
          </tr>
          <tr>
            <td><strong>第 10 組</strong></td><td>805 班</td><td>1車</td><td>7人</td>
            <td>林O竹、吳O鋒、簡O宇、郭O佑、陳O庭、嚴O諭、<strong style="color:#4ade80;">張O瑜(素)</strong></td>
          </tr>
        </tbody>
      </table>
      <div class="tip" style="margin-top:10px;">
        <span class="tip-tag">素食叮嚀</span>
        <div class="tip-body">第 10 組張O瑜同學為素食餐，野炊食材與鍋具嚴格獨立分開烹煮，展現同儕關懷！</div>
      </div>
    </div>
  </section>

  <!-- Slide 30: 去個資野炊分組表（三） -->
  <section class="slide" id="slide-30">
    <p class="s-eyebrow">COOKING SQUADS · 野炊炊事表 ③</p>
    <h2 class="s-title">第 11 組 ～ 第 15 組 野炊分組名冊（805班、806班、807班 去個資版）</h2>
    <div class="s-body">
      <table class="table-deck">
        <thead>
          <tr><th>組別</th><th>班級</th><th>車次</th><th>人數</th><th>小隊全體名冊及分工（去個資版）</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>第 11 組</strong></td><td>805 班</td><td>1車</td><td>4人</td>
            <td>劉O硯、吳O瑜、黃O薇、鄭O妮</td>
          </tr>
          <tr>
            <td><strong>第 12 組</strong></td><td>806 班</td><td>1車</td><td>9人</td>
            <td>廖O慈、洪O倫、范O英、林O妤、張O棋、吳O文、陳O臻、李O榕、曾O承</td>
          </tr>
          <tr>
            <td><strong>第 13 組</strong></td><td>807 班</td><td>丁車</td><td>7人</td>
            <td>郭O岑、黃O浠、詹O靜、張O瑄、胡O熙、古O潼、陳O伶</td>
          </tr>
          <tr>
            <td><strong>第 14 組</strong></td><td>807 班</td><td>丁車</td><td>6人</td>
            <td>吳O桐、林O妤、陳O錥、廖O涵、蕭O晨、簡O緹</td>
          </tr>
          <tr>
            <td><strong>第 15 組</strong></td><td>807 班</td><td>丁車</td><td>8人</td>
            <td>吳O霆、呂O辰、林O福、林O旻、洪O熙、張O睿、許O瀚、黃O壬</td>
          </tr>
        </tbody>
      </table>
      <div class="tip" style="margin-top:10px;">
        <span class="tip-tag">野炊考核</span>
        <div class="tip-body">評比包含：菜餚色香味俱全、桌面整潔、垃圾確實分類回收、器具歸還清點，爭取炊事錦標！</div>
      </div>
    </div>
  </section>

  <!-- Slide 31: 童軍技能分站教育學習單（一） -->
  <section class="slide" id="slide-31">
    <p class="s-eyebrow">SCOUT WORKSHEET ① · 童軍學習單 ①</p>
    <h2 class="s-title">童軍技能分站學習單（手冊 P.22）：營帳挑錯 ＆ 有毒生物 ＆ 中暑急救</h2>
    <div class="s-body">
      <div class="grid-deck-3">
        <!-- 任務一 -->
        <div class="card-slide">
          <h4 class="orange">⛺ 任務一：營帳挑錯（圈出5處違規）</h4>
          <img class="img-slide" src="assets/img/worksheet/tent_error_spotting.jpg" alt="營帳挑錯情境" style="height:120px; object-fit:contain; background:#111; margin-bottom:6px;">
          <ul style="font-size:11px; color:var(--cf-text-dim); line-height:1.5; padding-left:14px;">
            <li><strong>① 嚴禁帳內開火生火</strong>（極易引起帳篷燃燒或一氧化碳中毒）。</li>
            <li><strong>② 嚴禁帳內吸菸</strong>（火星引燃化學帳布，密閉煙霧窒息）。</li>
            <li><strong>③ 嚴禁帳內外散落食物</strong>（易引來蛇類、螞蟻、野狗及老鼠）。</li>
            <li><strong>④ 鞋子應倒扣朝外放於前庭</strong>（避免露水蟲蟻爬入）。</li>
            <li><strong>⑤ 營釘需45度外斜固定、營繩拉緊</strong>（未拉緊易坍塌灌風雨）。</li>
          </ul>
        </div>

        <!-- 任務二 -->
        <div class="card-slide">
          <h4 style="color:#38bdf8;">🌿 任務二：5大有毒動植物辨識配對</h4>
          <img class="img-slide" src="assets/img/worksheet/poisonous_matching.jpg" alt="有毒動植物配對" style="height:120px; object-fit:contain; background:#111; margin-bottom:6px;">
          <div style="font-size:11px; color:var(--cf-text-dim); line-height:1.5;">
            <div><strong>① 刺絲胞水母 (F)</strong>：觸鬚有毒刺絲胞，引起紅腫劇痛休克。</div>
            <div><strong>② 百步蛇 (B)</strong>：出血毒性強烈，體表三角斑紋，致死率高。</div>
            <div><strong>③ 咬人貓 (D)</strong>：全株具刺毛含蟻酸，碰觸灼痛紅腫。</div>
            <div><strong>④ 海檬果 (H)</strong>：全株劇毒含海檬果苷，白色汁液致心律不整。</div>
            <div><strong>⑤ 眼鏡蛇 (G)</strong>：神經性毒毒蛇，受驚時頸部扁平膨起。</div>
          </div>
        </div>

        <!-- 任務三 -->
        <div class="card-slide">
          <h4 style="color:#4ade80;">🚑 任務三：熱傷害／中暑急救 SOP</h4>
          <img class="img-slide" src="assets/img/worksheet/heatstroke_flowchart.jpg" alt="中暑急救流程" style="height:120px; object-fit:contain; background:#111; margin-bottom:6px;">
          <div style="font-size:11px; color:var(--cf-text-dim); line-height:1.5;">
            <div><strong>步驟 1【移】</strong>迅速移至陰涼通風處，解開衣物鬆開束縛。</div>
            <div><strong>步驟 2【降】</strong>冷水噴灑擦拭全身，以扇子風扇搧風加速蒸發。</div>
            <div><strong>步驟 3【補】</strong>患者清醒時補充適量清水或淡鹽水（昏迷絕不可灌水）。</div>
            <div><strong>步驟 4【送】</strong>體溫持續高燒不退或意識不清，保持側臥呼吸順暢儘速送醫。</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 32: 童軍技能分站教育學習單（二） -->
  <section class="slide" id="slide-32">
    <p class="s-eyebrow">SCOUT WORKSHEET ② · 童軍學習單 ②</p>
    <h2 class="s-title">童軍技能分站學習單（手冊 P.23）：繩結連線 ＆ 單結繩梯 ＆ 繩索特性</h2>
    <div class="s-body">
      <div class="grid-deck-3">
        <!-- 任務四：歡樂連線 -->
        <div class="card-slide">
          <h4 class="orange">🔗 歡樂連線（情境與繩結配對）</h4>
          <img class="img-slide" src="assets/img/worksheet/knot_matching.jpg" alt="繩結情境連線" style="height:120px; object-fit:contain; background:#111; margin-bottom:6px;">
          <ul style="font-size:11.5px; color:var(--cf-text-dim); line-height:1.6; padding-left:14px;">
            <li><strong>領巾配戴</strong> ➔ <strong>平結</strong>（平整美觀服貼於胸前）</li>
            <li><strong>熱水壺提把防燙</strong> ➔ <strong>連續雙半結／纏繞結</strong></li>
            <li><strong>抓繩攀爬防滑</strong> ➔ <strong>繩梯多重單結／防滑結</strong></li>
            <li><strong>腳踝三角巾固定</strong> ➔ <strong>平結</strong>（包紮平整不壓迫傷口）</li>
          </ul>
        </div>

        <!-- 單結與繩梯變化 -->
        <div class="card-slide">
          <h4 style="color:#38bdf8;">🪢 單結基本用途 ＆ 繩梯防滑變化</h4>
          <img class="img-slide" src="assets/img/worksheet/overhand_knot_variations.jpg" alt="單結繩梯變化" style="height:120px; object-fit:contain; background:#111; margin-bottom:6px;">
          <div style="font-size:11.5px; color:var(--cf-text-dim); line-height:1.6;">
            <div><strong>① 單結基本用途</strong>：</div>
            <div style="padding-left:8px; margin-bottom:4px;">繩端防脫結、最基礎簡易結繩打法、其他複合繩結之核心起點。</div>
            <div><strong>② 繩梯多重防滑結</strong>：</div>
            <div style="padding-left:8px;">沿攀爬主繩間隔等距打上單結或八字結，提供抓握支點與防滑踩踏階梯，大幅減輕攀登耗力。</div>
          </div>
        </div>

        <!-- 繩索材質比較 -->
        <div class="card-slide">
          <h4 style="color:#4ade80;">🧵 繩索材質比較（天然 vs 化學）</h4>
          <table class="table-deck" style="font-size:11px; margin-top:2px;">
            <thead>
              <tr><th>材質特性</th><th>天然纖維（麻繩/棉繩）</th><th>人造纖維（尼龍/特多龍）</th></tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>拉力強度</strong></td>
                <td>拉力較小，承重力普通</td>
                <td><strong style="color:#38bdf8;">拉力極高</strong>，承重極佳</td>
              </tr>
              <tr>
                <td><strong>吸水防腐</strong></td>
                <td>易吸水增重、潮濕易發霉腐爛</td>
                <td>耐水性強、快乾、不發霉腐爛</td>
              </tr>
              <tr>
                <td><strong>耐磨耐熱</strong></td>
                <td>耐摩擦耐高溫，不易熔化</td>
                <td>耐磨性佳，但遇高溫摩擦易熔化</td>
              </tr>
              <tr>
                <td><strong>最佳用途</strong></td>
                <td>童軍工程架設、包裝、結紮</td>
                <td>攀岩登山、水上救援、帳篷風繩</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 33: 二年級戶外教育活動自我檢核表 -->
  <section class="slide" id="slide-33">
    <p class="s-eyebrow">SELF CHECKLIST · 自我檢核表</p>
    <h2 class="s-title">二年級戶外教育活動自我檢核表（手冊 P.24 · 全 13 項標準評量）</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <table class="table-deck" style="font-size:11px;">
            <thead>
              <tr><th>#</th><th>檢核指標項目（手冊第24頁規範）</th><th>標準配分</th></tr>
            </thead>
            <tbody>
              <tr><td>1</td><td>我能學習規劃童軍體驗生活。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>2</td><td>我能運用資訊，做好行前準備。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>3</td><td>每個單元課程我都能仔細觀察。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>4</td><td>我能認真完成學習手冊。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>5</td><td>我能體會「行萬里路，勝讀萬卷書」的意義。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>6</td><td>集合時能守時，遵守作息規定。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>7</td><td>能熟讀生活須知並確實遵守。</td><td>5分（優/良/可/差/劣）</td></tr>
            </tbody>
          </table>
        </div>
        <div>
          <table class="table-deck" style="font-size:11px;">
            <thead>
              <tr><th>#</th><th>檢核指標項目（手冊第24頁規範）</th><th>標準配分</th></tr>
            </thead>
            <tbody>
              <tr><td>8</td><td>遵守團體紀律維護團體榮譽。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>9</td><td>聽從帶隊師長指導不私自行動。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>10</td><td>同學互助合作、互相照顧。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>11</td><td>我能傾聽及發表分享心得。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>12</td><td>尊重生命，愛惜大自然。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td>13</td><td>遊必有方，能每天向家人報平安。</td><td>5分（優/良/可/差/劣）</td></tr>
              <tr><td colspan="2"><strong style="color:var(--fire-orange);">滿分 65 分 · 綜合評分與導師簽章核可</strong></td><td><strong>總分 65</strong></td></tr>
            </tbody>
          </table>
          <div class="tip" style="margin-top:8px;">
            <span class="tip-tag">電子手冊連動</span>
            <div class="tip-body">手機版電子手冊「檢核表」分頁提供互動點選計分、自動換算達成率與評語簽章儲存功能！</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide 34: 青春美好回憶 ＆ 平安賦歸 -->
  <section class="slide" id="slide-34">
    <p class="s-eyebrow">MEMORIES & CONCLUSION · 美好回憶</p>
    <h2 class="s-title">青春美好回憶 · 榮譽感恩 ＆ 平安賦歸</h2>
    <div class="s-body">
      <div class="cols c2">
        <div>
          <div class="card-slide" style="border-left:4px solid var(--cf-accent); text-align:center; padding:18px 14px; margin-bottom:10px;">
            <p style="font-size:16px; color:#f8fafc; font-weight:700; line-height:1.8;">
              「在休閒旅遊的地圖上，找到失落已久的寶藏；<br>
              發現真實的自己，以及與心靈對話的樂趣；<br>
              而福爾摩沙的星空，有我最美的記憶。」
            </p>
            <p style="font-size:12px; color:var(--cf-accent); margin-top:8px;">
              —— 南投縣立南投國民中學 115 學年度二年級全體師生 留念
            </p>
          </div>
          <div class="card-slide">
            <h4>🙏 感恩與致謝</h4>
            <p style="font-size:11.5px; color:var(--cf-text-dim); line-height:1.6;">
              感謝校長、學務處團隊、全體二年級隨隊導師全程守護；<br>
              感謝車隊司機大哥平穩駕駛、營區工作人員與領隊隊輔熱情帶領；<br>
              更感謝每一位互相扶持、發揮童軍合作精神的南投國中同學！
            </p>
          </div>
        </div>
        <div>
          <div class="card-slide" style="text-align:center; padding:16px 12px; margin-bottom:10px;">
            <h4 style="justify-content:center; margin-bottom:8px;">⛺ 營隊榮譽錦標回顧</h4>
            <div style="font-size:12px; color:var(--cf-text-dim); line-height:1.7;">
              精神總錦標 ｜ 秩序錦標 ｜ 整潔錦標 ｜ 炊事錦標 ｜ 營火晚會演出獎<br>
              <span style="color:#fcd34d; font-weight:700;">每個小隊都收穫了無價的團隊合作與童軍生活淬鍊！</span>
            </div>
          </div>
          <div style="text-align:center; margin-top:16px;">
            <a href="index.html" class="deck-btn is-on" style="font-size:14px; padding:8px 20px; text-decoration:none;">📱 開啟手機版電子手冊 (index.html)</a>
          </div>
        </div>
      </div>
    </div>
  </section>

</main>

<!-- 懸浮左右快速翻頁大箭頭 -->
<button class="floating-nav-btn prev" id="float-prev" type="button" title="上一頁 (←)" aria-label="上一頁">‹</button>
<button class="floating-nav-btn next" id="float-next" type="button" title="下一頁 (→)" aria-label="下一頁">›</button>

<!-- 投影模式底部懸浮控制列 -->
<nav class="deck-ctrl" id="deck-ctrl" aria-label="簡報控制">
  <button class="ctrl-btn" id="ctrl-prev" type="button" title="上一頁 (←)">◀ 上一頁</button>
  <span class="ctrl-pos" id="ctrl-pos">01 / 34</span>
  <button class="ctrl-btn" id="ctrl-next" type="button" title="下一頁 (→ / 空白鍵)">下一頁 ▶</button>
  <button class="ctrl-btn" id="ctrl-toc-bottom" type="button" title="目錄總覽 (T)">📑 目錄總覽</button>
</nav>

<!-- 簡報目錄總覽彈出層 (TOC Modal) -->
<div class="deck-toc" id="deck-toc" hidden>
  <div class="deck-toc-panel">
    <div class="deck-toc-head">
      <span class="deck-toc-title">📑 簡報目錄總覽（全 34 頁）</span>
      <button class="deck-btn" id="toc-close" type="button">✕ 關閉 (ESC)</button>
    </div>
    <div class="deck-toc-grid" id="deck-toc-grid">
      <!-- 由 JS 動態生成每頁卡片 -->
    </div>
  </div>
</div>

<script src="lesson-deck.js?v=20261020_v2"></script>
</body>
</html>
"""

with open('slides.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully built slides.html with 31 comprehensive slides!")

/**
 * 南投縣立南投國民中學 115學年度 二年級隔宿露營行動數位手冊
 * 前端核心互動邏輯 (script.js)
 */

document.addEventListener("DOMContentLoaded", () => {
  if (typeof CAMP_DATA === "undefined") {
    console.error("CAMP_DATA is not loaded! Please check data.js.");
    return;
  }

  const { info, classes, itinerary, students, tents, squads, teachingGuides, checklist, rules } = CAMP_DATA;

  // 狀態管理（安全讀取 localStorage）
  let initialChecklistState = {};
  try {
    initialChecklistState = JSON.parse(localStorage.getItem("ntjh_camp_pack_list_v1") || "{}");
  } catch (e) {
    initialChecklistState = {};
  }

  const state = {
    activeTab: "itinerary",
    selectedDay: 1,
    tentQuery: "",
    tentClass: "all",
    tentViewMode: "card", // 'card' or 'table'
    squadQuery: "",
    squadClass: "all",
    squadViewMode: "card", // 'card' or 'table'
    rosterQuery: "",
    rosterFilter: "all",
    checklistState: initialChecklistState
  };

  /* ==========================================================================
     1. 導航切換 (Desktop Tabs & Mobile Bottom Nav)
     ========================================================================== */
  function switchTab(targetTab) {
    if (!targetTab) return;
    state.activeTab = targetTab;

    const desktopBtns = document.querySelectorAll(".nav-tab-btn");
    const mobileBtns = document.querySelectorAll(".mobile-nav-btn");
    const panes = document.querySelectorAll(".tab-pane");

    desktopBtns.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === targetTab);
    });
    mobileBtns.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === targetTab);
    });

    panes.forEach(pane => {
      const isTarget = pane.id === `tab-${targetTab}`;
      pane.classList.toggle("active", isTarget);
      pane.style.display = isTarget ? "block" : "none";
    });

    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, null, `#${targetTab}`);
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // 註冊全域函式以供呼叫
  window.switchTabTo = switchTab;

  function initNavigation() {
    const desktopBtns = document.querySelectorAll(".nav-tab-btn");
    const mobileBtns = document.querySelectorAll(".mobile-nav-btn");

    desktopBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const tab = btn.dataset.tab;
        if (tab) switchTab(tab);
      });
    });

    mobileBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const tab = btn.dataset.tab;
        if (tab) switchTab(tab);
      });
    });

    // 全域委派事件：確保點擊按鈕內文字、圖示或動態標籤均可切換
    document.addEventListener("click", (e) => {
      const tabTarget = e.target.closest("[data-tab]");
      if (tabTarget) {
        const tab = tabTarget.getAttribute("data-tab");
        if (tab) {
          switchTab(tab);
        }
      }
    });

    // 檢查網址 hash
    const hash = window.location.hash.replace("#", "");
    if (hash && document.getElementById(`tab-${hash}`)) {
      switchTab(hash);
    } else {
      switchTab("itinerary");
    }
  }

  // 安全依序初始化所有模組，個別異常不影響其他功能
  const modules = [
    ["導航功能", initNavigation],
    ["頂部卡片", initQuickHeroCards],
    ["行程總覽", initItinerary],
    ["帳篷速查", initTents],
    ["野炊小隊", initSquads],
    ["學生名冊", initRoster],
    ["營地景點", initAttractions],
    ["童軍技能卡", initScoutKnowledgeCards],
    ["營火晚會", initCampfireLyrics],
    ["山訓探索", initMountainTraining],
    ["行李清單", initChecklist],
    ["生活營規", initRules],
    ["車輛編組", initBusSchedule],
    ["手冊全文", initManualViewer]
  ];

  modules.forEach(([name, initFn]) => {
    try {
      initFn();
    } catch (err) {
      console.error(`[模組初始化異常 - ${name}]:`, err);
    }
  });

  /* ==========================================================================
     2. 頂部快速資訊 (Quick Hero Cards)
     ========================================================================== */
  function initQuickHeroCards() {
    const container = document.getElementById("hero-hotels-container");
    if (!container || !info.locations) return;

    container.innerHTML = info.locations.map(loc => `
      <div class="quick-card">
        <div>
          <div class="quick-card-title">${loc.tag}</div>
          <div class="quick-card-hotel">${loc.name}</div>
          <div style="font-size:0.75rem; color:rgba(255,255,255,0.85); margin-top:2px;">📍 ${loc.address}</div>
        </div>
        <div class="quick-card-actions">
          <a href="${loc.telLink}" class="quick-btn">
            📞 撥號 (${loc.phone})
          </a>
          <a href="${loc.mapUrl}" target="_blank" rel="noopener noreferrer" class="quick-btn">
            🗺️ 地圖導航
          </a>
        </div>
      </div>
    `).join("");
  }

  /* ==========================================================================
     3. 行程時間軸
     ========================================================================== */
  function initItinerary() {
    const daySelector = document.getElementById("day-selector");
    const container = document.getElementById("itinerary-content-container");
    if (!daySelector || !container || !itinerary) return;

    daySelector.innerHTML = itinerary.map((d, idx) => `
      <button class="day-pill-btn ${idx === 0 ? 'active' : ''}" data-day="${d.day}">
        <div class="d-title">第 ${d.day} 天</div>
        <div class="d-sub">${d.title.split('・')[0]}</div>
      </button>
    `).join("");

    function renderDayTimeline(dayNum) {
      const dayData = itinerary.find(d => d.day === dayNum) || itinerary[0];

      let mealsHtml = `
        <div class="meals-summary-box">
          <div><b>🍱 午餐：</b> ${dayData.meals.lunch}</div>
          <div><b>🍲 晚餐：</b> ${dayData.meals.dinner}</div>
          <div><b>🥣 早餐/宵夜：</b> ${dayData.meals.breakfast || dayData.meals.night}</div>
        </div>
      `;

      let itemsHtml = `
        <div class="timeline-list">
          ${dayData.timeline.map(item => `
            <div class="timeline-item">
              <div class="timeline-time">${item.time}</div>
              <div class="timeline-activity">${item.title.replace(/\n/g, ' ')}</div>
              <div class="timeline-desc">${item.desc}</div>
            </div>
          `).join("")}
        </div>
      `;

      container.innerHTML = `
        <div class="timeline-card">
          <h3 style="font-size:1.1rem; font-weight:800; color:var(--primary-dark); margin-bottom:12px;">
            第 ${dayData.day} 天 · ${dayData.title}
          </h3>
          ${mealsHtml}
          ${itemsHtml}
        </div>
      `;
    }

    renderDayTimeline(1);

    daySelector.querySelectorAll(".day-pill-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        daySelector.querySelectorAll(".day-pill-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        renderDayTimeline(parseInt(btn.dataset.day, 10));
      });
    });
  }

  /* ==========================================================================
     4. 帳篷住宿速查
     ========================================================================== */
  function initTents() {
    const container = document.getElementById("tents-cards-container");
    const tableContainer = document.getElementById("tents-table-container");
    const searchInput = document.getElementById("tents-search-input");
    const clearBtn = document.getElementById("tents-search-clear");
    const chipsContainer = document.getElementById("tents-class-filter-chips");
    const countLabel = document.getElementById("tents-results-count");
    const viewBtns = document.querySelectorAll(".tents-view-btn");
    if (!container || !tents) return;

    // Render filter chips
    const classList = ["all", "201", "202", "203", "204", "205", "206", "207"];
    if (chipsContainer) {
      chipsContainer.innerHTML = classList.map(c => `
        <button class="chip-btn ${c === 'all' ? 'active' : ''}" data-class="${c}">
          ${c === 'all' ? '全部班級 (27帳)' : c + ' 班'}
        </button>
      `).join("");
    }

    function render() {
      const kw = state.tentQuery.toLowerCase();
      const filtered = tents.filter(t => {
        const matchClass = (state.tentClass === "all") || (t.classNum === state.tentClass);
        const matchKw = !kw ||
          t.class.toLowerCase().includes(kw) ||
          t.tentName.toLowerCase().includes(kw) ||
          t.leaderName.toLowerCase().includes(kw) ||
          String(t.leaderSeat).includes(kw) ||
          t.members.toLowerCase().includes(kw) ||
          t.notes.toLowerCase().includes(kw);
        return matchClass && matchKw;
      });

      if (countLabel) {
        countLabel.textContent = `符合帳數：${filtered.length} 頂帳篷`;
      }

      if (filtered.length === 0) {
        container.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:30px; color:var(--text-muted);">無符合之帳篷資料</div>`;
        if (tableContainer) tableContainer.innerHTML = `<div style="text-align:center; padding:30px; color:var(--text-muted);">無符合之帳篷資料</div>`;
        return;
      }

      // 1. 卡片視圖
      container.innerHTML = filtered.map(t => `
        <div class="data-card">
          <div class="data-card-header">
            <div class="data-card-title">${t.class} · ${t.tentName}</div>
            <span class="badge-pill ${t.gender.includes('男') ? 'male' : 'female'}">${t.gender} · ${t.count}</span>
          </div>
          <div style="font-size:0.88rem; line-height:1.6;">
            <div style="margin-bottom:6px;">
              <span class="badge-pill leader">室長</span>
              <strong>${t.leaderSeat}號 ${t.leaderName}</strong>
            </div>
            <div>
              <b style="color:var(--text-main);">同帳成員：</b><br>
              <span style="color:var(--text-muted);">${t.members}</span>
            </div>
            ${t.notes ? `<div style="margin-top:6px; font-size:0.8rem; color:#d97706;">📌 ${t.notes}</div>` : ''}
          </div>
        </div>
      `).join("");

      // 2. 表格視圖
      if (tableContainer) {
        tableContainer.innerHTML = `
          <table class="custom-table">
            <thead>
              <tr>
                <th>班級</th>
                <th>性別</th>
                <th>帳別</th>
                <th>室長</th>
                <th>人數</th>
                <th>同帳成員名單</th>
                <th>備註</th>
              </tr>
            </thead>
            <tbody>
              ${filtered.map(t => `
                <tr>
                  <td><strong>${t.class}</strong></td>
                  <td><span class="badge-pill ${t.gender.includes('男') ? 'male' : 'female'}">${t.gender}</span></td>
                  <td><strong>${t.tentName}</strong></td>
                  <td><span class="badge-pill leader">室長</span> ${t.leaderSeat}號 ${t.leaderName}</td>
                  <td>${t.count}</td>
                  <td>${t.members}</td>
                  <td style="color:#d97706;">${t.notes || '—'}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        `;
      }
    }

    render();

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.tentQuery = e.target.value.trim();
        if (clearBtn) clearBtn.classList.toggle("visible", state.tentQuery.length > 0);
        render();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        state.tentQuery = "";
        searchInput.value = "";
        clearBtn.classList.remove("visible");
        render();
      });
    }

    if (chipsContainer) {
      chipsContainer.addEventListener("click", (e) => {
        if (e.target.matches(".chip-btn")) {
          chipsContainer.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
          e.target.classList.add("active");
          state.tentClass = e.target.dataset.class;
          render();
        }
      });
    }

    viewBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        viewBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        state.tentViewMode = btn.dataset.view;
        if (container) container.style.display = state.tentViewMode === "card" ? "grid" : "none";
        if (tableContainer) tableContainer.style.display = state.tentViewMode === "table" ? "block" : "none";
      });
    });
  }

  /* ==========================================================================
     5. 野炊小隊速查
     ========================================================================== */
  function initSquads() {
    const container = document.getElementById("squads-cards-container");
    const tableContainer = document.getElementById("squads-table-container");
    const searchInput = document.getElementById("squads-search-input");
    const clearBtn = document.getElementById("squads-search-clear");
    const chipsContainer = document.getElementById("squads-class-filter-chips");
    const countLabel = document.getElementById("squads-results-count");
    const viewBtns = document.querySelectorAll(".squads-view-btn");
    if (!container || !squads) return;

    const classList = ["all", "201", "202", "203", "204", "205", "206", "207"];
    if (chipsContainer) {
      chipsContainer.innerHTML = classList.map(c => `
        <button class="chip-btn ${c === 'all' ? 'active' : ''}" data-class="${c}">
          ${c === 'all' ? '全部小隊 (15隊)' : c + ' 班'}
        </button>
      `).join("");
    }

    function render() {
      const kw = state.squadQuery.toLowerCase();
      const filtered = squads.filter(s => {
        const matchClass = (state.squadClass === "all") || (s.classNum === state.squadClass);
        const matchKw = !kw ||
          s.class.toLowerCase().includes(kw) ||
          s.squadName.toLowerCase().includes(kw) ||
          s.leader.toLowerCase().includes(kw) ||
          s.deputy.toLowerCase().includes(kw) ||
          s.chef1.toLowerCase().includes(kw) ||
          s.chef2.toLowerCase().includes(kw) ||
          s.fire.toLowerCase().includes(kw) ||
          s.water.toLowerCase().includes(kw) ||
          s.affairs.toLowerCase().includes(kw) ||
          s.members.toLowerCase().includes(kw);
        return matchClass && matchKw;
      });

      if (countLabel) {
        countLabel.textContent = `符合隊數：${filtered.length} 個小隊`;
      }

      if (filtered.length === 0) {
        container.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:30px; color:var(--text-muted);">無符合之小隊資料</div>`;
        if (tableContainer) tableContainer.innerHTML = `<div style="text-align:center; padding:30px; color:var(--text-muted);">無符合之小隊資料</div>`;
        return;
      }

      // 卡片視圖
      container.innerHTML = filtered.map(s => `
        <div class="data-card">
          <div class="data-card-header">
            <div class="data-card-title">${s.class} · ${s.squadName}</div>
            <span class="badge-pill squad">${s.count}</span>
          </div>
          <div style="font-size:0.85rem; line-height:1.6;">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; margin-bottom:8px;">
              <div><b>隊長：</b>${s.leader}</div>
              <div><b>副隊：</b>${s.deputy}</div>
              <div><b>大廚：</b>${s.chef1}</div>
              <div><b>二廚：</b>${s.chef2}</div>
              <div><b>伙夫：</b>${s.fire}</div>
              <div><b>水夫：</b>${s.water}</div>
            </div>
            ${s.affairs && s.affairs !== '—' ? `<div><b>事務：</b>${s.affairs}</div>` : ''}
            ${s.members && s.members !== '—' ? `<div style="margin-top:4px;"><b>隊員：</b>${s.members}</div>` : ''}
          </div>
        </div>
      `).join("");

      // 表格視圖
      if (tableContainer) {
        tableContainer.innerHTML = `
          <table class="custom-table">
            <thead>
              <tr>
                <th>班級</th>
                <th>小隊</th>
                <th>人數</th>
                <th>小隊長</th>
                <th>副隊長</th>
                <th>大廚</th>
                <th>二廚</th>
                <th>伙夫</th>
                <th>水夫</th>
                <th>事務</th>
                <th>隊員名單</th>
              </tr>
            </thead>
            <tbody>
              ${filtered.map(s => `
                <tr>
                  <td><strong>${s.class}</strong></td>
                  <td><strong>${s.squadName}</strong></td>
                  <td>${s.count}</td>
                  <td>${s.leader}</td>
                  <td>${s.deputy}</td>
                  <td>${s.chef1}</td>
                  <td>${s.chef2}</td>
                  <td>${s.fire}</td>
                  <td>${s.water}</td>
                  <td>${s.affairs}</td>
                  <td>${s.members}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        `;
      }
    }

    render();

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.squadQuery = e.target.value.trim();
        if (clearBtn) clearBtn.classList.toggle("visible", state.squadQuery.length > 0);
        render();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        state.squadQuery = "";
        searchInput.value = "";
        clearBtn.classList.remove("visible");
        render();
      });
    }

    if (chipsContainer) {
      chipsContainer.addEventListener("click", (e) => {
        if (e.target.matches(".chip-btn")) {
          chipsContainer.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
          e.target.classList.add("active");
          state.squadClass = e.target.dataset.class;
          render();
        }
      });
    }

    viewBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        viewBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        state.squadViewMode = btn.dataset.view;
        if (container) container.style.display = state.squadViewMode === "card" ? "grid" : "none";
        if (tableContainer) tableContainer.style.display = state.squadViewMode === "table" ? "block" : "none";
      });
    });
  }

  /* ==========================================================================
     6. 全校學生名冊即時速查
     ========================================================================== */
  function initRoster() {
    const tbody = document.getElementById("roster-tbody");
    const searchInput = document.getElementById("roster-search-input");
    const clearBtn = document.getElementById("roster-search-clear");
    const chipsContainer = document.getElementById("roster-filter-chips");
    const countLabel = document.getElementById("roster-results-count");
    if (!tbody || !students) return;

    function render() {
      const kw = state.rosterQuery.toLowerCase();
      const filtered = students.filter(s => {
        let matchFilter = true;
        if (state.rosterFilter === "male") matchFilter = s.gender === "男";
        else if (state.rosterFilter === "female") matchFilter = s.gender === "女";
        else if (state.rosterFilter === "leader") matchFilter = s.isLeader;
        else if (state.rosterFilter === "veg") matchFilter = s.isVeg;

        const matchKw = !kw ||
          s.class.toLowerCase().includes(kw) ||
          s.name.toLowerCase().includes(kw) ||
          String(s.seat).includes(kw) ||
          s.tent.toLowerCase().includes(kw) ||
          s.squad.toLowerCase().includes(kw) ||
          s.role.toLowerCase().includes(kw) ||
          s.diet.toLowerCase().includes(kw) ||
          s.teacher.toLowerCase().includes(kw);

        return matchFilter && matchKw;
      });

      if (countLabel) {
        countLabel.textContent = `符合筆數：${filtered.length} 位同學（全校共 106 人）`;
      }

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; padding:24px; color:var(--text-muted);">無符合之學生資料</td></tr>`;
        return;
      }

      tbody.innerHTML = filtered.map((s, idx) => `
        <tr>
          <td>${idx + 1}</td>
          <td><strong>${s.class}</strong></td>
          <td>${s.seat}號</td>
          <td><strong>${s.name}</strong></td>
          <td><span class="badge-pill ${s.gender === '男' ? 'male' : 'female'}">${s.gender}</span></td>
          <td>${s.teacher}</td>
          <td>${s.tent}</td>
          <td>${s.isLeader ? '<span class="badge-pill leader">室長</span>' : '成員'}</td>
          <td>${s.squad}</td>
          <td>${s.role}</td>
          <td>${s.isVeg ? '<span class="badge-pill veg">素食</span>' : '葷食'}</td>
        </tr>
      `).join("");
    }

    render();

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.rosterQuery = e.target.value.trim();
        if (clearBtn) clearBtn.classList.toggle("visible", state.rosterQuery.length > 0);
        render();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        state.rosterQuery = "";
        searchInput.value = "";
        clearBtn.classList.remove("visible");
        render();
      });
    }

    if (chipsContainer) {
      chipsContainer.addEventListener("click", (e) => {
        if (e.target.matches(".chip-btn")) {
          chipsContainer.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
          e.target.classList.add("active");
          state.rosterFilter = e.target.dataset.filter;
          render();
        }
      });
    }
  }

  /* ==========================================================================
     7. 景點與營地導覽
     ========================================================================== */
  function initAttractions() {
    const container = document.getElementById("attractions-content-container");
    if (!container) return;

    const spots = [
      {
        id: "attract-jianshanpi",
        name: "台南柳營尖山埤渡假村",
        tag: "湖光山色 · 專業山訓基地 · 營火晚會草坪",
        img: "assets/img/jianshanpi_2.jpg",
        desc: "尖山埤渡假村座落於台南市柳營區，為台糖公司經營之國家級風景區。環抱碧波浩渺的尖山埤水庫，林木蔥鬱、生態豐富。園區內建置完善的戶外露營場、標準野炊烤肉區、高空垂直垂降塔台、人工抱石攀岩壁、低空PA探索體驗設施與開闊營火晚會大草坪，是全台國中隔宿露營與探索教育最佳場域。",
        features: ["露營區設有獨立衛浴與冷熱水", "高空垂降塔台配備國際級確保系統", "寬闊大草坪專供班呼、班歌與營火晚會"],
        phone: "(06) 623-3888",
        telLink: "tel:066233888",
        mapUrl: "https://maps.google.com/?q=柳營尖山埤渡假村",
        webUrl: "https://www.taisugar.com.tw/chinese/CP.aspx?s=357&n=10433"
      },
      {
        id: "attract-mingjian",
        name: "南投名間親子生態園區",
        tag: "共融生態樂園 · 5米高巨型彩虹溜滑梯",
        img: "assets/img/mingjian_1.jpg",
        desc: "南投縣名間鄉最新打造、佔地達 2.6 公頃的全齡共融式生態公園！全區以繽紛色彩結合綠意自然，最受矚目的地標為高達 5 公尺之巨型彩虹磨石子溜滑梯（設有大型遮陽天幕），兩側具備 25° 與 50° 草坡攀爬網與攀岩拉繩，並規劃長達 74 公尺的高架無障礙空中緩坡步道，可俯瞰心型大草坪。鄰近南投豬事文化園區，是返校前全班奔馳放電與大合影的絕美景點。",
        features: ["5米巨型彩虹磨石子雙軌溜滑梯", "草皮攀爬坡與拉繩挑戰", "心型景觀大草坪與無障礙空中景觀步道"],
        phone: "(049) 222-2106",
        telLink: "tel:0492222106",
        mapUrl: "https://maps.google.com/?q=名間親子生態園區",
        webUrl: "https://travel.nantou.gov.tw/spot/%E5%90%8D%E9%96%93%E8%A6%AA%E5%AD%90%E7%94%9F%E6%85%8B%E5%9C%92%E5%8D%80/"
      }
    ];

    container.innerHTML = `
      <div class="attractions-grid">
        ${spots.map(s => `
          <div class="attraction-card" id="${s.id}">
            <img class="attraction-img" src="${s.img}" alt="${s.name}">
            <div class="attraction-body">
              <div class="attraction-tag">${s.tag}</div>
              <h3 class="attraction-title">${s.name}</h3>
              <p class="attraction-desc">${s.desc}</p>
              <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:6px; padding:10px 12px; font-size:0.82rem; margin-bottom:12px;">
                <b style="color:var(--primary-dark);">亮點設施：</b>
                <ul style="padding-left:16px; margin-top:4px;">
                  ${s.features.map(f => `<li>${f}</li>`).join("")}
                </ul>
              </div>
              <div class="attraction-actions">
                <a href="${s.telLink}" class="quick-btn">📞 撥號</a>
                <a href="${s.mapUrl}" target="_blank" rel="noopener noreferrer" class="quick-btn">🗺️ Google 地圖</a>
                <a href="${s.webUrl}" target="_blank" rel="noopener noreferrer" class="quick-btn" style="background:var(--primary-light);">🌐 官方簡介</a>
              </div>
            </div>
          </div>
        `).join("")}
      </div>
    `;
  }

  /* ==========================================================================
     8. 童軍技能知識卡 (Scout Knowledge Flashcards)
     ========================================================================== */
  function initScoutKnowledgeCards() {
    const container = document.getElementById("scout-knowledge-container");
    if (!container || !teachingGuides.scoutSkills) return;

    const skills = teachingGuides.scoutSkills;
    const camping = teachingGuides.campingBasics;

    const cards = [
      {
        icon: "⛺",
        title: "野營常識 · 帳篷標準搭設六部曲與防風水線",
        summary: "一選平地二鋪布、三推營柱四拱起、五披外帳六拉線！",
        detail: `
          <b>1. 選地整平</b>：挑平坦地勢，清除碎石、硬枝雜物，避開窪地與枯木。<br>
          <b>2. 鋪設地布</b>：地布面積不可超出帳底，四周向內折入防積水雨水倒灌。<br>
          <b>3. 交叉穿柱</b>：兩根長營柱沿對角線穿管，切記<b>以「推」代拉</b>以免脫節卡住。<br>
          <b>4. 拱起立帳</b>：兩人對角同時將營柱頂彎，插銷固定，扣上內帳塑料掛勾。<br>
          <b>5. 披上外帳</b>：對準進出口，綁牢內部魔鬼氈，四角插扣拉緊調平張力。<br>
          <b>6. 打釘拉水線</b>：營釘呈 45°～60° 背對營繩敲入地面，外帳完全拉開，確保內外帳分開不反潮！
        `
      },
      {
        icon: "🔥",
        title: "生火技巧 · 火媒棒製作、三級柴火與野炊米飯秘訣",
        summary: "羽狀木屑引燃、井字柴架均勻受熱、米水比 1:1.1~1.2 與悶飯十五分",
        detail: `
          <b>火媒棒</b>：小刀 45 度角向前輕推，削出層層捲曲薄木屑，極易被火星點燃。<br>
          <b>三級柴火</b>：① 引火柴（乾枯松針、火種）② 助燃柴（小指粗枯枝）③ 燃燒柴（大木塊、耐燒木炭）。<br>
          <b>柴堆構型</b>：井字型通風蓄熱佳（架鍋野炊）；金字塔型向上竄升猛（晚會引火）。<br>
          <b>煮飯四部法</b>：大火煮滾大量冒氣 ➔ 中火收水聞到飯香 ➔ 微火慢煨 ➔ <b>離火加蓋悶飯 15 分鐘</b>，飯粒香Q彈牙！
        `
      },
      {
        icon: "🪖",
        title: "戰術偽裝與定向 · 凸暗凹亮迷彩原則與太陽手錶定向",
        summary: "額頭鼻樑塗暗色、眼窩陰影塗淺綠，打破面部輪廓；時針與12點角平分線為南方",
        detail: `
          <b>凸暗凹亮原則</b>：高光反射處（額頭、鼻樑、顴骨、下巴）塗深色；凹陷陰影處（眼眶、法令、頸部）塗淺綠色，打破面部對稱特徵。<br>
          <b>手錶太陽定向</b>：將指針錶時針指向太陽，時針與表面 12 點刻度夾角之中分線，所指方向即為<b>【正南方】</b>。<br>
          <b>指北針地圖定向</b>：紅色磁針恆指南北，配合刻度盤量測前進方位角。<br>
          <b>自然植被年輪</b>：獨立樹木向南面枝葉茂密，樹樁年輪南面寬疏、北面緊密；北側樹皮易生青苔。
        `
      },
      {
        icon: "🪢",
        title: "出神入化 · 童軍實用八大繩結全攻略",
        summary: "單結防脫、平結等粗、接繩異粗、雙半結固定、營繩結調張力、稱人結繩結之王",
        detail: `
          <b>1. 單結</b>：最基礎繩結，打於繩尾防止脫出滑輪或扣環。<br>
          <b>2. 平結</b>：左壓右右壓左，用於連接兩條<b>等粗</b>繩索，受力牢固好解開。<br>
          <b>3. 接繩結</b>：粗繩成環細繩穿繞，連接兩條<b>粗細不同</b>繩索。<br>
          <b>4. 雙半結</b>：將繩索牢固捆綁在樹幹柱子上，越拉越緊。<br>
          <b>5. 營繩結 (齊來結)</b>：可在繩上滑動調節張力，帳篷拉水線抗風必備。<br>
          <b>6. 稱人結</b>：繩結之王，繩圈受力永不緊縮，高空垂降救援必用。<br>
          <b>7. 雙套結</b>：繞木樁兩圈交叉，搭建先鋒工程旗桿營門起手式。<br>
          <b>8. 十字結</b>：兩垂直木桿緊密十字交叉捆紮，工程支架核心。
        `
      },
      {
        icon: "🐍",
        title: "臺灣六大毒蛇辨識 ＆ 咬傷黃金急救【五要五不】",
        summary: "神經毒（雨傘節/眼鏡蛇）、出血毒（龜殼花/赤尾青竹絲/百步蛇）、混合毒（鎖鏈蛇）",
        detail: `
          <b>六大毒蛇特徵</b>：<br>
          ▶ 雨傘節（神經毒，黑白相間等寬，咬傷無劇痛易呼吸衰竭）<br>
          ▶ 眼鏡蛇（神經/細胞毒，前半身立起膨頸嘶嘶叫）<br>
          ▶ 龜殼花（出血毒，烙鐵三角形頭，傷口腫脹流血不止）<br>
          ▶ 赤尾青竹絲（出血毒，綠身焦紅尾兩側白縱線）<br>
          ▶ 百步蛇（出血毒，頭大吻翹三角形幾何斑紋，排毒量大）<br>
          ▶ 鎖鏈蛇（混合毒，三列鏈狀圓斑，噴氣聲劇烈）。<br><br>
          <b>急救【五要】</b>：要視為毒蛇、要冷靜坐下、要脫戒指飾品、要彈性包紮（鬆緊可插一指，低於心臟）、要記蛇外觀速送醫。<br>
          <b>急救【五不】</b>：不要切開傷口、不要用嘴吸、不要冰敷、不要用止血帶緊勒截肢、不要喝濃茶酒類！
        `
      }
    ];

    container.innerHTML = cards.map(c => `
      <div class="flashcard-box">
        <div class="flashcard-header">
          <span>${c.icon} ${c.title}</span>
          <span class="flashcard-toggle-icon">▼</span>
        </div>
        <div style="font-size:0.82rem; color:var(--text-muted); margin-top:4px;">${c.summary}</div>
        <div class="flashcard-content">${c.detail}</div>
      </div>
    `).join("");

    container.querySelectorAll(".flashcard-box").forEach(box => {
      box.addEventListener("click", () => {
        box.classList.toggle("open");
      });
    });
  }

  /* ==========================================================================
     9. 營火晚會歌詞與動唱
     ========================================================================== */
  function initCampfireLyrics() {
    const container = document.getElementById("campfire-lyrics-container");
    if (!container) return;

    const songs = [
      {
        title: "🔥 神聖迎火儀式 · 拜火詞",
        desc: "引火入場、神聖祈福，全體肅立齊呼震撼營地！",
        lyrics: `「阿給拉～魯巴～魯巴！\n阿給拉～魯巴～魯巴！\n萬能的火神，請賜予南投國中無比的光明、勇氣與友誼！\n熊熊營火，燃燒吧！」`
      },
      {
        title: "🎵 《營火歌》· 經典傳唱",
        desc: "朋友！燃起這營火，照耀著我們的友誼！",
        lyrics: `朋友！燃起這營火，照耀著我們的友誼！\n火花在黑夜裡飛舞，照亮了少年的夢想！\n歌聲在山谷中迴盪，激盪著青春的熱血！\n讓我們手牽著手，圍繞在營火旁，\n唱出心中最美的歌，直到永遠！`
      },
      {
        title: "🥁 《成吉思汗》· 震撼動唱熱舞",
        desc: "全場齊呼！展現南投健兒磅礴氣勢！",
        lyrics: `風沙滾滾，戰馬奔馳，嘿！喝！嘿！喝！\n他是大英雄，天下無敵手！\n成！成！成吉思汗！\n有朝一日，統治天下，名揚四海！\n成！成！成吉思汗！\n南投國中，氣勢如虹，所向無敵！`
      },
      {
        title: "💃 《第一支舞》· 青春浪漫邀舞",
        desc: "帶著笑容，你走向我，做個邀請的動作...",
        lyrics: `帶著笑容，你走向我，做個邀請的動作。\n在這旋轉的舞會中，我們輕輕地擺動。\n請別問我，這是不是夢境，\n今晚的星空特別迷人，難忘的夜晚有你陪著我。\n旋轉，旋轉，在音樂聲中，舞出青春的光芒！`
      },
      {
        title: "🕯️ 《萍聚》· 燭光夜語心靈分享",
        desc: "只要我們曾經擁有過，對你我來講已經足夠...",
        lyrics: `別管以後將如何結束，至少我們曾經相聚過。\n不必費心地彼此約束，更不需要言語的承諾。\n只要我們曾經擁有過，對你我來講已經足夠，\n人的一生有許多回憶，只願你的追憶有個我！`
      },
      {
        title: "🤝 《朋友》· 同窗友誼大合唱",
        desc: "朋友一生一起走，那些日子不再有...",
        lyrics: `朋友一生一起走，那些日子不再有，\n一句話，一輩子，一生情，一杯酒。\n朋友不曾孤單過，一聲朋友你會懂，\n還有傷，還有痛，還要走，還有我！`
      }
    ];

    container.innerHTML = `
      <div style="background:#fff7ed; border:1px solid #ffedd5; border-radius:8px; padding:12px 16px; margin-bottom:16px; font-size:0.88rem; color:#9a3412;">
        <b>💡 晚會精神導引：</b> 營火燃燒的是青春的熱血，燭光映照的是師生最真誠的心聲。各班在隊輔帶領下放開胸懷盡情吶喊，在餘燼中與導師分享成長印記！
      </div>
      ${songs.map(s => `
        <div class="song-card">
          <div class="song-title">${s.title}</div>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:8px;">${s.desc}</div>
          <div class="song-lyrics">${s.lyrics}</div>
        </div>
      `).join("")}
    `;
  }

  /* ==========================================================================
     10. 山訓探索教育專題
     ========================================================================== */
  function initMountainTraining() {
    const container = document.getElementById("mountain-training-container");
    if (!container || !teachingGuides.mountainTraining) return;

    const mt = teachingGuides.mountainTraining;

    container.innerHTML = `
      <div style="display:grid; grid-template-columns:1fr; gap:16px;">
        ${mt.activities.map(act => `
          <div class="data-card" style="border-left:4px solid var(--primary);">
            <div class="data-card-header">
              <h3 style="font-size:1.05rem; font-weight:800; color:var(--primary-dark);">${act.title}</h3>
            </div>
            <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:8px;">${act.desc}</p>
            <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:6px; padding:8px 12px; margin-bottom:10px; font-size:0.82rem;">
              <b style="color:var(--primary-dark);">安全配備：</b> ${act.equip}
            </div>
            <div>
              <b style="font-size:0.85rem; color:var(--text-main);">操作要領與防護重點：</b>
              <ol style="font-size:0.85rem; color:var(--text-muted); line-height:1.6; padding-left:18px; margin-top:4px;">
                ${act.steps.map(s => `<li>${s}</li>`).join("")}
              </ol>
            </div>
          </div>
        `).join("")}
      </div>
    `;
  }

  /* ==========================================================================
     11. 行李打包清單
     ========================================================================== */
  function initChecklist() {
    const container = document.getElementById("checklist-container");
    const progressFill = document.getElementById("progress-fill");
    const progressText = document.getElementById("progress-text");
    const resetBtn = document.getElementById("reset-checklist-btn");
    if (!container || !checklist) return;

    let totalItems = 0;
    checklist.forEach(cat => totalItems += cat.items.length);

    function updateProgress() {
      let checkedCount = 0;
      container.querySelectorAll("input[type='checkbox']").forEach(cb => {
        if (cb.checked) checkedCount++;
      });

      const percent = totalItems > 0 ? Math.round((checkedCount / totalItems) * 100) : 0;
      if (progressText) progressText.textContent = `${checkedCount} / ${totalItems} 項 (${percent}%)`;
      if (progressFill) progressFill.style.width = `${percent}%`;
    }

    container.innerHTML = checklist.map((cat, catIdx) => `
      <div class="checklist-cat-card">
        <div class="checklist-cat-title">📦 ${cat.category}</div>
        <div>
          ${cat.items.map((item, itemIdx) => {
            const key = `c_${catIdx}_${itemIdx}`;
            const isChecked = state.checklistState[key] === true;
            return `
              <label class="check-item ${isChecked ? 'done' : ''}">
                <input type="checkbox" data-key="${key}" ${isChecked ? 'checked' : ''}>
                <span>${item}</span>
              </label>
            `;
          }).join("")}
        </div>
      </div>
    `).join("");

    updateProgress();

    container.addEventListener("change", (e) => {
      if (e.target.matches("input[type='checkbox']")) {
        const cb = e.target;
        const key = cb.dataset.key;
        state.checklistState[key] = cb.checked;
        cb.closest(".check-item").classList.toggle("done", cb.checked);
        localStorage.setItem("ntjh_camp_pack_list_v1", JSON.stringify(state.checklistState));
        updateProgress();
      }
    });

    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        if (confirm("確定要重設所有打包勾選項目嗎？")) {
          state.checklistState = {};
          localStorage.removeItem("ntjh_camp_pack_list_v1");
          container.querySelectorAll("input[type='checkbox']").forEach(cb => {
            cb.checked = false;
            cb.closest(".check-item").classList.remove("done");
          });
          updateProgress();
        }
      });
    }
  }

  /* ==========================================================================
     12. 生活須知與營規
     ========================================================================== */
  function initRules() {
    const container = document.getElementById("notices-content-container");
    if (!container || !rules) return;

    container.innerHTML = `
      <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:12px 16px; margin-bottom:16px;">
        <h3 style="color:#166534; font-size:1.05rem; font-weight:800; margin-bottom:4px;">🏕️ 南投國中二年級隔宿露營生活守則</h3>
        <p style="font-size:0.85rem; color:#15803d;">安全是返家的唯一道路，榮譽是全體南投健兒的共同標竿！</p>
      </div>

      <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:20px;">
        ${rules.map(r => `
          <div class="notice-box">
            ${r}
          </div>
        `).join("")}
      </div>

      <div class="data-card" style="border-left:4px solid #ef4444;">
        <div class="data-card-header">
          <h4 style="color:#b91c1c; font-size:1rem; font-weight:800;">🚑 緊急事故應變與醫療通報網絡</h4>
        </div>
        <div style="font-size:0.88rem; color:var(--text-muted); line-height:1.6;">
          <p>活動期間若遇任何意外傷病、蜂蛇螫咬、中暑暈眩、扭傷或發燒，請依循以下緊急通報程序：</p>
          <ol style="padding-left:20px; margin-top:6px;">
            <li><b>第一時間通報</b>：向同帳室長、小隊長或身旁隊輔教官高聲反映。</li>
            <li><b>導師現場掌握</b>：隨隊各班導師（黃O月、黃O君、林O玟、李O儒、林O銓、許O玉、黃O慧老師）第一時間到場關懷處置。</li>
            <li><b>醫護站即時照護</b>：迅速送至營地醫護站，由隨隊校護實施緊急冰敷、止血或生理檢測。</li>
            <li><b>緊急後送機制</b>：營地備有專屬緊急醫療接駁專車，直通<b>柳營奇美醫院急診中心</b>（台南市柳營區太康里太康201號，電話：06-6226999）。</li>
          </ol>
        </div>
      </div>
    `;
  }

  /* ==========================================================================
     13. 車輛編組與隨車師長團務表 (Bus Schedule)
     ========================================================================== */
  function initBusSchedule() {
    const container = document.getElementById("bus-content-container");
    if (!container || !CAMP_DATA.busSchedule) return;

    const busList = CAMP_DATA.busSchedule;

    container.innerHTML = `
      <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:12px 16px; margin-bottom:16px;">
        <h3 style="color:#1e40af; font-size:1.05rem; font-weight:800; margin-bottom:4px;">🚌 南投國中二年級隔宿露營 遊覽車編組團務表</h3>
        <p style="font-size:0.85rem; color:#2563eb;">全校共編配 4 部遊覽車（1車、2車、3車、丁車），共計 106 位學生（男48/女58，葷105/素1）與 9 位隨車行政及各班導師（男3/女6）。</p>
      </div>

      <!-- 車輛卡片網格 -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-bottom:20px;">
        ${busList.map(b => `
          <div class="data-card" style="border-top:4px solid var(--primary);">
            <div class="data-card-header">
              <div class="data-card-title" style="font-size:1.15rem; color:var(--primary-dark);">🚌 ${b.bus}</div>
              <span class="badge-pill squad">${b.subtotal.total} 人 (男${b.subtotal.male} / 女${b.subtotal.female})</span>
            </div>
            <div style="font-size:0.88rem; line-height:1.6;">
              <div style="margin-bottom:8px;">
                <b style="color:var(--text-main);">乘車班級：</b>
                <div style="margin-top:4px; padding-left:8px; border-left:2px solid #cbd5e1;">
                  ${b.classes.map(c => `
                    <div><strong>${c.class}</strong>：男 ${c.male} 人、女 ${c.female} 人，合計 <strong>${c.total} 人</strong> ${c.veg > 0 ? `<span class="badge-pill veg" style="font-size:0.75rem;">素食 ${c.veg}</span>` : ''}</div>
                  `).join("")}
                </div>
              </div>
              <div style="margin-bottom:8px; background:#f8fafc; padding:8px 10px; border-radius:6px; border:1px solid var(--border);">
                <b style="color:var(--primary-dark);">👨‍🏫 隨車師長 (${b.teachers.length} 位)：</b>
                <div style="color:var(--text-main); font-weight:600; margin-top:2px;">
                  ${b.teachers.join("、")}
                </div>
              </div>
              <div style="font-size:0.8rem; color:var(--text-muted);">
                📌 備註：${b.note}
              </div>
            </div>
          </div>
        `).join("")}
      </div>

      <!-- 依公文格式完整團務總表 -->
      <div class="data-card">
        <div class="data-card-header">
          <h4 style="font-size:1.05rem; font-weight:800; color:var(--text-main);">📋 南投縣立南投國民中學【團務表】官方車次配置總表</h4>
          <button onclick="window.print()" class="quick-btn" style="border:1px solid #cbd5e1; padding:4px 10px; font-size:0.8rem;">🖨️ 列印團務表</button>
        </div>
        <div style="overflow-x:auto;">
          <table class="custom-table" style="margin-top:8px;">
            <thead>
              <tr>
                <th rowspan="2" style="text-align:center; vertical-align:middle;">車次</th>
                <th rowspan="2" style="text-align:center; vertical-align:middle;">班級</th>
                <th colspan="2" style="text-align:center;">人數</th>
                <th rowspan="2" style="text-align:center; vertical-align:middle;">合計</th>
                <th rowspan="2" style="text-align:center; vertical-align:middle;">素食</th>
                <th rowspan="2" style="text-align:left; vertical-align:middle;">隨車師長</th>
              </tr>
              <tr>
                <th style="text-align:center;">男</th>
                <th style="text-align:center;">女</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td rowspan="2" style="text-align:center; font-weight:800; vertical-align:middle;">1車</td>
                <td>205 班</td>
                <td style="text-align:center;">7</td>
                <td style="text-align:center;">4</td>
                <td rowspan="2" style="text-align:center; font-weight:800; vertical-align:middle;">20</td>
                <td rowspan="2" style="text-align:center; font-weight:800; color:#16a34a; vertical-align:middle;">1</td>
                <td rowspan="2" style="vertical-align:middle;">董O遠 (主任)、林O銓 (205導師)、許O玉 (206導師)</td>
              </tr>
              <tr>
                <td>206 班</td>
                <td style="text-align:center;">4</td>
                <td style="text-align:center;">5</td>
              </tr>
              <tr>
                <td rowspan="2" style="text-align:center; font-weight:800; vertical-align:middle;">2車</td>
                <td>202 班</td>
                <td style="text-align:center;">6</td>
                <td style="text-align:center;">12</td>
                <td rowspan="2" style="text-align:center; font-weight:800; vertical-align:middle;">33</td>
                <td rowspan="2" style="text-align:center; vertical-align:middle;">0</td>
                <td rowspan="2" style="vertical-align:middle;">黃O君 (202導師)、李O儒 (204導師)</td>
              </tr>
              <tr>
                <td>204 班</td>
                <td style="text-align:center;">7</td>
                <td style="text-align:center;">8</td>
              </tr>
              <tr>
                <td rowspan="2" style="text-align:center; font-weight:800; vertical-align:middle;">3車</td>
                <td>201 班</td>
                <td style="text-align:center;">10</td>
                <td style="text-align:center;">7</td>
                <td rowspan="2" style="text-align:center; font-weight:800; vertical-align:middle;">32</td>
                <td rowspan="2" style="text-align:center; vertical-align:middle;">0</td>
                <td rowspan="2" style="vertical-align:middle;">黃O月 (201導師)、林O玟 (203導師)</td>
              </tr>
              <tr>
                <td>203 班</td>
                <td style="text-align:center;">6</td>
                <td style="text-align:center;">9</td>
              </tr>
              <tr>
                <td style="text-align:center; font-weight:800;">丁車</td>
                <td>207 班</td>
                <td style="text-align:center;">8</td>
                <td style="text-align:center;">13</td>
                <td style="text-align:center; font-weight:800;">21</td>
                <td style="text-align:center;">0</td>
                <td>姚O勤 (組長)、黃O慧 (207導師)</td>
              </tr>
              <tr style="background:#f1f5f9; font-weight:800;">
                <td colspan="2" style="text-align:center;">全校總計</td>
                <td style="text-align:center;">48</td>
                <td style="text-align:center;">58</td>
                <td style="text-align:center; color:var(--primary-dark);">106</td>
                <td style="text-align:center; color:#16a34a;">1</td>
                <td>隨車師長 9 位（男 3、女 6、素 0）</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 行車安全須知 -->
      <div class="data-card" style="margin-top:14px; border-left:4px solid #f59e0b;">
        <h4 style="color:#b45309; font-weight:800; font-size:0.95rem; margin-bottom:6px;">⚠️ 行車安全重點叮嚀（落實 921 地震公園逃生演練原則）</h4>
        <ul style="font-size:0.85rem; color:var(--text-muted); line-height:1.6; padding-left:18px;">
          <li><b>全程繫好安全帶</b>：車輛發動離校起至抵達目的地，全體人員必須全程繫妥安全帶。</li>
          <li><b>逃生門與走道淨空</b>：遊覽車走道與逃生門前嚴禁堆置背包行李，確保突發狀況迅速疏散。</li>
          <li><b>安全演練與裝備確認</b>：出發前確認車上滅火器（前後各一）、車窗擊破器（至少三具）之確切位置與操作方式。</li>
        </ul>
      </div>
    `;
  }

  /* ==========================================================================
     14. 手冊全文檢視與下載 (Manual Viewer)
     ========================================================================== */
  function initManualViewer() {
    const container = document.getElementById("manual-content-container");
    if (!container || !CAMP_DATA.fullManualMd) return;

    let md = CAMP_DATA.fullManualMd;

    function renderSimpleMd(text) {
      const lines = text.split('\n');
      let html = [];
      let inTable = false;
      let tableRows = [];

      function flushTable() {
        if (!inTable || tableRows.length === 0) return;
        let tHtml = '<table>';
        tableRows.forEach((r, idx) => {
          let cols = r.split('|').map(c => c.trim()).filter((c, i, arr) => i > 0 && i < arr.length - 1);
          if (cols.length === 0) return;
          if (cols.every(c => c.replace(/[\-:\s]/g, '').length === 0)) return;
          let tag = idx === 0 ? 'th' : 'td';
          tHtml += '<tr>' + cols.map(c => `<${tag}>${c}</${tag}>`).join('') + '</tr>';
        });
        tHtml += '</table>';
        html.push(tHtml);
        tableRows = [];
        inTable = false;
      }

      for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        if (line.trim().startsWith('|')) {
          inTable = true;
          tableRows.push(line.trim());
          continue;
        } else if (inTable) {
          flushTable();
        }

        if (line.startsWith('# ')) {
          html.push(`<h1>${line.slice(2)}</h1>`);
        } else if (line.startsWith('## ')) {
          html.push(`<h2>${line.slice(3)}</h2>`);
        } else if (line.startsWith('### ')) {
          html.push(`<h3>${line.slice(4)}</h3>`);
        } else if (line.startsWith('> ')) {
          html.push(`<blockquote>${line.slice(2)}</blockquote>`);
        } else if (line.startsWith('- [ ] ')) {
          html.push(`<div style="margin:4px 0;"><input type="checkbox" disabled> ${line.slice(6)}</div>`);
        } else if (line.startsWith('- ')) {
          html.push(`<li>${line.slice(2)}</li>`);
        } else if (line.trim() === '---') {
          html.push('<hr style="border:none; border-top:1px solid var(--border); margin:18px 0;">');
        } else if (line.trim().length > 0) {
          html.push(`<p style="margin:6px 0;">${line}</p>`);
        }
      }
      flushTable();
      return html.join('');
    }

    container.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
        <div>
          <span class="badge-tag highlight">去個資正式手冊</span>
          <span style="font-size:0.85rem; color:var(--text-muted); margin-left:6px;">檔案：南投國中隔宿手冊-去個資.md</span>
        </div>
        <div style="display:flex; gap:8px;">
          <button id="btn-download-md" class="quick-btn" style="border:1px solid #cbd5e1; padding:6px 12px;">📥 下載 Markdown 檔</button>
          <button onclick="window.print()" class="quick-btn" style="border:1px solid #cbd5e1; padding:6px 12px;">🖨️ 列印全手冊</button>
        </div>
      </div>
      <div class="manual-markdown-box">
        ${renderSimpleMd(md)}
      </div>
    `;

    const dlBtn = document.getElementById("btn-download-md");
    if (dlBtn) {
      dlBtn.addEventListener("click", () => {
        const blob = new Blob([CAMP_DATA.fullManualMd], { type: "text/markdown;charset=utf-8" });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "南投國中115學年度隔宿露營手冊-去個資版.md";
        a.click();
      });
    }
  }
});

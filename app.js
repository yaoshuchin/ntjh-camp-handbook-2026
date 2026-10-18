// ==========================================================================
// 南投國中 115學年度二年級隔宿露營行動手冊 - 互動邏輯 (app.js)
// ==========================================================================

document.addEventListener("DOMContentLoaded", function () {
  if (typeof CAMP_DATA === "undefined") {
    console.error("CAMP_DATA is not loaded!");
    return;
  }

  const { info, classes, itinerary, students, tents, squads, teachingGuides, checklist, rules } = CAMP_DATA;

  // 1. 渲染頂部快速營地卡片
  renderHeroCamps(info.locations);

  // 2. 初始化導航 Tabs 切換
  initTabs();

  // 3. 渲染行程時間軸
  renderItinerary(itinerary);

  // 4. 渲染帳篷速查
  renderTents(tents);

  // 5. 渲染野炊小隊速查
  renderSquads(squads);

  // 6. 渲染全體學生清冊
  renderRoster(students);

  // 7. 渲染野營常識
  renderCampingGuides(teachingGuides.campingBasics);

  // 8. 渲染童軍技能
  renderScoutSkills(teachingGuides.scoutSkills);

  // 9. 渲染山訓探索
  renderMountainGuides(teachingGuides.mountainTraining);

  // 10. 渲染打包清單與進度
  renderChecklist(checklist);

  // 11. 渲染營規公約
  renderRules(rules);
});

// --------------------------------------------------------------------------
// 1. 頂部營地卡片
// --------------------------------------------------------------------------
function renderHeroCamps(locations) {
  const container = document.getElementById("hero-camps-container");
  if (!container || !locations) return;

  container.innerHTML = locations.map(loc => `
    <div class="quick-hotel-card">
      <div class="q-hotel-info">
        <h4>⛺ ${loc.name}</h4>
        <p>${loc.tag}</p>
      </div>
      <div style="display:flex; gap:6px;">
        <a href="${loc.telLink}" class="q-hotel-btn" title="一鍵撥號">
          📞 撥號
        </a>
        <a href="${loc.mapUrl}" target="_blank" rel="noopener" class="q-hotel-btn" style="background:rgba(255,255,255,0.2); color:#fff; border:1px solid rgba(255,255,255,0.4);" title="開啟 Google 地圖">
          🗺️ 地圖
        </a>
      </div>
    </div>
  `).join("");
}

// --------------------------------------------------------------------------
// 2. Tabs 導航切換
// --------------------------------------------------------------------------
function initTabs() {
  const topTabBtns = document.querySelectorAll(".nav-tab-btn");
  const bottomNavItems = document.querySelectorAll(".m-nav-item");
  const panes = document.querySelectorAll(".tab-pane");

  function switchTab(tabId) {
    topTabBtns.forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });

    bottomNavItems.forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });

    panes.forEach(pane => {
      pane.classList.toggle("active", pane.id === `tab-${tabId}`);
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  topTabBtns.forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.getAttribute("data-tab")));
  });

  bottomNavItems.forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.getAttribute("data-tab")));
  });
}

// --------------------------------------------------------------------------
// 3. 行程時間軸
// --------------------------------------------------------------------------
function renderItinerary(itineraryList) {
  const daySelector = document.getElementById("day-selector");
  const timelineContainer = document.getElementById("timeline-container");
  if (!daySelector || !timelineContainer || !itineraryList) return;

  daySelector.innerHTML = itineraryList.map((dayItem, index) => `
    <button class="day-pill-btn ${index === 0 ? 'active' : ''}" data-day-index="${index}">
      <div class="d-title">第 ${dayItem.day} 天</div>
      <div class="d-sub">${dayItem.title.split('・')[0]}</div>
    </button>
  `).join("");

  function showDay(dayIndex) {
    const day = itineraryList[dayIndex];
    document.querySelectorAll(".day-pill-btn").forEach((btn, idx) => {
      btn.classList.toggle("active", idx === dayIndex);
    });

    let mealsHtml = `
      <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:8px; padding:10px 14px; margin-bottom:16px; font-size:13px; display:flex; flex-wrap:wrap; gap:12px;">
        <div><b>🍱 午餐：</b> ${day.meals.lunch}</div>
        <div><b>🍲 晚餐：</b> ${day.meals.dinner}</div>
        <div><b>🥣 宵夜/晨食：</b> ${day.meals.breakfast || day.meals.night}</div>
      </div>
    `;

    let timelineHtml = `
      <div class="timeline-list">
        ${day.timeline.map(item => `
          <div class="timeline-item">
            <div class="timeline-time">${item.time}</div>
            <div class="timeline-activity">${item.title.replace(/\n/g, ' ')}</div>
            <div class="timeline-desc">${item.desc}</div>
          </div>
        `).join("")}
      </div>
    `;

    timelineContainer.innerHTML = mealsHtml + timelineHtml;
  }

  showDay(0);

  daySelector.querySelectorAll(".day-pill-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const idx = parseInt(btn.getAttribute("data-day-index"), 10);
      showDay(idx);
    });
  });
}

// --------------------------------------------------------------------------
// 4. 帳篷住宿速查
// --------------------------------------------------------------------------
function renderTents(tentsList) {
  const container = document.getElementById("tents-cards-container");
  const searchInput = document.getElementById("tent-search-input");
  const chips = document.querySelectorAll("#tent-filter-chips .chip-btn");
  const countLabel = document.getElementById("tent-count-label");
  if (!container || !tentsList) return;

  let currentClass = "all";
  let searchKeyword = "";

  function filterAndRender() {
    const filtered = tentsList.filter(t => {
      const matchClass = (currentClass === "all") || (t.classNum === currentClass);
      const kw = searchKeyword.toLowerCase();
      const matchKeyword = !kw || 
        t.class.toLowerCase().includes(kw) ||
        t.tentName.toLowerCase().includes(kw) ||
        t.leaderName.toLowerCase().includes(kw) ||
        String(t.leaderSeat).includes(kw) ||
        t.members.toLowerCase().includes(kw);
      return matchClass && matchKeyword;
    });

    if (countLabel) {
      countLabel.textContent = `共符合 ${filtered.length} 頂帳篷`;
    }

    if (filtered.length === 0) {
      container.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:30px; color:var(--text-muted);">無符合之帳篷資料</div>`;
      return;
    }

    container.innerHTML = filtered.map(t => `
      <div class="data-card">
        <div class="data-card-header">
          <div class="data-card-title">${t.class} · ${t.tentName}</div>
          <span class="badge-pill ${t.gender.includes('男') ? 'male' : 'female'}">${t.gender} · ${t.count}</span>
        </div>
        <div class="data-card-body">
          <div style="margin-bottom:6px;">
            <span class="badge-pill leader">室長</span>
            <strong>${t.leaderSeat}號 ${t.leaderName}</strong>
          </div>
          <div>
            <b>同帳成員：</b><br>
            <span style="color:var(--text-main);">${t.members}</span>
          </div>
          ${t.notes ? `<div style="margin-top:6px; font-size:11.5px; color:#d97706;">📌 ${t.notes}</div>` : ''}
        </div>
      </div>
    `).join("");
  }

  filterAndRender();

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchKeyword = e.target.value.trim();
      filterAndRender();
    });
  }

  chips.forEach(btn => {
    btn.addEventListener("click", () => {
      chips.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentClass = btn.getAttribute("data-class");
      filterAndRender();
    });
  });
}

// --------------------------------------------------------------------------
// 5. 野炊小隊速查
// --------------------------------------------------------------------------
function renderSquads(squadsList) {
  const container = document.getElementById("squads-cards-container");
  const searchInput = document.getElementById("squad-search-input");
  const chips = document.querySelectorAll("#squad-filter-chips .chip-btn");
  if (!container || !squadsList) return;

  let currentClass = "all";
  let searchKeyword = "";

  function filterAndRender() {
    const filtered = squadsList.filter(s => {
      const matchClass = (currentClass === "all") || (s.classNum === currentClass);
      const kw = searchKeyword.toLowerCase();
      const matchKeyword = !kw || 
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
      return matchClass && matchKeyword;
    });

    if (filtered.length === 0) {
      container.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:30px; color:var(--text-muted);">無符合之小隊資料</div>`;
      return;
    }

    container.innerHTML = filtered.map(s => `
      <div class="data-card">
        <div class="data-card-header">
          <div class="data-card-title">${s.class} · ${s.squadName}</div>
          <span class="badge-pill veg">${s.count}</span>
        </div>
        <div class="data-card-body">
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
  }

  filterAndRender();

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchKeyword = e.target.value.trim();
      filterAndRender();
    });
  }

  chips.forEach(btn => {
    btn.addEventListener("click", () => {
      chips.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentClass = btn.getAttribute("data-class");
      filterAndRender();
    });
  });
}

// --------------------------------------------------------------------------
// 6. 全校學生名冊即時速查
// --------------------------------------------------------------------------
function renderRoster(studentsList) {
  const tbody = document.getElementById("roster-tbody");
  const searchInput = document.getElementById("roster-search-input");
  const chips = document.querySelectorAll("#roster-filter-chips .chip-btn");
  const countLabel = document.getElementById("roster-count-label");
  if (!tbody || !studentsList) return;

  let currentFilter = "all";
  let searchKeyword = "";

  function filterAndRender() {
    const filtered = studentsList.filter(s => {
      let matchFilter = true;
      if (currentFilter === "male") matchFilter = s.gender === "男";
      else if (currentFilter === "female") matchFilter = s.gender === "女";
      else if (currentFilter === "leader") matchFilter = s.isLeader;
      else if (currentFilter === "veg") matchFilter = s.isVeg;

      const kw = searchKeyword.toLowerCase();
      const matchKeyword = !kw ||
        s.class.toLowerCase().includes(kw) ||
        s.name.toLowerCase().includes(kw) ||
        String(s.seat).includes(kw) ||
        s.tent.toLowerCase().includes(kw) ||
        s.squad.toLowerCase().includes(kw) ||
        s.role.toLowerCase().includes(kw) ||
        s.diet.toLowerCase().includes(kw);

      return matchFilter && matchKeyword;
    });

    if (countLabel) {
      countLabel.textContent = `顯示 ${filtered.length} 位同學資料（全校共 106 人）`;
    }

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; padding:24px; color:var(--text-muted);">無符合條件之學生</td></tr>`;
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

  filterAndRender();

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchKeyword = e.target.value.trim();
      filterAndRender();
    });
  }

  chips.forEach(btn => {
    btn.addEventListener("click", () => {
      chips.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.getAttribute("data-filter");
      filterAndRender();
    });
  });
}

// --------------------------------------------------------------------------
// 7. 野營常識教學
// --------------------------------------------------------------------------
function renderCampingGuides(guide) {
  const container = document.getElementById("camping-guides-container");
  if (!container || !guide) return;

  container.innerHTML = `
    <div class="skill-card">
      <div class="skill-card-title">⛺ ${guide.subtitle}</div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:10px; margin-top:10px;">
        ${guide.steps.map(s => `
          <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:8px; padding:10px 12px;">
            <h4 style="font-size:14px; color:var(--primary); margin-bottom:4px;">${s.step}</h4>
            <p style="font-size:12.5px; color:var(--text-muted); line-height:1.5;">${s.desc}</p>
          </div>
        `).join("")}
      </div>
    </div>

    <div class="skill-card">
      <div class="skill-card-title">🧹 帳篷拆卸收整四大要領</div>
      <ul class="skill-list" style="font-size:13px; line-height:1.6; color:var(--text-muted);">
        ${guide.teardown.map(item => `<li>${item}</li>`).join("")}
      </ul>
    </div>

    <div class="skill-card">
      <div class="skill-card-title">🌿 無痕山林 (Leave No Trace, LNT) 七大準則</div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:8px; margin-top:8px;">
        ${guide.lntRules.map(r => `
          <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:6px; padding:8px 12px;">
            <b style="color:var(--primary-dark); font-size:13px;">${r.title}</b>
            <p style="font-size:12px; color:var(--text-muted); margin-top:2px;">${r.desc}</p>
          </div>
        `).join("")}
      </div>
    </div>
  `;
}

// --------------------------------------------------------------------------
// 8. 童軍技能教育
// --------------------------------------------------------------------------
function renderScoutSkills(skills) {
  const container = document.getElementById("scout-skills-container");
  if (!container || !skills) return;

  const secFire = skills.sections.find(s => s.id === "fire_cooking");
  const secCamo = skills.sections.find(s => s.id === "camo_navigation");
  const secKnots = skills.sections.find(s => s.id === "knots");
  const secSnakes = skills.sections.find(s => s.id === "snakes");
  const secCampfire = skills.sections.find(s => s.id === "campfire");

  container.innerHTML = `
    <!-- 生火與烹飪 -->
    <div class="skill-card">
      <div class="skill-card-title">🔥 ${secFire.title}</div>
      <ul class="skill-list" style="font-size:13px; line-height:1.6; color:var(--text-muted);">
        ${secFire.content.map(c => `<li>${c}</li>`).join("")}
      </ul>
    </div>

    <!-- 戰術偽裝與定向 -->
    <div class="skill-card">
      <div class="skill-card-title">🪖 ${secCamo.title}</div>
      <ul class="skill-list" style="font-size:13px; line-height:1.6; color:var(--text-muted);">
        ${secCamo.content.map(c => `<li>${c}</li>`).join("")}
      </ul>
    </div>

    <!-- 實用繩結 -->
    <div class="skill-card">
      <div class="skill-card-title">🪢 ${secKnots.title}</div>
      <div class="table-responsive">
        <table class="custom-table">
          <thead><tr><th>繩結名稱</th><th>主要用途</th><th>功能說明</th></tr></thead>
          <tbody>
            ${secKnots.knotsList.map(k => `
              <tr>
                <td><strong>${k.name}</strong></td>
                <td><span class="badge-pill veg">${k.usage}</span></td>
                <td>${k.desc}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>

    <!-- 六大毒蛇與急救 -->
    <div class="skill-card">
      <div class="skill-card-title">🐍 ${secSnakes.title}</div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:10px; margin-bottom:14px;">
        ${secSnakes.snakesList.map(s => `
          <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:8px; padding:10px 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <b style="font-size:14px; color:var(--text-main);">${s.name}</b>
              <span class="badge-pill ${s.toxin.includes('神經') ? 'male' : 'female'}">${s.toxin}</span>
            </div>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.5;"><b>外觀：</b>${s.feature}</p>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.5;"><b>習性：</b>${s.habit}</p>
          </div>
        `).join("")}
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:12px;">
          <h4 style="color:#15803d; margin-bottom:6px; font-size:14px;">✅ 毒蛇自救【五要】</h4>
          <ul class="skill-list" style="font-size:12px; line-height:1.5; color:#166534;">
            ${secSnakes.aidRules.fiveDo.map(d => `<li>${d}</li>`).join("")}
          </ul>
        </div>
        <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:8px; padding:12px;">
          <h4 style="color:#b91c1c; margin-bottom:6px; font-size:14px;">❌ 毒蛇自救【五不】</h4>
          <ul class="skill-list" style="font-size:12px; line-height:1.5; color:#991b1b;">
            ${secSnakes.aidRules.fiveDont.map(d => `<li>${d}</li>`).join("")}
          </ul>
        </div>
      </div>
    </div>

    <!-- 營火晚會 -->
    <div class="skill-card">
      <div class="skill-card-title">🔥 ${secCampfire.title}</div>
      <ul class="skill-list" style="font-size:13px; line-height:1.6; color:var(--text-muted);">
        ${secCampfire.content.map(c => `<li>${c}</li>`).join("")}
      </ul>
    </div>
  `;
}

// --------------------------------------------------------------------------
// 9. 山訓探索教育
// --------------------------------------------------------------------------
function renderMountainGuides(mt) {
  const container = document.getElementById("mountain-guides-container");
  if (!container || !mt) return;

  container.innerHTML = mt.activities.map(act => `
    <div class="skill-card">
      <div class="skill-card-title">🧗 ${act.title}</div>
      <p style="font-size:13.5px; color:var(--text-muted); margin-bottom:10px;">${act.desc}</p>
      <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:6px; padding:8px 12px; margin-bottom:10px; font-size:12.5px;">
        <b style="color:var(--primary-dark);">必備裝備：</b> ${act.equip}
      </div>
      <div>
        <b style="font-size:13px; color:var(--text-main);">操作步驟與技巧要領：</b>
        <ol class="skill-list" style="font-size:13px; line-height:1.6; color:var(--text-muted);">
          ${act.steps.map(st => `<li>${st}</li>`).join("")}
        </ol>
      </div>
    </div>
  `).join("");
}

// --------------------------------------------------------------------------
// 10. 行李打包清單 (含 LocalStorage 記憶與進度計算)
// --------------------------------------------------------------------------
function renderChecklist(checklistCategories) {
  const container = document.getElementById("checklist-container");
  const progressText = document.getElementById("pack-progress-text");
  const progressBar = document.getElementById("pack-progress-bar");
  const resetBtn = document.getElementById("btn-reset-checklist");
  if (!container || !checklistCategories) return;

  const STORAGE_KEY = "ntjh_camp_checklist_state_v1";
  let savedState = {};
  try {
    savedState = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch (e) {
    savedState = {};
  }

  let totalItems = 0;
  checklistCategories.forEach(cat => totalItems += cat.items.length);

  function updateProgress() {
    let checkedCount = 0;
    container.querySelectorAll("input[type='checkbox']").forEach(cb => {
      if (cb.checked) checkedCount++;
    });

    const percent = totalItems > 0 ? Math.round((checkedCount / totalItems) * 100) : 0;
    if (progressText) progressText.textContent = `${percent}% (${checkedCount}/${totalItems})`;
    if (progressBar) progressBar.style.width = `${percent}%`;
  }

  container.innerHTML = checklistCategories.map((cat, catIdx) => `
    <div class="checklist-category-card">
      <div class="checklist-cat-title">📦 ${cat.category}</div>
      <div class="check-list">
        ${cat.items.map((item, itemIdx) => {
          const key = `c_${catIdx}_${itemIdx}`;
          const isChecked = savedState[key] === true;
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
      const key = cb.getAttribute("data-key");
      savedState[key] = cb.checked;
      cb.closest(".check-item").classList.toggle("done", cb.checked);
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(savedState));
      } catch (err) {}
      updateProgress();
    }
  });

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (confirm("確定要重置所有打包勾選項目嗎？")) {
        savedState = {};
        try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
        container.querySelectorAll("input[type='checkbox']").forEach(cb => {
          cb.checked = false;
          cb.closest(".check-item").classList.remove("done");
        });
        updateProgress();
      }
    });
  }
}

// --------------------------------------------------------------------------
// 11. 營規公約
// --------------------------------------------------------------------------
function renderRules(rulesList) {
  const container = document.getElementById("rules-container");
  if (!container || !rulesList) return;

  container.innerHTML = `
    <div class="skill-card">
      <div class="skill-card-title">📜 南投國中二年級隔宿露營生活守則</div>
      <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
        ${rulesList.map(r => `
          <div style="background:var(--bg-main); border:1px solid var(--border); border-left:4px solid var(--primary); border-radius:6px; padding:10px 14px; font-size:13.5px; color:var(--text-main); line-height:1.6;">
            ${r}
          </div>
        `).join("")}
      </div>
    </div>
  `;
}

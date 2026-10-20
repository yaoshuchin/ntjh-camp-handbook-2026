/**
 * 南投縣立南投國民中學 115學年度 二年級隔宿露營專屬行動手冊
 * 前端核心互動邏輯 (app.js)
 */

document.addEventListener("DOMContentLoaded", () => {
  if (typeof CAMP_DATA === "undefined") {
    console.error("CAMP_DATA is not loaded! Please check data.js.");
    return;
  }

  const { info, classes, buses, students, tents, squads, itinerary, checklist, rules, scoutKnowledge, preCampBriefing, resortSpotGuide, worksheet, selfChecklist } = CAMP_DATA;

  // 1. 初始化狀態管理
  let initialChecklistState = {};
  try {
    initialChecklistState = JSON.parse(localStorage.getItem("ntjh_camp_pack_list_115") || "{}");
  } catch (e) {
    initialChecklistState = {};
  }

  const state = {
    activeTab: "itinerary",
    selectedDay: 1,
    tentQuery: "",
    tentClass: "all",
    tentGender: "all",
    tentView: "card",
    squadQuery: "",
    squadClass: "all",
    squadView: "card",
    rosterQuery: "",
    rosterClass: "all",
    rosterGender: "all",
    rosterDiet: "all",
    checklistState: initialChecklistState
  };

  // 姓名去個資過濾器（第2個字統一寫成 "O"，嚴格保護隱私）
  function pName(obj) {
    if (!obj) return "";
    let str = "";
    if (typeof obj === "string") {
      str = obj;
    } else {
      str = obj.name || obj.realName || "";
    }
    if (str.length <= 1) return str;
    if (str.length === 2) return str[0] + "O";
    return str[0] + "O" + str.slice(2);
  }

  function pMentor(classNum) {
    const c = classes[classNum];
    if (!c) return "";
    let m = c.mentorMasked || c.mentor || "";
    if (m.length <= 1) return m;
    if (m.length === 2) return m[0] + "O";
    return m[0] + "O" + m.slice(2);
  }

  // Toast 提示
  function showToast(msg) {
    let t = document.getElementById("toast-msg");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast-msg";
      t.className = "toast-msg";
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add("show");
    setTimeout(() => {
      t.classList.remove("show");
    }, 2200);
  }

  // 剪貼簿複製
  function copyText(txt, label = "內容") {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(() => {
        showToast(`已複製${label}到剪貼簿！`);
      }).catch(() => {
        fallbackCopy(txt, label);
      });
    } else {
      fallbackCopy(txt, label);
    }
  }

  function fallbackCopy(txt, label) {
    const ta = document.createElement("textarea");
    ta.value = txt;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy");
      showToast(`已複製${label}到剪貼簿！`);
    } catch (e) {
      prompt("請手動選取並複製：", txt);
    }
    document.body.removeChild(ta);
  }

  /* ==========================================================================
     導航切換與子分頁
     ========================================================================== */
  function switchTab(target) {
    if (!target) return;

    // 相容性映射：若外部請求 tents, squads 或 buses，自動導向 camp-groups 並切換子標籤
    let subTarget = null;
    if (target === "tents" || target === "squads" || target === "buses") {
      subTarget = target;
      target = "camp-groups";
    }

    state.activeTab = target;

    // 導航按鈕樣式
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === target);
    });
    document.querySelectorAll(".mobile-nav-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === target);
    });

    // 區塊切換
    document.querySelectorAll(".tab-pane").forEach(pane => {
      const isTarget = pane.id === `tab-${target}`;
      pane.classList.toggle("active", isTarget);
      pane.style.display = isTarget ? "block" : "none";
    });

    // 若有指定的子分頁，同時切換子區塊
    if (subTarget) {
      switchSubpane(subTarget);
    }

    // 捲動至頂部
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function switchSubpane(targetSub) {
    document.querySelectorAll(".groups-subnav-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.subpane === targetSub);
    });

    const subpanes = {
      buses: document.getElementById("subpane-buses"),
      squads: document.getElementById("subpane-squads"),
      tents: document.getElementById("subpane-tents")
    };

    if (targetSub === "all") {
      Object.values(subpanes).forEach(el => {
        if (el) el.style.display = "block";
      });
    } else {
      Object.entries(subpanes).forEach(([key, el]) => {
        if (el) el.style.display = (key === targetSub) ? "block" : "none";
      });
    }
  }

  // 全域綁定方便調用
  window.switchTab = switchTab;
  window.switchSubpane = switchSubpane;

  /* ==========================================================================
     1. 渲染頂部快捷卡片
     ========================================================================== */
  function renderHero() {
    const container = document.getElementById("hero-quick-actions");
    if (!container) return;

    container.innerHTML = `
      <a href="${info.campLocation.telLink}" class="quick-call-card" title="撥打電話至尖山埤營地">
        <div class="quick-call-left">
          <span class="quick-call-icon">⛺</span>
          <div>
            <div class="quick-call-name">尖山埤露營渡假村</div>
            <div class="quick-call-phone">${info.campLocation.phone}</div>
          </div>
        </div>
        <span class="quick-call-btn">📞 一鍵撥號</span>
      </a>

      <a href="${info.manager.telLink}" class="quick-call-card" title="撥打電話給旅行社團控經理">
        <div class="quick-call-left">
          <span class="quick-call-icon">👔</span>
          <div>
            <div class="quick-call-name">團控經理 ${pName(info.manager.name)}</div>
            <div class="quick-call-phone">${info.manager.phone}</div>
          </div>
        </div>
        <span class="quick-call-btn">📞 緊急聯絡</span>
      </a>

      <a href="${info.campLocation.mapUrl}" target="_blank" rel="noopener" class="quick-call-card" title="開啟尖山埤營地地圖導航">
        <div class="quick-call-left">
          <span class="quick-call-icon">📍</span>
          <div>
            <div class="quick-call-name">台南尖山埤營區地圖</div>
            <div class="quick-call-phone">台南市柳營區旭山里60號</div>
          </div>
        </div>
        <span class="quick-call-btn" style="background:#2563eb;">🗺️ 地圖導航</span>
      </a>
    `;
  }

  /* ==========================================================================
     2. 兩日行程時間軸
     ========================================================================== */
  function renderItinerary() {
    const daySwitchContainer = document.getElementById("day-switch-container");
    const contentContainer = document.getElementById("itinerary-content-container");
    if (!daySwitchContainer || !contentContainer) return;

    daySwitchContainer.innerHTML = itinerary.map(d => `
      <div class="day-switch-btn ${d.day === state.selectedDay ? 'active' : ''}" data-day="${d.day}">
        <span class="day-num">第 ${d.day} 天</span>
        <div class="day-date">${d.date.split(' ')[0]}</div>
        <div class="day-summary">${d.title.split('：')[1]}</div>
      </div>
    `).join("");

    const curDayData = itinerary.find(d => d.day === state.selectedDay) || itinerary[0];

    contentContainer.innerHTML = `
      <div class="timeline">
        ${curDayData.events.map((ev, idx) => `
          <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-card">
              <div class="timeline-header">
                <span class="timeline-time">⏰ ${ev.time}</span>
                <span class="meta-pill primary">${ev.title}</span>
              </div>
              <div class="timeline-loc">📍 地點：${ev.location}</div>
              <div class="timeline-desc">${ev.desc}</div>
              <div class="timeline-keypoint">💡 <strong>重點提醒：</strong>${ev.keyPoint}</div>
            </div>
          </div>
        `).join("")}
      </div>
    `;

    daySwitchContainer.querySelectorAll(".day-switch-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        state.selectedDay = parseInt(btn.dataset.day);
        renderItinerary();
      });
    });
  }

  /* ==========================================================================
     3. 帳篷住宿速查
     ========================================================================== */
  function renderTents() {
    const listContainer = document.getElementById("tents-list-container");
    const countBadge = document.getElementById("tents-count-badge");
    if (!listContainer) return;

    const q = state.tentQuery.trim().toLowerCase();
    const cFilter = state.tentClass;
    const gFilter = state.tentGender;

    const filtered = tents.filter(t => {
      if (cFilter !== "all" && t.classNum !== cFilter) return false;
      if (gFilter !== "all" && t.gender !== gFilter) return false;
      if (!q) return true;

      // 搜尋帳號
      if (t.tentId.toLowerCase().includes(q)) return true;
      if (t.className.toLowerCase().includes(q) || t.classNum.includes(q)) return true;
      // 搜尋帳員姓名
      const hasMember = t.members.some(m => 
        m.realName.toLowerCase().includes(q) || 
        m.name.toLowerCase().includes(q) ||
        String(m.seat).includes(q)
      );
      return hasMember;
    });

    if (countBadge) {
      countBadge.textContent = `共 ${filtered.length} 頂帳篷`;
    }

    if (filtered.length === 0) {
      listContainer.innerHTML = `
        <div style="text-align:center; padding:40px 16px; color:var(--text-muted); background:var(--bg-card); border-radius:var(--radius-md); border:1px solid var(--border);">
          <div style="font-size:2rem; margin-bottom:8px;">⛺🔍</div>
          <div>找不到符合條件的帳篷！請嘗試其他關鍵字或篩選標籤。</div>
        </div>
      `;
      return;
    }

    if (state.tentView === "card") {
      listContainer.className = "cards-grid";
      listContainer.innerHTML = filtered.map(t => {
        const isMale = t.gender === "男";
        return `
          <div class="tent-card ${isMale ? 'male' : 'female'}">
            <div class="card-top">
              <span class="card-id-badge">${isMale ? '🏕️' : '⛺'} ${t.tentId} 帳</span>
              <div class="card-meta-tags">
                <span class="meta-pill primary">${t.className}</span>
                <span class="meta-pill">${t.genderLabel}</span>
                <span class="meta-pill accent">${t.bus}</span>
                <span class="meta-pill">${t.count}人</span>
              </div>
            </div>

            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:8px;">
              導師：${pMentor(t.classNum)} 老師
            </div>

            <div class="member-chips-wrap">
              ${t.members.map(m => `
                <div class="member-chip ${m.isLeader ? 'leader' : ''} ${m.isVeg ? 'veg' : ''}">
                  <span class="seat-num">${m.seat}號</span>
                  <span class="member-name">${pName(m)}</span>
                  ${m.isLeader ? '<span class="role-tag" style="background:#fef08a; color:#854d0e;">👑室長</span>' : ''}
                  ${m.isVeg ? '<span class="role-tag" style="background:#bbf7d0; color:#166534;">素</span>' : ''}
                </div>
              `).join("")}
            </div>

            <div class="card-footer">
              <span>室長：<strong>${t.leader ? pName(t.leader) : '未指定'}</strong></span>
              <button class="copy-mini-btn" data-copy-tent="${t.tentId}">📋 複製名冊</button>
            </div>
          </div>
        `;
      }).join("");

      // 綁定複製事件
      listContainer.querySelectorAll("[data-copy-tent]").forEach(btn => {
        btn.addEventListener("click", () => {
          const tId = btn.dataset.copyTent;
          const target = tents.find(item => item.tentId === tId);
          if (target) {
            const lines = target.members.map(m => `${m.seat}號 ${pName(m)} ${m.isLeader ? '(室長)' : ''}`).join("、");
            const copyStr = `【南投國中115隔宿露營 帳號：${target.tentId}】(${target.className} ${target.genderLabel}，${target.count}人)\n成員：${lines}\n導師：${pMentor(target.classNum)}`;
            copyText(copyStr, `${tId} 帳名冊`);
          }
        });
      });
    } else {
      // 表格檢視
      listContainer.className = "table-responsive";
      listContainer.innerHTML = `
        <table class="styled-table">
          <thead>
            <tr>
              <th>帳號</th>
              <th>班級</th>
              <th>性別</th>
              <th>車次</th>
              <th>人數</th>
              <th>室長</th>
              <th>全體帳員名冊 (座號 姓名)</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${filtered.map(t => `
              <tr>
                <td><strong>${t.tentId}</strong></td>
                <td>${t.className}</td>
                <td>${t.genderLabel}</td>
                <td>${t.bus}</td>
                <td>${t.count} 人</td>
                <td><strong style="color:var(--primary);">${t.leader ? pName(t.leader) : '-'}</strong></td>
                <td>${t.members.map(m => `${m.seat}號 ${pName(m)}${m.isLeader ? ' ⭐' : ''}${m.isVeg ? ' (素)' : ''}`).join('、')}</td>
                <td><button class="copy-mini-btn" data-copy-tent="${t.tentId}">複製</button></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;

      listContainer.querySelectorAll("[data-copy-tent]").forEach(btn => {
        btn.addEventListener("click", () => {
          const tId = btn.dataset.copyTent;
          const target = tents.find(item => item.tentId === tId);
          if (target) {
            const lines = target.members.map(m => `${m.seat}號 ${pName(m)}`).join("、");
            copyText(`帳號 ${target.tentId}：${lines}`, `${tId} 帳名冊`);
          }
        });
      });
    }
  }

  /* ==========================================================================
     4. 野炊小隊速查
     ========================================================================== */
  function renderSquads() {
    const listContainer = document.getElementById("squads-list-container");
    const countBadge = document.getElementById("squads-count-badge");
    if (!listContainer) return;

    const q = state.squadQuery.trim().toLowerCase();
    const cFilter = state.squadClass;

    const filtered = squads.filter(sq => {
      if (cFilter !== "all" && sq.classNum !== cFilter) return false;
      if (!q) return true;

      if (sq.squadName.toLowerCase().includes(q) || String(sq.squadId).includes(q)) return true;
      if (sq.className.toLowerCase().includes(q) || sq.classNum.includes(q)) return true;
      const hasMember = sq.members.some(m => 
        m.realName.toLowerCase().includes(q) || 
        m.name.toLowerCase().includes(q) ||
        String(m.seat).includes(q) ||
        (m.role && m.role.toLowerCase().includes(q))
      );
      return hasMember;
    });

    if (countBadge) {
      countBadge.textContent = `共 ${filtered.length} 個野炊小隊`;
    }

    if (filtered.length === 0) {
      listContainer.innerHTML = `
        <div style="text-align:center; padding:40px 16px; color:var(--text-muted); background:var(--bg-card); border-radius:var(--radius-md); border:1px solid var(--border);">
          <div style="font-size:2rem; margin-bottom:8px;">🍳🔍</div>
          <div>找不到符合條件的野炊小隊！請更換搜尋詞或重設篩選。</div>
        </div>
      `;
      return;
    }

    if (state.squadView === "card") {
      listContainer.className = "cards-grid";
      listContainer.innerHTML = filtered.map(sq => {
        return `
          <div class="squad-card">
            <div class="card-top">
              <span class="card-id-badge">🍳 ${sq.squadName}</span>
              <div class="card-meta-tags">
                <span class="meta-pill primary">${sq.className}</span>
                <span class="meta-pill accent">${sq.bus}</span>
                <span class="meta-pill">${sq.count}人</span>
                ${sq.hasVeg ? '<span class="meta-pill" style="background:#dcfce7; color:#15803d; border-color:#86efac;">含素食</span>' : ''}
              </div>
            </div>

            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:8px;">
              導師：${pMentor(sq.classNum)} 老師 ｜ ${sq.vegNote}
            </div>

            <div class="member-chips-wrap">
              ${sq.members.map(m => `
                <div class="member-chip ${m.isVeg ? 'veg' : ''}">
                  <span class="seat-num">${m.seat}號</span>
                  <span class="member-name">${pName(m)}</span>
                  ${m.role ? `<span class="role-tag">${m.role}</span>` : ''}
                  ${m.isVeg ? '<span class="role-tag" style="background:#bbf7d0; color:#166534;">素</span>' : ''}
                </div>
              `).join("")}
            </div>

            <div class="card-footer">
              <span>小隊長：<strong>${sq.officers.leader ? pName(sq.officers.leader) : '未指定'}</strong></span>
              <button class="copy-mini-btn" data-copy-squad="${sq.squadId}">📋 複製分組</button>
            </div>
          </div>
        `;
      }).join("");

      listContainer.querySelectorAll("[data-copy-squad]").forEach(btn => {
        btn.addEventListener("click", () => {
          const sqId = parseInt(btn.dataset.copySquad);
          const target = squads.find(item => item.squadId === sqId);
          if (target) {
            const lines = target.members.map(m => `${m.seat}號 ${pName(m)} (${m.role || '組員'})`).join("、");
            const copyStr = `【南投國中115隔宿露營 野炊${target.squadName}】(${target.className}，${target.count}人)\n組員分工：${lines}\n導師：${pMentor(target.classNum)}`;
            copyText(copyStr, `${target.squadName}名單`);
          }
        });
      });
    } else {
      listContainer.className = "table-responsive";
      listContainer.innerHTML = `
        <table class="styled-table">
          <thead>
            <tr>
              <th>組別</th>
              <th>班級</th>
              <th>車次</th>
              <th>人數</th>
              <th>小隊長</th>
              <th>大廚 / 二廚</th>
              <th>全體組員及分工職掌</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${filtered.map(sq => `
              <tr>
                <td><strong>${sq.squadName}</strong></td>
                <td>${sq.className}</td>
                <td>${sq.bus}</td>
                <td>${sq.count} 人</td>
                <td><strong style="color:var(--accent-dark);">${sq.officers.leader ? pName(sq.officers.leader) : '-'}</strong></td>
                <td>${sq.officers.chef1 ? pName(sq.officers.chef1) : '-'} / ${sq.officers.chef2 ? pName(sq.officers.chef2) : '-'}</td>
                <td>${sq.members.map(m => `${m.seat}號 ${pName(m)}${m.role ? ' [' + m.role + ']' : ''}${m.isVeg ? ' (素)' : ''}`).join('、')}</td>
                <td><button class="copy-mini-btn" data-copy-squad="${sq.squadId}">複製</button></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;

      listContainer.querySelectorAll("[data-copy-squad]").forEach(btn => {
        btn.addEventListener("click", () => {
          const sqId = parseInt(btn.dataset.copySquad);
          const target = squads.find(item => item.squadId === sqId);
          if (target) {
            const lines = target.members.map(m => `${m.seat}號 ${pName(m)}`).join("、");
            copyText(`野炊 ${target.squadName}：${lines}`, `${target.squadName}名冊`);
          }
        });
      });
    }
  }

  /* ==========================================================================
     5. 全校學生名冊速查
     ========================================================================== */
  function renderRoster() {
    const listContainer = document.getElementById("roster-list-container");
    const countBadge = document.getElementById("roster-count-badge");
    if (!listContainer) return;

    const q = state.rosterQuery.trim().toLowerCase();
    const cFilter = state.rosterClass;
    const gFilter = state.rosterGender;
    const dFilter = state.rosterDiet;

    const filtered = students.filter(st => {
      if (cFilter !== "all" && st.classNum !== cFilter) return false;
      if (gFilter !== "all" && st.gender !== gFilter) return false;
      if (dFilter === "veg" && !st.isVeg) return false;
      if (dFilter === "meat" && st.isVeg) return false;

      if (!q) return true;
      if (st.realName.toLowerCase().includes(q) || st.name.toLowerCase().includes(q)) return true;
      if (String(st.seat).includes(q)) return true;
      if (st.classNum.includes(q) || st.className.includes(q)) return true;
      if (st.tentId.toLowerCase().includes(q)) return true;
      if (st.squadName.toLowerCase().includes(q) || String(st.squadId).includes(q)) return true;
      if (st.role.toLowerCase().includes(q)) return true;
      return false;
    });

    if (countBadge) {
      countBadge.textContent = `共 ${filtered.length} 位同學`;
    }

    if (filtered.length === 0) {
      listContainer.innerHTML = `
        <div style="text-align:center; padding:40px 16px; color:var(--text-muted); background:var(--bg-card); border-radius:var(--radius-md); border:1px solid var(--border);">
          <div style="font-size:2rem; margin-bottom:8px;">🔍</div>
          <div>查無符合學生資料，請嘗試其他搜尋詞或重設篩選！</div>
        </div>
      `;
      return;
    }

    listContainer.className = "table-responsive";
    listContainer.innerHTML = `
      <table class="styled-table">
        <thead>
          <tr>
            <th>班級</th>
            <th>座號</th>
            <th>姓名</th>
            <th>性別</th>
            <th>車次</th>
            <th>帳號</th>
            <th>野炊組別</th>
            <th>野炊分工職掌</th>
            <th>飲食習慣</th>
          </tr>
        </thead>
        <tbody>
          ${filtered.map(st => `
            <tr>
              <td><strong>${st.className}</strong></td>
              <td>${st.seat} 號</td>
              <td><strong>${pName(st)}</strong> ${st.isLeader ? '<span class="role-tag" style="background:#fef08a; color:#854d0e;">👑室長</span>' : ''}</td>
              <td>${st.gender}</td>
              <td><span class="meta-pill accent">${st.bus}</span></td>
              <td><span class="meta-pill ${st.gender === '男' ? 'primary' : 'accent'}">${st.tentId}</span></td>
              <td><span class="meta-pill">${st.squadName}</span></td>
              <td>${st.role || '組員'}</td>
              <td>${st.isVeg ? '<strong style="color:#16a34a;">素食</strong>' : '葷食'}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;
  }

  /* ==========================================================================
     6. 遊覽車編組與師長團務
     ========================================================================== */
  function renderBuses() {
    const container = document.getElementById("buses-content-container");
    if (!container) return;

    container.innerHTML = buses.map(bus => `
      <div class="info-card" style="margin-bottom:16px;">
        <div class="card-top">
          <span class="card-id-badge" style="background:#e0f2fe; color:#0369a1;">🚌 ${bus.busTitle}</span>
          <div class="card-meta-tags">
            ${bus.classes.map(c => `<span class="meta-pill primary">${c}</span>`).join("")}
            <span class="meta-pill accent">學生共 ${bus.studentCounts.total} 人 (男${bus.studentCounts.male}/女${bus.studentCounts.female})</span>
          </div>
        </div>

        <div style="margin-bottom:12px; background:var(--bg-subtle); padding:10px 14px; border-radius:var(--radius-sm);">
          <strong style="color:var(--text-primary); font-size:0.86rem;">隨車行政與導師：</strong>
          <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:4px;">
            ${bus.staff.map(sf => `
              <span class="meta-pill" style="background:#fff; border:1px solid var(--border);">
                👔 ${sf.title}：<strong>${pName(sf)}</strong>
              </span>
            `).join("")}
          </div>
        </div>

        <div>
          <strong style="font-size:0.84rem; color:var(--text-secondary); display:block; margin-bottom:6px;">搭乘學生名冊：</strong>
          <div class="member-chips-wrap">
            ${bus.students.map(st => `
              <div class="member-chip ${st.gender === '男' ? '' : 'veg'}">
                <span class="seat-num">${st.className.split(' ')[0]}-${st.seat}號</span>
                <span class="member-name">${pName(st)}</span>
                <span style="font-size:0.7rem; color:var(--text-muted);">${st.tentId}</span>
              </div>
            `).join("")}
          </div>
        </div>
      </div>
    `).join("");
  }

  /* ==========================================================================
     7. 行李清單 (LocalStorage 記憶)
     ========================================================================== */
  function renderChecklist() {
    const listContainer = document.getElementById("checklist-container");
    const progressFill = document.getElementById("pack-progress-fill");
    const progressPercent = document.getElementById("pack-progress-percent");
    const progressText = document.getElementById("pack-progress-text");
    if (!listContainer) return;

    const total = checklist.length;
    let checkedCount = 0;

    // 分類群組
    const categories = {};
    checklist.forEach(item => {
      if (!categories[item.category]) categories[item.category] = [];
      categories[item.category].push(item);
      if (state.checklistState[item.id]) checkedCount++;
    });

    const percent = total > 0 ? Math.round((checkedCount / total) * 100) : 0;
    if (progressFill) progressFill.style.width = `${percent}%`;
    if (progressPercent) progressPercent.textContent = `${percent}%`;
    if (progressText) progressText.textContent = `已完成 ${checkedCount} / ${total} 項必備行前裝備`;

    listContainer.innerHTML = Object.keys(categories).map(catName => {
      const items = categories[catName];
      return `
        <div class="checklist-group">
          <div class="checklist-cat-title">📁 ${catName}</div>
          ${items.map(it => {
            const isChecked = !!state.checklistState[it.id];
            return `
              <div class="checklist-item ${isChecked ? 'checked' : ''}" data-item-id="${it.id}">
                <input type="checkbox" class="checklist-cb" ${isChecked ? 'checked' : ''} data-item-id="${it.id}">
                <span style="font-size:1.25rem;">${it.icon}</span>
                <div class="item-content">
                  <div class="item-name">
                    ${it.name}
                    ${it.required ? '<span class="badge-required">必備</span>' : ''}
                  </div>
                  <div class="item-desc">${it.desc}</div>
                </div>
              </div>
            `;
          }).join("")}
        </div>
      `;
    }).join("");

    // 點擊項目觸發打勾
    listContainer.querySelectorAll(".checklist-item").forEach(el => {
      el.addEventListener("click", (e) => {
        const id = el.dataset.itemId;
        state.checklistState[id] = !state.checklistState[id];
        try {
          localStorage.setItem("ntjh_camp_pack_list_115", JSON.stringify(state.checklistState));
        } catch (err) {}
        renderChecklist();
      });
    });

    // 重設按鈕
    const resetBtn = document.getElementById("reset-checklist-btn");
    if (resetBtn) {
      resetBtn.onclick = () => {
        if (confirm("確定要重設所有行李勾選進度嗎？")) {
          state.checklistState = {};
          localStorage.removeItem("ntjh_camp_pack_list_115");
          renderChecklist();
          showToast("已重設行李清單！");
        }
      };
    }
  }

  /* ==========================================================================
     8. 童軍技能指引
     ========================================================================== */
  function renderScout() {
    const container = document.getElementById("scout-content-container");
    if (!container) return;

    container.innerHTML = `
      <div style="margin-bottom:14px; background:linear-gradient(135deg, #e0e7ff 0%, #ede9fe 100%); border:1px solid #c7d2fe; border-radius:var(--radius-md); padding:12px 16px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-size:1.5rem;">🌓</span>
          <div>
            <strong style="color:#3730a3; font-size:0.95rem; display:block;">自然方向辨識 · 數位互動教具：月相模擬器</strong>
            <span style="font-size:0.78rem; color:#4338ca;">立體觀測日月地空間相對位置與月相盈虧週期，掌握野外夜間辨位技巧</span>
          </div>
        </div>
        <a href="https://gemini.google.com/share/90fe02a031a5?social_preview=false&skid=498c1de2-4192-4fb7-9b14-92d3a058c761" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:6px; font-size:0.82rem; background:#4f46e5; color:#fff; padding:6px 14px; border-radius:var(--radius-full); text-decoration:none; font-weight:700; box-shadow:0 2px 6px rgba(79,70,229,0.25);">
          🌓 開啟月相模擬器 ↗
        </a>
      </div>
    ` + scoutKnowledge.map((sec, idx) => `
      <div class="accordion-item ${idx === 0 ? 'open' : ''}">
        <div class="accordion-header">
          <span>${sec.icon} ${sec.category}</span>
          <span class="accordion-arrow">▼</span>
        </div>
        <div class="accordion-content">
          <p style="margin-bottom:10px; color:var(--text-secondary); line-height:1.6;">${sec.desc || ''}</p>

          ${sec.image ? `
            <div style="margin:12px 0 16px; text-align:center; background:var(--bg-main); border:1px solid var(--border); border-radius:var(--radius-md); padding:10px;">
              <img src="${sec.image}" alt="${sec.category}" style="max-width:100%; max-height:280px; object-fit:contain; border-radius:var(--radius-sm); display:block; margin:0 auto; box-shadow:var(--shadow-sm);" loading="lazy">
              ${sec.imageCaption ? `<div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px; font-weight:600;">📷 ${sec.imageCaption}</div>` : ''}
            </div>
          ` : ''}

          ${sec.stepImages ? `
            <h4 style="margin:14px 0 8px; color:var(--primary);">⛺ 屋式帳搭設分解步驟（每步附圖）：</h4>
            <div class="cards-grid" style="grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; margin-bottom:14px;">
              ${sec.stepImages.map(st => `
                <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); overflow:hidden; display:flex; flex-direction:column;">
                  <img src="${st.image}" alt="${st.title}" style="width:100%; height:140px; object-fit:cover; background:#fff; border-bottom:1px solid var(--border);" loading="lazy">
                  <div style="padding:10px; flex:1;">
                    <strong style="color:var(--primary); font-size:0.88rem; display:block; margin-bottom:4px;">${st.title}</strong>
                    <p style="font-size:0.78rem; color:var(--text-secondary); line-height:1.45; margin:0;">${st.desc}</p>
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${sec.tentPitchSteps ? `
            <h4 style="margin-bottom:6px; color:var(--primary);">⛺ 屋式帳搭設步驟總結：</h4>
            <ol class="guide-step-list">
              ${sec.tentPitchSteps.map(s => `<li>${s}</li>`).join("")}
            </ol>
            <div class="mnemonic-box">
              <strong>🗣️ 搭帳口訣：</strong>${sec.mnemonics.pitch}<br>
              <strong>🗣️ 收外帳口訣：</strong>${sec.mnemonics.pack}<br>
              <strong>☀️ 曬帳技巧：</strong>${sec.mnemonics.sunTents}
            </div>
          ` : ''}

          ${sec.knots ? `
            <h4 style="margin:14px 0 8px; color:var(--primary);">🪢 八大繩結（每種皆附圖解與教學影片）：</h4>
            <div class="cards-grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
              ${sec.knots.map(k => `
                <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); overflow:hidden; display:flex; flex-direction:column;">
                  <img src="${k.image}" alt="${k.name}" style="width:100%; height:160px; object-fit:contain; background:#fff; padding:6px; border-bottom:1px solid var(--border);" loading="lazy">
                  <div style="padding:10px; flex:1; display:flex; flex-direction:column;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                      <strong style="color:var(--primary); font-size:0.92rem;">🪢 ${k.name}</strong>
                      <span style="font-size:0.72rem; background:rgba(34,197,94,0.15); color:var(--primary); padding:1px 6px; border-radius:4px; font-weight:700;">${k.type}</span>
                    </div>
                    <p style="font-size:0.78rem; color:var(--text-secondary); line-height:1.45; margin-bottom:8px; flex:1;">${k.desc}</p>
                    ${k.video ? `
                      <a href="${k.video.url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:4px; font-size:0.76rem; background:#fff; color:#dc2626; border:1px solid #fca5a5; padding:3px 8px; border-radius:var(--radius-full); text-decoration:none; font-weight:600; width:fit-content;">
                        🎬 ${k.video.title} ↗
                      </a>
                    ` : ''}
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${sec.methods ? `
            <h4 style="margin:14px 0 8px; color:var(--accent-dark);">🧭 自然方向辨識（每種皆附圖解與教學影片）：</h4>
            <div class="cards-grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
              ${sec.methods.map(m => `
                <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); overflow:hidden; display:flex; flex-direction:column;">
                  <img src="${m.image}" alt="${m.name}" style="width:100%; height:160px; object-fit:contain; background:#fff; padding:4px; border-bottom:1px solid var(--border);" loading="lazy">
                  <div style="padding:10px; flex:1; display:flex; flex-direction:column;">
                    <strong style="color:var(--accent-dark); font-size:0.92rem; margin-bottom:4px;">🧭 ${m.name}</strong>
                    <p style="font-size:0.78rem; color:var(--text-secondary); line-height:1.45; margin-bottom:8px; flex:1;">${m.desc}</p>
                    <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:auto;">
                      ${m.video ? `
                        <a href="${m.video.url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:4px; font-size:0.76rem; background:#fff; color:#dc2626; border:1px solid #fca5a5; padding:3px 8px; border-radius:var(--radius-full); text-decoration:none; font-weight:600; width:fit-content;">
                          🎬 ${m.video.title} ↗
                        </a>
                      ` : ''}
                      ${m.simUrl ? `
                        <a href="${m.simUrl}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:4px; font-size:0.76rem; background:#4f46e5; color:#ffffff; border:1px solid #6366f1; padding:3px 10px; border-radius:var(--radius-full); text-decoration:none; font-weight:700; width:fit-content;">
                          🌓 ${m.simTitle || '月相模擬器'} ↗
                        </a>
                      ` : ''}
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${sec.firstAid ? `
            <h4 style="margin:14px 0 8px; color:#b91c1c;">🩹 野外簡易急救處置（每種皆附圖解與教學影片）：</h4>
            <div class="cards-grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
              ${sec.firstAid.map(fa => `
                <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); overflow:hidden; display:flex; flex-direction:column;">
                  <img src="${fa.image}" alt="${fa.title}" style="width:100%; height:160px; object-fit:contain; background:#fff; padding:4px; border-bottom:1px solid var(--border);" loading="lazy">
                  <div style="padding:10px; flex:1; display:flex; flex-direction:column;">
                    <strong style="color:#b91c1c; font-size:0.92rem; margin-bottom:4px;">🩹 ${fa.title}</strong>
                    <p style="font-size:0.78rem; color:var(--text-secondary); line-height:1.45; margin-bottom:8px; flex:1; white-space:pre-line;">${fa.desc}</p>
                    ${fa.video ? `
                      <a href="${fa.video.url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:4px; font-size:0.76rem; background:#fff; color:#dc2626; border:1px solid #fca5a5; padding:3px 8px; border-radius:var(--radius-full); text-decoration:none; font-weight:600; width:fit-content;">
                        🎬 ${fa.video.title} ↗
                      </a>
                    ` : ''}
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${sec.snakes ? `
            <h4 style="margin:14px 0 8px; color:#991b1b;">🐍 臺灣四大毒蛇生態辨識（每種皆附圖解與教學影片）：</h4>
            <div class="cards-grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px; margin-bottom:14px;">
              ${sec.snakes.map(sn => `
                <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); overflow:hidden; display:flex; flex-direction:column;">
                  <img src="${sn.image}" alt="${sn.name}" style="width:100%; height:160px; object-fit:contain; background:#fff; padding:4px; border-bottom:1px solid var(--border);" loading="lazy">
                  <div style="padding:10px; flex:1; display:flex; flex-direction:column;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                      <strong style="color:#991b1b; font-size:0.9rem;">🐍 ${sn.name}</strong>
                      <span style="font-size:0.72rem; background:#fee2e2; color:#991b1b; padding:1px 6px; border-radius:4px; font-weight:700;">${sn.venom}</span>
                    </div>
                    <p style="font-size:0.78rem; color:var(--text-secondary); line-height:1.45; margin-bottom:8px; flex:1;">${sn.desc}</p>
                    ${sn.video ? `
                      <a href="${sn.video.url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:4px; font-size:0.76rem; background:#fff; color:#dc2626; border:1px solid #fca5a5; padding:3px 8px; border-radius:var(--radius-full); text-decoration:none; font-weight:600; width:fit-content;">
                        🎬 ${sn.video.title} ↗
                      </a>
                    ` : ''}
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${sec.firstAidFiveDos ? `
            <div style="margin-top:14px;">
              <h4 style="color:#15803d; font-size:0.95rem; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                <span>✅</span> <span>毒蛇咬傷黃金急救【五要】守則（每項圖示詳解）：</span>
              </h4>
              <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:8px; margin-bottom:14px;">
                ${sec.firstAidFiveDos.map(d => `
                  <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-sm); padding:10px; display:flex; gap:10px; align-items:flex-start;">
                    <span style="font-size:1.6rem; line-height:1;">${d.icon}</span>
                    <div>
                      <strong style="color:#166534; font-size:0.86rem; display:block; margin-bottom:2px;">${d.title}</strong>
                      <span style="font-size:0.76rem; color:#15803d; line-height:1.4; display:block;">${d.desc}</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}

          ${sec.firstAidFiveDonts ? `
            <div>
              <h4 style="color:#b91c1c; font-size:0.95rem; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                <span>❌</span> <span>毒蛇咬傷禁忌【五不】原則（每項圖示警示）：</span>
              </h4>
              <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:8px; margin-bottom:14px;">
                ${sec.firstAidFiveDonts.map(d => `
                  <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:var(--radius-sm); padding:10px; display:flex; gap:10px; align-items:flex-start;">
                    <span style="font-size:1.6rem; line-height:1;">${d.icon}</span>
                    <div>
                      <strong style="color:#991b1b; font-size:0.86rem; display:block; margin-bottom:2px;">${d.title}</strong>
                      <span style="font-size:0.76rem; color:#b91c1c; line-height:1.4; display:block;">${d.desc}</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}

          ${sec.videos && sec.videos.length > 0 ? `
            <div style="margin-top:16px; padding:12px 14px; background:rgba(239,68,68,0.06); border:1px solid rgba(239,68,68,0.22); border-radius:var(--radius-sm);">
              <div style="color:#b91c1c; font-size:0.86rem; font-weight:700; display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                <span>🎬</span> <span>延伸實務影音教學全輯：</span>
              </div>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                ${sec.videos.map(v => `
                  <a href="${v.url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:5px; font-size:0.82rem; background:#fff; color:#dc2626; border:1px solid #fca5a5; padding:5px 12px; border-radius:var(--radius-full); text-decoration:none; font-weight:600; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
                    ▶️ ${v.title} ↗
                  </a>
                `).join('')}
              </div>
            </div>
          ` : ''}
        </div>
      </div>
    `).join("");

    // 手風琴切換
    container.querySelectorAll(".accordion-header").forEach(hdr => {
      hdr.addEventListener("click", () => {
        const item = hdr.parentElement;
        item.classList.toggle("open");
      });
    });
  }

  /* ==========================================================================
     9. 營規與生活公約
     ========================================================================== */
  function renderRules() {
    const container = document.getElementById("rules-content-container");
    if (!container) return;

    container.innerHTML = rules.map(rule => `
      <div class="info-card" style="margin-bottom:14px;">
        <div class="card-top">
          <span class="card-id-badge" style="background:#dcfce7; color:#15803d;">
            ${rule.icon} ${rule.title}
          </span>
        </div>
        <ul style="padding-left:20px; font-size:0.88rem; color:var(--text-secondary); line-height:1.7;">
          ${rule.items.map(it => `<li style="margin-bottom:6px;">${it}</li>`).join("")}
        </ul>
      </div>
    `).join("");
  }

  /* ==========================================================================
     10. 營地與活動資訊
     ========================================================================== */
  function renderInfo() {
    const container = document.getElementById("info-content-container");
    if (!container) return;

    container.innerHTML = `
      <div class="info-card" style="margin-bottom:16px;">
        <h3 style="font-size:1.1rem; color:var(--primary); margin-bottom:10px;">🏫 活動基本資料與主承辦單位</h3>
        <table class="styled-table">
          <tbody>
            <tr><th style="width:120px;">活動名稱</th><td>${info.title}</td></tr>
            <tr><th>活動時間</th><td>${info.dates}（${info.duration}）</td></tr>
            <tr><th>主辦單位</th><td>${info.school}</td></tr>
            <tr><th>承辦單位</th><td>${info.contractor}</td></tr>
            <tr><th>露營地點</th><td>${info.campLocation.name}（${info.campLocation.address}）</td></tr>
            <tr><th>全校統計</th><td>共 ${info.stats.classesCount} 班、學生 ${info.stats.studentsTotal} 人（男 ${info.stats.maleStudents} / 女 ${info.stats.femaleStudents}）</td></tr>
            <tr><th>帳篷與野炊</th><td>帳篷共 ${info.stats.tentsTotal} 頂（男 ${info.stats.maleTents} / 女 ${info.stats.femaleTents}）｜ 野炊小隊共 ${info.stats.squadsTotal} 組</td></tr>
          </tbody>
        </table>
      </div>

      <div class="info-card" style="margin-bottom:16px;">
        <h3 style="font-size:1.1rem; color:var(--primary); margin-bottom:10px;">👥 工作人員與隨隊導師一覽表</h3>
        <div class="cards-grid" style="grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap:10px;">
          ${info.staff.map(sf => `
            <div style="background:var(--bg-main); border:1px solid var(--border); padding:10px; border-radius:var(--radius-sm); text-align:center;">
              <span class="meta-pill primary" style="margin-bottom:4px; display:inline-block;">${sf.title}</span>
              <div style="font-size:1.05rem; font-weight:800; color:var(--text-primary);">${pName(sf)}</div>
              <span style="font-size:0.74rem; color:var(--text-muted);">隨車：${sf.bus}</span>
            </div>
          `).join("")}
        </div>
      </div>

      ${resortSpotGuide ? `
      <!-- 尖山埤渡假村景點風光與休閒設施全覽 -->
      <div class="info-card" style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
          <div>
            <span class="meta-pill primary" style="font-size:0.75rem; margin-bottom:4px; display:inline-block;">🏞️ 營訓基地全覽</span>
            <h3 style="font-size:1.25rem; color:var(--primary); font-weight:800; margin:0;">${resortSpotGuide.title}</h3>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">${resortSpotGuide.subtitle}</p>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <a href="${resortSpotGuide.officialUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-sm" style="display:inline-flex; align-items:center; gap:5px; text-decoration:none; padding:7px 14px; border-radius:8px; font-weight:800; font-size:0.82rem; background:var(--primary); color:#ffffff; box-shadow:0 2px 6px rgba(0,0,0,0.12);" title="前往台糖尖山埤官方網站">
              🌐 尖山埤官方網站
            </a>
            <a href="${resortSpotGuide.tourismBureauUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-sm" style="display:inline-flex; align-items:center; gap:5px; text-decoration:none; padding:7px 14px; border-radius:8px; font-weight:800; font-size:0.82rem; background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd;" title="台南市觀光旅遊局官方景點頁面">
              🏛️ 觀光旅遊局介紹
            </a>
            <a href="${resortSpotGuide.mapUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-sm" style="display:inline-flex; align-items:center; gap:5px; text-decoration:none; padding:7px 14px; border-radius:8px; font-weight:800; font-size:0.82rem; background:#f1f5f9; color:#334155; border:1px solid #cbd5e1;" title="開啟 Google 地圖全景與路線">
              🗺️ 地圖導航
            </a>
          </div>
        </div>

        <p style="font-size:0.9rem; line-height:1.75; color:var(--text-secondary); margin-bottom:14px; background:var(--bg-main); padding:12px 14px; border-radius:var(--radius-sm); border-left:4px solid var(--primary);">
          ${resortSpotGuide.overview}
        </p>

        <!-- 4大核心亮點 -->
        <div style="margin-bottom:20px;">
          <h4 style="font-size:0.95rem; font-weight:800; color:var(--text-primary); margin-bottom:8px;">✨ 園區四大核心特色亮點</h4>
          <div class="cards-grid" style="grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap:8px;">
            ${resortSpotGuide.features.map(f => `
              <div style="background:var(--bg-card); border:1px solid var(--border); padding:8px 12px; border-radius:var(--radius-sm); font-size:0.82rem; color:var(--text-secondary); display:flex; align-items:flex-start; gap:6px;">
                <span style="color:var(--primary); font-weight:900;">✔</span>
                <span>${f}</span>
              </div>
            `).join("")}
          </div>
        </div>

        <!-- 3部精選推薦影音專區 -->
        <div style="margin-bottom:24px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
            <h4 style="font-size:1.05rem; font-weight:800; color:var(--primary); margin:0; display:flex; align-items:center; gap:6px;">
              🎬 尖山埤渡假村 · 3部精選推薦影音介紹（100% 驗證有效）
            </h4>
            <span style="font-size:0.75rem; color:#16a34a; font-weight:700; background:#dcfce7; padding:2px 8px; border-radius:4px; border:1px solid #86efac;">✓ 影音連結均經 YouTube API 測試確認</span>
          </div>
          <div class="cards-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:12px;">
            ${resortSpotGuide.videos.map(v => `
              <div style="background:var(--bg-main); border:1px solid var(--border); border-radius:var(--radius-md); overflow:hidden; display:flex; flex-direction:column; box-shadow:0 2px 6px rgba(0,0,0,0.04);">
                <div style="position:relative; width:100%; height:150px; background:#000; overflow:hidden;">
                  <img src="https://img.youtube.com/vi/${v.videoId}/mqdefault.jpg" alt="${v.title}" style="width:100%; height:100%; object-fit:cover;" onerror="this.src='assets/img/resort/resort_1_boat.jpg'">
                  <div style="position:absolute; bottom:6px; right:8px; background:rgba(0,0,0,0.75); color:#fff; font-size:0.7rem; padding:2px 6px; border-radius:4px; font-weight:700;">YouTube</div>
                </div>
                <div style="padding:12px; flex:1; display:flex; flex-direction:column;">
                  <span class="meta-pill" style="font-size:0.7rem; width:fit-content; margin-bottom:6px; background:#fef2f2; color:#dc2626; border:1px solid #fecaca; font-weight:700;">📺 ${v.channel}</span>
                  <div style="font-size:0.9rem; font-weight:800; color:var(--text-primary); margin-bottom:6px; line-height:1.4;">${v.title}</div>
                  <p style="font-size:0.78rem; color:var(--text-muted); line-height:1.5; margin-bottom:12px; flex:1;">${v.desc}</p>
                  <a href="${v.url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; justify-content:center; gap:6px; text-decoration:none; padding:8px 12px; border-radius:6px; font-weight:700; font-size:0.82rem; background:#dc2626; color:#ffffff; transition:opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">
                    ▶ 立即播放影音介紹
                  </a>
                </div>
              </div>
            `).join("")}
          </div>
        </div>

        <!-- 6大特色風光照片圖文說明 -->
        <div>
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
            <h4 style="font-size:1.05rem; font-weight:800; color:var(--primary); margin:0; display:flex; align-items:center; gap:6px;">
              📸 尖山埤渡假村 · 六大代表特色風光圖文說明
            </h4>
            <span style="font-size:0.75rem; color:var(--text-muted);">官方實景照片 · 配有完整景點解說</span>
          </div>
          <div class="cards-grid" style="grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap:14px;">
            ${resortSpotGuide.photos.map(p => `
              <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-md); overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.06); display:flex; flex-direction:column;">
                <div style="width:100%; height:195px; background:#e2e8f0; overflow:hidden;">
                  <img src="${p.file}" alt="${p.title}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.3s ease;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'" loading="lazy">
                </div>
                <div style="padding:12px; flex:1; display:flex; flex-direction:column;">
                  <h5 style="font-size:0.95rem; font-weight:800; color:var(--primary); margin:0 0 6px 0;">${p.title}</h5>
                  <p style="font-size:0.82rem; color:var(--text-secondary); line-height:1.6; margin:0;">${p.desc}</p>
                </div>
              </div>
            `).join("")}
          </div>
        </div>

      </div>
      ` : ""}
    `;
  }

  /* ==========================================================================
     行前說明會四大重點宣導（源自：隔宿露營行前說明會.txt）
     ========================================================================== */
  function renderBriefing() {
    const container = document.getElementById("briefing-content-container");
    if (!container || !preCampBriefing) return;

    container.innerHTML = `
      <div style="background:linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%); border:2px solid #fdba74; border-radius:var(--radius-md); padding:16px 18px; margin-bottom:16px; box-shadow:0 3px 12px rgba(234,88,12,0.06);">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
          <span style="font-size:2rem;">📢</span>
          <div>
            <h3 style="margin:0; font-size:1.25rem; color:#9a3412; font-weight:800;">${preCampBriefing.title}</h3>
            <p style="margin:2px 0 0; font-size:0.86rem; color:#c2410c;">${preCampBriefing.subtitle}</p>
          </div>
        </div>
        <div style="background:#ffffff; border:1px solid #fed7aa; border-radius:var(--radius-sm); padding:12px 14px;">
          <strong style="color:#c2410c; font-size:0.88rem; display:block; margin-bottom:6px;">📜 10/23 說明會宣導重點原文：</strong>
          <pre style="white-space:pre-wrap; font-family:inherit; font-size:0.88rem; color:#7c2d12; line-height:1.75; margin:0; font-weight:500;">${preCampBriefing.rawText || ''}</pre>
        </div>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px;">
        ${preCampBriefing.items.map(item => `
          <div class="info-card" style="border-left:5px solid ${item.num === '四' ? '#dc2626' : (item.num === '一' ? '#ea580c' : (item.num === '三' ? '#16a34a' : '#2563eb'))}; background:#fff; position:relative;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:1.6rem; line-height:1;">${item.icon}</span>
                <h4 style="margin:0; font-size:1.02rem; color:var(--text-primary); font-weight:700;">${item.title}</h4>
              </div>
              <span class="meta-pill" style="background:${item.num === '四' ? '#fee2e2' : (item.num === '一' ? '#ffedd5' : (item.num === '三' ? '#dcfce7' : '#e0f2fe'))}; color:${item.num === '四' ? '#991b1b' : (item.num === '一' ? '#c2410c' : (item.num === '三' ? '#166534' : '#0369a1'))}; font-weight:700;">
                ${item.tag}
              </span>
            </div>
            <p style="font-size:0.88rem; color:var(--text-secondary); line-height:1.65; margin:0;">
              ${item.desc}
            </p>
          </div>
        `).join('')}
      </div>
    `;
  }

  /* ==========================================================================
     童軍技能分站教育學習單 (手冊第 22、23 頁)
     ========================================================================== */
  function renderWorksheet() {
    const container = document.getElementById("worksheet-content-container");
    if (!container || !worksheet) return;

    let savedWorksheet = {};
    try {
      savedWorksheet = JSON.parse(localStorage.getItem("ntjh_camp_worksheet_answers_115") || "{}");
    } catch (e) { savedWorksheet = {}; }

    container.innerHTML = `
      <div style="background:linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); border:2px solid #818cf8; border-radius:var(--radius-md); padding:16px 20px; margin-bottom:18px; box-shadow:0 3px 12px rgba(99,102,241,0.08);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <h3 style="margin:0; font-size:1.25rem; color:#3730a3; font-weight:800;">📝 ${worksheet.title}</h3>
            <p style="margin:4px 0 0; font-size:0.86rem; color:#4338ca;">${worksheet.subtitle}</p>
          </div>
          <div style="display:flex; gap:8px;">
            <button id="ws-save-btn" class="btn btn-primary" style="background:#4f46e5; border-color:#4f46e5; font-size:0.82rem; padding:6px 14px; border-radius:var(--radius-full); cursor:pointer;">💾 儲存作答</button>
            <button id="ws-print-btn" class="btn" style="background:#fff; border:1px solid #c7d2fe; color:#3730a3; font-size:0.82rem; padding:6px 14px; border-radius:var(--radius-full); cursor:pointer;">🖨️ 列印學習單</button>
          </div>
        </div>
      </div>

      <!-- 任務一：營帳使用原則挑錯題 -->
      <div class="info-card" style="margin-bottom:20px; background:#fff; border-top:4px solid #ea580c;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
          <div>
            <h4 style="margin:0; font-size:1.1rem; color:#c2410c; font-weight:800;">🏕️ ${worksheet.sections[0].title}</h4>
            <p style="font-size:0.86rem; color:var(--text-secondary); margin:4px 0 0;">${worksheet.sections[0].instruction}</p>
          </div>
          <span class="meta-pill" style="background:#ffedd5; color:#c2410c; font-weight:700;">手冊第 22 頁</span>
        </div>

        <div style="text-align:center; margin:12px 0; background:#f8fafc; border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px;">
          <img src="${worksheet.sections[0].image}" alt="營帳使用原則挑錯" style="max-width:100%; max-height:360px; object-fit:contain; border-radius:var(--radius-sm); box-shadow:var(--shadow-sm); display:block; margin:0 auto;" loading="lazy">
          <div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px; font-weight:600;">📷 ${worksheet.sections[0].imageCaption}</div>
        </div>

        <div style="margin-top:14px;">
          <label style="display:block; font-weight:700; color:var(--text-primary); margin-bottom:6px; font-size:0.9rem;">✍️ 我的作答（請寫出圖中違反營帳原則的地方）：</label>
          <textarea id="ws-input-tent" class="search-input" style="width:100%; height:80px; padding:10px; font-size:0.88rem; line-height:1.5; border:1px solid var(--border); border-radius:var(--radius-sm); resize:vertical;" placeholder="例如：1. 在帳篷內使用瓦斯爐生火煮食...">${savedWorksheet.tent || ''}</textarea>
        </div>

        <details style="margin-top:12px; background:#fff7ed; border:1px solid #fed7aa; border-radius:var(--radius-sm); padding:10px 14px;">
          <summary style="font-weight:700; color:#c2410c; cursor:pointer; font-size:0.9rem;">💡 點此查看【官方參考解答與違規解析】（共 5 大違規點）</summary>
          <div style="margin-top:10px; display:flex; flex-direction:column; gap:8px;">
            ${worksheet.sections[0].errors.map(err => `
              <div style="background:#fff; border-left:4px solid #ea580c; padding:8px 12px; border-radius:4px; font-size:0.86rem;">
                <strong style="color:#c2410c;">${err.num}. ${err.point}</strong>
                <p style="margin:3px 0 0; color:var(--text-secondary); line-height:1.5;">${err.reason}</p>
              </div>
            `).join('')}
          </div>
        </details>
      </div>

      <!-- 任務二：有毒動植物連連看 -->
      <div class="info-card" style="margin-bottom:20px; background:#fff; border-top:4px solid #dc2626;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
          <div>
            <h4 style="margin:0; font-size:1.1rem; color:#dc2626; font-weight:800;">🌿 ${worksheet.sections[1].title}</h4>
            <p style="font-size:0.86rem; color:var(--text-secondary); margin:4px 0 0;">${worksheet.sections[1].instruction}</p>
          </div>
          <span class="meta-pill" style="background:#fee2e2; color:#dc2626; font-weight:700;">手冊第 22 頁</span>
        </div>

        <div style="text-align:center; margin:12px 0; background:#f8fafc; border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px;">
          <img src="${worksheet.sections[1].image}" alt="有毒動植物辨識連連看" style="max-width:100%; max-height:300px; object-fit:contain; border-radius:var(--radius-sm); box-shadow:var(--shadow-sm); display:block; margin:0 auto;" loading="lazy">
          <div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px; font-weight:600;">📷 ${worksheet.sections[1].imageCaption}</div>
        </div>

        <div style="margin-top:14px;">
          <label style="display:block; font-weight:700; color:var(--text-primary); margin-bottom:6px; font-size:0.9rem;">✍️ 我的配對答案（圖 1～5 對應 A～J 代號）：</label>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:8px;">
            ${[1, 2, 3, 4, 5].map(n => `
              <div style="display:flex; align-items:center; gap:6px; background:#f8fafc; padding:6px 10px; border-radius:var(--radius-sm); border:1px solid var(--border);">
                <span style="font-weight:700; font-size:0.88rem; color:#b91c1c;">圖 ${n}：</span>
                <input type="text" id="ws-poison-${n}" maxlength="2" value="${savedWorksheet['poison_' + n] || ''}" style="width:40px; text-align:center; font-weight:800; border:1px solid var(--border); border-radius:4px; padding:3px; text-transform:uppercase;" placeholder="代號">
              </div>
            `).join('')}
          </div>
        </div>

        <details style="margin-top:12px; background:#fef2f2; border:1px solid #fecdd3; border-radius:var(--radius-sm); padding:10px 14px;">
          <summary style="font-weight:700; color:#dc2626; cursor:pointer; font-size:0.9rem;">💡 點此查看【官方參考配對答案與特徵說明】</summary>
          <div style="margin-top:10px; display:flex; flex-direction:column; gap:8px;">
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:8px;">
              ${worksheet.sections[1].pairs.map(p => `
                <div style="background:#fff; border-left:4px solid #dc2626; padding:8px 12px; border-radius:4px; font-size:0.85rem;">
                  <strong style="color:#b91c1c; font-size:0.92rem;">圖 ${p.imgIndex} ➔ 【${p.code}. ${p.name}】</strong>
                  <p style="margin:2px 0 0; color:var(--text-secondary); line-height:1.45;">${p.feature}</p>
                </div>
              `).join('')}
            </div>
            <div style="margin-top:6px; font-size:0.82rem; color:#991b1b; background:#fff; padding:8px 12px; border-radius:4px;">
              <b>📌 其餘干擾項目速查：</b>
              ${worksheet.sections[1].distractors.map(d => `<span>【${d.code}. ${d.name}】${d.desc}　</span>`).join('')}
            </div>
          </div>
        </details>
      </div>

      <!-- 任務三：中暑急救流程圖判讀 -->
      <div class="info-card" style="margin-bottom:20px; background:#fff; border-top:4px solid #2563eb;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
          <div>
            <h4 style="margin:0; font-size:1.1rem; color:#2563eb; font-weight:800;">🚑 ${worksheet.sections[2].title}</h4>
            <p style="font-size:0.86rem; color:var(--text-secondary); margin:4px 0 0;">${worksheet.sections[2].instruction}</p>
          </div>
          <span class="meta-pill" style="background:#dbeafe; color:#2563eb; font-weight:700;">手冊第 22 頁</span>
        </div>

        <div style="text-align:center; margin:12px 0; background:#f8fafc; border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px;">
          <img src="${worksheet.sections[2].image}" alt="中暑急救流程圖" style="max-width:100%; max-height:280px; object-fit:contain; border-radius:var(--radius-sm); box-shadow:var(--shadow-sm); display:block; margin:0 auto;" loading="lazy">
          <div style="font-size:0.8rem; color:var(--text-muted); margin-top:8px; font-weight:600;">📷 ${worksheet.sections[2].imageCaption}</div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; margin-top:12px;">
          ${worksheet.sections[2].steps.map((st, i) => `
            <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:var(--radius-sm); padding:10px;">
              <strong style="color:#1d4ed8; font-size:0.88rem; display:block; margin-bottom:3px;">${st.step}</strong>
              <p style="font-size:0.8rem; color:#1e40af; margin:0; line-height:1.45;">${st.desc}</p>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- 任務四：繩結情境歡樂連線與功能深度解析 -->
      <div class="info-card" style="margin-bottom:20px; background:#fff; border-top:4px solid #16a34a;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
          <div>
            <h4 style="margin:0; font-size:1.1rem; color:#16a34a; font-weight:800;">🪢 ${worksheet.sections[3].title}</h4>
            <p style="font-size:0.86rem; color:var(--text-secondary); margin:4px 0 0;">${worksheet.sections[3].instruction}</p>
          </div>
          <span class="meta-pill" style="background:#dcfce7; color:#16a34a; font-weight:700;">手冊第 23 頁</span>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:12px; margin:12px 0;">
          <div style="text-align:center; background:#f8fafc; border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px;">
            <img src="${worksheet.sections[3].image1}" alt="繩結歡樂連線" style="max-width:100%; max-height:280px; object-fit:contain; border-radius:var(--radius-sm); display:block; margin:0 auto;" loading="lazy">
            <div style="font-size:0.78rem; color:var(--text-muted); margin-top:6px; font-weight:600;">📷 歡樂連線情境圖（領巾、茶壺、爬繩、腳踝包紮）</div>
          </div>
          <div style="text-align:center; background:#f8fafc; border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px;">
            <img src="${worksheet.sections[3].image2}" alt="單結與繩梯變化" style="max-width:100%; max-height:280px; object-fit:contain; border-radius:var(--radius-sm); display:block; margin:0 auto;" loading="lazy">
            <div style="font-size:0.78rem; color:var(--text-muted); margin-top:6px; font-weight:600;">📷 單結基礎與繩梯多重單結防滑變化圖</div>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:12px; margin-top:14px;">
          <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-sm); padding:12px 14px;">
            <strong style="color:#15803d; font-size:0.92rem; display:block; margin-bottom:4px;">Q1. 歡樂連線解答：</strong>
            <p style="margin:0; font-size:0.86rem; color:#166534; line-height:1.6; white-space:pre-line;">${worksheet.sections[3].qa[0].ans}</p>
          </div>

          <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-sm); padding:12px 14px;">
            <strong style="color:#15803d; font-size:0.92rem; display:block; margin-bottom:4px;">Q2 & Q3. 單結與繩梯結應用：</strong>
            <p style="margin:0 0 6px; font-size:0.86rem; color:#166534; line-height:1.5;"><b>單結用途：</b>${worksheet.sections[3].qa[1].ans}</p>
            <p style="margin:0; font-size:0.86rem; color:#166534; line-height:1.5;"><b>繩梯結變化：</b>${worksheet.sections[3].qa[2].ans}</p>
          </div>

          <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-sm); padding:12px 14px;">
            <strong style="color:#15803d; font-size:0.92rem; display:block; margin-bottom:8px;">Q4. 繩子對十大人、事、物之用途（手冊第 23 頁 A～J）：</strong>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:8px;">
              ${worksheet.sections[3].qa[3].items.map(it => `
                <div style="background:#fff; border-left:3px solid #16a34a; padding:6px 10px; border-radius:4px; font-size:0.82rem;">
                  <strong style="color:#15803d;">${it.item}：</strong>
                  <span style="color:var(--text-secondary);">${it.use}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-sm); padding:12px 14px;">
            <strong style="color:#15803d; font-size:0.92rem; display:block; margin-bottom:8px;">Q5. 哪些材料可以做繩子？天然 vs 化學纖維功能區別：</strong>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:10px;">
              ${worksheet.sections[3].qa[4].materials.map(mat => `
                <div style="background:#fff; border:1px solid #bbf7d0; padding:10px; border-radius:4px; font-size:0.84rem;">
                  <strong style="color:#15803d; display:block; margin-bottom:4px;">${mat.type}</strong>
                  <div style="color:var(--text-secondary); line-height:1.5;">
                    <b style="color:#166534;">優點：</b>${mat.pros}<br>
                    <b style="color:#991b1b;">缺點：</b>${mat.cons}<br>
                    <b style="color:#2563eb;">最適用於：</b>${mat.bestFor}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </div>
    `;

    // 綁定儲存按鈕
    const saveBtn = document.getElementById("ws-save-btn");
    if (saveBtn) {
      saveBtn.addEventListener("click", () => {
        const tentVal = document.getElementById("ws-input-tent")?.value || "";
        const dataToSave = { tent: tentVal };
        [1, 2, 3, 4, 5].forEach(n => {
          dataToSave['poison_' + n] = document.getElementById(`ws-poison-${n}`)?.value || "";
        });
        localStorage.setItem("ntjh_camp_worksheet_answers_115", JSON.stringify(dataToSave));
        saveBtn.textContent = "✅ 已儲存！";
        setTimeout(() => { saveBtn.textContent = "💾 儲存作答"; }, 2000);
      });
    }

    // 綁定列印按鈕
    const printBtn = document.getElementById("ws-print-btn");
    if (printBtn) {
      printBtn.addEventListener("click", () => {
        window.print();
      });
    }
  }

  /* ==========================================================================
     自我檢核表 (手冊第 24 頁)
     ========================================================================== */
  function renderSelfChecklist() {
    const container = document.getElementById("selfcheck-content-container");
    if (!container || !selfChecklist) return;

    let savedGrades = {};
    let savedNote = "";
    try {
      const data = JSON.parse(localStorage.getItem("ntjh_camp_selfcheck_grades_115") || "{}");
      savedGrades = data.grades || {};
      savedNote = data.note || "";
    } catch (e) {
      savedGrades = {};
      savedNote = "";
    }

    const gradePoints = { '優': 5, '良': 4, '可': 3, '差': 2, '劣': 1 };
    let totalScore = 0;
    let answeredCount = 0;

    selfChecklist.items.forEach(it => {
      const g = savedGrades[it.id];
      if (g && gradePoints[g]) {
        totalScore += gradePoints[g];
        answeredCount++;
      }
    });

    const maxScore = selfChecklist.items.length * 5; // 65分
    const scorePct = maxScore > 0 ? Math.round((totalScore / maxScore) * 100) : 0;

    container.innerHTML = `
      <div style="background:linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border:2px solid #6ee7b7; border-radius:var(--radius-md); padding:16px 20px; margin-bottom:18px; box-shadow:0 3px 12px rgba(16,185,129,0.08);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <h3 style="margin:0; font-size:1.25rem; color:#065f46; font-weight:800;">✅ ${selfChecklist.title}</h3>
            <p style="margin:4px 0 0; font-size:0.86rem; color:#047857;">${selfChecklist.subtitle}</p>
          </div>
          <div style="display:flex; gap:8px;">
            <button id="sc-save-btn" class="btn btn-primary" style="background:#059669; border-color:#059669; font-size:0.82rem; padding:6px 14px; border-radius:var(--radius-full); cursor:pointer;">💾 儲存評量</button>
            <button id="sc-print-btn" class="btn" style="background:#fff; border:1px solid #a7f3d0; color:#065f46; font-size:0.82rem; padding:6px 14px; border-radius:var(--radius-full); cursor:pointer;">🖨️ 列印檢核表</button>
          </div>
        </div>

        <div style="margin-top:14px; background:#fff; border:1px solid #a7f3d0; border-radius:var(--radius-sm); padding:12px 16px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
          <div>
            <span style="font-size:0.85rem; color:#047857; font-weight:700;">目前檢核進度：已評定 ${answeredCount} / ${selfChecklist.items.length} 題</span>
            <div style="font-size:1.15rem; font-weight:800; color:#065f46; margin-top:2px;">
              綜合得分：${totalScore} / ${maxScore} 分（達成率 ${scorePct}%）
            </div>
          </div>
          <div style="width:160px; background:#e2e8f0; border-radius:999px; height:12px; overflow:hidden;">
            <div style="width:${scorePct}%; background:#10b981; height:100%; transition:width 0.3s ease;"></div>
          </div>
        </div>
      </div>

      <div style="background:#fff; border:1px solid var(--border); border-radius:var(--radius-md); padding:18px 20px; margin-bottom:18px; box-shadow:var(--shadow-sm);">
        <p style="font-size:0.92rem; color:var(--text-secondary); line-height:1.7; margin-bottom:14px; font-weight:500;">
          『115 學年度二年級戶外教育活動』，即將進入尾聲，當思緒由絢爛回歸平靜，我們一起來檢核一下是否做到下列幾點：
        </p>

        <div style="display:flex; flex-direction:column; gap:10px;">
          ${selfChecklist.items.map((it, idx) => {
            const currentGrade = savedGrades[it.id] || '';
            return `
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; padding:10px 14px; background:${idx % 2 === 0 ? '#f8fafc' : '#fff'}; border:1px solid var(--border); border-radius:var(--radius-sm);">
                <div style="display:flex; align-items:center; gap:8px; flex:1; min-width:260px;">
                  <span style="font-family:var(--font-mono); font-weight:700; color:#059669; min-width:24px;">${String(it.id).padStart(2, '0')}.</span>
                  <span style="font-size:0.9rem; color:var(--text-primary); font-weight:600;">${it.text}</span>
                  <span class="meta-pill" style="font-size:0.72rem; padding:1px 6px; background:#e0f2fe; color:#0369a1;">${it.cat}</span>
                </div>
                <div class="grade-button-group" style="display:flex; gap:6px;">
                  ${selfChecklist.grades.map(g => `
                    <button type="button" class="sc-grade-btn ${currentGrade === g ? 'active' : ''}" data-id="${it.id}" data-grade="${g}" style="padding:4px 10px; font-size:0.8rem; font-weight:700; border-radius:4px; border:1px solid ${currentGrade === g ? '#059669' : 'var(--border)'}; background:${currentGrade === g ? '#059669' : '#fff'}; color:${currentGrade === g ? '#fff' : 'var(--text-secondary)'}; cursor:pointer; transition:all 0.15s ease;">
                      ${g}
                    </button>
                  `).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div style="margin-top:20px; border-top:1px dashed var(--border); padding-top:16px;">
          <label style="display:block; font-weight:700; color:var(--text-primary); margin-bottom:6px; font-size:0.92rem;">💭 個人心得反思（本次隔宿露營我最大的收穫與感動）：</label>
          <textarea id="sc-note-input" class="search-input" style="width:100%; height:90px; padding:10px; font-size:0.88rem; line-height:1.6; border:1px solid var(--border); border-radius:var(--radius-sm); resize:vertical;" placeholder="分享你的成長歷程、小隊團隊合作感動，或是給自己未來的期許...">${savedNote}</textarea>
        </div>

        <!-- 導師簽章欄 -->
        <div style="margin-top:16px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-sm); padding:12px 16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <strong style="color:#15803d; font-size:0.9rem;">綜合表現評核（本欄由隨隊導師填寫）：</strong>
            <div style="margin-top:4px; font-size:0.84rem; color:#166534;">
              整體表現：【 優 ｜ 良 ｜ 可 ｜ 差 ｜ 劣 】 ｜ 表現優異者得推薦全校生活教育楷模獎項。
            </div>
          </div>
          <div style="font-size:0.88rem; color:#166534; font-weight:700; border-bottom:1px solid #15803d; padding-bottom:2px; min-width:140px; text-align:center;">
            導師簽名：____________
          </div>
        </div>
      </div>
    `;

    // 綁定各題評分按鈕
    container.querySelectorAll(".sc-grade-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const qId = btn.dataset.id;
        const grade = btn.dataset.grade;
        savedGrades[qId] = grade;
        const note = document.getElementById("sc-note-input")?.value || "";
        localStorage.setItem("ntjh_camp_selfcheck_grades_115", JSON.stringify({ grades: savedGrades, note }));
        renderSelfChecklist();
      });
    });

    // 綁定儲存按鈕
    const saveBtn = document.getElementById("sc-save-btn");
    if (saveBtn) {
      saveBtn.addEventListener("click", () => {
        const note = document.getElementById("sc-note-input")?.value || "";
        localStorage.setItem("ntjh_camp_selfcheck_grades_115", JSON.stringify({ grades: savedGrades, note }));
        saveBtn.textContent = "✅ 已儲存！";
        setTimeout(() => { saveBtn.textContent = "💾 儲存評量"; }, 2000);
      });
    }

    // 綁定列印按鈕
    const printBtn = document.getElementById("sc-print-btn");
    if (printBtn) {
      printBtn.addEventListener("click", () => {
        window.print();
      });
    }
  }


  /* ==========================================================================
     全部重新渲染（切換隱私模式時使用）
     ========================================================================== */
  function reRenderAll() {
    renderHero();
    renderItinerary();
    renderTents();
    renderSquads();
    renderRoster();
    renderBuses();
    renderBriefing();
    renderChecklist();
    renderScout();
    renderRules();
    renderInfo();
    renderWorksheet();
    renderSelfChecklist();
  }

  /* ==========================================================================
     事件綁定 (篩選、搜尋、去個資切換)
     ========================================================================== */
  function initEvents() {
    // 1. 帳篷篩選與搜尋
    const tentInput = document.getElementById("tent-search-input");
    const tentClear = document.getElementById("tent-search-clear");
    if (tentInput) {
      tentInput.addEventListener("input", (e) => {
        state.tentQuery = e.target.value;
        if (tentClear) tentClear.style.display = state.tentQuery ? "block" : "none";
        renderTents();
      });
    }
    if (tentClear) {
      tentClear.addEventListener("click", () => {
        state.tentQuery = "";
        if (tentInput) tentInput.value = "";
        tentClear.style.display = "none";
        renderTents();
      });
    }

    document.querySelectorAll(".tent-class-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".tent-class-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.tentClass = chip.dataset.class;
        renderTents();
      });
    });

    document.querySelectorAll(".tent-gender-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".tent-gender-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.tentGender = chip.dataset.gender;
        renderTents();
      });
    });

    document.querySelectorAll(".tent-view-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tent-view-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        state.tentView = btn.dataset.view;
        renderTents();
      });
    });

    // 3. 野炊小隊篩選與搜尋
    const squadInput = document.getElementById("squad-search-input");
    const squadClear = document.getElementById("squad-search-clear");
    if (squadInput) {
      squadInput.addEventListener("input", (e) => {
        state.squadQuery = e.target.value;
        if (squadClear) squadClear.style.display = state.squadQuery ? "block" : "none";
        renderSquads();
      });
    }
    if (squadClear) {
      squadClear.addEventListener("click", () => {
        state.squadQuery = "";
        if (squadInput) squadInput.value = "";
        squadClear.style.display = "none";
        renderSquads();
      });
    }

    document.querySelectorAll(".squad-class-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".squad-class-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.squadClass = chip.dataset.class;
        renderSquads();
      });
    });

    document.querySelectorAll(".squad-view-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".squad-view-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        state.squadView = btn.dataset.view;
        renderSquads();
      });
    });

    // 4. 學生名冊篩選與搜尋
    const rosterInput = document.getElementById("roster-search-input");
    const rosterClear = document.getElementById("roster-search-clear");
    if (rosterInput) {
      rosterInput.addEventListener("input", (e) => {
        state.rosterQuery = e.target.value;
        if (rosterClear) rosterClear.style.display = state.rosterQuery ? "block" : "none";
        renderRoster();
      });
    }
    if (rosterClear) {
      rosterClear.addEventListener("click", () => {
        state.rosterQuery = "";
        if (rosterInput) rosterInput.value = "";
        rosterClear.style.display = "none";
        renderRoster();
      });
    }

    document.querySelectorAll(".roster-class-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".roster-class-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.rosterClass = chip.dataset.class;
        renderRoster();
      });
    });

    document.querySelectorAll(".roster-gender-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".roster-gender-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.rosterGender = chip.dataset.gender;
        renderRoster();
      });
    });

    document.querySelectorAll(".roster-diet-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".roster-diet-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.rosterDiet = chip.dataset.diet;
        renderRoster();
      });
    });

    // 5. 導航 Tab 綁定
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        switchTab(btn.dataset.tab);
      });
    });

    document.querySelectorAll(".mobile-nav-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        switchTab(btn.dataset.tab);
      });
    });

    // 5.5 車.野炊.帳棚 子分頁切換按鈕綁定
    document.querySelectorAll(".groups-subnav-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        switchSubpane(btn.dataset.subpane);
      });
    });
  }

  // 初次執行渲染
  initEvents();
  reRenderAll();
  switchTab("itinerary");
});

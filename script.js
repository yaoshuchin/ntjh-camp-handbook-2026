/**
 * 南投縣立南投國民中學 115學年度 二年級隔宿露營專屬行動手冊
 * 前端核心互動邏輯 (app.js)
 */

document.addEventListener("DOMContentLoaded", () => {
  if (typeof CAMP_DATA === "undefined") {
    console.error("CAMP_DATA is not loaded! Please check data.js.");
    return;
  }

  const { info, classes, buses, students, tents, squads, itinerary, checklist, rules, scoutKnowledge } = CAMP_DATA;

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
     導航切換
     ========================================================================== */
  function switchTab(target) {
    if (!target) return;
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

    // 捲動至頂部
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // 全域綁定方便調用
  window.switchTab = switchTab;

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

    container.innerHTML = scoutKnowledge.map((sec, idx) => `
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
                    ${m.video ? `
                      <a href="${m.video.url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:4px; font-size:0.76rem; background:#fff; color:#dc2626; border:1px solid #fca5a5; padding:3px 8px; border-radius:var(--radius-full); text-decoration:none; font-weight:600; width:fit-content;">
                        🎬 ${m.video.title} ↗
                      </a>
                    ` : ''}
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
    `;
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
    renderChecklist();
    renderScout();
    renderRules();
    renderInfo();
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
  }

  // 初次執行渲染
  initEvents();
  reRenderAll();
  switchTab("itinerary");
});

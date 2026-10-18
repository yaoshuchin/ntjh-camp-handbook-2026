/* ============================================================
   DSLab Lesson · 網頁簡報引擎
   - 固定 1280×720 畫布，用 transform:scale 等比縮放（投影所見即所得）
   - present：一次一頁、方向鍵翻頁 ／ read：全部攤開捲動
   - 複製鈕、溢出檢查（機械擋門，不靠人眼一頁頁看）
   ============================================================ */
(function () {
    'use strict';

    var SLIDE_W = 1280;
    var SLIDE_H = 720;

    var body = document.body;
    var stage = document.getElementById('deck-stage');
    if (!stage) return;

    // 把每張 .slide 包進 .slide-fit（負責佔位與比例）
    var raw = Array.prototype.slice.call(stage.querySelectorAll('.slide'));
    var fits = raw.map(function (sl, i) {
        var fit = document.createElement('div');
        fit.className = 'slide-fit';
        sl.parentNode.insertBefore(fit, sl);
        fit.appendChild(sl);
        var no = document.createElement('div');
        no.className = 'slide-no';
        no.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(raw.length).padStart(2, '0');
        sl.appendChild(no);
        return fit;
    });

    var total = fits.length;
    var idx = 0;

    /* ── 縮放：把 1280 寬的畫布縮到容器寬 ── */
    function rescale() {
        fits.forEach(function (fit) {
            var w = fit.clientWidth;
            if (!w) return;
            var k = w / SLIDE_W;
            var sl = fit.querySelector('.slide');
            sl.style.transform = 'scale(' + k + ')';
        });
    }

    /* ── 模式 ── */
    function setMode(mode) {
        body.setAttribute('data-mode', mode);
        var btn = document.getElementById('mode-btn');
        if (btn) {
            btn.textContent = mode === 'present' ? '閱讀模式' : '簡報模式';
            btn.classList.toggle('is-on', mode === 'present');
        }
        try { localStorage.setItem('dslab-deck-mode', mode); } catch (e) { /* 無痕視窗會丟例外 */ }
        if (mode === 'present') go(idx);
        // 換模式後容器寬度會變，必須重量一次
        requestAnimationFrame(rescale);
    }

    /* ── 翻頁 ── */
    function go(n) {
        idx = Math.max(0, Math.min(total - 1, n));
        fits.forEach(function (f, i) { f.classList.toggle('is-current', i === idx); });
        var pos = document.getElementById('ctrl-pos');
        if (pos) pos.textContent = (idx + 1) + ' / ' + total;
        var cnt = document.getElementById('deck-count');
        if (cnt) cnt.textContent = (idx + 1) + ' / ' + total;
        var p = document.getElementById('ctrl-prev');
        var x = document.getElementById('ctrl-next');
        if (p) p.disabled = idx === 0;
        if (x) x.disabled = idx === total - 1;
        if (body.getAttribute('data-mode') === 'present') window.scrollTo(0, 0);
        markTocCurrent();
    }

    /* ── 綁定 ── */
    var modeBtn = document.getElementById('mode-btn');
    if (modeBtn) {
        modeBtn.addEventListener('click', function () {
            setMode(body.getAttribute('data-mode') === 'present' ? 'read' : 'present');
        });
    }
    var fsBtn = document.getElementById('fs-btn');
    if (fsBtn) {
        fsBtn.addEventListener('click', function () {
            if (document.fullscreenElement) document.exitFullscreen();
            else document.documentElement.requestFullscreen();
        });
    }
    var prev = document.getElementById('ctrl-prev');
    var next = document.getElementById('ctrl-next');
    if (prev) prev.addEventListener('click', function () { go(idx - 1); });
    if (next) next.addEventListener('click', function () { go(idx + 1); });

    /* ── 總覽：投影時直接跳主題，不必一頁一頁翻 ── */
    var toc = document.getElementById('deck-toc');
    var tocGrid = document.getElementById('deck-toc-grid');

    function buildToc() {
        if (!tocGrid) return;
        tocGrid.innerHTML = '';
        fits.forEach(function (fit, i) {
            var sl = fit.querySelector('.slide');
            // 標題取投影片上實際的文字，不另外維護一份清單——
            // 另外維護就會有「改了標題忘了改總覽」這種不會報錯的漂移。
            var eyebrow = sl.querySelector('.s-eyebrow');
            var h = sl.querySelector('.s-title, .s-title-xl');
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'toc-item';
            // 標題是文字節點，逐個建元素比拼 innerHTML 安全（標題含 & 或 < 也不會壞）
            var no = document.createElement('span');
            no.className = 'toc-no';
            no.textContent = String(i + 1).padStart(2, '0');
            var txt = document.createElement('span');
            txt.className = 'toc-txt';
            var eb = document.createElement('span');
            eb.className = 'toc-eyebrow';
            eb.textContent = eyebrow ? eyebrow.textContent : '';
            var hh = document.createElement('span');
            hh.className = 'toc-h';
            hh.textContent = h ? h.textContent : '(無標題)';
            txt.appendChild(eb);
            txt.appendChild(hh);
            btn.appendChild(no);
            btn.appendChild(txt);
            btn.addEventListener('click', function () {
                closeToc();
                if (body.getAttribute('data-mode') === 'present') go(i);
                else fit.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
            tocGrid.appendChild(btn);
        });
    }

    function markTocCurrent() {
        if (!tocGrid) return;
        var items = tocGrid.querySelectorAll('.toc-item');
        for (var i = 0; i < items.length; i++) items[i].classList.toggle('is-current', i === idx);
    }

    function openToc() {
        if (!toc) return;
        markTocCurrent();
        toc.hidden = false;
        var cur = tocGrid && tocGrid.querySelector('.toc-item.is-current');
        if (cur) cur.scrollIntoView({ block: 'center' });
    }
    function closeToc() { if (toc) toc.hidden = true; }

    var tocBtn = document.getElementById('toc-btn');
    var tocClose = document.getElementById('toc-close');
    if (tocBtn) tocBtn.addEventListener('click', function () { toc.hidden ? openToc() : closeToc(); });
    if (tocClose) tocClose.addEventListener('click', closeToc);
    if (toc) toc.addEventListener('click', function (e) { if (e.target === toc) closeToc(); });

    document.addEventListener('keydown', function (e) {
        if (e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;
        // 總覽在兩種模式下都能開（閱讀模式也常常需要跳到某一段）
        if (e.key === 'Escape') { closeToc(); return; }
        if (toc && !toc.hidden) return;   // 總覽開著的時候方向鍵不翻頁
        if (body.getAttribute('data-mode') !== 'present') return;
        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); go(idx + 1); }
        else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(idx - 1); }
        else if (e.key === 'Home') { e.preventDefault(); go(0); }
        else if (e.key === 'End') { e.preventDefault(); go(total - 1); }
    });

    window.addEventListener('resize', rescale);

    /* ── 複製鈕 ── */
    document.addEventListener('click', function (e) {
        var btn = e.target.closest ? e.target.closest('.copy-btn') : null;
        if (!btn) return;
        var box = btn.closest('.copybox');
        var pre = box && box.querySelector('pre');
        if (!pre) return;
        var text = pre.innerText;
        var done = function () {
            var old = btn.textContent;
            btn.textContent = '已複製 ✓';
            btn.classList.add('done');
            setTimeout(function () { btn.textContent = old; btn.classList.remove('done'); }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(done, fallback);
        } else { fallback(); }
        function fallback() {
            // http 或舊瀏覽器沒有 clipboard API，退回 execCommand
            var ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); done(); } catch (err) { btn.textContent = '請手動選取'; }
            document.body.removeChild(ta);
        }
    });

    /* ── 機械擋門：量每一頁有沒有超出 720px ──
       投影模式是固定高度，超出的內容在投影機上會被切掉。
       這件事用眼睛一頁頁看會漏，所以讓它自己報。
       （摺疊起來的 <details> 不算，那是使用者點開才展開的） */
    function lintOverflow() {
        // 🚨 圖片是 loading="lazy"，畫面外的還沒載入時高度是 0 —— 這時候量會【系統性低估】。
        //    所以先強制把所有圖載完再量。量測工具要遷就真相，不是把真相關掉來遷就量測。
        var imgs = Array.prototype.slice.call(stage.querySelectorAll('img'));
        imgs.forEach(function (im) { im.loading = 'eager'; });
        var waits = imgs.map(function (im) {
            if (im.complete && im.naturalHeight) return Promise.resolve();
            return new Promise(function (r) { im.onload = im.onerror = r; });
        });
        Promise.all(waits).then(function () { setTimeout(doLint, 60); });
    }

    function doLint() {
        var bad = [];
        fits.forEach(function (fit, i) {
            var sl = fit.querySelector('.slide');
            // 門檻對齊【使用者看得到的現象】：只要會長出捲軸就算超出，
            // 不要用「容忍 2px」這種對我方便、但對症狀免疫的數字。
            var over = sl.scrollHeight - sl.clientHeight;
            if (over > 0) bad.push({ page: i + 1, over: over, id: sl.id || '(無 id)' });
        });
        if (bad.length) {
            console.warn('🚨 有 ' + bad.length + ' 頁內容超出 720px 畫布，投影時會被切掉：');
            bad.forEach(function (b) {
                console.warn('   第 ' + b.page + ' 頁 [' + b.id + '] 超出 ' + b.over + 'px');
            });
        } else {
            console.log('✅ 全部 ' + total + ' 頁都在 720px 畫布內');
        }
        window.__deckLint = bad;   // 給自動化驗證讀
        window.__deckTotal = total;
    }

    /* ── 啟動 ── */
    var saved = 'read';
    try { saved = localStorage.getItem('dslab-deck-mode') || 'read'; } catch (e) { /* ignore */ }
    buildToc();
    setMode(saved === 'present' ? 'present' : 'read');
    go(0);
    rescale();
    // 圖片/影片載入會改變高度，等資源到齊再量
    window.addEventListener('load', function () { rescale(); lintOverflow(); });
})();


/* ━━━━━━━━━━ 圖片點擊放大 ━━━━━━━━━━
   工作流截圖在 1280×720 的投影片上一定看不清楚，點開才看得到節點名稱。
   實作沿用 0919TC 台中課程那一套。 */
(function () {
    var lb = document.getElementById('lb');
    if (!lb) return;
    var im = document.getElementById('lb-img'), cap = document.getElementById('lb-cap');
    function open(src, alt) {
        im.src = src; im.alt = alt || '';
        cap.textContent = alt || ''; cap.hidden = !alt;
        lb.hidden = false; document.body.classList.add('lb-on');
    }
    function close() {
        lb.hidden = true; im.src = ''; document.body.classList.remove('lb-on');
    }
    document.querySelectorAll('.deck-stage .s-img').forEach(function (el) {
        el.addEventListener('click', function (ev) {
            ev.preventDefault(); ev.stopPropagation();
            open(el.currentSrc || el.src, el.getAttribute('alt'));
        });
    });
    lb.addEventListener('click', close);
    document.addEventListener('keydown', function (ev) {
        if (lb.hidden) return;
        if (ev.key === 'Escape' || ev.key === ' ' || ev.key === 'Enter') {
            ev.preventDefault(); ev.stopImmediatePropagation(); close();
        }
    }, true);
})();

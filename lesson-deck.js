/* ============================================================
   DSLab Lesson · 網頁簡報引擎（南投國中專屬完美版）
   - 固定 1280×720 畫布，用 transform:scale 等比縮放（投影所見即所得）
   - present：逐頁全螢幕投影模式 ／ read：全部攤開捲動閱讀模式
   - 包含：目錄總覽 (TOC Modal)、頂部/底部/懸浮 上一頁/下一頁切換、鍵盤與手機滑動翻頁
   - 支援 6 款淡色系背景切換：淡綠、淡紫、淡紅、淡藍、淺灰、淺橙
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
            if (sl) {
                sl.style.transform = 'scale(' + k + ')';
            }
        });
    }

    /* ── 模式切換 (present / read) ── */
    function setMode(mode) {
        body.setAttribute('data-mode', mode);
        var btn = document.getElementById('mode-btn');
        if (btn) {
            btn.textContent = mode === 'present' ? '📖 閱讀模式' : '🖥️ 簡報模式';
            btn.classList.toggle('is-on', mode === 'present');
        }
        var ctrl = document.getElementById('deck-ctrl');
        if (ctrl) {
            ctrl.style.display = mode === 'present' ? 'flex' : 'none';
        }

        try { localStorage.setItem('dslab-deck-mode', mode); } catch (e) {}
        if (mode === 'present') go(idx);
        requestAnimationFrame(rescale);
    }

    /* ── 翻頁核心邏輯 ── */
    function go(n) {
        idx = Math.max(0, Math.min(total - 1, n));
        fits.forEach(function (f, i) { f.classList.toggle('is-current', i === idx); });

        var posText = String(idx + 1).padStart(2, '0') + ' / ' + String(total).padStart(2, '0');

        var pos = document.getElementById('ctrl-pos');
        if (pos) pos.textContent = posText;

        var cnt = document.getElementById('deck-count');
        if (cnt) cnt.textContent = posText;

        // 底部控制鈕狀態
        var p = document.getElementById('ctrl-prev');
        var x = document.getElementById('ctrl-next');
        if (p) p.disabled = idx === 0;
        if (x) x.disabled = idx === total - 1;

        // 頂部導航鈕狀態
        var pTop = document.getElementById('nav-prev-top');
        var xTop = document.getElementById('nav-next-top');
        if (pTop) pTop.disabled = idx === 0;
        if (xTop) xTop.disabled = idx === total - 1;

        // 螢幕左右側懸浮大按鈕狀態
        var fPrev = document.getElementById('float-prev');
        var fNext = document.getElementById('float-next');
        if (fPrev) fPrev.disabled = idx === 0;
        if (fNext) fNext.disabled = idx === total - 1;

        if (body.getAttribute('data-mode') === 'present') {
            window.scrollTo(0, 0);
        } else {
            fits[idx].scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        markTocCurrent();
    }

    /* ── 頂部與底部按鈕事件綁定 ── */
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

    // 上一頁按鈕集合綁定
    ['ctrl-prev', 'nav-prev-top', 'float-prev'].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.addEventListener('click', function () { go(idx - 1); });
    });

    // 下一頁按鈕集合綁定
    ['ctrl-next', 'nav-next-top', 'float-next'].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.addEventListener('click', function () { go(idx + 1); });
    });

    /* ── 目錄總覽 (TOC Modal) ── */
    var toc = document.getElementById('deck-toc');
    var tocGrid = document.getElementById('deck-toc-grid');

    function buildToc() {
        if (!tocGrid) return;
        tocGrid.innerHTML = '';
        fits.forEach(function (fit, i) {
            var sl = fit.querySelector('.slide');
            if (!sl) return;
            var eyebrow = sl.querySelector('.s-eyebrow');
            var h = sl.querySelector('.s-title, .s-title-xl');

            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'toc-item';
            btn.setAttribute('data-index', i);

            var no = document.createElement('span');
            no.className = 'toc-no';
            no.textContent = String(i + 1).padStart(2, '0');

            var txt = document.createElement('span');
            txt.className = 'toc-txt';

            var eb = document.createElement('span');
            eb.className = 'toc-eyebrow';
            eb.textContent = eyebrow ? eyebrow.textContent.trim() : 'SLIDE';

            var hh = document.createElement('span');
            hh.className = 'toc-h';
            var cleanH = h ? h.textContent.replace(/\s+/g, ' ').trim() : '頁面 ' + (i + 1);
            hh.textContent = cleanH;
            btn.title = cleanH;

            txt.appendChild(eb);
            txt.appendChild(hh);
            btn.appendChild(no);
            btn.appendChild(txt);

            btn.addEventListener('click', function () {
                closeToc();
                if (body.getAttribute('data-mode') === 'present') {
                    go(i);
                } else {
                    fit.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
            tocGrid.appendChild(btn);
        });
    }

    function markTocCurrent() {
        if (!tocGrid) return;
        var items = tocGrid.querySelectorAll('.toc-item');
        for (var i = 0; i < items.length; i++) {
            items[i].classList.toggle('is-current', i === idx);
        }
    }

    function openToc() {
        if (!toc) return;
        buildToc();
        markTocCurrent();
        toc.hidden = false;
        toc.style.display = 'flex';
        var cur = tocGrid && tocGrid.querySelector('.toc-item.is-current');
        if (cur) cur.scrollIntoView({ block: 'center' });
    }

    function closeToc() {
        if (!toc) return;
        toc.hidden = true;
        toc.style.display = 'none';
    }

    // 目錄開關按鈕
    var tocBtn = document.getElementById('toc-btn');
    var tocBtnBottom = document.getElementById('ctrl-toc-bottom');
    var tocClose = document.getElementById('toc-close');

    if (tocBtn) {
        tocBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (toc.hidden || toc.style.display === 'none') {
                openToc();
            } else {
                closeToc();
            }
        });
    }
    if (tocBtnBottom) {
        tocBtnBottom.addEventListener('click', function (e) {
            e.stopPropagation();
            if (toc.hidden || toc.style.display === 'none') {
                openToc();
            } else {
                closeToc();
            }
        });
    }
    if (tocClose) {
        tocClose.addEventListener('click', closeToc);
    }
    if (toc) {
        toc.addEventListener('click', function (e) {
            if (e.target === toc) closeToc();
        });
    }

    /* ── 鍵盤快速鍵翻頁 ── */
    document.addEventListener('keydown', function (e) {
        if (e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;

        if (e.key === 'Escape') {
            closeToc();
            return;
        }

        // 按 T 鍵隨時開啟/關閉目錄總覽
        if ((e.key === 't' || e.key === 'T') && !e.ctrlKey && !e.altKey && !e.metaKey) {
            e.preventDefault();
            if (!toc) return;
            if (toc.hidden || toc.style.display === 'none') {
                openToc();
            } else {
                closeToc();
            }
            return;
        }

        if (toc && (!toc.hidden && toc.style.display !== 'none')) return;
        if (body.getAttribute('data-mode') !== 'present') return;

        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
            e.preventDefault();
            go(idx + 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            e.preventDefault();
            go(idx - 1);
        } else if (e.key === 'Home') {
            e.preventDefault();
            go(0);
        } else if (e.key === 'End') {
            e.preventDefault();
            go(total - 1);
        }
    });

    /* ── 手機觸控左右滑動翻頁 ── */
    var touchStartX = 0;
    var touchStartY = 0;
    document.addEventListener('touchstart', function (e) {
        if (e.touches.length === 1) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }
    }, { passive: true });

    document.addEventListener('touchend', function (e) {
        if (body.getAttribute('data-mode') !== 'present') return;
        if (toc && (!toc.hidden && toc.style.display !== 'none')) return;
        if (e.changedTouches.length === 1) {
            var diffX = e.changedTouches[0].clientX - touchStartX;
            var diffY = e.changedTouches[0].clientY - touchStartY;
            if (Math.abs(diffX) > 40 && Math.abs(diffX) > Math.abs(diffY)) {
                if (diffX < 0) {
                    go(idx + 1); // 向左滑 -> 下一頁
                } else {
                    go(idx - 1); // 向右滑 -> 上一頁
                }
            }
        }
    }, { passive: true });

    window.addEventListener('resize', rescale);

    /* ── 簡報底色主題切換 (淡綠、淡紫、淡紅、淡藍、淺灰、淺橙) ── */
    var VALID_THEMES = ['green', 'purple', 'red', 'blue', 'gray', 'orange'];
    function setTheme(th) {
        if (VALID_THEMES.indexOf(th) === -1) th = 'blue';
        VALID_THEMES.forEach(function (t) {
            body.classList.remove('theme-' + t);
        });
        body.classList.add('theme-' + th);
        try { localStorage.setItem('ntjh-deck-theme', th); } catch (e) {}

        // 同步更新所有底色選取鈕之 active 狀態
        var allBtns = document.querySelectorAll('[data-set-theme]');
        allBtns.forEach(function (btn) {
            btn.classList.toggle('active', btn.getAttribute('data-set-theme') === th);
        });
    }

    // 點擊切換主題
    document.addEventListener('click', function (e) {
        var tBtn = e.target.closest('[data-set-theme]');
        if (tBtn) {
            var th = tBtn.getAttribute('data-set-theme');
            setTheme(th);
        }
    });

    /* ── 啟動 ── */
    var savedTheme = 'blue';
    try { savedTheme = localStorage.getItem('ntjh-deck-theme') || 'blue'; } catch (e) {}
    setTheme(savedTheme);

    var savedMode = 'present';
    try { savedMode = localStorage.getItem('dslab-deck-mode') || 'present'; } catch (e) {}
    buildToc();
    setMode(savedMode === 'present' ? 'present' : 'read');
    go(0);
    rescale();
    window.addEventListener('load', function () { rescale(); });
})();

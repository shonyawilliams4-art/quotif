/* Quoti Live — free quote platform (donation-powered, no subscription)
   Created By: iTechSmart Inc. */
(function () {
  "use strict";

  /* Configure your payment handle here (PayPal.Me, Stripe Payment Link, etc.).
     "{amount}" is replaced with the chosen dollar amount. */
  var DONATE_URL = "https://www.paypal.com/paypalme/quoticonsulting/{amount}";

  var DATA = "assets/data/quotes/";
  var PAGE_SIZE = 12;

  var state = {
    index: null,          // {total, categories:[{slug,name,emoji,count}]}
    cache: {},            // slug -> [quotes]
    view: { mode: "category", slug: null, query: "" },
    results: [],          // [{slug, i, text}]
    shown: 0,
    current: null,        // quote in the big stage {slug, i, text}
    amount: 1
  };

  /* ---------- helpers ---------- */
  function $(id) { return document.getElementById(id); }
  function catName(slug) {
    var c = state.index.categories.find(function (c) { return c.slug === slug; });
    return c ? c.emoji + " " + c.name : slug;
  }
  function loadCat(slug) {
    if (state.cache[slug]) return Promise.resolve(state.cache[slug]);
    return fetch(DATA + slug + ".json").then(function (r) { return r.json(); })
      .then(function (list) { state.cache[slug] = list; return list; });
  }
  function loadAll() {
    return Promise.all(state.index.categories.map(function (c) { return loadCat(c.slug); }));
  }
  function favs() {
    try { return JSON.parse(localStorage.getItem("quoti-live-favs") || "[]"); }
    catch (e) { return []; }
  }
  function setFavs(list) {
    localStorage.setItem("quoti-live-favs", JSON.stringify(list));
    $("ql-fav-count").textContent = list.length;
  }
  function favKey(q) { return q.slug + ":" + q.i; }
  function isFav(q) { return favs().indexOf(favKey(q)) !== -1; }

  function toast(msg) {
    var t = document.querySelector(".ql-toast");
    if (!t) {
      t = document.createElement("div");
      t.className = "ql-toast";
      t.setAttribute("role", "status");
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(t._h);
    t._h = setTimeout(function () { t.classList.remove("show"); }, 2200);
  }

  /* ---------- quote of the day / random ---------- */
  function dayNumber() {
    var now = new Date();
    return Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 864e5) + now.getFullYear() * 366;
  }
  function quoteOfTheDay() {
    var cats = state.index.categories;
    var c = cats[dayNumber() % cats.length];
    return loadCat(c.slug).then(function (list) {
      return { slug: c.slug, i: dayNumber() * 37 % list.length, text: list[dayNumber() * 37 % list.length] };
    });
  }
  function randomQuote() {
    var cats = state.index.categories;
    var c = cats[Math.floor(Math.random() * cats.length)];
    return loadCat(c.slug).then(function (list) {
      var i = Math.floor(Math.random() * list.length);
      return { slug: c.slug, i: i, text: list[i] };
    });
  }

  /* ---------- stage (big card) ---------- */
  function showQuote(q) {
    state.current = q;
    var el = $("ql-text");
    el.style.opacity = 0;
    setTimeout(function () {
      el.textContent = q.text;
      $("ql-cat").textContent = catName(q.slug);
      $("ql-count").textContent = "#" + (q.i + 1) + " of 500 in this category";
      syncFavButton();
      el.style.opacity = 1;
    }, 180);
  }
  function syncFavButton() {
    var b = $("ql-fav");
    if (!state.current) return;
    var on = isFav(state.current);
    b.classList.toggle("ql-on", on);
    b.querySelector("svg").style.fill = on ? "currentColor" : "none";
    b.lastChild.textContent = on ? " Saved" : " Save";
  }

  /* ---------- browse / results ---------- */
  function renderCats() {
    var wrap = $("ql-cats");
    wrap.innerHTML = "";
    state.index.categories.forEach(function (c) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "ql-pill";
      b.setAttribute("role", "tab");
      b.dataset.slug = c.slug;
      b.innerHTML = c.emoji + " " + c.name + ' <span class="ql-badge">' + c.count + "</span>";
      b.addEventListener("click", function () { openCategory(c.slug); });
      wrap.appendChild(b);
    });
  }
  function markActivePill() {
    document.querySelectorAll(".ql-pill").forEach(function (p) {
      p.classList.toggle("active", state.view.mode === "category" && p.dataset.slug === state.view.slug);
    });
  }
  function openCategory(slug) {
    state.view = { mode: "category", slug: slug, query: "" };
    $("ql-search").value = "";
    loadCat(slug).then(function (list) {
      state.results = list.map(function (text, i) { return { slug: slug, i: i, text: text }; });
      resetResults();
    });
  }
  function openFavorites() {
    state.view = { mode: "favorites", slug: null, query: "" };
    var keys = favs();
    if (!keys.length) {
      state.results = [];
      resetResults();
      toast("No favorites yet — tap Save on any quote.");
      return;
    }
    var slugs = {};
    keys.forEach(function (k) { slugs[k.split(":")[0]] = true; });
    Promise.all(Object.keys(slugs).map(loadCat)).then(function () {
      state.results = keys.map(function (k) {
        var parts = k.split(":");
        var i = parseInt(parts[1], 10);
        return { slug: parts[0], i: i, text: (state.cache[parts[0]] || [])[i] || "" };
      }).filter(function (q) { return q.text; });
      resetResults();
    });
  }
  function runSearch(query) {
    state.view = { mode: "search", slug: null, query: query };
    var resultsEl = $("ql-results");
    resultsEl.innerHTML = '<p class="muted ql-loading">Searching all 10,000 quotes…</p>';
    loadAll().then(function () {
      var ql = query.toLowerCase();
      var out = [];
      state.index.categories.forEach(function (c) {
        state.cache[c.slug].forEach(function (text, i) {
          if (text.toLowerCase().indexOf(ql) !== -1) out.push({ slug: c.slug, i: i, text: text });
        });
      });
      state.results = out;
      resetResults();
      toast(out.length ? out.length.toLocaleString() + " quotes found" : "No matches — try another word");
    });
  }
  function resetResults() {
    state.shown = 0;
    $("ql-results").innerHTML = "";
    markActivePill();
    renderMore();
  }
  function renderMore() {
    var wrap = $("ql-results");
    var slice = state.results.slice(state.shown, state.shown + PAGE_SIZE);
    slice.forEach(function (q) {
      var card = document.createElement("figure");
      card.className = "card ql-mini";
      var saved = isFav(q);
      card.innerHTML =
        '<blockquote>' + q.text + "</blockquote>" +
        '<figcaption><span class="ql-mini-cat">' + catName(q.slug) + "</span>" +
        '<span class="ql-mini-actions">' +
        '<button type="button" class="ql-icon-btn" data-act="copy" title="Copy" aria-label="Copy quote">⧉</button>' +
        '<button type="button" class="ql-icon-btn' + (saved ? " ql-on" : "") + '" data-act="fav" title="Save" aria-label="Save to favorites">' + (saved ? "♥" : "♡") + "</button>" +
        '<button type="button" class="ql-icon-btn" data-act="stage" title="Open large" aria-label="Open large">⤢</button>' +
        "</span></figcaption>";
      card.addEventListener("click", function (e) {
        var act = e.target.getAttribute && e.target.getAttribute("data-act");
        if (act === "copy") copyQuote(q);
        if (act === "fav") { toggleFav(q); e.target.classList.toggle("ql-on"); e.target.textContent = isFav(q) ? "♥" : "♡"; }
        if (act === "stage") { showQuote(q); document.getElementById("daily").scrollIntoView({ behavior: "smooth" }); }
      });
      wrap.appendChild(card);
    });
    state.shown += slice.length;
    $("ql-more").hidden = state.shown >= state.results.length;
    if (!state.results.length) {
      wrap.innerHTML = '<p class="muted ql-loading">' +
        (state.view.mode === "favorites" ? "Nothing saved yet — your favorites will live here." : "No quotes to show.") + "</p>";
    }
  }

  /* ---------- actions ---------- */
  function copyQuote(q) {
    var text = "“" + q.text + "” — Quoti Live";
    (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject())
      .then(function () { toast("Copied to clipboard"); })
      .catch(function () { toast("Press Ctrl+C to copy"); });
  }
  function shareQuote(q) {
    var text = "“" + q.text + "” — Quoti Live";
    if (navigator.share) {
      navigator.share({ text: text, url: location.href }).catch(function () {});
    } else {
      window.open("https://twitter.com/intent/tweet?text=" + encodeURIComponent(text), "_blank", "noopener");
    }
  }
  function toggleFav(q) {
    var list = favs();
    var k = favKey(q);
    var at = list.indexOf(k);
    if (at === -1) { list.push(k); toast("Saved to favorites"); }
    else { list.splice(at, 1); toast("Removed from favorites"); }
    setFavs(list);
    if (state.current && favKey(state.current) === k) syncFavButton();
  }

  /* ---------- image card download ---------- */
  function wrapText(ctx, text, maxWidth) {
    var words = text.split(" ");
    var lines = [];
    var line = "";
    words.forEach(function (w) {
      var test = line ? line + " " + w : w;
      if (ctx.measureText(test).width > maxWidth && line) { lines.push(line); line = w; }
      else { line = test; }
    });
    if (line) lines.push(line);
    return lines;
  }
  function downloadImage(q) {
    var c = document.createElement("canvas");
    c.width = 1080; c.height = 1080;
    var x = c.getContext("2d");
    var g = x.createLinearGradient(0, 0, 1080, 1080);
    g.addColorStop(0, "#14100A");
    g.addColorStop(1, "#0B0906");
    x.fillStyle = g;
    x.fillRect(0, 0, 1080, 1080);
    var glow = x.createRadialGradient(830, 160, 40, 830, 160, 620);
    glow.addColorStop(0, "rgba(221,180,74,.22)");
    glow.addColorStop(1, "rgba(221,180,74,0)");
    x.fillStyle = glow;
    x.fillRect(0, 0, 1080, 1080);
    x.strokeStyle = "#A8791A";
    x.lineWidth = 3;
    x.strokeRect(42, 42, 996, 996);
    x.fillStyle = "#E9C963";
    x.font = "220px Georgia, serif";
    x.fillText("“", 70, 280);
    x.fillStyle = "#F6F1E4";
    var size = q.text.length > 150 ? 44 : q.text.length > 90 ? 52 : 62;
    x.font = "italic " + size + "px Georgia, serif";
    var lines = wrapText(x, q.text, 860);
    var lh = size * 1.42;
    var startY = 540 - (lines.length - 1) * lh / 2;
    lines.forEach(function (l, i) { x.fillText(l, 110, startY + i * lh); });
    x.fillStyle = "#DDB44A";
    x.font = "600 30px Georgia, serif";
    x.fillText(catName(q.slug).replace(/^\S+\s/, ""), 110, 950);
    x.fillStyle = "#A2977E";
    x.font = "26px Georgia, serif";
    x.textAlign = "right";
    x.fillText("Quoti Live • free forever", 970, 950);
    x.textAlign = "left";
    var a = document.createElement("a");
    a.download = "quoti-live-quote.png";
    a.href = c.toDataURL("image/png");
    a.click();
    toast("Image downloaded — post it anywhere");
  }

  /* ---------- donation ---------- */
  function bindDonate() {
    var amtLabel = $("ql-donate-amt");
    var custom = $("ql-custom-amt");
    document.querySelectorAll(".ql-amt").forEach(function (b) {
      b.addEventListener("click", function () {
        state.amount = parseInt(b.dataset.amount, 10);
        custom.value = "";
        document.querySelectorAll(".ql-amt").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
        amtLabel.textContent = "$" + state.amount;
      });
    });
    custom.addEventListener("input", function () {
      var v = Math.max(1, Math.floor(Number(custom.value) || 0));
      if (custom.value) {
        state.amount = v;
        amtLabel.textContent = "$" + v;
        document.querySelectorAll(".ql-amt").forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
      }
    });
    $("ql-donate-btn").addEventListener("click", function () {
      var url = DONATE_URL.replace("{amount}", String(state.amount || 1));
      window.open(url, "_blank", "noopener");
      toast("Thank you! Opening secure donation page…");
    });
  }

  /* ---------- boot ---------- */
  function boot() {
    if (!$("ql-stage")) return; // not on Quoti Live page
    fetch(DATA + "index.json")
      .then(function (r) { return r.json(); })
      .then(function (idx) {
        state.index = idx;
        renderCats();
        setFavs(favs());
        quoteOfTheDay().then(showQuote);
        openCategory(idx.categories[dayNumber() % idx.categories.length].slug);
      })
      .catch(function () {
        $("ql-text").textContent = "The quote vault could not be loaded. Please refresh.";
      });

    $("ql-random").addEventListener("click", function () { randomQuote().then(showQuote); });
    $("ql-copy").addEventListener("click", function () { if (state.current) copyQuote(state.current); });
    $("ql-share").addEventListener("click", function () { if (state.current) shareQuote(state.current); });
    $("ql-fav").addEventListener("click", function () { if (state.current) toggleFav(state.current); });
    $("ql-image").addEventListener("click", function () { if (state.current) downloadImage(state.current); });
    $("ql-more").addEventListener("click", renderMore);
    $("ql-favs-view").addEventListener("click", openFavorites);

    var searchTimer;
    $("ql-search").addEventListener("input", function (e) {
      clearTimeout(searchTimer);
      var v = e.target.value.trim();
      searchTimer = setTimeout(function () {
        if (v.length >= 2) runSearch(v);
        else if (!v && state.index) openCategory(state.index.categories[0].slug);
      }, 350);
    });

    bindDonate();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();

/* Quoti Consulting — site behavior
   Created By: iTechSmart Inc. */
(function () {
  "use strict";

  /* ---------- Theme (light / dark) ---------- */
  const root = document.documentElement;
  const stored = localStorage.getItem("quoti-theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initial = stored || (prefersDark ? "dark" : "light");
  root.setAttribute("data-theme", initial);

  function bindThemeToggle() {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        localStorage.setItem("quoti-theme", next);
      });
    });
  }

  /* ---------- Mobile nav ---------- */
  function bindNav() {
    const burger = document.querySelector(".nav-burger");
    const nav = document.querySelector(".main-nav");
    if (!burger || !nav) return;
    burger.addEventListener("click", function () {
      const open = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("open"); });
    });
  }

  /* ---------- Header scroll state ---------- */
  function bindHeader() {
    const header = document.querySelector(".site-header");
    if (!header) return;
    const onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Scroll reveal ---------- */
  function bindReveal() {
    const els = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || !els.length) {
      els.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Animated counters ---------- */
  function bindCounters() {
    const nums = document.querySelectorAll("[data-count]");
    if (!nums.length) return;
    const animate = function (el) {
      const target = parseFloat(el.getAttribute("data-count"));
      const suffix = el.getAttribute("data-suffix") || "";
      const prefix = el.getAttribute("data-prefix") || "";
      const dur = 1600;
      const start = performance.now();
      const step = function (now) {
        const p = Math.min((now - start) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        const val = Math.round(target * eased);
        el.textContent = prefix + val.toLocaleString() + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          animate(e.target);
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.4 });
    nums.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Forms (progressive placeholder) ---------- */
  function bindForms() {
    document.querySelectorAll("form[data-quoti-form]").forEach(function (form) {
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        const success = form.querySelector(".form-success") ||
          form.parentElement.querySelector(".form-success");
        if (success) {
          success.classList.add("visible");
          success.scrollIntoView({ behavior: "smooth", block: "center" });
        }
        form.querySelectorAll("input, select, textarea, button").forEach(function (el) {
          el.disabled = true;
        });
      });
    });
  }

  /* ==================================================
     Motion layer — parallax, split-text, spotlight,
     tilt, magnetic buttons, scroll progress, smart header
     ================================================== */
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Scroll progress bar ---------- */
  function bindProgress() {
    if (reduceMotion) return;
    const bar = document.createElement("div");
    bar.className = "scroll-progress";
    bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);
    let ticking = false;
    const update = function () {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ")";
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- Smart header (hide on down, show on up) ---------- */
  function bindSmartHeader() {
    const header = document.querySelector(".site-header");
    const nav = document.querySelector(".main-nav");
    if (!header || reduceMotion) return;
    let lastY = window.scrollY;
    window.addEventListener("scroll", function () {
      const y = window.scrollY;
      if (nav && nav.classList.contains("open")) { lastY = y; return; }
      if (y > 340 && y > lastY + 6) header.classList.add("hide");
      else if (y < lastY - 6 || y < 340) header.classList.remove("hide");
      lastY = y;
    }, { passive: true });
  }

  /* ---------- Parallax (uses composable `translate`) ---------- */
  function bindParallax() {
    if (reduceMotion) return;
    const els = [];
    document.querySelectorAll(".hero-mark-watermark, .orb").forEach(function (el) {
      const speed = el.classList.contains("orb") ? 0.08 : 0.14;
      const rect = el.getBoundingClientRect();
      els.push({ el: el, speed: speed, base: rect.top + window.scrollY, h: rect.height });
    });
    if (!els.length) return;
    let ticking = false;
    const update = function () {
      const vhMid = window.innerHeight / 2;
      els.forEach(function (o) {
        const center = o.base + o.h / 2 - window.scrollY;
        const y = (center - vhMid) * o.speed;
        o.el.style.translate = "0 " + y.toFixed(1) + "px";
      });
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", function () {
      els.forEach(function (o) {
        o.el.style.translate = "0 0";
        const rect = o.el.getBoundingClientRect();
        o.base = rect.top + window.scrollY;
        o.h = rect.height;
      });
      update();
    });
    update();
  }

  /* ---------- Word-by-word heading reveal ---------- */
  function bindSplitText() {
    if (reduceMotion || !("IntersectionObserver" in window)) return;
    const headings = document.querySelectorAll("main h1, main section > .container h2, main .container .center h2, main .cta-band h2, main .kicker-row h2, main .split-target");
    let seen = new Set();
    const split = function (h) {
      if (seen.has(h)) return;
      seen.add(h);
      let i = 0;
      const frag = document.createDocumentFragment();
      const words = function (text, extraClass) {
        text.split(/(\s+)/).forEach(function (tok) {
          if (!tok) return;
          if (/^\s+$/.test(tok)) { frag.appendChild(document.createTextNode(tok)); return; }
          const s = document.createElement("span");
          s.className = extraClass ? extraClass + " w" : "w";
          s.style.setProperty("--wi", i++);
          s.textContent = tok;
          frag.appendChild(s);
        });
      };
      Array.prototype.slice.call(h.childNodes).forEach(function (node) {
        if (node.nodeType === 3) {
          words(node.textContent, "");
        } else if (node.nodeName === "BR") {
          frag.appendChild(node.cloneNode());
        } else if (node.classList && ["gold", "blue", "royal", "purple"].some(function (c) { return node.classList.contains(c); })) {
          // flatten gradient phrases into per-word gradient spans so text wraps naturally
          words(node.textContent, ["gold", "blue", "royal", "purple"].filter(function (c) { return node.classList.contains(c); })[0]);
        } else {
          const el = node.cloneNode(true);
          el.classList.add("w");
          el.style.setProperty("--wi", i++);
          frag.appendChild(el);
        }
      });
      h.textContent = "";
      h.appendChild(frag);
      ["reveal", "reveal-d1", "reveal-d2", "reveal-d3", "reveal-d4", "in"].forEach(function (c) { h.classList.remove(c); });
      h.classList.add("split-heading");
    };
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.3 });
    headings.forEach(function (h) { split(h); io.observe(h); });
  }

  /* ---------- Cursor spotlight on cards ---------- */
  function bindSpotlight() {
    if (window.matchMedia("(hover: none)").matches) return;
    document.querySelectorAll(".card").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        const r = card.getBoundingClientRect();
        card.style.setProperty("--mx", (e.clientX - r.left) + "px");
        card.style.setProperty("--my", (e.clientY - r.top) + "px");
      });
    });
  }

  /* ---------- 3D tilt on pricing & quote cards ---------- */
  function bindTilt() {
    if (reduceMotion || window.matchMedia("(hover: none)").matches) return;
    document.querySelectorAll(".price-card, .quote-card").forEach(function (card) {
      card.addEventListener("pointerenter", function () {
        card.style.transition = "transform .15s ease-out, border-color .4s, box-shadow .4s";
      });
      card.addEventListener("pointermove", function (e) {
        const r = card.getBoundingClientRect();
        const dx = (e.clientX - r.left) / r.width - 0.5;
        const dy = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = "perspective(950px) rotateX(" + (-dy * 5).toFixed(2) + "deg) rotateY(" + (dx * 5).toFixed(2) + "deg) translateY(-6px)";
      });
      card.addEventListener("pointerleave", function () {
        card.style.transition = "";
        card.style.transform = "";
      });
    });
  }

  /* ---------- Magnetic gold buttons ---------- */
  function bindMagnetic() {
    if (reduceMotion || window.matchMedia("(hover: none)").matches) return;
    document.querySelectorAll(".btn-gold").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        const r = btn.getBoundingClientRect();
        const dx = (e.clientX - (r.left + r.width / 2)) * 0.15;
        const dy = (e.clientY - (r.top + r.height / 2)) * 0.3;
        btn.style.translate = Math.max(-6, Math.min(6, dx)).toFixed(1) + "px " + Math.max(-5, Math.min(5, dy)).toFixed(1) + "px";
      });
      btn.addEventListener("pointerleave", function () {
        btn.style.translate = "0 0";
      });
    });
  }

  /* ---------- Footer year ---------- */
  function bindYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindThemeToggle();
    bindNav();
    bindHeader();
    bindReveal();
    bindCounters();
    bindForms();
    bindYear();
    bindProgress();
    bindSmartHeader();
    bindParallax();
    bindSplitText();
    bindSpotlight();
    bindTilt();
    bindMagnetic();
  });
})();

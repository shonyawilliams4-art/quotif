/* Quoti Consulting — site behavior
   Created By: iTechSmart Inc. */
(function () {
  "use strict";

  /* ---------- Theme (light / dark) ---------- */
  const root = document.documentElement;
  const stored = localStorage.getItem("quoti-theme");
  const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
  const initial = stored || (prefersLight ? "light" : "dark");
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
  });
})();

/* EarningMoneyOnline, Liquid Glass behaviour. No build step. gsap is optional. */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var root = document.documentElement.getAttribute("data-root") || "/preview/";

  /* pointer light on glass */
  document.addEventListener("pointermove", function (e) {
    var el = e.target.closest && e.target.closest(".lit");
    if (!el) return;
    var r = el.getBoundingClientRect();
    el.style.setProperty("--x", (e.clientX - r.left) + "px");
    el.style.setProperty("--y", (e.clientY - r.top) + "px");
  }, { passive: true });

  /* motion, only when gsap arrived and the visitor allows motion */
  function motion() {
    var g = window.gsap;
    if (!g || reduce) return;
    g.utils.toArray(".sky i").forEach(function (b, i) {
      g.to(b, { x: "random(-12,12,1)vw", y: "random(-10,10,1)vh", scale: "random(.85,1.2)",
        duration: 14 + i * 4, ease: "sine.inOut", repeat: -1, yoyo: true, repeatRefresh: true });
    });
    var stage = document.querySelector(".stage");
    if (!stage) return;
    var line = stage.querySelector(".ln"), area = stage.querySelector(".ar"),
        dot = stage.querySelector(".dot"), coin = stage.querySelector(".coin"),
        rim = stage.querySelector(".coin-rim"), chips = stage.querySelectorAll(".fc");
    var len = line.getTotalLength();
    g.set(line, { strokeDasharray: len, strokeDashoffset: len });
    g.set(area, { opacity: 0 });
    g.set(chips, { opacity: 0, y: 12 });
    var tl = g.timeline({ delay: 0.2 });
    tl.from(coin, { y: -40, opacity: 0, duration: 0.9, ease: "back.out(1.6)", transformOrigin: "50% 50%" })
      .to(line, { strokeDashoffset: 0, duration: 1.8, ease: "power2.inOut" }, "-=0.3")
      .to(area, { opacity: 1, duration: 0.8 }, "-=0.9")
      .to(chips, { opacity: 1, y: 0, duration: 0.6, stagger: 0.18, ease: "power2.out" }, "-=0.8");
    var pt = { p: 0 };
    tl.to(pt, { p: 1, duration: 1.8, ease: "power2.inOut", onUpdate: function () {
      var q = line.getPointAtLength(pt.p * len); dot.setAttribute("cx", q.x); dot.setAttribute("cy", q.y);
    } }, 1.0);
    g.to(coin, { y: -8, duration: 2.4, ease: "sine.inOut", repeat: -1, yoyo: true, delay: 1.2 });
    g.to(rim, { rotation: 360, transformOrigin: "50% 50%", duration: 18, ease: "none", repeat: -1 });
  }
  if (window.gsap) motion(); else window.addEventListener("load", motion);

  /* search, the homepage input */
  var box = document.getElementById("q");
  if (!box) return;
  var list = document.getElementById("res"), data = null, loading = null, sel = -1;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fmt(d) {
    if (!d) return "";
    var m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], p = d.split("-");
    return (+p[2]) + " " + m[+p[1] - 1] + " " + p[0];
  }
  function load() {
    if (data) return Promise.resolve(data);
    if (loading) return loading;
    loading = fetch(root + "assets/search.json", { cache: "force-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) {
        data = j.map(function (a) { a.k = (a.t + " " + a.c + " " + (a.x || "")).toLowerCase(); return a; });
        return data;
      });
    loading.catch(function () { loading = null; });
    return loading;
  }
  function show(html) { list.innerHTML = html; list.hidden = false; box.setAttribute("aria-expanded", "true"); }
  function hide() { list.hidden = true; sel = -1; box.setAttribute("aria-expanded", "false"); }
  function href(a) { return (window.__EMO_PREVIEW && window.__EMO_PREVIEW[a.u]) ? root + "articles/" + a.u : "/articles/" + a.u; }

  function run() {
    var q = box.value.trim().toLowerCase();
    if (q.length < 2) { hide(); return; }
    show('<p>Loading guides…</p>');
    load().then(function (all) {
      var words = q.split(/\s+/).filter(Boolean);
      var hits = all.filter(function (a) { return words.every(function (w) { return a.k.indexOf(w) > -1; }); })
        .map(function (a) { var t = a.t.toLowerCase(), s = 0; words.forEach(function (w) { if (t.indexOf(w) > -1) s += 2; }); return { a: a, s: s }; })
        .sort(function (x, y) { return y.s - x.s || (y.a.d || "").localeCompare(x.a.d || ""); })
        .slice(0, 8);
      if (!hits.length) {
        show('<p>No guide matches “' + esc(box.value.trim()) + '”. Try <a href="#" data-q="tax">tax</a> or <a href="#" data-q="energy">energy</a>.</p>');
        return;
      }
      sel = -1;
      show(hits.map(function (h, i) {
        var a = h.a;
        return '<a role="option" id="o' + i + '" href="' + href(a) + '"><b>' + esc(a.t) + '</b><span>' + esc(a.c) + (a.d ? " · " + fmt(a.d) : "") + '</span></a>';
      }).join(""));
    }).catch(function () {
      show('<p>Search could not load. Browse the categories below instead.</p>');
    });
  }
  var t;
  box.addEventListener("input", function () { clearTimeout(t); t = setTimeout(run, 90); });
  box.addEventListener("focus", function () { load().catch(function () {}); if (box.value.trim().length > 1) run(); });
  box.addEventListener("keydown", function (e) {
    var opts = list.querySelectorAll("a[role=option]");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      if (!opts.length) return;
      e.preventDefault();
      sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + opts.length) % opts.length;
      opts.forEach(function (o, i) { o.setAttribute("aria-selected", i === sel ? "true" : "false"); });
      box.setAttribute("aria-activedescendant", "o" + sel);
      opts[sel].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter") {
      if (opts.length) { e.preventDefault(); location.href = opts[sel > -1 ? sel : 0].href; }
    } else if (e.key === "Escape") { hide(); }
  });
  list.addEventListener("click", function (e) {
    var a = e.target.closest("a[data-q]");
    if (a) { e.preventDefault(); box.value = a.getAttribute("data-q"); run(); box.focus(); }
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".srch")) hide(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== box && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); box.focus(); }
  });
})();

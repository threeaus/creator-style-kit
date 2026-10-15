/* Creator Style Kit — motion runtime (GSAP, seek-safe, deterministic).
 *
 *   const kit = CSK.create({ tl, root: "#my-comp", style: STYLE_JSON });
 *   kit.textIn(".csk-head .ttl", 1.2);
 *   kit.list(".csk-list li", [2.0, 2.4, 2.8]);
 *   kit.number(".csk-stat .val", 4.1, 1600);
 *   kit.emphasis(".csk-head em", 2.2);
 *   const cover = kit.transition(5.8);      // returns the time the frame is fully covered
 *
 * The same call renders differently per style: style.motion picks the effect.
 * No onUpdate/callbacks and no Math.random — everything is tl.set/tl.to so any
 * frame can be seeked directly. Text scrambles use a seeded PRNG.
 */
(function () {
  const GLYPHS = "01#_/<>{}[]*+=~%$&";

  function rng(seed) { return function () { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  // "cubic(a,b,c,d)" → easing function (CSS cubic-bezier), otherwise pass GSAP ease names through.
  function ease(spec) {
    const m = /^cubic\(([^)]+)\)$/.exec(spec || "");
    if (!m) return spec || "power2.out";
    const [x1, y1, x2, y2] = m[1].split(",").map(Number);
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx, cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    const sx = (t) => ((ax * t + bx) * t + cx) * t, sy = (t) => ((ay * t + by) * t + cy) * t, dx = (t) => (3 * ax * t + 2 * bx) * t + cx;
    return function (x) {
      let t = x;
      for (let i = 0; i < 8; i++) { const e = sx(t) - x; if (Math.abs(e) < 1e-5) break; const d = dx(t); if (Math.abs(d) < 1e-6) break; t -= e / d; }
      return sy(Math.min(1, Math.max(0, t)));
    };
  }

  function create({ tl, root, style }) {
    const R = typeof root === "string" ? document.querySelector(root) : root;
    const M = style.motion, C = style.colors, D = M.dur;
    const E = { enter: ease(M.ease.enter), exit: ease(M.ease.exit), snap: ease(M.ease.snap) };
    const rand = rng(style.seed || 7);
    const all = (sel) => (typeof sel === "string" ? Array.from(R.querySelectorAll(sel)) : Array.isArray(sel) ? sel : sel instanceof Element ? [sel] : Array.from(sel));
    const one = (sel) => all(sel)[0];

    // ---------- splitting ----------
    function chars(el) {
      if (el.dataset.cskSplit === "c") return Array.from(el.querySelectorAll(".ch"));
      // each glyph becomes an inline-block .ch; glyphs of one word (a run without spaces, ≤ 8 chars so long CJK
      // sentences can still wrap) go in a nowrap .wd box, so a line never breaks inside "5.5" or "实测"
      const walk = (node) => {
        Array.from(node.childNodes).forEach((n) => {
          if (n.nodeType === 3) {
            const frag = document.createDocumentFragment();
            for (const tok of n.textContent.split(/(\s+)/)) {
              if (!tok) continue;
              const box = /\s/.test(tok) || [...tok].length > 8 ? frag : frag.appendChild(Object.assign(document.createElement("span"), { className: "wd" }));
              for (const c of tok) { const s = document.createElement("span"); s.className = "ch"; s.textContent = c; box.appendChild(s); }
            }
            n.replaceWith(frag);
          } else if (n.nodeType === 1 && !n.classList.contains("ch")) walk(n);
        });
      };
      walk(el); el.dataset.cskSplit = "c";
      return Array.from(el.querySelectorAll(".ch"));
    }
    function masked(el) {
      if (el.querySelector(":scope > .csk-mask")) return el.querySelector(".csk-in");
      const m = document.createElement("span"); m.className = "csk-mask";
      const i = document.createElement("span"); i.className = "csk-in";
      while (el.firstChild) i.appendChild(el.firstChild);
      m.appendChild(i); el.appendChild(m);
      if (el.dataset.suffix) { i.dataset.suffix = el.dataset.suffix; el.classList.add("csk-sfx-in"); }  // suffix rises with the masked figure
      return i;
    }

    // ---------- shared helpers ----------
    const SVG = "http://www.w3.org/2000/svg";
    const svgEl = (tag, attrs) => { const e = document.createElementNS(SVG, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
    const node = (cls, parent, css) => { const d = document.createElement("i"); d.className = cls; if (css) d.style.cssText = css; if (parent) parent.appendChild(d); return d; };
    const decimals = (v) => (String(v).split(".")[1] || "").length;
    // Count by frame-accurate tl.set steps (exact strings, decimals OK, seek-safe). fps < 30 gives a stepped LCD feel.
    function countSets(el, t, dur, to, easeSpec, fps = 30, from = 0) {
      const dec = decimals(to), fn = typeof easeSpec === "function" ? easeSpec : gsap.parseEase(easeSpec || "power3.out"), n = Math.max(2, Math.round(dur * fps));
      for (let k = 0; k <= n; k++) tl.set(el, { textContent: (from + (to - from) * fn(k / n)).toFixed(dec) }, t + k / fps);
    }
    function lineScribble(el, t, d, width) {
      wrapEmph(el);
      const svg = svgEl("svg", { class: "csk-scribble", viewBox: "0 0 200 30", preserveAspectRatio: "none" });
      const p = svgEl("path", { d, fill: "none", stroke: C.accent, "stroke-width": width, "stroke-linecap": "round", pathLength: 100 });
      p.style.strokeDasharray = "100"; svg.appendChild(p); el.appendChild(svg);
      tl.fromTo(p, { strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, t);
    }
    function boxDraw(el, t, { color, width = 3, keep = true, radius = 0 }) {
      wrapEmph(el);
      const svg = svgEl("svg", { class: "csk-box" }), r = svgEl("rect", { x: 0, y: 0, width: "100%", height: "100%", rx: radius, fill: "none", stroke: color, "stroke-width": width, pathLength: 100 });
      r.style.strokeDasharray = "100"; svg.appendChild(r); el.appendChild(svg);
      tl.fromTo(r, { strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.55, ease: "power2.inOut" }, t);
      if (!keep) tl.to(svg, { opacity: 0, duration: 0.4 }, t + 1.15);
    }
    // 5×7 dot-matrix glyphs for particle numbers
    const DM = {
      0: "01110100011001110101110011000101110", 1: "00100011000010000100001000010001110", 2: "01110100010000100010001000100011111",
      3: "11111000100010000010000011000101110", 4: "00010001100101010010111110001000010", 5: "11111100001111000001000011000101110",
      6: "00110010001000011110100011000101110", 7: "11111000010001000100010000100001000", 8: "01110100011000101110100011000101110",
      9: "01110100011000101111000010001001100", ".": "00000000000000000000000000110001100", "%": "11000110010001000100010001001100011",
    };

    // per-char stagger, capped so a long line never crawls: the whole line is in within D.in + 0.4 s
    const stg = (n) => Math.min(D.charStagger || 0, 0.4 / Math.max(1, n - 1));
    // ---------- text in / out ----------
    const textIns = {
      "blur-rise": (el, t) => { const cs = chars(el); tl.fromTo(cs, { opacity: 0, y: 28, filter: "blur(14px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: D.in, stagger: stg(cs.length), ease: E.enter }, t); },
      "clip-rise": (el, t) => tl.fromTo(masked(el), { yPercent: 108 }, { yPercent: 0, duration: D.in, ease: E.enter }, t),
      "paper-slap": (el, t) => {
        const r = (rand() - 0.5) * 1.6;
        tl.fromTo(el, { opacity: 0, scale: 1.18, rotation: r - 1.2, filter: "blur(10px)" }, { opacity: 1, scale: 1, rotation: r, filter: "blur(0px)", duration: D.in, ease: E.enter, transformOrigin: "30% 60%" }, t);
      },
      "spring-pop": (el, t) => {
        const cs = chars(el);
        cs.forEach((c, i) => { const r = (rand() - 0.5) * 7; tl.fromTo(c, { opacity: 0, scale: 0.55, rotation: r * 2, transformOrigin: "50% 80%" }, { opacity: 1, scale: 1, rotation: r * 0.4, duration: D.in, ease: E.enter }, t + i * stg(cs.length)); });
      },
      "drop-letters": (el, t) => {
        const cs = chars(masked(el));
        tl.fromTo(cs, { yPercent: -125 }, { yPercent: 0, duration: D.in, stagger: stg(cs.length), ease: E.enter }, t);
        // outline echoes above and below big display words only, then they fade back
        if (parseFloat(getComputedStyle(el).fontSize) < 100) return;
        [-1, 1].forEach((dir, k) => {
          const e = el.cloneNode(true); e.classList.add("csk-echo"); e.removeAttribute("id"); e.style.width = el.offsetWidth + "px";
          e.style.position = "absolute";  // the 2nd clone copies el's inline position:relative — keep echoes out of the flow
          el.style.position = el.style.position || "relative"; el.appendChild(e);
          tl.fromTo(e, { opacity: 0, yPercent: 0 }, { opacity: 0.32, yPercent: dir * 92, duration: D.in * 1.2, ease: E.enter }, t + 0.12 + k * 0.05);
          tl.to(e, { opacity: 0, duration: 0.4 }, t + 1.3);
        });
      },
      "type-scramble": (el, t) => {
        const cs = chars(el);
        cs.forEach((c, i) => {
          const real = c.textContent, ti = t + i * D.charStagger;
          tl.set(c, { opacity: 0 }, 0);
          if (/\s/.test(real)) { tl.set(c, { opacity: 1 }, ti); return; }
          tl.set(c, { opacity: 1, textContent: GLYPHS[Math.floor(rand() * GLYPHS.length)], color: C.accent }, ti);
          tl.set(c, { textContent: GLYPHS[Math.floor(rand() * GLYPHS.length)] }, ti + 0.05);
          tl.set(c, { textContent: real, color: "" }, ti + 0.1);
        });
      },
      // Manim "Write": outline strokes on left→right, then the fill floods in (CSS var --wf drives fill + stroke)
      write: (el, t) => {
        const cs = chars(el); el.classList.add("csk-write");
        tl.set(cs, { "--wf": 0, clipPath: "inset(-30% 100% -30% 0%)" }, 0);
        tl.to(cs, { clipPath: "inset(-30% 0% -30% 0%)", duration: D.in * 0.55, stagger: stg(cs.length), ease: "none" }, t);
        tl.to(cs, { "--wf": 1, duration: D.in * 0.7, stagger: stg(cs.length), ease: "power1.inOut" }, t + D.in * 0.4);
      },
      // blueprint: a construction line is ruled first, then the lettering is drafted along it
      "draft-in": (el, t) => {
        const inner = masked(el), g = node("csk-guide", el);
        el.style.position = el.style.position || "relative";
        tl.fromTo(g, { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: 0.4, ease: "none" }, t);
        tl.fromTo(inner, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: D.in, ease: E.enter }, t + 0.15);
        tl.to(g, { opacity: 0.3, duration: 0.3 }, t + 0.15 + D.in);
        // release the mask once drafted so emphasis marks above/below the line (dimension) are not clipped
        tl.set(inner, { clipPath: "none" }, t + 0.16 + D.in); tl.set(inner.parentNode, { overflow: "visible" }, t + 0.16 + D.in);
      },
      // HUD: a scan bar sweeps and leaves the text behind it, then one flicker
      "scan-in": (el, t) => {
        const inner = masked(el), bar = node("csk-scanbar", el);
        el.style.position = el.style.position || "relative";
        tl.set(bar, { opacity: 0 }, 0);
        tl.fromTo(inner, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: D.in, ease: E.enter }, t);
        tl.fromTo(bar, { left: "0%", opacity: 1 }, { left: "100%", duration: D.in, ease: E.enter }, t);
        tl.set(bar, { opacity: 0 }, t + D.in);
        tl.set(inner, { opacity: 0.35 }, t + D.in + 0.03); tl.set(inner, { opacity: 1 }, t + D.in + 0.07);
      },
      // particles: each glyph gathers out of scattered dust
      converge: (el, t) => {
        chars(el).forEach((c) => {
          const a = rand() * Math.PI * 2, r = 110 + rand() * 230;
          tl.fromTo(c, { opacity: 0, x: Math.cos(a) * r, y: Math.sin(a) * r, scale: 0.3, filter: "blur(10px)" }, { opacity: 1, x: 0, y: 0, scale: 1, filter: "blur(0px)", duration: D.in, ease: E.enter }, t + rand() * 0.28);
        });
      },
      // ink wash: glyphs bleed out of the paper, soft and slow
      "ink-bleed": (el, t) => { const cs = chars(el); tl.fromTo(cs, { opacity: 0, filter: "blur(16px)", scale: 1.1, transformOrigin: "50% 60%" }, { opacity: 1, filter: "blur(0px)", scale: 1, duration: D.in, stagger: stg(cs.length), ease: E.enter }, t); },
      // instrument LCD: glyphs switch on with a 2-frame flicker
      "segment-on": (el, t) => {
        const cs = chars(el); cs.forEach((c, i) => { const ti = t + i * stg(cs.length); tl.set(c, { opacity: 0 }, 0); tl.set(c, { opacity: 1 }, ti); tl.set(c, { opacity: 0.2 }, ti + 0.04); tl.set(c, { opacity: 1 }, ti + 0.08); });
      },
      // quiet editorial: glyphs fade up a few pixels
      "fade-up": (el, t) => { const cs = chars(el); tl.fromTo(cs, { opacity: 0, y: 14, filter: "blur(4px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: D.in, stagger: stg(cs.length), ease: E.enter }, t); },
      // Bauhaus: a solid colour block wipes over, the text is behind it when it wipes off
      "slide-block": (el, t) => {
        const inner = masked(el), m = inner.parentNode;
        m.style.display = "inline-block"; m.style.position = "relative"; m.style.verticalAlign = "top";
        const b = node("csk-block", m), half = D.in * 0.5;
        tl.set(inner, { opacity: 0 }, 0);
        tl.fromTo(b, { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: half, ease: E.snap }, t);
        tl.set(inner, { opacity: 1 }, t + half);
        tl.set(b, { transformOrigin: "100% 50%" }, t + half);
        tl.to(b, { scaleX: 0, duration: half, ease: E.snap }, t + half + 0.02);
      },
    };
    function textIn(sel, t, mode) { all(sel).forEach((el, i) => (textIns[mode || M.textIn] || textIns["blur-rise"])(el, t + i * D.lineStagger)); }
    function textOut(sel, t) {
      const els = all(sel);
      const deco = els.flatMap((e) => Array.from(e.querySelectorAll(".csk-uline, .csk-scribble, .csk-echo, .csk-box, .csk-dim, .csk-brk, .csk-seal, .csk-shape")));
      if (deco.length) tl.to(deco, { opacity: 0, duration: 0.15 }, t);
      // explicit exit grammar (newer styles); older styles keep the textIn-derived defaults below
      if (M.textOut === "cut") return tl.set(els, { opacity: 0 }, t);
      if (M.textOut === "fade") return tl.to(els, { opacity: 0, duration: D.out, ease: E.exit }, t);
      if (M.textOut === "sink") return tl.to(els, { opacity: 0, y: 16, duration: D.out, ease: E.exit }, t);
      if (M.textOut === "lift") return tl.to(els, { opacity: 0, y: -24, duration: D.out, ease: E.exit }, t);
      if (M.textOut === "disperse") return tl.to(els, { opacity: 0, scale: 1.04, filter: "blur(14px)", duration: D.out, ease: E.exit }, t);
      if (M.textIn === "clip-rise") return tl.to(els.map(masked), { yPercent: -108, duration: D.out, ease: E.exit }, t);
      if (M.textIn === "type-scramble") return tl.to(els, { opacity: 0, duration: 0.01, stagger: 0.03 }, t);
      if (M.textIn === "drop-letters") return tl.to(els, { yPercent: 40, opacity: 0, duration: D.out, ease: E.exit }, t);
      return tl.to(els, { opacity: 0, y: -18, filter: "blur(8px)", duration: D.out, ease: E.exit }, t);
    }

    // ---------- emphasis ----------
    function wrapEmph(el) { el.classList.add("csk-emph"); return el; }
    const emph = {
      "accent-glint": (el, t) => { tl.to(el, { color: C.accent, duration: 0.35, ease: "power2.out" }, t); tl.fromTo(el, { scale: 1 }, { scale: 1.06, duration: 0.16, yoyo: true, repeat: 1, ease: "power2.out" }, t); },
      "knife-underline": (el, t) => { const u = document.createElement("i"); u.className = "csk-uline"; wrapEmph(el).appendChild(u); tl.fromTo(u, { scaleX: 0 }, { scaleX: 1, duration: 0.32, ease: E.snap }, t); tl.set(el, { attr: { "data-acc": "1" } }, t + 0.32); },
      highlighter: (el, t) => { el.style.backgroundImage = `linear-gradient(${C.accent}, ${C.accent})`; el.style.backgroundRepeat = "no-repeat"; el.style.backgroundPosition = "0 88%"; tl.fromTo(el, { backgroundSize: "0% 46%" }, { backgroundSize: "100% 46%", duration: 0.45, ease: "power2.out" }, t); },
      selection: (el, t) => { el.style.backgroundImage = `linear-gradient(${C.select || "rgba(56,139,253,.4)"}, ${C.select || "rgba(56,139,253,.4)"})`; el.style.backgroundRepeat = "no-repeat"; el.style.backgroundPosition = "0 50%"; tl.fromTo(el, { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.3, ease: "steps(6)" }, t); },
      scribble: (el, t) => {
        wrapEmph(el);
        const ns = "http://www.w3.org/2000/svg", svg = document.createElementNS(ns, "svg"); svg.setAttribute("class", "csk-scribble"); svg.setAttribute("viewBox", "0 0 200 30"); svg.setAttribute("preserveAspectRatio", "none");
        const p = document.createElementNS(ns, "path"); p.setAttribute("d", "M4 18 C 30 6, 52 28, 80 16 S 128 6, 150 18 S 186 24, 196 12"); p.setAttribute("fill", "none"); p.setAttribute("stroke", C.accent); p.setAttribute("stroke-width", "7"); p.setAttribute("stroke-linecap", "round"); p.setAttribute("pathLength", "100");
        p.style.strokeDasharray = "100"; svg.appendChild(p); el.appendChild(svg);
        tl.fromTo(p, { strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.42, ease: "power2.inOut" }, t);
      },
      "recolor-char": (el, t) => { tl.set(el, { attr: { "data-acc": "1" } }, t); tl.fromTo(el, { scale: 1.25 }, { scale: 1, duration: 0.3, ease: "expo.out" }, t); },
      // Manim Circumscribe + Indicate: a box is drawn round the term, the term takes the accent, the box lets go
      circumscribe: (el, t) => { boxDraw(el, t, { color: C.accent, width: 3, keep: false, radius: 6 }); tl.to(el, { color: C.accent, duration: 0.3 }, t + 0.1); tl.fromTo(el, { scale: 1 }, { scale: 1.08, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }, t + 0.1); },
      // paper: a thin \boxed{} frame that stays
      boxed: (el, t) => { boxDraw(el, t, { color: C.accent, width: 2.5, keep: true }); tl.to(el, { color: C.accent, duration: 0.3 }, t + 0.3); },
      // blueprint: a dimension line |←→| opens above the term
      dimension: (el, t) => { wrapEmph(el); const d = node("csk-dim", el); tl.fromTo(d, { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: E.snap }, t); tl.to(el, { color: C.accent, duration: 0.25 }, t + 0.2); },
      // HUD: four corner brackets collapse onto the term (target lock)
      "bracket-lock": (el, t) => {
        wrapEmph(el);
        [["tl", -1, -1], ["tr", 1, -1], ["bl", -1, 1], ["br", 1, 1]].forEach(([k, dx, dy]) => { const b = node("csk-brk " + k, el); tl.fromTo(b, { opacity: 0, x: dx * 26, y: dy * 26 }, { opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power4.out" }, t); });
        tl.set(el, { color: C.accent }, t + 0.3); tl.set(el, { opacity: 0.4 }, t + 0.33); tl.set(el, { opacity: 1 }, t + 0.37);
      },
      // particles / glass: the term lights up from inside
      halo: (el, t) => tl.fromTo(el, { textShadow: `0 0 0px ${C.accent}00` }, { color: C.accent, textShadow: `0 0 34px ${C.accent}88`, duration: 0.6, ease: "power2.out" }, t),
      // ink: the term turns cinnabar and a small seal is pressed beside it
      "seal-stamp": (el, t) => {
        wrapEmph(el); const s = node("csk-seal", el); s.textContent = el.dataset.seal || "要";
        tl.fromTo(s, { opacity: 0, scale: 1.8, rotation: -16 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.26, ease: "power4.in" }, t);
        tl.to(el, { color: C.seal || C.accent, duration: 0.4 }, t + 0.2);
      },
      // glass / aurora: a gradient sweeps through the term
      "gradient-sweep": (el, t) => { tl.set(el, { attr: { "data-grad": "1" } }, t); tl.fromTo(el, { "--gp": "100%" }, { "--gp": "0%", duration: 0.9, ease: "power2.inOut" }, t); },
      // clay serif: a calm hand-drawn underline
      "underline-soft": (el, t) => lineScribble(el, t, "M4 19 C 50 13, 120 12, 196 17", 5),
      // Bauhaus: a primary-colour circle lands behind the term
      "shape-mark": (el, t) => { wrapEmph(el); el.style.isolation = "isolate"; const s = node("csk-shape", el); tl.fromTo(s, { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.45, ease: E.snap }, t); },
      // instrument: the term becomes a lit signal-orange key cap
      "led-tag": (el, t) => { tl.set(el, { attr: { "data-led": "1" } }, t); tl.set(el, { attr: { "data-led": "0" } }, t + 0.05); tl.set(el, { attr: { "data-led": "1" } }, t + 0.1); },
    };
    function emphasis(sel, t, mode) { all(sel).forEach((el) => (emph[mode || M.emphasis] || emph["accent-glint"])(el, t)); }

    // ---------- numbers ----------
    function digits(el, value) {
      const s = String(value); el.innerHTML = "";
      return Array.from(s).map((d) => { const sp = document.createElement("span"); sp.className = "dg"; sp.textContent = d; el.appendChild(sp); return sp; });
    }
    const nums = {
      "scramble-lock": (el, t, v) => {
        const ds = digits(el, v);
        tl.fromTo(el, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.4, ease: E.enter }, t);
        ds.forEach((d, i) => { const real = d.textContent, lock = t + 0.35 + i * 0.1; for (let k = 0, tt = t; tt < lock; k++, tt += 0.05) tl.set(d, { textContent: String(Math.floor(rand() * 10)), color: C.muted }, tt); tl.set(d, { textContent: real, color: "" }, lock); });
      },
      "step-climb": (el, t, v) => { tl.fromTo(masked(el), { yPercent: 108 }, { yPercent: 0, duration: D.in, ease: E.enter }, t); countSets(masked(el), t, 0.9, v, "none", 13); },
      stamp: (el, t, v) => { el.textContent = String(v); el.style.color = C.red || C.accent; tl.fromTo(el, { opacity: 0, scale: 1.7, rotation: -12 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.28, ease: "power4.in" }, t); tl.fromTo(el, { scale: 1 }, { scale: 1.035, duration: 0.08, yoyo: true, repeat: 1 }, t + 0.28); },
      "bubble-count": (el, t, v) => { tl.fromTo(el, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.2)" }, t); countSets(el, t, 1.1, v, "expo.out"); },
      odometer: (el, t, v) => {
        const s = String(v); el.innerHTML = "";
        Array.from(s).forEach((d, i) => {
          if (!/\d/.test(d)) { const sp = document.createElement("span"); sp.className = "dg"; sp.textContent = d; el.appendChild(sp); return; }
          const col = document.createElement("span"); col.className = "dg"; col.style.cssText = "display:inline-block;overflow:hidden;height:0.9em;line-height:0.9;vertical-align:top";
          const strip = document.createElement("span"); strip.style.cssText = "display:block"; strip.innerHTML = Array.from({ length: 20 }, (_, k) => `<span style="display:block;height:0.9em">${k % 10}</span>`).join("");
          col.appendChild(strip); el.appendChild(col);
          tl.fromTo(strip, { y: 0 }, { y: () => -(10 + Number(d)) * col.offsetHeight, duration: 1.1 + i * 0.15, ease: "expo.out" }, t);
        });
        tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.15 }, t);
      },
      // Manim DecimalNumber: a smooth, exact count (keeps decimals)
      "decimal-tracker": (el, t, v) => { tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.25 }, t); countSets(el, t, 1.3, v, "power2.inOut"); },
      // calm count with a soft blur-in (clay, glass)
      "soft-count": (el, t, v) => { tl.fromTo(el, { opacity: 0, filter: "blur(12px)", y: 20 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.7, ease: E.enter }, t); countSets(el, t, 1.4, v, "expo.out"); },
      // data journalism: the figure counts while its bar is drawn against a full-scale track
      "bar-grow": (el, t, v) => {
        const max = Number(el.dataset.max) || (v <= 100 ? 100 : v * 1.25), wrap = node("csk-numbar", null), fill = node("fill", wrap);
        el.after(wrap);
        tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t);
        tl.fromTo(wrap, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t);
        tl.fromTo(fill, { scaleX: 0 }, { scaleX: v / max, duration: 1.2, ease: "power3.out" }, t);
        countSets(el, t, 1.2, v, "power3.out");
      },
      // HUD: a 270° gauge fills to the value, ticks around it
      gauge: (el, t, v) => {
        const max = Number(el.dataset.max) || (v <= 100 ? 100 : v * 1.25), host = el.parentNode;
        const svg = svgEl("svg", { class: "csk-gauge", viewBox: "0 0 100 100" });
        for (let k = 0; k <= 54; k++) { const a = (135 + k * 5) * Math.PI / 180, r1 = k % 6 ? 46.5 : 45, r2 = 48.5; svg.appendChild(svgEl("line", { x1: 50 + r1 * Math.cos(a), y1: 50 + r1 * Math.sin(a), x2: 50 + r2 * Math.cos(a), y2: 50 + r2 * Math.sin(a), class: "tk" })); }
        const track = svgEl("circle", { cx: 50, cy: 50, r: 42, class: "trk", pathLength: 100 }), arc = svgEl("circle", { cx: 50, cy: 50, r: 42, class: "arc", pathLength: 100 });
        [track, arc].forEach((c) => { c.style.strokeDasharray = "75 100"; c.style.transform = "rotate(135deg)"; c.style.transformOrigin = "50% 50%"; svg.appendChild(c); });
        host.insertBefore(svg, host.firstChild);
        tl.fromTo(svg, { opacity: 0, rotation: -30, scale: 0.92 }, { opacity: 1, rotation: 0, scale: 1, duration: 0.6, ease: E.enter }, t - 0.1);
        tl.fromTo(arc, { strokeDasharray: "0 100" }, { strokeDasharray: `${75 * v / max} 100`, duration: 1.3, ease: "power3.out" }, t);
        tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.15 }, t);
        countSets(el, t, 1.3, v, "power3.out");
      },
      // particles: a dust cloud flies in and settles into a dot-matrix figure; the typeset figure stays hidden underneath
      "particle-form": (el, t, v) => {
        const s = String(v) + (el.dataset.suffix || ""), fs = parseFloat(getComputedStyle(el).fontSize), pitch = Math.round(fs * 0.105), dot = Math.round(pitch * 0.72);
        const host = node("csk-pform", el.parentNode); el.style.color = "transparent"; el.classList.add("csk-pform-src");
        let x0 = 0;
        Array.from(s).forEach((ch) => {
          const g = DM[ch]; if (!g) { x0 += pitch * 3; return; }
          for (let k = 0; k < 35; k++) {
            if (g[k] !== "1") continue;
            const d = node("pd", host, `left:${x0 + (k % 5) * pitch}px;top:${Math.floor(k / 5) * pitch}px;width:${dot}px;height:${dot}px`);
            const a = rand() * Math.PI * 2, r = 380 + rand() * 520;
            tl.fromTo(d, { opacity: 0, x: Math.cos(a) * r, y: Math.sin(a) * r, scale: 0.25 }, { opacity: 1, x: 0, y: 0, scale: 1, duration: 1.15, ease: "expo.out" }, t + rand() * 0.4);
          }
          x0 += pitch * (ch === "." ? 3.4 : 6);
        });
        host.style.width = x0 + "px";
      },
      // instrument: LCD self-test (all segments lit) then a stepped 12 fps count
      segment: (el, t, v) => {
        const s = String(v);
        tl.set(el, { opacity: 0 }, 0);
        tl.set(el, { opacity: 1, textContent: s.replace(/\d/g, "8"), color: C.accent }, t);
        tl.set(el, { opacity: 0.25 }, t + 0.08); tl.set(el, { opacity: 1 }, t + 0.16);
        tl.set(el, { color: "" }, t + 0.32);
        countSets(el, t + 0.32, 1.0, v, "power2.out", 12);
      },
      // ink: the figure bleeds in over one dry brush sweep
      "ink-count": (el, t, v) => {
        const host = el.parentNode, svg = svgEl("svg", { class: "csk-brush", viewBox: "0 0 800 160", preserveAspectRatio: "none" });
        const p = svgEl("path", { d: "M30 96 C 180 40, 420 128, 770 60", fill: "none", "stroke-width": 92, "stroke-linecap": "round", pathLength: 100 });
        p.style.strokeDasharray = "100"; svg.appendChild(p); host.insertBefore(svg, host.firstChild);
        tl.fromTo(p, { strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.55, ease: "power3.out" }, t);
        tl.fromTo(el, { opacity: 0, filter: "blur(18px)", scale: 1.06 }, { opacity: 1, filter: "blur(0px)", scale: 1, duration: 1.0, ease: E.enter }, t + 0.15);
        countSets(el, t + 0.15, 1.0, v, "expo.out");
      },
      // Bauhaus: a big primary circle lands, the figure snaps in on top of it
      "geo-count": (el, t, v) => {
        const c = node("csk-geo", el.parentNode);
        el.parentNode.insertBefore(c, el.parentNode.firstChild);
        tl.fromTo(c, { scale: 0 }, { scale: 1, duration: 0.5, ease: E.snap }, t - 0.1);
        tl.fromTo(masked(el), { yPercent: 108 }, { yPercent: 0, duration: D.in, ease: E.snap }, t);
        countSets(masked(el), t, 0.8, v, "power2.out", 15);
      },
    };
    function number(sel, t, v, mode) { all(sel).forEach((el) => (nums[mode || M.number] || nums["scramble-lock"])(el, t, v)); }

    // ---------- lists ----------
    const lists = {
      "rise-dim": (li, t, i, prev) => { tl.fromTo(li, { opacity: 0, y: 34, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: D.in, ease: E.enter }, t); if (prev) tl.to(prev, { opacity: 0.35, duration: 0.4 }, t); },
      "index-snap": (li, t) => {
        const idx = li.querySelector(".idx"), txt = li.querySelector(".txt"), rule = li.querySelector(".rule");
        tl.set(li, { opacity: 1 }, t);
        if (idx) tl.fromTo(masked(idx), { yPercent: 108 }, { yPercent: 0, duration: 0.35, ease: E.snap }, t);
        if (rule) tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "none" }, t + 0.1);
        if (txt) tl.fromTo(masked(txt), { yPercent: 108 }, { yPercent: 0, duration: 0.45, ease: E.snap }, t + 0.16);
      },
      "index-cards": (li, t) => { const r = (rand() - 0.5) * 2.4; tl.fromTo(li, { opacity: 0, scale: 1.14, rotation: r - 1.4, filter: "blur(8px)" }, { opacity: 1, scale: 1, rotation: r, filter: "blur(0px)", duration: D.in, ease: E.enter }, t); },
      "sticker-cards": (li, t) => { const r = (rand() - 0.5) * 6; tl.fromTo(li, { opacity: 0, scale: 0.5, rotation: r * 3 }, { opacity: 1, scale: 1, rotation: r, duration: D.in, ease: E.enter }, t); },
      "slam-alternate": (li, t, i) => { const dir = i % 2 ? 1 : -1; tl.fromTo(li, { opacity: 0, xPercent: dir * 110 }, { opacity: 1, xPercent: 0, duration: 0.42, ease: "expo.out" }, t); tl.fromTo(li, { scale: 1.08 }, { scale: 1, duration: 0.2, ease: "power2.out" }, t + 0.38); },
      "terminal-lines": (li, t) => {
        tl.set(li, { opacity: 1 }, t);
        const idx = li.querySelector(".idx"), txt = li.querySelector(".txt");
        if (idx) { tl.set(idx, { opacity: 0 }, 0); tl.set(idx, { opacity: 1 }, t); }
        if (txt) textIns["type-scramble"](txt, t + 0.08);
      },
      // data journalism / benchmarks: each row is a horizontal bar that grows to li[data-v] (0–100) with its value counting
      "bar-chart": (li, t) => {
        const v = Number(li.dataset.v) || 0, txt = li.querySelector(".txt"), bar = node("csk-lbar", li), val = node("csk-lval", li);
        tl.set(li, { opacity: 1 }, t);
        if (txt) tl.fromTo(masked(txt), { yPercent: 108 }, { yPercent: 0, duration: 0.45, ease: E.enter }, t);
        tl.fromTo(bar, { scaleX: 0 }, { scaleX: v / 100, duration: 0.9, ease: "power3.out" }, t + 0.1);
        tl.fromTo(val, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t + 0.1);
        countSets(val, t + 0.1, 0.9, v, "power3.out");
      },
      // quiet: rows slide in a few pixels and fade (paper, clay)
      "fade-rows": (li, t) => tl.fromTo(li, { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: D.in, ease: E.enter }, t),
      // Manim: rows grow out of their bullet (GrowFromPoint)
      "grow-in": (li, t) => tl.fromTo(li, { opacity: 0, scale: 0.6, transformOrigin: "0% 50%" }, { opacity: 1, scale: 1, duration: D.in, ease: E.enter }, t),
      // blueprint: node pops, leader line is ruled, label is drafted
      "leader-lines": (li, t) => {
        const idx = li.querySelector(".idx"), txt = li.querySelector(".txt"), rule = li.querySelector(".rule");
        tl.set(li, { opacity: 1 }, t);
        if (idx) tl.fromTo(idx, { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(2)" }, t);
        if (rule) tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "none" }, t + 0.08);
        if (txt) textIns["draft-in"](txt, t + 0.12);
      },
      // HUD: rows scan in, value ticks up at the right edge
      readout: (li, t) => {
        const idx = li.querySelector(".idx"), txt = li.querySelector(".txt"), rule = li.querySelector(".rule"), v = li.dataset.v;
        tl.set(li, { opacity: 1 }, t);
        if (idx) textIns["segment-on"](idx, t);
        if (rule) tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: E.enter }, t);
        if (txt) textIns["scan-in"](txt, t + 0.05);
        if (v) { const val = node("csk-lval", li); tl.fromTo(val, { opacity: 0 }, { opacity: 1, duration: 0.1 }, t + 0.1); countSets(val, t + 0.1, 0.7, Number(v), "power2.out", 20); }
      },
      // particles: each row condenses from scattered dust
      "converge-rows": (li, t) => { const a = rand() * Math.PI * 2; tl.fromTo(li, { opacity: 0, x: Math.cos(a) * 160, y: Math.sin(a) * 90, filter: "blur(14px)", scale: 0.9 }, { opacity: 1, x: 0, y: 0, filter: "blur(0px)", scale: 1, duration: D.in, ease: E.enter }, t); },
      // glass: frosted cards rise out of blur, a light sheen runs along the edge
      "glass-cards": (li, t) => {
        const sh = node("csk-sheen", li);
        tl.fromTo(li, { opacity: 0, y: 44, scale: 0.96, filter: "blur(12px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: D.in, ease: E.enter }, t);
        tl.fromTo(sh, { backgroundPosition: "160% 0%" }, { backgroundPosition: "-60% 0%", duration: 1.1, ease: "power2.inOut" }, t + 0.1);
      },
      // isometric: slabs drop onto the stack (skin puts the list on an iso plane; z offsets set per index)
      "iso-stack": (li, t, i) => { const base = i * 120; tl.fromTo(li, { opacity: 0, z: base + 340 }, { opacity: 1, z: base, duration: D.in, ease: E.enter }, t); },
      // Bauhaus: the index shape rotates in, the label slides out from behind a block
      "geo-blocks": (li, t) => {
        const idx = li.querySelector(".idx"), txt = li.querySelector(".txt");
        tl.set(li, { opacity: 1 }, t);
        if (idx) tl.fromTo(idx, { scale: 0, rotation: -120 }, { scale: 1, rotation: 0, duration: 0.45, ease: E.snap }, t);
        if (txt) textIns["slide-block"](txt, t + 0.1);
      },
      // instrument: key caps drop in, get pressed, their LED lights
      "key-press": (li, t) => {
        const idx = li.querySelector(".idx");
        tl.fromTo(li, { opacity: 0, y: -26 }, { opacity: 1, y: 0, duration: 0.28, ease: "power4.out" }, t);
        tl.to(li, { y: 6, duration: 0.06, ease: "power2.in" }, t + 0.3); tl.to(li, { y: 0, duration: 0.12, ease: "power2.out" }, t + 0.36);
        if (idx) tl.set(idx, { attr: { "data-led": "1" } }, t + 0.32);
      },
      // ink: rows bleed in like ink taking to paper
      "ink-rows": (li, t) => tl.fromTo(li, { opacity: 0, filter: "blur(14px)", x: -10 }, { opacity: 1, filter: "blur(0px)", x: 0, duration: D.in, ease: E.enter }, t),
    };
    function list(sel, times, mode) {
      const els = all(sel), fn = lists[mode || M.list] || lists["rise-dim"];
      els.forEach((li) => tl.set(li, { opacity: 0 }, 0));
      els.forEach((li, i) => fn(li, times[i], i, els[i - 1]));
    }

    // ---------- transitions (overlay in .csk-tr) ----------
    let tr = R.querySelector(".csk-tr");
    if (!tr) { tr = document.createElement("div"); tr.className = "csk-tr"; R.appendChild(tr); }
    const mk = (cls, css) => { const d = document.createElement("div"); d.className = cls; if (css) d.style.cssText = css; tr.appendChild(d); return d; };
    const trans = {
      // each returns cover time; `half` = "in" (reveal only), "out" (cover only) or both
      "light-sweep": (t, half) => {
        const b = mk("band"); tl.set(b, { opacity: 0 }, 0);
        tl.fromTo(b, { xPercent: -160, opacity: 1 }, { xPercent: 330, duration: 0.7, ease: "power2.inOut" }, t);
        tl.set(b, { opacity: 0 }, t + 0.71);
        return t + 0.3;
      },
      "column-wipe": (t, half) => {
        const n = 6, w = 1080 / n, ps = Array.from({ length: n }, (_, i) => mk("p", `left:${i * w}px;width:${w + 1}px;transform-origin:50% 0%`));
        if (half !== "in") tl.fromTo(ps, { scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, duration: 0.32, stagger: 0.035, ease: E.snap }, t);
        else tl.set(ps, { scaleY: 1 }, 0);
        const cover = half === "in" ? t : t + 0.32 + 0.035 * (n - 1);
        if (half !== "out") tl.to(ps, { scaleY: 0, transformOrigin: "50% 100%", duration: 0.32, stagger: 0.035, ease: E.snap }, cover + 0.02);
        return cover;
      },
      "sheet-wipe": (t, half) => {
        const s = mk("sheet");
        if (half !== "in") tl.fromTo(s, { xPercent: 105 }, { xPercent: 0, duration: 0.4, ease: "power3.in" }, t); else tl.set(s, { xPercent: 0 }, 0);
        const cover = half === "in" ? t : t + 0.4;
        if (half !== "out") tl.to(s, { xPercent: -110, duration: 0.45, ease: "power3.out" }, cover + 0.04);
        return cover;
      },
      "card-zoom": (t, half) => {
        const c = mk("card");
        tl.set(c, { opacity: 0 }, 0); tl.set(c, { opacity: 1 }, half === "in" ? 0 : t);
        if (half !== "in") tl.fromTo(c, { scale: 0.05, rotation: -8, borderRadius: 120 }, { scale: 1.08, rotation: 0, borderRadius: 0, duration: 0.5, ease: "expo.inOut" }, t); else tl.set(c, { scale: 1.08 }, 0);
        const cover = half === "in" ? t : t + 0.5;
        if (half !== "out") tl.to(c, { scale: 1.6, opacity: 0, duration: 0.45, ease: "power2.out" }, cover + 0.02);
        return cover;
      },
      "ground-slats": (t, half, next) => {
        const n = 5, w = 1080 / n, col = next || C.accent, ss = Array.from({ length: n }, (_, i) => mk("slat", `left:${i * w}px;width:${w + 1}px;background:${col}`));
        if (half !== "in") tl.fromTo(ss, { yPercent: 100 }, { yPercent: 0, duration: 0.38, stagger: 0.04, ease: "expo.in" }, t); else tl.set(ss, { yPercent: 0 }, 0);
        const cover = half === "in" ? t : t + 0.38 + 0.04 * (n - 1);
        if (half !== "out") tl.to(ss, { yPercent: -100, duration: 0.38, stagger: 0.04, ease: "expo.out" }, cover + 0.02);
        return cover;
      },
      "glitch-slice": (t, half) => {
        const scenes = Array.from(R.querySelectorAll(".csk-scene"));
        const bars = [0.18, 0.43, 0.61, 0.77].map((y, i) => mk("bar", `top:${y * 100}%;height:${12 + i * 9}px;opacity:0`));
        const frames = [[26, 6], [-34, -9], [14, 3], [0, 0]];
        frames.forEach(([x, sk], k) => {
          tl.set(scenes, { x, skewX: sk }, t + k / 30);
          bars.forEach((b) => tl.set(b, { opacity: k < 3 ? 0.9 : 0, x: (rand() - 0.5) * 300 }, t + k / 30));
        });
        return t + 0.05;
      },
      // quiet dip to the ground colour (Manim FadeOut/FadeIn, paper, clay)
      dip: (t, half) => {
        const d = mk("dip"), len = Math.max(0.3, D.out);
        if (half !== "in") tl.fromTo(d, { opacity: 0 }, { opacity: 1, duration: len, ease: "power1.in" }, t); else tl.set(d, { opacity: 1 }, 0);
        const cover = half === "in" ? t : t + len;
        if (half !== "out") tl.to(d, { opacity: 0, duration: len + 0.1, ease: "power1.out" }, cover + 0.02);
        return cover;
      },
      // a sheet with a lit leading edge travels down (journal rule, HUD scan line) — edges are styled per skin
      "edge-wipe": (t, half) => {
        const s = mk("sheet edge-y"), len = 0.38;
        if (half !== "in") tl.fromTo(s, { yPercent: -102 }, { yPercent: 0, duration: len, ease: "power3.in" }, t); else tl.set(s, { yPercent: 0 }, 0);
        const cover = half === "in" ? t : t + len;
        if (half !== "out") tl.to(s, { yPercent: 102, duration: len + 0.05, ease: "power3.out" }, cover + 0.03);
        return cover;
      },
      // blueprint: the drawing sheet is pulled across horizontally with a ruled leading edge
      "draft-wipe": (t, half) => {
        const s = mk("sheet edge-x"), len = 0.42;
        if (half !== "in") tl.fromTo(s, { xPercent: -102 }, { xPercent: 0, duration: len, ease: "power2.in" }, t); else tl.set(s, { xPercent: 0 }, 0);
        const cover = half === "in" ? t : t + len;
        if (half !== "out") tl.to(s, { xPercent: 102, duration: len + 0.05, ease: "power2.out" }, cover + 0.03);
        return cover;
      },
      // particles: warp through a dust field
      "particle-warp": (t, half) => {
        const d = mk("dip"), n = 70, dots = Array.from({ length: n }, () => mk("pw"));
        dots.forEach((p, i) => {
          const a = rand() * Math.PI * 2, r0 = 20 + rand() * 80, r1 = 700 + rand() * 600;
          tl.set(p, { opacity: 0 }, 0);
          tl.fromTo(p, { x: Math.cos(a) * r0, y: Math.sin(a) * r0, scale: 0.4, opacity: 0.9 }, { x: Math.cos(a) * r1, y: Math.sin(a) * r1, scale: 1.6, opacity: 0, duration: 0.75, ease: "power2.in" }, t + rand() * 0.15);
        });
        if (half !== "in") tl.fromTo(d, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.in" }, t + 0.1); else tl.set(d, { opacity: 1 }, 0);
        const cover = half === "in" ? t : t + 0.4;
        if (half !== "out") tl.to(d, { opacity: 0, duration: 0.4, ease: "power2.out" }, cover + 0.02);
        return cover;
      },
      // glass: the whole frame frosts over and clears again
      frost: (t, half) => {
        const f = mk("frost"), len = 0.4;
        if (half !== "in") tl.fromTo(f, { backdropFilter: "blur(0px)", opacity: 0 }, { backdropFilter: "blur(48px)", opacity: 1, duration: len, ease: "power2.in" }, t); else tl.set(f, { backdropFilter: "blur(48px)", opacity: 1 }, 0);
        const cover = half === "in" ? t : t + len;
        if (half !== "out") tl.to(f, { backdropFilter: "blur(0px)", opacity: 0, duration: len + 0.1, ease: "power2.out" }, cover + 0.02);
        return cover;
      },
      // isometric: a panel slides along the iso axis (30°)
      "iso-slide": (t, half) => {
        const s = mk("sheet"), len = 0.42;
        if (half !== "in") tl.fromTo(s, { xPercent: -110, yPercent: 63 }, { xPercent: 0, yPercent: 0, duration: len, ease: E.snap }, t); else tl.set(s, { xPercent: 0, yPercent: 0 }, 0);
        const cover = half === "in" ? t : t + len;
        if (half !== "out") tl.to(s, { xPercent: 110, yPercent: -63, duration: len, ease: E.snap }, cover + 0.03);
        return cover;
      },
      // Bauhaus: an accent circle irises open to fill the frame, then closes onto the next layout
      "shape-iris": (t, half) => {
        const c = mk("iris"), len = 0.42;
        if (half !== "in") tl.fromTo(c, { scale: 0 }, { scale: 1, duration: len, ease: E.snap }, t); else tl.set(c, { scale: 1 }, 0);
        const cover = half === "in" ? t : t + len;
        if (half !== "out") { tl.set(c, { transformOrigin: "100% 100%" }, cover + 0.02); tl.to(c, { scale: 0, duration: len, ease: E.snap }, cover + 0.03); }
        return cover;
      },
      // ink: a blot of ink spreads to cover, then dissolves into fresh paper
      "ink-spread": (t, half) => {
        if (!document.getElementById("csk-ink-edge")) {
          const defs = svgEl("svg", { width: 0, height: 0, style: "position:absolute" });
          defs.innerHTML = '<filter id="csk-ink-edge" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.006" numOctaves="3" seed="5"/><feDisplacementMap in="SourceGraphic" scale="260"/></filter>';
          R.appendChild(defs);
        }
        const b = mk("ink"), len = 0.55;
        if (half !== "in") tl.fromTo(b, { scale: 0, opacity: 1 }, { scale: 1, duration: len, ease: "power2.in" }, t); else tl.set(b, { scale: 1, opacity: 1 }, 0);
        const cover = half === "in" ? t : t + len;
        if (half !== "out") tl.to(b, { opacity: 0, duration: 0.55, ease: "power1.out" }, cover + 0.04);
        return cover;
      },
      // instrument: horizontal shutter blades close and open
      shutter: (t, half) => {
        const n = 8, h = 1920 / n, ps = Array.from({ length: n }, (_, i) => mk("blade", `top:${i * h}px;height:${h + 1}px`));
        if (half !== "in") tl.fromTo(ps, { scaleY: 0, transformOrigin: (i) => (i % 2 ? "50% 100%" : "50% 0%") }, { scaleY: 1, duration: 0.26, stagger: 0.025, ease: E.snap }, t); else tl.set(ps, { scaleY: 1 }, 0);
        const cover = half === "in" ? t : t + 0.26 + 0.025 * (n - 1);
        if (half !== "out") tl.to(ps, { scaleY: 0, duration: 0.26, stagger: 0.025, ease: E.snap }, cover + 0.03);
        return cover;
      },
    };
    function transition(t, half, next) { return (trans[M.transition] || trans["light-sweep"])(t, half, next); }

    // ---------- ambient ----------
    function ambient(t0, t1) {
      const scenes = Array.from(R.querySelectorAll(".csk-scene"));
      if (M.camera === "slow-push") tl.fromTo(scenes, { scale: 1 }, { scale: 1.03, duration: t1 - t0, ease: "none" }, t0);
      if (M.camera === "gentle-float") scenes.forEach((s, i) => tl.fromTo(s, { y: -5 }, { y: 5, duration: 1.6, yoyo: true, repeat: Math.max(1, Math.floor((t1 - t0) / 1.6) - 1), ease: "sine.inOut" }, t0));
      const st = R.querySelector(".tex-paper, .tex-halftone");
      if (M.camera === "stutter-texture" && st) tl.fromTo(R.querySelectorAll(".tex-paper, .tex-halftone"), { backgroundPosition: "0px 0px" }, { backgroundPosition: "240px 120px", duration: t1 - t0, ease: `steps(${Math.round((t1 - t0) * 12)})` }, t0);
      R.querySelectorAll(".tape .run").forEach((r, i) => tl.fromTo(r, { x: i % 2 ? -600 : 0 }, { x: i % 2 ? 0 : -600, duration: t1 - t0, ease: "none" }, t0));
      R.querySelectorAll(".csk-caret").forEach((c) => { for (let tt = t0, k = 0; tt < t1; tt += 0.53, k++) tl.set(c, { opacity: k % 2 ? 0 : 1 }, tt); });
      const span = t1 - t0;
      if (M.camera === "drift") tl.fromTo(scenes, { y: 10, scale: 1 }, { y: -10, scale: 1.015, duration: span, ease: "none" }, t0);
      // particle field: seeded dots, each drifting on its own slow line
      R.querySelectorAll(".tex-particles").forEach((f) => {
        const n = Number(f.dataset.n) || 120;
        for (let i = 0; i < n; i++) {
          const s = 2 + rand() * 4, d = node("pf", f, `left:${rand() * 1080}px;top:${rand() * 1920}px;width:${s}px;height:${s}px;opacity:${(0.12 + rand() * 0.5).toFixed(2)}`);
          tl.fromTo(d, { x: 0, y: 0 }, { x: (rand() - 0.5) * 80, y: -(30 + rand() * 110), duration: span, ease: "none" }, t0);
        }
      });
      // liquid blobs: slow sine orbits
      R.querySelectorAll(".tex-blobs .blob").forEach((b, i) => {
        const p = 3.2 + i * 0.9, reps = Math.max(1, Math.ceil(span / p) - 1);
        tl.fromTo(b, { x: (rand() - 0.5) * 120, y: (rand() - 0.5) * 160, scale: 1 }, { x: (rand() - 0.5) * 260, y: (rand() - 0.5) * 300, scale: 1.15, duration: p, yoyo: true, repeat: reps, ease: "sine.inOut" }, t0);
      });
      R.querySelectorAll(".spin").forEach((s, i) => tl.fromTo(s, { rotation: 0 }, { rotation: (i % 2 ? -1 : 1) * 40, duration: span, ease: "none" }, t0));
      R.querySelectorAll(".tex-bp").forEach((g) => tl.fromTo(g, { backgroundPosition: "0px 0px" }, { backgroundPosition: "-48px -24px", duration: span, ease: "none" }, t0));
    }

    function punch(t, amt = 0.12) { const s = R.querySelectorAll(".csk-scene"); tl.fromTo(s, { scale: 1 + amt }, { scale: 1, duration: 4 / 30 * 2, ease: "power2.out", immediateRender: false }, t); }  // immediateRender:false — otherwise every frame before the hit is zoomed

    return { textIn, textOut, emphasis, number, list, transition, ambient, punch, chars, masked, ease: E, rand };
  }

  window.CSK = { create, ease };
})();

/* OFFNORM 3D tee. A lofted tee model whose surface is painted from the approved flat (design 01, round 5):
   raglan seams in thread colour, white lower-sleeve panel on the wearer's right arm only, O centre front,
   wordmark + D3 data block on the back, F and NM at the back hem corners. Colours and details come from OFN_COLS. */
(function () {
  const COLS = window.OFN_COLS, PT = window.OFN_PATHS, TS = 2048, S = TS / 800;
  const PARTS = { sym: [0, 300, 118, 339, 243], f: [0, 175, 416, 261, 224], nm: [0, 481, 416, 308, 224], wm: [1, 179, 673, 781, 83] };
  const INK = "#151617", CHALK = "#F3F4F2";
  let imgs = null; const cache = {};
  const loadImg = (src) => new Promise((r) => { const i = new Image(); i.onload = () => r(i); i.src = src; });
  const hex = (h) => [1, 3, 5].map((j) => parseInt(h.slice(j, j + 2), 16));
  function sprite(part, color) {
    const key = part + color; if (cache[key]) return cache[key];
    const [k, x, y, w, h] = PARTS[part]; const c = document.createElement("canvas"); c.width = w + 6; c.height = h + 6;
    const g = c.getContext("2d"); g.drawImage(imgs[k], x - 3, y - 3, w + 6, h + 6, 0, 0, w + 6, h + 6);
    const d = g.getImageData(0, 0, c.width, c.height), [r, gg, b] = hex(color);
    for (let i = 0; i < d.data.length; i += 4) {
      const a = Math.max(0, Math.min(1, (d.data[i] - 70) / 130));
      d.data[i] = r; d.data[i + 1] = gg; d.data[i + 2] = b; d.data[i + 3] = a * 255;
    }
    g.putImageData(d, 0, 0); return (cache[key] = c);
  }
  function logo(g, part, x, y, w, color) { const sp = sprite(part, color); g.drawImage(sp, x, y, w, (w * sp.height) / sp.width); }
  function seam(g, d, color, w) {
    const p = new Path2D(d); g.lineCap = "round"; g.setLineDash([]); g.strokeStyle = color; g.lineWidth = w; g.stroke(p);
    g.lineCap = "butt"; g.strokeStyle = "rgba(0,0,0,.22)"; g.setLineDash([1.2, 3.2]); g.stroke(p); g.setLineDash([]);
  }
  function stitch(g, d, ink) { g.strokeStyle = ink; g.globalAlpha = 0.3; g.lineWidth = 1.3; g.setLineDash([7, 5]); g.stroke(new Path2D(d)); g.setLineDash([]); g.globalAlpha = 1; }
  function text(g, t, x, y, fs, align, alpha, weight, ink) {
    g.font = `${weight || 500} ${fs}px "IBM Plex Mono", ui-monospace, Menlo, monospace`; g.textAlign = align; g.fillStyle = ink; g.globalAlpha = alpha || 1; g.fillText(t, x, y); g.globalAlpha = 1;
  }
  function dot(g, x, y, r) { g.fillStyle = "#fff"; g.beginPath(); g.arc(x, y, r, 0, 6.3); g.fill(); g.strokeStyle = "rgba(0,0,0,.25)"; g.lineWidth = 0.8; g.stroke(); }
  function drawTex(c, back) {
    const cv = document.createElement("canvas"); cv.width = cv.height = TS; const g = cv.getContext("2d");
    const ink = c.light ? INK : CHALK, dark = c.light ? "#000" : "#fff";
    g.fillStyle = c.body; g.fillRect(0, 0, TS, TS);
    for (let i = 0; i < 90000; i++) { g.fillStyle = Math.random() < 0.5 ? "rgba(255,255,255,.035)" : "rgba(0,0,0,.035)"; g.fillRect(Math.random() * TS, Math.random() * TS, 2, 2); }
    g.save(); g.scale(S, S);
    g.fillStyle = c.panel; g.fill(new Path2D(back ? PT.PANEL_R : PT.PANEL_L));            // wearer's right arm only
    seam(g, PT.RL, c.thread, 4.2); seam(g, PT.RR, c.thread, 4.2); seam(g, back ? PT.PSEAM_R : PT.PSEAM_L, c.thread, 3.4);
    const jx = back ? 800 - 267.5 : 267.5;
    g.save(); g.translate(jx, 241.25); g.rotate(((back ? 50 : -50) * Math.PI) / 180); g.fillStyle = c.thread; g.fillRect(-7, -2.6, 14, 5.2); g.restore();
    dot(g, 204, 352, 3.6); dot(g, 596, 352, 3.6);
    stitch(g, "M138,400 L62,320", dark); stitch(g, "M662,400 L738,320", dark); stitch(g, "M206,690 H594", dark);
    if (!back) {
      logo(g, "sym", 368, 296, 64, ink);
      g.save(); g.translate(566, 648); g.rotate((-3 * Math.PI) / 180); g.fillStyle = c.thread; g.fillRect(0, 0, 34, 20); g.restore();
    } else {
      logo(g, "wm", 300, 226, 200, ink);
      text(g, "OFN—" + c.code + "—001", 300, 266, 6.6, "left", 1, 600, ink); text(g, c.name.toUpperCase(), 300, 276, 5.6, "left", 0.7, 500, ink);
      text(g, c.cond[0] + " / " + c.cond[1], 500, 266, 6.6, "right", 1, 600, ink); text(g, c.cond[2], 500, 276, 5.6, "right", 0.7, 500, ink);
      g.strokeStyle = ink; g.globalAlpha = 0.6; g.lineWidth = 0.6; g.beginPath(); g.moveTo(300, 284); g.lineTo(500, 284); g.stroke(); g.globalAlpha = 1;
      text(g, c.lat.toFixed(4) + "°N  " + c.lon.toFixed(4) + "°E", 400, 295, 6.4, "center", 1, 500, ink);
      logo(g, "f", 248, 632, 40, ink); logo(g, "nm", 504, 632, 48, ink);
    }
    g.restore();
    const t = new THREE.CanvasTexture(cv); t.encoding = THREE.sRGBEncoding; t.anisotropy = 8; return t;
  }
  const sup = (c, n) => Math.sign(c) * Math.pow(Math.abs(c), 2 / n);
  function half(front) {
    const pos = [], uv = [], idx = [];
    function grid(rows, cols, fn) {
      const base = pos.length / 3;
      for (let i = 0; i <= rows; i++) for (let j = 0; j <= cols; j++) {
        const p = fn(i / rows, j / cols); pos.push(p[0], p[1], p[2]);
        const px = front ? p[0] * 555 + 400 : 400 - p[0] * 555, py = 712 - (p[1] + 0.55) * 555; uv.push(px / 800, 1 - py / 800);
      }
      for (let i = 0; i < rows; i++) for (let j = 0; j < cols; j++) { const a = base + i * (cols + 1) + j, b = a + 1, c = a + cols + 1, d = c + 1; idx.push(a, c, b, b, c, d); }
    }
    const A0 = front ? 0 : Math.PI;
    grid(64, 44, (u, v) => {                                   // torso
      const y = -0.55 + u * 1.02; let a, b;
      if (y <= 0.2) { a = 0.365 - 0.012 * ((y + 0.55) / 0.75); b = 0.2; }
      else { const t = (y - 0.2) / 0.27; a = 0.13 + (0.353 - 0.13) * Math.sqrt(Math.max(0, 1 - t * t)); b = 0.2 + (0.115 - 0.2) * t; }
      const th = A0 + v * Math.PI, fold = 0.006 * Math.sin(y * 21 + Math.cos(th) * 5) * (y < 0.15 ? 1 : 0);
      return [a * sup(Math.cos(th), 2.6), y, (b + fold) * sup(Math.sin(th), 2.6)];
    });
    [-1, 1].forEach((sx) => grid(20, 28, (u, v) => {           // sleeves: top edge starts on the shoulder line, no bump
      const x0 = 0.206, y0 = 0.296, x1 = 0.56, y1 = 0.066, L = Math.hypot(x1 - x0, y1 - y0), dx = (x1 - x0) / L, dy = (y1 - y0) / L;
      const cx = x0 + (x1 - x0) * u, cy = y0 + (y1 - y0) * u, r = 0.14 - u * 0.04, ph = A0 + v * Math.PI;
      return [sx * (cx + r * Math.cos(ph) * -dy), cy + r * Math.cos(ph) * dx, r * 0.8 * Math.sin(ph)];
    }));
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
    g.setIndex(idx); g.computeVertexNormals(); return g;
  }
  let GF, GB;
  function tee(c) {
    GF = GF || half(true); GB = GB || half(false);
    const grp = new THREE.Group();
    [[GF, false], [GB, true]].forEach(([geo, back]) => grp.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: drawTex(c, back), roughness: 0.94, metalness: 0, side: THREE.DoubleSide }))));
    const col = new THREE.Mesh(new THREE.TorusGeometry(1, 0.085, 10, 56), new THREE.MeshStandardMaterial({ color: new THREE.Color(c.body).multiplyScalar(0.86), roughness: 0.95 }));
    col.rotation.x = Math.PI / 2; col.scale.set(0.131, 0.116, 0.16); col.position.y = 0.468; grp.add(col);
    return grp;
  }
  function stage() {
    const sc = new THREE.Scene();
    sc.add(new THREE.HemisphereLight(0xffffff, 0x8a9096, 0.78));
    const d = new THREE.DirectionalLight(0xffffff, 0.72); d.position.set(1.6, 2.2, 3); sc.add(d);
    const f = new THREE.DirectionalLight(0xffffff, 0.22); f.position.set(-2.4, 0.4, 1.2); sc.add(f);
    const cam = new THREE.PerspectiveCamera(24, 1, 0.1, 20); cam.position.set(0, 0.02, 3.45); cam.lookAt(0, -0.045, 0);
    return { sc, cam };
  }
  function dispose(grp) { grp.children.forEach((m) => { if (m.material.map) m.material.map.dispose(); m.material.dispose(); }); }
  async function run() {
    if (!window.THREE) return;
    imgs = await Promise.all([loadImg(window.OFN_P8), loadImg(window.OFN_P9)]);
    try { await document.fonts.load('500 16px "IBM Plex Mono"'); await document.fonts.load('600 16px "IBM Plex Mono"'); } catch (e) {}
    // still renders for every collection
    const R = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    R.setSize(900, 900, false); R.outputEncoding = THREE.sRGBEncoding; R.setClearColor(0x000000, 0);
    const { sc, cam } = stage();
    for (const c of COLS) {
      const g = tee(c); sc.add(g);
      for (const view of ["front", "back"]) {
        g.rotation.set(0.05, view === "front" ? 0.42 : Math.PI - 0.42, 0); R.render(sc, cam);
        const el = document.querySelector(`img.r3d[data-code="${c.code}"][data-view="${view}"]`); if (el) el.src = R.domElement.toDataURL("image/png");
      }
      sc.remove(g); dispose(g);
    }
    R.dispose();
    // one model the viewer can turn
    const cv = document.getElementById("tee-live"); if (!cv) return;
    const L = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); L.outputEncoding = THREE.sRGBEncoding; L.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    const st = stage(); let cur = null, rot = 0.42, auto = true, drag = null;
    function size() { const w = cv.clientWidth; L.setSize(w, w, false); }
    function pick(code) {
      if (cur) { st.sc.remove(cur); dispose(cur); }
      cur = tee(COLS.find((c) => c.code === code)); st.sc.add(cur);
      document.querySelectorAll("[data-pick]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.pick === code));
    }
    document.querySelectorAll("[data-pick]").forEach((b) => b.addEventListener("click", () => pick(b.dataset.pick)));
    cv.addEventListener("pointerdown", (e) => { drag = e.clientX; auto = false; cv.setPointerCapture(e.pointerId); });
    cv.addEventListener("pointermove", (e) => { if (drag !== null) { rot += (e.clientX - drag) * 0.012; drag = e.clientX; } });
    cv.addEventListener("pointerup", () => { drag = null; });
    window.addEventListener("resize", size); size(); pick(COLS[0].code);
    const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    (function loop() { if (auto && !still) rot += 0.006; if (cur) cur.rotation.set(0.05, rot, 0); L.render(st.sc, st.cam); requestAnimationFrame(loop); })();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();

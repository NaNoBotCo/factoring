// zeros.js — the explicit formula: add the zeros one wave at a time and watch the primes appear.
// psi(x) = x − Σ x^ρ/ρ − ln 2π − ½ ln(1 − x⁻²), the sum over the zeros ρ = ½ ± iγ.
(function () {
  const cv = document.getElementById("explicit");
  if (!cv) return;
  const out = document.getElementById("explicitout");
  const slider = document.getElementById("nzeros");
  const play = document.getElementById("zplay");
  const base = document.body.dataset.base || "/";
  const css = getComputedStyle(document.documentElement);
  const C = { ink: css.getPropertyValue("--ink").trim(), mute: css.getPropertyValue("--mute").trim(), c0: css.getPropertyValue("--c0").trim(), c1: css.getPropertyValue("--c1").trim(), c2: css.getPropertyValue("--c2").trim(), line: css.getPropertyValue("--line").trim() };
  let gammas = [], truth = null, timer = null;
  const XMAX = 100;

  function primesTo(n) { const s = new Uint8Array(n + 1); const p = []; for (let i = 2; i <= n; i++) { if (!s[i]) { p.push(i); for (let j = i * i; j <= n; j += i) s[j] = 1; } } return p; }
  function psiTrue(x) { let t = 0; for (const p of primesTo(x)) { let pk = p; while (pk <= x) { t += Math.log(p); pk *= p; } } return t; }
  function psiFormula(x, n) {
    if (x < 2) return 0;
    let t = x - Math.log(2 * Math.PI) - 0.5 * Math.log(1 - 1 / (x * x));
    const lx = Math.log(x), sx = Math.sqrt(x);
    for (let i = 0; i < n; i++) {
      const g = gammas[i];
      // 2 Re( x^ρ / ρ ), ρ = ½ + iγ:  x^ρ = √x (cos(γ ln x) + i sin(γ ln x));  1/ρ = (½ − iγ)/(¼ + γ²)
      const re = sx * Math.cos(g * lx), im = sx * Math.sin(g * lx);
      const d = 0.25 + g * g;
      t -= 2 * (re * 0.5 + im * g) / d;
    }
    return t;
  }
  function draw() {
    const n = +slider.value;
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    const L = 44, B = 28, T = 10, R = 10;
    const sx = (x) => L + (x - 2) / (XMAX - 2) * (W - L - R);
    const sy = (y) => H - B - y / 100 * (H - B - T);
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = C.line; ctx.lineWidth = 1;
    for (let y = 0; y <= 100; y += 20) { ctx.beginPath(); ctx.moveTo(L, sy(y)); ctx.lineTo(W - R, sy(y)); ctx.stroke(); ctx.fillStyle = C.mute; ctx.font = "11px ui-monospace, Menlo"; ctx.textAlign = "right"; ctx.fillText(y, L - 6, sy(y) + 4); }
    for (let x = 10; x <= 100; x += 10) { ctx.fillStyle = C.mute; ctx.textAlign = "center"; ctx.fillText(x, sx(x), H - 8); }
    // the truth: a staircase
    ctx.strokeStyle = C.c1; ctx.lineWidth = 2; ctx.beginPath();
    for (let x = 2; x <= XMAX; x++) { const y = truth[x]; if (x === 2) ctx.moveTo(sx(x), sy(y)); else { ctx.lineTo(sx(x), sy(truth[x - 1])); ctx.lineTo(sx(x), sy(y)); } }
    ctx.lineTo(sx(XMAX + 0.99), sy(truth[XMAX])); ctx.stroke();
    // the formula
    ctx.strokeStyle = C.c0; ctx.lineWidth = 2; ctx.beginPath();
    let err = 0, cnt = 0;
    for (let x = 2; x <= XMAX; x += 0.1) { const y = psiFormula(x, n); if (x === 2) ctx.moveTo(sx(x), sy(y)); else ctx.lineTo(sx(x), sy(y)); if (Math.abs(x - Math.round(x)) > 0.2) { err += Math.abs(y - truth[Math.floor(x)]); cnt++; } }
    ctx.stroke();
    ctx.fillStyle = C.c1; ctx.textAlign = "left"; ctx.font = "12px ui-monospace, Menlo"; ctx.fillText("ψ(x): the primes, counted with weight ln p", L + 8, T + 14);
    ctx.fillStyle = C.c0; ctx.fillText(`the formula with ${n} zero${n === 1 ? "" : "s"}`, L + 8, T + 30);
    out.innerHTML = `<div><span class="k">zeros used</span> <span class="good">${n}</span> · <span class="k">average miss between the steps</span> <span class="v">${(err / cnt).toFixed(2)}</span>${n ? ` · <span class="k">highest zero in</span> ${gammas[n - 1].toFixed(2)}` : ""}</div>` +
      `<div class="k">${n === 0 ? "With no zeros the formula is just the line x: the smooth guess, no steps." : n < 10 ? "The first zeros put the big wobbles in. The steps are still soft." : n < 50 ? "Steps forming at every prime and prime power." : "Nearly there — and it took a hundred zeros to draw a hundred numbers' worth of primes."}</div>`;
  }
  fetch(base + "data/zeros.json").then((r) => r.json()).then((d) => {
    gammas = d.gamma;
    truth = []; for (let x = 0; x <= XMAX; x++) truth[x] = psiTrue(x);
    slider.max = gammas.length;
    draw();
  });
  slider.addEventListener("input", draw);
  play.addEventListener("click", () => {
    if (timer) { clearInterval(timer); timer = null; play.textContent = "play"; return; }
    slider.value = 0; play.textContent = "stop";
    timer = setInterval(() => { slider.value = +slider.value + 1; draw(); if (+slider.value >= +slider.max) { clearInterval(timer); timer = null; play.textContent = "play"; } }, 120);
  });
})();

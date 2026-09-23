// period.js — Shor's algorithm, the part you can see: a^x mod N repeats, the period gives
// the factors, and a quantum computer reads the period off the frequency view.
(function () {
  const cv = document.getElementById("period");
  if (!cv) return;
  const fq = document.getElementById("freq");
  const out = document.getElementById("periodout");
  const selN = document.getElementById("pN"), selA = document.getElementById("pa");
  const NS = [15, 21, 33, 35, 39, 51, 55, 57, 65, 77, 85, 91, 95, 119, 143];
  NS.forEach((n) => { const o = document.createElement("option"); o.value = n; o.textContent = n; selN.appendChild(o); });
  const css = getComputedStyle(document.documentElement);
  const C = { ink: css.getPropertyValue("--ink").trim(), mute: css.getPropertyValue("--mute").trim(), c0: css.getPropertyValue("--c0").trim(), c1: css.getPropertyValue("--c1").trim(), c2: css.getPropertyValue("--c2").trim() };
  function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
  function fillA() {
    const N = +selN.value; selA.innerHTML = "";
    for (let a = 2; a < N; a++) if (gcd(a, N) === 1) { const o = document.createElement("option"); o.value = a; o.textContent = a; selA.appendChild(o); }
    selA.value = N === 15 ? 7 : N === 21 ? 2 : selA.options[0].value;
  }
  function run() {
    const N = +selN.value, a = +selA.value;
    const Q = 128;
    const seq = []; let v = 1;
    for (let x = 0; x < Q; x++) { seq.push(v); v = v * a % N; }
    let r = 1; while (seq[r] !== 1) r++;
    // the sequence
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H);
    const bw = W / 64;
    for (let x = 0; x < 64; x++) {
      const h = (seq[x] / N) * (H - 24);
      ctx.fillStyle = x % r === 0 ? C.c0 : C.c1;
      ctx.fillRect(x * bw + 1, H - 18 - h, bw - 2, h);
    }
    ctx.fillStyle = C.mute; ctx.font = "12px ui-monospace, Menlo, monospace"; ctx.textAlign = "left";
    ctx.fillText(`a^x mod N for x = 0 … 63, N = ${N}, a = ${a}: the amber bars are where it comes back to 1, every ${r} steps`, 4, H - 4);
    // the frequency view: DFT of the indicator of the residue at x = 0, over Q points
    const ind = seq.map((s) => (s === 1 ? 1 : 0));
    const fctx = fq.getContext("2d"); const FW = fq.width, FH = fq.height;
    fctx.clearRect(0, 0, FW, FH);
    const mags = [];
    for (let k = 0; k < Q; k++) { let re = 0, im = 0; for (let x = 0; x < Q; x++) if (ind[x]) { re += Math.cos(2 * Math.PI * k * x / Q); im -= Math.sin(2 * Math.PI * k * x / Q); } mags.push(Math.hypot(re, im)); }
    const mx = Math.max(...mags);
    const fw = FW / Q;
    for (let k = 0; k < Q; k++) {
      const h = mags[k] / mx * (FH - 24);
      const peak = mags[k] > 0.5 * mx;
      fctx.fillStyle = peak ? C.c2 : C.mute + "66";
      fctx.fillRect(k * fw, FH - 18 - h, Math.max(1, fw - 1), h);
    }
    fctx.fillStyle = C.mute; fctx.font = "12px ui-monospace, Menlo, monospace";
    fctx.fillText(`what the quantum register reads: peaks every ${Q}/${r} ≈ ${(Q / r).toFixed(1)} — so the period is ${r}`, 4, FH - 4);
    // the classical finish
    let html = `<div><span class="k">period</span> r = <span class="good">${r}</span> <span class="k">(${a}^${r} ≡ 1 mod ${N})</span></div>`;
    if (r % 2) html += `<div class="bad">r is odd — no luck with this a. Shor's algorithm picks another a and tries again; at least half of them work.</div>`;
    else {
      let h = 1; for (let i = 0; i < r / 2; i++) h = h * a % N;
      if (h === N - 1) html += `<div class="bad">a^(r/2) ≡ −1 mod N — the trivial square root. No luck with this a; pick another.</div>`;
      else {
        const g1 = gcd(h - 1, N), g2 = gcd(h + 1, N);
        html += `<div><span class="k">a^(r/2) mod N =</span> ${h}, <span class="k">so</span> ${h}² ≡ 1 <span class="k">and N divides (${h} − 1)(${h} + 1)</span></div>` +
          `<div><span class="k">gcd(${h - 1}, ${N}) =</span> <span class="good">${g1}</span> · <span class="k">gcd(${h + 1}, ${N}) =</span> <span class="good">${g2}</span> · <span class="k">so</span> ${N} = <span class="good">${g1} × ${g2}</span></div>`;
      }
    }
    html += `<div class="k">The only quantum step is reading the period. Everything else is Euclid, and runs on a pencil.</div>`;
    out.innerHTML = html;
  }
  selN.addEventListener("change", () => { fillA(); run(); });
  selA.addEventListener("change", run);
  selN.value = 15; fillA(); run();
})();

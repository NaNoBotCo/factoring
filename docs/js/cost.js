// cost.js — the number field sieve's bill for a key of any size, anchored on the records.
// log10 L(bits) = c (ln N)^(1/3) (ln ln N)^(2/3) / ln 10, c = (64/9)^(1/3); the ratio to
// RSA-250's 2,700 core-years is the estimate. A crude ruler — the papers say so too.
(function () {
  const sl = document.getElementById("bits");
  if (!sl) return;
  const out = document.getElementById("costout");
  const c = Math.cbrt(64 / 9);
  const L = (bits) => { const l = bits * Math.LN2; return c * Math.cbrt(l) * Math.pow(Math.log(l), 2 / 3) / Math.LN10; };
  const anchors = [
    { name: "RSA-250 (2020)", bits: 829, years: 2700, unit: "core-years of a 2.1 GHz Xeon" },
    { name: "RSA-896 (2026)", bits: 896, years: 30, unit: "GPU-years on B200-class parts" },
  ];
  function human(y) {
    if (y < 1 / 365) return `${(y * 365 * 24).toFixed(1)} hours`;
    if (y < 1) return `${(y * 365).toFixed(0)} days`;
    if (y < 1e4) return `${y.toFixed(0)}`;
    return y.toExponential(2);
  }
  function draw() {
    const bits = +sl.value;
    document.getElementById("bitsv").textContent = bits;
    const digits = Math.ceil(bits * Math.LOG10E * Math.LN2);
    let html = `<div><span class="k">${bits} bits ≈ ${digits} digits</span></div>`;
    for (const a of anchors) {
      const ratio = Math.pow(10, L(bits) - L(a.bits));
      const est = a.years * ratio;
      html += `<div><span class="k">scaled from ${a.name}:</span> <span class="${ratio > 1e6 ? "bad" : "good"}">${human(est)}</span> <span class="k">${a.unit}</span> <span class="k">(${ratio >= 1 ? ratio.toExponential(1) + "× harder" : (1 / ratio).toFixed(0) + "× easier"})</span></div>`;
    }
    const secs2048 = 2700 * Math.pow(10, L(2048) - L(829));
    html += `<div class="k">${bits >= 2048 ? "For scale: the RSA-250 team's 2,700 core-years took about a year of wall time on a cluster. Multiply that year by the ratio above." : bits >= 1024 ? "RSA-1024: the number the whole web used until about 2013. The 2026 GPU runs put it within reach of a data-centre fleet; nobody has published one yet." : "Below 1024 bits this has been done, and at 512 bits it costs about $75 of cloud time (2015)."}</div>`;
    out.innerHTML = html;
  }
  sl.addEventListener("input", draw);
  draw();
})();

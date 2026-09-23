// kraitchik.js — two squares that agree mod N. The idea under every sieve since 1926.
// Walk x up from √N, keep the x² − N that break into small primes, find a set whose
// exponents are all even, and gcd the two square roots against N.
(function () {
  const box = document.getElementById("kra");
  if (!box) return;
  const out = document.getElementById("kraout");
  const input = document.getElementById("kran");
  const BASE = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29];

  function factorSmooth(v) {
    const e = new Array(BASE.length).fill(0);
    let r = v;
    for (let i = 0; i < BASE.length; i++) { while (r % BASE[i] === 0) { r /= BASE[i]; e[i]++; } }
    return r === 1 ? e : null;
  }
  function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
  function isqrt(n) { return Math.floor(Math.sqrt(n)); }
  function modmul(a, b, m) { return Number((BigInt(a) * BigInt(b)) % BigInt(m)); }

  // Gaussian elimination over GF(2) on the exponent parities; returns index sets that combine to a square
  function combos(rels) {
    const rows = rels.map((r, i) => ({ bits: r.e.map((x) => x & 1), set: new Set([i]) }));
    const pivots = [];
    const outSets = [];
    for (const row of rows) {
      for (const pv of pivots) {
        if (row.bits[pv.col]) { row.bits = row.bits.map((b, j) => b ^ pv.bits[j]); for (const s of pv.set) row.set.has(s) ? row.set.delete(s) : row.set.add(s); }
      }
      const col = row.bits.findIndex((b) => b);
      if (col < 0) outSets.push(row.set); else pivots.push({ col, bits: row.bits, set: row.set });
    }
    return outSets;
  }

  function run() {
    const N = parseInt(input.value, 10);
    if (!(N > 3) || N > 2e9) { out.innerHTML = `<span class="bad">give me a whole number between 4 and two billion</span>`; return; }
    if (N % 2 === 0) { out.innerHTML = `even — 2 divides it, no sieve needed`; return; }
    const r = isqrt(N);
    if (r * r === N) { out.innerHTML = `${N} = ${r}²`; return; }
    const rels = [];
    const rowsHtml = [];
    for (let x = r + 1; x < r + 400 && rels.length < 24; x++) {
      const v = x * x - N;
      const e = factorSmooth(v);
      if (!e) continue;
      rels.push({ x, v, e });
      const fac = e.map((k, i) => k ? `${BASE[i]}${k > 1 ? "<sup>" + k + "</sup>" : ""}` : "").filter(Boolean).join(" · ");
      rowsHtml.push(`<tr><td class="n">${x}</td><td class="n">${x * x}</td><td class="n">${v}</td><td>${fac}</td><td class="n">${e.map((k) => k & 1).join("")}</td></tr>`);
    }
    let html = `<div class="k">x² − N for x from ${r + 1} up, keeping only values whose primes are all ≤ 29 (${rels.length} found in the first 400):</div>` +
      `<div class="wrap"><table><thead><tr><th class="n">x</th><th class="n">x²</th><th class="n">x² − N</th><th>factored</th><th class="n">parities</th></tr></thead><tbody>${rowsHtml.join("")}</tbody></table></div>`;
    const sets = combos(rels);
    if (!sets.length) { out.innerHTML = html + `<div class="bad">no combination with all-even exponents yet — a bigger factor base or more x would find one</div>`; return; }
    let found = false;
    for (const s of sets) {
      const idx = [...s].sort((a, b) => a - b);
      let X = 1; const E = new Array(BASE.length).fill(0);
      for (const i of idx) { X = modmul(X, rels[i].x, N); rels[i].e.forEach((k, j) => E[j] += k); }
      let Y = 1; E.forEach((k, j) => { for (let t = 0; t < k / 2; t++) Y = modmul(Y, BASE[j], N); });
      const g = gcd(Math.abs(X - Y), N);
      const xs = idx.map((i) => rels[i].x).join(" · ");
      html += `<div style="margin-top:.6rem"><span class="k">combine x =</span> ${xs} <span class="k">→ X ≡</span> ${X}, <span class="k">√(product of the x² − N) ≡</span> ${Y} <span class="k">(mod N)</span>`;
      if (g > 1 && g < N) { html += ` <span class="k">→ gcd(X − Y, N) =</span> <span class="good">${g}</span>, <span class="k">and N = </span><span class="good">${g} × ${N / g}</span></div>`; found = true; break; }
      html += ` <span class="k">→ gcd gives ${g === N ? "N itself" : "1"} — a dud, try the next combination</span></div>`;
    }
    if (!found) html += `<div class="bad">every combination found was a dud (X ≡ ±Y). About half are; more relations would fix it.</div>`;
    out.innerHTML = html;
  }
  document.getElementById("krago").addEventListener("click", run);
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") run(); });
  box.querySelectorAll("[data-n]").forEach((b) => b.addEventListener("click", () => { input.value = b.dataset.n; run(); }));
  run();
})();

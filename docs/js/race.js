// race.js — four old methods on the same number, step counters side by side.
// Which one wins depends on the number's shape, which is the lesson.
(function () {
  const box = document.getElementById("race");
  if (!box) return;
  const out = document.getElementById("raceout");
  const PRESETS = [
    { n: 10007n * 10037n, label: "10007 × 10037 — two primes close together", why: "Fermat's method wins: a² − N is a square after a few steps because the factors straddle the square root." },
    { n: 1009n * 999983n, label: "1009 × 999983 — one small prime, one big", why: "Trial division wins: it only has to count to 1009. Fermat has to walk almost half a million steps." },
    { n: 4294967297n, label: "641 × 6700417 — Euler's Fermat number", why: "Rho finds 641 in a few dozen steps; trial division needs 320. Euler did it by hand in 1732 with a shortcut about the shape of the factors." },
    { n: 2311n * 10007n, label: "2311 × 10007 — a prime with a smooth neighbour", why: "Pollard's p − 1 wins: 2310 = 2·3·5·7·11, so the first factor falls out of one exponentiation with bound 11." },
    { n: 1649n, label: "17 × 97 — Pomerance's example", why: "Everything wins; it is here so you can see all four finish." },
    { n: 1000000007n * 1000000009n, label: "1000000007 × 1000000009 — twin ten-digit primes", why: "Fermat's method finishes in one step; every other method here would take ages. Real key generators keep the two primes far apart for exactly this reason." },
  ];
  const sel = document.getElementById("racepick");
  PRESETS.forEach((p, i) => { const o = document.createElement("option"); o.value = i; o.textContent = p.label; sel.appendChild(o); });
  let timer = null;

  function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
  function isqrt(n) { let x = BigInt(Math.floor(Math.sqrt(Number(n)))); while (x * x > n) x--; while ((x + 1n) * (x + 1n) <= n) x++; return x; }
  function modpow(b, e, m) { let r = 1n; b %= m; while (e > 0n) { if (e & 1n) r = r * b % m; b = b * b % m; e >>= 1n; } return r; }

  // each method is a generator that yields after every step and returns a factor
  function* trial(N) { if (N % 2n === 0n) return 2n; for (let d = 3n; d * d <= N; d += 2n) { yield; if (N % d === 0n) return d; } return N; }
  function* fermat(N) { let a = isqrt(N); if (a * a < N) a++; for (;;) { yield; const b2 = a * a - N; const b = isqrt(b2); if (b * b === b2) return a - b; a++; } }
  function* rho(N) { let x = 2n, y = 2n, c = 1n; const f = (v) => (v * v + c) % N; for (;;) { yield; x = f(x); y = f(f(y)); const g = gcd(x > y ? x - y : y - x, N); if (g === N) { c++; x = y = 2n; continue; } if (g > 1n) return g; } }
  function* pminus1(N) { let a = 2n; for (let k = 2n; k < 100000n; k++) { yield; a = modpow(a, k, N); const g = gcd(a - 1n, N); if (g > 1n && g < N) return g; if (g === N) return null; } return null; }

  function run() {
    if (timer) clearInterval(timer);
    const P = PRESETS[+sel.value]; const N = P.n;
    const lanes = [["trial division", trial(N)], ["Fermat (1643)", fermat(N)], ["Pollard rho (1975)", rho(N)], ["Pollard p − 1 (1974)", pminus1(N)]]
      .map(([name, g]) => ({ name, g, steps: 0, done: null }));
    const cap = 3000000;
    const draw = () => {
      out.innerHTML = `<div class="k">N = ${N.toString()} — ${P.why}</div>` + lanes.map((l) => {
        const w = Math.min(100, 100 * Math.log10(1 + l.steps) / 6.5);
        const tail = l.done === undefined ? `<span class="bad">gave up at ${l.steps.toLocaleString()} steps</span>`
          : l.done === null ? `<span class="v">${l.steps.toLocaleString()} steps…</span>`
          : `<span class="good">${l.done}</span> after <span class="v">${l.steps.toLocaleString()}</span> steps`;
        return `<div class="lane"><span class="k">${l.name}</span><i style="width:${w}%"></i>${tail}</div>`;
      }).join("");
    };
    timer = setInterval(() => {
      let alive = false;
      for (const l of lanes) {
        if (l.done !== null) continue;
        for (let i = 0; i < 4000; i++) {
          const r = l.g.next();
          l.steps++;
          if (r.done) { l.done = r.value === null || r.value === N ? undefined : r.value.toString(); break; }
          if (l.steps >= cap) { l.done = undefined; break; }
        }
        if (l.done === null) alive = true;
      }
      draw();
      if (!alive) { clearInterval(timer); timer = null; }
    }, 16);
    draw();
  }
  sel.addEventListener("change", run);
  document.getElementById("racego").addEventListener("click", run);
  run();
})();

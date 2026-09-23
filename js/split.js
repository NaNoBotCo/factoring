// split.js — make a semiprime, then try to split it. BigInt throughout.
// Making one: two random primes (Miller–Rabin), one multiplication. Splitting one: trial
// division counts up from 2; Pollard's rho walks a pseudo-random path. The counters are
// live so the reader watches the wall arrive.
(function () {
  const $ = (id) => document.getElementById(id);
  const box = $("split");
  if (!box) return;
  const out = $("splitout");
  const bigOut = $("bigout");
  const sizes = box.querySelectorAll("[data-digits]");
  let digits = 6, p = 0n, q = 0n, N = 0n, running = null;

  // ---- arithmetic
  function modpow(b, e, m) { let r = 1n; b %= m; while (e > 0n) { if (e & 1n) r = r * b % m; b = b * b % m; e >>= 1n; } return r; }
  function randBig(bits) {
    const bytes = new Uint8Array(Math.ceil(bits / 8));
    crypto.getRandomValues(bytes);
    let x = 0n; for (const b of bytes) x = (x << 8n) | BigInt(b);
    x &= (1n << BigInt(bits)) - 1n; x |= 1n << BigInt(bits - 1); x |= 1n;   // top and bottom bits set
    return x;
  }
  const SMALL = [3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n, 41n, 43n, 47n];
  function isPrime(n, rounds) {
    if (n < 2n) return false;
    for (const s of SMALL) { if (n === s) return true; if (n % s === 0n) return false; }
    let d = n - 1n, r = 0; while ((d & 1n) === 0n) { d >>= 1n; r++; }
    const bases = rounds || 12;
    for (let i = 0; i < bases; i++) {
      const a = 2n + BigInt(i) * 7n + BigInt(Math.floor(Math.random() * 1000));
      let x = modpow(a % (n - 3n) + 2n, d, n);
      if (x === 1n || x === n - 1n) continue;
      let ok = false;
      for (let j = 1; j < r; j++) { x = x * x % n; if (x === n - 1n) { ok = true; break; } }
      if (!ok) return false;
    }
    return true;
  }
  function randPrime(bits) { for (;;) { const c = randBig(bits); if (isPrime(c)) return c; } }
  function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a < 0n ? -a : a; }
  function isqrt(n) { if (n < 2n) return n; let x = BigInt(Math.floor(Math.sqrt(Number(n)))); while (x * x > n) x--; while ((x + 1n) * (x + 1n) <= n) x++; return x; }
  const fmt = (n) => n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  const bitsFor = (d) => Math.ceil(d * 3.3219) ;

  // ---- make
  function make() {
    stop();
    const t0 = performance.now();
    p = randPrime(bitsFor(digits)); q = randPrime(bitsFor(digits));
    if (p === q) q = randPrime(bitsFor(digits));
    const t1 = performance.now();
    N = p * q;
    const t2 = performance.now();
    out.innerHTML =
      `<div><span class="k">first prime</span> <span class="v">${fmt(p)}</span> <span class="k">(${p.toString().length} digits, found in ${(t1 - t0).toFixed(1)} ms)</span></div>` +
      `<div><span class="k">second prime</span> <span class="v">${fmt(q)}</span></div>` +
      `<div><span class="k">their product</span> <span class="good">${fmt(N)}</span> <span class="k">(${N.toString().length} digits, multiplied in ${(t2 - t1).toFixed(3)} ms)</span></div>` +
      `<div class="k">Now forget the two primes. Try to get them back from the product.</div>`;
    $("trial").disabled = $("rho").disabled = false;
  }

  // ---- trial division, in slices so the page stays alive
  function trial() {
    stop();
    const root = isqrt(N);
    let d = 3n, steps = 0, t0 = performance.now();
    const line = document.createElement("div");
    out.appendChild(line);
    if (N % 2n === 0n) { line.innerHTML = `<span class="k">trial division</span> 2 divides it.`; return; }
    running = setInterval(() => {
      const slice = 40000;
      for (let i = 0; i < slice; i++) {
        if (N % d === 0n) {
          clearInterval(running); running = null;
          line.innerHTML = `<span class="k">trial division</span> found <span class="good">${fmt(d)}</span> after <span class="v">${fmt(BigInt(steps + i + 1))}</span> divisions, ${((performance.now() - t0) / 1000).toFixed(2)} s.`;
          return;
        }
        d += 2n;
      }
      steps += slice;
      const secs = (performance.now() - t0) / 1000;
      const rate = steps / secs;
      const need = Number(root) / 2 / rate;
      line.innerHTML = `<span class="k">trial division</span> <span class="v">${fmt(BigInt(steps))}</span> divisions, ${secs.toFixed(1)} s, at ${fmt(BigInt(Math.round(rate)))} a second. Worst case to the square root at this rate: <span class="bad">${human(need)}</span>.`;
    }, 0);
  }

  // ---- Pollard rho (Brent's cycle finding)
  function rho() {
    stop();
    let c = 1n, y = 2n, r = 1n, qq = 1n, g = 1n, x = y, ys = y, steps = 0;
    const t0 = performance.now();
    const line = document.createElement("div");
    out.appendChild(line);
    const f = (v) => (v * v + c) % N;
    let k = 0n;
    running = setInterval(() => {
      const budget = 20000;
      let used = 0;
      while (used < budget) {
        if (g !== 1n) break;
        // one Brent round
        x = y;
        for (let i = 0n; i < r; i++) y = f(y);
        k = 0n;
        while (k < r && g === 1n) {
          ys = y;
          const lim = (r - k) < 128n ? (r - k) : 128n;
          for (let i = 0n; i < lim; i++) { y = f(y); qq = qq * (x > y ? x - y : y - x) % N; }
          g = gcd(qq, N);
          k += lim; used += Number(lim); steps += Number(lim);
        }
        r *= 2n;
      }
      const secs = (performance.now() - t0) / 1000;
      if (g === N) { // backtrack
        g = 1n;
        do { ys = f(ys); g = gcd(x > ys ? x - ys : ys - x, N); steps++; } while (g === 1n);
      }
      if (g !== 1n && g !== N) {
        clearInterval(running); running = null;
        line.innerHTML = `<span class="k">Pollard rho</span> found <span class="good">${fmt(g)}</span> after <span class="v">${fmt(BigInt(steps))}</span> steps, ${secs.toFixed(2)} s.`;
        return;
      }
      const rate = steps / secs;
      const expect = Math.sqrt(Number(isqrt(N))) * 1.03;   // about sqrt(p)
      line.innerHTML = `<span class="k">Pollard rho</span> <span class="v">${fmt(BigInt(steps))}</span> steps, ${secs.toFixed(1)} s, at ${fmt(BigInt(Math.round(rate)))} a second. Expected steps about the square root of the smaller prime: <span class="bad">${human(expect / rate)}</span> at this rate.`;
    }, 0);
  }

  function human(secs) {
    if (!isFinite(secs)) return "forever";
    if (secs < 1) return "under a second";
    if (secs < 120) return `${secs.toFixed(0)} seconds`;
    if (secs < 7200) return `${(secs / 60).toFixed(0)} minutes`;
    if (secs < 172800) return `${(secs / 3600).toFixed(1)} hours`;
    const y = secs / 31557600;
    if (y < 1) return `${(secs / 86400).toFixed(0)} days`;
    if (y < 1e6) return `${fmt(BigInt(Math.round(y)))} years`;
    return `${y.toExponential(1)} years (the universe is 1.4e10 years old)`;
  }
  function stop() { if (running) { clearInterval(running); running = null; } }

  // ---- a 2048-bit key, made here
  function big() {
    bigOut.innerHTML = `<span class="k">looking for two 1024-bit primes…</span>`;
    setTimeout(() => {
      const t0 = performance.now();
      const P = randPrime(1024), Q = randPrime(1024);
      const t1 = performance.now();
      const M = P * Q;
      bigOut.innerHTML =
        `<div><span class="k">two 1024-bit primes, found in ${((t1 - t0) / 1000).toFixed(1)} s in this tab</span></div>` +
        `<div><span class="k">their product, ${M.toString().length} digits, ${M.toString(2).length} bits — the shape of an RSA-2048 key</span></div>` +
        `<div style="word-break:break-all;font-size:.78em;line-height:1.5" class="v">${M.toString()}</div>` +
        `<div class="k">Making it: one second. Splitting it: no machine on Earth, as of ${document.body.dataset.asof || "2026"}. That gap is the whole business.</div>`;
    }, 30);
  }

  sizes.forEach((b) => b.addEventListener("click", () => {
    sizes.forEach((x) => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
    digits = +b.dataset.digits; make();
  }));
  $("make").addEventListener("click", make);
  $("trial").addEventListener("click", trial);
  $("rho").addEventListener("click", rho);
  $("stop").addEventListener("click", stop);
  if ($("big")) $("big").addEventListener("click", big);
  make();
})();

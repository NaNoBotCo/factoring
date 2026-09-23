// sieve.js — Eratosthenes on a grid, one prime at a time, with the count against x / ln x.
(function () {
  const cv = document.getElementById("sieve");
  if (!cv) return;
  const out = document.getElementById("sieveout");
  const ctx = cv.getContext("2d");
  const COLS = 30, ROWS = 20, N = COLS * ROWS;   // 600
  const cell = cv.width / COLS;
  const state = new Uint8Array(N + 1);   // 0 unknown, 1 prime, 2 struck
  const strikeBy = new Uint16Array(N + 1);
  const primes = [];
  let p = 2, timer = null;
  const css = getComputedStyle(document.documentElement);
  const C = { ink: css.getPropertyValue("--ink").trim(), mute: css.getPropertyValue("--mute").trim(), c0: css.getPropertyValue("--c0").trim(), c1: css.getPropertyValue("--c1").trim(), c2: css.getPropertyValue("--c2").trim(), line: css.getPropertyValue("--line").trim() };
  const palette = [C.c1, C.c2, "#b79cff", "#7fd06b", "#ff9a5c", "#5fa8ff", "#e9d66b", "#c78bff"];

  function draw(active) {
    ctx.clearRect(0, 0, cv.width, cv.height);
    for (let n = 1; n <= N; n++) {
      const i = n - 1, x = (i % COLS) * cell, y = Math.floor(i / COLS) * cell;
      let fill = "#14141f";
      if (state[n] === 1) fill = C.c0;
      else if (state[n] === 2) fill = palette[primes.indexOf(strikeBy[n]) % palette.length] + "55";
      if (active && n % active === 0 && n !== active) fill = palette[primes.indexOf(active) % palette.length];
      ctx.fillStyle = fill; ctx.fillRect(x + 1, y + 1, cell - 2, cell - 2);
      ctx.fillStyle = state[n] === 1 ? "#0a0a10" : C.ink;
      ctx.font = `${Math.floor(cell * 0.42)}px ui-monospace, Menlo, monospace`;
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText(n, x + cell / 2, y + cell / 2);
    }
  }
  function step() {
    while (p <= N && state[p] === 2) p++;
    if (p > N) { finish(); return; }
    state[p] = 1; primes.push(p);
    for (let m = p * p; m <= N; m += p) if (state[m] === 0) { state[m] = 2; strikeBy[m] = p; }
    draw(p);
    const count = primes.length;
    out.innerHTML = `<div><span class="k">striking multiples of</span> <span class="good">${p}</span> · <span class="k">primes so far</span> <span class="v">${count}</span></div>`;
    if (p * p > N) {
      // everything left unstruck is prime
      for (let n = 2; n <= N; n++) if (state[n] === 0) { state[n] = 1; primes.push(n); }
      finish(); return;
    }
    p++;
  }
  function finish() {
    if (timer) { clearInterval(timer); timer = null; }
    draw(0);
    const c = primes.length, guess = N / Math.log(N);
    out.innerHTML = `<div><span class="k">primes up to ${N}</span> <span class="good">${c}</span> · <span class="k">${N} / ln ${N}</span> <span class="v">${guess.toFixed(1)}</span> · <span class="k">the gap between them is what the Riemann Hypothesis is about</span></div>` +
      `<div class="k">Once the striking prime passes √${N} ≈ ${Math.sqrt(N).toFixed(1)} there is nothing left to strike. Every number still standing is prime.</div>`;
  }
  function reset() { state.fill(0); strikeBy.fill(0); primes.length = 0; p = 2; draw(0); out.innerHTML = `<span class="k">press play</span>`; }
  document.getElementById("sieveplay").addEventListener("click", () => {
    if (timer) return;
    if (p > N || (p * p > N && primes.length)) reset();
    timer = setInterval(step, 650);
  });
  document.getElementById("sievestep").addEventListener("click", () => { if (timer) { clearInterval(timer); timer = null; } step(); });
  document.getElementById("sievereset").addEventListener("click", () => { if (timer) { clearInterval(timer); timer = null; } reset(); });
  reset();
})();

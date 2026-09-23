// curve.js — the wallet's lock, small enough to see: y² = x³ + 7 over the integers mod 97.
// Hop from G. Then hide the count and try to get it back. Then the same thing at 256 bits.
(function () {
  const cv = document.getElementById("curve");
  if (!cv) return;
  const out = document.getElementById("curveout");
  const base = document.body.dataset.base || "/";
  const css = getComputedStyle(document.documentElement);
  const C = { ink: css.getPropertyValue("--ink").trim(), mute: css.getPropertyValue("--mute").trim(), c0: css.getPropertyValue("--c0").trim(), c1: css.getPropertyValue("--c1").trim(), c2: css.getPropertyValue("--c2").trim(), line: css.getPropertyValue("--line").trim() };
  let D = null, k = 0, timer = null, secret = 0;

  function draw(upto, hideTrail) {
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height, p = D.p;
    const s = (v) => 8 + v / (p - 1) * (W - 16);
    const sy = (v) => H - 8 - v / (p - 1) * (H - 16);
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = C.mute + "55";
    for (const [x, y] of D.allpoints) { ctx.beginPath(); ctx.arc(s(x), sy(y), 2.2, 0, 7); ctx.fill(); }
    if (!hideTrail) {
      ctx.strokeStyle = C.c1 + "88"; ctx.lineWidth = 1;
      for (let i = 1; i < upto && i < D.walk.length; i++) { const a = D.walk[i - 1], b = D.walk[i]; if (!a || !b) continue; ctx.beginPath(); ctx.moveTo(s(a[0]), sy(a[1])); ctx.lineTo(s(b[0]), sy(b[1])); ctx.stroke(); }
    }
    for (let i = 0; i < upto && i < D.walk.length; i++) { const q = D.walk[i]; if (!q) continue; ctx.fillStyle = i === 0 ? C.c0 : i === upto - 1 ? C.c2 : C.c1; ctx.beginPath(); ctx.arc(s(q[0]), sy(q[1]), i === 0 || i === upto - 1 ? 6 : 3.5, 0, 7); ctx.fill(); }
    ctx.fillStyle = C.mute; ctx.font = "12px ui-monospace, Menlo"; ctx.textAlign = "left";
    ctx.fillText(`y² = x³ + 7 (mod ${D.p}): ${D.points} points, plus one at infinity`, 8, 14);
  }
  function hop() {
    if (k >= D.G_order) { k = 0; }
    k++;
    draw(k, false);
    const q = D.walk[k - 1];
    out.innerHTML = `<div><span class="k">k =</span> <span class="good">${k}</span> · <span class="k">k·G =</span> ${q ? `(${q[0]}, ${q[1]})` : "the point at infinity — the cycle closed"} · <span class="k">G has order ${D.G_order}, so k·G runs through ${D.G_order} points before it repeats</span></div>` +
      `<div class="k">Each hop is one 'addition': draw the line through the last point and G, take the third crossing, flip it. Cheap. The landing spot looks random.</div>`;
  }
  function challenge() {
    stop();
    secret = 2 + Math.floor(Math.random() * (D.G_order - 3));
    const q = D.walk[secret - 1];
    k = 0;
    draw(0, true);
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height, p = D.p;
    const s = (v) => 8 + v / (p - 1) * (W - 16), sy = (v) => H - 8 - v / (p - 1) * (H - 16);
    ctx.fillStyle = C.c0; ctx.beginPath(); ctx.arc(s(D.G[0]), sy(D.G[1]), 6, 0, 7); ctx.fill();
    ctx.fillStyle = C.c2; ctx.beginPath(); ctx.arc(s(q[0]), sy(q[1]), 6, 0, 7); ctx.fill();
    out.innerHTML = `<div><span class="k">the public key is</span> <span class="v">(${q[0]}, ${q[1]})</span> · <span class="k">the private key is the k that lands there from G. Find it.</span></div>` +
      `<div class="k">On this curve, counting hops from G works: at most ${D.G_order} of them. Press brute force.</div>`;
  }
  function brute() {
    stop();
    if (!secret) { challenge(); }
    let i = 0;
    timer = setInterval(() => {
      i++;
      draw(i, false);
      const q = D.walk[i - 1];
      if (i === secret) {
        stop();
        out.innerHTML = `<div><span class="k">found it:</span> k = <span class="good">${secret}</span> <span class="k">after ${secret} hops.</span></div>` +
          `<div class="k">Bitcoin's curve has about 2<sup>256</sup> points — 1.16 × 10<sup>77</sup>. The best classical method needs about 2<sup>128</sup> hops. At a trillion hops a second that is 10<sup>19</sup> years. Shor's method on a quantum machine reads k another way: it does not hop at all.</div>`;
      } else out.innerHTML = `<div><span class="k">hop</span> <span class="v">${i}</span> <span class="k">→</span> (${q[0]}, ${q[1]}) <span class="k">not it yet…</span></div>`;
    }, 90);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }

  // ---- a real key, made here (BigInt secp256k1)
  const P = 2n ** 256n - 2n ** 32n - 977n;
  const Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798n;
  const Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8n;
  function inv(a, m) { let [g, x, y] = [m, 0n, 1n], b = ((a % m) + m) % m; let [r0, r1, s0, s1] = [m, b, 0n, 1n]; while (r1) { const q = r0 / r1; [r0, r1] = [r1, r0 - q * r1]; [s0, s1] = [s1, s0 - q * s1]; } return ((s0 % m) + m) % m; }
  function add(A, B) {
    if (!A) return B; if (!B) return A;
    const [x1, y1] = A, [x2, y2] = B;
    if (x1 === x2 && (y1 + y2) % P === 0n) return null;
    const l = x1 === x2 ? (3n * x1 * x1) * inv(2n * y1, P) % P : (y2 - y1) * inv(x2 - x1, P) % P;
    const x3 = ((l * l - x1 - x2) % P + P) % P;
    return [x3, ((l * (x1 - x3) - y1) % P + P) % P];
  }
  function mul(k, G) { let R = null, Q = G; while (k > 0n) { if (k & 1n) R = add(R, Q); Q = add(Q, Q); k >>= 1n; } return R; }
  function realKey() {
    const bytes = new Uint8Array(32); crypto.getRandomValues(bytes);
    let d = 0n; for (const b of bytes) d = (d << 8n) | BigInt(b);
    const t0 = performance.now();
    const Q = mul(d, [Gx, Gy]);
    const ms = performance.now() - t0;
    const hex = (n) => n.toString(16).padStart(64, "0");
    document.getElementById("keyout").innerHTML =
      `<div><span class="k">private key (a random 256-bit number)</span></div><div class="v" style="word-break:break-all;font-size:.8em">${hex(d)}</div>` +
      `<div><span class="k">public key = private × G on secp256k1, computed in ${ms.toFixed(1)} ms</span></div><div style="word-break:break-all;font-size:.8em">02/03 ${hex(Q[0])}</div>` +
      `<div class="k">Your address is a hash of that public key. Going down the page took a millisecond. Going back up is the discrete logarithm. This key was made for the demonstration and thrown away; do not send anything to it.</div>`;
  }

  fetch(base + "data/curve.json").then((r) => r.json()).then((d) => {
    D = d;
    D.allpoints = [];
    for (let x = 0; x < d.p; x++) for (let y = 0; y < d.p; y++) if ((y * y - (x * x * x + d.b)) % d.p === 0) D.allpoints.push([x, y]);
    draw(0, false);
    out.innerHTML = `<span class="k">press hop</span>`;
  });
  document.getElementById("hop").addEventListener("click", () => { stop(); secret = 0; hop(); });
  document.getElementById("hopplay").addEventListener("click", () => { stop(); secret = 0; timer = setInterval(hop, 160); });
  document.getElementById("challenge").addEventListener("click", challenge);
  document.getElementById("brute").addEventListener("click", brute);
  if (document.getElementById("realkey")) document.getElementById("realkey").addEventListener("click", realKey);
})();

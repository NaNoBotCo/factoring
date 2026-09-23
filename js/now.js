// now.js — filter the ledger by lane.
(function () {
  const bar = document.getElementById("lanes");
  if (!bar) return;
  const rows = document.querySelectorAll("tr[data-lane]");
  bar.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
    bar.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
    const lane = b.dataset.lane;
    let n = 0;
    rows.forEach((r) => { const show = lane === "all" || r.dataset.lane === lane; r.hidden = !show; if (show) n++; });
    document.getElementById("lanecount").textContent = `${n} row${n === 1 ? "" : "s"}`;
  }));
})();

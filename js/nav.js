// nav.js — hide the sticky header on the way down a small screen, bring it back on the way up.
(function () {
  let last = 0;
  addEventListener("scroll", () => {
    const y = scrollY;
    document.body.classList.toggle("nav-away", y > 220 && y > last);
    last = y;
  }, { passive: true });
})();

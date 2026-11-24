// THE ALLFORM site-v2 — 섹션 등장, 상단 메뉴 색 전환, 모바일 메뉴, 사례 넘기기, 필터, 사진 크게 보기
(function () {
  const gnb = document.querySelector(".gnb");

  // 1) 화면에 들어온 섹션은 글자 등장
  const reveal = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) e.target.classList.add("is-in"); });
  }, { threshold: 0.2 });
  document.querySelectorAll(".panel").forEach((p) => reveal.observe(p));

  // 2) 상단 메뉴 바로 아래에 있는 섹션의 테마(data-theme)로 메뉴 글자색을 맞춤.
  //    data-gnb="solid"인 섹션(흰 바탕) 위에서는 메뉴에 흰 배경을 깐다.
  const sections = document.querySelectorAll("main [data-theme], body > [data-theme]:not(.gnb)");
  const underGnb = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      gnb.dataset.theme = e.target.dataset.theme || "light";
      gnb.classList.toggle("is-solid", e.target.dataset.gnb === "solid");
    });
  }, { rootMargin: "0px 0px -92% 0px" });
  sections.forEach((s) => underGnb.observe(s));

  // 3) 모바일 메뉴
  const drawer = document.getElementById("drawer");
  const dim = document.querySelector(".drawer-dim");
  const openBtn = document.querySelector(".gnb-menu");
  const closeBtn = document.querySelector(".drawer-close");
  function setDrawer(open) {
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    openBtn.setAttribute("aria-expanded", String(open));
    dim.hidden = !open;
    document.body.style.overflow = open ? "hidden" : "";
    if (open) closeBtn.focus();
  }
  openBtn.addEventListener("click", () => setDrawer(true));
  closeBtn.addEventListener("click", () => setDrawer(false));
  dim.addEventListener("click", () => setDrawer(false));
  drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setDrawer(false)));

  // 4) 시공사례 좌우 넘기기 (한 페이지에 여러 개 가능)
  document.querySelectorAll(".cases").forEach((track) => {
    const nav = track.nextElementSibling;
    if (!nav || !nav.classList.contains("cases-nav")) return;
    const step = () => (track.querySelector(".case")?.getBoundingClientRect().width || 400) + 16;
    nav.querySelector(".cases-prev").addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    nav.querySelector(".cases-next").addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
  });

  // 5) 시공사례 필터 (data-filter ↔ 카드의 data-tags)
  const filters = document.querySelector(".filters");
  if (filters) {
    const cards = document.querySelectorAll(".cards [data-tags]");
    filters.addEventListener("click", (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;
      filters.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      const f = btn.dataset.filter;
      cards.forEach((c) => { c.hidden = f !== "all" && !c.dataset.tags.split(" ").includes(f); });
    });
  }

  // 6) 사진 크게 보기 (button.card[data-full])
  const box = document.querySelector(".lightbox");
  let lastFocus = null;
  function closeBox() {
    if (!box || box.hidden) return;
    box.hidden = true;
    document.body.style.overflow = "";
    lastFocus?.focus();
  }
  if (box) {
    const img = box.querySelector("img");
    const cap = box.querySelector("figcaption");
    document.querySelectorAll("button.card[data-full]").forEach((card) => {
      card.addEventListener("click", () => {
        lastFocus = card;
        img.src = card.dataset.full;
        img.alt = card.querySelector("img").alt;
        cap.innerHTML = card.querySelector("figcaption").innerHTML;
        box.hidden = false;
        document.body.style.overflow = "hidden";
        box.querySelector(".lightbox-close").focus();
      });
    });
    box.addEventListener("click", (e) => { if (e.target === box || e.target.closest(".lightbox-close")) closeBox(); });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    setDrawer(false);
    closeBox();
  });
  // 6) 첫 화면 사진 자동 전환 (6초마다, 점을 누르면 그 사진으로). 움직임 줄이기 설정이면 자동 전환 안 함
  const hero = document.querySelector(".panel-hero");
  if (hero) {
    const slides = hero.querySelectorAll(".hero-slide");
    const dots = hero.querySelectorAll(".hero-dots button");
    const cap = hero.querySelector(".hero-caption");
    const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let cur = 0, timer = null;
    function go(n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach((s, i) => s.classList.toggle("is-on", i === cur));
      dots.forEach((d, i) => d.classList.toggle("is-on", i === cur));
      cap.textContent = slides[cur].dataset.caption;
    }
    function play() { if (!still) { clearInterval(timer); timer = setInterval(() => go(cur + 1), 6000); } }
    dots.forEach((d, i) => d.addEventListener("click", () => { go(i); play(); }));
    document.addEventListener("visibilitychange", () => { if (document.hidden) clearInterval(timer); else play(); });
    play();
  }
})();

// THE ALLFORM site prototype — shared behaviors (no build step, no dependencies)

document.addEventListener("DOMContentLoaded", () => {
  // mobile nav toggle
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      nav.classList.toggle("open");
    });
  }

  // Q&A accordion
  document.querySelectorAll(".qna-item").forEach((item) => {
    const q = item.querySelector(".qna-q");
    if (!q) return;
    q.addEventListener("click", () => {
      const isOpen = item.classList.contains("open");
      document.querySelectorAll(".qna-item.open").forEach((el) => el.classList.remove("open"));
      if (!isOpen) item.classList.add("open");
    });
  });

  // project gallery filter
  const filterBar = document.querySelector(".filter-bar");
  if (filterBar) {
    const items = document.querySelectorAll(".gallery-item");
    filterBar.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        filterBar.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const key = btn.dataset.filter;
        items.forEach((it) => {
          const match = key === "all" || it.dataset.tags.includes(key);
          it.style.display = match ? "" : "none";
        });
      });
    });
  }

  // simple lightbox for gallery images
  const lightbox = document.createElement("div");
  lightbox.className = "lightbox";
  lightbox.style.cssText = "display:none;position:fixed;inset:0;background:rgba(10,10,10,0.92);z-index:1000;align-items:center;justify-content:center;padding:40px;cursor:zoom-out;";
  const lbImg = document.createElement("img");
  lbImg.style.cssText = "max-width:100%;max-height:100%;box-shadow:0 20px 60px rgba(0,0,0,0.5);";
  lightbox.appendChild(lbImg);
  document.body.appendChild(lightbox);
  lightbox.addEventListener("click", () => (lightbox.style.display = "none"));

  document.querySelectorAll(".gallery-item img").forEach((img) => {
    img.addEventListener("click", () => {
      lbImg.src = img.src;
      lbImg.alt = img.alt;
      lightbox.style.display = "flex";
    });
  });

  // count-up for stat numbers (hero float card, intro stat row)
  const statEls = document.querySelectorAll("[data-count]");
  if (statEls.length && "IntersectionObserver" in window) {
    const animate = (el) => {
      const target = parseInt(el.dataset.count, 10);
      const suffix = el.dataset.suffix || "";
      const duration = 900;
      const start = performance.now();
      const step = (now) => {
        const p = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    statEls.forEach((el) => io.observe(el));
  }
});

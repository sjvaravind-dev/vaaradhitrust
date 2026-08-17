(() => {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  // Sticky header shadow
  const header = $("#siteHeader");
  const onScrollHeader = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };
  window.addEventListener("scroll", onScrollHeader, { passive: true });
  onScrollHeader();

  // Mobile nav
  const toggle = $("#navToggle");
  const nav = $("#primaryNav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      toggle.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    $$("a", nav).forEach((link) => {
      link.addEventListener("click", () => {
        document.body.classList.remove("nav-open");
        toggle.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
    $$(".has-mega > .nav-link-btn", nav).forEach((btn) => {
      btn.addEventListener("click", () => {
        const li = btn.parentElement;
        const open = !li.classList.contains("is-open");
        $$(".has-mega", nav).forEach((el) => el.classList.remove("is-open"));
        li.classList.toggle("is-open", open);
        btn.setAttribute("aria-expanded", String(open));
      });
    });
  }

  // Hero slider
  const slider = $("#heroSlider");
  if (slider) {
    const slides = $$(".hero-slide", slider);
    const dotsWrap = $("#heroDots");
    const progressBar = $("#heroProgress");
    const SLIDE_MS = 6500;
    let index = 0;
    let timer;
    let progressRAF;

    const resetProgress = () => {
      if (!progressBar) return;
      const start = performance.now();
      cancelAnimationFrame(progressRAF);
      progressBar.style.width = "0%";
      const tick = (now) => {
        const p = Math.min(1, (now - start) / SLIDE_MS);
        progressBar.style.width = `${p * 100}%`;
        if (p < 1) progressRAF = requestAnimationFrame(tick);
      };
      progressRAF = requestAnimationFrame(tick);
    };

    const go = (i) => {
      index = (i + slides.length) % slides.length;
      slides.forEach((s, n) => s.classList.toggle("is-active", n === index));
      if (dotsWrap) {
        $$("button", dotsWrap).forEach((d, n) => d.classList.toggle("is-active", n === index));
      }
      $$(".hero-slide__index-current", slider).forEach((el) => {
        el.textContent = String(index + 1).padStart(2, "0");
      });
      resetProgress();
    };

    if (slides.length > 1 && dotsWrap) {
      slides.forEach((_, n) => {
        const b = document.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", `Go to slide ${n + 1}`);
        b.addEventListener("click", () => {
          go(n);
          restart();
        });
        dotsWrap.appendChild(b);
      });
      const prev = $(".hero-prev", slider);
      const next = $(".hero-next", slider);
      prev && prev.addEventListener("click", () => { go(index - 1); restart(); });
      next && next.addEventListener("click", () => { go(index + 1); restart(); });
      const restart = () => {
        clearInterval(timer);
        timer = setInterval(() => go(index + 1), SLIDE_MS);
      };
      go(0);
      restart();
    } else if (slides.length === 1 && progressBar) {
      progressBar.style.width = "100%";
    }
  }

  // Impact number count-up (0 → target)
  const parseCountValue = (raw) => {
    const str = String(raw).trim();
    const numMatch = str.match(/[\d,]+(?:\.\d+)?/);
    if (!numMatch) return null;
    const num = parseFloat(numMatch[0].replace(/,/g, ""));
    if (Number.isNaN(num)) return null;
    return {
      num,
      prefix: str.slice(0, numMatch.index),
      suffix: str.slice(numMatch.index + numMatch[0].length),
    };
  };

  const formatCount = (value, parsed) =>
    parsed.prefix + Math.round(value).toLocaleString("en-IN") + parsed.suffix;

  const animateCount = (el) => {
    if (el.dataset.animated === "1") return;
    const parsed = parseCountValue(el.dataset.count);
    if (!parsed) {
      el.textContent = el.dataset.count || el.textContent;
      return;
    }
    el.dataset.animated = "1";
    const { num, prefix, suffix } = parsed;
    const parsedFull = { prefix, suffix };
    const duration = Math.min(2400, 900 + num * 0.06);
    const start = performance.now();
    const ease = (t) => 1 - Math.pow(1 - t, 4);

    el.textContent = formatCount(0, parsedFull);
    const step = (now) => {
      const p = Math.min(1, (now - start) / duration);
      el.textContent = formatCount(num * ease(p), parsedFull);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = formatCount(num, parsedFull);
    };
    requestAnimationFrame(step);
  };

  const impactValues = $$(".impact-value[data-count]");
  if (impactValues.length) {
    const runVisibleCounts = () => {
      impactValues.forEach((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.92 && rect.bottom > 0) {
          animateCount(el);
        }
      });
    };

    if ("IntersectionObserver" in window) {
      const countIO = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              animateCount(entry.target);
              countIO.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.35 }
      );
      impactValues.forEach((el) => countIO.observe(el));
    }
    setTimeout(runVisibleCounts, 350);
  }

  // Scroll reveal — impact stats above the fold start visible sooner
  const revealEls = $$("[data-animate]");
  if (revealEls.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-inview");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -20px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
    // Kick in above-the-fold impact items immediately
    $$(".impact-band [data-animate], .impact-stat[data-animate]").forEach((el, i) => {
      setTimeout(() => el.classList.add("is-inview"), 120 + i * 80);
    });
  } else {
    revealEls.forEach((el) => el.classList.add("is-inview"));
  }

  // Back to top
  const backTop = $("#backToTop");
  if (backTop) {
    window.addEventListener(
      "scroll",
      () => backTop.classList.toggle("is-visible", window.scrollY > 480),
      { passive: true }
    );
    backTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  // Popup (once per session per banner id)
  const popup = $("#sitePopup");
  if (popup) {
    const id = popup.dataset.popupId || "default";
    const key = `vaaradhi_popup_closed_${id}`;
    const closeBtn = $("#popupClose");

    const openPopup = () => {
      popup.hidden = false;
      popup.classList.add("is-open");
      document.body.style.overflow = "hidden";
    };

    const closePopup = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      popup.classList.remove("is-open");
      popup.hidden = true;
      document.body.style.overflow = "";
      try {
        sessionStorage.setItem(key, "1");
      } catch (_) {}
    };

    if (!sessionStorage.getItem(key)) {
      openPopup();
    } else {
      closePopup();
    }

    if (closeBtn) {
      closeBtn.addEventListener("click", closePopup);
    }
    popup.addEventListener("click", (e) => {
      if (e.target === popup) closePopup(e);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && popup.classList.contains("is-open")) closePopup(e);
    });
  }
})();

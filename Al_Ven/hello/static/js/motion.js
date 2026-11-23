// Маленькие движения, которым нужен JS: прогресс прокрутки, компактный docbar,
// счётчик остатков, «тик» цены после фильтрации и индикатор сложности пароля.
// Всё остальное анимируется чистым CSS из style.css.
(() => {
    "use strict";

    const reduceMotion = Boolean(
        window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches
    );

    // 1. Полоса прогресса прокрутки.
    const progressBar = document.querySelector(".scroll-progress span");
    if (progressBar) {
        let ticking = false;
        const updateProgress = () => {
            const max = document.documentElement.scrollHeight - window.innerHeight;
            const ratio = max > 0 ? Math.min(window.scrollY / max, 1) : 0;
            document.documentElement.style.setProperty("--scroll-progress", ratio.toFixed(4));
            ticking = false;
        };
        window.addEventListener("scroll", () => {
            if (!ticking) {
                ticking = true;
                window.requestAnimationFrame(updateProgress);
            }
        }, { passive: true });
        updateProgress();
    }

    // 2. Строка документа слегка сжимается и прилипает при прокрутке.
    const updateDocbar = () => {
        document.body.classList.toggle("docbar--compact", window.scrollY > 80);
    };
    window.addEventListener("scroll", updateDocbar, { passive: true });
    updateDocbar();

    // 3. Счётчик остатков на главной: число начинается с 0, когда блок виден.
    const counters = document.querySelectorAll("[data-count]");
    if (counters.length) {
        counters.forEach((element) => {
            const target = Number(element.dataset.count) || 0;
            if (reduceMotion || !("IntersectionObserver" in window)) {
                element.textContent = String(target);
                return;
            }

            element.textContent = "0";
            const observer = new IntersectionObserver((entries, currentObserver) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    currentObserver.unobserve(entry.target);
                    const started = performance.now();
                    const duration = 700;
                    const step = (now) => {
                        const elapsed = Math.min((now - started) / duration, 1);
                        const eased = 1 - Math.pow(1 - elapsed, 3);
                        element.textContent = String(Math.round(target * eased));
                        if (elapsed < 1) window.requestAnimationFrame(step);
                    };
                    window.requestAnimationFrame(step);
                });
            }, { threshold: 0.4 });
            observer.observe(element);
        });
    }

    // 4. Короткий «тик» цены после применения фильтров каталога.
    const filterKeys = ["q", "material", "sort", "stock", "category_id"];
    const params = new URLSearchParams(window.location.search);
    const hasFilter = filterKeys.some((key) => params.has(key));
    if (hasFilter && !reduceMotion) {
        document.querySelectorAll(".doc-table tbody .price").forEach((element, index) => {
            window.setTimeout(() => element.classList.add("price--tick"), index * 30);
        });
    }

    // 5. Индикатор сложности пароля в reg/vhod и форме смены пароля.
    const scorePassword = (value) => {
        if (!value) return 0;
        let score = 0;
        if (value.length >= 8) score += 1;
        if (value.length >= 12) score += 1;
        if (/[A-ZА-ЯЁ]/u.test(value)) score += 1;
        if (/\d/.test(value)) score += 1;
        if (/[^A-Za-zА-Яа-яЁё0-9]/u.test(value)) score += 1;
        return Math.min(score, 4);
    };

    document.querySelectorAll('input[name="password"], input[name="new_password1"]').forEach((input) => {
        const meter = document.createElement("div");
        meter.className = "password-strength";
        meter.dataset.score = "0";
        meter.setAttribute("aria-hidden", "true");
        meter.appendChild(document.createElement("span"));
        input.insertAdjacentElement("afterend", meter);

        const update = () => {
            meter.dataset.score = String(scorePassword(input.value));
        };
        input.addEventListener("input", update);
        update();
    });

    // 6. Кнопка «Наверх» — появляется при скролле на 300 пикселей и возвращает
    //    в начало плавно. Уважает prefers-reduced-motion и состояние «hidden».
    const backToTop = document.getElementById("back-to-top");
    if (backToTop) {
        let ticking = false;
        const toggle = () => {
            const shouldShow = window.scrollY > 300 && !reduceMotion;
            if (shouldShow && backToTop.hidden) {
                backToTop.hidden = false;
            } else if (!shouldShow && !backToTop.hidden) {
                backToTop.hidden = true;
            }
            ticking = false;
        };
        window.addEventListener("scroll", () => {
            if (!ticking) {
                ticking = true;
                window.requestAnimationFrame(toggle);
            }
        }, { passive: true });
        toggle();
        backToTop.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
        });
    }

    // 7. Мобильная навигация: синхронизация aria-expanded и закрытие по ссылке/Escape.
    const menuToggle = document.querySelector(".menu-toggle");
    const menu = document.getElementById("main-menu");
    if (menuToggle && menu) {
        const setMenuOpen = (open) => {
            menuToggle.setAttribute("aria-expanded", String(open));
            menuToggle.querySelector(".visually-hidden").textContent =
                open ? "Закрыть меню" : "Открыть меню";
            document.body.classList.toggle("menu-open", open);
        };
        menuToggle.addEventListener("click", () => {
            setMenuOpen(menuToggle.getAttribute("aria-expanded") !== "true");
        });
        menu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => setMenuOpen(false));
        });
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") setMenuOpen(false);
        });
    }
})();

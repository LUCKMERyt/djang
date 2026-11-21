// Общее модальное окно для каталога и команды (нативный <dialog>).
// Кнопка с aria-controls="<id окна>" передаёт данные через data-<prefix>-* атрибуты,
// а окно с data-prefix="<prefix>" подставляет их в элементы [data-field="..."].
// Данные вставляются через textContent, поэтому HTML из базы не выполняется.
(() => {
    const read = (button, prefix, key) =>
        button.dataset[prefix + key.charAt(0).toUpperCase() + key.slice(1)] || "";

    document.querySelectorAll("dialog[data-prefix]").forEach((modal) => {
        const prefix = modal.dataset.prefix;
        const imageWrap = modal.querySelector(".product-modal__image-wrap");
        const image = modal.querySelector(".product-modal__image");
        let opener = null;

        document.querySelectorAll(`[aria-controls="${modal.id}"]`).forEach((button) => {
            button.addEventListener("click", () => {
                opener = button;

                modal.querySelectorAll("[data-field]").forEach((element) => {
                    const value = read(button, prefix, element.dataset.field);
                    // data-suffix добавляет единицу измерения, data-empty задаёт текст для пустого значения.
                    element.textContent = value
                        ? value + (element.dataset.suffix || "")
                        : (element.dataset.empty ?? "—");
                });

                const src = read(button, prefix, "image");
                if (src) {
                    image.src = src;
                    image.alt = read(button, prefix, "name");
                } else {
                    image.removeAttribute("src");
                    image.alt = "";
                }
                imageWrap.hidden = !src;

                const monogram = modal.querySelector(".person-monogram");
                if (monogram && prefix === "person") {
                    const fullName = read(button, prefix, "name");
                    monogram.textContent = fullName ? fullName.charAt(0).toUpperCase() : "С";
                    monogram.classList.remove("is-popping");
                    // Перезапуск анимации при каждом открытии карточки сотрудника.
                    void monogram.offsetWidth;
                    monogram.classList.add("is-popping");
                }

                // ! showModal() сохраняет фокус и делает окно доступным для клавиатуры.
                modal.showModal();
            });
        });

        modal.querySelectorAll(".product-modal__close, .product-modal__done").forEach((button) => {
            button.addEventListener("click", () => modal.close());
        });
        modal.addEventListener("click", (event) => {
            if (event.target === modal) modal.close();
        });
        modal.addEventListener("close", () => opener && opener.focus());
    });
})();

// Если файл картинки в таблице не загрузился, показываем ту же заглушку, что и для товаров без фото.
document.querySelectorAll("img.thumb").forEach((img) => {
    const showPlaceholder = () => {
        const stub = document.createElement("div");
        stub.className = "thumb thumb--empty";
        stub.textContent = "Не загрузилось";
        img.replaceWith(stub);
    };
    if (img.complete && img.naturalWidth === 0) {
        showPlaceholder();
    } else {
        img.addEventListener("error", showPlaceholder);
    }
});

// В окне товара при ошибке загрузки просто скрываем блок картинки.
document.querySelectorAll(".product-modal__image").forEach((img) => {
    img.addEventListener("error", () => {
        img.closest(".product-modal__image-wrap").hidden = true;
    });
});

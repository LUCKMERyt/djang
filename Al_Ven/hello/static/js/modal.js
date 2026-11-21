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

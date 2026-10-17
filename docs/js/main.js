// Простой JavaScript: проверка совпадения паролей при регистрации
var pass = document.getElementById("pass");
var confirm = document.getElementById("pass_confirm");
var hint = document.getElementById("pass_hint");

if (pass && confirm && hint) {
    function check() {
        if (confirm.value === "") {
            hint.textContent = "";
        } else if (pass.value === confirm.value) {
            hint.textContent = "Пароли совпадают";
            hint.className = "ok";
        } else {
            hint.textContent = "Пароли не совпадают";
            hint.className = "bad";
        }
    }
    pass.addEventListener("input", check);
    confirm.addEventListener("input", check);
}

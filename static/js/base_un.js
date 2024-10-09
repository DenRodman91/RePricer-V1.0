document.addEventListener("DOMContentLoaded", function() {
    // Получаем текущий путь URL.
    var path = window.location.pathname;

    // Находим все ссылки в навигационном меню.
    var links = document.querySelectorAll(".navbar-nav .nav-link");

    // Перебираем все ссылки.
    links.forEach(function(link) {
        // Если href ссылки совпадает с текущим путем, добавляем класс 'active'.
        if (link.getAttribute("href") === path) {
            link.classList.add("active");
        }
    });
});
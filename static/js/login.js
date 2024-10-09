function goBack() {
    window.history.back();
}
document.getElementById('request-password').addEventListener('click', function() {
    const email = document.getElementById('email').value;
    const button = document.getElementById('request-password');
    const countdown = document.createElement('div');
    
    // Проверка заполненности поля email
    if (!email) {
        alert('Пожалуйста, введите ваш email.');
        return;
    }
    
    // Скрываем кнопку и добавляем сообщение с таймером
    button.style.display = 'none';
    countdown.id = 'countdown';
    countdown.innerText = "Повторный запрос через 2 минуты";
    button.parentNode.insertBefore(countdown, button.nextSibling);
    
    // Отправка запроса на сервер
    fetch('/request-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Предполагается, что сервер возвращает сообщение в формате JSON
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Ошибка при отправке запроса.');
    });
    
    // Таймер обратного отсчета
    let timeLeft = 120; // 2 минуты
    const timerId = setInterval(updateCountdown, 1000);

    function updateCountdown() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        countdown.innerText = `Повторный запрос через ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        timeLeft -= 1;

        if (timeLeft < 0) {
            clearInterval(timerId);
            countdown.remove();
            button.style.display = 'block'; // Показываем кнопку снова
        }
    }
});


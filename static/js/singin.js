let userCount = 0; // Счетчик пользователей для идентификации
document.getElementById('add-user').addEventListener('click', function() {
    userCount++;
    const usersDiv = document.getElementById('users');
    const newUserDiv = document.createElement('div');
    newUserDiv.classList.add('user-group');
    newUserDiv.innerHTML = `
        <div class="form-group">
            <label>Пользователь ${userCount}</label>
            <input class="input" type="email" name="email${userCount}" placeholder="Электронная почта">
        </div>
        <div class="form-group">
            <label></label>
            <input class="input" type="text" name="telegram${userCount}" placeholder="Телеграмм ник">
        </div>
        <div class="form-group">
            <label></label>
            <select name="role${userCount}" class="input">
                <option value="owner">Владелец</option>
                <option value="manager">Менеджер</option>
                <option value="developer">Программист</option>
                <option value="director">Директор</option>
            </select>
        </div>
    `;
    usersDiv.appendChild(newUserDiv);
});
function goBack() {
    window.history.back();
}
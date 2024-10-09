function openModal(plan) {
    document.getElementById("modal").style.display = "block";
    let title = "";
    switch(plan) {
        case 'junior':
            title = "Младший брат";
            break;
        case 'classmate':
            title = "Одноклассник";
            break;
        case 'conor':
            title = "КОНОР МАКДОНАЛЬДС";
            break;
    }
    document.getElementById("modal-title").innerText = title;
    document.getElementById("tarif").innerText = plan;
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}


// Close the modal if the user clicks anywhere outside of the modal
window.onclick = function(event) {
    const modal = document.getElementById("modal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


function submitData() {
    const inputData = document.getElementById("input-field").value;
    var tarif = document.getElementById("tarif").innerText;
    console.log(`Submitted data: ${inputData}`);
    document.getElementById("input-field").value = "";
    // Создаем URL с параметром запроса sum
    const url = `/payment?sum=${encodeURIComponent(inputData)}&tarif=${encodeURIComponent(tarif)}`;
    
    // Выполняем запрос на сервер
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Обработка ответа сервера здесь
    })
    .catch(error => {
        console.error('Error:', error);
    });

    closeModal();
}
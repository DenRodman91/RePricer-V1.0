function down_sebes(ip) {


    fetch('/upload_excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: ip }) // Если необходимо отправить данные, замените {} на нужные данные
    })
    .then(response => {
        if (response.ok) {
            return response.blob(); // Получаем файл в виде Blob
        }
        throw new Error('Network response was not ok.');
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'download.xlsx'; // Имя скачиваемого файла
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}


function uploadFile() {
    const fileInput = document.getElementById('excelFile');
    const file = fileInput.files[0];
    const messageElement = document.getElementById('message');

    if (!file) {
        messageElement.textContent = 'Please select a file.';
        return;
    }

    if (!['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'].includes(file.type)) {
        messageElement.textContent = 'Please upload a valid Excel file.';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_excel2', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            messageElement.textContent = 'File uploaded and processed successfully.';
        } else {
            messageElement.textContent = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        messageElement.textContent = 'An error occurred: ' + error.message;
    });
}
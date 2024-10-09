// Получаем модальное окно
var modal = document.getElementById("myModal");

// Получаем кнопку, которая открывает модальное окно
var btn = document.getElementById("openModal");

// Получаем элемент <span>, который закрывает модальное окно
var span = document.getElementsByClassName("close")[0];

// Когда пользователь кликает на кнопку, открывается модальное окно
btn.onclick = function() {
  modal.style.display = "block";
}

// Когда пользователь кликает на <span> (x), модальное окно закрывается
span.onclick = function() {
  modal.style.display = "none";
}

// Когда пользователь кликает в любом месте за пределами модального окна, оно закрывается
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


function checkInputs() {
  const content = document.getElementById("inputContent").value;
  const price = document.getElementById("inputPrice").value;
  const stats = document.getElementById("inputStats").value;
  const anal = document.getElementById("inputAnus").value;
  const saveButton = document.getElementById("saveButton");
  if (content && price && stats && anal) {
      saveButton.disabled = false;
  } else {
      saveButton.disabled = true;
  }
}

async function submitForm() {
  const form = document.getElementById("addCabinetForm");
  const formData = new FormData(form);
  const saveButton = document.getElementById("saveButton");
  const errorMessage = document.getElementById("errorMessage");
    console.log(formData)
  saveButton.disabled = true;

  try {
      const response = await fetch('/validate', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              'p': formData.get('inputPrice'),
              'k': formData.get('inputContent'),
              's': formData.get('inputStats'),
              'q': formData.get('inputAnus'),
              'u_d': formData.get('update_raz'),
              'u_p': formData.get('update_pr'),
              'a': formData.get('artcheck')
          })
      });

      const result = await response.json();

      if (response.ok) {
          if (result.success) {
              const finalResponse = await fetch('/mydata', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                      'p': formData.get('inputPrice'),
                      'i': formData.get('companyName'),
                      'm': formData.get('marketplace'),
                      'k': formData.get('inputContent'),
                      'q': formData.get('inputAna'),
                      'u_d': formData.get('update_raz'),
                      'u_p': formData.get('update_pr'),
                      's': formData.get('inputStats')
                      
                      
                  })
              });

              const finalResult = await finalResponse.json();

              if (finalResponse.ok && finalResult.success) {
                  alert('Кабинет загуржен успешно! Данные появяться в течении 10 минут!');
                  window.location.reload();
                  form.reset();
                  errorMessage.textContent = '';
              } else {
                  errorMessage.textContent = finalResult.message || 'Error occurred while saving data';
              }
          } else {
              errorMessage.textContent = result.message || 'Validation failed';
          }
      } else {
          errorMessage.textContent = result.message || 'Validation request failed';
      }
  } catch (error) {
      errorMessage.textContent = 'Error occurred: ' + error.message;
  } finally {
      saveButton.disabled = false;
  }
}

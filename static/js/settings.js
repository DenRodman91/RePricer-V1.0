document.addEventListener("DOMContentLoaded", function() {
    var breadcrumbItems = document.querySelectorAll('.breadcrumb-item');
    var backButton = document.getElementById('back-btn');
    var nextButton = document.getElementById('next-btn');
    var readyButton = document.getElementById('ready-btn');
    var currentIndex = 0;

    // Изначально скрываем кнопки "Назад" и "Готово"
    backButton.style.display = 'none';
    readyButton.style.display = 'none';

    // Обработчик событий для кнопки "Назад"
    backButton.addEventListener('click', function() {
        // Возвращаемся к первой странице и обновляем хлебные крошки
        changeActiveBreadcrumb(-1);
        document.getElementById('first-page').style.display = 'block';
        document.getElementById('second-page').style.display = 'none';
        backButton.style.display = 'none'; // Скрываем кнопку "Назад"
        nextButton.style.display = 'inline-block'; // Показываем кнопку "Далее"
        readyButton.style.display = 'none'; // Скрываем кнопку "Готово"
    });

    // Обработчик событий для кнопки "Далее"
    nextButton.addEventListener('click', function() {
        // if (currentIndex === 0) { // Предполагается, что проверка чекбоксов нужна на первом шаге
        //     if (!anyCheckboxChecked()) {
        //         alert("Вы не выбрали ни один артикул");
        //         return; // Прекращаем выполнение функции, не переходим к следующему шагу
        //     }
        // }
        changeActiveBreadcrumb(1);
        document.getElementById('first-page').style.display = 'none';
        document.getElementById('second-page').style.display = 'block';
        backButton.style.display = 'inline-block'; // Показываем кнопку "Назад"
        nextButton.style.display = 'none'; // Скрываем кнопку "Далее"
        readyButton.style.display = 'inline-block'; // Показываем кнопку "Готово"
    });

    function changeActiveBreadcrumb(direction) {
        var nextIndex = currentIndex + direction;

        if (nextIndex >= 0 && nextIndex < breadcrumbItems.length) {
            breadcrumbItems[currentIndex].classList.remove('active');
            breadcrumbItems[nextIndex].classList.add('active');
            currentIndex = nextIndex;
        }
    }

    function anyCheckboxChecked() {
        // Возвращает true, если хотя бы один чекбокс выбран
        return document.querySelectorAll('.rowlist input[type="checkbox"]:checked').length > 0;
    }
});




// Настройка для фильтрации артикула ВБ
$(document).ready(function(){
    $("#searchInputArt").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#listArt li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

// Настройка для фильтрации Кабинет
$(document).ready(function(){
    $("#searchInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#list li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});


// Настройка для фильтрации Артикул Продавца
$(document).ready(function(){
    $("#searchInputSeller").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#listSeller li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

// Настройка для фильтрации Бренд

$(document).ready(function(){
    $("#searchInputBrand").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#listBrand li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});



function getSelectedValues(id) {
    var values = [];
    $(id + ' input[type="checkbox"]:checked').each(function() {
        values.push($(this).siblings("p").text().toLowerCase().trim());
    });
    return values;
}

function filterRows() {
    var brands = getSelectedValues("#listBrand");
    var artVBs = getSelectedValues("#listArt");
    var artSellers = getSelectedValues("#listSeller");
    var nameFilter = $("#name-filter").val().toLowerCase();

    $(".rowlist").each(function() {
        var brand = $(this).data("brand") ? $(this).data("brand").toString().toLowerCase() : "";
        var artVB = $(this).data("artvb") ? $(this).data("artvb").toString().toLowerCase() : "";
        var artSeller = $(this).data("artseller") ? $(this).data("artseller").toString().toLowerCase() : "";
        var name = $(this).find(".card-title").text().toLowerCase();
    
        var brandMatch = !brands.length || brands.includes(brand);
        var artVBMatch = !artVBs.length || artVBs.includes(artVB);
        var artSellerMatch = !artSellers.length || artSellers.includes(artSeller);
        var nameMatch = name.includes(nameFilter);
    
        $(this).toggle(brandMatch && artVBMatch && artSellerMatch && nameMatch);
    });
}    

// Обработчики событий для чекбоксов и полей ввода
$("#listBrand input, #listArt input, #listSeller input, #name-filter").on("change keyup", filterRows);


$(document).ready(function() {
    $('#select-all').click(function() {
        // Выбираем все видимые чекбоксы и устанавливаем их в состояние 'checked'
        $('.rowlist:visible input[type="checkbox"]').each(function() {
            $(this).prop('checked', true);
        });
    });

    $('#deselect-all').click(function() {
        // Снимаем выбор со всех видимых чекбоксов
        $('.rowlist:visible input[type="checkbox"]').each(function() {
            $(this).prop('checked', false);
        });
    });
});


$(document).ready(function() {
    // Функция для обновления количества выбранных артикулов
    function updateSelectedCount() {
        var count = $('.rowlist input[type="checkbox"]:checked').length;  // Подсчитываем количество отмеченных чекбоксов
        var text = "Выбрано для настройки " + count + " Артикулов";  // Формируем строку для отображения
        $('#quantityART').text(text);  // Обновляем текст в элементе
    }

    // При изменении состояния любого чекбокса обновляем количество выбранных артикулов
    $('.rowlist input[type="checkbox"]').on('change', function() {
        updateSelectedCount();
    });

    // Обновление количества при инициализации страницы
    updateSelectedCount();
});
$('#select-all').click(function() {
    $('.rowlist:visible input[type="checkbox"]').prop('checked', true).trigger('change');
});

$('#deselect-all').click(function() {
    $('.rowlist:visible input[type="checkbox"]').prop('checked', false).trigger('change');
});


$(document).ready(function() {
    // Обработчик для кнопки сброса фильтров
    $('#reset-filters').click(function() {
        // Очистка всех полей ввода
        $('#searchInput, #searchInputArt, #searchInputSeller, #searchInputBrand, #name-filter').val('');

        

        // Сброс фильтров и обновление видимости элементов
        $('.rowlist').show();

        // Сброс чекбоксов фильтрации (если есть)
        $('input[type="checkbox"][name="filter"]').prop('checked', false);

        // Обновление количества выбранных артикулов
        updateSelectedCount();

        // Вызов функции фильтрации, если она определена
        if (typeof filterRows === "function") {
            filterRows();
        }
    });
});




function openMWartCheck() {
    var selectedItems = $('.rowlist input[type="checkbox"]:checked').map(function() {
        return $(this).closest('.rowlist').data("artvb"); // Получаем значение атрибута "data-artvb"
    }).get();
    return selectedItems
};


$(document).ready(function() {
    $('.btn-open-modal').click(function() {
        var nazvanie = $(this).data('nazvanie');
        var brand = $(this).data('brand');
        var artwb = $(this).data('articul');
        var ph = $(this).data('photo');
        $('#modal-nazvanie').text('Название: ' + nazvanie);
        $('#modal-brand').text('Бренд: ' + brand);
        $('#modal-artwb').text('Артикул МП: ' + artwb);
        $('#modal-photo').attr('src', ph); 
        $('#myModal').show(); // Показать модальное окно
        document.getElementById('sticky-filters').style.zIndex = '-1'
    });

    // Закрыть модальное окно при нажатии на крестик
    $('.close').click(function() {
        $('#myModal').hide(); // Скрыть модальное окно
        document.getElementById('sticky-filters').style.zIndex = '100'
    });
});
// Закрытие модального окна при щелчке вне его области
window.onclick = function(event) {
    var modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}



$(document).ready(function() {
    $('.btn-open-modal2').click(function() {
        var selectedItems = $('.rowlist input[type="checkbox"]:checked').map(function() {
            return {
                artvb: $(this).closest('.rowlist').data("artvb") || "Нет артикула",
                nazvanie: $(this).closest('.rowlist').data("name") || "Название не указано",
                brand: $(this).closest('.rowlist').data("brand") || "Бренд не указан"
            };
        }).get();

        var itemsHtml = '';
        selectedItems.forEach(function(item) {
            itemsHtml += '<div class="col">' +
                '<input type="checkbox" checked data-artvb="' + item.artvb + '">' +
                item.nazvanie + ' - ' + item.brand + '</div>';
        });

        $('#selected-items').html(itemsHtml);
        $('#myModal2').show(); // Показать модальное окно
    });

    $('.close').click(function() {
        $('#myModal2').hide(); // Скрыть модальное окно
    });

    window.onclick = function(event) {
        var modal = document.getElementById('myModal2');
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    $('#selected-items').on('change', 'input[type="checkbox"]', function() {
        var artvb = $(this).data('artvb');
        var checked = $(this).is(':checked');
        $('.rowlist').each(function() {
            if ($(this).data('artvb') === artvb) {
                $(this).find('input[type="checkbox"]').prop('checked', checked);
            }
        });
    });
});





$(document).ready(function() {
    $('.info').click(function() {
        var infoText = $(this).attr('data-info');
        $('#info-box').text(infoText); // Отображаем информацию в информационном окошке
    });
});

$(document).ready(function() {
    $('input[type="checkbox"][name="metr"]').change(function() {
        var checkbox = $(this);
        var isChecked = checkbox.is(':checked');
        var metricId = checkbox.attr('id');

        if (isChecked) {
            var label = checkbox.next('label').text();
            var info = checkbox.siblings('.info').attr('data-info');
            var metricHtml = '<div class="metric-item" id="selected-' + metricId + '"><input type="checkbox" name="metr" checked data-metric-id="' + metricId + '"><label>' + label + '</label><span class="info" data-info="' + info + '">?</span>';

            if (['kdz_mp'].includes(metricId) && document.getElementById('olduser').checked) { 
                metricHtml += '<input type="number" value="30" placeholder="Введите значение" style="margin-left: 10px;" class="metric-input" id="metricInput-' + metricId + '">';
            } else {
                metricHtml += '<input type="number" value="30" placeholder="Введите значение" style="margin-left: 10px; display:none;" class="metric-input" id="metricInput-' + metricId + '">';
            }

            metricHtml += '</div>';
            $('#selected-metrics').append(metricHtml);
        } else {
            $('#selected-' + metricId).remove();
        }
    });
});

    // Обработка изменений в "Выбранные метрики"
    $('#selected-metrics').on('change', 'input[type="checkbox"][name="metr"]', function() {
        var selectedCheckbox = $(this);
        var metricId = selectedCheckbox.data('metric-id');
        var isChecked = selectedCheckbox.is(':checked');
        
        $('#' + metricId).prop('checked', isChecked); // Синхронизация состояния с основным списком

        if (!isChecked) {
            // Если чекбокс снят, удаляем метрику из списка
            $('#selected-' + metricId).remove();
        }
    });

    // Обработка клика по знаку вопроса для отображения информации
    $(document).on('click', '.info', function() {
        var infoText = $(this).attr('data-info');
        $('#info-box').text(infoText); // Отображаем информацию в информационном окошке
    });

    $('#strategy-select').change(function() {
        var selectedStrategy = $(this).val();
        if (selectedStrategy === 'max_profit') {
            $('#sdp, #kdz_mp, #kdn').prop('checked', true).change();
        } else {
            $('#sdp, #kdz_mp, #kdn').prop('checked', false).change();
        }
    });
// });







document.addEventListener('DOMContentLoaded', function () {
    // Элементы для управления видимостью
    const roundPriceCheckbox = document.getElementById('beautiful_price');
    const promotionCheckbox = document.getElementById('participation_in_promotions');
    const roundPriceInput = document.getElementById('roundPriceInput'); // Предполагаем, что у вас есть такой инпут
    const saleDiv = document.querySelector('[name="set_sale"]');

    // Обработчик для чекбокса "Красивая цена"
    roundPriceCheckbox.addEventListener('change', function() {
        if (this.checked) {
            roundPriceInput.style.display = 'block'; // Показать поле для ввода степени округления
        } else {
            roundPriceInput.style.display = 'none'; // Скрыть поле, если чекбокс снят
        }
    });

    // Обработчик для чекбокса "Участие в акциях"
    promotionCheckbox.addEventListener('change', function() {
        if (this.checked) {
            saleDiv.style.display = 'block'; // Показать див с артикулами
            loadSelectedArticles(); // Загрузить выбранные артикулы
        } else {
            saleDiv.style.display = 'none'; // Скрыть див
        }
    });

    // Функция для загрузки выбранных артикулов
    function loadSelectedArticles() {
        var selectedItems = $('.rowlist input[type="checkbox"]:checked').map(function() {
            return {
                artvb: $(this).closest('.rowlist').data("artvb") || "Нет артикула",
                nazvanie: $(this).closest('.rowlist').data("name") || "Название не указано",
                brand: $(this).closest('.rowlist').data("urlphoto") || "Бренд не указан"
            };
        }).get();

        var itemsHtml = '';
        selectedItems.forEach(function(item) {
            itemsHtml += '<div><div class="row"><div class="col-1" name="photo"><img src="'+ item.brand+'" class="card-img-top" alt="..." style="height: 40px; width: 40px;"></div>'+
                        '<div class="col-5" name="name"> '+ item.nazvanie+'</div>'+
                        '<div class="col-2" name="name"> '+ item.artvb+'</div>'+
                        '<div class="col-1" name="artwb"><input type="checkbox" id="add"></div>'+
                        '<div class="col-2" name="param"><input type="number" id="param_sale" placeholder="Уступить цену до..."> </div></div></div>';
        });

        $('#art_sale').html(itemsHtml);
        };
});




$(document).ready(function() {
    var currentIndex = 0; // Убедитесь, что это определено, если используется в логике

    $('.btn-open-modal3').click(function() {
        if (currentIndex === 0) {
            if (!anyCheckboxChecked2()) {
                alert("Вы не выбрали ни одну метрику");
                return; // Прекращаем выполнение функции, не переходим к следующему шагу
            }
        }
        $('#myModal3').show(); // Показать модальное окно
    });

    $('.close3').click(function() {
        $('#myModal3').hide(); // Скрыть модальное окно
    });

    $(window).click(function(event) {
        var modal = $('#myModal3');
        if (event.target === modal[0] ) {
            modal.hide();
        }
    });

    function anyCheckboxChecked2() {
        // Возвращает true, если хотя бы один чекбокс выбран
        return $('.metrics-list input[type="checkbox"]:checked').length > 0;
    }
});
document.addEventListener('DOMContentLoaded', function() {
    // Находим кнопку внутри элемента с id="cl" и добавляем обработчик клика
    document.querySelector('#cl button').addEventListener('click', function() {
        document.getElementById('myModal3').style.display = 'none'; // Скрываем модальное окно
    });
});





function collectData() {
    // Сбор выбранных артикулов
    var articuls = $('.rowlist input[type="checkbox"]:checked').map(function() {
        return $(this).closest('.rowlist').data('artvb');
    }).get();

    // Сбор выбранных метрик и их параметров
    var metrics = $('.metrics-list input[type="checkbox"]:checked').map(function() {
        var id = this.id;
        var metricInput = $('#metricInput-' + id);
        var metricInputValue = metricInput.length ? metricInput.val() : null;
        return {
            id: id,
            value: metricInputValue
        };
    }).get();

    // Сбор дополнительных параметров
    var add_params = [];
    if ($('#beautiful_price').is(':checked')) {
        add_params.push({
            id: 'beautiful_price',
            roundPrice: $('#roundPriceInput').val() || 0
        });
    }
    if ($('#participation_in_promotions').is(':checked')) {
        add_params.push('participation_in_promotions');
    }

    // Сбор доп. метрик к определенным артикулам
    var sale_akc = [];
    $('#art_sale .row').each(function() {
        var artvb = $(this).find('[name="artwb"]').data('artvb');
        var param_sale = $(this).find('#param_sale').val();
        sale_akc.push({[artvb]: param_sale});
    });

    // Получение значения выбранного элемента из select
    var strat = document.getElementById('strategy-select').value;

    return {
        articuls: articuls,
        strat: strat,
        metrics: metrics,
        add_param: add_params,
        sale_akc: sale_akc
    };
}

$('#sendButton').click(function() {
    var data = collectData();
    sendDataToServer(data);
});

function sendDataToServer(data) {
    $.ajax({
        url: '/addparam',  // Укажите правильный URL
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            console.log('Данные успешно отправлены:', response);
        },
        error: function(error) {
            console.error('Ошибка при отправке данных:', error);
        }
    });
    window.location.reload(true);
}





document.addEventListener('DOMContentLoaded', function() {
    var radios = document.querySelectorAll('input[type="radio"][name="userType"]');
    radios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            var metricsBlock = document.querySelector('.userlvl');  // Используем селектор класса
            if (document.getElementById('olduser').checked) {
                metricsBlock.style.display = 'block'; // Показать блок
            } else {
                metricsBlock.style.display = 'none'; // Скрыть блок
            }
        });
    });
});





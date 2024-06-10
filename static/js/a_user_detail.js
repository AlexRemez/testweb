// Кнопка редактирования
const editBtn = document.getElementById('edit-btn');
// Форма редактирования
const editForm = document.getElementById('edit-form');
// Кнопка сохранения изменений
const saveBtn = document.getElementById('save-btn');
// Кнопка отмены
const cancelBtn = document.getElementById('cancel-btn');


document.addEventListener('DOMContentLoaded', () => {
            function getQueryParams() {
                const params = {};
                window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, (str, key, value) => {
                    params[key] = decodeURIComponent(value);
                });
                return params;
            }

            function removeQueryParam(param) {
                const url = new URL(window.location);
                url.searchParams.delete(param);
                window.history.replaceState({}, document.title, url.pathname + url.search);
            }

            function showNotification(message) {
                const notificationContainer = document.getElementById('notificationContainer');
                const notification = document.getElementById('notification');
                notification.textContent = message;
                notificationContainer.style.display = 'block';

                setTimeout(() => {
                    notificationContainer.style.display = 'none';
                }, 5000);
            }

            const queryParams = getQueryParams();
            if (queryParams.message) {
                showNotification(queryParams.message);
                removeQueryParam('message');
            }

            const deleteBtn = document.getElementById('delete-btn');
            const confirmModal = document.getElementById('confirm-modal');
            const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
            const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

            deleteBtn.addEventListener('click', () => {
                confirmModal.style.display = 'flex';
            });

            cancelDeleteBtn.addEventListener('click', () => {
                confirmModal.style.display = 'none';
            });

            confirmDeleteBtn.addEventListener('click', async () => {
                const tgId = document.getElementById('tg_id').textContent;

                const response = await fetch('/admin/delete_user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ tg_id: tgId }),
                });

                if (response.ok) {
                    window.location.href = '/admin/users?message=Пользователь успешно удален!';
                } else {
                    alert('Ошибка при удалении пользователя');
                }
            });
        });

// При нажатии на кнопку редактирования
editBtn.addEventListener('click', () => {
    // Скрываем кнопку редактирования
    editBtn.style.display = 'none';
    // Отображаем форму редактирования
    editForm.style.display = 'block';
});

// При нажатии на кнопку отмены
cancelBtn.addEventListener('click', () => {
    // Отображаем кнопку редактирования
    editBtn.style.display = 'block';
    // Скрываем форму редактирования
    editForm.style.display = 'none';
});


// Функция для опроса сервера
function pollServerForUpdates() {
    // Отправляем GET-запрос на сервер для получения актуальных данных пользователя
    fetch('/get_user_data')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Обновляем данные на странице
        document.getElementById('tg_id').innerText = data.tg_id;
        document.getElementById('first_name').innerText = data.first_name;
        document.getElementById('username').innerText = data.username;
        document.getElementById('global_points').innerText = data.global_points;

        // Выводим сообщение об успешном обновлении
        console.log('Data was successfully updated:', data);
    })
    .catch(error => {
        console.error('There was a problem updating the data:', error);
    });
}

// При нажатии на кнопку сохранения изменений
saveBtn.addEventListener('click', () => {
    // Получаем новые значения из формы редактирования
    const tg_id = document.getElementById('edit-tg_id').value;
    const first_name = document.getElementById('edit-first_name').value;
    const username = document.getElementById('edit-username').value;
    const global_points = document.getElementById('edit-global_points').value;

    // Обновляем значения на странице
    document.getElementById('tg_id').innerText = tg_id;
    document.getElementById('first_name').innerText = first_name;
    document.getElementById('username').innerText = username;
    document.getElementById('global_points').innerText = global_points;

    // Формируем объект с данными для отправки на сервер
    const formData = {
        tg_id: tg_id,
        first_name: first_name,
        username: username,
        global_points: global_points
    };

    // Отправляем POST-запрос на сервер
    fetch('/update_user_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Data was successfully updated:', data);

        // Ждем некоторое время и затем опрашиваем сервер для получения актуальных данных
        setTimeout(pollServerForUpdates, 5000); // Опрос каждые 5 секунд (5000 миллисекунд)
    })
    .catch(error => {
        console.error('There was a problem updating the data:', error);
    });

    // Отображаем кнопку редактирования
    editBtn.style.display = 'block';
    // Скрываем форму редактирования
    editForm.style.display = 'none';
});


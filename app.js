let exercises = [];
let filteredExercises = [];
let currentPage = 1;
const itemsPerPage = 10;


const tg = window.Telegram.WebApp; //обьявление обьекта telegram.webapp для взаимодействия с ботом

tg.expand(); //открывает веб-приложение во все окно
tg.ready(); // Инициализация
console.log("Telegram WebApp initialized:", tg.initDataUnsafe); // Пример использования tg

document.addEventListener("DOMContentLoaded", () => {
    fetch('exercises_co.json')
        .then(response => response.json())
        .then(data => {
            exercises = data;
            filteredExercises = [...exercises];
            renderExercises();
            populateTags();
            prefetchAdjacentPages(); // Предзагрузка соседних страниц
        })
        .catch(error => console.error('Error loading JSON:', error));
});

function renderExercises() {
    const container = document.getElementById("exercises-container");
    container.innerHTML = "";

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const exercisesToShow = filteredExercises.slice(start, end);

    exercisesToShow.forEach(exercise => {
        const card = document.createElement("div");
        card.className = "card";

        // Проверим формат изображения и преобразуем путь
        let imgSrc = exercise.ex_img_bytes;
        if (imgSrc.startsWith('C:\\Users\\remez\\PycharmProjects\\Parsing\\poolbilliards.co\\images\\')) {
            imgSrc = imgSrc.replace('C:\\Users\\remez\\PycharmProjects\\Parsing\\poolbilliards.co\\', '');
        }
        // Заменяем подчеркивания на пробелы
        imgSrc = imgSrc.replace(/_/g, ' ');

        card.innerHTML = `
            <h3>${exercise.ex_name}</h3>
            <img src="${imgSrc}" alt="${exercise.ex_name}">
            <p>${exercise.ex_description || ''}</p>
            <p>Тэги: ${exercise.ex_tags.join(", ")}</p>
            <button class="change-color-btn">Выбрать</button> <!-- Добавляем кнопку -->
        `;
        container.appendChild(card);
    });

    // Обновляем элемент page-info
    document.getElementById("page-info").innerText = `Страница ${currentPage} из ${Math.ceil(filteredExercises.length / itemsPerPage)}`;

    attachButtonClickHandlers(); // Переподключаем обработчики кнопок после рендеринга
}

function attachButtonClickHandlers() {
    // Добавляем обработчик нажатия на кнопки для каждой карточки
    document.querySelectorAll('.change-color-btn').forEach((btn, index) => {
        btn.addEventListener('click', () => {
            const card = document.querySelectorAll('.card')[index]; // Находим соответствующую карточку
            card.style.backgroundColor = '#f0f0f0'; // Изменяем цвет карточки

            const cardTitle = card.querySelector('h3').innerText; // Получаем название карточки
            const userID = tg.initDataUnsafe.user.id

            // Формируем данные для отправки на сервер
            const data = {
                userID: `${userID}`,
                Exercise: `${cardTitle}`
            };

            // Отправляем данные на сервер
            fetch('http://localhost:8000/send-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    });
}

function populateTags() {
    const tagSet = new Set();
    exercises.forEach(ex => ex.ex_tags.forEach(tag => tagSet.add(tag)));

    const filterSelect = document.getElementById("filter-select");
    tagSet.forEach(tag => {
        const option = document.createElement("option");
        option.value = tag;
        option.innerText = tag;
        filterSelect.appendChild(option);
    });
}

function filterExercises() {
    const selectedTag = document.getElementById("filter-select").value;
    filteredExercises = selectedTag ? exercises.filter(ex => ex.ex_tags.includes(selectedTag)) : [...exercises];
    currentPage = 1;
    renderExercises();
    prefetchAdjacentPages(); // Предзагрузка соседних страниц после фильтрации
}

function searchExercise() {
    const searchInput = document.getElementById("search-input").value.toLowerCase();
    filteredExercises = exercises.filter(ex => ex.ex_name.toLowerCase().includes(searchInput));
    currentPage = 1;
    renderExercises();
    prefetchAdjacentPages(); // Предзагрузка соседних страниц после поиска
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderExercises();
        prefetchAdjacentPages(); // Предзагрузка соседних страниц после смены страницы
    }
}

function nextPage() {
    if (currentPage * itemsPerPage < filteredExercises.length) {
        currentPage++;
        renderExercises();
        prefetchAdjacentPages(); // Предзагрузка соседних страниц после смены страницы
    }
}

function prefetchAdjacentPages() {
    // Предзагрузка предыдущей страницы
    if (currentPage > 1) {
        const prevPageStart = (currentPage - 2) * itemsPerPage;
        const prevPageEnd = prevPageStart + itemsPerPage;
        const prevPageExercises = filteredExercises.slice(prevPageStart, prevPageEnd);
        prefetchImages(prevPageExercises);
    }

    // Предзагрузка следующей страницы
    if (currentPage * itemsPerPage < filteredExercises.length) {
        const nextPageStart = currentPage * itemsPerPage;
        const nextPageEnd = nextPageStart + itemsPerPage;
        const nextPageExercises = filteredExercises.slice(nextPageStart, nextPageEnd);
        prefetchImages(nextPageExercises);
    }
}

function prefetchImages(exercises) {
    exercises.forEach(exercise => {
        let imgSrc = exercise.ex_img_bytes;
        if (imgSrc.startsWith('C:\\Users\\remez\\PycharmProjects\\Parsing\\poolbilliards.co\\images\\')) {
            imgSrc = imgSrc.replace('C:\\Users\\remez\\PycharmProjects\\Parsing\\poolbilliards.co\\', '');
        }
        imgSrc = imgSrc.replace(/_/g, ' ');

        const img = new Image();
        img.src = imgSrc;
    });
}

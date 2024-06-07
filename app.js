let exercises = [];
let filteredExercises = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener("DOMContentLoaded", () => {
    fetch('exercises_co.json')
        .then(response => response.json())
        .then(data => {
            exercises = data;
            filteredExercises = [...exercises];
            renderExercises();
            populateTags();
            attachButtonClickHandlers(); // Добавляем обработчики нажатия на кнопки после загрузки данных
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
            <button class="change-color-btn">Изменить цвет</button> <!-- Добавляем кнопку -->
        `;
        container.appendChild(card);
    });

    document.getElementById("page-info").innerText = `Страница ${currentPage} из ${Math.ceil(filteredExercises.length / itemsPerPage)}`;
}

function attachButtonClickHandlers() {
    // Добавляем обработчик нажатия на кнопки для каждой карточки
    document.querySelectorAll('.change-color-btn').forEach((btn, index) => {
        btn.addEventListener('click', () => {
            const card = document.querySelectorAll('.card')[index]; // Находим соответствующую карточку
            card.style.backgroundColor = '#f0f0f0'; // Изменяем цвет карточки
            const cardTitle = card.querySelector('h3').innerText; // Получаем название карточки
            const data = { title: cardTitle }; // Формируем данные для отправки на сервер бота
            tg.sendData(data); // Отправляем данные на сервер телеграм бота
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
}

function searchExercise() {
    const searchInput = document.getElementById("search-input").value.toLowerCase();
    filteredExercises = exercises.filter(ex => ex.ex_name.toLowerCase().includes(searchInput));
    currentPage = 1;
    renderExercises();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderExercises();
    }
}

function nextPage() {
    if (currentPage * itemsPerPage < filteredExercises.length) {
        currentPage++;
        renderExercises();
    }
}


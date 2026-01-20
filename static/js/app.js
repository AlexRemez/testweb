let exercises = [];
let filteredExercises = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener("DOMContentLoaded", () => {
    const mainContent = document.getElementById("main-content");
    const container = document.getElementById("exercises-container");
    if (!mainContent || !container) return;

    mainContent.style.display = "none"; // скрываем контент до загрузки

    const tg = window.Telegram.WebApp;
    tg.expand();
    tg.ready();

    // ----------- Загрузка JSON -------------
    fetch('/static/json/exercises_co.json')
        .then(response => response.json())
        .then(data => {
            exercises = data;
            filteredExercises = [...exercises];

            renderExercises();
            populateTags();

            mainContent.style.display = "block"; // показываем контент
            updateBottomNav();
        })
        .catch(err => console.error('Ошибка загрузки JSON:', err));

    // ----------- Рендер карточек -------------
    function renderExercises() {
        container.innerHTML = "";
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const exercisesToShow = filteredExercises.slice(start, end);

        exercisesToShow.forEach(exercise => {
            const card = document.createElement("div");
            card.className = "card";

            let imgSrc = exercise.ex_img_bytes;
            if (imgSrc.startsWith('C:\\Users\\')) {
                imgSrc = imgSrc.replace(/.*\\images\\/, '/static/images/');
            }
            imgSrc = imgSrc.replace(/_/g, ' ');

            card.innerHTML = `
                <h3>${exercise.ex_name}</h3>
                <img src="${imgSrc}" alt="${exercise.ex_name}">
                <p>Тэги: ${exercise.ex_tags.join(", ")}</p>
                <button class="change-color-btn">Выбрать</button>
            `;
            container.appendChild(card);
        });

        const pageInfo = document.getElementById("page-info");
        if (pageInfo) {
            pageInfo.innerText = `Страница ${currentPage} из ${Math.ceil(filteredExercises.length / itemsPerPage)}`;
        }

        attachButtonClickHandlers();
    }

    // ----------- Обработчики кнопок -------------
    function attachButtonClickHandlers() {
        document.querySelectorAll('.change-color-btn').forEach((btn, index) => {
            btn.addEventListener('click', () => {
                const card = document.querySelectorAll('.card')[index];
                if (!card) return;

                card.style.backgroundColor = '#f0f0f0';
                const cardTitle = card.querySelector('h3').innerText;

                const userId = tg.initDataUnsafe?.user?.id || 0;
                const data = { tg_id: userId, exercise: cardTitle };
                const encodedData = encodeURIComponent(JSON.stringify(data));
                window.location.href = `/exercise?data=${encodedData}`;
            });
        });
    }

    // ----------- Фильтры -------------
    function populateTags() {
        const tagSet = new Set();
        exercises.forEach(ex => ex.ex_tags.forEach(tag => tagSet.add(tag)));

        const filterSelect = document.getElementById("filter-select");
        if (!filterSelect) return;

        filterSelect.innerHTML = '<option value="">Все</option>';
        tagSet.forEach(tag => {
            const option = document.createElement("option");
            option.value = tag;
            option.innerText = tag;
            filterSelect.appendChild(option);
        });
    }

    window.filterExercises = () => {
        const selectedTag = document.getElementById("filter-select")?.value || "";
        filteredExercises = selectedTag
            ? exercises.filter(ex => ex.ex_tags.includes(selectedTag))
            : [...exercises];
        currentPage = 1;
        renderExercises();
    };

    window.searchExercise = () => {
        const searchInput = document.getElementById("search-input")?.value.trim() || "";
        filteredExercises = !searchInput
            ? [...exercises]
            : exercises.filter(ex => {
                const match = ex.ex_name.match(/(\d+)$/);
                return match ? match[1] === searchInput : false;
            });
        currentPage = 1;
        renderExercises();
    };

    window.prevPage = () => {
        if (currentPage > 1) {
            currentPage--;
            renderExercises();
        }
    };

    window.nextPage = () => {
        if (currentPage * itemsPerPage < filteredExercises.length) {
            currentPage++;
            renderExercises();
        }
    };

    window.updateBottomNav = () => {
        const path = window.location.pathname;
        const btnHome = document.getElementById('btn-home');
        const btnRanking = document.getElementById('btn-ranking');
        if (!btnHome || !btnRanking) return;

        btnHome.classList.remove('disabled');
        btnRanking.classList.remove('disabled');

        if (path === '/') btnHome.classList.add('disabled');
        else if (path === '/ranking') btnRanking.classList.add('disabled');
    };
});

document.addEventListener('DOMContentLoaded', function () {
    let newsContainer = document.getElementById('news-container');
    let isFetching = false;  // Флаг для предотвращения множественных запросов
    const newsUrl = newsContainer.getAttribute('data-news-url');

    // Функция для отправки AJAX-запроса и обновления новостей
    function fetchNews(page = 1) {
        if (isFetching) return; // Предотвращаем повторный запрос
        isFetching = true;

        const query = document.getElementById('searchNews').value;
        const selectedTag = document.querySelector('.tag-list .selected')?.dataset.tag || document.getElementById('tag-select')?.value || '';
        const url = new URL(window.location.origin + newsUrl);

        // Добавляем параметры запроса
        if (query) url.searchParams.set('search_query', query);
        if (selectedTag) url.searchParams.set('tag', selectedTag);
        url.searchParams.set('page', page);

        // Добавляем класс для плавного исчезновения контента
        newsContainer.classList.add('fade-out');

        setTimeout(() => {
            fetch(url, {headers: {'X-Requested-With': 'XMLHttpRequest'}})
                .then(response => response.json())
                .then(data => {
                    // Обновляем контейнер с новостями и пагинацию
                    newsContainer.innerHTML = data.news_html;
                    document.querySelector('#pagination-container').innerHTML = data.pagination_html;

                    // Убираем класс fade-out и добавляем fade-in для плавного появления
                    newsContainer.classList.remove('fade-out');
                    newsContainer.classList.add('fade-in');

                    // Прокручиваем к началу новостей
                    const isMobile = window.innerWidth <= 768;
                    const newsStart = document.getElementById(isMobile ? 'news-start-mobile' : 'news-start');
                    newsStart.scrollIntoView({behavior: 'smooth'});

                    // Обновляем URL
                    window.history.pushState({}, '', url);

                    // Удаляем класс fade-in после завершения анимации
                    setTimeout(() => {
                        newsContainer.classList.remove('fade-in');
                        isFetching = false; // Снимаем блокировку после завершения
                    }, 1000);

                    // Переподключаем обработчики для тегов и пагинации
                    attachTagEventListeners();
                    attachPaginationEventListeners();
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    isFetching = false;  // Снимаем блокировку в случае ошибки
                });
        }, 500);
    }

    // Обработчик для поиска новостей
    document.getElementById('searchFormNews').addEventListener('submit', function (e) {
        e.preventDefault();
        fetchNews();
    });

    // Функция для установки событий на теги
    function attachTagEventListeners() {
        document.querySelectorAll('#tag-container a').forEach(tagLink => {
            tagLink.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelectorAll('#tag-container a').forEach(tag => tag.classList.remove('selected'));
                this.classList.add('selected');
                fetchNews();
            });
        });

        // Для select, если используешь
        const select = document.getElementById('tag-select');
        if (select) {
            select.addEventListener('change', function () {
                document.querySelectorAll('#tag-container a').forEach(tag => tag.classList.remove('selected'));
                fetchNews();
            });
        }
    }


    // Функция для установки событий на пагинацию
    function attachPaginationEventListeners() {
        document.querySelectorAll('#pagination-container a').forEach(paginationLink => {
            paginationLink.addEventListener('click', function (e) {
                e.preventDefault();
                const page = new URL(this.href).searchParams.get('page');
                fetchNews(page);
            }, {once: true});
        });
    }

    // Инициализация
    attachTagEventListeners();
    attachPaginationEventListeners();
});
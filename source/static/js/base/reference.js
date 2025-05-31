// Скрипт для страницы "Справочная информация"

document.addEventListener("DOMContentLoaded", () => {
  // Инициализация сортировки
  initSorting()

  // Инициализация анимаций
  initAnimations()

  // Обработчики кнопок
  initButtonHandlers()
})

// Функция инициализации сортировки
function initSorting() {
  const sortSelect = document.getElementById("sortSelect")
  const materialsGrid = document.getElementById("materialsGrid")

  if (!sortSelect || !materialsGrid) return

  sortSelect.addEventListener("change", function () {
    const sortType = this.value
    const cards = Array.from(materialsGrid.children)

    // Добавляем класс загрузки
    materialsGrid.classList.add("loading")

    setTimeout(() => {
      // Сортируем карточки
      cards.sort((a, b) => {
        if (sortType === "date") {
          const dateA = Number.parseInt(a.dataset.date)
          const dateB = Number.parseInt(b.dataset.date)
          return dateB - dateA // От новых к старым
        } else if (sortType === "name") {
          const nameA = a.dataset.name.toLowerCase()
          const nameB = b.dataset.name.toLowerCase()
          return nameA.localeCompare(nameB) // По алфавиту
        }
        return 0
      })

      // Очищаем контейнер и добавляем отсортированные карточки
      materialsGrid.innerHTML = ""
      cards.forEach((card) => materialsGrid.appendChild(card))

      // Убираем класс загрузки
      materialsGrid.classList.remove("loading")

      // Перезапускаем анимации
      restartAnimations()
    }, 300)
  })
}

// Функция инициализации анимаций
function initAnimations() {
  // Intersection Observer для анимации появления
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = "running"
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    },
  )

  // Наблюдаем за карточками материалов
  const materialCards = document.querySelectorAll(".material-card")
  materialCards.forEach((card) => {
    card.style.animationPlayState = "paused"
    observer.observe(card)
  })

  // Наблюдаем за карточками разделов
  const sectionCards = document.querySelectorAll(".section-card")
  sectionCards.forEach((card) => {
    observer.observe(card)
  })
}

// Функция перезапуска анимаций
function restartAnimations() {
  const materialCards = document.querySelectorAll(".material-card")
  materialCards.forEach((card, index) => {
    card.style.animation = "none"
    card.offsetHeight // Принудительный reflow
    card.style.animation = `fadeInUp 0.6s ease forwards`
    card.style.animationDelay = `${(index + 1) * 0.1}s`
  })
}

// Функция инициализации обработчиков кнопок
function initButtonHandlers() {
  // Обработчики кнопок "Посмотреть"
  document.addEventListener("click", (e) => {
    if (e.target.closest(".view-button")) {
      e.preventDefault()
      const card = e.target.closest(".material-card")
	  const title = card.querySelector(".material-title").textContent
	  const viewUrl = card.dataset.viewUrl

      // Показываем уведомление
      showNotification(`Открытие документа: ${title}`, "info")

      // Здесь можно добавить логику открытия документа
	  console.log("Открытие документа:", title)
	  if (viewUrl) {
		window.open(viewUrl, "_blank") // открывает PDF в новой вкладке
	  }
    }
  })

  // Обработчики кнопок "Скачать"
  document.addEventListener("click", (e) => {
    if (e.target.closest(".download-button")) {
      e.preventDefault()
      const card = e.target.closest(".material-card")
      const title = card.querySelector(".material-title").textContent

      // Показываем уведомление
      showNotification(`Скачивание документа: ${title}`, "success")

      // Здесь можно добавить логику скачивания документа
      console.log("Скачивание документа:", title)

      // Имитация скачивания
      setTimeout(() => {
        showNotification(`Документ "${title}" успешно скачан`, "success")
      }, 1500)
    }
  })

  // Обработчики кнопок разделов
  document.addEventListener("click", (e) => {
	const button = e.target.closest(".section-button");
    if (e.target.closest(".section-button")) {
      e.preventDefault()
      const card = e.target.closest(".section-card")
      const title = card.querySelector(".section-title").textContent

      // Показываем уведомление
	  showNotification(`Переход к разделу: ${title}`, "info")
	  const url = button.getAttribute("href");
	  if (url && url !== "#") {
		window.open(url, "_blank");
	  }

      // Здесь можно добавить логику перехода к разделу
      console.log("Переход к разделу:", title)
    }
  })
}

// Функция показа уведомлений
function showNotification(message, type = "info") {
  // Создаем элемент уведомления
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`
  notification.textContent = message

  // Добавляем стили
  Object.assign(notification.style, {
    position: "fixed",
    top: "20px",
    right: "20px",
    padding: "1rem 1.5rem",
    borderRadius: "8px",
    color: "white",
    fontWeight: "500",
    zIndex: "9999",
    transform: "translateX(100%)",
    transition: "transform 0.3s ease",
    maxWidth: "300px",
    wordWrap: "break-word",
  })

  // Устанавливаем цвет в зависимости от типа
  switch (type) {
    case "success":
      notification.style.backgroundColor = "#4caf50"
      break
    case "error":
      notification.style.backgroundColor = "#f44336"
      break
    case "warning":
      notification.style.backgroundColor = "#ff9800"
      break
    default:
      notification.style.backgroundColor = "#2196f3"
  }

  // Добавляем в DOM
  document.body.appendChild(notification)

  // Показываем уведомление
  setTimeout(() => {
    notification.style.transform = "translateX(0)"
  }, 100)

  // Скрываем уведомление через 3 секунды
  setTimeout(() => {
    notification.style.transform = "translateX(100%)"
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification)
      }
    }, 300)
  }, 3000)
}

// Функция для плавной прокрутки к элементу
function scrollToElement(element, offset = 0) {
  const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
  const offsetPosition = elementPosition - offset

  window.scrollTo({
    top: offsetPosition,
    behavior: "smooth",
  })
}

// Функция для обновления текущего года в футере
function updateCurrentYear() {
  const yearElement = document.getElementById("currentYear")
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear()
  }
}

// Обновляем год при загрузке
updateCurrentYear()

// Функция для обработки ошибок
function handleError(error, context = "") {
  console.error(`Ошибка ${context}:`, error)
  showNotification("Произошла ошибка. Попробуйте еще раз.", "error")
}

// Функция для проверки поддержки браузера
function checkBrowserSupport() {
  const features = {
    intersectionObserver: "IntersectionObserver" in window,
    css3Animations: CSS.supports("animation", "fadeIn 1s"),
    flexbox: CSS.supports("display", "flex"),
    grid: CSS.supports("display", "grid"),
  }

  const unsupportedFeatures = Object.entries(features)
    .filter(([feature, supported]) => !supported)
    .map(([feature]) => feature)

  if (unsupportedFeatures.length > 0) {
    console.warn("Некоторые функции могут работать некорректно:", unsupportedFeatures)
  }

  return unsupportedFeatures.length === 0
}

// Проверяем поддержку браузера при загрузке
checkBrowserSupport()

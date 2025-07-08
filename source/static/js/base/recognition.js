// Скрипт для страницы "Признание степеней и квалификаций"

document.addEventListener("DOMContentLoaded", () => {
  // Инициализация компонентов
  initAccordions()
  initPageNavigation()
  initContactForm()
  initScrollAnimations()

  // Обновление года в футере
  updateCurrentYear()
})

// Функция инициализации аккордеонов
function initAccordions() {
  // Аккордеоны для руководства
  const guidelineHeaders = document.querySelectorAll('.card-header[data-toggle="collapse"]')
  guidelineHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target")
      const target = document.querySelector(targetId)
      const isExpanded = this.getAttribute("aria-expanded") === "true"

      // Закрываем все остальные аккордеоны в той же группе
      const allHeaders = document.querySelectorAll('.guidelines-section .card-header[data-toggle="collapse"]')
      const allContents = document.querySelectorAll(".guidelines-section .card-content")

      allHeaders.forEach((h) => h.setAttribute("aria-expanded", "false"))
      allContents.forEach((c) => c.classList.remove("show"))

      // Открываем/закрываем текущий аккордеон
      if (!isExpanded) {
        this.setAttribute("aria-expanded", "true")
        target.classList.add("show")

        // Плавная прокрутка к открытому элементу
        setTimeout(() => {
          this.scrollIntoView({ behavior: "smooth", block: "nearest" })
        }, 300)
      }
    })
  })

  // Аккордеоны для глоссария
  const glossaryHeaders = document.querySelectorAll('.glossary-header[data-toggle="collapse"]')
  glossaryHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target")
      const target = document.querySelector(targetId)
      const isExpanded = this.getAttribute("aria-expanded") === "true"

      if (isExpanded) {
        this.setAttribute("aria-expanded", "false")
        target.classList.remove("show")
      } else {
        this.setAttribute("aria-expanded", "true")
        target.classList.add("show")
      }
    })
  })
}

// Функция инициализации навигации по странице
function initPageNavigation() {
  const navLinks = document.querySelectorAll(".page-nav-link")
  const sections = document.querySelectorAll("section[id]")

  // Обработчики кликов по ссылкам навигации
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault()
      const targetId = this.getAttribute("href").substring(1)
      const targetSection = document.getElementById(targetId)

      if (targetSection) {
        const headerHeight = document.querySelector(".header").offsetHeight
        const navHeight = document.querySelector(".page-navigation").offsetHeight
        const offset = headerHeight + navHeight + 20

        const elementPosition = targetSection.getBoundingClientRect().top + window.pageYOffset
        const offsetPosition = elementPosition - offset

        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth",
        })

        // Обновляем активную ссылку
        updateActiveNavLink(this)
      }
    })
  })

  // Отслеживание прокрутки для активной ссылки
  let ticking = false

  function updateNavOnScroll() {
    if (!ticking) {
      requestAnimationFrame(() => {
        const headerHeight = document.querySelector(".header").offsetHeight
        const navHeight = document.querySelector(".page-navigation").offsetHeight
        const offset = headerHeight + navHeight + 100

        let currentSection = null

        sections.forEach((section) => {
          const rect = section.getBoundingClientRect()
          if (rect.top <= offset && rect.bottom >= offset) {
            currentSection = section
          }
        })

        if (currentSection) {
          const activeLink = document.querySelector(`.page-nav-link[href="#${currentSection.id}"]`)
          if (activeLink) {
            updateActiveNavLink(activeLink)
          }
        }

        ticking = false
      })
      ticking = true
    }
  }

  window.addEventListener("scroll", updateNavOnScroll)

  // Функция обновления активной ссылки
  function updateActiveNavLink(activeLink) {
    navLinks.forEach((link) => link.classList.remove("active"))
    activeLink.classList.add("active")
  }
}

// Функция инициализации контактной формы
function initContactForm() {
  const form = document.querySelector(".question-form")

  if (!form) return

  form.addEventListener("submit", function (e) {
    e.preventDefault()

    // Получаем данные формы
    const formData = new FormData(this)
    const data = Object.fromEntries(formData.entries())

    // Валидация
    if (!validateForm(data)) {
      return
    }

    // Показываем индикатор загрузки
    const submitButton = form.querySelector(".submit-button")
    const originalText = submitButton.innerHTML

    submitButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin">
        <path d="M21 12a9 9 0 11-6.219-8.56"/>
      </svg>
      Отправка...
    `
    submitButton.disabled = true

    // Имитация отправки
    setTimeout(() => {
      showNotification("Ваш вопрос успешно отправлен! Мы свяжемся с вами в ближайшее время.", "success")
      form.reset()

      // Восстанавливаем кнопку
      submitButton.innerHTML = originalText
      submitButton.disabled = false
    }, 2000)
  })
}

// Функция валидации формы
function validateForm(data) {
  const errors = []

  if (!data.name || data.name.trim().length < 2) {
    errors.push("Имя должно содержать минимум 2 символа")
  }

  if (!data.email || !isValidEmail(data.email)) {
    errors.push("Введите корректный email адрес")
  }

  if (!data.message || data.message.trim().length < 10) {
    errors.push("Сообщение должно содержать минимум 10 символов")
  }

  if (errors.length > 0) {
    showNotification(errors.join("\n"), "error")
    return false
  }

  return true
}

// Функция проверки email
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Функция инициализации анимаций при прокрутке
function initScrollAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = "running"
          observer.unobserve(entry.target)
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    },
  )

  // Наблюдаем за элементами с анимацией
  const animatedElements = document.querySelectorAll(".guideline-card, .glossary-item, .material-card")
  animatedElements.forEach((element, index) => {
    element.style.animationDelay = `${index * 0.1}s`
    element.style.animationPlayState = "paused"
    observer.observe(element)
  })
}

// Функция показа уведомлений
function showNotification(message, type = "info") {
  // Удаляем существующие уведомления
  const existingNotifications = document.querySelectorAll(".notification")
  existingNotifications.forEach((notification) => notification.remove())

  // Создаем новое уведомление
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`

  // Разбиваем сообщение на строки для многострочных уведомлений
  const lines = message.split("\n")
  if (lines.length > 1) {
    const list = document.createElement("ul")
    lines.forEach((line) => {
      const listItem = document.createElement("li")
      listItem.textContent = line
      list.appendChild(listItem)
    })
    notification.appendChild(list)
  } else {
    notification.textContent = message
  }

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
    maxWidth: "400px",
    wordWrap: "break-word",
    boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
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

  // Скрываем уведомление
  const hideTimeout = type === "error" ? 5000 : 3000
  setTimeout(() => {
    notification.style.transform = "translateX(100%)"
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification)
      }
    }, 300)
  }, hideTimeout)
}

// Функция обновления текущего года
function updateCurrentYear() {
  const yearElement = document.getElementById("currentYear")
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear()
  }
}

// Функция для плавной прокрутки к началу страницы
function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  })
}

// Добавляем кнопку "Наверх" при прокрутке
function initScrollToTop() {
  const scrollButton = document.createElement("button")
  scrollButton.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
  `
  scrollButton.className = "scroll-to-top"
  scrollButton.setAttribute("aria-label", "Прокрутить наверх")

  Object.assign(scrollButton.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    width: "50px",
    height: "50px",
    backgroundColor: "var(--primary-color)",
    color: "white",
    border: "none",
    borderRadius: "50%",
    cursor: "pointer",
    display: "none",
    alignItems: "center",
    justifyContent: "center",
    zIndex: "1000",
    transition: "all 0.3s ease",
    boxShadow: "0 2px 10px rgba(0, 0, 0, 0.2)",
  })

  scrollButton.addEventListener("click", scrollToTop)
  document.body.appendChild(scrollButton)

  // Показываем/скрываем кнопку при прокрутке
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      scrollButton.style.display = "flex"
    } else {
      scrollButton.style.display = "none"
    }
  })
}

// Инициализируем кнопку "Наверх"
initScrollToTop()

// Обработка ошибок
window.addEventListener("error", (e) => {
  console.error("Ошибка на странице:", e.error)
})

// Функция для печати страницы
function printPage() {
  // Раскрываем все аккордеоны перед печатью
  const allContents = document.querySelectorAll(".card-content, .glossary-content")
  allContents.forEach((content) => content.classList.add("show"))

  window.print()
}

// Добавляем обработчик для комбинации Ctrl+P
document.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "p") {
    e.preventDefault()
    printPage()
  }
})

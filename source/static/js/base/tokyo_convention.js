// Токийская конвенция - JavaScript функциональность

document.addEventListener("DOMContentLoaded", () => {
  // Инициализация всех компонентов
  initScrollToTop()
  initSmoothScrolling()
  initVideoPlayers()
  initDocumentActions()
  initAnimations()
  initMobileLanguageDropdown()
})

// Кнопка "Наверх"
function initScrollToTop() {
  const scrollToTopBtn = document.getElementById("scrollToTop")

  if (!scrollToTopBtn) return

  // Показать/скрыть кнопку при прокрутке
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      scrollToTopBtn.classList.add("visible")
    } else {
      scrollToTopBtn.classList.remove("visible")
    }
  })

  // Плавная прокрутка наверх
  scrollToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    })
  })
}

// Плавная прокрутка для якорных ссылок
function initSmoothScrolling() {
  const anchorLinks = document.querySelectorAll('a[href^="#"]')

  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href")

      if (href.startsWith("#") && href.length > 1) {
        e.preventDefault()
        const targetId = href.substring(1)
        const targetElement = document.getElementById(targetId)

        if (targetElement) {
          const headerHeight = document.querySelector(".header").offsetHeight
          const targetPosition = targetElement.offsetTop - headerHeight - 20

          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          })
        }
      }
    })
  })
}

// Видеоплееры
// function initVideoPlayers() {
//   const playButtons = document.querySelectorAll(".play-button")

//   playButtons.forEach((button) => {
//     button.addEventListener("click", function () {
//       const videoCard = this.closest(".video-card")
//       const videoTitle = videoCard.querySelector(".video-title").textContent

//       // Здесь можно добавить логику для открытия видео
//       // Например, модальное окно или переход на страницу видео
//       showNotification(`Открытие видео: ${videoTitle}`, "info")
//     })
//   })
// }
function initVideoPlayers() {
  const playButtons = document.querySelectorAll(".play-button");
  const videoLinks = [
    "https://www.youtube.com/watch?v=74ItiSaAt00",
    "https://www.youtube.com/watch?v=dBrU328Yazk"
  ];

  playButtons.forEach((button, index) => {
    button.addEventListener("click", function () {
      window.open(videoLinks[index], "_blank");
    });
  });
}

// Действия с документами
function initDocumentActions() {
  const viewButtons = document.querySelectorAll(".btn-outline")
  const downloadButtons = document.querySelectorAll(".btn-primary")

  viewButtons.forEach((button) => {
    if (button.textContent.includes("Просмотр")) {
      button.addEventListener("click", function () {
        const documentCard = this.closest(".document-card")
        const documentTitle = documentCard.querySelector(".document-title").textContent

        showNotification(`Открытие документа: ${documentTitle}`, "info")
      })
    }
  })

  downloadButtons.forEach((button) => {
    if (button.textContent.includes("Скачать")) {
      button.addEventListener("click", function () {
        const documentCard = this.closest(".document-card")
        const documentTitle = documentCard.querySelector(".document-title").textContent

        showNotification(`Загрузка документа: ${documentTitle}`, "success")
      })
    }
  })
}

// Анимации при прокрутке
function initAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate-in")
      }
    })
  }, observerOptions)

  // Наблюдаем за элементами для анимации
  const animatedElements = document.querySelectorAll(".info-item, .document-card, .video-card, .stage-card, .info-card")

  animatedElements.forEach((element) => {
    observer.observe(element)
  })
}

// Мобильное языковое меню
function initMobileLanguageDropdown() {
  const mobileLanguageButton = document.querySelector(".mobile-language-button")
  const mobileLanguageDropdown = document.querySelector(".mobile-language-dropdown")

  if (mobileLanguageButton && mobileLanguageDropdown) {
    mobileLanguageButton.addEventListener("click", (e) => {
      e.stopPropagation()
      mobileLanguageDropdown.style.display = mobileLanguageDropdown.style.display === "block" ? "none" : "block"
    })

    // Закрытие при клике вне меню
    document.addEventListener("click", () => {
      mobileLanguageDropdown.style.display = "none"
    })

    // Обработка выбора языка
    const languageOptions = mobileLanguageDropdown.querySelectorAll(".mobile-language-option")
    languageOptions.forEach((option) => {
      option.addEventListener("click", function (e) {
        e.preventDefault()
        const selectedLang = this.textContent
        mobileLanguageButton.childNodes[0].textContent = selectedLang
        mobileLanguageDropdown.style.display = "none"

        showNotification(`Язык изменен на: ${selectedLang}`, "info")
      })
    })
  }
}

// Система уведомлений
function showNotification(message, type = "info") {
  // Удаляем существующие уведомления
  const existingNotifications = document.querySelectorAll(".notification")
  existingNotifications.forEach((notification) => notification.remove())

  // Создаем новое уведомление
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`
  notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${getNotificationIcon(type)}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close">✕</button>
        </div>
    `

  // Добавляем стили для уведомления
  const style = document.createElement("style")
  style.textContent = `
        .notification {
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 1000;
            max-width: 400px;
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            border-left: 4px solid var(--primary-color);
            animation: slideInRight 0.3s ease;
        }
        
        .notification-info { border-left-color: var(--primary-color); }
        .notification-success { border-left-color: #28a745; }
        .notification-warning { border-left-color: var(--accent-color); }
        .notification-error { border-left-color: #dc3545; }
        
        .notification-content {
            display: flex;
            align-items: center;
            padding: 1rem;
            gap: 0.75rem;
        }
        
        .notification-icon {
            font-size: 1.25rem;
            flex-shrink: 0;
        }
        
        .notification-message {
            flex: 1;
            color: var(--text-color);
            font-size: 0.875rem;
            line-height: 1.4;
        }
        
        .notification-close {
            background: none;
            border: none;
            color: var(--text-lighter);
            font-size: 1rem;
            cursor: pointer;
            padding: 0.25rem;
            border-radius: 50%;
            transition: var(--transition);
        }
        
        .notification-close:hover {
            background-color: var(--secondary-color);
            color: var(--text-color);
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @media (max-width: 640px) {
            .notification {
                top: 1rem;
                right: 1rem;
                left: 1rem;
                max-width: none;
            }
        }
    `

  if (!document.querySelector("#notification-styles")) {
    style.id = "notification-styles"
    document.head.appendChild(style)
  }

  // Добавляем уведомление на страницу
  document.body.appendChild(notification)

  // Обработчик закрытия
  const closeButton = notification.querySelector(".notification-close")
  closeButton.addEventListener("click", () => {
    notification.remove()
  })

  // Автоматическое закрытие через 5 секунд
  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove()
    }
  }, 5000)
}

function getNotificationIcon(type) {
  const icons = {
    info: "ℹ️",
    success: "✅",
    warning: "⚠️",
    error: "❌",
  }
  return icons[type] || icons.info
}

// Обработка ошибок
window.addEventListener("error", (e) => {
  console.error("JavaScript Error:", e.error)
})

// Дополнительные утилиты
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Оптимизированная прокрутка
const optimizedScroll = debounce(() => {
  // Дополнительная логика при прокрутке
}, 100)

window.addEventListener("scroll", optimizedScroll)

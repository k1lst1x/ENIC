document.addEventListener("DOMContentLoaded", () => {
  // Установка текущего года в футере
  document.getElementById("currentYear").textContent = new Date().getFullYear()

  // Мобильное меню
  const menuToggle = document.querySelector(".menu-toggle")
  const mobileMenu = document.getElementById("mobileMenu")

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener("click", () => {
      mobileMenu.style.display = mobileMenu.style.display === "block" ? "none" : "block"
    })
  }

  // Поисковая строка
  const searchButton = document.querySelector(".search-button")
  const searchButtonMobile = document.querySelector(".search-button-mobile")
  const searchBar = document.getElementById("searchBar")
  const searchClose = document.querySelector(".search-close")

  if (searchButton && searchBar) {
    searchButton.addEventListener("click", () => {
      searchBar.style.display = "block"
      searchBar.querySelector("input").focus()
    })
  }

  if (searchButtonMobile && searchBar) {
    searchButtonMobile.addEventListener("click", () => {
      searchBar.style.display = "block"
      searchBar.querySelector("input").focus()
    })
  }

  if (searchClose && searchBar) {
    searchClose.addEventListener("click", () => {
      searchBar.style.display = "none"
    })
  }

  // Слайдер новостей
  const sliderTrack = document.getElementById("sliderTrack")
  const slides = sliderTrack ? sliderTrack.querySelectorAll(".slide") : []
  const indicators = document.querySelectorAll(".indicator")
  const prevButton = document.querySelector(".slider-nav.prev")
  const nextButton = document.querySelector(".slider-nav.next")

  let currentSlide = 0
  let slideInterval

  function showSlide(index) {
    if (!sliderTrack) return

    // Скрываем все слайды
    slides.forEach((slide) => {
      slide.classList.remove("active")
    })

    // Убираем активный класс у всех индикаторов
    indicators.forEach((indicator) => {
      indicator.classList.remove("active")
    })

    // Показываем нужный слайд и активируем индикатор
    slides[index].classList.add("active")
    indicators[index].classList.add("active")

    currentSlide = index
  }

  function nextSlide() {
    const newIndex = (currentSlide + 1) % slides.length
    showSlide(newIndex)
  }

  function prevSlide() {
    const newIndex = (currentSlide - 1 + slides.length) % slides.length
    showSlide(newIndex)
  }

  // Инициализация слайдера
  if (slides.length > 0) {
    // Автоматическая смена слайдов
    slideInterval = setInterval(nextSlide, 5000)

    // Обработчики событий для кнопок
    if (prevButton) {
      prevButton.addEventListener("click", () => {
        clearInterval(slideInterval)
        prevSlide()
        slideInterval = setInterval(nextSlide, 5000)
      })
    }

    if (nextButton) {
      nextButton.addEventListener("click", () => {
        clearInterval(slideInterval)
        nextSlide()
        slideInterval = setInterval(nextSlide, 5000)
      })
    }

    // Обработчики событий для индикаторов
    indicators.forEach((indicator, index) => {
      indicator.addEventListener("click", () => {
        clearInterval(slideInterval)
        showSlide(index)
        slideInterval = setInterval(nextSlide, 5000)
      })
    })
  }

  // Табы в блоке событий
  const tabButtons = document.querySelectorAll(".tab-button")
  const tabContents = document.querySelectorAll(".tab-content")

  tabButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const tabId = this.getAttribute("data-tab")

      // Убираем активный класс у всех кнопок и контента
      tabButtons.forEach((btn) => btn.classList.remove("active"))
      tabContents.forEach((content) => content.classList.remove("active"))

      // Активируем нужную вкладку
      this.classList.add("active")
      document.getElementById(`${tabId}-tab`).classList.add("active")
    })
  })

  // Календарь событий
  const calendarDays = document.querySelectorAll(".calendar-day")
  const selectedDateEvents = document.getElementById("selectedDateEvents")

  // События по датам (для демонстрации)
  const eventsByDate = {
    5: [{ title: "Конференция по цифровизации образования", time: "10:00", location: "Онлайн" }],
    25: [{ title: "Семинар по академической мобильности", time: "14:00", location: "Онлайн" }],
    28: [{ title: "Круглый стол с работодателями", time: "11:00", location: "Нур-Султан, ул. Достык, 13" }],
    30: [{ title: "Вебинар по аккредитации образовательных программ", time: "15:30", location: "Онлайн" }],
  }

  calendarDays.forEach((day) => {
    if (day.textContent.trim() !== "") {
      day.addEventListener("click", function () {
        const date = this.textContent.trim()

        // Убираем выделение со всех дней
        calendarDays.forEach((d) => d.classList.remove("selected"))

        // Выделяем выбранный день
        this.classList.add("selected")

        // Показываем события на выбранную дату
        if (selectedDateEvents) {
          if (eventsByDate[date]) {
            let eventsHTML = `<h5 class="calendar-events-title">События на ${date} мая:</h5>`
            eventsHTML += '<div class="calendar-events-list">'

            eventsByDate[date].forEach((event) => {
              eventsHTML += `
                <div class="calendar-event">
                  <p class="calendar-event-title">${event.title}</p>
                  <p class="calendar-event-details">${event.time}, ${event.location}</p>
                </div>
              `
            })

            eventsHTML += "</div>"
            selectedDateEvents.innerHTML = eventsHTML
            selectedDateEvents.style.display = "block"
          } else {
            selectedDateEvents.innerHTML = `<p class="no-events">Нет событий на ${date} мая</p>`
            selectedDateEvents.style.display = "block"
          }
        }
      })
    }
  })

  // Слайдер партнеров
  const partnersSlider = document.getElementById("partnersSlider")
  const partnerPrev = document.querySelector(".partner-nav.prev")
  const partnerNext = document.querySelector(".partner-nav.next")

  if (partnersSlider) {
    if (partnerPrev) {
      partnerPrev.addEventListener("click", () => {
        partnersSlider.scrollBy({ left: -200, behavior: "smooth" })
      })
    }

    if (partnerNext) {
      partnerNext.addEventListener("click", () => {
        partnersSlider.scrollBy({ left: 200, behavior: "smooth" })
      })
    }

    // Автоматическая прокрутка партнеров
    let scrollDirection = 1 // 1 - вправо, -1 - влево
    let isPaused = false

    function autoScroll() {
      if (isPaused) return

      const maxScroll = partnersSlider.scrollWidth - partnersSlider.clientWidth

      // Изменение направления при достижении края
      if (partnersSlider.scrollLeft >= maxScroll - 10) {
        scrollDirection = -1
      } else if (partnersSlider.scrollLeft <= 10) {
        scrollDirection = 1
      }

      partnersSlider.scrollLeft += scrollDirection
    }

    const scrollInterval = setInterval(autoScroll, 30)

    // Пауза при наведении
    partnersSlider.addEventListener("mouseenter", () => {
      isPaused = true
    })

    partnersSlider.addEventListener("mouseleave", () => {
      isPaused = false
    })
  }
})

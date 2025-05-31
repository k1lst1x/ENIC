document.addEventListener("DOMContentLoaded", () => {
  // Фильтрация дайджестов по годам
  const yearButtons = document.querySelectorAll(".year-button")
  const yearSections = document.querySelectorAll(".year-section")

  yearButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const selectedYear = this.getAttribute("data-year")

      // Убираем активный класс у всех кнопок
      yearButtons.forEach((btn) => btn.classList.remove("active"))

      // Активируем выбранную кнопку
      this.classList.add("active")

      // Показываем/скрываем секции
      yearSections.forEach((section) => {
        const sectionYear = section.getAttribute("data-year")

        if (selectedYear === "all" || selectedYear === sectionYear) {
          section.classList.remove("hidden")
        } else {
          section.classList.add("hidden")
        }
      })
    })
  })

  // Анимация появления карточек при прокрутке
  const digestCards = document.querySelectorAll(".digest-card")

  function checkCardsInView() {
    digestCards.forEach((card) => {
      const rect = card.getBoundingClientRect()
      const isInViewport =
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)

      if (isInViewport) {
        card.classList.add("animate")
      }
    })
  }

  // Проверяем при загрузке и при прокрутке
  checkCardsInView()
  window.addEventListener("scroll", checkCardsInView)

  // Обработка кликов по кнопкам "Посмотреть" и "Скачать"
  const viewButtons = document.querySelectorAll(".view-button")
  const downloadButtons = document.querySelectorAll(".download-button")

  viewButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault()
      // Здесь можно добавить логику для открытия PDF в новом окне
	  console.log("Открытие документа для просмотра")
	  const url = button.getAttribute("href");
      window.open(url, "_blank");
    })
  })

  downloadButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault()
      // Здесь можно добавить логику для скачивания файла
      console.log("Скачивание документа")
    })
  })
})

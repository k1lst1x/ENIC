document.addEventListener("DOMContentLoaded", () => {
  // Табы в блоке структуры BFUG
  const structureTabButtons = document.querySelectorAll(".structure-tabs .tab-button")
  const structureTabContents = document.querySelectorAll(".structure-tabs .tab-content")

  structureTabButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const tabId = this.getAttribute("data-tab")

      // Убираем активный класс у всех кнопок и контента
      structureTabButtons.forEach((btn) => btn.classList.remove("active"))
      structureTabContents.forEach((content) => content.classList.remove("active"))

      // Активируем нужную вкладку
      this.classList.add("active")
      document.getElementById(`${tabId}-tab`).classList.add("active")
    })
  })

  // Анимация для таймлайна при прокрутке
  const timelineItems = document.querySelectorAll(".timeline-item")

  function checkTimelineInView() {
    timelineItems.forEach((item) => {
      const rect = item.getBoundingClientRect()
      const isInViewport =
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)

      if (isInViewport) {
        item.classList.add("animate")
      }
    })
  }

  // Проверяем при загрузке и при прокрутке
  checkTimelineInView()
  window.addEventListener("scroll", checkTimelineInView)
})

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const navMenu = document.querySelector("nav ul");

  toggle.addEventListener("click", () => {
    navMenu.classList.toggle("active");
    toggle.classList.toggle("open");
  });
});

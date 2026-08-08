document.addEventListener("DOMContentLoaded", () => {
  // 1. Sticky Navigation Scroll Handler
  const navbar = document.getElementById("navbar");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 20) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });

  // 2. Scroll-Triggered Fade & Slide Animations (IntersectionObserver)
  const revealElements = document.querySelectorAll(".scroll-reveal");

  const observerOptions = {
    root: null,
    rootMargin: "0px 0px -50px 0px",
    threshold: 0.15
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("active");
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  revealElements.forEach((el) => revealObserver.observe(el));

  // Trigger initial hero reveal
  setTimeout(() => {
    const heroElements = document.querySelectorAll("#hero .scroll-reveal");
    heroElements.forEach((el) => el.classList.add("active"));
  }, 100);
});

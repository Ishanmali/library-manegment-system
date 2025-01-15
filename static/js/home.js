import anime from "{{ url_for('static', filename='lib/anime.es.js') }}";

const slides = document.querySelectorAll(".hero");
let currentSlide = 0;

const changeSlide = () => {
    // Remove the 'active' class from the current slide
    slides[currentSlide].classList.remove("active");

    // Update to the next slide
    currentSlide = (currentSlide + 1) % slides.length;

    // Add the 'active' class to the next slide
    slides[currentSlide].classList.add("active");

    // Animation for title and content
    const currentHero = slides[currentSlide];
    const h1 = currentHero.querySelector("h1");
    const p = currentHero.querySelector("p");

    // Title animation
    anime({
        targets: h1,
        translateX: [1000, 0],
        opacity: [0, 1],
        duration: 800,
        easing: 'easeInOutQuad',
    });

    // Paragraph animation
    anime({
        targets: p,
        translateY: [100, 0],
        opacity: [0, 1],
        duration: 800,
        easing: 'easeInOutQuad',
        delay: 300,
    });
};

// Initial active class
slides[currentSlide].classList.add("active");

// Change slide every 3 seconds
setInterval(changeSlide, 3000);

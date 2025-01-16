// JavaScript is not required for the CSS slideshow above. However, if you want to add interactivity like allowing users to change images manually or set the timing dynamically, here's an example for the timing adjustment:

document.addEventListener('DOMContentLoaded', function() {
    const hero = document.querySelector('.hero');
    let intervalTime = 15000; // Default 15 seconds for the background image transition
    
    // Function to set background images manually (if needed)
    function changeBackgroundImage() {
        const images = [
            '{{ url_for("static", filename="image/ai.jpg") }}',
            '{{ url_for("static", filename="image/666.jpg") }}',
            '{{ url_for("static", filename="image/back.jpg") }}'
        ];

        let currentIndex = 0;

        setInterval(function() {
            hero.style.backgroundImage = `url(${images[currentIndex]})`;
            currentIndex = (currentIndex + 1) % images.length;
        }, intervalTime); // Set timing interval as per `intervalTime`
    }

    changeBackgroundImage(); // Start the background image change
});

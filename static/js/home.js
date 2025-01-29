

document.addEventListener('DOMContentLoaded', function() {
    const hero = document.querySelector('.hero');
    let intervalTime = 15000;
    

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
        }, intervalTime); 
    }

    changeBackgroundImage(); 
});

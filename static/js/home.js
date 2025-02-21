

document.addEventListener('DOMContentLoaded', function() {
    const hero = document.querySelector('.hero');
    let intervalTime = 15000;
    

    function changeBackgroundImage() {
        const images = [

        ];

        let currentIndex = 0;

        setInterval(function() {
            hero.style.backgroundImage = `url(${images[currentIndex]})`;
            currentIndex = (currentIndex + 1) % images.length;
        }, intervalTime); 
    }

    changeBackgroundImage(); 
});

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.querySelector("body").classList.add("loaded");
    }, 1000)
  });



  
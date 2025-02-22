

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

  document.addEventListener('DOMContentLoaded', function () {
    const arrowLeft = document.querySelectorAll('.arrow-btn .ri-arrow-left-wide-line');
    const arrowRight = document.querySelectorAll('.arrow-btn .ri-arrow-right-wide-line');

    arrowLeft.forEach(arrow => {
        arrow.addEventListener('click', () => {
            const bookGrid = arrow.closest('.book-section').querySelector('.book-grid');
            bookGrid.scrollBy({ left: -300, behavior: 'smooth' });
        });
    });

    arrowRight.forEach(arrow => {
        arrow.addEventListener('click', () => {
            const bookGrid = arrow.closest('.book-section').querySelector('.book-grid');
            bookGrid.scrollBy({ left: 300, behavior: 'smooth' });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const myapi=   "AIzaSyBXAzmRYtYaq2bBgdMKS3-aUMKt-6uwwJg"     ;
    const new_book= document.getElementById("new-books");
    const fiction_books= document.getElementById("fiction-books");

    fetch(`https://www.googleapis.com/books/v1/volumes?q=new&maxResults=8&key=${myapi}`)
       .then(response => response.json())
       .then(data =>{
        const book =data.item;
        book.forEach(book =>{
            const book_item= Books(book);
            new_book.appendChild(book_item);
        })
       })


       
    fetch('https://www.googleapis.com/books/v1/volumes?q=new&maxResults=8&key=${myapi}')   
      
})



  
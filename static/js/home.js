

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
    const myapi = "AIzaSyBXAzmRYtYaq2bBgdMKS3-aUMKt-6uwwJg"; // Replace with your actual API key
    const newBooksContainer = document.getElementById("new-books");
    const fictionBooksContainer = document.getElementById("fiction-books");

    // Fetch new books
    fetch(`https://www.googleapis.com/books/v1/volumes?q=new&maxResults=8&key=${myapi}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.items) {
                throw new Error('No items found in the response');
            }
            const books = data.items;
            books.forEach(book => {
                const bookItem = createBookItem(book);
                newBooksContainer.appendChild(bookItem);
            });
        })
        .catch(error => {
            console.error('Error fetching new books:', error);
            newBooksContainer.innerHTML = '<p>Failed to load new books. Please try again later.</p>';
        });

    // Fetch fiction books
    fetch(`https://www.googleapis.com/books/v1/volumes?q=fiction&maxResults=8&key=${myapi}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.items) {
                throw new Error('No items found in the response');
            }
            const books = data.items;
            books.forEach(book => {
                const bookItem = createBookItem(book);
                fictionBooksContainer.appendChild(bookItem);
            });
        })
        .catch(error => {
            console.error('Error fetching fiction books:', error);
            fictionBooksContainer.innerHTML = '<p>Failed to load fiction books. Please try again later.</p>';
        });
});

// Function to create a book item
function createBookItem(book) {
    const bookItem = document.createElement('div');
    bookItem.className = 'book-item col-md-3';

    const coverImage = book.volumeInfo.imageLinks?.thumbnail || 'https://via.placeholder.com/150x200'; // Fallback for missing covers
    const title = book.volumeInfo.title;
    const authors = book.volumeInfo.authors?.join(', ') || 'Unknown Author';

    bookItem.innerHTML = `
        <img src="${coverImage}" alt="${title}">
        <h6>${title}</h6>
        <p>${authors}</p>
    `;

    return bookItem;
}


  
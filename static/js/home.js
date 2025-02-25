
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.querySelector("body").classList.add("loaded");
    }, 1000);
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
    const myapi = "AIzaSyBXAzmRYtYaq2bBgdMKS3-aUMKt-6uwwJg"; 
    const newBooksContainer = document.getElementById("new-books");
    const fictionBooksContainer = document.getElementById("fiction-books");

    // Fetch books from the API
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
            newBooksContainer.innerHTML += '<p>Failed to load new books from the API. Please try again later.</p>';
        });

    //  fiction books API
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
            fictionBooksContainer.innerHTML += '<p>Failed to load fiction books from the API. Please try again later.</p>';
        });
});

// Function book item
function createBookItem(book) {
    const bookItem = document.createElement('div');
    bookItem.className = 'book-item col-md-3';

    const coverImage = book.volumeInfo.imageLinks?.thumbnail || 'https://via.placeholder.com/150x200'; 

    bookItem.innerHTML = `
        <img src="${coverImage}" alt="${book.volumeInfo.title}">
    `;

    return bookItem;
}

function createBookItem(book) {
    const bookItem = document.createElement('div');
    bookItem.className = 'book-item col-md-3';

    const coverImage = book.volumeInfo.imageLinks?.thumbnail || 'https://via.placeholder.com/150x200'; 

    bookItem.innerHTML = `
        <img src="${coverImage}" alt="${book.volumeInfo.title}">
    `;

    
    bookItem.addEventListener('click', () => {
        const bookId = book.id; 
        window.location.href = `/book/${bookId}`; 
    });

    return bookItem;
}
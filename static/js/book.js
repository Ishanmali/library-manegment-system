document.addEventListener("DOMContentLoaded", () => {
    const searchBox = document.getElementById("search-box");
    const Filter = document.getElementById("genre-filter");
    const bookRows = document.querySelectorAll(".books-table tbody tr");

    function filterBooks() {
        const searchText = searchBox.value.toLowerCase();
        const Genre = Filter.value;

        bookRows.forEach(row => {
            const title = row.children[1].textContent.toLowerCase();
            const genre = row.children[3].textContent.toLowerCase();

            const matchesSearch = title.includes(searchText);
            const matche= Genre === "all" || genre === Genre;

            row.style.display = matchesSearch && matche ? "" : "none";
        });
    }

    searchBox.addEventListener("input", filterBooks);
    Filter.addEventListener("change", filterBooks);
});

document.addEventListener("DOMContentLoaded", () => {
    const AddBookBtn = document.getElementById("toggle-add-book-form");
    const BookContainer = document.getElementById("add-book-form-container");
    const cancelBtn = document.getElementById("cancel-add-book");
    const addBookForm = document.getElementById("add-book-form");

   
    if (AddBookBtn && BookContainer) {
        AddBookBtn.addEventListener("click", () => {
            if (BookContainer.classList.contains("hidden")) {
                BookContainer.classList.remove("hidden");
                AddBookBtn.textContent = "- Cancel Adding Book";
            } else {
                BookContainer.classList.add("hidden");
                AddBookBtn.textContent = "+ Add New Book";
            }
        });
    }

    if (cancelBtn ) {
        cancelBtn .addEventListener("click", () => {
            BookContainer.classList.add("hidden");
            AddBookBtn.textContent = "+ Add New Book";
        });
    }

    if (addBookForm) {
        addBookForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const title = document.getElementById("title").value;
            const author = document.getElementById("author").value;
            const genre = document.getElementById("genre").value;
            const copies = document.getElementById("copies").value;
            const status = document.getElementById("status").value;

         
            if (!title || !author || !genre || !copies || !status) {
                alert("Please fill out all fields.");
                return;
            }


            const bookTable = document.getElementById("book-table-body");
            const newRow = document.createElement("tr");

            newRow.innerHTML = `
                <td>New</td>
                <td>${title}</td>
                <td>${author}</td>
                <td>${genre}</td>
                <td>${copies}</td>
                <td>${copies > 0 ? "Available" : "Unavailable"}</td>
                <td>
                    <button class="btn edit">Edit</button>
                    <button class="btn delete">Delete</button>
                </td>
            `;
            bookTable.appendChild(newRow);

            addBookForm.reset();

            BookContainer.classList.add("hidden");
            AddBookBtn.textContent = "+ Add New Book";
        });
    }

    document.querySelectorAll('.delete-btn').forEach(button =>{
        button.addEventListener('click' ,(e)=>{
            if(!confirm("are you sure to delete this book "))
            {
                e.preventDefault();
            }
        })
    })
});

document.addEventListener("DOMContentLoaded", () => {
    const searchBox = document.getElementById("search-box");
    const genreFilter = document.getElementById("genre-filter");
    const bookRows = document.querySelectorAll(".books-table tbody tr");

    // Filter books by search or genre
    function filterBooks() {
        const searchText = searchBox.value.toLowerCase();
        const selectedGenre = genreFilter.value;

        bookRows.forEach(row => {
            const title = row.children[1].textContent.toLowerCase();
            const genre = row.children[3].textContent.toLowerCase();

            const matchesSearch = title.includes(searchText);
            const matchesGenre = selectedGenre === "all" || genre === selectedGenre;

            row.style.display = matchesSearch && matchesGenre ? "" : "none";
        });
    }

    searchBox.addEventListener("input", filterBooks);
    genreFilter.addEventListener("change", filterBooks);
});
document.addEventListener("DOMContentLoaded", () => {
    const toggleAddBookFormBtn = document.getElementById("toggle-add-book-form");
    const addBookFormContainer = document.getElementById("add-book-form-container");
    const cancelAddBookBtn = document.getElementById("cancel-add-book");
    const addBookForm = document.getElementById("add-book-form");

    // Show/hide the inline form
    toggleAddBookFormBtn.addEventListener("click", () => {
        if (addBookFormContainer.classList.contains("hidden")) {
            addBookFormContainer.classList.remove("hidden");
            toggleAddBookFormBtn.textContent = "- Cancel Adding Book";
        } else {
            addBookFormContainer.classList.add("hidden");
            toggleAddBookFormBtn.textContent = "+ Add New Book";
        }
    });

    // Hide the form when cancel is clicked
    cancelAddBookBtn.addEventListener("click", () => {
        addBookFormContainer.classList.add("hidden");
        toggleAddBookFormBtn.textContent = "+ Add New Book";
    });

    // Handle form submission
    addBookForm.addEventListener("submit", (event) => {
        event.preventDefault();

        // Collect form data
        const title = document.getElementById("title").value;
        const author = document.getElementById("author").value;
        const genre = document.getElementById("genre").value;
        const copies = document.getElementById("copies").value;
        const status = document.getElementById("status").value;

        // Validate data
        if (!title || !author || !genre || !copies || !status) {
            alert("Please fill out all fields.");
            return;
        }

        // Add new row to the table dynamically
        const bookTableBody = document.getElementById("book-table-body");
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
        bookTableBody.appendChild(newRow);

        // Reset the form
        addBookForm.reset();

        // Hide the form
        addBookFormContainer.classList.add("hidden");
        toggleAddBookFormBtn.textContent = "+ Add New Book";
    });
});

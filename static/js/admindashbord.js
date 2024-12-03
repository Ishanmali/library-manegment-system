document.addEventListener("DOMContentLoaded", () => {
    const menuItems = document.querySelectorAll(".menu-item");
    const mainContent = document.getElementById("main-content");

    menuItems.forEach((item) => {
        item.addEventListener("click", (event) => {
            event.preventDefault(); 

            
            menuItems.forEach((menu) => menu.classList.remove("active"));

          
            item.classList.add("active");

           
            const contentId = item.id; 
            loadContent(contentId, mainContent);
        });
    });

    
    function loadContent(contentId, container) {
        switch (contentId) {
            case "dashboard":
                container.innerHTML = `
                    <h2>Dashboard</h2>
                    <p>Welcome to the dashboard. Here you can manage everything.</p>`;
                break;
            case "books":
                container.innerHTML = `
                    <h2>Books</h2>
                    <p>Here you can manage books.</p>`;
                break;
            case "users":
                container.innerHTML = `
                    <h2>Logged-In Users</h2>
                    <p>View and manage logged-in users.</p>`;
                break;
            case "logout":
                container.innerHTML = `
                    <h2>Logout</h2>
                    <p>You have successfully logged out.</p>`;
                break;
            default:
                container.innerHTML = `<h2>Welcome</h2><p>Click on a menu item to get started.</p>`;
        }
    }
});

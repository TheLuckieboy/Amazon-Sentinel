// main.js
document.addEventListener("DOMContentLoaded", () => {
    console.log("Main.js loaded!");

    const dropdownButton = document.getElementById("dropdown-button");
    const dropdownMenu = document.getElementById("dropdown-menu");

    if (!dropdownButton || !dropdownMenu) {
        console.error("Dropdown elements not found!");
        return;
    }

    console.log("Dropdown elements found!");

    // Toggle dropdown visibility when the button is clicked
    dropdownButton.addEventListener("click", () => {
        const isOpen = dropdownMenu.style.display === "block";
        console.log(`Dropdown is currently ${isOpen ? "open" : "closed"}`);
        dropdownMenu.style.display = isOpen ? "none" : "block";
        console.log(`Dropdown is now ${!isOpen ? "open" : "closed"}`);
    });
});
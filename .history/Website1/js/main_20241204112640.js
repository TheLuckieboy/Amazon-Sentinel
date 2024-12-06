// main.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("Main.js loaded!");

    const options = [
        { value: "all", label: "All" },
        { value: "active", label: "Active" },
        { value: "suspended", label: "Suspended" },
        { value: "terminated", label: "Terminated" }
    ];

    const dropdownButton = document.getElementById("dropdown-button");
    const dropdownButtonLabel = document.getElementById("dropdown-button-label");
    const dropdownMenu = document.getElementById("dropdown-menu");

    if (!dropdownButton || !dropdownMenu) {
        console.error("Dropdown elements not found!");
        return;
    }

    // Populate dropdown options
    options.forEach(option => {
        const li = document.createElement("li");
        li.setAttribute("role", "option");
        li.setAttribute("data-value", option.value);
        li.classList.add("dropdown-item");
        li.textContent = option.label;

        li.addEventListener("click", () => {
            console.log(`Selected: ${option.label}`);
            dropdownButtonLabel.textContent = option.label;
            dropdownMenu.setAttribute("data-open", "false");
            dropdownMenu.style.display = "none";
        });

        dropdownMenu.appendChild(li);
    });

    // Toggle dropdown visibility
    dropdownButton.addEventListener("click", () => {
        const isOpen = dropdownMenu.getAttribute("data-open") === "true";
        dropdownMenu.setAttribute("data-open", isOpen ? "false" : "true");
        dropdownMenu.style.display = isOpen ? "none" : "block";
    });
});

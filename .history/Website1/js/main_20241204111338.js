// main.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("Main.js loaded!");

    // Options for the dropdown
    const options = [
        { value: "all", label: "All" },
        { value: "active", label: "Active" },
        { value: "suspended", label: "Suspended" },
        { value: "terminated", label: "Terminated" }
    ];

    // Target the dropdown elements
    const dropdownButton = document.getElementById("formField104-1733327897845-6089");
    const dropdownMenu = document.getElementById("option-list106-1733327897845-1479");

    if (!dropdownButton || !dropdownMenu) {
        console.error("Dropdown elements not found!");
        return;
    }

    // Populate the dropdown dynamically
    options.forEach(option => {
        const li = document.createElement("li");
        li.setAttribute("role", "option");
        li.setAttribute("data-value", option.value);
        li.classList.add("dropdown-item"); // Add a class for styling, if needed
        li.textContent = option.label;

        // Add click event for selecting an option
        li.addEventListener("click", () => {
            console.log(`Selected: ${option.label}`);
            dropdownButton.querySelector("span.awsui_trigger_dwuol_16dn4_164").textContent = option.label; // Update the button label
            dropdownMenu.setAttribute("data-open", "false"); // Close the menu
            dropdownMenu.style.display = "none"; // Hide menu
        });

        dropdownMenu.appendChild(li);
    });

    console.log("Dropdown options added!");

    // Toggle dropdown menu visibility on button click
    dropdownButton.addEventListener("click", () => {
        const isOpen = dropdownMenu.getAttribute("data-open") === "true";
        dropdownMenu.setAttribute("data-open", isOpen ? "false" : "true");
        dropdownMenu.style.display = isOpen ? "none" : "block"; // Show or hide the menu
    });
});

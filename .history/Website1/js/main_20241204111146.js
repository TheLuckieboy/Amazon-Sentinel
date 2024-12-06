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

    // Target the dropdown list
    const dropdown = document.getElementById("option-list106-1733327897845-1479");

    // Check if the dropdown element exists
    if (dropdown) {
        // Populate the dropdown dynamically
        options.forEach(option => {
            const li = document.createElement("li");
            li.setAttribute("role", "option");
            li.setAttribute("data-value", option.value);
            li.textContent = option.label;
            dropdown.appendChild(li);
        });
        console.log("Dropdown options added!");
    } else {
        console.error("Dropdown element not found!");
    }
});

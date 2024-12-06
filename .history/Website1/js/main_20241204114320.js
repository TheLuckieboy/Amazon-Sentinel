// Wait for the DOM to load before executing
document.addEventListener("DOMContentLoaded", function() {
    // Select the input element by its ID
    const inputField = document.getElementById('formField114-1733328551164-4247');

    // Optional: Add a listener to handle input changes (if you need it)
    inputField.addEventListener('input', function() {
        // Get the current value of the input field
        const inputValue = inputField.value;
        
        // Log or use the input value as needed
        console.log("Input Value: ", inputValue);
        
        // Example: Store it for later use
        sessionStorage.setItem("employeeID", inputValue);
    });

    // Example: Retrieve the stored input value later (when needed)
    const storedValue = sessionStorage.getItem("employeeID");
    console.log("Stored Employee ID: ", storedValue);
});

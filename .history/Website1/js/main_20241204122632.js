document.addEventListener("DOMContentLoaded", function() {
    // Select the input element and the search button
    const inputField = document.getElementById('formField114-1733328551164-4247');
    const searchButton = document.querySelector('button[data-analytics-funnel-value="button130-1733328551171-3358"]');
    
    // Function to perform search (for both button click and Enter key press)
    function performSearch() {
        const inputValue = inputField.value;

        // Check if the input value exists
        if (inputValue.trim()) {
            // Log or process the search (use inputValue to search the profile)
            console.log("Searching for profile with ID: ", inputValue);

            // Example: Store the input value in sessionStorage if not already done
            sessionStorage.setItem("employeeID", inputValue);
            
        } else {
            console.log("Please enter an Employee ID.");
        }
    }

    // Button click event listener to trigger search
    searchButton.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent the form from submitting if inside a form
        performSearch();  // Call the search function
    });

    // Listen for the "Enter" key press to trigger the search
    inputField.addEventListener('keypress', function(event) {
        if (event.key === "Enter") {
            event.preventDefault();  // Prevent form submission if inside a form
            performSearch();  // Call the search function on Enter key
        }
    });
});

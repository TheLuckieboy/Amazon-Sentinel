document.addEventListener("DOMContentLoaded", function() {
    // Select the input element and the search button
    const inputField = document.getElementById('formField114-1733328551164-4247');
    const searchButton = document.querySelector('button[data-analytics-funnel-value="button130-1733328551171-3358"]');
    
    function performSearch() {
        const inputValue = inputField.value.trim();
    
        if (inputValue) {
            console.log("Searching for profile with ID:", inputValue);
    
            // Fetch profiles from the server
            fetch('http://localhost:3000/profiles.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch profiles.');
                    }
                    return response.json();
                })
                .then(profiles => {
                    // Search for a profile with the matching ID
                    const profile = profiles.find(p => p.ID === inputValue);
    
                    if (profile) {
                        // Log profile information to the console
                        console.log("Profile found:", profile);
                    } else {
                        // Log a message if no profile is found
                        console.log("Profile not found.");
                    }
                })
                .catch(error => {
                    // Log errors to the console
                    console.error("Error fetching profiles:", error);
                });
    
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

document.addEventListener("DOMContentLoaded", function() {
    // Select the input element and the search button
    const inputField = document.getElementById('formField114-1733328551164-4247');
    const searchButton = document.querySelector('button[data-analytics-funnel-value="button130-1733328551171-3358"]');
    
    function performSearch() {
        const inputValue = inputField.value;
    
        // Check if the input value exists
        if (inputValue.trim()) {
            console.log("Searching for profile with ID: ", inputValue);
    
            // Fetch the profile data based on inputValue (ID)
            fetch('http://localhost:3000/profiles.json')
                .then(response => response.json())
                .then(profiles => {
                    // Find the profile that matches the input ID
                    const profile = profiles.find(p => p.id === inputValue);
    
                    if (profile) {
                        console.log('Found profile:', profile);
                        // Here, you can later display the profile data on the page
                    } else {
                        console.log('Profile not found.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching profiles:', error);
                });
            
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

document.addEventListener("DOMContentLoaded", function() {
    // Select the input element and the search button
    const idInputField = document.getElementById('formField114-1733328551164-4247');
    const loginInputField = document.getElementById('formField113-1733328551163-6001');
    const searchButton = document.querySelector('button[data-analytics-funnel-value="button130-1733328551171-3358"]');
    
    // Function to perform search based on input type
    function performSearch() {
        const idInputValue = idInputField.value.trim();
        const loginInputValue = loginInputField.value.trim();

        if (!idInputValue && !loginInputValue) {
            console.log("Please enter an Employee ID or Login.");
            return;
        }

        console.log("Performing search...");
        fetch('http://localhost:3000/profiles.json')
            .then(response => response.json())
            .then(profiles => {
                let profile = null;

                if (idInputValue) {
                    profileData = profiles.find(p => p.Employee_ID === idInputValue);
                } else if (loginInputValue) {
                    profileData = profiles.find(p => p.Login === loginInputValue);
                }

                if (profileData) {
                    //console.log('Found profile:', profileData);
                    //displayProfile(profileData);
                    console.log('Profile.');
                } else {
                    console.log('Profile not found.');
                }
            })
            .catch(error => {
                console.error('Error fetching profiles:', error);
            });
    }

    // Button click event listener
    searchButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent form submission
        performSearch();
    });

    // Enter key event listeners for both inputs
    idInputField.addEventListener('keypress', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            performSearch();
        }
    });

    loginInputField.addEventListener('keypress', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            performSearch();
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById('formField114-1733328551164-4247');
    const searchButton = document.querySelector('button[data-analytics-funnel-value="button130-1733328551171-3358"]');
    
    // Fetch profiles from the server
    async function fetchProfiles() {
        const response = await fetch('/profiles');
        const profiles = await response.json();
        return profiles;
    }

    // Function to perform search
    async function performSearch() {
        const inputValue = inputField.value.trim();
        const profiles = await fetchProfiles();  // Fetch profiles

        if (inputValue) {
            // Search the profiles list for a match
            const profile = profiles.find(p => p.id === inputValue);

            if (profile) {
                // If the profile is found, display it
                displayProfile(profile);
            } else {
                alert("Profile not found.");
            }
        } else {
            alert("Please enter an Employee ID.");
        }
    }

    // Function to display the profile
    function displayProfile(profile) {
        const profileSection = document.getElementById("profileDisplay");
        profileSection.innerHTML = `
            <h3>Profile Found:</h3>
            <p><strong>ID:</strong> ${profile.id}</p>
            <p><strong>Name:</strong> ${profile.name}</p>
            <p><strong>Title:</strong> ${profile.title}</p>
            <p><strong>Status:</strong> ${profile.status}</p>
        `;
    }

    searchButton.addEventListener('click', function(event) {
        event.preventDefault();
        performSearch();
    });

    inputField.addEventListener('keypress', function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            performSearch();
        }
    });
});

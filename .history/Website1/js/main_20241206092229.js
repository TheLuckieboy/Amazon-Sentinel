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
                    profile = profiles.find(p => p.Employee_ID === idInputValue);
                } else if (loginInputValue) {
                    profile = profiles.find(p => p.Login === loginInputValue);
                }

                if (profile) {
                    console.log('Found profile:', profile);
                    displayProfile(profile);
                } else {
                    console.log('Profile not found.');
                }
            })
            .catch(error => {
                console.error('Error fetching profiles:', error);
            });
    }
    
    function displayProfile(profile) {
        console.log("Profile Information:");
        console.log(`Login: ${profile.Login}`);
        console.log(`Employee ID: ${profile.Employee_ID}`);
        console.log(`Person ID: ${profile.Person_ID}`);
        console.log(`Name: ${profile.First_Name} ${profile.Last_Name}`);
        console.log(`Type: ${profile.Employee_Type}`);
        console.log(`Status: ${profile.Employee_Status}`);
        console.log(`Manager: ${profile.Manager}`);
        console.log(`Tenure: ${profile.Tenure}`);
        console.log(`Region: ${profile.Region}`);
        console.log(`Building/Country: ${profile["Building/Country"]}`);
        console.log(`Badge Count: ${profile.Badge_Count}`);
        console.log("Badges:");
        profile.Badges.forEach((badge, index) => {
            console.log(`  Badge ${index + 1}:`);
            console.log(`    ID: ${badge.Badge_ID}`);
            console.log(`    Status: ${badge.Badge_Status}`);
            console.log(`    Type: ${badge.Badge_Type}`);
            console.log(`    Activate On: ${badge.Badge_ActivateOn}`);
            console.log(`    Deactivate On: ${badge.Badge_DeactivateOn}`);
            console.log(`    Last Updated: ${badge.Badge_LastUpdatedUTC}`);
            console.log(`    Last Location Reader Name: ${badge.Badge_LastLocationReaderName}`);
            console.log(`    Last Location Event Type: ${badge.Badge_LastLocationEventType}`);
        });
        console.log(`Access Level Count: ${profile.AccessLvl_Count}`);
        console.log("Access Levels:");
        profile.AccessLvl.forEach((access, index) => {
            console.log(`  Access Level ${index + 1}:`);
            console.log(`    Level: ${access.AccessLevel}`);
            console.log(`    Activate On: ${access.AccessLevel_ActivateOn}`);
            console.log(`    Deactivate On: ${access.AccessLevel_Deactivate}`);
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

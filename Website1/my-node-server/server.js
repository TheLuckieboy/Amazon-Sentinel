const express = require('express');
const app = express();
const path = require('path');
const fs = require('fs');
const cors = require('cors');

// Enable CORS for cross-origin requests
app.use(cors());

// Serve static files (HTML, CSS, JS) from the "Website1" directory
app.use(express.static(path.join(__dirname, 'Website1')));

// API endpoint to fetch profiles
app.get('/profiles.json', (req, res) => {
    // Correct the path to point directly to 'profiles.json' in the 'my-node-server' folder
    const profilesPath = path.join(__dirname, 'profiles.json');
    console.log('Looking for profiles.json at:', profilesPath); // Log the path being used

    fs.readFile(profilesPath, 'utf8', (err, data) => {
        if (err) {
            console.error("Error reading profiles.json file:", err); // Log the error
            return res.status(500).send("Error reading profiles file.");
        }
        res.json(JSON.parse(data)); // Send JSON data
    });
});

// Start the server on port 3000
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});

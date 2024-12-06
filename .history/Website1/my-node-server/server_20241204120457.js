const express = require('express');
const app = express();
const path = require('path');
const fs = require('fs');

// Serve static files (like HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'Website1')));

// API endpoint to fetch profiles
app.get('/profiles', (req, res) => {
    fs.readFile('./profiles.json', 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send("Error reading profiles file.");
        }
        res.json(JSON.parse(data));
    });
});

// Start the server on port 3000
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
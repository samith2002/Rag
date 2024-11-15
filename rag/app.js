// app.js

const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const axios = require("axios");  // For making HTTP requests to the Python server

const app = express();
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "views", "index.html"));
});

app.post("/query", async (req, res) => {
    const { query } = req.body;

    try {
        // Send the query to the Python RAG API server
        const response = await axios.post("http://127.0.0.1:5000/query", { query });
        res.json(response.data);  // Forward the response from Python to the frontend
    } catch (error) {
        res.status(500).json({ error: "Error fetching response from Python API" });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Node.js server running on http://localhost:${PORT}`);
});

const express = require('express');
const app = express();
const PORT = 3001;

// Define a route handler for the root path
app.get('/', (req, res) => {
  res.send('Welcome to the backend server!');
});

// Define your existing /api/ping route
app.get('/api/ping', (req, res) => {
  res.json({ message: 'pong' });
});

app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});

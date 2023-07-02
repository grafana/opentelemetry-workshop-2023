// Configure app
const express = require('express')
const app = express()

// Handle requests to http://localhost:4321/
app.get('/', (req, res) => {
  res.send('ok')
})

// Handle requests to http://localhost:4321/error
app.get('/error', (req, res) => {
  throw new Error()
})

// Run the app when executing this file
app.listen(4321, '0.0.0.0', () => {
  console.log('Running on 0.0.0.0:4321')
})

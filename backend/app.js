const express = require('express')
const app = express()
const cors = require('cors')
app.use(cors())
app.use(express.json())
app.use(express.static('../frontend/dist'))
// endpoints
app.get('/api', (req, res) => res.json({ message: 'Hello REST API' }))

const port = 3000
app.listen(port, () => {
  console.log(`Server is running on port ${port}`)
})

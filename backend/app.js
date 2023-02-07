const express = require('express')
const app = express()
const cors = require('cors')
app.use(cors())
app.use(express.json())
app.use(express.static('../frontend/dist'))
const getSubtitles = require('youtube-captions-scraper').getSubtitles
// endpoints
app.get('/api/:videoId', async (req, res) => {
  await getSubtitles({
    videoID: req.params.videoId,
    lang: 'es'
  }).then(function (captions) {
    let ans = captions.map(caption => caption.text.replaceAll('\"/\n', ' ').replaceAll('[Música]', ''))
    ans = ans.join(' ')
    res.status(200).json({ data: ans })
  }).catch((err) => { res.status(409).json({ message: 'Not found' }) })
})

// end scraper
const port = 3000
app.listen(port, () => {
  console.log(`Server is running on port ${port}`)
})

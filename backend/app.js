const path = require('path')
const express = require('express')
const app = express()
const cors = require('cors')

const cohere = require('cohere-ai')
cohere.init(process.env.COHERE_API_KEY)
app.use(cors())
app.use(express.json())
app.use(express.static(path.join('..', 'frontend', 'dist')))
const getSubtitles = require('youtube-captions-scraper').getSubtitles
// endpoints
app.get('/api/:videoId', async (req, res) => {
  await getSubtitles({
    videoID: req.params.videoId,
    lang: 'es'
  }).then(async function (captions) {
    let ans = captions.map(caption => caption.text.replaceAll('"/\n', ' ').replaceAll('[Música]', ''))
    ans = ans.join(' ')
    const response = await cohere.generate({
      model: 'command-xlarge-nightly',
      prompt: `Summary the main idea of the following text:\n\n${ans}`,
      max_tokens: 64,
      temperature: 0.9,
      k: 0,
      p: 0.75,
      frequency_penalty: 0,
      presence_penalty: 0,
      stop_sequences: [],
      return_likelihoods: 'NONE'
    })
    console.log(`Prediction: ${response.body.generations[0].text}`)

    res.status(200).json({ data: response.body.generations[0].text })
  }).catch(() => { res.status(409).json({ message: 'Not found' }) })
})

const port = 3000 || process.env.PORT
app.listen(port, () => {
  console.log(`Server is running on port ${port}`)
})

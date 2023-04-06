<script setup>
import AppBarComponent from './components/AppBarComponent.vue'
import BannerComponent from './components/BannerComponent.vue'
import debounce from 'just-debounce-it'
import { ref } from 'vue'
let searchInput = ref('')
let loading = ref(false)
let loadingWithUserAPI = ref(false)
let videoId = ref('')
let userAPIKey = ref('')
let summary = ref('')
let captions = ref('')
let player = ref('')
let responseOk = ref('')
let warningMessage = ref('')
const exampleURLVideo = 'https://youtu.be/rB9ql0L0cUQ'

function isYoutubeUrl(url) {
  const pattern = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+$/;
  return pattern.test(url);
}

const search = debounce(async () => {
  loading.value = true
  if (!searchInput.value) {
    resetValues()
    return
  }

  videoId.value = ''
  summary.value = ''
  captions.value = ''
  warningMessage.value = ''

  if (!isYoutubeUrl(searchInput.value)) {
    warningMessage.value = 'Invalid link'
    loading.value = false
    return
  }
  videoId.value = getVideoId(searchInput.value)
  await fetch(`/api/${videoId.value}`)
    .then(response => {
      responseOk.value = response.ok
      return response
    })
    .then(data => data.json())
    .then(data => {
      console.log(data)
      return data
    })
    .then(data => {
      summary.value = data.data
      captions.value = data.captions
    }).then(() => {
      player.value = new YT.Player('video-player', {
        width: '100%',
        height: '100%',
        videoId: videoId.value
      })
    }).catch(error => {
      warningMessage.value = "We couldn't summarize this video."
      console.error(error)
    })
  loading.value = false
  console.log("loading", loading.value);
}, 800, true)

const resetValues = () => {
  searchInput.value = ''
  loading.value = false
  loadingWithUserAPI.value = false
  videoId.value = ''
  userAPIKey.value = ''
  summary.value = ''
  captions.value = ''
  player.value = null
  responseOk.value = ''
  warningMessage.value = ''
  document.querySelector('#video-player-parent').innerHTML = '<div id="video-player"></div>'
}

const pasteFromClipboard = async () => {
  try {
    // when user click paste from clipboard ask to able navigator clipboard
    await navigator.permissions.query({ name: 'clipboard-read' })
    const text = await navigator.clipboard.readText()
    searchInput.value = text
    search()
  } catch (error) {
    console.error(error)
  }
}

const copyToClipboard = async (text = 'https://youtu.be/uyEUVgNMvGI') => {
  try {
    await navigator.clipboard.writeText(text)
  } catch (error) {
    console.error(error)
  }
}

const getVideoId = (urlVideo) => {
  try {
    // 
    const pattern = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+$/;
    if (!pattern.test(urlVideo))
      throw new Error('Invalid URL')
    const url = new URL(urlVideo)
    const searchParams = new URLSearchParams(url.search)
    return searchParams.get('v') || url.pathname.split('/').pop()
  } catch {
    warningMessage.value = 'Invalid link'
    console.log('Invalid link');
  }
  return ''
}

const formatToTime = (seconds) => {
  // this functions format seconds to hours, minutes and seconds
  const date = new Date(null)
  date.setSeconds(seconds)
  return date.toISOString().substr(11, 8)

}

const seekTo = (startSecond) => {
  player.value.seekTo(parseInt(startSecond))
}

const useUserAPIKey = async openaiAPIKey => {
  const apiUrl = 'https://api.openai.com/v1/chat/completions'
  let capsJoined = captions.value.map(i => i.text).join(' ').replace(/\n/g, ' ')
  capsJoined = capsJoined.replace(/\[.*?\]/g, '')
  const data = {
    model: 'gpt-3.5-turbo',
    messages: [
      { role: 'user', content: "Summarize in Spanish the following text extracted of a YouTube video: \n" + capsJoined }
    ]
  }
  loadingWithUserAPI.value = true
  let res = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${openaiAPIKey}`
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      summary.value = data.choices[0].message.content
      return data
    })
    .catch(error => console.error(error))
  console.log({ res });
  loadingWithUserAPI.value = false

}

</script>

<template>
  <AppBarComponent />
  <main class="container"
    :style="{ 'justifyContent': summary ? 'start' : 'center', 'height': responseOk ? 'auto' : '80vh' }">
    <BannerComponent v-show="!responseOk" />
    <form class="searcher-form" @submit.prevent="">
      <input v-model="searchInput" type="" placeholder="Paste a YouTube Link here" @input="search()">
      <button class="search-cleaner" v-show="searchInput" @click="resetValues()">
        <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" fill="#000000">
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <path fill="#000000"
              d="M764.288 214.592 512 466.88 259.712 214.592a31.936 31.936 0 0 0-45.12 45.12L466.752 512 214.528 764.224a31.936 31.936 0 1 0 45.12 45.184L512 557.184l252.288 252.288a31.936 31.936 0 0 0 45.12-45.12L557.12 512.064l252.288-252.352a31.936 31.936 0 1 0-45.12-45.184z">
            </path>
          </g>
        </svg>
      </button>
      <button class="past-clipboard" @click="pasteFromClipboard()" v-show="!searchInput">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <path
              d="M14.3498 2H9.64977C8.60977 2 7.75977 2.84 7.75977 3.88V4.82C7.75977 5.86 8.59977 6.7 9.63977 6.7H14.3498C15.3898 6.7 16.2298 5.86 16.2298 4.82V3.88C16.2398 2.84 15.3898 2 14.3498 2Z"
              fill="#000000"></path>
            <path
              d="M17.2391 4.81949C17.2391 6.40949 15.9391 7.70949 14.3491 7.70949H9.64906C8.05906 7.70949 6.75906 6.40949 6.75906 4.81949C6.75906 4.25949 6.15906 3.90949 5.65906 4.16949C4.24906 4.91949 3.28906 6.40949 3.28906 8.11949V17.5295C3.28906 19.9895 5.29906 21.9995 7.75906 21.9995H16.2391C18.6991 21.9995 20.7091 19.9895 20.7091 17.5295V8.11949C20.7091 6.40949 19.7491 4.91949 18.3391 4.16949C17.8391 3.90949 17.2391 4.25949 17.2391 4.81949ZM15.7491 16.9995C15.7491 17.4095 15.4091 17.7495 14.9991 17.7495H11.9991C11.5891 17.7495 11.2491 17.4095 11.2491 16.9995C11.2491 16.5895 11.5891 16.2495 11.9991 16.2495H13.1891L8.46906 11.5295C8.17906 11.2395 8.17906 10.7595 8.46906 10.4695C8.75906 10.1795 9.23906 10.1795 9.52906 10.4695L14.2491 15.1895V13.9995C14.2491 13.5895 14.5891 13.2495 14.9991 13.2495C15.4091 13.2495 15.7491 13.5895 15.7491 13.9995V16.9995Z"
              fill="#000000"></path>
          </g>
        </svg>
      </button>
    </form>
    <div>
      <div v-show="responseOk" class="result-success">
        <div class="result-success-preview">
          <div id="video-player-parent" style="width: 100%; aspect-ratio: 16 / 9;">
            <div id="video-player"></div>
          </div>
          <div>
            <div v-if="summary">
              <h4>Summary:</h4>
              <p>{{ summary }}</p>
            </div>
            <div v-else>
              <form class="form-to-request-user-api-key" @submit.prevent="">
                <p style="text-align: center;">
                  <strong style="text-transform: uppercase;">⚠️ We couldn't generate a summary. ⚠️</strong><br>
                </p>
                <p style="margin-bottom: .5rem;">Try putting your own <a
                    href="https://platform.openai.com/account/api-keys" target="_blank">OPENAI_API_KEY
                    <svg style="width: 0.85rem; transform: scale(-1,1);" viewBox="0 0 24 24" fill="none"
                      xmlns="http://www.w3.org/2000/svg">
                      <g id="SVGRepo_bgCarrier" stroke-width="0" class="astro-F5U63AYJ"></g>
                      <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" class="astro-F5U63AYJ">
                      </g>
                      <g id="SVGRepo_iconCarrier" class="astro-F5U63AYJ">
                        <path
                          d="M3 3V2.5H2.5V3H3ZM12.6464 13.3536C12.8417 13.5488 13.1583 13.5488 13.3536 13.3536C13.5488 13.1583 13.5488 12.8417 13.3536 12.6464L12.6464 13.3536ZM3.5 11V3H2.5V11H3.5ZM3 3.5H11V2.5H3V3.5ZM2.64645 3.35355L12.6464 13.3536L13.3536 12.6464L3.35355 2.64645L2.64645 3.35355Z"
                          fill="currentColor" class="astro-F5U63AYJ"></path>
                        <path
                          d="M4 15V15C4 16.8692 4 17.8038 4.40192 18.5C4.66523 18.9561 5.04394 19.3348 5.5 19.5981C6.19615 20 7.13077 20 9 20H14C16.8284 20 18.2426 20 19.1213 19.1213C20 18.2426 20 16.8284 20 14V9C20 7.13077 20 6.19615 19.5981 5.5C19.3348 5.04394 18.9561 4.66523 18.5 4.40192C17.8038 4 16.8692 4 15 4V4"
                          stroke="currentColor" stroke-linecap="round" class="astro-F5U63AYJ"></path>
                      </g>
                    </svg>
                  </a>.</p>
                <div style="display: flex; gap: .8rem">
                  <input type="text" v-model="userAPIKey" placeholder="Paste your OPENAI API KEY here"
                    style="margin-bottom: 0;">
                  <button type="submit" style="width: 3.5rem;" @click="useUserAPIKey(userAPIKey)">Try</button>
                </div>
                <p class="suggestion-link">Data will not be stored</p>
                <a v-if="loadingWithUserAPI" href="#" aria-busy="true">Getting data, please wait…</a>
              </form>
            </div>

          </div>
        </div>
        <div>
          <h4 style="margin-bottom: .5rem;">Captions</h4>
          <div class="result-success-summary auto-scroll" style="min-height: 300px;">
            <!-- iterate captions  -->
            <p v-for="caption in captions" :key="caption" style="margin-bottom: 0;">
              <span style="color: #3ea6ff; cursor: pointer;" @click="seekTo(caption.start)">
                {{ formatToTime(caption.start) }}
              </span>:
              <span>{{ caption.text }}</span>
            </p>
          </div>
        </div>
      </div>
      <div class="result-unknown">
        <a v-if="loading" href="#" aria-busy="true">Getting data, please wait…</a>
        <div v-else>
          <div v-show="!searchInput" class="suggestion-link">
            For example copy
            <a :href="exampleURLVideo" target="_blank">
              this link</a>
            video 👉
            <button @click="copyToClipboard(text = exampleURLVideo)">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                  <path
                    d="M16 16V18.8C16 19.9201 16 20.4802 15.782 20.908C15.5903 21.2843 15.2843 21.5903 14.908 21.782C14.4802 22 13.9201 22 12.8 22H5.2C4.0799 22 3.51984 22 3.09202 21.782C2.71569 21.5903 2.40973 21.2843 2.21799 20.908C2 20.4802 2 19.9201 2 18.8V11.2C2 10.0799 2 9.51984 2.21799 9.09202C2.40973 8.71569 2.71569 8.40973 3.09202 8.21799C3.51984 8 4.0799 8 5.2 8H8M11.2 16H18.8C19.9201 16 20.4802 16 20.908 15.782C21.2843 15.5903 21.5903 15.2843 21.782 14.908C22 14.4802 22 13.9201 22 12.8V5.2C22 4.0799 22 3.51984 21.782 3.09202C21.5903 2.71569 21.2843 2.40973 20.908 2.21799C20.4802 2 19.9201 2 18.8 2H11.2C10.0799 2 9.51984 2 9.09202 2.21799C8.71569 2.40973 8.40973 2.71569 8.21799 3.09202C8 3.51984 8 4.07989 8 5.2V12.8C8 13.9201 8 14.4802 8.21799 14.908C8.40973 15.2843 8.71569 15.5903 9.09202 15.782C9.51984 16 10.0799 16 11.2 16Z"
                    stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                </g>
              </svg>
            </button>
          </div>
          <p style="color: #ff0e0e;" v-show="searchInput && warningMessage">
            {{ warningMessage }}
          </p>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 80vh;
  width: min(100%, 1024px);
}

h4 {
  margin-bottom: 1rem;
}

form.searcher-form input {
  border-radius: 30px;
}

.searcher-form {
  display: flex;
  align-items: center;
  gap: 5px;
  width: min(100%, 720px);
  margin: 0 auto;
}

.search-cleaner {
  width: 55px;
  padding: 0;
  background-color: transparent;
  border-radius: 50%;
  border: none;
  padding: 8px;
}

.past-clipboard {
  width: 55px;
  padding: 0;
  background-color: transparent;
  border-radius: 50%;
  border: 1px solid #41546277;
  padding: 8px;
}

.suggestion-link {
  font-size: .9rem;
  color: #999;
  text-align: center;
}

.suggestion-link button {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  padding: 0 6px;
  background-color: transparent;
  border: none;
}

.result-unknown {
  min-height: 100px;
}

.auto-scroll {
  /* add scroll if content is much large */
  overflow-y: auto;
  max-height: 100%;
}

.auto-scroll {
  --sb-track-color: #eeeeee;
  --sb-thumb-color: #b3b3b3;
  --sb-size: 10px;
  scrollbar-color: var(--sb-thumb-color) var(--sb-track-color);
}

.auto-scroll::-webkit-scrollbar {
  width: var(--sb-size);
}

.auto-scroll::-webkit-scrollbar-track {
  background: var(--sb-track-color);
  border-radius: 8px;
}

.auto-scroll::-webkit-scrollbar-thumb {
  background: var(--sb-thumb-color);
  border-radius: 8px;
}

.result-title {
  margin: 1rem 0;
  font-size: 1.3rem;
  font-weight: 400;
}

.result-success {
  display: flex;
  grid-template-columns: 55% 45%;
  gap: 3rem;
  height: 85vh;
  padding: 2rem 1rem;
}

.result-success-summary {
  --sb-track-color: #eeeeee;
  --sb-thumb-color: #b3b3b3;
  --sb-size: 10px;
  scrollbar-color: var(--sb-thumb-color) var(--sb-track-color);
}

.result-success-summary::-webkit-scrollbar {
  width: var(--sb-size);
}

.result-success-summary::-webkit-scrollbar-track {
  background: var(--sb-track-color);
  border-radius: 8px;
}

.result-success-summary::-webkit-scrollbar-thumb {
  background: var(--sb-thumb-color);
  border-radius: 8px;
}

.result-success-preview {
  min-width: 45%;
  width: 50%;
}

.result-success-preview img {
  width: fit-content;
}

@media (max-width: 768px) {
  .searcher-form {
    width: 85%;
  }

  .result-success {
    display: flex;
    flex-direction: column;
    gap: .8rem;
  }

  .result-success-summary {
    width: 100%;
  }

  .result-success-preview {
    width: 100%;
  }

  .auto-scroll {
    max-height: 35vh;
  }
}

.form-to-request-user-api-key {
  display: flex;
  flex-direction: column;
  gap: .5rem;
  width: 100%;
  max-width: 500px;
  margin: auto;
  margin-top: 1rem;
}

.form-to-request-user-api-key * {
  margin: 0 !important;
}</style>

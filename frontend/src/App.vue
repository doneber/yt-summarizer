<script setup>
import AppBarComponent from './components/AppBarComponent.vue'
import BannerComponent from './components/BannerComponent.vue'
import debounce from 'just-debounce-it'
import { ref } from 'vue'
let searchInput = ref('')
let loading = ref(false)
let videoId = ref('')

const search = debounce(async () => {
    loading.value = true
    // add delay to show loading
    await new Promise((resolve) => setTimeout(resolve, 300))
    videoId.value = getVideoId(searchInput.value)
    loading.value = false
}, 800, true)

const pasteFromClipboard = async () => {
  try {
    const text = await navigator.clipboard.readText()
    searchInput.value = text
    search()
  } catch (error) {
    console.error(error)
  }
}

const getVideoId = (urlVideo) => {
  try {
    const url = new URL(urlVideo)
    const searchParams = new URLSearchParams(url.search)
    return searchParams.get('v') || url.pathname.split('/').pop()
  } catch {
    console.log('Invalid link');
  }
  return ''
}

</script>

<template>
  <AppBarComponent />
  <main class="container">
    <BannerComponent />
    <form class="searcher-form" @submit.prevent="">
      <input v-model="searchInput" type="search" placeholder="Paste youtube video link here" @input="search()">
      <button class="past-clipboard" @click="pasteFromClipboard()">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M14.3498 2H9.64977C8.60977 2 7.75977 2.84 7.75977 3.88V4.82C7.75977 5.86 8.59977 6.7 9.63977 6.7H14.3498C15.3898 6.7 16.2298 5.86 16.2298 4.82V3.88C16.2398 2.84 15.3898 2 14.3498 2Z" fill="#000000"></path> <path d="M17.2391 4.81949C17.2391 6.40949 15.9391 7.70949 14.3491 7.70949H9.64906C8.05906 7.70949 6.75906 6.40949 6.75906 4.81949C6.75906 4.25949 6.15906 3.90949 5.65906 4.16949C4.24906 4.91949 3.28906 6.40949 3.28906 8.11949V17.5295C3.28906 19.9895 5.29906 21.9995 7.75906 21.9995H16.2391C18.6991 21.9995 20.7091 19.9895 20.7091 17.5295V8.11949C20.7091 6.40949 19.7491 4.91949 18.3391 4.16949C17.8391 3.90949 17.2391 4.25949 17.2391 4.81949ZM15.7491 16.9995C15.7491 17.4095 15.4091 17.7495 14.9991 17.7495H11.9991C11.5891 17.7495 11.2491 17.4095 11.2491 16.9995C11.2491 16.5895 11.5891 16.2495 11.9991 16.2495H13.1891L8.46906 11.5295C8.17906 11.2395 8.17906 10.7595 8.46906 10.4695C8.75906 10.1795 9.23906 10.1795 9.52906 10.4695L14.2491 15.1895V13.9995C14.2491 13.5895 14.5891 13.2495 14.9991 13.2495C15.4091 13.2495 15.7491 13.5895 15.7491 13.9995V16.9995Z" fill="#000000"></path> </g></svg>
      </button>
    </form>
    <div class="result">
      <div v-if="loading">
        <a href="#" aria-busy="true">Getting data, please wait…</a>
      </div>
      <div v-else-if="!searchInput">
        <p><i>Pst! Past some link</i></p>
      </div>
      <div v-else-if="videoId">
        <h3 class="result-title">Resultado:</h3>
        <div class="result-thumpnail">
          <img :src="`https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`" width="350" />
          <img :src="`https://img.shields.io/youtube/views/${videoId}?color=%23333&label=Views&style=social`" />
        </div>
        <p>Summary should go here</p>
      </div>
      <div v-else>
        <p><i>Invalid link</i></p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.result {
  display: flex;
  flex-direction: column;
}

.result-title {
  margin: 1rem 0;
  font-size: 1.3rem;
  font-weight: 400;
}

.past-clipboard {
  width: 55px;
  /* height: 45px; */
  padding: 0;
  background-color: transparent;
  /* border: none; */
  border-radius: 50%;
  border: 1px solid #41546277;
  padding: 8px;
}

body {
  height: 100vh;
}

main {
  display: flex;
  height: 80%;
  flex-direction: column;
  justify-content: center;
  width: min(100%, 720px);
}

.searcher-form {
  display: flex;
  align-items: center;
  gap: 5px;
  width: min(100%, 720px);
  margin: 0 auto;
}

.result-thumpnail {
  display: flex;
  flex-direction: column;
  gap: .5rem;
}

.result-thumpnail img {
  width: fit-content;
  /* margin: 1rem 0; */
}
</style>

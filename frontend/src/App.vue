<script setup>
import AppBarComponent from './components/AppBarComponent.vue'
import { ref } from 'vue'
let searchInput = ref('')
let loading = ref(false)
let videoId = ref('')

const search = async () => {
  loading.value = true

  // add delay to show loading
  await new Promise((resolve) => setTimeout(resolve, 300))
  videoId.value = getVideoId(searchInput.value)

  loading.value = false
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
    <form class="searcher-form" action="">
      <input v-model="searchInput" type="search" placeholder="Paste youtube video link here" @input="search()">
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
          <img :src="`https://img.shields.io/youtube/views/${videoId}?color=%23333&label=YouTube&style=social`" />
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
  /* display: flex; */
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

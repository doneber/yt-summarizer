<template>
  <header>
    <h1>YouTube Summarizer</h1>
    <p>Summarize a YouTube video in just a few seconds!</p>
  </header>
</template>

<style scoped>
header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: .8rem;
}

header h1 {
  font-size: 3rem;
  margin: 0;
  text-align: center;
  line-height: 1;
}

header p {
  text-align: center;
}

@media (max-width: 400px) {
  header h1 {
    font-size: 2.5rem;
  }
}
</style>
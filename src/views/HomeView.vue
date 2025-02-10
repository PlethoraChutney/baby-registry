<script setup>
import NavBar from "../components/NavBar.vue";
import { useMouseImage } from "../composables/mouseImage.js"

const { x, y } = useMouseImage("/images/dancing-baby.gif");
</script>

<template>
  <main>
    <NavBar/>
    <div class="content">
      <h1 class="title">It's freakin' baby time!!!</h1>
      <p>Seriously! It's time to have a baby!</p>
    </div>
  </main>
</template>

<style scoped>
main {
  grid-template-columns: 1fr;
  grid-template-rows: max-content 1fr;
  grid-template-areas:
    "nav"
    "content";
}

nav {
  grid-area: nav;
}

.content {
  grid-area: content;
  width: 50vw;
  height: 100%;
  margin: 0 auto;
}

.title {
  font-size: 4rem;
}
</style>
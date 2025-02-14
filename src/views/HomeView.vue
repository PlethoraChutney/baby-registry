<script setup>
import NavBar from "../components/NavBar.vue";
import { useMouseImage } from "../composables/mouseImage.js"
import { store } from "@/store";

const { x, y } = useMouseImage("/images/dancing-baby.gif");
</script>

<template>
  <main>
    <NavBar/>
    <div class="content">
      <h1 class="title" @click="store.notify('Test', 'Test body content, let us put a bit more this time. Lots and lots of content.', 3000)">It's freakin' baby time!!!</h1>
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
  user-select: none;
  -webkit-user-select: none;
}
</style>
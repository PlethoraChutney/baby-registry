<script setup>
import NavBar from "../components/NavBar.vue";
import { useMouseImage } from "../composables/mouseImage.js"
import { store } from "@/store";

useMouseImage("/images/dancing-baby.gif");
</script>

<template>
  <main>
    <NavBar/>

    <div class="content" v-if="store.titleReady">
      <h1 class="title">{{ store.homepageInfo.title}}</h1>
      <p class="subtitle">{{ store.homepageInfo.subtitle}}</p>

      <table class="itinerary">
        <tbody>
          <tr>
            <td>When?</td>
            <td>
              {{ store.homepageItinerary('date') }}
              at
              {{ store.homepageItinerary('time') }}
            </td>
          </tr>
          <tr>
            <td>Where?</td>
            <td>{{ store.homepageItinerary('location') }}</td>
          </tr>
        </tbody>
      </table>

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
  width: max-content;
  max-width: 50vw;
  height: 100%;
  margin: 0 auto;
}

.title {
  font-size: 4rem;
  user-select: none;
  -webkit-user-select: none;
}

.itinerary {
  width: 100%;
  font-size: var(--h2-size);
}
.itinerary td:first-of-type {
  text-align: right;
  padding-right: 0.5em;
}
.itinerary td:nth-of-type(2) {
  padding-left: 0.5em;
}


@media (width < 800px) {
  .content {
    max-width: 90vw;
  }

  .title {
    font-size: var(--h1-size);
  }
}
</style>
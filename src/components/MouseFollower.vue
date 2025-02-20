<script setup>

import { ref, computed } from "vue";
import { store } from "@/store";

const mouseFollower = computed(() => {
  const styleDict = {
    transform: `translate(${store.imageX}px, ${store.imageY}px)`
  }
  return styleDict;
})

</script>

<template>
    <img :src="store.imageUrl" alt="" class="mouse-follower" :style="mouseFollower" v-if="store.imageShow">
</template>

<style scoped>
.mouse-follower {
    pointer-events: none;
    position: absolute;
    width: 3em;
    top: 0;
    left: 0;
    transition: transform 1.2s linear(0, 0.544 5.5%, 0.947 11.5%, 1.213 18.1%, 1.298 21.7%, 1.352 25.5%, 1.372 28.2%, 1.379 31.1%, 1.374 34.2%, 1.357 37.6%, 1.307 43.7%, 1.121 61.8%, 1.074 67.8%, 1.04 73.7%, 1.007 84.7%, 1);
}
</style>
<script setup>

import { ref, computed } from "vue";
import { store } from "@/store";
import { onMounted } from "vue";
import { watch } from "vue";

const targetX = ref(0);
const targetY = ref(0);

let previous;
function step(timestep) {
    let elapsed;
    if (previous === undefined) {
        previous = timestep;
        elapsed = 0
    } else {
        elapsed = timestep - previous;
        previous = timestep;
    }
    const proportionMoved = 1 - Math.pow(0.75, elapsed / 100);
    const distX = store.imageX - targetX.value;
    const distY = store.imageY - targetY.value;
    targetX.value += (distX * proportionMoved);
    targetY.value += (distY * proportionMoved);

    if (store.imageShow) {
        requestAnimationFrame(step)
    }
}

function runAnimation() {
    targetX.value = store.imageX;
    targetY.value = store.imageY;
    requestAnimationFrame(step);
}

onMounted(runAnimation);
watch(() => store.imageShow, (newValue) => {
    if (newValue) {
        runAnimation();
    }
})

const mouseFollower = computed(() => {
  const styleDict = {
    transform: `translate(${targetX.value}px, ${targetY.value}px)`
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
}
</style>
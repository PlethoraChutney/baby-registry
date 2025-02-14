<script setup>
import MouseFollower from "@/components/MouseFollower.vue"
import Notification from "./components/Notification.vue";
import { RouterLink, RouterView } from 'vue-router';

</script>

<template>
  <RouterView />
  <MouseFollower/>
  <Notification/>
</template>

<style scoped>
</style>

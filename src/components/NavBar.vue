<script setup>
import { RouterLink } from 'vue-router'

</script>

<template>
<nav>
    <RouterLink :to="{name: 'home'}">Home</RouterLink>
    <RouterLink :to="{name: 'registry'}">Registry</RouterLink>
</nav>
</template>

<style scoped>

nav {
    font-size: var(--h2-size);
    font-weight: var(--h2-weight);
    display: flex;
    gap: 1em;
}

a {
    text-decoration: none;
}

</style>
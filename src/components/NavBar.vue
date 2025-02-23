<script setup>
import { RouterLink } from 'vue-router'

</script>

<template>
<nav>
    <RouterLink :to="{name: 'home'}">Home</RouterLink>
    <RouterLink :to="{name: 'registry'}">Registry</RouterLink>
    <RouterLink :to="{name: 'nameSuggestions'}">Suggest Names</RouterLink>
</nav>
</template>

<style scoped>

nav {
    font-size: var(--h3-size);
    font-weight: var(--h2-weight);
    display: flex;
    gap: 1em;
}

a {
    text-decoration: none;
}
a.router-link-active {
    border-bottom: 2px solid var(--blue);
    font-style: italic;
}

@media (width < 800px) {
    nav {
        font-size: var(--base-font-size);
        font-weight: var(--base-font-weight);
    }
}

</style>
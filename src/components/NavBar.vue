<script setup>
import { RouterLink } from 'vue-router'
const props = defineProps(["darkBg"])

</script>

<template>
<nav :class="{'dark-bg': props.darkBg}">
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

nav.dark-bg a {
    color: var(--flexoki-base-50)
}
nav.dark-bg a.router-link-active {
    border-color: var(--flexoki-base-50);
}

@media (width < 800px) {
    nav {
        font-size: var(--base-font-size);
        font-weight: var(--base-font-weight);
    }
}

</style>
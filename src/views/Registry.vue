<script setup>
import NavBar from "../components/NavBar.vue";
</script>

<template>
<main>

    <NavBar/>
    <div class="title-info">
        <h1 class="title">Here's some shit you can buy!</h1>
    </div>

</main>
</template>

<style scoped>
main {
    grid-template-columns: 1fr;
    grid-template-rows: max-content max-content 1fr;
    grid-template-areas:
        "nav"
        "title-info";
}

nav {
    grid-area: nav;
}

.title-info {
    grid-area: title-info;
}

.content {
    grid-area: content;
}

.title {
    text-align: center;
}
</style>
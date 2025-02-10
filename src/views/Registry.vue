<script setup>
import NavBar from "../components/NavBar.vue";
import ItemCard from "@/components/ItemCard.vue";
import items from "@/assets/items-info.json";
</script>

<template>
<main>

    <NavBar/>
    <div class="title-info">
        <h1 class="title">Here's some shit you can buy!</h1>
    </div>
    <div class="content">
        <div class="card-container">
            <ItemCard
            v-for="item, uuid of items"
            :key="uuid"
            :uuid
            :item
            />
        </div>
    </div>

</main>
</template>

<style scoped>
main {
    grid-template-columns: 1fr;
    grid-template-rows: max-content max-content 1fr;
    grid-template-areas:
        "nav"
        "title-info"
        "content";
}

nav {
    grid-area: nav;
}

.title-info {
    grid-area: title-info;
}
.title {
    text-align: center;
}

.content {
    grid-area: content;
}
/* .card-container {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2em;
} */
.card-container {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(auto-fit, var(--card-width));
    gap: 2em;
    padding: 2em;
    justify-content: center;
}

</style>
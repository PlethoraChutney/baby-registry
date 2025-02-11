<script setup>
import NavBar from "../components/NavBar.vue";
import ItemCard from "@/components/ItemCard.vue";
import items from "@/assets/items-info.json";
</script>

<template>
<main>

    <NavBar/>
    <h1 class="title">Here's some shit you can buy!</h1>
    <div class="info">
        <p>
            Remember! Gifts are <em>optional</em>! But here are some things we'd like to have
            for the baby. The pictures are links to where you can buy them new, but we encourage
            you to look around and try to find them used on Craigslist or Facebook Marketplace or
            whatever! If you're looking used, we've made some notes on things to look out
            for in the dropdown!
        </p>
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
    grid-template-columns: 1fr 1fr;
    grid-template-rows: max-content max-content 1fr;
    grid-template-areas:
        "nav nav"
        "title info"
        "content content";
}

nav {
    grid-area: nav;
}

.title {
    grid-area: title;
    text-align: right;
    padding-right: 0.5rem;
}

.info {
    grid-area: info;
    padding-left: 0.5rem;
}

.info p {
    max-width: 40em;
}

.content {
    grid-area: content;
}
.card-container {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(auto-fit, var(--card-width));
    gap: 2em;
    padding: 2em;
    justify-content: center;
}

</style>
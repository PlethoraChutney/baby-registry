<script setup>
import NavBar from "../components/NavBar.vue";
import ItemCard from "@/components/ItemCard.vue";
import { ref, useTemplateRef } from "vue";
import { onMounted } from "vue";
import { store } from "@/store";
import { onBeforeMount } from "vue";

onBeforeMount(() => store.updateItems());

const purchasedItems = ref({});
function purchased(uuid) {
    const quant = store.items[uuid].purchased;
    return quant ?? 0;
}

// don't buy stuff dialog
const dontBuyStuff = useTemplateRef("dont-buy-stuff");
onMounted(() => {
    if (!store.buyingAcknowledged) {
        dontBuyStuff.value.showModal();
    }
})
</script>

<template>
<dialog ref="dont-buy-stuff" class="dont-buy-stuff">
    <img src="/images/do-not-buy.png" alt="">
    <div>
        <h1>Stop!</h1>
        <p>
            Buying gifts is <em>optional</em>. We invited you to our baby shower
            because we want you to come have a good time,
            <em>not</em> because we want things. We made a registry
            in case you <em>want</em> to buy stuff!
        </p>
        <p>
            By proceeding to look at the registry, you acknowledge that
            gifts are optional, and that if you've already given us baby
            stuff that counts as a gift.
        </p>
        <div class="button-holder">
            <button @click="() => {dontBuyStuff.close(); store.buyingAcknowledged = true;}">
                OK, you freaks!
            </button>
            <a href="https://www.google.com/search?&q=cute+cats&udm=2">
                <button>
                    No, I kinda feel like I have to get you stuff.
                </button>
            </a>
        </div>
    </div>
</dialog>
<main>

    <NavBar/>
    <div class="info">
        <div>
            <h1 class="title">Here's some shit you can buy!</h1>
        </div>
        <div>
            <p>
                Remember! Gifts are <em>optional</em>! But here are some things we'd like to have
                for the baby. The pictures are links to where you can buy them new, but we encourage
                you to look around and try to find them used on Craigslist or Facebook Marketplace or
                whatever! If you're looking used, we've made some notes on things to look out
                for in the dropdown!
            </p>
        </div>
    </div>
    <div class="content">
        <div class="card-container">
            <ItemCard
            v-for="item, uuid of store.items"
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
    grid-template-columns: 100%;
    grid-template-rows: max-content max-content 1fr;
    grid-template-areas:
        "nav"
        "info"
        "content";
}

nav {
    grid-area: nav;
}


.info {
    grid-area: info;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 1em;
    width: 100%;
}
.info div {
    width: 50%;
}
.info p {
    max-width: 40em;
    margin-right: auto;
}

.info h1 {
    text-align: right;
    margin-left: auto;
}

@media (width < 800px) {
  .info {
    display: block;
  }
  .info div {
    width: 100%;
  }
  .info h1 {
    text-align: left;
    max-width: 100%;
  }
  .info p {
    max-width: 100%;
  }
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

.button-holder a {
    width: 100%;
}

.dont-buy-stuff[open] {
    display: grid;
    grid-template-columns: 30% 1fr;
    grid-template-rows: 100%;
    gap: 1em;
}
.dont-buy-stuff img {
    width: 100%;
    max-height: 100%;
    margin-top: auto;
    margin-bottom: -1em;
}
.dont-buy-stuff > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
}



@media (width < 800px) {
  .dont-buy-stuff[open] {
    display: block;
  }
  .dont-buy-stuff img {
    visibility: hidden;
    display: none;
  }
}
</style>
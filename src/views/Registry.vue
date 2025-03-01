<script setup>
import NavBar from "../components/NavBar.vue";
import ItemCard from "@/components/ItemCard.vue";
import { ref, useTemplateRef } from "vue";
import { onMounted } from "vue";
import { store } from "@/store";
import { onBeforeMount } from "vue";

onBeforeMount(() => store.updateItems());

const registryCopy = ref({});
onBeforeMount(updateRegistryCopy);
async function updateRegistryCopy() {
  return fetch(
    "/api/get-copy/registry",
    {
      credentials: "include"
    }
  )
  .then(response => response.json())
  .then(data => registryCopy.value = data)
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
        <h1>{{ registryCopy.dialogTitle }}</h1>
        <p
        v-for="(item, idx) in registryCopy.dialogBody"
        :key="idx"
        >
            {{ item }}
        </p>
        <div class="button-holder">
            <button @click="() => {dontBuyStuff.close(); store.buyingAcknowledged = true;}">
                {{ registryCopy.dialogAccept }}
            </button>
            <a href="https://www.google.com/search?&q=cute+cats&udm=2">
                <button>
                    {{ registryCopy.dialogReject }}
                </button>
            </a>
        </div>
    </div>
</dialog>
<main>

    <NavBar/>
    <div class="info">
        <div>
            <h1 class="title">{{ registryCopy.title }}</h1>
        </div>
        <div>
            <p>
                {{ registryCopy.body }}
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

button {
    padding: 0.25em;
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
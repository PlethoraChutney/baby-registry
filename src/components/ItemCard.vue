<script setup>

const props = defineProps({
    "uuid": {type: String, required: true},
    "item": {type: Object, required: true}
})

</script>

<template>
<div class="card">
    <div class="img-container">
        <h3>{{ props.item.label }}</h3>
        <img :src="`/images/item-images/${ props.uuid }.png`" alt="">
    </div>
    <p class="description">{{ props.item.description }}</p>
    <button>
        I got it!
    </button>
</div>
</template>

<style scoped>
.card {
    width: var(--card-width);
    height: calc(var(--card-width) * 1.618);

    border: 6px solid var(--color-ui);
    padding: 1em;

    display: grid;
    grid-template-rows: max-content 1fr;
    grid-template-columns: 1fr;

    box-shadow: 5px 10px 20px 1px var(--color-ui);
}

.purchased {
    filter: saturate(0);
    opacity: 0.6;
}

.img-container {
    position: relative;
}
.img-container :is(h2, h3) {
    position: absolute;
    margin: 0;
    padding: 0.125em 0.25em;
    width: 100%;
    background-color: color-mix(in srgb, var(--color-bg) 50%, transparent);
    backdrop-filter: blur(3px);
}
.img-container img {
    width: 100%;
    aspect-ratio: 1;
}

button {
    border: none;
    background-color: var(--blue);
    color: var(--color-bg);
    font-family: inherit;
    font-size: inherit;
    padding: 0.25em 0;
    cursor: pointer;
    width: 100%;
}
button:hover {
    background-color: var(--blue-2);
}
button:active {
    transform-origin: center;
    transform: scale(0.95);
}
</style>
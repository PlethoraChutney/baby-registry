<script setup>
import { computed } from 'vue';

const props = defineProps({
    "uuid": {type: String, required: true},
    "item": {type: Object, required: true},
    "purchased": {type: Number, required: true}
})

const needMore = computed(() => {
    if (String(Number(props.item.quantity)) !== props.item.quantity) {
        return props.item.quantity;
    }
    return `${props.item.quantity - props.purchased} more`;
});

const numberGuess = computed(() => {
    if (props.item.quantity === "?") {
        return null
    }
    if (String(Number(props.item.quantity)) === props.item.quantity) {
        return Number(props.item.quantity)
    }
    const firstPart = props.item.quantity.split(" ")[0];
    if (String(Number(firstPart)) === firstPart) {
        return Number(firstPart)
    }
    return null
})

const gotWhat = computed(() => {
    if (numberGuess.value === 1) {
        return "it"
    } else {
        return "one"
    }
})

const percentPurchased = computed(() => {
    let propPurchased;
    if (numberGuess.value === null) {
        propPurchased = 0;
    } else {
        propPurchased = props.purchased / numberGuess.value;
    }

    return propPurchased * 100;
})

const buttonBackground = computed(() => {
    return `linear-gradient(to right, var(--yellow) ${percentPurchased.value}%, var(--blue) ${percentPurchased.value}%)`
})

</script>

<template>
<div class="card">
    <div class="img-container">
        <h3>{{ props.item.label }}</h3>
        <a
        :href="item.link"
        target="_blank"
        rel="noopener noreferrer"
        >
            <img :src="`/images/item-images/${ props.uuid }.png`" alt="">
            <p>Here it is new!</p>
        </a>
    </div>

    <p class="description">{{ props.item.description }}</p>

    <details v-if="item.specs">
        <summary class="no-select">Info for getting it used</summary>
        <p>{{ item.specs }}</p>
    </details>
    <div v-else></div>

    <button class="no-select" :style="{background: buttonBackground}">
        Need {{ needMore }}. Click if you got {{ gotWhat }}!
    </button>
</div>
</template>

<style scoped>
.card {
    --color-blur-bg: color-mix(in srgb, var(--color-bg) 15%, transparent);

    width: var(--card-width);
    height: calc(var(--card-width) * 1.618);

    font-size: 0.9rem;

    border: 6px solid var(--color-txt-2);
    padding: 1em;

    display: grid;
    grid-template-rows: max-content 1fr 1.5lh 1.5lh;
    grid-template-columns: 1fr;
    gap: 0.5rem;

    box-shadow: 5px 10px 20px 2px color-mix(in srgb, var(--color-txt-2) 75%, transparent);
}

@media (prefers-color-scheme: dark) {
    .card {
        box-shadow: unset;
    }
}

.purchased {
    filter: saturate(0);
    opacity: 0.6;
}

.img-container {
    position: relative;
}

.img-container img {
    width: 100%;
    aspect-ratio: 1;
}
.img-container a h3 {
    color: var(--color-txt);
    text-decoration: none;
}

.img-container a p {
    bottom: 0;
}
.img-container :is(h3, p) {
    position: absolute;
    margin: 0;
    width: 100%;
    padding: 0.125em 0.25em;
    background-color: var(--color-blur-bg);
    backdrop-filter: blur(6px);
}

.description {
    font-style: italic;
}

details {
    position: relative;
    height: 100%;
    top: 0;
    z-index: 2;
}
details p {
    background-color: var(--color-bg);
    padding: 0.5em 1em;
    border: 1px solid var(--color-txt-2);
    border-color: var(--color-ui) var(--color-txt-2) var(--color-txt-2) var(--color-txt-2);
}
summary {
    cursor: pointer;
    border: 1px solid var(--color-txt-2);
    height: 100%;
    width: 100%;
    padding: 0.25lh;
}

details[open] summary {
    border-width: 1px 1px 0 1px;
}

button {
    border: none;
    color: var(--color-bg);
    font-family: inherit;
    font-size: inherit;
    cursor: pointer;
    width: 100%;
    position: relative;
}
button:hover {
    background-color: var(--blue-2);
}
button:active {
    transform-origin: center;
    transform: scale(0.95);
}
</style>
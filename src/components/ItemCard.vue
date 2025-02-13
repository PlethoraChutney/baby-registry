<script setup>
import { ref } from 'vue';
import { computed } from 'vue';
import { PhCheck, PhX } from "@phosphor-icons/vue";

const props = defineProps({
    "uuid": {type: String, required: true},
    "item": {type: Object, required: true},
    "purchased": {type: Number, required: true}
})

const emit = defineEmits(["bought"]);
const nonstandardQuantity = String(Number(props.item.quantity)) !== String(props.item.quantity);

// figure out how many we want and how many we have

const purchased = ref(props.purchased);

const wantMoreString = computed(() => {
    if (nonstandardQuantity) {
        return props.item.quantity;
    }
    return `${wantedRemainingNumber.value} more`;
});

const wantedTotalNumber = computed(() => {
    if (props.item.quantity === "?") {
        return null
    }
    if (!nonstandardQuantity) {
        return Number(props.item.quantity)
    }
    const firstPart = props.item.quantity.split(" ")[0];
    if (String(Number(firstPart)) === firstPart) {
        return Number(firstPart)
    }
    return null
})

const wantedRemainingNumber = computed(() => {
    if (wantedTotalNumber.value === null) {
        return null;
    }
    return wantedTotalNumber.value - purchased.value;
})

const wantMoreSuffix = computed(() => {
    if (!nonstandardQuantity && wantedRemainingNumber.value === 1) {
        return "it"
    } else {
        return "one"
    }
})

// button fill in
const percentPurchased = computed(() => {
    let propPurchased;
    if (wantedTotalNumber.value === null) {
        propPurchased = 0;
    } else {
        propPurchased = purchased.value / wantedTotalNumber.value;
    }

    return propPurchased * 100;
})

const buttonBackground = computed(() => {
    return `linear-gradient(to right, var(--yellow) ${percentPurchased.value}%, var(--blue) ${percentPurchased.value}%)`
})

const itemsPurchased = computed(() => {
    return purchased.value === wantedTotalNumber.value
})

// purchase single
const purchasingSingle = ref(false);
function purchaseButtonClick() {
    if (!wantedTotalNumber.value) {
        return
    }

    if (wantedRemainingNumber.value === 1) {
        purchasingSingle.value = true;
    } else {
        purchaseMultiple();
    }
}

function completeSinglePurchase() {
    purchased.value += 1;
    emit("bought");
    purchasingSingle.value = false;
}
function abortSinglePurchase() {
    purchasingSingle.value = false
}

// purchase multiple
const purchasingMultiple = ref(false);
const purchaseAmount = ref("1");

function purchaseMultiple() {
    purchaseAmount.value = 1;
    purchasingMultiple.value = true;
}

function validatePurchaseAmount() {
    if (String(Number(purchaseAmount.value)) != purchaseAmount.value || purchaseAmount.value < 1) {
        purchaseAmount.value = "1";
    }

    if (purchaseAmount.value > wantedRemainingNumber.value) {
        purchaseAmount.value = wantedRemainingNumber.value;
    }
    
}

function completeMultiPurchase() {
    purchased.value += purchaseAmount.value;
    emit("bought");
    purchasingMultiple.value = false;
}
function abortMultiPurchase() {
    purchasingMultiple.value = false;
}

</script>

<template>
<div class="card" :class="{'purchased': itemsPurchased}">
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

    <details v-if="item.specs && !itemsPurchased">
        <summary class="no-select">Info for getting it used</summary>
        <p>{{ item.specs }}</p>
    </details>
    <div v-else></div>

    <button
    class="no-select"
    :style="{background: buttonBackground}"
    @click="purchaseButtonClick"
    v-show="!itemsPurchased && !purchasingMultiple && !purchasingSingle"
    >
        We'd love {{ wantMoreString }}. Click if you got {{ wantMoreSuffix }}!
    </button>
    <div
    v-if="!itemsPurchased && purchasingSingle"
    class="purchase-buttons single"
    >
        <button @click="completeSinglePurchase" class="green hover">Confirm!</button>
        <button @click="abortSinglePurchase" class="red hover">Oops! Misclick!</button>
    </div>
    <div
    v-if="!itemsPurchased && purchasingMultiple"
    class="purchase-buttons multiple"
    >
        <input
        type="number"
        v-model="purchaseAmount"
        min="1"
        :max="wantedRemainingNumber ?? 5"
        @change="validatePurchaseAmount"
        >
        <button @click="completeMultiPurchase" class="green hover"><PhCheck/></button>
        <button @click="abortMultiPurchase" class="red hover"><PhX/></button>
    </div>
    <p v-if="itemsPurchased" class="button-replacement">
        That's plenty! Thank you so much!
    </p>
</div>
</template>

<style scoped>
.card {
    --color-blur-bg: color-mix(in srgb, var(--color-bg) 50%, transparent);

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

    transition: opacity 500ms ease-out;
}

@media (prefers-color-scheme: dark) {
    .card {
        box-shadow: unset;
    }
}

.purchased {
    filter: saturate(0);
    opacity: 0.3;

    transition: opacity 500ms ease-out;
}

.img-container {
    position: relative;
}

.img-container img {
    width: 100%;
    aspect-ratio: 1;
}
.img-container h3 {
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
    backdrop-filter: blur(2px);
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

.button-replacement {
    height: 100%;
    width: 100%;
    text-align: center;
    align-content: center;
    user-select: none;
    -webkit-user-select: none;
}

button {
    color: var(--color-bg);
    width: 100%;
    position: relative;
}
button p {
    pointer-events: none;
}

.purchase-buttons {
    width: 100%;
    display: flex;
    gap: 0.125em;
}
input {
    flex-grow: 1;
    margin: 0 0.5em;
}
.purchase-buttons.multiple button {
    width: max-content;
    aspect-ratio: 1;
}
.purchase-buttons.single button {
    flex-grow: 1;
}
</style>
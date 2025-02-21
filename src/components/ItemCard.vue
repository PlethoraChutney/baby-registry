<script setup>
import { ref } from 'vue';
import { computed, useTemplateRef } from 'vue';
import { PhCheck, PhX } from "@phosphor-icons/vue";
import { store } from '@/store';
import { nextTick } from 'vue';

const props = defineProps({
    "uuid": {type: String, required: true},
    "item": {type: Object, required: true},
})

const emit = defineEmits(["bought"]);
const nonstandardQuantity = String(Number(props.item.quantity)) !== String(props.item.quantity);

async function purchaseItems(uuid, quant) {
    const body = JSON.stringify({"uuid": uuid, "num_purchased": quant})
    return fetch(
        "/api/purchase_item/",
        {
            "method": "POST",
            "credentials": "include",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": body
        }
    )
    .then(response => response.json())
    .then(data => {
        if (data["new_purchased"]) {
            store.items[props.uuid].purchased = data["new_purchased"]
        }
    })
}

// figure out how many we want and how many we have

const wantMoreString = computed(() => {
    if (nonstandardQuantity) {
        return props.item.quantity;
    }
    return `${wantedRemainingNumber.value} more`;
});

const wantedRemainingNumber = computed(() => {
    if (props.item.numeric_quant === null) {
        return null;
    }
    return props.item.numeric_quant - props.item.purchased;
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
    if (props.item.numeric_quant === null) {
        propPurchased = 0;
    } else {
        propPurchased = props.item.purchased / props.item.numeric_quant;
    }

    return propPurchased * 100;
})

const buttonBackground = computed(() => {
    return `linear-gradient(to right, var(--yellow) ${percentPurchased.value}%, var(--blue) ${percentPurchased.value}%)`
})

const itemsPurchased = computed(() => {
    return props.item.purchased === props.item.numeric_quant
})

// purchase single
const purchasingSingle = ref(false);
async function purchaseButtonClick() {
    const oldValue = props.item.purchased;
    store.updatePurchased()
    .then(response => {
        if (props.item.purchased !== oldValue) {
            if (wantedRemainingNumber.value === 0) {
                store.notify(
                    "Someone bought this!",
                    "While you were looking, someone bought all of this item that we want! Thank you though!",
                    5000
                )
                return
            } else {
                store.notify(
                    "Someone bought some of these!",
                    `While you were looking, someone bought a few of this item. We now only want ${wantedRemainingNumber.value} more! Thank you!`,
                    5000
                )
            }
        }
        if (!props.item.numeric_quant && props.wantedRemainingNumber > 0) {
            return
        }

        if (wantedRemainingNumber.value === 1) {
            purchasingSingle.value = true;
        } else {
            purchaseMultiple();
        }
    })
}

function completeSinglePurchase() {
    purchaseItems(props.uuid, 1)
    emit("bought");
    purchasingSingle.value = false;
}
function abortSinglePurchase() {
    purchasingSingle.value = false;
}

// purchase multiple
const purchasingMultiple = ref(false);
const purchaseAmount = ref("1");
const purchaseAmountInput = useTemplateRef("purchase-amount-input")

function purchaseMultiple() {
    purchaseAmount.value = 1;
    purchasingMultiple.value = true;
    nextTick(() => {
        purchaseAmountInput.value.select();
    })
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
    purchaseItems(props.uuid, purchaseAmount.value)
    emit("bought");
    purchasingMultiple.value = false;
}
function abortMultiPurchase() {
    purchasingMultiple.value = false;
}

// handle if someone purchased items while a user
// is looking at the site

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
        ref="purchase-amount-input"
        min="1"
        :max="wantedRemainingNumber ?? 5"
        @change="validatePurchaseAmount"
        @keyup.enter="completeMultiPurchase"
        @keyup.esc="abortMultiPurchase"
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
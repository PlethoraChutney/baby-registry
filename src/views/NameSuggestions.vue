<script setup>
import NavBar from '@/components/NavBar.vue';
import Blob from '@/components/Blob.vue';

import { store } from '@/store';
import { useTemplateRef } from 'vue';
import { onBeforeMount } from 'vue';
import { computed } from 'vue';


import { ref } from 'vue';

const nameCopy = ref({});
onBeforeMount(updateNameCopy);
async function updateNameCopy() {
  return fetch(
    "/api/get-copy/name-suggestions",
    {
      credentials: "include"
    }
  )
  .then(response => response.json())
  .then(data => nameCopy.value = data)
}

function numToString(n) {
    if (n > 20) {
        return n.toString();
    }
    return [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"
    ][n]
}

// load suggestions
const suggestionLimit = ref(5);
const nameSuggestions = ref([]);
async function getNameSuggestions() {
    return fetch(
        "/api/name/",
        {
            credentials: "include"
        }
    )
    .then(response => response.json())
    .then(suggestionData => {
        console.log(suggestionData);
        suggestionLimit.value = suggestionData["limit"]
        nameSuggestions.value = suggestionData["current_suggestions"];
        return suggestionData;
    })
}
onBeforeMount(getNameSuggestions)

// suggest a name
const nameRegex = new RegExp("^[A-Za-z]+$")
const currentNameSuggestion = ref("");
const nameValid = computed(() => {
    return nameRegex.test(currentNameSuggestion.value) && !nameSuggestions.value.includes(currentNameSuggestion.value);
})
const nameInput = useTemplateRef("name-input");

const nameMessage = computed(() => {
    const name = currentNameSuggestion.value;
    if (name.length === 0) {
        return "Enter a name"
    }
    if (!nameRegex.test(name)) {
        return "No numbers or punctuation"
    }
    if (nameSuggestions.value.includes(currentNameSuggestion.value)) {
        return `You've already suggested ${currentNameSuggestion.value}`
    }
    
    return "Submit suggestion!"
})
async function submitName() {
    if (!nameValid.value) {
        return
    }
    return fetch(
        "/api/name/",
        {
            method: "POST",
            credentials: "include",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify({name: currentNameSuggestion.value})
        }
    )
    .then(async response => {
        if (response.status === 400) {
            const err = await response.json();
            store.notify("Submission error", err.error, 3000);
            return response
        } else if (response.status === 200) {
            getNameSuggestions();
            currentNameSuggestion.value = "";
            nameInput.value.focus();
        }
    })
}


</script>

<template>

<Blob
    v-for="i in Array(15).fill().map((x,i)=>i)"
    :key="i"
    :idx="i % 5"
    :offset="[30, 30]"
/>
<main>
    <NavBar/>

    <div class="info">
        <div>
            <h1 class="title">{{ nameCopy.title }}</h1>
        </div>
        <div>
            <p
            v-for="(item, idx) of nameCopy.body"
            :key="idx"
            >
                {{ item }}
            </p>
        </div>
    </div>

    <div class="name-input" v-if="nameSuggestions.length < suggestionLimit">
        <input id="name-input" v-model="currentNameSuggestion" type="text" @keyup.enter="submitName" ref="name-input">
        <p v-if="!nameValid">{{ nameMessage }}</p>
        <button @click="submitName" v-else>{{ nameMessage }}</button>
    </div>

    <div class="current-names" v-if="nameSuggestions.length > 0">
        <p>Your submitted name suggestions:</p>
        <ul>
            <li
            v-for="name of nameSuggestions"
            :key="name"
            >{{ name }}</li>
        </ul>
    </div>
    <div class="current-names" v-else>
        <p>You haven't suggested any names yet!</p>
    </div>

</main>
</template>

<style scoped>
main {
    grid-template-rows: max-content max-content 1fr;
    grid-template-columns: 1fr 1fr;
    grid-template-areas: 
    "nav nav"
    "info info"
    "name-input current-names";
    gap: 1rem;
}

.info {
    margin-bottom: 5rem;
}

li {
    list-style-type: none;
    position: relative;
    padding: 0.25em;
}
li::before {
    content: url("@/assets/marker.svg");
    display: inline-block;
    position: absolute;
    left: -1.25em;
    top: 0.375em;
    height: 1em;
    aspect-ratio: 1;
}

.name-input {
    grid-area: name-input;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.name-input :is(p, button, input) {
    text-align: center;
    width: 20rem;
    height: 1.5lh;
}
.name-input input {
    z-index: 2;
}
.name-input p {
    background-color: var(--color-bg-2);
    display: flex;
    justify-content: center;
    align-items: center;
}

.current-names {
    grid-area: current-names;
    display: grid;
    grid-template-rows: max-content 1fr;
    grid-template-columns: 100%;
}


@media (width < 800px) {
  main {
    grid-template-rows: repeat(4, max-content);
    grid-template-columns: 100%;
    grid-template-areas: 
    "nav"
    "info"
    "name-input"
    "current-names";
  }

  .info {
    margin: 0;
  }
}
</style>
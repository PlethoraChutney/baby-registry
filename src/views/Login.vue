<script setup>
import { ref } from 'vue';
import { useMouseImage } from '@/composables/mouseImage';
import { store } from "@/store";
import router from '@/router';
import { computed } from 'vue';

useMouseImage("/images/dancing-baby.gif");

const firstName = ref("");
const lastName = ref("");
const userId = computed(() => {
    return `${firstName.value.toLowerCase()} ${lastName.value.toLowerCase()}`
})
const password = ref("");

async function loginUser() {
    if (userId.value.length === 0 || password.value.length === 0) {
        return
    }

    fetch(
        "/api/login/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "user_id": userId.value,
                "password": password.value
            })
        }
    )
    .then(response => response.json())
    .then(response => {
        if (response.success) {
            store.updateHomepageInfo();
            store.userId = response.user_id;
            store.loginAuthenticated();
            router.push({name: "home"});
        } else {
            store.notify(
                "Login Error",
                response.error
            )
        }
    })
}
</script>

<template>
<main>
    <div>
        <h1>Welcome to the baby shower!</h1>
        <div class="login">
            <label for="firstname">
                What's your first name?
                <input id="firstname" type="text" v-model="firstName" @keyup.enter="loginUser">
            </label>
            <label for="lastname">
                What's your last name?
                <input id="lastname" type="text" v-model="lastName" @keyup.enter="loginUser">
            </label>
            <label for="password">
                What's the password?
                <input id="password" type="text" v-model="password" @keyup.enter="loginUser">
            </label>
            <button
            v-if="firstName.length > 0 && lastName.length > 0 && password.length > 0"
            @click="loginUser"
            >
                Lemme in!
            </button>
        </div>
    </div>
</main>
</template>

<style scoped>

main {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    justify-content: center;
    justify-items: center;
    align-items: center;
}

h1 {
    margin-bottom: 1em;
}

.login {
    height: max-content;
    min-height: 10rem;
    width: max-content;
    min-width: 20rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 1em;
}

label {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: 1em;
    padding: 0 0.25em;
}

input {
    padding: 0.125em;
}

button {
    width: 100%;
    padding: 0.25em;
}

</style>
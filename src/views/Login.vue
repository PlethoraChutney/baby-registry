<script setup>
import { ref } from 'vue';
import { useMouseImage } from '@/composables/mouseImage';
import { store } from "@/store";
import router from '@/router';
import { computed, useTemplateRef } from 'vue';
import Blob from '@/components/Blob.vue';

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

// peekaboos
const firstnameInputActive = ref(false);
const firstnamePeekabooX = computed(() => {
    if (firstName.value.length > 0 && !firstnameInputActive.value) {
        return "0px"
    } else {
        return "-100%"
    }
})
const firstnamePeekaboo = () => {
    return {
        "transform": `translate(${firstnamePeekabooX.value}, -25vh)`
    }
}

const lastnameInputActive = ref(false);
const lastnamePeekabooX = computed(() => {
    if (lastName.value.length > 0 && !lastnameInputActive.value) {
        return "0px"
    } else {
        return "100%"
    }
})
const lastnamePeekaboo = () => {
    return {
        "transform": `translate(${lastnamePeekabooX.value}, 0px)`
    }
}

const passwordInputActive = ref(false);
const passwordPeekabooX = computed(() => {
    if (password.value.length > 0 && !passwordInputActive.value) {
        return "0px"
    } else {
        return "-100%"
    }
})
const passwordPeekaboo = () => {
    return {
        "transform": `translate(${passwordPeekabooX.value}, 25vh)`
    }
}
</script>

<template>
<main>
    <Blob
    v-for="i in Array(15).fill().map((x,i)=>i)"
    :key="i"
    :idx="i % 5"
    />
    <img src="/images/peekaboo-1.png" alt="" class="peekaboo left" :style="firstnamePeekaboo()">
    <img src="/images/peekaboo-3.png" alt="" class="peekaboo right" :style="lastnamePeekaboo()">
    <img src="/images/peekaboo-2.png" alt="" class="peekaboo left" :style="passwordPeekaboo()">
    <div>
        <h1>Welcome to the baby shower!</h1>
        <div class="login">
            <label for="firstname">
                What's your first name?

                <input
                id="firstname"
                type="text"
                v-model="firstName"
                @keyup.enter="loginUser"
                @focus="firstnameInputActive = true"
                @blur="firstnameInputActive = false"
                >
            </label>
            <label for="lastname">
                What's your last name?

                <input
                id="lastname"
                type="text"
                v-model="lastName"
                @keyup.enter="loginUser"
                ref="lastnameInput"
                @focus="lastnameInputActive = true"
                @blur="lastnameInputActive = false"
                >
            </label>
            <label for="password">
                What's the password?

                <input
                id="password"
                type="text"
                v-model="password"
                @keyup.enter="loginUser"
                ref="passwordInput"
                @focus="passwordInputActive = true"
                @blur="passwordInputActive = false"
                >
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

.peekaboo {
    position: absolute;
    height: 50vh;
    transition: transform 500ms cubic-bezier(0.16, 1, 0.3, 1);
}

.left {
    left: 0;
}

.right {
    right: 0;
}

@media (width < 800px) {
    .peekaboo {
        display: none;
        visibility: hidden;
    }

    label {
        display: flex;
        flex-direction: column;
        padding-bottom: 1em;
        gap: 0;
    }
}

</style>
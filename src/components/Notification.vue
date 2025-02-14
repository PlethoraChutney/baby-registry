<script setup>
import { store } from '@/store';
</script>

<template>
    <div
    class="notification"
    :class="{show: store.showNotification}"
    >
        <h3>{{ store.notificationTitle }}</h3>
        <p>{{ store.notificationBody }}</p>
    </div>
</template>

<style scoped>
.notification {
    position: absolute;
    right: 2rem;
    bottom: 1rem;
    max-width: 20rem;
    padding: 1rem;
    height: max-content;
    background-color: var(--yellow);
    border: 6px solid var(--color-ui);
    transform: translate(22rem, 0px);
    transition: transform 200ms linear;
}

.show {
    transform: translate(0px, 0px);
    transition: transform 400ms linear(0, 0.998 44.6%, 0.885 52%, 0.85 58.6%, 1 77.4%, 0.976 84.6%, 1);
}
</style>
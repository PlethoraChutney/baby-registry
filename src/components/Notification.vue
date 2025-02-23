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
    min-width: 15rem;
    width: max-content;
    max-width: 20rem;
    min-height: 5lh;
    height: max-content;

    display: grid;
    grid-template-rows: max-content 1fr;
    align-items: center;

    padding: 1rem;
    background-color: var(--yellow);
    border: 6px solid var(--color-ui);
    transform: translate(22rem, 0px);
    transition: transform 200ms linear;
    z-index: 3;
}

.show {
    transform: translate(0px, 0px);
    transition: transform 400ms linear(0, 0.998 44.6%, 0.885 52%, 0.85 58.6%, 1 77.4%, 0.976 84.6%, 1);
}

/* TODO: mobile notifications not working */
@media (width < 800px) {
  .notification {
    left: 10vw;
    right: 10vw;
    min-width: 80vw;
    max-width: 80vw;
    transform: translate(100vw, 0px);
  }
}
</style>
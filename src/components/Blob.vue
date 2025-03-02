<script setup>

const props = defineProps({
    idx: {type: Number, required: false},
    offset: {type: Array, required: false},
    rotation: {type: Number, required: false},
    width: {type: Number, required: false},
    opacity: {type: Number, required: false}
});

const numBlobs = 5;
const blobIdx = props.idx ?? Math.floor(Math.random() * numBlobs);
const blobSrc = `/images/blobs/blob-${blobIdx}.svg`;

const blobRotation = props.rotation ?? Math.random() * 360;
const blobTranslationX = props.offset ? props.offset[0] : 100 * (Math.random() - 0.5);
const blobTranslationY = props.offset ? props.offset[1] : 100 * (Math.random() - 0.5);

const blobWidth = props.width ?? (Math.random() + 0.1) * 30;

const blobOpacity = props.opacity ?? Math.min(Math.random() + 0.3, 0.8);

const styleDict = {
    transform: `translate(${blobTranslationX}vw, ${blobTranslationY}vh) rotate(${blobRotation}deg)`,
    width: `${blobWidth}vw`,
    opacity: blobOpacity
};

</script>

<template>
<img :src="blobSrc" :style="styleDict" alt="">
</template>

<style scoped>
img {
    position: absolute;
    z-index: -1;
}
</style>
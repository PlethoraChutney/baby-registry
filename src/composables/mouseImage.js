import {ref, onMounted, onUnmounted} from "vue"
import { store } from "@/store";

export function useMouseImage(imageUrl) {
    const x = ref(null);
    const y = ref(null);

    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    if (isMobile) {
        return {x, y}
    }

    function update(event) {
        x.value = event.pageX;
        store.setImageX(event.pageX);

        y.value = event.pageY
        store.setImageY(event.pageY);
    }

    onMounted(() => {
        store.showImage(imageUrl);
        window.addEventListener("mousemove", update);
    });
    onUnmounted(() => {
        store.hideImage();
        window.addEventListener("mousemove", update);
    });

    return {x, y}
}
import {ref, onMounted, onUnmounted} from "vue"
import { store } from "@/store";

export function useMouseImage(imageUrl) {
    const x = ref(null);
    const y = ref(null);

    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    if (isMobile) {
        return
    }

    function update(event) {
        store.setImageX(event.pageX);
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
}
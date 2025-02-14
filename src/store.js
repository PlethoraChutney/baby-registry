import { reactive } from "vue";

export const store = reactive({
    "imageX": 0,
    "imageY": 0,
    "imageShow": false,
    "imageUrl": "",
    showImage(url) {
        this.imageUrl = url;
        this.imageShow = true;
    },
    setImageX(x) {
        this.imageX = x;
    },
    setImageY(y) {
        this.imageY = y;
    },
    hideImage() {
        this.imageShow = false;
        this.imageUrl = "";
    },

    buyingAcknowledged: false,

    items: {},
    async updateItems() {
        return fetch("/api/items/")
        .then(response => response.json())
        .then(items => {
            console.log(items);
            this.items = items;
        })
        .catch(err => console.error(err))
    },
    async updatePurchased() {
        return fetch("/api/purchased/")
        .then(response => response.json())
        .then(items => items.forEach(e => this.items[e[0]].purchased = e[1]))
    }
})
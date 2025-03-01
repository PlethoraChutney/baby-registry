import { reactive } from "vue";

export const store = reactive({
    userName: "",
    currentAuthStatus: null,
    async isAuthenticated() {
        if (this.currentAuthStatus !== null) {
            return this.currentAuthStatus;
        }

        return fetch(
            "/api/login/",
            {
                credentials: "include"
            }
        )
        .then(response => response.json())
        .then(response => {
            this.currentAuthStatus = response.is_authenticated;
            return this.currentAuthStatus;
        })
    },
    loginAuthenticated() {
        this.currentAuthStatus = true;
    },
    imageX: 0,
    imageY: 0,
    imageShow: false,
    imageUrl: "",
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
            this.items = items;
        })
        .catch(err => console.error(err))
    },
    async updatePurchased() {
        return fetch("/api/purchased/")
        .then(response => response.json())
        .then(items => items.forEach(e => {
            this.items[e[0]].purchased = e[1]}
        ))
    },

    notificationTitle: "",
    notificationBody: "",
    showNotification: false,
    notify(title, body, duration = 2000) {
        this.notificationTitle = title;
        this.notificationBody = body;
        this.showNotification = true;
        setTimeout(() => store.hideNotification(), duration)
    },
    hideNotification() {
        this.showNotification = false;
        setTimeout(() => {
            this.notificationTitle = "";
            this.notificationBody = "";
        }, 500)
    },
})
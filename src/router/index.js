import { createRouter, createWebHistory } from 'vue-router'
import { store } from '@/store'
import HomeView from '@/views/HomeView.vue'
import Registry from '@/views/Registry.vue'
import Login from "@/views/Login.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: "/registry",
      name: "registry",
      component: Registry
    },
    {
      path: "/login",
      name: "login",
      component: Login
    }
  ],
})

router.beforeEach(async (to, from) => {
  const isAuthenticated = await store.isAuthenticated();
  if (!isAuthenticated && to.name !== "login") {
    return {name: "login"}
  }
})

export default router

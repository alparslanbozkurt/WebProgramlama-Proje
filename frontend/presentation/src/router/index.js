import { createRouter, createWebHistory } from "vue-router";
// Daha önceki Home.vue satırını güncelledik:
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  // (başka view yoksa bu kadarı yeterli)
];

export default createRouter({
  history: createWebHistory(),
  routes,
});

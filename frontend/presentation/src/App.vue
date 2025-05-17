<template>
  <div id="app" class="d-flex flex-column vh-100">
    <NavBar @toggle-sidebar="sidebarOpen = !sidebarOpen" />

    <div class="d-flex flex-fill">
      <SidebarMenu :open="sidebarOpen" />

      <main class="flex-fill p-4 overflow-auto">
        <router-view />
      </main>
    </div>

    <FooterSection />
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import SidebarMenu from "./components/SidebarMenu.vue";
import FooterSection from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    NavBar,
    SidebarMenu,
    FooterSection,
  },
  data() {
    return {
      sidebarOpen: false,
    };
  },
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
}
</style>

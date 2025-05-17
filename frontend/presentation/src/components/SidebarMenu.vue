<template>
  <div
    :class="[
      'bg-secondary text-white vh-100 p-3 d-flex flex-column',
      open ? 'd-block' : 'd-none',
      'd-lg-block',
    ]"
  >
    <ul class="nav flex-column">
      <li class="nav-item mb-2">
        <router-link class="nav-link text-white" to="/">
          Ana Sayfa
        </router-link>
      </li>
      <li class="nav-item mb-2">
        <router-link class="nav-link text-white" to="/watchlist">
          İzleme Listem
        </router-link>
      </li>
      <li class="nav-item mb-2">
        <router-link class="nav-link text-white" to="/favorites">
          Favoriler
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SidebarMenu",
  props: {
    open: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

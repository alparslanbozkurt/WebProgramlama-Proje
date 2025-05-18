<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light px-3">
    <div class="container-fluid">
      <button
        type="button"
        class="btn btn-outline-secondary d-lg-none me-3"
        @click="$emit('toggle-sidebar')"
      >
        <span class="navbar-toggler-icon" />
      </button>

      <a class="navbar-brand me-auto me-lg-0" href="#">
        <img src="@/assets/logo.png" alt="Logo" height="30" />
      </a>

      <form class="d-flex mx-auto mx-lg-3" role="search">
        <input
          class="form-control me-2"
          type="search"
          placeholder="Film ara..."
          aria-label="Search"
        />
        <button class="btn btn-outline-success" type="submit">Ara</button>
      </form>

      <ul class="navbar-nav mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link class="nav-link" to="/profile"> Profil </router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" @click.prevent="logout"> Çıkış </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  methods: {
    logout() {
      console.log("Kullanıcı çıkış yaptı");
      this.$router.push("/login");
    },
  },
};
</script>

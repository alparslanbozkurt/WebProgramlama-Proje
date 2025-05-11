<template>
  <div class="card h-100">
    <img
      :src="movie.posterUrl"
      class="card-img-top"
      :alt="movie.title"
      v-if="movie.posterUrl"
    />
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ movie.title }}</h5>
      <p class="card-text">{{ movie.overview }}</p>
      <button @click="addToWatchlist" class="btn btn-outline-light mt-auto">
        İzleme Listesine Ekle
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "RecommendationCard",
  props: {
    movie: {
      type: Object,
      required: true,
    },
  },
  methods: {
    addToWatchlist() {
      // Örnek: LocalStorage’a ekleyebilir veya API’ye POST atabilirsiniz
      console.log("İzleme listesine eklendi:", this.movie);
      alert(`${this.movie.title} izleme listenize eklendi!`);
    },
  },
};
</script>

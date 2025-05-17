<template>
  <div>
    <!-- 1) Loading spinner -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <!-- 2) Eğer hiç film yoksa -->
    <div v-else-if="movies.length === 0" class="text-center my-5">
      <p>Henüz öneri yok.</p>
    </div>

    <!-- 3) Film kartları -->
    <div v-else class="row">
      <div
        class="col-12 col-md-6 col-lg-4 mb-4"
        v-for="movie in movies"
        :key="movie.id"
      >
        <RecommendationCard :movie="movie" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import RecommendationCard from "./RecommendationCard.vue";

export default {
  name: "RecommendationList",
  components: { RecommendationCard },
  data() {
    return {
      movies: [],
      loading: true,
    };
  },
  mounted() {
    axios
      .get("/api/recommendations")
      .then((res) => {
        this.movies = res.data;
      })
      .catch((err) => {
        console.error("Öneri çekme hatası:", err);
      })
      .finally(() => {
        this.loading = false;
      });
  },
};
</script>

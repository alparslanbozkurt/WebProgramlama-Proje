<template>
  <div class="p-4">
    <h1 class="display-4 mb-4">Önerilen Filmler</h1>
    <RecommendationList />
  </div>
</template>

<script>
import RecommendationList from "../components/RecommendationList.vue";

export default {
  name: "HomeView",
  components: { RecommendationList },
};
</script>

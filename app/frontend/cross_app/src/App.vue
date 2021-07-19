<template>
  <div class="app-container" :style="isLoading ? 'height: 100vh;' : ''">
    <Loader v-if="isLoading" />
    <div v-else>
      <Home 
        v-if="!isGridGenerated"
        @generate-grid="initCrossword" 
      />
      <Grid v-else :grid-data="gridData" />
    </div>
  </div>
</template>

<script>
import { ref, getCurrentInstance, onMounted } from 'vue';
import Home from './components/page-sections/Home.vue';
import Grid from './components/Grid.vue';
import Loader from './components/utils/Loader.vue';

import axios from 'axios';

export default {
  name: 'App',
  components: {
    Home,
    Grid,
    Loader
  },
  setup() {
    const isLoading = ref(false);
    const isGridGenerated = ref(false);
    const gridData = ref(null);
    const isTesting = ref(false);
    
    const internalInstance = getCurrentInstance(); // globalproperties

    const initCrossword = async (inputData) => {
      await fetchCrosswordData(inputData);
      isGridGenerated.value = true;
    }
    
    const fetchCrosswordData = async (inputData) => {
      const PORT = 5000;
      const endpoint = isTesting.value ? 'clues_test' : 'clues';
      isLoading.value = true;
      
      await axios.post(`http://localhost:${PORT}/${endpoint}`, {
        ...inputData
      })
        .then(res => {
          gridData.value = {
            ...res.data,
            theme: inputData.theme
          };
          isLoading.value = false;
        })
        .catch(e => {
          console.log(e);
          isLoading.value = false;
        });
    }

    onMounted(() => {
      isTesting.value = internalInstance.appContext.config.globalProperties.is_testing;
      const theme = internalInstance.appContext.config.globalProperties.pdf_title;
      if (isTesting.value) {
        initCrossword({'theme': theme});
      }
    })

    return {
      isLoading,
      isGridGenerated,
      gridData,
      initCrossword
    };
  }
}
</script>

<style lang="scss" scoped>
body, #app {
  margin: 0;
  padding: 0;
}
#app{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  color: rgb(37, 32, 32);
}
app-container {
  max-width: 1060px;
  width: 100%;
} 
</style>

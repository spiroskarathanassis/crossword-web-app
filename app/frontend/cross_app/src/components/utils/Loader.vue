<template>
  <div class="flex-center">
    <h1>The new generation Crossword</h1>

    <div class="flex-center">
      <div class="pixel-spinner">
        <div class="pixel-spinner-inner"></div>
      </div>
      <p>System takes some time to generate it. Good luck.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Loader'
}
</script>

<style scoped>
.flex-center {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.pixel-spinner, .pixel-spinner * {
  box-sizing: border-box;
}

.pixel-spinner {
  height: 70px;
  width: 70px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.pixel-spinner .pixel-spinner-inner {
  width: calc(70px / 7);
  height: calc(70px / 7);
  background-color: #ff1d5e;
  color: #ff1d5e;
  box-shadow: 15px 15px  0 0,
              -15px -15px  0 0,
              15px -15px  0 0,
              -15px 15px  0 0,
              0 15px  0 0,
              15px 0  0 0,
              -15px 0  0 0,
              0 -15px 0 0;
  animation: pixel-spinner-animation 2000ms linear infinite;
}

@keyframes pixel-spinner-animation {
  50% {
    box-shadow: 20px 20px 0px 0px,
                -20px -20px 0px 0px,
                20px -20px 0px 0px,
                -20px 20px 0px 0px,
                0px 10px 0px 0px,
                10px 0px 0px 0px,
                -10px 0px 0px 0px,
                0px -10px 0px 0px;
  }
  75% {
    box-shadow: 20px 20px 0px 0px,
                -20px -20px 0px 0px,
                20px -20px 0px 0px,
                -20px 20px 0px 0px,
                0px 10px 0px 0px,
                10px 0px 0px 0px,
                -10px 0px 0px 0px,
                0px -10px 0px 0px;
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
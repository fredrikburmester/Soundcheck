<template>
    <router-view />
</template>

<script>
export default {
}
</script>

<style>
body {
  min-height: 100vh;
  min-height: -webkit-fill-available;
}
html {
  height: -webkit-fill-available;
}

html,
body {
    margin: 0;
    padding: 0;
}
#app {
    color: white;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    min-width: 100vw;
    position: fixed;
    top: 0;
    left: 0;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    background-color: #191414;
    overflow-y: scroll;
}
</style>

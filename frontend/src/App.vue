<template>
    <router-view />
</template>

<script>
export default {
}
</script>

<style>
html,
body {
    margin: 0;
    padding: 0;
}
*::-webkit-scrollbar {
  display: none;
}
#app {
    color: white;
    margin: 0;
    padding: 0;
    height: 100vh;
    width: 100vw;
    position: fixed;
    top: 0;
    left: 0;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    background-color: #191414;
    /* overflow-y: scroll; */
}
</style>

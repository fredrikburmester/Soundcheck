<template>
    <div class="loader">
        <p>Loading...</p>
    </div>
</template>

<script>
export default {
    name: 'Loader'
}
</script>

<style scoped>
.loader {
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.7);
    position: fixed;
    top: 0;
    left: 0;
    display: grid;
    place-items: center;
}
</style>
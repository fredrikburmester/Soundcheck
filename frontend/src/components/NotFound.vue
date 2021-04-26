<template>
    <div class="page">
        <div class="text">
            <h1>404</h1>
            <p>This is not the room you're looking for...</p>
        </div>
        <Button class="button" buttonText="Go Home" buttonLink="/"></Button>
    </div>
</template>
<script>
import Button from '../components/Button';
export default {
    name: 'NotFound',
    components: {
        Button,
    },
};
</script>
<style scoped>
.page {
    height: 100vh;
    width: 100vw;
    padding: 0;
    margin: 0;
}
.page .text {
    position: fixed;
    bottom: 50vh;
    left: 50%;
    transform: translateX(-50%);
}
.page .button {
    position: fixed;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
}
</style>

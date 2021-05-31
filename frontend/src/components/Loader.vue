/* 
Loading component, covers entire screen. Implemented in App.vue, enabled by changing the store loadingState to true. 
Takes no arguments.
*/

<template>
    <div class="loader">
        <img
            width="63" height="75" :src="logo"
            class="logo" 
        >
    </div>
</template>

<script>
import logo from '../assets/soundcheck-logo.png'

export default {
    name: 'Loader',
    data() {
        return {
            logo: logo
        }
    }
}
</script>

<style scoped>
.loader {
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 1);
    position: fixed;
    top: 0;
    left: 0;
    display: grid;
    place-items: center;
    z-index: 9999;
}
img {
    transform-origin: 50% 50%; 
    animation-name: spin;
    animation-duration: 1000ms;
    margin-bottom: 10vh;
    animation-iteration-count: infinite;
    animation-timing-function: cubic-bezier(0.71, 0.05, 0.38, 0.98); 
}
@keyframes spin {
    from {
        transform:rotate(0deg);
    }
    to {
        transform:rotate(360deg);
    }
}

</style>
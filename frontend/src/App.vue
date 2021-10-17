/*
This is the main container for the app. A global loader based on the store value 'loading' is implemented here, kept updated by the watch function. 
 */

<template>
    <transition name="fade" mode="out-in">
        <Loader v-if="loading" />
        <router-view v-else />
    </transition>
</template>

<script>
import Loader from './components/Loader'

export default {
    components: {
        Loader,
    },
    computed: {
        loading() {
            return this.$store.state.loading
        }
    },
    watch: {
        '$store.state.loading': function() {}
    }
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
    min-height: 100vh;
    min-height: -webkit-fill-available;
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
.fade-enter-active, .fade-leave-active {
  transition: opacity .1s ease;
  -webkit-transition: opacity .1s ease;
  -moz-transition: opacity .1s ease;
  -o-transition: opacity .1s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>

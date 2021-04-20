<template>
    <div class="create">
        <h1>Almost there...</h1>
        <Button v-on:click="createRoom" buttonText="Quick start"></Button>
        <div class="back">
            <Button buttonLink="/" buttonText="Back" color="#CD1A2B"></Button>
        </div>
    </div>
</template>

<script>
import Button from '../components/Button';

export default {
    name: 'Create',
    components: {
        Button,
    },
    sockets: {
        roomCode(data) {
            this.$router.push(data.code);
        },
    },
    methods: {
        createRoom: function () {
            this.$socket.client.emit('createRoom', {
                sid: localStorage.getItem('sid'),
            });
        },
    },
};
</script>

<style scoped>
.create {
    margin-top: 30vh;
}
.back {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
}
</style>

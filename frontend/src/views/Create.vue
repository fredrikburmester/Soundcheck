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
const io = require('socket.io-client');
// const socket = io("https://musicwithfriends.fdrive.se");
var socket;

if(process.env.NODE_ENV == 'production') {
    socket = io('https://musicwithfriends.fdrive.se', {
        path: '/ws/socket.io',
    });
} else {
    socket = io();
}

export default {
    name: 'Create',
    components: {
        Button,
    },
    data() {
        return {};
    },
    methods: {
        // Function for creating a room.
        createRoom: function () {
            socket.emit('createRoom');
        },
    },

    mounted() {
        // When room is created the server will return a code that we can go to to join the room.
        socket.on('roomCode', (data) => {
            this.$router.push(data.code);
        });
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

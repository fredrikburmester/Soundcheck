<template>
	<div class="create">
		<h1>Almost there...</h1>
        <Button buttonLink="/" buttonText="Back"></Button>
        <Button v-on:click="createRoom" buttonText="Quick start"></Button>
	</div>
</template>

<script>
import Button from '../components/Button'
const io = require("socket.io-client");
// const socket = io("https://musicwithfriends.fdrive.se");
const socket = io("https://musicwithfriends.fdrive.se", {path: '/ws/socket.io'});

export default {
	name: "Create",
	components: {
        Button
	},
    data() {
        return {
        }
    },
	methods: {
        // Function for creating a room.
		createRoom: function() { 
            socket.emit('createRoom');
        }
	},
    
    mounted() {
        // When room is created the server will return a code that we can go to to join the room.
        socket.on("roomCode", (data) => {
            this.$router.push(data.code)
        });
    }
};
</script>

<style scoped>
	.create {
		margin-top:30vh;
	}
</style>

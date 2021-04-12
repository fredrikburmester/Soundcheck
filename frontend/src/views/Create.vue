<template>
	<div class="create">
		<h1>Create Room</h1>
	    <router-link to="/">Home</router-link>
        <button v-on:click="createRoom">Create Room</button>
	</div>
</template>

<script>
// Creating the websockets instance
const io = require("socket.io-client");
const socket = io("http://localhost:5000");

export default {
	name: "Create",
	components: {
 
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

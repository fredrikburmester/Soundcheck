<template>
    <div>
        Nothing to see here
    </div>
</template>

<script>
const io = require("socket.io-client");
const socket = io();

export default {
    name: "LoginCallback",
    methods: {
        handleLoginCallback: function() {
            let uri = window.location.href.split('=')[1]
            let code = uri.split('&')[0]
            socket.emit('generate_access_token',{'code': code});
        } 
    },
    mounted() {
        this.handleLoginCallback()

        socket.on("access_token", (data) => {
            localStorage.setItem('access_token', data.access_token)
            localStorage.setItem('refresh_token', data.refresh_token)
            console.log(data.access_token, data.refresh_token);
            this.$router.push('/')
        });
    },
}
</script>
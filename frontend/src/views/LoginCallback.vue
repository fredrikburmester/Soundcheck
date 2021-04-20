<template>
    <div>Nothing to see here</div>
</template>

<script>
export default {
    name: 'LoginCallback',
    sockets: {
        connect() {
            console.log('socket connected');
        },
        access_token(data) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            localStorage.setItem('sid', data.sid);

            if (localStorage.getItem('toRoom')) {
                var toRoom = localStorage.getItem('toRoom');
                localStorage.removeItem('toRoom');
                this.$router.push(`/${toRoom}`);
            } else {
                this.$router.push('/');
            }
        },
    },
    methods: {
        handleLoginCallback: function () {
            let uri = window.location.href.split('=')[1];
            let code = uri.split('&')[0];
            this.$socket.client.emit('generate_access_token', { code: code });
        },
    },
    mounted() {
        this.handleLoginCallback();
    },
};
</script>

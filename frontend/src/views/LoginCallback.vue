/* 
After authenticating with Spotify, the client is directed to this page which saves the recieved token and request a 
new spotify API token from our server.   
 */

<template>
    <Loader />
</template>

<script>
import Loader from '../components/Loader'
export default {
    name: 'LoginCallback',
    components: {
        Loader
    },
    sockets: {
        // get access_token from our server back. 
        access_token(data) {
            this.$store.commit('setAccessToken', data.access_token)
            this.$store.commit('setSid', data.sid)

            // localStorage.setItem('access_token', data.access_token);
            // localStorage.setItem('sid', data.sid);
            // localStorage.setItem('refresh_token', data.refresh_token);

            if (localStorage.getItem('toRoom')) {
                var toRoom = localStorage.getItem('toRoom');
                localStorage.removeItem('toRoom');
                this.$router.push(`/${toRoom}`);
            } else {
                this.$router.push('/');
            }
        },
    },
    mounted() {
        // Send spotify token to our server
        this.handleLoginCallback();
    },
    methods: {
        handleLoginCallback: function () {
            let uri = window.location.href.split('=')[1];
            let code = uri.split('&')[0];
            this.$socket.client.emit('generate_access_token', { code: code });
        },
    },
};
</script>

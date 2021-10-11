/* 

 */

<template>
    <Loader />
</template>

<script>
import Loader from '../components/Loader'

export default {
    name: 'LoginRedirect',
    components: {
        Loader
    },
    mounted() {
        if(this.$route.params.sid !== undefined) {
            this.$store.commit('setSid', this.$route.params.sid)
            this.loginWithSpotify()
        }
    },
    methods: {
        loginWithSpotify: function () {
            window.location.href = `https://accounts.spotify.com/authorize?client_id=bad02ecfaf4046638a1daa7f60cbe42b&response_type=code&redirect_uri=${process.env.VUE_APP_CALLBACK_URL}&scope=user-read-private%20user-top-read%20user-read-email%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20playlist-read-collaborative&state=34fFs29kd09&show_dialog=true`;
        },
    },
};
</script>

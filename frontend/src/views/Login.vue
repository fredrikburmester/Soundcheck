<template>
    <div class="login">
        <h1>Music With Friends</h1>
        <Button
            button-text="Authenticate"
            @click="loginWithSpotify"
        />
        <p>Click to log in with Spotify</p>
    </div>
</template>

<script>
import Button from '../components/Button';
export default {
    name: 'Login',
    components: {
        Button,
    },
    beforeMount() {
        this.checkToken();
    },
    methods: {
        loginWithSpotify: function () {
            window.location.href = `https://accounts.spotify.com/authorize?client_id=bad02ecfaf4046638a1daa7f60cbe42b&response_type=code&redirect_uri=${process.env.VUE_APP_CALLBACK_URL}&scope=user-read-private%20user-top-read%20user-read-email%20playlist-modify-public%20playlist-modify-private&state=34fFs29kd09&show_dialog=true`;
        },
        checkToken: function () {
            if (localStorage.getItem('token')) {
                this.$router.push('/');
            }
        },
    },
};
</script>

<style scoped>
.login {
    margin-top: 30vh;
}
p {
    color: rgba(255, 255, 255, 0.68);
    font-style: italic;
}
</style>

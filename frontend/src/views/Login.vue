<template>
    <div class="login">
        <h1>Music With Friends</h1>
        <Button v-on:click="loginWithSpotify" buttonText="Authenticate" />
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
    methods: {
        loginWithSpotify: function () {
            window.location.href =
                'https://accounts.spotify.com/authorize?client_id=bad02ecfaf4046638a1daa7f60cbe42b&response_type=code&redirect_uri=https://musicwithfriends.fdrive.se/logincallback&scope=user-read-private%20user-read-email&state=34fFs29kd09&show_dialog=true';
        },
        checkToken: function () {
            if (localStorage.getItem('token')) {
                this.$router.push('/');
            }
        },
    },
    beforeMount() {
        this.checkToken();
    },
};
</script>

<style scoped>
.login {
    margin-top: 30vh;
}
p {
    opacity: 70%;
    font-style: italic;
}
</style>

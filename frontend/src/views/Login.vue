<template>
    <div class="login">
        <div id="brand">
            <img :src="logo" alt="soundcheck">
        </div>
        <Button
            button-text="Authenticate"
            @click="loginWithSpotify"
        />
        <p>Click to log in with Spotify</p>

        <div class="about" @click="aboutPage">
            <p>
                About Soundcheck
            </p>
        </div>
    </div>
</template>

<script>
import Button from '../components/Button';
import logo from '../assets/soundcheck.png';
export default {
    name: 'Login',
    components: {
        Button,
    },
    data: function () {
        return {
            logo: logo
        };
    },
    beforeMount() {
        this.checkToken();
    },
    methods: {
        loginWithSpotify: function () {
            window.location.href = `https://accounts.spotify.com/authorize?client_id=bad02ecfaf4046638a1daa7f60cbe42b&response_type=code&redirect_uri=${process.env.VUE_APP_CALLBACK_URL}&scope=user-read-private%20user-top-read%20user-read-email%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20playlist-read-collaborative&state=34fFs29kd09&show_dialog=true`;
        },
        checkToken: function () {
            if (localStorage.getItem('token')) {
                this.$router.push('/');
            }
        },
        aboutPage: function(){
            this.$router.push('/about');
        }
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.login {
    margin-top: 30vh;
    padding: 0 2rem 0 2rem;
}
#brand > img{
	width: 80vw;
    max-width: 400px;
    margin-bottom: 60px;
}
p {
    color: rgba(255, 255, 255, 0.68);
    font-style: italic;
}
.about{
    font-family: 'Roboto', sans-serif;
    width: 100vw;
    text-align: center;
    position: fixed;
    bottom: 0;
    color: rgba(255, 255, 255, 0.88);
}
</style>

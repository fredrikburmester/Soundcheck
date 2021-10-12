/*
Page for users to authenticate with Spotify. Essentially logging in.

The flow for logging in is as such: 
    - /login -> Spotify Authentication System -> /logincallback
 */

<template>
    <div class="login">
        <div id="brand">
            <img :src="logo" alt="soundcheck">
        </div>
        <Button
            button-text="Authenticate"
            @click="loginRedirect"
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
import { Browser } from '@capacitor/browser';
import { Clipboard } from '@capacitor/clipboard';


export default {
    name: 'Login',
    components: {
        Button,
    },
    data: function () {
        return {
            logo: logo,
            sid: String
        };
    },
    sockets: {
        generate_sid({sid}) {
            this.sid = sid
        },
        access_token(data) {
            this.$store.commit('setAccessToken', data.access_token)
            this.$store.commit('setSid', data.sid)

            if (localStorage.getItem('toRoom')) {
                var toRoom = localStorage.getItem('toRoom');
                localStorage.removeItem('toRoom');
                this.$router.push(`/${toRoom}`);
            } else {
                this.$router.push('/');
            }

            this.closeBrowser()
        },
    },
    beforeMount() {
        this.checkToken();
    },
    mounted() {
        this.$socket.client.emit('generate-sid');
    },
    methods: {
        // Sends the user to spotify authentication system
        loginRedirect: async function() {
            if(this.sid != null) {
                await Browser.open({ url: `${process.env.VUE_APP_PROTOCOL}://${process.env.VUE_APP_PUBLIC_URL}/login-redirect/${this.sid}` });
            }
        },
        closeBrowser: async function() {
            await Browser.close()
        },
        checkToken: function () {
            if (this.$store.getters.getAccessToken) {
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
    font-size: 16px;
    width: 100vw;
    margin-left: -2rem;
    text-align: center;
    position: fixed;
    bottom: 40px;
}
.about > p {
    color: rgb(101, 101, 101)
}
</style>

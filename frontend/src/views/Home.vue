<template>
    <div class="home">
        <div class="content">
            <div id="brand">
                <img :src="logo" alt="soundcheck">
            </div>
            <!-- <h1>Start a game...</h1> -->
            <Button
                button-link="/create"
                button-text="Create Room"
            />
            <Button
                button-link="/join"
                button-text="Join Room"
            />
            <Button
                button-link="/me"
                button-text="my games"
                color="#454545"
            />
            <p>{{ name }}</p>
            <div class="button-container">
                <div class="logout">
                    <Button
                        color="#CD1A2B"
                        button-link="/logout"
                        button-text="Log out"
                        class="logout"
                        @click="logout"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
const axios = require('axios');
import Button from '../components/Button';
import logo from '../assets/soundcheck.png'

export default {
    name: 'Home',
    components: {
        Button,
    },
    data: function () {
        return {
            name: '',
            logo: logo
        };
    },
    methods: {
        getUserData: function () {
            var self = this;
            var token = localStorage.getItem('access_token');
            axios
                .get('https://api.spotify.com/v1/me', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                })
                .then(function (response) {
                    self.name = response.data.display_name;
                });
        },
        logout: function () {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_id');
            this.$router.push('/login');
        },
    },
};
</script>

<style scoped>
#brand > img{
	width: 80vw;
    max-width: 400px;
    margin-bottom: 60px;
}
.home {
    display: grid;
    padding: 26vh 2rem 0 2rem;
}
.button-container {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    width: 100vw;
}
.logout {
    padding: 0 2rem 0 2rem;
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 0 2rem 2rem 2rem;
}
</style>

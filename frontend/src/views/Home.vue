<template>
  <div class="home">
    <h1>Start a game...</h1>
    <Button
      button-link="/create"
      button-text="Create Room"
    />
    <Button
      button-link="/join"
      button-text="Join Room"
    />
    <p>{{ name }}</p>
    <div class="logout">
      <Button
        color="#CD1A2B"
        button-link="/logout"
        button-text="Log out"
        @click="logout"
      />
    </div>
  </div>
</template>

<script>
const axios = require('axios');
import Button from '../components/Button';

export default {
    name: 'Home',
    components: {
        Button,
    },
    data: function () {
        return {
            name: '',
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
            this.$router.push('/login');
        },
    },
};
</script>

<style scoped>
.home {
    margin-top: 30vh;
}
.logout {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
}
</style>

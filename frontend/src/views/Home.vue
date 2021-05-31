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

            <div v-if="error" class="errorpopup">
                <div  class="noTopTrack"/>           
                <div class="modal-view">
                        <span class="close" @click="close()">&times;</span>
                        <h3>Error!</h3>
                        <p>No top tracks found</p>   
                </div>
            </div>
            
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
            logo: logo,
            error: this.$store.state.noTracksFound
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
        close(){
            this.error = false
            self.$store.commit(
                'updateNoTracks',
                false
            );
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
.close {
    color: #aaa;
    font-size: 28px;
    font-weight: bold;
    position: absolute;
    right: 20px;
    cursor: pointer;
}
.noTopTrack{
   width: 100vw;
   height: 100vh;
   opacity: 0.5;
   background-color: #000;
   position: fixed;
   top: 0;
   left: 0;
   z-index: 3;
}
.modal-view{
    z-index: 4;
    position: absolute;
    background-color: rgba(255, 255, 255);  
    color: #CD1A2B;
    top: 50%;
    left: 50%;
    width: 80vw;
    height: 80px;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    border-radius: 10px;
    padding: 2rem;
}
</style>

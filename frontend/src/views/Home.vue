/*
Home page with options for creating or joining a room and logging out. 
 */

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
import Button from '../components/Button';
import logo from '../assets/soundcheck.png'

export default {
    name: 'Home',
    components: {
        Button,
    },
    data: function () {
        return {
            logo: logo,
            error: this.$store.state.noTracksFound,
            sid: this.$store.getters.getSid
        };
    },
    mounted: function () {
        this.generateSid()
    },
    sockets: {
        generate_sid({sid}) {
            this.sid = sid
            this.$store.commit('setSid', this.sid)
        },
    },
    methods: {
        logout: function () {
            this.$store.commit('clearCredentials')
            this.$router.push('/login');
        },
        // closes the "player has no tracks" modal
        close(){
            this.error = false
            self.$store.commit(
                'updateNoTracks',
                false
            );
        },
        generateSid() {
            this.$socket.client.emit('generate_sid', { path: 'Home' });
        }
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
    bottom: 15px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    width: 100vw;
}
.logout {
    padding: 0 2rem 0 2rem;
}

</style>

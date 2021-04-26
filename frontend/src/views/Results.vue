<template>
    <div>
        <h1 class="code">{{ code }}</h1>
        <div class="hr"></div>
        <h3 class="title">Results</h3>
        <div class="list">
            <PlayerAvatar
                class="player-guess"
                :id="player.id"
                v-for="player in players"
                v-bind:key="player.id"
                :playerName="getPoints(player)"
                :color="player.color"
            />
        </div>
        <Button class="goHome" buttonLink="/" buttonText="Play again" />
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';

const axios = require('axios');

export default {
    name: 'Results',
    components: {
        PlayerAvatar,
        Button,
    },
    data: function () {
        return {
            code: this.$route.params.code,
            players: null,
        };
    },
    mounted() {
        var self = this;
        var url;
        if (
            process.env.NODE_ENV == 'development' ||
            process.env.NODE_ENV == 'dev'
        ) {
            url = `http://${process.env.VUE_APP_SERVER_URL}/api/${this.code}/results`;
        } else {
            url = `https://${process.env.VUE_APP_SERVER_URL}/api/${this.code}/results`;
        }
        axios.get(url).then(function (response) {
            console.log(response);
            self.players = response.data.players;
        });
    },
    methods: {
        getPoints: function (player) {
            return `${player.name} - ${player.points}`;
        },
    },
};
</script>

<style scoped>
.code {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 0;
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 1rem 2rem 1rem 2rem;
}
.title {
    font-style: italic;
    color: darkgrey;
    text-align: left;
    margin-left: 2rem;
    margin-top: 0;
    margin-bottom: 20px;
}
.list {
    height: calc(100vh - 420px);
    overflow-y: scroll;
    margin-left: 2rem;
    margin-right: 2rem;
    overflow-x: hidden;
}
.goHome {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    z-index: 1;
}
</style>

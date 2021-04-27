<template>
    <div v-bind:key="state">
        <div v-if="state == 'loading'">
            <p>Loading...</p>
        </div>
        <div v-if="state == 'found'">
            <h1 class="code">{{ code }}</h1>
            <p class="date">{{ date }}</p>
            <div class="hr"></div>
            <h3 class="title">Results</h3>
            <div class="list">
                <div
                    :class="
                        selected == player.id
                            ? 'expand player-block'
                            : 'player-block'
                    "
                    v-for="player in players"
                    v-bind:key="player.id"
                >
                    <PlayerAvatar
                        class="player-guess"
                        :id="player.id"
                        :playerName="getPoints(player)"
                        :color="player.color"
                        @click="selectPlayer(player)"
                    />
                    <div v-if="selected == player.id">
                        <div v-for="guess in player.guesses" v-bind:key="guess">
                            <GuessIcon
                                :trackID="guess.info"
                                :guess="guess.guess"
                                :answer="guess.correct_answer"
                            />
                        </div>
                    </div>
                </div>
            </div>
            <Button class="goHome" buttonLink="/" buttonText="Play again" />
        </div>
        <div v-if="state == 'not-found'">
            <NotFound />
        </div>
        <Button class="goHome" buttonLink="/" buttonText="Play again" />
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';
import NotFound from '../components/NotFound';
import GuessIcon from '../components/GuessIcon';

const axios = require('axios');

export default {
    name: 'Results',
    components: {
        PlayerAvatar,
        Button,
        NotFound,
        GuessIcon,
    },
    data: function () {
        return {
            code: this.$route.params.code,
            players: null,
            state: 'loading',
            date: null,
            selected: '',
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
        axios
            .get(url)
            .then(function (response) {
                console.log(response);
                var data = response.data;
                self.state = 'found';
                self.players = data.players;
                var date = new Date(data.date * 1000);
                var date_string = date.toLocaleDateString('se');
                var hour = date.getHours();
                var minute = date.getMinutes();
                if (minute < 10) minute = '0' + minute.toString();
                // var second = date.getSeconds()

                /* eslint-disable */
                self.date = `Played on ${date_string} @ ${hour}:${minute}`;
                /* eslint-enable */

                // Convert answer ids to names
                for (let player of data.players) {
                    for (let guess of player.guesses) {
                        for (let player2 of data.players) {
                            if (player2.sid == guess.guess) {
                                guess.guess = player.name;
                            }
                            if (player2.sid == guess.correct_answer) {
                                guess.correct_answer = player.name;
                            }
                        }
                    }
                }
            })
            .catch(function (error) {
                console.log(error);
                self.state = 'not-found';
            });
    },
    methods: {
        getPoints: function (player) {
            return `${player.name}: ${player.points} points`;
        },
        selectPlayer(player) {
            console.log('select player');
            this.selected = player.id;
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
.date {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 0;
    color: gray;
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
.player-block {
    height: 90px;
    transition: 1s;
    overflow: hidden;
}
.expand {
    transition: 1s;
    height: 250px;
}
</style>

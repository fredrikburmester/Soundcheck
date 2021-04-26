<template>
    <div v-if="found" :key="found" class="gameroom">
        <div v-if="showQR" class="bigQR" @click="showQR = false">
            <img :src="qr" @click="showQR = false" />
        </div>
        <div v-if="started" :key="started">
            <ProgressBar class="progressbar" />
            <h2>Guess who this song belongs to!</h2>
            <p>
                Players guessed: {{ getPlayersGuessed }} / {{ players.length }}
            </p>
            <p>
                Current_question: {{ current_question }} / {{ nr_of_questions }}
            </p>
            <div class="list" v-bind:key="my_guess">
                <PlayerAvatar
                    @click="guess(player)"
                    v-for="player in players"
                    class="player-guess"
                    v-bind:key="player.id"
                    :id="player.id"
                    :playerName="player.name"
                    :color="player.color"
                    :host="player.host"
                    :selected="selected(player.sid)"
                />
            </div>
            <div v-if="host" class="next-song">
                <Button
                    v-on:click="sendNextQuestion"
                    buttonText="next question"
                    color="#1DB954"
                />
            </div>
            <div class="leave-started-game">
                <Button
                    v-if="host"
                    v-on:click="leaveRoom"
                    buttonText="end game"
                    color="#CD1A2B"
                />
                <Button
                    v-else
                    v-on:click="leaveRoom"
                    buttonText="Leave Room"
                    color="#CD1A2B"
                />
            </div>
            <iframe
                class="webplayer"
                :src="iframeurl"
                allowtransparency="true"
                allow="encrypted-media"
            ></iframe>
        </div>
        <div v-else>
            <h1 class="code">{{ code }}</h1>
            <div class="hr"></div>
            <h3 class="title">Players:</h3>
            <p v-if="!host">{{ status }}</p>
            <div class="list">
                <PlayerAvatar
                    v-for="player in players"
                    v-bind:key="player.id"
                    :playerName="player.name"
                    :color="player.color"
                    :host="player.host"
                />
            </div>

            <div class="qr">
                <img :src="qr" @click="showQR = true" />
            </div>

            <div class="buttons">
                <div class="copycode">
                    <Button
                        @click="copyToClipboard"
                        color="#FFF"
                        :buttonText="clipboardtext"
                        :key="clipboardtext"
                    ></Button>
                </div>
                <div v-if="host" :key="host" class="startgame">
                    <Button
                        @click="startGame()"
                        buttonText="Start Game"
                    ></Button>
                </div>
                <div class="leave">
                    <Button
                        v-if="host"
                        v-on:click="leaveRoom"
                        buttonText="end game"
                        color="#CD1A2B"
                    />
                    <Button
                        v-else
                        v-on:click="leaveRoom"
                        buttonText="Leave Room"
                        color="#CD1A2B"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';
import ProgressBar from '../components/ProgressBar';

const QRCode = require('qrcode');
const axios = require('axios');

export default {
    name: 'Home',
    components: {
        PlayerAvatar,
        Button,
        ProgressBar,
    },
    data: function () {
        return {
            clipboardtext: `copy invite link`,
            current_question: 0,
            iframeurl: '',
            started: false,
            players: [],
            colors: [],
            showQR: false,
            status: 'Waiting for host to start the game...',
            found: false,
            nr_of_questions: 0,
            my_guess: '',
            host: false,
            code: this.$route.params.code,
            qr: '',
        };
    },
    sockets: {
        not_a_room() {
            console.log('room does not exist');
            this.$store.commit('updateError', 'Room does not exist!');
            this.$router.push('/join');
        },
        no_access_to_room() {
            this.$store.commit('updateError', 'Game already started!');
            this.$router.push('/join');
        },
        join_room_first_time(data) {
            // Do things before page load
            this.players = data.players;
            this.generateQR();
            this.isHost();
            this.getTopTrack();

            // Show page!
            this.found = true;
        },
        reconnect_to_lobby(data) {
            // Do things before page load
            this.players = data.players;
            this.generateQR();
            this.isHost();

            // Show page!
            this.found = true;
        },
        reconnect_to_game(data) {
            // Do things before page load
            this.players = data.players;
            this.isHost();

            // Show page!
            this.found = true;
        },
        update_players_list(data) {
            this.players = data.players;
        },
        go_to_result() {
            this.$router.push(`/${this.code}/results`);
        },
        players_guess(data) {
            //mark player that guessed
            this.$store.commit('updatePlayersGuessed', data['sid']);
        },
        next_question(data) {
            if (this.current_question > 0) {
                this.sendGuess();
            }
            this.current_question += 1;
            this.setIframeUrl(data.trackid);
            this.my_guess = '';
            this.$store.commit('clearPlayersGuessed');
        },
        game_ended() {
            this.sendGuess();
            this.$router.push(`/${this.code}/results`);
        },
        start_game(data) {
            this.nr_of_questions = data.nr_of_questions;
            this.started = true;
        },
    },
    methods: {
        async copyToClipboard() {
            await navigator.clipboard.writeText(window.location.href);
            this.clipboardtext = 'copied!';
        },
        connectToRoom() {
            var access_token = localStorage.getItem('access_token');
            var refresh_token = localStorage.getItem('refresh_token');
            this.$socket.client.emit('connect_to_room', {
                code: this.code,
                sid: localStorage.getItem('sid'),
                access_token: access_token,
                refresh_token: refresh_token,
            });
        },
        generateQR() {
            var self = this;
            QRCode.toDataURL(
                `https://musicwithfriends.fdrive.se/${this.code}`,
                function (err, url) {
                    self.qr = url;
                }
            );
        },
        isHost() {
            var self = this;
            this.players.forEach((player) => {
                if (player.sid == localStorage.getItem('sid')) {
                    if (player.host == true) {
                        self.host = true;
                    }
                }
            });
        },
        startGame() {
            this.$socket.client.emit('start_game', { code: this.code });
            this.sendNextQuestion();
        },
        sendNextQuestion() {
            // var self = this;
            if (this.current_question < this.players.length) {
                this.$socket.client.emit('next_question', {
                    current_question: this.current_question,
                    code: this.code,
                });
            } else {
                this.$socket.client.emit('game_ended', { code: this.code });
            }
        },
        guess(player) {
            // this.resetGuessBackgroundColor();
            this.my_guess = player.sid;
            // document.getElementById(player.id).style.backgroundColor = 'green';
            this.$socket.client.emit('player_guess', {
                sid: localStorage.getItem('sid'),
                code: this.code,
            });
        },

        selected(id) {
            if (id == this.my_guess) {
                return true;
            }
            return false;
        },
        sendGuess() {
            this.$socket.client.emit('guess', {
                guess: this.my_guess,
                sid: localStorage.getItem('sid'),
                current_question: this.current_question - 1,
                code: this.code,
            });
        },
        setIframeUrl(id) {
            this.iframeurl = `https://open.spotify.com/embed?uri=spotify:track:${id}`;
        },
        leaveRoom() {
            this.$socket.client.emit('leave_room', {
                code: this.code,
                sid: localStorage.getItem('sid'),
            });
            this.$router.push('/');
        },
        getTopTrack() {
            var self = this;
            var token = localStorage.getItem('access_token');
            axios
                .get(
                    'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=1',
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                            Accept: 'application/json',
                            'Content-Type': 'application/json',
                        },
                    }
                )
                .then(function (response) {
                    if (response.data.items.length == 0) {
                        axios
                            .get(
                                'https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=1',
                                {
                                    headers: {
                                        Authorization: `Bearer ${token}`,
                                        Accept: 'application/json',
                                        'Content-Type': 'application/json',
                                    },
                                }
                            )
                            .then(function (response) {
                                if (response.data.items.length == 0) {
                                    self.leaveRoom();
                                } else {
                                    var trackid = response.data.items[0].uri.split(
                                        ':'
                                    )[2];
                                    self.$socket.client.emit('toptrack', {
                                        trackid: trackid,
                                        sid: localStorage.getItem('sid'),
                                        room: self.code,
                                    });
                                }
                            });
                    } else {
                        var trackid = response.data.items[0].uri.split(':')[2];
                        self.$socket.client.emit('toptrack', {
                            trackid: trackid,
                            sid: localStorage.getItem('sid'),
                            room: self.code,
                        });
                    }
                });
        },
    },
    computed: {
        getPlayersGuessed() {
            return this.$store.state.players_guessed.length;
        },
    },
    mounted: function () {
        this.connectToRoom();
    },
};
</script>

<style scoped>
.gameroom {
    height: 100vh;
    width: 100vw;
    position: fixed;
    top: 0;
}
.code {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 0;
}
.title {
    font-style: italic;
    color: darkgrey;
    text-align: left;
    margin-left: 2rem;
    margin-top: 0;
    margin-bottom: 20px;
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 1rem 2rem 1rem 2rem;
}
.QR {
    transform: scale(0.5);
    border: 5px solid rgb(255, 255, 255);
}
.qr {
    position: fixed;
    right: 0;
    top: 0;
    padding: 1rem 2rem;
}
.qr > img {
    width: 50px;
}
.list {
    height: calc(100vh - 420px);
    overflow-y: scroll;
    margin-left: 2rem;
    margin-right: 2rem;
    overflow-x: hidden;
}
.startgame {
    position: fixed;
    left: 50%;
    bottom: 160px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    z-index: 1;
}
.copycode {
    position: fixed;
    left: 50%;
    bottom: 90px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    z-index: 1;
}
.leave {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    z-index: 1;
}
.webplayer {
    position: fixed;
    height: 80px;
    width: 100vw;
    left: 0;
    bottom: 0;
}
.progressbar {
    position: fixed;
    bottom: 85px;
    width: 100%;
}
.bigQR {
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.7);
    width: 100vw;
    height: 100vh;
    z-index: 100;
}
.bigQR > img {
    width: 60vw;
    height: auto;
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
}
.leave-started-game {
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
}
.next-song {
    position: fixed;
    bottom: 170px;
    left: 50%;
    transform: translateX(-50%);
}
@media only screen and (min-width: 600px) {
    .bigQR > img {
        height: 30vh;
        width: auto;
    }
}
</style>

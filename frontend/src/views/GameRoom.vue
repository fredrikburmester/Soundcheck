<template>
    <div
        v-if="found"
        id="gameroom"
        :key="found"
        class="gameroom"
    >
        <div
            v-if="showQR"
            class="bigQR"
            @click="showQR = false"
        >
            <img
                :src="qr"
                @click="showQR = false"
            >
        </div>
        <div
            v-if="leaveRoomModal == true"
            :key="leaveRoomModal"
            class="leaveroom-modal"
        >
            <div>
                <h2 v-if="host" style="padding: 0 2rem 0 2rem">
                    Do you really want to end the game?
                </h2>
                <h2 v-else>
                    Do you really want to leave?
                </h2>
                <p>All progress will be lost...</p>
                <Button
                    v-if="host"
                    button-text="end game"
                    color="#CD1A2B"
                    @click="leaveRoom"
                />
                <Button
                    v-else
                    button-text="Leave room"
                    color="#CD1A2B"
                    @click="leaveRoom"
                />
                <Button
                    button-text="Go back"
                    color="#1DB954"
                    @click="toggleModal"
                />
            </div>
        </div>
        <div
            v-if="started"
            :key="started"
            class="started-grid"
            :style="startedGridStyle"
        >
            <div>
                <ProgressBar
                    :key="current_question"
                    :time="progressbarTime"
                    class="progressbar"
                />
                <h2 class="code">
                    Guess!
                </h2>
                <p class="title">
                    Who's song is this?
                </p>
                <div class="stats">
                    <p>
                        Players guessed: {{ getPlayersGuessed }} /
                        {{ players.length }}
                    </p>
                    <p>
                        Question: {{ current_question + 1 }} / {{ nr_of_questions }}
                    </p>
                </div>
            </div>
            <div id="active-list" :key="my_guess" class="list">
                <PlayerAvatar
                    v-for="player in players"
                    :id="player.id"
                    :key="player.id"
                    class="player-guess"
                    :player-name="player.name"
                    :color="player.color"
                    :host="player.host"
                    :selected="selected(player.sid)"
                    @click="guess(player)"
                />
            </div>
            <div>
                <div
                    v-if="host"
                    class="next-song"
                >
                    <Button
                        :key="current_question"
                        :button-text="(current_question + 1) == nr_of_questions ? 'Go to results' : 'next question'"
                        color="#1DB954"
                        @click="sendNextQuestion"
                    />
                </div>
                <div class="close-button">
                    <CloseButton 
                        @click="toggleModal"
                    />
                </div>
            </div>
            <iframe
                class="webplayer"
                :src="iframeurl"
                allowtransparency="true"
                allow="encrypted-media"
            />
        </div>
        <div
            v-else 
            class="lobby-grid-outer"
        >
            <div class="qr">
                <img :src="qr" @click="showQR = true">
            </div>
            <div 
                :style="lobbyGridStyle"
                class="lobby-grid"
            >
                <div>
                    <h1 class="code">
                        {{ code }}
                    </h1>
                    <div class="hr" style="margin-top: 1rem; margin-bottom: 1rem" />
                    <h3 class="title">
                        Players:
                    </h3>
                </div>
                <div class="list">
                    <PlayerAvatar
                        v-for="player in players"
                        :key="player.id"
                        :player-name="player.name"
                        :color="player.color"
                        :host="player.host"
                    />
                </div>
                <div class="buttons">
                    <p v-if="!host">
                        {{ status }}
                    </p>
                    <div class="copycode">
                        <Button
                            :key="clipboardtext"
                            color="#FFF"
                            :button-text="clipboardtext"
                            @click="copyToClipboard"
                        />
                    </div>
                    <div v-if="host" :key="host" class="startgame">
                        <Button
                            button-text="Start Game"
                            @click="startGame()"
                        />
                    </div>
                    <div class="leave">
                        <Button
                            v-if="host"
                            button-text="end game"
                            color="#CD1A2B"
                            @click="toggleModal"
                        />
                        <Button
                            v-else
                            button-text="Leave Room"
                            color="#CD1A2B"
                            @click="toggleModal"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';
import ProgressBar from '../components/ProgressBar';
import CloseButton from '../components/CloseButton';
import { nextTick } from 'vue'

const QRCode = require('qrcode');
const axios = require('axios');

export default {
    name: 'Home',
    components: {
        PlayerAvatar,
        Button,
        ProgressBar,
        CloseButton,
    },
    data: function () {
        return {
            code: this.$route.params.code,
            clipboardtext: `copy invite link`,
            status: 'Waiting for host to start the game...',
            iframeurl: '',
            settings: '',
            my_guess: '',
            qr: '',
            current_question: 0,
            nr_of_questions: 0,
            started: false,
            showQR: false,
            found: false,
            host: false,
            leaveRoomModal: false,
            players: [],
            progressbarTime: 0,
            players_guessed: [],
        };
    },
    sockets: {
        connectToRoom({
            status,
            access,
            question,
            settings,
            answers,
            questionTimeStarted,
            players_guessed,
        }) {
            console.log({
                status,
                access,
                question,
                settings,
                answers,
                questionTimeStarted,
            });
            if (status == 'lobby') {
                // join lobby
                this.generateQR();
                this.settings = settings;
                this.getTopTrack();
                this.found = true;
            } else if (status == 'playing') {
                if (access == true) {
                    // enter room
                    this.settings = settings;
                    // set current song
                    this.current_question = question;
                    this.setIframeUrl(answers[question]['info']);
                    this.nr_of_questions = answers.length;
                    this.players_guessed = players_guessed;

                    // Set progressbar progression
                    var unixTime = Date.now().toString();
                    unixTime = unixTime.substring(0, unixTime.length - 3);

                    var diff = unixTime - questionTimeStarted + 1;
                    if (diff > 30) {
                        this.progressbarTime = 1;
                    } else {
                        this.progressbarTime = diff / 30;
                    }

                    this.started = true;
                    this.found = true;
                } else {
                    // set error
                    this.$store.commit(
                        'updateError',
                        'Game has already started!'
                    );
                    // go to join
                    this.$router.push('/join');
                }
            } else if (status == 'ended') {
                // game has ended
                this.$router.push(`/${this.code}/results`);
            } else if (status == 'NaR') {
                // Room does not exist
                // set error
                this.$store.commit('updateError', 'That room does not exist!');
                // go to join
                this.$router.push('/join');
            }
        },
        update_list_of_players({ players }) {
            this.players = players;
            this.isHost();
        },
        room_closed_by_host() {
            this.started = false;
            this.status = 'Host ended the game...';
            this.players = [];
            this.$store.commit('clearPlayersGuessed');
        },
        nr_of_players_guessed(data) {
            this.players_guessed = data.players; // set the array of players who have guessed
        },
        next_question(data) {
            // Set the current question and reset the progressbar
            this.current_question = data.current_question;
            this.progressbarTime = 0;

            // If the current question is -1 then the game is ending and we show a loading screen and await the "game_ended" socket
            if (data.current_question == '-1') {
                // this.loading = true;
            } else {
                this.setIframeUrl(data.trackid); // Set the song in the iframe
                this.my_guess = ''; // Reset the guess
            }

            // Reset number of players guessed
            this.players_guessed = [];
        },
        game_ended() {
            // this.loading = true;
            // this.$router.push(`/${this.code}/results`);
        },
        start_game(data) {
            this.nr_of_questions = data.nr_of_questions;
            this.started = true;
        },
    },
    computed: {
        getPlayersGuessed() {
            return this.players_guessed.length;
        },
        lobbyGridStyle() {
            if(this.host) {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '125px auto 210px'
                }
            } else {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '125px auto 190px'
                    
                };
            }
        },
        startedGridStyle() {
            if(this.host) {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '125px auto 70px 80px'
                }
            } else {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '125px auto 0px 80px'
                    
                };
            }
        },
    },
    mounted: function () {
        this.connectToRoom();
    },
    methods: {
        toggleModal() {
            this.leaveRoomModal = !this.leaveRoomModal;
        },
        async copyToClipboard() {
            await navigator.clipboard.writeText(window.location.href);
            this.clipboardtext = 'copied!';
        },
        connectToRoom() {
            var access_token = this.$store.getters.getAccessToken;
            var refresh_token = localStorage.getItem('refresh_token');
            this.$socket.client.emit('connect_to_room', {
                code: this.code,
                sid: this.$store.getters.getSid,
                access_token: access_token,
                refresh_token: refresh_token,
            });
        },
        generateQR() {
            var self = this;
            QRCode.toDataURL(
                `https://soundcheck.fdrive.se/${this.code}`, {scale: 30, margin: 1, color: {dark: '#eee', light: '#191414'}}, 
                function (err, url) {
                    self.qr = url;
                }
            );
        },
        isHost() {
            var self = this;
            this.players.forEach((player) => {
                if (player.sid == this.$store.getters.getSid) {
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
            // Send next question
            this.$socket.client.emit('next_question', {
                code: this.code,
            });
        },
        async guess(player) {
            var pos = document.getElementById('active-list')
            var pos = pos.scrollTop

            this.my_guess = player.sid;
            this.$socket.client.emit('player_guess', {
                sid: this.$store.getters.getSid,
                code: this.code,
                guess: this.my_guess,
            });

            await nextTick()
            document.getElementById('active-list').scrollTop = pos
        },
        selected(id) {
            if (id == this.my_guess) {
                return true;
            }
            return false;
        },
        setIframeUrl(id) {
            this.iframeurl = `https://open.spotify.com/embed?uri=spotify:track:${id}`;
        },
        leaveRoom() {
            this.$socket.client.emit('leave_room', {
                code: this.code,
                sid: this.$store.getters.getSid,
            });
            this.$router.push('/');
        },
        getTopTrack() {
            var self = this;
            var token = this.$store.getters.getAccessToken;

            var time_range = this.settings[0];
            var no_songs = this.settings[1];

            axios
                .get(
                    `https://api.spotify.com/v1/me/top/tracks?time_range=${time_range}&limit=${no_songs}`,
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
                                `https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=${no_songs}`,
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
                                    var trackid = [];
                                    for (var i = 0; i < no_songs; i++) {
                                        trackid.push(
                                            response.data.items[0].uri.split(
                                                ':'
                                            )[2]
                                        );
                                    }
                                    self.$socket.client.emit('toptrack', {
                                        trackid: trackid,
                                        sid: self.$store.getters.getSid,
                                        room: self.code,
                                    });
                                }
                            });
                    } else {
                        var trackid = [];
                        for (var i = 0; i < no_songs; i++) {
                            trackid.push(
                                response.data.items[i].uri.split(':')[2]
                            );
                        }
                        self.$socket.client.emit('toptrack', {
                            trackid: trackid,
                            sid: self.$store.getters.getSid,
                            room: self.code,
                        });
                    }
                });
        },
    },
};
</script>

<style scoped>
.gameroom {
    display: grid;
}
.lobby-grid-outer {
    display: grid;
}
.lobby-grid {
    display: grid;
    grid-template-rows: minmax(160px,170px) auto minmax(0px, 220px);
}
.started-grid {
    display: grid;
    grid-template-rows: 140px auto minmax(0px, 70px) 80px;
    height: 99vh;
}
.buttons {
    margin-top: 20px;
    margin-bottom: 20px;
    margin-right: 2rem;
    margin-left: 2rem;
    
}
.buttons p {
    margin-top: 0;
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
}
.stats {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    text-align: center;
    color: darkgrey;
    margin-left: 2rem;
    margin-right: 2rem;
    margin-top: 0;
    margin-bottom: 20px;
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 0 2rem 0 2rem;
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
    margin-left: 2rem;
    margin-right: 2rem;
    /* height: 100%; */
    overflow: scroll;
    border-color: aquamarine;
    border-bottom: 1px solid gray;
}
.webplayer {
    height: 80px;
    width: 100vw;
}
.progressbar {
    position: fixed;
    top: 90px;
    width: calc(100vw - 4rem);
    margin-left: 50%;
    transform: translateX(-50%);
}
.progressbar {
    height: 5px !important;
    overflow: hidden;
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
/* .loading {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background-color: rgba(0, 0, 0, 0.832);
    display: grid;
    place-items: center;
    z-index: 2;
} */
.leaveroom-modal {
    display: grid;
    place-items: center;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background-color: black;
    z-index: 2;
}
.close-button {
    position: fixed;
    top: 30px;
    right: 2rem;
}
.next-song {
    margin-top: 10px;
    margin-right: 2rem;
    margin-left: 2rem;
}
@media only screen and (min-width: 700px) {
    .bigQR > img {
    width: 45vw;
    height: auto;
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    }
}
@media only screen and (min-width: 1100px) {
    .bigQR > img {
    width: 30vw;
    height: auto;
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    }
}
</style>

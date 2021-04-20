<template>
    <div v-if="found" :key="found" class="gameroom">
        <div v-if="started" :key="started">
            <ProgressBar class="progressbar" />
            <h1>Guess who this song belongs to!</h1>
            <div class="list">
                <PlayerAvatar
                    v-for="player in players"
                    v-bind:key="player.id"
                    :playerName="player.name"
                    :color="player.color"
                    :host="player.host"
                    @onclick="guess(player)"
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
            <p v-if="!host">{{status}}</p>
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
                <img :src="qr" />
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
                        v-on:click="closeRoom"
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

// const io = require('socket.io-client');
// var socket;

// if (process.env.NODE_ENV == 'production') {
//     socket = io('https://musicwithfriends.fdrive.se', {
//         path: '/ws/socket.io',
//     });
// } else {
//     socket = io('localhost:5000');
// }

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
            currentSong: 0,
            iframeurl: '',
            started: false,
            players: [],
            colors: [],
            status: 'Waiting for host to start the game...',
            found: false,
            host: false,
            code: this.$route.params.code,
            qr: '',
        };
    },
    sockets: {
        not_a_room() {
            this.$router.push('/join');
        },
        new_track(data) {
            console.log(data);
            this.setIframeUrl(data.trackid);
        },
        start_game() {
            console.log('Game starting!');
            this.started = true;
            this.nextTrack();
        },
        top_tracks_list(data) {
            console.log(data.top_tracks_list);
        },
        close_room() {
            this.status = "The host has ended the game!"
            this.players = []
            // this.$router.push('/join');
        },
        list_of_players(data) {
            console.log('list_of_players', this.players);
            this.players.length = 0;
            var self = this;
            data.players.forEach((player) => {
                if (player.sid == localStorage.getItem('sid')) {
                    if (player.host == true) {
                        self.host = true;
                    }
                }
                self.players.push(player);
            });
            self.found = true;
        }
    },
    methods: {
        async copyToClipboard() {
            await navigator.clipboard.writeText(window.location.href);
            this.clipboardtext = 'copied!';
        },
        leaveRoom: function () {
            this.$socket.client.emit('leave_room', {
                code: this.code,
                sid: localStorage.getItem('sid')
            });
            this.$router.push('/');
        },
        closeRoom: function() {
            this.$socket.client.emit('close_room', {
                code: this.code,
            });
            this.$router.push('/');
        },
        setIframeUrl(id) {
            this.iframeurl = `https://open.spotify.com/embed?uri=spotify:track:${id}`;
        },
        startGame() {
            this.$socket.client.emit('start_game', { code: this.code });
        },
        nextTrack() {
            if (this.currentSong < this.players.length) {
                console.log('Current Song:', this.currentSong);
                this.$socket.client.emit('next_song', {
                    track_nr: this.currentSong,
                    code: this.code,
                });
                this.currentSong += 1;
                setTimeout(this.nextTrack(), 5000);
            } else {
                //game end
            }
        },
        guess(player) {
            console.log(`You guessed on ${player.name}`);
        },
        joinedRoom() {
            this.$socket.client.emit('joinRoom', {
                access_token: localStorage.getItem('access_token'),
                refresh_token: localStorage.getItem('refresh_token'),
                code: this.code,
                sid: localStorage.getItem('sid'),
            });
        }
    },

    computed: {},
    mounted: function () {
        var self = this;

        QRCode.toDataURL(
            `https://musicwithfriends.fdrive.se/${this.code}`,
            function (err, url) {
                self.qr = url;
            }
        );

        this.joinedRoom()

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
                var trackid = response.data.items[0].uri.split(':')[2];
                self.$socket.client.emit('toptrack', {
                    trackid: trackid,
                    sid: localStorage.getItem('sid'),
                    room: self.code,
                });
            });
    },
};
</script>

<style scoped>
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
}
.copycode {
    position: fixed;
    left: 50%;
    bottom: 90px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
}
.leave {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
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
</style>

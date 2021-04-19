<template>
    <div v-if="found" class="gameroom">
        <div v-if="started">
            <ProgressBar class="progressbar" />
            <h1>Guess who this song belongs to!</h1>
            <div class="list">
                <PlayerAvatar
                    v-for="player in players"
                    v-bind:key="player.id"
                    :playerName="player.name"
                    :color="player.color"
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
            <h1 v-if="host" :key="host">Start game</h1>
            <h1 v-else>Waiting for host to start game</h1>
            <p>{{ code }}</p>
            <div class="list">
                <PlayerAvatar
                    v-for="player in players"
                    v-bind:key="player.id"
                    :playerName="player.name"
                    :color="player.color"
                />
            </div>
            <div class="copycode">
                <p>Click to copy</p>
                <Button
                    @click="copyToClipboard"
                    color="#FFF"
                    :buttonText="clipboardtext"
                    :key="clipboardtext"
                ></Button>
            </div>

            <div class="qr">
                <img :src="qr" />
            </div>
            <div v-if="host" :key="host" class="startgame">
                <Button @click="startGame()" buttonText="Start Game"></Button>
            </div>
            <div class="leave">
                <Button
                    v-on:click="leaveRoom"
                    buttonText="Leave Room"
                    color="#CD1A2B"
                />
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

const io = require('socket.io-client');
var socket;

if(process.env.NODE_ENV == 'production') {
    socket = io('https://musicwithfriends.fdrive.se', {
        path: '/ws/socket.io',
    });
} else {
    socket = io();
}

export default {
    name: 'Home',
    components: {
        PlayerAvatar,
        Button,
        ProgressBar,
    },
    data: function () {
        return {
            players: [],
            colors: [],
            found: false,
            qr: '',
            code: this.$route.params.code,
            clipboardtext: `copy invite link`,
            started: false,
            iframeurl: '',
            host: false,
            currentSong: 0,
        };
    },
    methods: {
        leaveRoom: function () {
            socket.emit('leave_room', {
                code: this.code,
            });
            this.$router.push('/');
        },
        async copyToClipboard() {
            await navigator.clipboard.writeText(window.location.href);
            this.clipboardtext = 'copied!';
        },
        setIframeUrl(id) {
            this.iframeurl = `https://open.spotify.com/embed?uri=spotify:track:${id}`;
        },
        startGame() {
            socket.emit('start_game', { code: this.code });
        },
        nextTrack() {
            if (this.currentSong < this.players.length) {
                console.log('Current Song:', this.currentSong);
                socket.emit('next_song', {
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

        socket.emit('joinRoom', {
            access_token: localStorage.getItem('access_token'),
            refresh_token: localStorage.getItem('refresh_token'),
            code: this.code,
            sid: localStorage.getItem('sid'),
        });

        socket.on('not_a_room', () => {
            self.$router.push('/join');
        });

        socket.on('new_track', (data) => {
            console.log(data);
            self.setIframeUrl(data.trackid);
        });

        socket.on('start_game', () => {
            console.log('Game starting!');
            self.started = true;
            this.nextTrack();
        });

        socket.on('top_tracks_list', (data) => {
            console.log(data.top_tracks_list);
        });

        socket.on('listofplayers', (data) => {
            console.log('listofplayers', self.players);
            self.players.length = 0;
            data.players.forEach((player) => {
                if (player.sid == localStorage.getItem('sid')) {
                    if (player.host == true) {
                        self.host = true;
                    }
                }
                self.players.push(player);
            });
            self.found = true;
        });

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
                var trackid = response.data.items[0].uri;
                trackid = trackid.split(':');
                trackid = trackid[2];
                socket.emit('toptrack', {
                    trackid: trackid,
                    sid: localStorage.getItem('sid'),
                    room: self.code,
                });
            });
    },
};
</script>

<style scoped>
.QR {
    transform: scale(0.5);
    border: 5px solid rgb(255, 255, 255);
}
.leave {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
}
.copycode {
    position: fixed;
    left: 50%;
    bottom: 240px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
}
.qr {
    width: auto;
    height: 300px;
    height: auto;
    position: fixed;
    left: 50%;
    bottom: 50px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
}
.list {
    height: 200px;
    overflow: scroll;
    padding-left: 1em;
    padding-right: 1em;
}
.startgame {
    position: fixed;
    left: 50%;
    bottom: 370px;
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

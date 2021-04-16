<template>
    <div v-if="found" class="home">
        <h1>Room</h1>
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
        <div class="leave">
            <Button
                v-on:click="leaveRoom"
                buttonText="Leave Room"
                color="#CD1A2B"
            />
        </div>
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';

const QRCode = require('qrcode');

const io = require('socket.io-client');
// const socket = io("https://musicwithfriends.fdrive.se");
const socket = io('https://musicwithfriends.fdrive.se', {
    path: '/ws/socket.io',
});

export default {
    name: 'Home',
    components: {
        PlayerAvatar,
        Button,
    },
    data: function () {
        return {
            players: [],
            colors: [],
            found: false,
            qr: '',
            code: this.$route.params.code,
            clipboardtext: `copy invite link`,
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
        });

        socket.on('not_a_room', () => {
            self.$router.push('/join');
        });

        // socket.on('playerJoined', (data) => {
        //     console.log('Player joined:', data.player.name);
        //     var found = false;
        //     self.players.forEach((player) => {
        //         if (player.name == data.player.name) found = true;
        //     });
        //     if (!found) self.players.push(data.player);
        // });

        socket.on('listofplayers', (data) => {
            console.log('listofplayers', self.players);
            self.players.length = 0;
            data.players.forEach((player) => {
                self.players.push(player);
            });
            self.found = true;
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
    height: calc(100vh - 40vw - 228px);
}
</style>

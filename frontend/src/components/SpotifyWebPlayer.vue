<template>
    <div id="spotify-web-player-div">
        Hej
        <button @click="playSong('spotify:track:3XVBdLihbNbxUwZosxcGuJ')">
            Play song
        </button>
        <button @click="togglePlay()">
            Toggle Play
        </button>
        <button @click="player.pause()">
            Pause
        </button>
        <button @click="player.pause()">
            Play
        </button>
    </div>
</template>

<script>
//import * as external from '@/assets/external.js'

export default {
    name: 'SpotifyWebPlayer',
    data() {
        return {
            device_id: '',
            player: null,
            token: this.$store.getters.getAccessToken
        }
    },
    async mounted() {
        var self = this;

        window.onSpotifyWebPlaybackSDKReady = () => {
            const player = new Spotify.Player({
                name: 'Soundcheck',
                getOAuthToken: cb => { cb(self.token); },
                volume: 0.5
            });

            self.player = player

            player.addListener('initialization_error', ({ message }) => { console.error(message); });
            player.addListener('authentication_error', ({ message }) => { console.error(message); });
            player.addListener('account_error', ({ message }) => { console.error(message); });
            player.addListener('playback_error', ({ message }) => { console.error(message); });
    
            // Playback status updates
            player.addListener('player_state_changed', state => { console.log(state); });
     
            // Ready
            player.addListener('ready', ({ device_id }) => {
                console.log('Ready with Device ID', device_id);
                self.device_id = device_id
            });
    
            // Not Ready
            player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID has gone offline', device_id);
            });
    
            // Connect to the player!
            player.connect();

        }
    },
    methods: {
        playSong (spotify_uri) {
            var self = this
            fetch(`https://api.spotify.com/v1/me/player/play?device_id=${self.device_id}`, {
                method: 'PUT',
                body: JSON.stringify({ 
                    context_uri: "spotify:album:5ht7ItJgpBH7W6vJ5BqpPr",
                    offset: {
                        position: 5
                    },
                    position_ms: 0
                 }),
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer self.token`
                },
            })
        },
        async togglePlay() {
            this.player.togglePlay().then(() => {
                console.log('Toggled playback!');
            });
        },
        async nextTrack() {
            this.player.nextTrack().then(() => {
                console.log('Toggled playback!');
            });
        },
    }
}
</script>


<style scoped>
</style>

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
        //const token = 'BQCXLYNjMKB9lU6-S5pwRyOqKpkWdG-ACvHujZGbwFmWLB-ekX2AnEsKPN-KnMQ9UQA2zhKOA9DlNMoT8xhxCY4XCpUI3SKm4ntaQJfOOPrs0vCC_s_usj_33FuFQqwa_MSI_smF3dlcUcInogbFcpg2Tcs39PzAeqVAN27NnoaCxeQqJMxFbndCw9G2j0ggSr9j5473w0PslyRkzqq2b3IQ8kWWr2oSMQmRbWBBBJO1It-UnroiOgMf4n6VDqJbo3ITqvd2uUMrXLBX6ZHs4w'

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
                    'Authorization': `Bearer BQAqDWlUdWmTr3MWHiFpWDGPxosk_EJEJwlbvYjlISIiwBGSTHamvXhBf3_PofYDGKJsisWjytGbPol3DxGaOq6GRgzGsJnDs1YYcQg8aeRku99Jy7gi4m3ddN8XqYjnW45uKJ1JLU7We5x4X_1wLshtiuUWv38Hwoq_EnvHvPYShnT5aZevt_MIoqc2drjOk0dbb9n9iSxsVJ7yxLTXSbHyuOO9m682pTqxcoYMhYYHVKmq71ZlzGEBW3nn89lsrBplupJgEv6FgrDdPZ6t_A`
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
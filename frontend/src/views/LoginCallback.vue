/* 
After authenticating with Spotify, the client is directed to this page which saves the recieved token and request a 
new spotify API token from our server.   
 */

<template>
    <Loader />
</template>

<script>
import Loader from '../components/Loader'
import { Browser } from '@capacitor/browser';

export default {
    name: 'LoginCallback',
    components: {
        Loader
    },
    sockets: {
    },
    async mounted() {
        this.getToken()
    },
    methods: {
        getToken: function() {
            let uri = window.location.href.split('=')[1];
            let code = uri.split('&')[0];

            this.$socket.client.emit('generate_access_token', { code: code, sid: this.$store.getters.getSid });

            //this.closeCapacitorBrowser()
        },
        closeCapacitorBrowser: async function() {
            await Browser.close();
        }
    },
};
</script>

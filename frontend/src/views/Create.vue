/*
View for creating a game room. This view have settings that are sent to the server, returned from the server is the game room code. 
 */

<template>
    <div class="create">
        <h1 class="head">
            Room settings
        </h1>
        <div class="hr" />
        
        <div class="container">
            <h3>Select Time Range</h3>
            <Select :list="timeRanges" :default-value="timeRanges[0]" @selected="setTimeRange" />
           
            <h3>Number of songs per player</h3>
            <Select :list="nrOfSongsArray" :default-value="nrOfSongsArray[0]" @selected="setNrOfSongs" />
           
            <br>
            <br>

            <Button
                button-text="Create Room"
                @click="createRoom"
            />

            <div class="button-container">
                <div class="back">
                    <Button
                        button-link="/"
                        button-text="Back"
                        color="#CD1A2B"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Button from '../components/Button';
import Select from '../components/Select';

export default {
    name: 'Create',
    components: {
        Button,
        Select,
    },
    sockets: {
        // When the server has created the room, the client is pushed to the url by this function. 
        roomCode(data) {
            this.$router.push(data.code);
        },
    },
    data() {
        return {
            no_songs: 1,
            time_range: 'short_term', 
            // Time rages are specific to the spotify API and not chosen by us. 
            timeRanges: [
                {value: '4 weeks', key: 'short_term'},
                {value: '6 months', key: 'medium_term'},
                {value: 'Over a year', key: 'long_term'} 
            ],
            nrOfSongsArray: Array.from({length: 20}, (_, i) => i + 1)
        };
    },
    methods: {
        // After setting all settings, they are sent to the server. 
        createRoom: function () {
            this.$socket.client.emit('createRoom', {
                sid: this.$store.getters.getSid,
                time_range: this.time_range,
                no_songs: this.no_songs,
            });
        },
        setTimeRange(value) {
            this.time_range = value
        },
        setNrOfSongs(value) {
            this.no_songs = value
        }
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.head {
    display: inline-block;
    margin: 10px 0 10px 0;
}
.create {
    margin-top: 0;
    display: grid;
    padding: 0 2rem 0 2rem;
}

.hr {
    margin-left: auto;
    margin-right: auto;
    width: 80vw;
    height: 2px;
    background-color: rgb(63, 63, 63);
}
.drop-down{
    background-color: #fff;
    font-weight: 400;
    border: 1px solid #000;
    border-radius: 100px;
    height: 47px;
    text-align-last: center;
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    margin-bottom: 10px;

    /* Width and center*/ 
    width: 100%;
    max-width: 340px;
    /* --------------- */ 

    -webkit-appearance: none;
}
.button-container {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    width: 100vw;
}
.back {
    padding: 0 2rem 0 2rem;
}
.drop-down:focus{
    outline: none;
}
</style>

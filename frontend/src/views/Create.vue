<template>
    <div class="create">
        <h1 class="head">
            Settings
        </h1>
        <div class="hr" />
        
        <div class="container">
            <h3>Select Time Range</h3>
            <select v-model="time_range" class="drop-down">
                <option v-for="option in options" :key="option.value" :value="option.value">
                    {{ option.text }}
                </option>
            </select>
            
            <h3>Number of songs per player</h3>
            <select v-model="no_songs" class="drop-down"> 
                <option v-for="n in 8" :key="n">
                    {{ n }}
                </option>
            </select>
            <br>
            <br>
            <Button
                button-text="Create Room"
                @click="createRoom"
            />
            <Button
                button-link="/"
                button-text="Back"
                color="#CD1A2B"
            />
        </div>
    </div>
</template>

<script>
import Button from '../components/Button';
import SettingsButton from '../components/SettingsButton';
//import ToggleSwitch from '../components/ToggleSwitch';

export default {
    name: 'Create',
    components: {
        Button,
        SettingsButton,
        // ToggleSwitch,
    },
    sockets: {
        roomCode(data) {
            this.$router.push(data.code);
        },
    },
    data() {
        return {
            no_songs: 1,
            time_range: 'short_term',
            options: [
                {text: '4 weeks', value: 'short_term'},
                {text: '6 months', value: 'medium_term'},
                {text: 'Over a year', value: 'long_term'} 
            ]
        };
    },
    methods: {
        createRoom: function () {
            this.$socket.client.emit('createRoom', {
                sid: localStorage.getItem('sid'),
                time_range: this.time_range,
                no_songs: this.no_songs,
            });
        },
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.head {
    display: inline-block;
}
.create {
    margin-top: 0;
    display: grid;
}

.hr {
    margin-left: auto;
    margin-right: auto;
    width: 80vw;
    height: 2px;
    background-color: rgb(63, 63, 63);
}

.container{
    height: 80vh;
    padding-bottom: 80px;
    overflow-y: scroll;
    overflow-x: hidden;
}

.drop-down{
    display: inline-block;
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    letter-spacing: 1px;
    border-radius: 100px;
    width: 50vw;
    padding: 15px 20px 15px 20px;
    text-align-last: center;
    cursor: pointer;
    margin-bottom: 10px;
    font-variant: small-caps;
    background-color: white;
}
.drop-down:focus{
    outline: none;
}
</style>

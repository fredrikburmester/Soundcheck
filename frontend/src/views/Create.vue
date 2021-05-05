<template>
    <div class="create">
        <h1 class="head">
            Room settings
        </h1>
        <div class="hr" />
        <div class="settingsbox">
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
// import SettingsButton from '../components/SettingsButton';
//import ToggleSwitch from '../components/ToggleSwitch';

export default {
    name: 'Create',
    components: {
        Button,
        // SettingsButton,
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
    margin: 10px 0 10px 0;
}
.create {
    margin-top: 0;
    display: grid;
    padding: 0 2rem 0 2rem;
}

.settingsbox {
    height: calc(100vh - 160px);
    overflow-y: scroll;
    overflow-x: hidden;
    padding-bottom: 100px;
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
option{
    font-size: 16px;
    font-family: 'Roboto', sans-serif;
}
</style>

<template>
    <div class="create">
        <h1 class="head">
            Settings
        </h1>
        <div class="hr" />
        <div class="settingsbox">
            <h3>Select Time Range</h3>
            <!-- <Button
                button-text="last 4 weeks"
                @click="onTimeChange(`4 weeks`)"
            />
            <Button
                button-text="last 6 months"
                @click="onTimeChange(`6 months`)"
            />
            <Button
                button-text="more than a year"
                @click="onTimeChange(`More than a year`)"
            /> -->
            <div class="v-model-select">
                <select v-model="time_range" class="drop-down">
                    <option v-for="option in options" :key="option.value" :value="option.value">
                        {{ option.text }}
                    </option>
                </select>
            </div>

            <div style="padding-bottom: 20px">
                <h3>Number of songs per player</h3>
                <div class="v-model-select">
                <select v-model="no_songs" class="drop-down"> 
                    <option v-for="n in 8" :key="n">{{ n }}</option>
                </select>
                <br>
                <br>
                <span> {{ no_songs }} songs </span>
            </div>
            </div>

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
.v-model-select{
    font-family: 'Roboto', sans-serif;
    width: 80vw;
    display: inline-block;
    padding: 15px 30px;
    margin-top: 1em;
    margin-bottom: 20px;
    overflow-x: auto;
}
.drop-down{
    background-color: #fff;
    width: 55vw;
    height: 47px;
    text-align-last: center;
    display: inline;
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    border: 2px solid #eee;
    border-radius: 100px;
    cursor: pointer;
}
option{
    align-items: center;
}
</style>

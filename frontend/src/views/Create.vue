<template>
    <div class="create">
        <h1 class="head">Settings</h1>
        <div class="hr"></div>
        <div class="settingsbox">
            <h3>Select Time Range</h3>
            <Button @click="onTimeChange(`4 weeks`)"  buttonText="last 4 weeks"></Button>
            <Button @click="onTimeChange(`6 months`)" buttonText="last 6 months"></Button>
            <Button @click="onTimeChange(`More than a year`)" buttonText="more than a year"></Button>
            <p>Time range: {{time_range}}</p>
            
            <h3>Number of songs per player</h3>
            <SettingsButton @clicked="onClickChild" :marked="1==no_songs" v-bind:key="no_songs" buttonText="1"/>
            <SettingsButton @clicked="onClickChild" :marked="2==no_songs" v-bind:key="no_songs" buttonText="2"/>
            <SettingsButton @clicked="onClickChild" :marked="3==no_songs" v-bind:key="no_songs" buttonText="3"/>
            <SettingsButton @clicked="onClickChild" :marked="4==no_songs" v-bind:key="no_songs" buttonText="4"/>
            
            <h3> Include Top Genre </h3>
            <ToggleSwitch @clicked="onToggleChild"/>    
            <br>
            <Button v-on:click="createRoom" buttonText="Start Game"></Button>
            <Button buttonLink="/" buttonText="Back" color="#CD1A2B"></Button>
        </div>
    </div>
</template>

<script>
import Button from '../components/Button';
import SettingsButton from '../components/SettingsButton';
import ToggleSwitch from '../components/ToggleSwitch'

export default {
    name: 'Create',
    components: {
        Button,
        SettingsButton,
        ToggleSwitch,
    },
    sockets: {
        roomCode(data) {
            this.$router.push(data.code);
        },
    },
    data(){
        return{
            no_songs: 0,
            time_range: '4 weeks',
        }
    },
    methods: {
        createRoom: function () {
            this.$socket.client.emit('createRoom', {
                sid: localStorage.getItem('sid'),
            });
        },
        onClickChild(value){
            this.no_songs = value
            this.$store.commit('update_no_songs', this.no_songs);
        },
        onToggleChild(value){
            this.$store.commit('update_genre', value);
        },
        onTimeChange(value){
            this.time_range = value
            if(value == '4 weeks') this.$store.commit('update_time_range', 'short_term');
            else if(value == '6 months') this.$store.commit('update_time_range', 'medium_term');
            else if(value == 'More than a year') this.$store.commit('update_time_range', 'long_term');
        }
    },
};
</script>

<style scoped>
.head{
    display: inline-block;
 }
.create {
    margin-top: 3vh;
}

.settingsbox{
    height: calc(100vh - 190px);
    overflow-y: scroll;
    overflow-x: hidden;
    
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 0.5rem 2rem 0.5rem 2rem;
}
@media only screen and (min-width: 900px) {
    .settingsbox{
        margin-top: 15vh;
        overflow: hidden;
    }
}
</style>

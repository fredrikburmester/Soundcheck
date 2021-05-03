<template>
    <div class="create">
        <h1 class="head">
            Settings
        </h1>
        <div class="hr" />
        <div class="settingsbox">
            <h3>Select Time Range</h3>
            <Button
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
            />
            <p>Time range: {{ time_range }}</p>

            <div style="padding-bottom: 20px">
                <h3>Number of songs per player</h3>
                <SettingsButton
                    :key="no_songs"
                    :marked="1 == no_songs"
                    button-text="1"
                    @clicked="onClickChild"
                />
                <SettingsButton
                    :key="no_songs"
                    :marked="2 == no_songs"
                    button-text="2"
                    @clicked="onClickChild"
                />
                <SettingsButton
                    :key="no_songs"
                    :marked="3 == no_songs"
                    button-text="3"
                    @clicked="onClickChild"
                />
                <SettingsButton
                    :key="no_songs"
                    :marked="4 == no_songs"
                    button-text="4"
                    @clicked="onClickChild"
                />
            </div>

            <!-- <h3>Include Top Genre</h3>
            <ToggleSwitch @clicked="onToggleChild" />-->

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
import ToggleSwitch from '../components/ToggleSwitch';

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
            no_songs: 0,
            time_range: '4 weeks',
        };
    },
    methods: {
        createRoom: function () {
            this.$socket.client.emit('createRoom', {
                sid: localStorage.getItem('sid'),
                time_range: this.$store.state.time_range,
                no_songs: this.$store.state.no_songs,
            });
        },
        onClickChild(value) {
            this.no_songs = value;
            this.$store.commit('update_no_songs', this.no_songs);
        },
        onToggleChild(value) {
            this.$store.commit('update_genre', value);
        },
        onTimeChange(value) {
            this.time_range = value;
            if (value == '4 weeks')
                this.$store.commit('update_time_range', 'short_term');
            else if (value == '6 months')
                this.$store.commit('update_time_range', 'medium_term');
            else if (value == 'More than a year')
                this.$store.commit('update_time_range', 'long_term');
        },
    },
};
</script>

<style scoped>
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
@media only screen and (min-width: 900px) {
    /* .settingsbox{
        margin-top: 15vh;
        overflow: hidden;
    } */
}
</style>

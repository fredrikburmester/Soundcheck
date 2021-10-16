/*
Page for joining a room by entering a room code. 
 */

<template>
    <div class="join">
        <h1>Enter room code...</h1>
        <p style="color: rgba(205,26,43,1)">{{ error }}</p>
        <InputField 
            class="input"
            :text="code"
            placeholder="ABCD"
            @keyup="enterPress"
        />
        <Button
            button-text="Join Room"
            @click="isRoom"
        />
        <br>
        <h2 style="color: rgba(255, 255, 255, 0.5)">
            Or...
        </h2>
        <h3>Scan QR-code in your camera app</h3>
        <div class="back-container">
            <div class="back">
                <Button
                    button-link="/"
                    button-text="Back"
                    color="#CD1A2B"
                />
            </div>
        </div>
    </div>
</template>

<script>
import Button from '../components/Button';
import InputField from '../components/InputField';

export default {
    name: 'Join',
    components: {
        Button,
        InputField,
    },
    data() {
        return {
            error: this.$store.state.error,
        };
    },
    sockets: {
        // If the room exists the person is pushed to the room url. Otherwise an error message is displayed.
        isRoom(data) {
            if (data.isRoom == 'true' || data.isRoom == true) {
                this.$router.push(this.code);
            } else {
                this.$store.commit('updateError', 'Room does not exist!');
                this.error = 'Room does not exist!';
            }
        },
    },
    computed: {
        code() {
            return this.$store.state.roomCode;
        },
    },
    methods: {
        // Before joining, the client checks with the server if the room exists. 
        isRoom: function () {
            this.$socket.client.emit('isRoom', { code: this.code });
        },
        enterPress: function(e){
            if(e.keyCode == 13){
                this.isRoom();
            }
        }
    },
};
</script>

<style scoped>
.join {
    margin-top: 10vh;
    margin-left: 2rem;
    margin-right: 2rem;
}
.back-container {
    position: fixed;
    left: 50%;
    bottom: 15px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    width: 100vw;
}
.back {
    padding: 0 2rem 0 2rem;
}
@media only screen and (min-height: 550px) {
    .join {
        margin-top: 20vh;
    }
}
@media only screen and (min-height: 680px) {
    .join {
        margin-top: 30vh;
    }
}
</style>

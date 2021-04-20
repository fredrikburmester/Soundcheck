<template>
    <div class="join">
        <h1>Enter room code...</h1>
        <p>{{ error }}</p>
        <InputField :text="code" placeholder="ABCD" />
        <Button @click="isRoom" buttonText="Join Room" />
        <br />
        <h2 style="color: rgba(255, 255, 255, 0.5)">Or...</h2>
        <h3>Scan QR-code in your camera app</h3>
        <div class="back">
            <Button buttonLink="/" buttonText="Back" color="#CD1A2B" />
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
            error: '',
        };
    },
    sockets: {
        isRoom(data) {
            if (data.isRoom == 'true' || data.isRoom == true) {
                this.$router.push(this.code);
            } else {
                this.error = 'Room does not exist';
            }
        },
    },
    methods: {
        isRoom: function () {
            this.$socket.client.emit('isRoom', { code: this.code });
        },
    },
    computed: {
        code() {
            return this.$store.state.roomCode;
        },
    },
};
</script>

<style scoped>
.join {
    margin-top: 30vh;
}
.back {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
}
</style>

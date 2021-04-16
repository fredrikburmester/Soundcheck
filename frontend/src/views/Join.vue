<template>
    <div class="join">
        <h1>Enter room code...</h1>
        <!-- <input v-model="code" placeholder="Enter Room Code..."> -->
        <InputField @input="updateCode" placeholder="ABCD" />
        <Button :buttonLink="code_" buttonText="Join Room" />
        <br />
        <h1>Or...</h1>
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
    props: {
        code: {
            type: String,
            default: '/',
        },
    },
    data() {
        return {
            code_: this.code,
        };
    },
    components: {
        Button,
        InputField,
    },
    methods: {
        updateCode(value) {
            if (value.inputType == 'deleteContentBackward') {
                this.code_ = this.code_.slice(0, -1);
            } else {
                this.code_ += value.data;
            }
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

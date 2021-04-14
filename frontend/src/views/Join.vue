<template>
  <div class="join">
    <h1>Enter room code...</h1>
    <!-- <input v-model="code" placeholder="Enter Room Code..."> -->
    <InputField @input="updateCode" placeholder="ABCD" />
    <Button :buttonLink="code_" buttonText="Join Room" />
    <br />
    <h1>Or...</h1>
    <h1>Scan QR-code</h1>
    <Button buttonLink="/" buttonText="Back" />
  </div>
</template>

<script>
import Button from "../components/Button";
import InputField from "../components/InputField";

export default {
  name: "Join",
  props: {
    code: {
      type: String,
      default: "/",
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
      console.log(value);
      if (value.inputType == "deleteContentBackward") {
        this.code_ = this.code_.slice(0, -1);
      } else {
        this.code_ += value.data;
      }
      console.log(this.code_);
    },
  },
};
</script>

<style scoped>
.join {
  margin-top: 20vh;
}
</style>

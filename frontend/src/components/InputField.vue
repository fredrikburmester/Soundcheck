<template>
  <input
    id="input"
    v-model="text_"
    type="text"
    :placeholder="placeholder_"
    @input="sendValue()"
  >
</template>

<script>
export default {
    name: 'InputField',
    props: {
        placeholder: {
            type: String,
            default: ''
        },
        text: {
            type: String,
            default: ''
        },
    },
    data() {
        return {
            placeholder_: this.placeholder,
            text_: this.text,
        };
    },
    methods: {
        sendValue: function () {
            this.$store.commit('updateRoomCode', this.text_);
        },
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
input {
    display: inline-block;
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    letter-spacing: 10px;
    background-color: white;
    border-radius: 100px;
    padding: 15px 20px 15px 20px;
    width: 50vw;
    margin-bottom: 10px;
    cursor: pointer;
    text-align: center;
}
</style>

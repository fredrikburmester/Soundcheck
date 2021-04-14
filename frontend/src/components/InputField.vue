<template>
  <input type="text" name="" id="" :placeholder="placeholder_" />
</template>

<script>
export default {
  name: "InputField",
  props: {
    placeholder: {
      type: String,
    },
  },
  data() {
    return {
      placeholder_: this.placeholder,
    };
  },
  watch: {
    sendValue: function (value) {
      console.log(value);
      this.$emit("changed", "soee");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap");
input {
  font-size: 15px;
  font-family: "Roboto", sans-serif;
  font-weight: 500;
  letter-spacing: 10px;
  background-color: white;
  border-radius: 100px;
  padding: 15px 0px 15px 0px;
  width: 60vw;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 10px;
  box-sizing: border-box;
}
</style>

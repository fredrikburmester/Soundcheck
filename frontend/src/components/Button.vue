<template>
  <router-link :to="buttonLink">{{ buttonText }}</router-link>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    buttonLink: String,
    buttonText: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

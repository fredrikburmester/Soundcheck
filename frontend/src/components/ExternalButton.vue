<template>
    <div class="button">
        <router-link :to="buttonLink">{{ buttonText }}</router-link>
    </div>
</template>

<script>
export default {
    name: 'HelloWorld',
    props: {
        buttonLink: String,
        buttonText: String,
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.button {
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    letter-spacing: 2px;
    background-color: green;
    border-radius: 100px;
    padding: 15px 25px 15px 25px;
    width: 50vw;
    margin-left: auto;
    margin-right: auto;
}
.button a {
    color: white;
    text-transform: uppercase;
    text-decoration: none;
}
</style>

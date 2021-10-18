/*
About page.
 */

<template>
    <div class="aboutPage">
        <h1>About Soundcheck</h1>
        <div class="text">
            <VueMarkdownIt :style="style" :source="content" />
        </div>
        <div class="button-container">
            <Button 
                button-link="/login" 
                button-text="Back"
                color="#CD1A2B"
            />
        </div>
    </div>
</template>

<script>
import Button from '../components/Button'
import VueMarkdownIt from 'vue3-markdown-it'

export default {
    name: 'About',
    components: {
        Button,
        VueMarkdownIt
    },
    data(){
        return{
            content: 'Soundcheck is a game you can play with your friends. You sign in with your spotify account and then you create a room for your friends to join.'
                + '\n\nWhen you play, a random players top song will be displayed in a music player at the bottom of the screen so everyone can listen to the song'
                + 'To make a guess, tap on the player you think the song belongs to.\n\n'
                + 'When the game is over, your Spotify username, top songs and guesses will be saves in our database for users to view the results after the game.:)'
                + '\n\n _By using this website you agree that the information mentioned above can be stored_.'
                + '\n\n Creators: \n - Fredrik Burmester \n - Josef Hamnert \n - Daniel Hagstedt'
                + '\n\n Contact: \n - [fredrik.burmester@gmail.com](mailto:fredrik.burmester@gmail.com) \n - [josef.hamnert@gmail.com](mailto:josef.hamnert@gmail.com) \n - [dhagstedt@gmail.com](mailto:dhagstedt@gmail.com)'
        };
    },
    computed: {
        style() {
            return {
                'color': 'white !important',
                'text-decoration': 'none !important'
            }
        }
    }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.aboutPage{
    text-align: center;
    display: grid;
    grid-template-rows: 100px auto 200px;
    width: 100vw;
}
.text{
    font-family: 'Roboto', sans-serif;
    display: inline-block;
    text-align: left;
    margin: 0 2rem 0 2rem;
    overflow-y: scroll;
}
a {
    color: white !important; 
    text-decoration: none !important;
}
.button-container {
    padding: 2rem 2rem 2rem 2rem;
}
.aboutPage > .button {
    position: fixed;
    bottom: 30px;
}
@media only screen and (min-width: 900px) {
    .text {
        width: 40vw;
    }
}
</style>
/*
About page.
 */

<template>
    <div class="aboutPage">
        <h1>About Soundcheck</h1>
        <div class="text">
            <p>Soundcheck is a music game you can play with your friends. Sign in with your Spotify account and create a room for your friends to join.</p>
            <p>When you play, you and your friends top songs will be displayed and a music player at the bottom of the screen enables to listen to the song. To make a guess, tap on the player you think the song belongs to!</p>
            <p>When the game is over, your Spotify username, the songs in the game and guesses will be saves in our database for users to view the results after the game :)</p>
            <p><em>By using this website you agree that the information mentioned above can be stored.</em></p>
            <p>Creators:</p>
            <ul>
                <li><a href="mailto:fredrik.burmester@gmail.com"> Fredrik Burmester</a></li>
                <li><a href="mailto:dhagstedt@gmail.com"> Daniel Hagstedt</a></li>
                <li><a href="mailto:josef.hamnert@gmail.com"> Josef Hamnert</a></li>
            </ul>
            <p>Github: <a href="https://github.com/fredrikburmester/Soundcheck">Link</a></p>
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

export default {
    name: 'About',
    components: {
        Button,
    },
    data(){
        return{
            content: 'Soundcheck is a music game you can play with your friends. Sign in with your Spotify account and create a room for your friends to join.'
                + '\n\nWhen you play, you and your friends top songs will be displayed and a music player at the bottom of the screen enables to listen to the song. '
                + 'To make a guess, tap on the player you think the song belongs to!\n\n'
                + 'When the game is over, your Spotify username, the songs in the game and guesses will be saves in our database for users to view the results after the game :)'
                + '\n\n _By using this website you agree that the information mentioned above can be stored. \nIn your My Games panel you can always remove your stored name and username from the database. Other people can still se the game history but without your name._'
                + '\n\n Creators: \n - Fredrik Burmester \n - Josef Hamnert \n - Daniel Hagstedt'
                + '\n\n Contact: \n - [fredrik.burmester@gmail.com](mailto:fredrik.burmester@gmail.com) \n - [josef.hamnert@gmail.com](mailto:josef.hamnert@gmail.com) \n - [dhagstedt@gmail.com](mailto:dhagstedt@gmail.com)'
                + '\n\n _This game has no affiliation with Spotify._'
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
    height: 100vh;
    width: 100vw;
    text-align: center;
    display: grid;
    grid-template-rows: 100px auto 200px;
}
.text{
    font-family: 'Roboto', sans-serif;
    display: inline-block;
    text-align: left;
    overflow-y: scroll;
    padding: 0 8rem 0 8rem;
}
h1 {
    margin-top: 40px
}
p {
    line-height: 25px;
}
a {
    color: white !important; 
    text-decoration: none;
    font-weight: bold;
}
.button-container {
    padding: 2rem 2rem 2rem 2rem;
}
.aboutPage > .button {
    position: fixed;
}
@media only screen and (max-width: 1000px) {
    .text {
        padding: 0 2rem 0 2rem;
    }
}
</style>
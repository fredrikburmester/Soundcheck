/*
Page for displaying the results of one game. A list of all users and their points are displayed. If a player is clicked, their personal guesses are 
displayed in a modal. 
 */

<template>
    <div>
        <div v-if="state == 'found'">
            <transition name="fade">
            <div v-if="selected" :style="personalResultStyle" class="individual-grid">
                <div class="individual-grid-header">
                    <h1 class="code">
                        {{ selected_player.name }}
                    </h1>
                    <p class="date">
                        {{ date }}
                    </p>
                    <div class="hr" />
                    <h3 class="title">
                        Individual results
                    </h3>
                    <div class="close-button" @click="deselectPlayer()">
                        <CloseButton color="red"/>
                    </div>
                </div>
                <div class="personal-list">
                    <div v-for="guess in selected_player.guesses" :key="guess">
                        <GuessIcon
                            :trackid="guess.info"
                            :guess="guess.guess"
                            :answer="guess.correct_answer"
                        />
                    </div>
                </div>
            </div>
            </transition>
            <div class="grid" :style="resultGridStyle">
                <div class="grid-header">
                    <h1 class="code">
                        {{ code }}
                    </h1>
                    <p class="date">
                        {{ date }}
                    </p>
                </div>
                <div class="list">
                    <div v-for="player, index in players" :key="player.sid">
                        <h3 v-if="index == 0" class="title" style="padding-left: 0; margin-left: 0; color: gold">
                            Winner
                        </h3>
                        <h3 v-if="index > 0 && players[index-1].points != player.points" class="title" style="padding-left: 0; margin-left: 0; color: silver">
                            Second place
                        </h3>
                        <h3 v-if="index > 1 && players[index-1].points != player.points" class="title" style="padding-left: 0; margin-left: 0; color: #26c28">
                            Third place
                        </h3>
                        <h3 v-if="index > 2 && players[index-1].points != player.points" class="title" style="padding-left: 0; margin-left: 0; color: #26c28">
                            The rest of you loosers 💩
                        </h3>
                        <div style="height: 80px;">
                            <PlayerAvatar
                                :id="player.sid"
                                class="player-guess"
                                :player-name="player.name"
                                :color="player.color"
                                @click="selectPlayer(player)"
                            />
                            <p class="points">
                                {{ player.points }} Points
                            </p>
                        </div>
                    </div>
                </div>
                    
                <div class="play-again-container">
                    <div class="hr" />
                    <div class="button-container">
                        <Button
                            class="createPlaylist"
                            button-text="Create playlist"
                            @click="managePlaylists()"
                        />
                        <Button class="goHome" button-link="/" button-text="Play again" />
                    </div>
                </div>
            </div>
        </div>
        <div v-if="state == 'not-found'">
            <NotFound />
        </div>
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';
import NotFound from '../components/NotFound';
import GuessIcon from '../components/GuessIcon';
import CloseButton from '../components/CloseButton';

const axios = require('axios');

export default {
    name: 'Results',
    components: {
        PlayerAvatar,
        Button,
        NotFound,
        GuessIcon,
        CloseButton
    },
    data: function () {
        return {
            code: this.$route.params.code,
            players: [],
            date: '',
            selected: false,
            selected_player: null,
            answers: null,
            tracksForPlaylist: [],
            state: ''
        };
    },
    computed: {
        resultGridStyle() {
            return {
                'height': `${window.innerHeight}px`,
                'grid-template-rows': '170px auto 178px'
            }
        },
        personalResultStyle() {
            return {
                'height': `${window.innerHeight}px`,
                'width': `${window.innerWidth}px`
            }
        },
    },
    mounted() {
        
        var self = this;
        var url;

        //Needed to avoid multiple loads of the same tracks in /playlist route
        self.$store.commit('clearTracksForPlaylist');

        url = `${process.env.VUE_APP_PROTOCOL}://${process.env.VUE_APP_SERVER_URL}/api/${this.code}/results`;

        // When pressing a player for more information the data is loaded from the server:
        axios
            .get(url)
            .then(function (response) {
                var data = response.data;
                self.players = data.players;
                self.answers = data.answers;
                
                self.date = self.getDateFromUnix(data.date)

                // Convert answer ids to names for display
                for(let p1 of self.players) { // go through the players
                    for(let guess of p1.guesses) { // go through the guesses of that player
                        for(let p2 of self.players) { // find the username (id) for the guess 
                            if(guess.guess == p2.id) {  
                                guess.guess = p2.name // set id to the player name for display
                            }
                            if(guess.correct_answer == p2.id) {
                                guess.correct_answer = p2.name
                            }
                        }
                    }
                }

                // sorting the players based on points
                self.players.sort(function(a, b) {
                    var keyA = a.points,
                        keyB = b.points;
                    // Compare the 2 values
                    if (keyA < keyB) return 1;
                    if (keyA > keyB) return -1;
                    return 0;
                });
                
                //Add tracks to store so that they can be used in the /playlist route
                // get the tracks from the first players guesses
                for(let guess of self.players[0].guesses) {
                    self.$store.commit('addTrack', guess.info)
                }
                self.state = 'found';
            })
            .catch(function (err) {
                console.log(err)
                self.state = 'not-found';
            })
    },
    methods: {
        getPoints: function (player) {
            return `${player.name}: ${player.points} points`;
        },
        getDateFromUnix(unix) {
            var date = new Date(unix * 1000);
            var date_string = date.toLocaleDateString('se');
            var hour = date.getHours();
            var minute = date.getMinutes();
            if (minute < 10) minute = '0' + minute.toString();
            // var second = date.getSeconds()

            /* eslint-disable */
            return `Played on ${date_string} @ ${hour}:${minute}`;
            /* eslint-enable */
        },
        selectPlayer(player) {
            this.selected = true;
            this.selected_player = player;
        },
        managePlaylists(){
            this.$router.push(`/${this.code}/playlist`);
        },
        deselectPlayer() {
            this.selected = false;
        },
    }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s ease;
  -webkit-transition: opacity .2s ease;
  -moz-transition: opacity .2s ease;
  -o-transition: opacity .2s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.grid {
    display: grid;
    grid-template-columns: 1fr;
}
.grid-header {
    margin-top: 45px;
}
.individual-grid {
    position: fixed;
    top: 0;
    left: 0;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 220px auto;
    background: rgba(0, 0, 0, 0.84);
    z-index: 2;
    overflow: hidden;
    backdrop-filter: blur(4px);
}
.individual-grid-header {
    margin-top: 45px;
}
.personal-list {
    overflow-y: scroll;
    overflow-x: hidden;
    margin: 0px 2rem 0 2rem;
}
.song > .image {
    margin: 5px;
}
.code {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 0;
    width: 75vw;
}
.date {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 20px;
    color: gray;
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 0 2rem 0 2rem;
}
.title {
    font-style: italic;
    color: darkgrey;
    text-align: left;
    margin-top: 10px;
    margin-left: 2rem;
    margin-bottom:0;
    padding: 0;
}
.list {
    margin-left: 2rem;
    margin-right: 2rem;
    overflow-y: scroll;
    overflow-x: hidden;
}

.close-button {
    position: fixed;
    top: 70px;
    right: 2rem;
    height: 35px;
    width: 35px;
}
.button-container { 
    margin-top: 20px;
}
.line {
    background-color: red;
    
    height: 3px;
    width: 25px;
    cursor: pointer;
}
#line1 {
    transform: translateY(3px) rotate(45deg);
    margin-top: 10px;
    margin-left: 5px;

}
#line2 {
    transform: rotate(-45deg);
    margin-top: 0px;
    margin-left: 5px;

}
.points {
  position: relative;
  top: -40px;
  left: 80px;
  text-align: left;
  color: rgb(170, 170, 170);
  font-style: italic;
}
.play-again-container {
    padding: 0 2rem 0 2rem;
}
</style>

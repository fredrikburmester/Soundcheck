<template>
    <div>
        <transition name="fade" mode="out-in">
            <div v-if="state == 'loading'">
                <Loader />
            </div>
        </transition>

        <transition name="fade" mode="out-in">
            <div v-if="state == 'found'">
                <div v-if="selected" :style="personalResultStyle" class="individual-grid">
                    <div>
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
                            <div
                                id="line1"
                                class="line"
                            />
                            <div
                                id="line2"
                                class="line"
                            />
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
                <div class="grid" :style="resultGridStyle">
                    <div>
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
                            <h3 v-if="index == 1" class="title" style="padding-left: 0; margin-left: 0; color: silver">
                                Second place
                            </h3>
                            <h3 v-if="index == 2" class="title" style="padding-left: 0; margin-left: 0; color: #26c28">
                                Third place
                            </h3>
                            <h3 v-if="index == 3" class="title" style="padding-left: 0; margin-left: 0; color: #26c28">
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
                        <Button
                            class="createPlaylist"
                            button-text="Create playlist"
                            @click="createPlaylist(date)"
                        />
                    </div>
                    <div class="play-again-container">
                        <div class="hr" />
                        <Button style="margin-top: 20px" class="goHome" button-link="/" button-text="Play again" />
                    </div>
                </div>
            </div>
            <div class="list">
                <div v-for="player, index in players" :key="player.sid">
                    <h3 v-if="index == 0" class="title" style="padding-left: 0; margin-left: 0; color: gold">
                        Winner
                    </h3>
                    <h3 v-if="index == 1" class="title" style="padding-left: 0; margin-left: 0; color: silver">
                        Second place
                    </h3>
                    <h3 v-if="index == 2" class="title" style="padding-left: 0; margin-left: 0; color: #26c28">
                        Third place
                    </h3>
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
                <Button
                    class="createPlaylist"
                    button-text="Create playlist"
                    @click="managePlaylists()"
                />
                <Button class="goHome" button-link="/" button-text="Play again" />
            </div>
        </transition>
        <transition name="fade" mode="out-in">
            <div v-if="state == 'not-found'">
                <NotFound />
            </div>
        </transition>
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';
import NotFound from '../components/NotFound';
import GuessIcon from '../components/GuessIcon';
import Loader from '../components/Loader';

const axios = require('axios');

export default {
    name: 'Results',
    components: {
        PlayerAvatar,
        Button,
        NotFound,
        GuessIcon,
        Loader
    },
    data: function () {
        return {
            code: this.$route.params.code,
            players: [],
            state: 'loading',
            date: '',
            selected: false,
            selected_player: null,
            answers: null,
            tracksForPlaylist: [],
        };
    },
    computed: {
        resultGridStyle() {
            return {
                'height': `${window.innerHeight}px`,
                'grid-template-rows': '125px auto 100px'
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

        if (
            process.env.NODE_ENV == 'development' ||
            process.env.NODE_ENV == 'dev'
        ) {
            url = `http://${process.env.VUE_APP_SERVER_URL}/api/${this.code}/results`;
        } else {
            url = `https://${process.env.VUE_APP_SERVER_URL}/api/${this.code}/results`;
        }
        axios
            .get(url)
            .then(function (response) {
                var data = response.data;
                self.players = data.players;
                self.answers = data.answers;
                
                self.date = self.getDateFromUnix(data.date)

                // Convert answer ids to names
                for (let player of data.players) {
                    for (let guess of player.guesses) {
                        for (let player2 of data.players) {
                            if (player2.sid == guess.guess) {
                                guess.guess = player2.name;
                            }
                            if (player2.sid == guess.correct_answer) {
                                guess.correct_answer = player2.name;
                            }
                        }
                    }
                }

                self.players.forEach(player => {
                    var sid = player.sid
                    self.answers.forEach(answer => {
                        if(answer.player == sid) {
                            answer.player = player.name
                        }
                    })
                })

                self.players.sort(function(a, b) {
                    var keyA = a.points,
                        keyB = b.points;
                    // Compare the 2 dates
                    if (keyA < keyB) return 1;
                    if (keyA > keyB) return -1;
                    return 0;
                });

                self.players.forEach(player => {
                    self.answers.forEach((answer, index) => {
                        var found = false
                        player.guesses.forEach(guess => {
                            if (guess.question == index) {
                                found = true
                            }   
                        })
                        if(!found) {
                            player.guesses.push({
                                'correct_answer': answer.player,
                                'guess': '',
                                'info': answer.info,
                                'question': index
                            })
                        }
                    })
                })
                
                //Add tracks to store so that they can be used in the /playlist route
                self.answers.forEach((answer) => {
                    self.$store.commit('addTrack', answer['info'])
                })

                setTimeout(function(){ self.state = 'found'; }, 300);

            })
            .catch(function (err) {
                console.log(err)
                self.state = 'not-found';
            });
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
        createPlaylist() {

            this.$socket.client.emit('createPlaylist', {
                sid: localStorage.getItem('sid'),
                access_token: localStorage.getItem('access_token'),
                user_id: localStorage.getItem('user_id'),
                name: `Soundcheck - ${this.code}`,
                tracksForPlaylist: this.tracksForPlaylist,
            });
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
  transition: opacity .5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.grid {
    display: grid;
    grid-template-columns: 1fr;
}
.individual-grid {
    position: fixed;
    top: 0;
    left: 0;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 165px auto;
    background: black;
    z-index: 2;
    overflow: hidden;
}
.personal-list {
    overflow-y: scroll;
    overflow-x: hidden;
    margin: 30px 2rem 0 2rem;
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
    margin-top: 20px;
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
    top: 35px;
    right: 2rem;
}
.line {
    background-color: red;
    height: 3px;
    width: 25px;
    cursor: pointer;
}
#line1 {
    transform: translateY(3px) rotate(45deg);
}
#line2 {
    transform: rotate(-45deg);
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

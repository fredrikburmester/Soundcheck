<template>
  <div :key="state">
    <div v-if="state == 'loading'">
      <p>Loading...</p>
    </div>
    <div v-if="state == 'found'">
      <keep-alive>
        <div
          class="personalResultsModal"
        >
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
          <div
            class="close-button"
            @click="deselectPlayer()"
          >
            <div
              id="line1"
              class="line"
            />
            <div
              id="line2"
              class="line"
            />
          </div>
          <div
            class="personal-list"
          >
            <div
              v-for="guess in selected_player.guesses"
              :key="guess"
            >
              <GuessIcon
                :trackid="guess.info"
                :guess="guess.guess"
                :answer="guess.correct_answer"
              />
            </div>
          </div>
        </div>
      </keep-alive>
      
      <h1 class="code">
        {{ code }}
      </h1>
      <p class="date">
        {{ date }}
      </p>
      <div class="hr" />
      <h3 class="title">
        Results
      </h3>
      <div class="list">
        <div
          v-for="player in players"
          :key="player.sid"
          :class="
            selected == player.sid
              ? 'expand player-block'
              : 'player-block'
          "
        >
          <PlayerAvatar
            :id="player.sid"
            class="player-guess"
            :player-name="getPoints(player)"
            :color="player.color"
            @click="selectPlayer(player)"
          />
        </div>
      </div>
      <Button
        class="goHome"
        button-link="/"
        button-text="Play again"
      />
    </div>
    <div v-if="state == 'not-found'">
      <NotFound />
    </div>
    <Button
      class="goHome"
      button-link="/"
      button-text="Play again"
    />
  </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';
import NotFound from '../components/NotFound';
import GuessIcon from '../components/GuessIcon';

const axios = require('axios');

export default {
    name: 'Results',
    components: {
        PlayerAvatar,
        Button,
        NotFound,
        GuessIcon,
    },
    data: function () {
        return {
            code: this.$route.params.code,
            players: [],
            state: 'loading',
            date: '',
            selected: false,
            selected_player: null
        };
    },
    mounted() {
        var self = this;
        var url;
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
                console.log('Answers: ', response);
                var data = response.data;
                self.players = data.players;
                var date = new Date(data.date * 1000);
                var date_string = date.toLocaleDateString('se');
                var hour = date.getHours();
                var minute = date.getMinutes();
                if (minute < 10) minute = '0' + minute.toString();
                // var second = date.getSeconds()

                /* eslint-disable */
                self.date = `Played on ${date_string} @ ${hour}:${minute}`;
                /* eslint-enable */

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

                console.log(self.players);
                self.state = 'found';
            })
            .catch(function (error) {
                console.log(error);
                self.state = 'not-found';
            });
    },
    methods: {
        getPoints: function (player) {
            return `${player.name}: ${player.points} points`;
        },
        selectPlayer(player) {
            console.log('select player');
            this.selected = true
            this.selected_player = player
        },
        deselectPlayer() {
            this.selected = false
        }
    },
};
</script>

<style scoped>
.code {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 0;
}
.date {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 0;
    color: gray;
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 1rem 2rem 1rem 2rem;
}
.title {
    font-style: italic;
    color: darkgrey;
    text-align: left;
    margin-left: 2rem;
    margin-top: 0;
    margin-bottom: 20px;
}
.list {
    height: calc(100vh - 420px);
    overflow-y: scroll;
    margin-left: 2rem;
    margin-right: 2rem;
    overflow-x: hidden;
}
.personal-list {
    height: calc(100vh - 220px);
    overflow-y: scroll;
    overflow-x: hidden;
}
.goHome {
    position: fixed;
    left: 50%;
    bottom: 20px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    z-index: 1;
}
.personalResultsModal {
    background-color: black;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    z-index: 2;
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
</style>

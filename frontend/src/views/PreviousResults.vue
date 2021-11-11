/*
Displays a list of previous games for one user. 
 */

<template>
    <div v-if="!loading">
        <div class="grid" :style="resultGridStyle">
            <div class="grid-header">
                <h1 class="title">
                    Previous Games <br><span @click="removeUserData" style="color: red; font-size: 15px; cursor: pointer;">Remove Data</span>
                </h1>
                <p class="username">
                    {{ username }}
                </p>
            </div>
            <div class="list">
                <div v-for="result in results.slice().reverse()" :key="result" class="list-item" @click="goTo(result.code)">
                    <PreviousResultIcon :code="result.code" :date="getDateStringFromUnix(result.date)" :uri="result.answers[0].info" />
                </div>
            </div>
            <div class="buttons">
                <Button button-text="back" @click="goBack()" />
            </div>
        </div>
    </div>
</template>

<script>
import API from '../libs/api.js'
import PreviousResultIcon from '../components/PreviousResultIcon'
import Button from '../components/Button'
import store from '../store/index'

export default {
    components: {
        PreviousResultIcon,
        Button,
    },
    // before entering the route the previous games are loaded from the server. loading time is added here for design puposes. 
    beforeRouteEnter (to, from, next) {
        var self = this;
        API.getPersonalResults(store.getters.getUserId).then((result) => {
            if(result === null) {
                next(self => self.results = [])
            } else {
                setTimeout(()=> {
                    next(self => self.results = result.data.results)
                },600)
            }
        })
    },
    data() {
        return {
            results: [],
            username: this.$store.getters.getUserId,
        }
    },
    computed: {
        resultGridStyle() {
            return {
                'height': `${window.innerHeight}px`,
            }
        }
    },
    methods: {
        getDateStringFromUnix(unix) {
            var gameDate = new Date(unix * 1000);
            var currentDate = new Date();

            var hour = gameDate.getHours();
            var minute = gameDate.getMinutes();
            if (minute < 10) minute = '0' + minute.toString();

            var gameDateString = `${gameDate.getFullYear()}-${gameDate.getMonth()}-${gameDate.getDate()}`;
            currentDate = `${currentDate.getFullYear()}-${currentDate.getMonth()}-${currentDate.getDate()}`;

            var date_string;
            if(gameDateString == currentDate) {
                date_string = "Today"
                /* eslint-disable */
                return `${date_string} @ ${hour}:${minute}`;
                /* eslint-enable */
            } else {
                date_string = gameDate.toLocaleDateString('se');
                /* eslint-disable */
                return `Played on ${date_string} @ ${hour}:${minute}`;
                /* eslint-enable */
            }
        },
        goTo(code) {
            this.$router.push(`/${code}/results`)
        },
        goBack() {
            this.$router.go(-1)
        },
        removeUserData() {
            // send socket to call clearPlayerData function
            this.$socket.client.emit('clearPlayerData', {
                id: this.$store.getters.getUserId,
            });
            this.$store.commit('updateLoading', true);

            const self = this;
            setTimeout(function(){ 
                self.$router.go(0)
                self.$store.commit('updateLoading', false);
            }, 500);
        }
    }
}
</script>

<style scoped>

.grid {
    display: grid;
    grid-template-rows: 190px auto 120px;
    padding: 0 2rem 0 2rem;
}
.grid-header {
margin-top: 45px;
}
.title, .username {
    text-align: left;
    margin-bottom: 0;
}
.username {
    color: gray;
    font-style: italic;  
    margin-top: 0;  
}
.buttons {
    margin-top: 20px
}
.list {
    overflow-y: scroll;
    overflow-x: hidden;
    border-top: 1px gray solid;
    border-bottom: 1px gray solid;
    padding-bottom: 20px;
    padding-top: 5px
}
.list-item {
    overflow: hidden;
}
.date {
  position: relative;
  top: -40px;
  left: 80px;
  text-align: left;
  color: rgb(170, 170, 170);
  font-style: italic;
}
</style>
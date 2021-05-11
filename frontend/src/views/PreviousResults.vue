<template>
    <div>
        <transition name="fade" mode="out-in">
            <div v-if="!loaded">
                <Loader />
            </div>
        </transition>
        <transition name="fade" mode="out-in">
            <div class="grid" :style="resultGridStyle">
                <div>
                    <h1 class="title">
                        Previous Games
                    </h1>
                    <p class="username">
                        {{ username }}
                    </p>
                </div>
                <div class="list">
                    <div v-for="result in results" :key="result" style="height: 80px;" @click="goTo(result.code)">
                        <PreviousResultIcon :code="result.code" :date="getDateStringFromUnix(result.date)" :uri="result.answers[0].info" />
                    </div>
                </div>
                <div class="buttons">
                    <Button button-text="back" @click="goBack()" />
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import API from '../libs/api.js'
import PreviousResultIcon from '../components/PreviousResultIcon'
import Button from '../components/Button'
import Loader from '../components/Loader'

export default {
    components: {
        PreviousResultIcon,
        Button,
        Loader
    },
    data() {
        return {
            results: [],
            loaded: false,
            username: this.$store.getters.getUsername
        }
    },
    computed: {
        resultGridStyle() {
            return {
                'height': `${window.innerHeight}px`,
            }
        },
    },
    mounted() {
        this.getResults()
    },
    methods: {
        async getResults() {
            try {
                const result = await API.getPersonalResults(this.$store.getters.getUsername)
                this.results = result.data.results
            } catch {
                console.log("No songs")
            } finally {
                var self = this
                setTimeout(function(){ self.loaded = true; }, 600);
            }
        },
        getDateStringFromUnix(unix) {
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
        goTo(code) {
            this.$router.push(`/${code}/results`)
        },
        goBack() {
            this.$router.go(-1)
        }
    }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s ease;
  -webkit-transition: opacity .5s ease;
  -moz-transition: opacity .5s ease;
  -o-transition: opacity .5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.grid {
    display: grid;
    grid-template-rows: 100px auto 100px;
    padding: 0 2rem 0 2rem;
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
    border-bottom: 1px gray solid
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
/* 
Component that displays a persons guess in the game on the results page. 
Takes the trackid, guess and answer as props. 
Gathers album art, track and artist name from spotify API here.
*/

<template>
    <div>
        <transition name="fade">
            <div v-if="imgSrc" class="song">
                <div class="image-container">
                    <img :src="imgSrc" alt="image">
                </div>
                <div class="info">
                    <p id="song" style="color: gray">
                        Song
                    </p>
                    <p id="track-name">
                        {{ track_name }}
                    </p>
                    <p id="artist">
                        {{ artist }}
                    </p>
                    <br>
                    <p id="answer">
                        Answer: <span>{{ answer }}</span> 
                    </p>
                    <p id="guess">
                        Guess: <span :style="guess == answer ? 'color: green' : 'color: red'">{{ guess }}</span>
                    </p>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
const axios = require('axios');

export default {
    name: 'PlayerAvatar',
    props: {
        trackid: {
            type: String,
            default: ''
        },
        guess: {
            type: String,
            default: ''
        },
        answer: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            trackid_: this.trackid,
            imgSrc: '',
            loaded: false,
            track_name: '',
            artist: ''
        };
    },
    mounted() {
        this.getAlbumArt(this.trackid_);
    },
    methods: {
        async getAlbumArt(uri) {
            var token = this.$store.getters.getAccessToken;
            var self = this;
            axios
                .get(`https://api.spotify.com/v1/tracks/${uri}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                })
                .then(function (response) {
                    self.imgSrc = response.data.album.images[0].url;
                    self.track_name = response.data.name
                    self.artist = response.data.artists[0].name
                });
        },
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease;
  -webkit-transition: opacity 1s ease;
  -moz-transition: opacity 1s ease;
  -o-transition: opacity 1s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.song {
	display: flex;
	flex-direction: row;
    margin-bottom: 2rem;
}
.image-container {
	width: 60px;
	height: 60px;
    margin: 5px;
}
.image-container img {
	width: 60px;
	height: 60px;
	border-radius: 100px;
}
.info {
	margin-left: 20px;
	text-align: left;
	line-height: 20px;
}
p {
	margin: 0;
}

</style>

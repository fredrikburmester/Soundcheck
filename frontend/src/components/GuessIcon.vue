<template>
    <div>
        <div class="song">
            <div class="image">
                <img :src="imgSrc" class="circle">
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
            console.log("uri: ", uri)
            console.log('getting art');
            var token = localStorage.getItem('access_token');
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
                    console.log(response)
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

.song {

	display: flex;
	flex-direction: row;
	margin: 5vh 2rem 5vh 2rem;
}
.image {
	width: 60px;
	height: 60px;
}
.image img {
	width: 60px;
	height: 60px;
	border-radius: 50%;
	background-color: white;
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

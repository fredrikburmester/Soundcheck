<template>
    <div>
        <div class="song">
            <div class="image">
                <img :src="imgSrc" class="circle">
            </div>
            <div class="info">
                <p id="track-name">
                    {{ track_name }}
                </p>
                <p id="artist">
                    {{ artist }}
                </p>
            </div>
        </div>
    </div>
</template>
<script>
const axios = require('axios');

export default {
    name: 'TrackIcon',
    props: {
        trackid: {
            type: String,
            default: ''
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
    margin: 20px 0 20px 0
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
    display: flex;
    justify-content: center;
    flex-direction: column;
}
p {
    margin: 0;
}
</style>
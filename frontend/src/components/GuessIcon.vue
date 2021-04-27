<template>
    <div class="playerAvatar">
        <div class="image">
            <img :src="imgSrc" class="circle">
        </div>
        <div class="name">
            Guess: {{guess}}<br>
            Answer: {{answer}}
        </div>
    </div>
</template>

<script>
const axios = require('axios');

export default {
    name: 'PlayerAvatar',
    props: {
        trackID: {
            type: String,
        },
        guess: {
            type: String,
        },
        answer: {
            type: String,
            default: '',
        }
    },
    data() {
        return {
            trackID_: this.trackID,
            imgSrc: '',
            loaded: false
        };
    },
    methods: {
        async getAlbumArt(uri) {
            console.log("getting art")
            var token = localStorage.getItem('access_token')
            var self = this;
            axios
                .get(
                    `https://api.spotify.com/v1/tracks/${uri}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                            Accept: 'application/json',
                            'Content-Type': 'application/json',
                        },
                    }
                )
                .then(function (response) {
                    self.imgSrc = response.data.album.images[0].url
                })
        }
    },
    mounted() {
        this.getAlbumArt(this.trackID_)
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.playerAvatar {
display: flex;
flex-direction: row;
margin-bottom: 10px;
}
.image {
    width: 60px;
    height: 60px;
}
.image img {
    width: 60px;
    height: 60px;
    border-radius: 50%;

}
.name {
    margin-left: 20px;
    text-align: left;
}
</style>

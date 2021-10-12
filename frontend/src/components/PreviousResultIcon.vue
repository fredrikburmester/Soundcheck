/* 
Component for displaying a previous game icon. 
Takes the game code, date and a trackuri as arguments. 
Gathers information about the game from our API. 
*/

<template>
    <div v-if="loaded" class="roomIcon">
        <div class="image">
            <img :key="imgSrc" :src="imgSrc">
        </div>
        <div class="text">
            <div class="code">
                <p>
                    {{ code_ }}
                </p>
            </div>
            <div class="date">
                <p>
                    {{ date_ }}
                </p>
            </div>
        </div>
    </div>
</template>

<script>
import API from '../libs/api'

export default {
    name: 'PreviousResultIcon',
    props: {
        code: {
            type: String,
            default: ''
        },
        date: {
            type: String,
            default: '',
        },
        uri: {
            type: String,
            default: '',
        }
    },
    data() {
        return {
            code_: this.code,
            date_: this.date,
            uri_: this.uri,
            imgSrc: 'fdsa',
            loaded: false
        };
    },
    mounted() {
        this.getImgSrc()
    },
    methods: {
        async getImgSrc() {
            this.imgSrc = await API.getAlbumArt(this.uri_)
            this.loaded = true
        }

    }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.roomIcon {
    display: flex;
    position: relative;
    margin-bottom: 10px;
    margin-top: 10px;

    /* height: 70px; */
    overflow-x: hidden;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: center;
}
.circle {
    border-radius: 50%;
    font-family: 'Roboto', sans-serif;
    width: 60px;
    height: 60px;
    left: 0;
    margin: 5px;
    display: grid;
    align-items: center;
    background: white;
}
.text {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-items: center;

}
.code > p {
    white-space: nowrap;
    margin: 0 0 0 10px;
    padding: 0;
}
.date > p {
    white-space: nowrap;
    padding: 0;
    margin: 0 0 0 10px;
    color: gray
}
.image {
	width: 60px;
	height: 60px;
    margin: 5px;
}
.image img {
	width: 60px;
	height: 60px;
	border-radius: 50%;
	background-color: white;
}
</style>

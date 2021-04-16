<template>
    <div :style="btnStyles" class="button">
        <a :style="aColor" v-if="external">{{ buttonText_ }}</a>
        <router-link :style="aColor" v-else :to="buttonLink_">{{ buttonText_ }}</router-link>
    </div>
</template>

<script>
export default {
    name: 'Button',
    props: {
        buttonLink: {
            type: String,
        },
        buttonText: {
            type: String,
        },
        color: {
            type: String,
            default: '#1DB954',
        },
    },
    data() {
        return {
            buttonLink_: this.buttonLink,
            buttonText_: this.buttonText,
            color_: this.color,
        };
    },
    computed: {
        external() {
            if (this.buttonLink_ === undefined) {
                return true;
            } else {
                return false;
            }
        },
        btnStyles() {
            return {
                'background-color': this.color,
            };
        },
        aColor() {
            if(this.color == "#FFF" || this.color == "#FFFFFF") {
                return {
                    'color': 'black'
                }
            } else {
                return {
                    'color': 'white',
                };
            }
        }
    },
    watch: {
        buttonLink: function (value) {
            this.buttonLink_ = value;
        },
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.button {
    display: inline-block;
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    letter-spacing: 2px;
    border-radius: 100px;
    padding: 15px 20px 15px 20px;
    width: 50vw;
    margin-bottom: 10px;
}
.button a {
    color: white;
    text-transform: uppercase;
    text-decoration: none;
    margin-left: auto;
    margin-right: auto;
}
</style>

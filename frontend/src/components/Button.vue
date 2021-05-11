<template>
    <div
        :style="colorStyles"
        class="button"
        @click="go"
    >
        {{ buttonText_ }}
    </div>
</template>

<script>
export default {
    name: 'Button',
    props: {
        buttonLink: {
            type: String,
            default: ''
        },
        buttonText: {
            type: String,
            default: ''
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
        colorStyles() {
            if (
                this.color_ == '#FFF' ||
                this.color_ == '#FFFFFF' ||
                this.color_ == 'white'
            ) {
                return {
                    'background-color': this.color_,
                    color: 'black',
                };
            } else {
                return {
                    'background-color': this.color_,
                    color: 'white',
                };
            }
        },
    },
    methods: {
        go: function () {
            if (!this.external) {
                this.$router.push(this.buttonLink_);
            }
        },
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.button {
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    letter-spacing: 2px;
    border-radius: 100px;
    padding: 15px 20px 15px 20px !important;
    max-width: 300px;
    margin-bottom: 10px;
    cursor: pointer;
}

.button:active {
    background-color: rgb(63, 63, 63) !important;
}

.button {
    color: white;
    text-transform: uppercase;
    text-decoration: none;
    margin-left: auto;
    margin-right: auto;
}
@media only screen and (max-width: 315px) {
    .button {
        font-size: 0.75em;
    }
}
</style>

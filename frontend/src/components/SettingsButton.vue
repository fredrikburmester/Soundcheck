<template>
    <div @click="select" class="settingbutton" :style="colorStyle">
        {{ buttonText_ }}
    </div>
</template>

<script>
export default {
    name: 'SettingsButton',
    props: {
        buttonText: {
            type: String,
        },
        color: {
            type: String,
            default: '#777777',
        },
        marked: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            buttonText_: this.buttonText,
            color_: this.color,
        };
    },
    methods: {
        select: function () {
            this.$emit('clicked', this.buttonText_);
        },
    },
    computed: {
        colorStyle() {
            if (this.marked) {
                return {
                    'background-color': '#1DB954',
                };
            } else {
                return {
                    'background-color': this.color,
                };
            }
        },
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.settingbutton {
    position: relative;
    display: inline-block;
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    border-radius: 50%;
    padding: 15px 20px 15px 20px;
    margin: 0 5px 0 5px;
    cursor: pointer;
}
</style>

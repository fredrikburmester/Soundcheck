<template>
    <div class="playerAvatar">
        <div :style="playerIconStyles" class="circle">
            <p class="initials">
                {{ initials }}
            </p>
        </div>
        <p class="name" v-if="host">{{ playerName_ }} (Host)</p>
        <p class="name" v-else>
            {{ playerName_ }}
        </p>
    </div>
</template>

<script>
export default {
    name: 'PlayerAvatar',
    props: {
        playerName: {
            type: String,
        },
        color: {
            type: String,
            default: '#FFF',
        },
        host: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            playerName_: this.playerName,
            initials: this.playerName[0] + this.playerName[1],
            color_: this.color,
            host_: this.host,
        };
    },
    computed: {
        playerIconStyles() {
            return {
                'background-color': this.color,
            };
        },
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.playerAvatar {
    width: 70vw;
    display: flex;
    flex-direction: row;
    margin-bottom: 20px;
}
.circle {
    border-radius: 50%;
    font-family: 'Roboto', sans-serif;
    width: 60px;
    height: 60px;
}
.initials {
    margin-top: 20px;
    font-family: 'Roboto', sans-serif;
}
.name {
    margin-top: 20px;
    margin-left: 20px;
}
</style>

/* 
Player avatar implemented in the game waiting room. Displays if the person is host or not and the name of the player. 
Takes player name, color, and host as arguments. 

Component also implemented as guessing icon when game has started.
*/

<template>
    <div class="playerAvatar">
        <div>
            <div
                :style="playerIconStyles"
                class="circle"
            >
                <p class="initials">
                    {{ initials }}
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PlayerAvatar',
    props: {
        playerName: {
            type: String,
            default: ''
        },
        color: {
            type: String,
            default: '#FFF',
        },
        host: {
            type: Boolean,
            default: false,
        },
        isMe: {
            type: Boolean,
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
    methods: {

    }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.playerAvatar {
    display: flex;
    position: relative;
    margin-bottom: 10px;
    margin-top: 10px;

    height: 40px;
    overflow: hidden;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: center;
    cursor: pointer;
}
.circle {
    border-radius: 50%;
    font-family: 'Roboto', sans-serif;
    width: 40px;
    height: 40px;
    left: 0;
    margin: 5px;
    display: grid;
    align-items: center;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 4px #00ff74;
    }
    50% {
        box-shadow: 0 0 0 4px black;
    }
    100% {
        box-shadow: 0 0 0 4px #00ff74;
    }
}
.initials {
    font-family: 'Roboto', sans-serif;
    position: absolute;
    margin-left: 13px;
    z-index: 1;
}
</style>

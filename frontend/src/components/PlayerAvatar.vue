/* 
Player avatar implemented in the game waiting room. Displays if the person is host or not and the name of the player. 
Takes player name, color, and host and selected as arguments. 

Component also implemented as guessing icon when game has started. Hence the selected prop.
*/

<template>
    <div class="playerAvatar">
        <div>
            <div
                :class="selected_ ? 'selected' : ''"
                :style="playerIconStyles"
                class="circle"
            >
                <p class="initials">
                    {{ initials }}
                </p>
            </div>
        </div>
        <div class="avatar-text">
            <p class="name" :class="selected_ ? 'selected-text' : ''">
                {{ playerName_ }}
            </p>
            <p v-if="guesses_ > 1" class="guesses">Guessed: {{guesses_}} times</p>
            <p v-if="guesses_ == 1" class="guesses">Guessed: {{guesses_}} time</p>
        </div>
        <div
            v-if="host"
            class="star"
        >
            <span style="font-size: 12px; color: gray; margin-left: 54px">Game leader</span> 
            
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
        selected: {
            type: Boolean,
        },
        guesses: {
            type: Number,
            default: 0
        },
        numberOfSongs: {
            type: Number,
            default: 0
        },
    },
    data() {
        return {
            playerName_: this.playerName,
            initials: this.playerName[0] + this.playerName[1],
            color_: this.color,
            host_: this.host,
            selected_: this.selected,
            guesses_ : this.guesses,
            numberOfSongs_ : this.numberOfSongs,
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
    display: flex;
    position: relative;
    margin-bottom: 10px;
    margin-top: 10px;

    height: 70px;
    overflow: hidden;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: center;
    cursor: pointer;
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
}
.selected {
    box-shadow: 0 0 0 3px #00ff74;
    box-sizing: border-box;
    animation-name: pulse;
    animation-duration: 1s;
    animation-iteration-count: infinite;
}
.selected-text {
    color: #00ff74;
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
    z-index: 1;
    top: 0;
    padding: 0;
}
.guesses {
    font-size: 12px;
    top: 33px; 
    margin-left: 10px;
    position: absolute;
}
.name {
    white-space: nowrap;
    margin-left: 10px;
}
.star {
    position: absolute;
    top: -2px;
    left: 26px;
    font-size: 20px;
}
</style>

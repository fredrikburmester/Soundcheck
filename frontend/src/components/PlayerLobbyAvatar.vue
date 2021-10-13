/* 
Player avatar implemented in the game waiting room. Displays if the person is host or not and the name of the player. 
Takes player name, color, and host as arguments. 

Component also implemented as guessing icon when game has started.
*/

<template>
    <div class="playerAvatar">
        <div class="changeNameModal">

        </div>
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
        <div class="name" >
            <input @click="changeName($event)" @keyup.enter="onEnter" type="text" id="playerName" readonly="readonly" :value="playerName"> 
        </div>
        <div
            v-if="host"
            class="star"
        >
            👑 <span style="font-size: 12px; color: gray; margin-left: 10px">Game leader</span> 
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
        changeName: function(event) {
            console.log(this.isMe)
            if (this.isMe && event.target.hasAttribute('readonly')) {
                event.target.removeAttribute('readonly');
            } 
        },
        onEnter: function(event) {
            event.target.blur()
            event.target.setAttribute('readonly','readonly')
            this.playerName_ = event.target.value
            console.log(`New name: ${this.playerName_}`)
            this.$emit('updateName', this.playerName_)
        }
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
.name > p {
    white-space: nowrap;
    margin-left: 10px;
}
.name > input {
    background: none;
    color: white;
    border: none;
    margin-left: 10px;
    font-size: 17px;
}
.star {
    position: absolute;
    top: 40px;
    left: 45px;
    font-size: 20px;
}
</style>

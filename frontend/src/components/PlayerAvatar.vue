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
    <div class="name">
      <p :class="selected_ ? 'selected-text' : ''">
        {{ playerName_ }}
      </p>
    </div>
    <div
      v-if="host"
      class="star"
    >
      ⭐️
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
    },
    data() {
        return {
            playerName_: this.playerName,
            initials: this.playerName[0] + this.playerName[1],
            color_: this.color,
            host_: this.host,
            selected_: this.selected,
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
    margin-bottom: 10px;
    overflow-x: hidden;
    flex-wrap: nowrap;
    justify-content: start;
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
.name > p {
    white-space: nowrap;
    margin-left: 10px;
}
.star {
    position: absolute;
    margin-top: 35px;
    margin-left: 45px;
    font-size: 20px;
}
</style>

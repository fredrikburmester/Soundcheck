<template>
  <div class="home">
    <h1>Room</h1>   
    <p>{{ code }}</p>
    <PlayerAvatar v-for="player in players" v-bind:key="player" :playerName="player" :color="color" />
    <img :src="'https://api.qrserver.com/v1/create-qr-code/?data=/' + code" class="QR"/>
    <Button v-on:click="leaveRoom" buttonText="Leave Room" color="#CD1A2B"/>
  </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar'
import Button from '../components/Button'

const io = require("socket.io-client");
const socket = io("http://localhost:5000");

export default {
  name: "Home",
  components: {
    PlayerAvatar,
    Button
  },
  data: function () {
    return {
        players: [],
        colors: [],
        color: this.generator()
    }
  },
  methods: {
    generator: function(){
        return '#'+(Math.random()*0xFFFFFF<<0).toString(16);
    },
    leaveRoom: function(){

        this.$router.push('/')
    }
  },
  computed: {
      code() {
          return this.$route.params.code
      }
  },
  beforeMount() {
        socket.emit('joinRoom',{'access_token':localStorage.getItem('access_token'),'code': this.code});
  },
  mounted() {
        var self = this

        socket.on("connect", () => {
          console.log(socket.id);
        });

        socket.on("playerJoined", (data) => {
            console.log("player joined")
            self.players.push(data.name)
        });

        socket.on("listofplayers", (data) => {
            self.players = [] 
            data.players.forEach(player => {
                self.players.push(player)
            });
        });
  }


};
</script>

<style scoped>
.QR{
  transform: scale(0.5);
  border: 5px solid rgb(255, 255, 255);
}
</style>
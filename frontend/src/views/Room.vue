<template>
  <div class="home">
    <h1>Room</h1>   
    <p>{{ code }}</p>
    <p v-for="player in players" v-bind:key="player">{{ player }}</p>
  </div>
</template>

<script>
const io = require("socket.io-client");
const socket = io("http://localhost:5000");

export default {
  name: "Home",
  components: {
  },
  data: function () {
    return {
        players: []
    }
  },
  methods: {

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

<template>
  <div class="home">
    <h1>Start a game...</h1>
    <Button buttonLink="/create" buttonText="Create Room" />
    <Button buttonLink="/join" buttonText="Join Room" />
    <p>{{ name }}</p>
    <div class="logout">
      <Button
        @click="logout"
        color="#CD1A2B"
        buttonLink="/logout"
        buttonText="Log out"
      />
    </div>
  </div>
</template>

<script>
const axios = require("axios");
import Button from "../components/Button";

export default {
  name: "Home",
  components: {
    Button,
  },
  data: function () {
    return {
      name: "",
    };
  },
  methods: {
    getUserData: function () {
      var self = this;
      var token = localStorage.getItem("access_token");
      axios
        .get("https://api.spotify.com/v1/me", {
          headers: {
            Authorization: `Bearer ${token}`,
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then(function (response) {
          // handle success
          console.log(response.data);
          self.name = response.data.display_name;
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        })
        .then(function () {
          // always executed
        });
    },
    getUserTopTracks: function () {
      // var self = this;
      var token = localStorage.getItem("token");
      console.log(token);
      console.log(decodeURIComponent(token));
      axios
        .get("https://api.spotify.com/v1/me/top/tracks", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then(function (response) {
          // handle success
          console.log(response.data);
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        })
        .then(function () {
          // always executed
        });
    },
    logout: function () {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.$router.push("/login");
    },
  },
  beforeMount() {},
};
</script>

<style scoped>
.home {
  margin-top: 30vh;
}
.logout {
  position: fixed;
  left: 50%;
  bottom: 20px;
  transform: translate(-50%, -50%);
  margin: 0 auto;
}
</style>

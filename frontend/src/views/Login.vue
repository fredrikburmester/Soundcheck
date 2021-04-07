<template>
  <div class="login">
    <h1>Login Page</h1>
    <button v-on:click="loginWithSpotify">Log in with Spotify</button>
  </div>
</template>

<script>
export default {
  name: "Login",
  components: {
 
  },
  methods: {
      loginWithSpotify: function() {
          console.log("[1]")
          window.location.href = "https://accounts.spotify.com/authorize?client_id=bad02ecfaf4046638a1daa7f60cbe42b&response_type=code&redirect_uri=http://localhost:8080/logincallback&scope=user-read-private%20user-read-email&state=34fFs29kd09"
      } 
  }
};
</script>

import VueSocketIOExt from 'vue-socket.io-extended';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

console.log("pp ", process.env.NODE_ENV)

var io = require('socket.io-client');
var socket;

if(process.env.NODE_ENV == 'development') {
    socket = io('http://localhost:5000');
} else {
    socket = io('https://musicwithfriends.fdrive.se/', {'path': '/ws'});
}

const app = createApp(App);
app.use(store)
app.use(router)
app.use(VueSocketIOExt, socket);
app.mount("#app")

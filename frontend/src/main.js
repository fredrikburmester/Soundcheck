import VueSocketIOExt from 'vue-socket.io-extended';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

var io = require('socket.io-client');
var socket;

if (process.env.NODE_ENV == 'development' || process.env.NODE_ENV == 'dev') {
    console.log('Running in development mode');
    socket = io('http://localhost:5000');
} else {
    console.log('Running in production mode');
    socket = io('https://musicwithfriends.fdrive.se/', { path: '/ws' });
}

const app = createApp(App);
app.use(store);
app.use(router);
app.use(VueSocketIOExt, socket);
app.mount('#app');

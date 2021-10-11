import VueSocketIOExt from 'vue-socket.io-extended';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

var io = require('socket.io-client');
var socket;

// Depending on if the server is running in production of development we assign different node process variables. 
if (process.env.NODE_ENV == 'development' || process.env.NODE_ENV == 'dev') {
    console.log('Running in development mode');
    socket = io('http://localhost:5001');
} else {
    console.log('Running in production mode');
    //socket = io('https://soundcheck.fdrive.se/', { path: '/ws' });
    socket = io('http://localhost:5001');
}

const app = createApp(App);
app.use(store);
app.use(router);
app.use(VueSocketIOExt, socket);
app.mount('#app');

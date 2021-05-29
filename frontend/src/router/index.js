import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Join from '../views/Join.vue';
import Create from '../views/Create.vue';
// import Room from '../views/Room.vue';
import GameRoom from '../views/GameRoom.vue';
import Results from '../views/Results.vue';
import Playlist from '../views/Playlist.vue';
import LoginCallback from '../views/LoginCallback.vue';
import NotFound from '../components/NotFound.vue';
import About from '../views/About.vue'
import PreviousResults from '../views/PreviousResults.vue'
import store from '../store';

const axios = require('axios');

function checkAccessToken(to, from, next) {
    if (store.getters.getAccessToken) {
        var token = store.getters.getAccessToken;
    } else {
        next({ name: 'Login' });
        return;
    }

    axios
        .get('https://api.spotify.com/v1/me', {
            headers: {
                Authorization: `Bearer ${token}`,
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
        .then(function (response) {
            if(!localStorage.getItem('user_id', response.data.id)) {
                localStorage.setItem('user_id', response.data.id);
            }
            
            next();
            return;
        })
        .catch(function () {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_id');
            next({ name: 'Login' });
            return;
        });

    return;
}

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        beforeEnter: (to, from, next) => {
            checkAccessToken(to, from, next);
        },
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        beforeEnter: (to, from, next) => {
            if (store.getters.getAccessToken) {
                next({ name: 'Home' });
                return;
            } else {
                next();
                return;
            }
        },
    },
    {
        path: '/about',
        name: 'About',
        component: About
    },
    {
        path: '/logincallback',
        name: 'LoginCallback',
        component: LoginCallback,
    },
    {
        path: '/join',
        name: 'Join',
        component: Join,
        beforeEnter: (to, from, next) => {
            checkAccessToken(to, from, next);
        },
    },
    {
        path: '/create',
        name: 'Create',
        component: Create,
        beforeEnter: (to, from, next) => {
            checkAccessToken(to, from, next);
        },
    },
    {
        path: '/me',
        name: 'PreviousResults',
        component: PreviousResults,
        beforeEnter: (to, from, next) => {
            checkAccessToken(to, from, next);
        },
    },
    {
        path: '/:code/results',
        name: 'Results',
        component: Results,
        beforeEnter: (to, from, next) => {
            checkAccessToken(to, from, next);
        },
    },
    {
        path: '/:code',
        name: 'Room',
        component: GameRoom,
        beforeEnter: (to, from, next) => {
            var code = window.location.href.split('/');
            code = code[code.length - 1];

            if (store.getters.getAccessToken) {
                var token = store.getters.getAccessToken;
            } else {
                localStorage.setItem('toRoom', code);
                next({ name: 'Login' });
                return;
            }

            axios
                .get('https://api.spotify.com/v1/me', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                })
                .then(function () {
                    next();
                    return;
                })
                .catch(function () {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    localStorage.setItem('toRoom', code);
                    next({ name: 'Login' });
                    return;
                });
        },
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound,
    },
    {
        path: '/:code/playlist',
        name: 'Playlist',
        component: Playlist,
        beforeEnter: (to, from, next) => {
            checkAccessToken(to, from, next);
        },
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;

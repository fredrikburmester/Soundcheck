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

const axios = require('axios');

import store from '../store/index'
import API from '../libs/api'

async function checkAccessToken(to, from, next) {
    var check = false
    if (localStorage.getItem('access_token')) {
        var token = localStorage.getItem('access_token');
    } else {
        return false;
    }

    await axios
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
            console.log("[1]")
            check = true;
        })
        .catch(function () {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_id');
            console.log("[2]")
            check = false;
        });

    return check;
}

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        beforeEnter: (to, from, next) => {
            if(!checkAccessToken()) {
                next({ name: 'Login' });
            } else {
                next()
            }
        },
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem('access_token')) {
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
            if(!checkAccessToken()) {
                next({ name: 'Login' });
            } else {
                next()
            }
        },
    },
    {
        path: '/create',
        name: 'Create',
        component: Create,
        beforeEnter: (to, from, next) => {
            if(!checkAccessToken()) {
                next({ name: 'Login' });
            } else {
                next()
            }
        },
    },
    {
        path: '/me',
        name: 'PreviousResults',
        component: PreviousResults,
        beforeEnter: (to, from, next) => {
            if(!checkAccessToken()) {
                next({ name: 'Login' });
            } else {
                next()
            }
        },
    },
    {
        path: '/:code/results',
        name: 'Results',
        component: Results,
        beforeEnter: (to, from, next) => {
            if(!checkAccessToken()) {
                next({ name: 'Login' });
            } else {
                next()
            }
        },
    },
    {
        path: '/:code',
        name: 'Room',
        component: GameRoom,
        beforeEnter: (to, from, next) => {
            var code = window.location.href.split('/');
            code = code[code.length - 1];

            if (localStorage.getItem('access_token')) {
                var token = localStorage.getItem('access_token');
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
            if(!checkAccessToken()) {
                next({ name: 'Login' });
            } else {
                next()
            }
        },
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

router.beforeEach((to, from, next) => {
    store.commit('updateLoading', true)
    next()
})
router.afterEach(() => {
    store.commit('updateLoading', false)
})

export default router;

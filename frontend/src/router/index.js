import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Join from '../views/Join.vue';
import Create from '../views/Create.vue';
import Room from '../views/Room.vue';
import LoginCallback from '../views/LoginCallback.vue';

const axios = require('axios');

function checkAccessToken(to, from, next) {
    if (localStorage.getItem('access_token')) {
        var token = localStorage.getItem('access_token');
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
        .then(function () {
            next();
            return;
        })
        .catch(function () {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
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
        path: '/:code',
        name: 'Room',
        component: Room,
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
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;

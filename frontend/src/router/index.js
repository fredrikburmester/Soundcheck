import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Join from "../views/Join.vue";
import Create from "../views/Create.vue";
import Room from "../views/Room.vue";
import LoginCallback from "../views/LoginCallback.vue";

const axios = require('axios');

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    beforeEnter: (to, from, next) => {
		if(localStorage.getItem('token')) {
			var token = localStorage.getItem('token')
		} else {
			next({ name: 'Login' })
		}

		axios.get('https://api.spotify.com/v1/me', {
			headers: {
				'Authorization': `Bearer ${token}`,
				"Accept": "application/json",
				"Content-Type": "application/json",
			}
		})
		.then(function (response) {
			console.log("Data ", response.data);
			console.log("Status ",response.status);
			next()
		})
		.catch(function (error) {
			console.log(error);
			// next({ name: 'Login' })
		})
		.then(function () {
			// always executed
		});
    }
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/logincallback",
    name: "LoginCallback",
    component: LoginCallback,
  },
  {
    path: "/join",
    name: "Join",
    component: Join,
  },
  {
    path: "/create",
    name: "Create",
    component: Create,
  },
  {
    path: "/:code",
    name: "Room",
    component: Room,
	beforeEnter: (to, from, next) => {
		if(localStorage.getItem('token')) {
			var token = localStorage.getItem('token')
		} else {
			next({ name: 'Login' })
		}

		axios.get('https://api.spotify.com/v1/me', {
			headers: {
				'Authorization': `Bearer ${token}`,
				"Accept": "application/json",
				"Content-Type": "application/json",
			}
		})
		.then(function (response) {
			console.log("Data ", response.data);
			console.log("Status ",response.status);
			next()
		})
		.catch(function (error) {
			console.log(error);
			// next({ name: 'Login' })
		})
		.then(function () {
			// always executed
		});
    }
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

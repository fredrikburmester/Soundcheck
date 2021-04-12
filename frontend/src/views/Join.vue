<template>
	<div class="join">
		<h1>Join Room</h1>
	    <router-link to="/">Home</router-link>
        <input v-model="code" placeholder="Enter Room Code...">
        <Button v-bind:buttonLink="code" buttonText="Join Room" />
	</div>
</template>

<script>
import Button from '../components/Button'

export default {
	name: "Join",
    data() {
        return {
            code: ''
        }
    },
	components: {
        Button
	},
	methods: {
    }
};
</script>

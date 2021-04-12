<template>
    <div>
        Nothing to see here
    </div>
</template>

<script>
export default {
    name: "LoginCallback",
    methods: {
        handleLoginCallback: function() {
            console.log(this.$route.query.access_token)
            
            let uri = window.location.href.split('=')[1]
            let token = uri.split('&')[0]

            localStorage.setItem('token', token)

            this.$router.push('/')
        } 
    },
    mounted() {
        this.handleLoginCallback()
    },
}
</script>
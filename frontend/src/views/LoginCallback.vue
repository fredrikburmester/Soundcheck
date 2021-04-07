<template>
    <div>
        Nothing to see here
    </div>
</template>

<script>
export default {
    name: "LoginCallback",
    methods: {
        handleLoginAuthentication: function() {
            console.log(this.$route.query.code)
            localStorage.setItem('token', this.$route.query.code)
            this.$router.push('/')
        } 
    },
    beforeMount() {
        this.handleLoginAuthentication()
    },
}
</script>
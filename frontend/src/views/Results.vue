<template>
    <div>
        <h1>Results</h1>
        {{ code }}
    </div>
</template>

<script>
export default {
    name: 'Results',
    data: function() {
        return {
            code: this.$route.params.code
        }
    }
}
</script>
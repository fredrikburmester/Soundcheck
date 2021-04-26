<template>
    <div class="playerAvatar">
        <div>
            <img class="circle">
        </div>
        <div class="name">
            Hej
        </div>
    </div>
</template>

<script>
export default {
    name: 'PlayerAvatar',
    props: {
        trackid: {
            type: String,
        },
        guess: {
            type: String,
            default: '#FFF',
        },
        answer: {
            type: Boolean,
            default: false,
        }
    },
    data() {
        return {

        };
    },
    computed: {

    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

</style>

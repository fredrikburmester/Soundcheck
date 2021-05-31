/* 
Dynamic progressbar, active during each game round. 
Takes the progress time as argument. 

Currently not implemented in game functionality except design. 
*/

<template>
    <div id="container" />
</template>

<script>
var ProgressBar = require('progressbar.js');
export default {
    name: 'ProgressBar',
    components: {},
    props: {
        time: {
            type: Number,
            default: 0,
        },
    },
    data() {
        return {
            time_: this.time,
        };
    },
    mounted: function () {
        var line = new ProgressBar.Line('#container', {
            strokeWidth: 10,
            trailWidth: 10,
        });
        line.set(this.time_);
        var duration = (30 - 30 * this.time_) * 1000;
        line.animate(1, {
            duration: duration,
            color: '#1DB954',
            trailColor: '#eee',
            from: { color: '#1DB954' },
            to: { color: '#CD1A2B' },
            step: (state, bar) => {
                bar.path.setAttribute('stroke', state.color);
            },
        });
    },
};
</script>

<style scoped></style>

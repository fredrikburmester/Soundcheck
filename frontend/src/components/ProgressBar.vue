<template>
    <div id="container" />
</template>

<script>
var ProgressBar = require('progressbar.js');
export default {
    name: 'ProgressBar',
    components: {},

    mounted: function () {
        var line = new ProgressBar.Line('#container');
        line.animate(1, {
            duration: 30000,
            color: '#1DB954',
            trailColor: '#eee',
            trailWidth: 1,
            svgStyle: { width: '100%', height: '100%' },
            from: { color: '#1DB954' },
            to: { color: '#CD1A2B' },
            step: (state, bar) => {
                bar.path.setAttribute('stroke', state.color);
            },
        });
        console.log(line);
    },
};
</script>

<style scoped>
#container > svg {
    height: 10px;
}
</style>

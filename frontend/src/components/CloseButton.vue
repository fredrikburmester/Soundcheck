/* 
Simple close icon, no logic here.
*/

<template>
    <div>
        <div
            id="line1"
            class="line"
        />
        <div
            id="line2"
            class="line"
        />
    </div>
</template>

<script>
export default {
    name: 'CloseButton'
}
</script>

<style scoped>
    .line {
        background-color: gray;
        height: 3px;
        width: 25px;
        cursor: pointer;
    }
        #line1 {
        transform: translateY(3px) rotate(45deg);
    }
        #line2 {
        transform: rotate(-45deg);
    }
</style>

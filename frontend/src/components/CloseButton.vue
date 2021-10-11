/* 
Simple close icon, no logic here.
*/

<template>
    <div class="close-button-component">
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
    .close-button-component{
        width: 30px;
        height: 30px;
        cursor: pointer;
        padding-top: 5px;
        padding-left: 5px
    }
    .line {
        background-color: gray;
        height: 3px;
        width: 25px;
        position: relative
    }
        #line1 {
        transform: translateY(3px) rotate(45deg);
    }
        #line2 {
        transform: rotate(-45deg);
    }
</style>

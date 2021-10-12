/* 
Simple close icon, no logic here.
*/

<template>
    <div class="close-button-component">
            <div
                id="line1"
                class="line"
                :style="colorStyles"
            />
            <div
                id="line2"
                class="line"
                :style="colorStyles"
            />
    </div>
</template>

<script>
export default {
    name: 'CloseButton',
    props: {
        color: {
            type: String,
            default: 'gray'
        }
    },
    computed: {
        colorStyles() {
            if(this.color == "red") {
                return {
                    'background-color': "red"
                };
            } else {
                return {
                    "background-color": "gray"
                }
            }
        }
    }
}
</script>

<style scoped>
    .close-button-component{
        width: 25px;
        height: 25px;
        cursor: pointer;
        padding: 10px
    }
    .line {
        background-color: gray;
        height: 3px;
        width: 25px;
        position: absolute;
    }
    #line1 {
        margin-top: 10px;
        transform: translateY(0px) rotate(45deg);
    }
        #line2 {
            margin-top: 0;
        transform: translateY(10px) rotate(-45deg);
    }
</style>

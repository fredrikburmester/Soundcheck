<template>
    <div>
        <select v-model="selectedValue" class="select" @change="emitValueToParent">
            <option v-for="value in list" :key="value.key || value" :value="value.key || value">
                {{ value.value || value }}
            </option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'Select',
    props: {
        list: {
            type: Array,
            default: () => []
        },
        defaultValue: {
            type: String,
            default: 'Please select a value'
        }
    },
    emits: ['selected'],
    data() {
        return {
            selectedValue: this.defaultValue.key || this.defaultValue
        }
    },
    mounted: function() {
        // console.log(typeof(this.list))
    },
    methods: {
        emitValueToParent() {
            this.$emit('selected', this.selectedValue)
        }
    }
}
</script>

<style scoped>
.select {
    background-color: rgb(255, 255, 255);
    font-weight: 400;
    border: 1px solid #000;
    border-radius: 100px;
    height: 47px;
    text-align-last: center;
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    margin-bottom: 10px;

    /* Width and center*/ 
    width: 100%;
    max-width: 340px;
    /* --------------- */ 

    -webkit-appearance: none;
}
</style>
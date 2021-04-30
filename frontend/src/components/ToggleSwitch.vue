<template>
    <div class="genre">
        <p class="p-off">
            Off
        </p>
        <label class="switch">
            <input
                type="checkbox"
                @click="check"
            >
            <span class="slider" />
        </label>
        <p class="p-on">
            On
        </p>
    </div>
</template>

<script>
export default {
    name: 'ToggleSwitch',
    emits: ['clicked'],
    data: function () {
        return {
            is_checked: false,
        };
    },
    methods: {
        check() {
            this.is_checked = !this.is_checked;
            this.$emit('clicked', this.is_checked);
        },
    },
};
</script>

<style scoped>
.switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #cd1a2b;
    -webkit-transition: 0.4s;
    transition: 0.4s;
    border-radius: 34px;
}

.slider:before {
    position: absolute;
    content: '';
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: 0.4s;
    transition: 0.4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: #1db954;
}

input:focus + .slider {
    box-shadow: 0 0 1px #1db954;
}

input:checked + .slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
}
.genre {
    position: relative;
    display: inline-flex;
    margin-bottom: 20px;
}
.p-off {
    margin: 8px 15px 0 15px;
}
.p-on {
    margin: 8px 15px 0 15px;
}
</style>

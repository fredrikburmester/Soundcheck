import { createStore } from 'vuex';

export default createStore({
    state: {
        roomCode: '',
    },
    mutations: {
        updateRoomCode(state, value) {
            state.roomCode = value.toUpperCase();
        },
    },
    actions: {},
    modules: {},
});

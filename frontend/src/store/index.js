import { createStore } from 'vuex';

export default createStore({
    state: {
        roomCode: '',
        error: '',
    },
    mutations: {
        updateRoomCode(state, value) {
            state.roomCode = value.toUpperCase();
        },
        updateError(state, value) {
            state.error = value;
        },
    },
    actions: {},
    modules: {},
});

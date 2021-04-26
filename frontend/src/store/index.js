import { createStore } from 'vuex';

export default createStore({
    state: {
        roomCode: '',
        error: '',
        players_guessed: [],
    },
    mutations: {
        updateRoomCode(state, value) {
            state.roomCode = value.toUpperCase();
        },
        updateError(state, value) {
            state.error = value;
        },
        updatePlayersGuessed(state, value) {
            for (let i of state.players_guessed) {
                if (i == value) {
                    return;
                }
            }
            state.players_guessed.push(value.toString());
        },
        clearPlayersGuessed(state) {
            state.players_guessed = [];
        },
    },
    actions: {},
    modules: {},
});

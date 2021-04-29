import { createStore } from 'vuex';

export default createStore({
    state: {
        roomCode: '',
        error: '',
        players_guessed: [],
        genre: false,
        no_songs: '1',
        time_range: 'short_term',
    },
    mutations: {
        updateRoomCode(state, value) {
            state.roomCode = value.toUpperCase();
        },
        updateError(state, value) {
            state.error = value;
        },
        updatePlayersGuessed(state, value) {
            state.players_guessed = value;
        },
        clearPlayersGuessed(state) {
            state.players_guessed = [];
        },
        update_genre(state, value) {
            state.genre = value;
        },
        update_no_songs(state, value) {
            state.no_songs = value;
        },
        update_time_range(state, value) {
            state.time_range = value;
        },
    },
    actions: {},
    modules: {},
});

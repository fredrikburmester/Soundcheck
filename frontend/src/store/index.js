import { createStore } from 'vuex';

export default createStore({
    state: {
        roomCode: '',
        error: '',
        genre: false,
        no_songs: '1',
        time_range: 'short_term',
        username: ''
    },
    mutations: {
        updateRoomCode(state, value) {
            state.roomCode = value.toUpperCase();
        },
        updateError(state, value) {
            state.error = value;
        },
    },
    actions: {
    },
    modules: {},
    getters: {
        getUsername(state) {
            if(!state.username || state.username.length < 1) {
                state.username = localStorage.getItem('user_id')
            }
            return state.username
        }
    }
});

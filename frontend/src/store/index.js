import { createStore } from 'vuex';

export default createStore({
    state: {
        roomCode: '',
        error: '',
        genre: false,
        no_songs: '1',
        time_range: 'short_term',
        tracksForPlaylist: [],
        nrOfTrackstoAdd: 0,
        noTracksFound: false,
        user_id: null,
        loading: false,
        accessToken: null,
        sid: null,
    },
    mutations: {
        setUserId(state, value) {
            localStorage.setItem('user_id', value)
            state.user_id = value
        },
        setSid(state, value) {
            localStorage.setItem('sid', value)
            state.sid = value
        },
        setAccessToken(state, value) {
            localStorage.setItem('access_token', value)
            state.accessToken = value
        },
        updateRoomCode(state, value) {
            state.roomCode = value.toUpperCase();
        },
        updateLoading(state, value) {
            state.loading = value;
        },
        updateError(state, value) {
            state.error = value;
        },
        addTrack(state, value){
            if(!state.tracksForPlaylist.includes(value)){
                state.tracksForPlaylist.push([value, true]);
                state.nrOfTrackstoAdd +=1;
            }
        },
        //used to mark which tracks a user wants to save to a playlist
        updateTracksForPlaylist(state, value){
            if(state.tracksForPlaylist[value][1]){
                state.tracksForPlaylist[value][1] = false;
                state.nrOfTrackstoAdd -= 1;
            }
            else{
                state.tracksForPlaylist[value][1] = true;
                state.nrOfTrackstoAdd += 1;
            }
        },
        //Needed to avoid tracks loading multiple times when reentering /playlist route from /results
        clearTracksForPlaylist(state){
            state.nrOfTrackstoAdd = 0;
            state.tracksForPlaylist = [];
        },
        updateNoTracksModal(state, value){
            state.noTracksFound = value;
        },
        clearCredentials(state) {
            state.user_id = null
            state.accessToken = null
            state.sid = null
            state.error = ''

            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_id');
            localStorage.removeItem('sid');
        }

    },
    actions: {
    },
    modules: {},
    getters: {
        getUserId(state) {
            if(!state.user_id) {
                state.user_id = localStorage.getItem('user_id');
            }
            return state.user_id
        },
        getAccessToken(state){
            if(!state.accessToken){
                state.accessToken = localStorage.getItem('access_token');
            }
            return state.accessToken;
        },
        getSid(state){
            if(!state.sid){
                state.sid = localStorage.getItem('sid');
            }
            return state.sid;
        },
        getLoadingStatus: state => state.loading,
    }
});

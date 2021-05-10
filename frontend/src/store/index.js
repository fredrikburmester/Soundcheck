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
    },
    mutations: {
        updateRoomCode(state, value) {
            state.roomCode = value.toUpperCase();
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
                console.log(state.nrOfTrackstoAdd)
            }
            else{
                state.tracksForPlaylist[value][1] = true;
                state.nrOfTrackstoAdd += 1;
                console.log(state.nrOfTrackstoAdd)
            }
        },
        //Needed to avoid tracks loading multiple times when reentering /playlist route from /results
        clearTracksForPlaylist(state){
            state.nrOfTrackstoAdd = 0;
            state.tracksForPlaylist = [];
        }
    },
    actions: {},
    modules: {},
});

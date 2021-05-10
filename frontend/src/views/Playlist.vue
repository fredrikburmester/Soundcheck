<template>
    <div> 
        <div :class="{ dim: (existingPlaylist || newPlaylist)}">
            <div><h3>Tap to select/deselect tracks</h3></div>
            <div class="track-list-container">
                <div v-for="track in tracks" :key="track" :class="{ iconlist: track[1]}">
                    <TrackIcon
                        :trackid="track[0]"
                        @click="selectTrack(tracks.indexOf(track))"
                    />
                </div>
            </div>
            <p v-if="nrOfTrackstoAdd>1">Add {{ nrOfTrackstoAdd }} tracks to:</p>
            <p v-else-if="nrOfTrackstoAdd==1">Add {{ nrOfTrackstoAdd }} tracks to:</p>
            <p v-else>Select tracks to add!</p>
            <Button
                button-text="Existing playlist"
                @click="existingPlaylistToggle()"
            />
            <Button
                button-text="New playlist"
                @click="newPlaylistToggle()"
            />
        </div>
        <div v-if="existingPlaylist" class="playlist-modal-view">
            <span class="close" @click="close(existingPlaylist)">&times;</span>
            <div class="button-container">
                <select v-model="selectedPlaylist" class="drop-down" aria-placeholder="Choose a playlist">
                    <option value="" disabled hidden>Select a playlist</option>
                    <option v-for="playlist in userPlaylists" :key="playlist" :value="playlist[1]">
                        {{ playlist[0] }}
                    </option>
                </select> 
                <Button class="playlist-modal-button"
                    button-text="Confirm"
                    @click="addTracksExisting()"
                />
            </div>
        </div>
        <div v-if="newPlaylist" class="playlist-modal-view">
            <span class="close" @click="close(newPlaylist)">&times;</span>
            <div class="button-container">
                <input
                    id="input"
                    v-model="newPlaylistName"
                    type="text"
                    placeholder="Enter a name"
                    autocomplete="off"


                >
                <Button class="playlist-modal-button"
                button-text="Confirm"
                @click="addTracksNew()"
                />
            </div>
        </div>
    </div>
</template>

<script>

import Button from '../components/Button';
import TrackIcon from '../components/TrackIcon';
const axios = require('axios');

export default {
    name: 'Playlist',
    components:{
        Button,
        TrackIcon,
    },
    data: function () {
        return {
            code: this.$route.params.code,
            tracks: this.$store.state.tracksForPlaylist,
            userPlaylists: [],
            selectedPlaylist: '',
            existingPlaylist: false,
            newPlaylist: false,
            nrOfTrackstoAdd: this.$store.state.nrOfTrackstoAdd,


        };
    },
    mounted(){
        var token = localStorage.getItem('access_token');
        var user_id = localStorage.getItem('user_id');
        var self = this;
        axios
            .get(
                `https://api.spotify.com/v1/users/${user_id}/playlists`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                }
            ).then(function (response) {
                for(let item of response.data.items){
                    //allow user to modify their own + collaborative playlists
                    if((item.owner.id == user_id) || (item.owner.id != user_id && item.collaborative == true)){
                        self.userPlaylists.push([item.name, item.id])
                    }
                    //TODO sort data
                }
            });
    },
    methods:{
        log(){
            //console.log(this.tracks);
            //console.log(this.userPlaylists);  
            console.log(this.selectedPlaylist)
        },
        selectTrack(index){
            //change boolean value associated with track in store
            this.$store.commit('updateTracksForPlaylist', index)
            this.nrOfTrackstoAdd = this.$store.state.nrOfTrackstoAdd;
        },
        //the following three methods are used to hide/show modal
        existingPlaylistToggle(){
            this.existingPlaylist = true;
        },
        newPlaylistToggle(){
            this.newPlaylist = true;
        },
        close(){
            this.existingPlaylist = false;
            this.newPlaylist = false;
        },
        addTracksExisting(){
            console.log(this.selectedPlaylist)
            let tracksToSend = [];
            console.log(this.tracks)
            for(let track of this.tracks){
                if(track[1]){
                    tracksToSend.push(track[0])
                }
            }
            this.$socket.client.emit('addToPlaylist', {
                sid: localStorage.getItem('sid'),
                access_token: localStorage.getItem('access_token'),
                user_id: localStorage.getItem('user_id'),
                playlist_id: this.selectedPlaylist,
                tracksForPlaylist: tracksToSend,
            });

        },
        addTracksNew(){
            console.log(this.newPlaylistName)
            let tracksToSend = [];
            for(let track of this.tracks){
                if(track[1]){
                    tracksToSend.push(track[0])
                }
            }
            console.log(tracksToSend)
            this.$socket.client.emit('createPlaylist', {
                sid: localStorage.getItem('sid'),
                access_token: localStorage.getItem('access_token'),
                user_id: localStorage.getItem('user_id'),
                name: this.newPlaylistName,
                tracksForPlaylist: tracksToSend,
            });
        }

    }

}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.iconlist{
    background: linear-gradient(90deg, rgba(25,20,20,1) 0%, rgba(29,185,84,1) 100%);
    border-radius: 0 40px 40px 0;
    margin-right: 5px;
    }
.playlist-modal-view{
    z-index: 2;
    position: absolute;
    background-color: rgba(255, 255, 255, .15);  
    backdrop-filter: blur(10px);
    top: 50%;
    left: 50%;
    max-width: 300px;
    max-height: 200px;
    min-height: 200px;
    height: 100vw;
    width: 100vw;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    border-radius: 10px;
    }
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  margin-right: 10px;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.dim{
    opacity: 0.5;
    pointer-events: none;
}
.drop-down{
    background-color: #fff;
    font-weight: 400;
    max-width: 300px;
    width: 82vw;
    height: 47px;
    text-align-last: center;
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    letter-spacing: 3px;
    border: 1px solid #000;
    border-radius: 100px;
    cursor: pointer;
    margin-bottom: 20px;
}
.playlist-modal-button{
    max-width: 260px;
    width: 70vw;
}
input {
    display: inline-block;
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    letter-spacing: 3px;
    max-width: 260px;
    background-color: white;
    border-radius: 100px;
    border-style: none;
    padding: 15px 20px 15px 20px;
    width: 70vw;
    margin-bottom: 10px;
    cursor: pointer;
    text-align: center;
}
.button-container{
    margin-top: 45px;
}
.track-list-container{
    height: calc(100vh - 220px);
    overflow-y: scroll;
    overflow-x: hidden;
    border-top: 1px gray solid;
    border-bottom: 1px gray solid

}
</style>
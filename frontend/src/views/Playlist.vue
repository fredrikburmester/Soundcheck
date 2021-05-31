/*
Page for saving game tracks to a user playlist in spotify. 
 */
<template>
    <div>
        <transition name="fade" mode="out-in">
            <div v-if="loading">
                <Loader />
            </div>
        </transition>
        <transition name="fade" mode="out-in">
            <div> 
                <div :style="gridStyle" :class="(existingPlaylist || newPlaylist) ? 'dim grid' : 'grid'">
                    <div>
                        <h3>Tap to select/deselect</h3>
                        <div class="close-button">
                            <CloseButton 
                                @click="goBack()"
                            />
                        </div>
                    </div>
                    <div class="track-list-container">
                        <div v-for="track in tracks" :key="track" :class="{ iconlist: track[1]}">
                            <TrackIcon
                                :trackid="track[0]"
                                @click="selectTrack(tracks.indexOf(track))"
                            />
                        </div>
                    </div>
                    <div class="buttons">
                        <p v-if="nrOfTrackstoAdd>1">
                            Add {{ nrOfTrackstoAdd }} tracks to:
                        </p>
                        <p v-else-if="nrOfTrackstoAdd==1">
                            Add {{ nrOfTrackstoAdd }} track to:
                        </p>
                        <p v-else>
                            Select tracks to add!
                        </p>
                        <Button
                            button-text="Existing playlist"
                            :disabled="nrOfTrackstoAdd == 0 ? true : false"
                            @click="existingPlaylistToggle()"
                        />
                        <Button
                            button-text="New playlist"
                            :disabled="nrOfTrackstoAdd == 0 ? true : false"
                            @click="newPlaylistToggle()"
                        />
                    </div>
                </div>
                <div v-if="existingPlaylist" class="playlist-modal-view">
                    <span class="close" @click="close(existingPlaylist)">&times;</span>
                    <p v-if="nrOfTrackstoAdd > 1" style="margin: 10px 0 0 0;">
                        Add tracks to existing playlist
                    </p>
                    <p v-else style="margin: 10px 0 0 0;">
                        Add track to existing playlist
                    </p>
                    <div class="button-container-modal">
                        <select v-model="selectedPlaylist" class="drop-down" aria-placeholder="Choose a playlist">
                            <option value="" disabled hidden>
                                Select a playlist
                            </option>
                            <option v-for="playlist in userPlaylists" :key="playlist" :value="playlist[1]">
                                {{ playlist[0] }}
                            </option>
                        </select> 
                        <Button
                            class="playlist-modal-button"
                            button-text="Confirm"
                            :disabled="selectedPlaylist ? false : true"
                            @click="addTracksExisting()"
                        />
                    </div>
                </div>
                <div v-if="newPlaylist" class="playlist-modal-view">
                    <span class="close" @click="close(newPlaylist)">&times;</span>
                    <p v-if="nrOfTrackstoAdd > 1">
                        Add tracks to new playlist
                    </p>
                    <p v-else>
                        Add track to new playlist
                    </p>
                    <div class="button-container-modal">
                        <input
                            id="input"
                            v-model="newPlaylistName"
                            type="text"
                            placeholder="Enter a name"
                            autocomplete="off"
                        >
                        <Button
                            class="playlist-modal-button"
                            button-text="Confirm"
                            @click="addTracksNew()"
                        />
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>

import Button from '../components/Button';
import TrackIcon from '../components/TrackIcon';
import Loader from '../components/Loader';
import CloseButton from '../components/CloseButton';
const axios = require('axios');

export default {
    name: 'Playlist',
    components:{
        Button,
        TrackIcon,
        Loader,
        CloseButton,
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
            loading: false,
            newPlaylistName: ''
        };
    },
    sockets: {
        // If the playlist has been created close modals
        playlistCreated() {
            this.loading = false
            this.existingPlaylist = false
            this.newPlaylist = false
        }
    },
    computed: {
        gridStyle() {
            return {
                'height': `${window.innerHeight}px`,
                'width': `${window.innerWidth}px`
            }
        },    
    },
    mounted(){
        // if user refreshes the page, the "tracks" variable in the store will be empty and /playlist will have nothing to display.
        if(this.tracks.length == 0){
            // if this is the case, push user back to /results, in order to force an update in the store
            this.goBack();
        }

        var token = this.$store.getters.getAccessToken;
        var user_id = this.$store.getters.getUserId;
        var self = this;

        // gather user playlists from spotify api
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
        goBack(){
            this.$router.push(`/${this.code}/results`);
        },
        selectTrack(index){
            //change boolean value associated with track in store
            this.$store.commit('updateTracksForPlaylist', index)
            this.nrOfTrackstoAdd = this.$store.state.nrOfTrackstoAdd;
        },
        //the following three methods are used to hide/show modal
        existingPlaylistToggle(){
            if(this.nrOfTrackstoAdd != 0) {
                this.existingPlaylist = true;
            }
        },
        newPlaylistToggle(){
            if(this.nrOfTrackstoAdd != 0) {
                this.newPlaylist = true;
            }
        },
        close(){
            this.existingPlaylist = false;
            this.newPlaylist = false;
        },
        // add the tracks to an existing playlist of user choice
        addTracksExisting(){
            let tracksToSend = [];
            for(let track of this.tracks){
                if(track[1]){
                    tracksToSend.push(track[0])
                }
            }
            this.loading = true
            this.$socket.client.emit('addToPlaylist', {
                sid: this.$store.getters.getSid,
                access_token: this.$store.getters.getAccessToken,
                user_id: this.$store.getters.getUserId,
                playlist_id: this.selectedPlaylist,
                tracksForPlaylist: tracksToSend,
            });

        },
        // add tracks to a new playlist with a name defined by the user
        addTracksNew(){
            let tracksToSend = [];
            for(let track of this.tracks){
                if(track[1]){
                    tracksToSend.push(track[0])
                }
            }
            this.loading = true
            this.$socket.client.emit('createPlaylist', {
                sid: this.$store.getters.getSid,
                access_token: this.$store.getters.getAccessToken,
                user_id: this.$store.getters.getUserId,
                name: this.newPlaylistName.length > 0 ? this.newPlaylistName : `Soundcheck - ${this.code}`,
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
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s ease;
  -webkit-transition: opacity .5s ease;
  -moz-transition: opacity .5s ease;
  -o-transition: opacity .5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.grid {
    display: grid;
    grid-template-rows: 65px auto 200px;
}
.playlist-modal-view{
    z-index: 2;
    position: absolute;
    background-color: rgba(255, 255, 255, .15);  
    backdrop-filter: blur(10px);
    top: 50%;
    left: 50%;
    width: 300px;
    height: 200px;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    border-radius: 10px;
    padding: 10px;
}
.buttons {
    margin: 0 2rem 0 2rem;
}
.close {
    color: #aaa;
    font-size: 28px;
    font-weight: bold;
    position: absolute;
    right: 20px;
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
    max-width: 280px;
    width: 82vw;
    height: 47px;
    text-align-last: center;
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    letter-spacing: 3px;
    border-radius: 100px;
    cursor: pointer;
    margin-bottom: 20px;
}
.playlist-modal-button{
    max-width: 240px;
    width: 70vw;
}
input {
    display: inline-block;
    font-size: 15px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500;
    letter-spacing: 3px;
    max-width: 240px;
    background-color: white;
    border-radius: 100px;
    border-style: none;
    padding: 15px 20px 15px 20px;
    width: 70vw;
    margin-bottom: 10px;
    cursor: pointer;
    text-align: center;
}
.button-container-modal{
    margin-top: 20px;
}
.track-list-container{
    overflow-y: scroll;
    overflow-x: hidden;
    border-top: 1px gray solid;
    border-bottom: 1px gray solid;
    margin:  0 2rem 0 2rem;
}
.close-button {
    position: fixed;
    top: 25px;
    right: 1rem;
}
</style>